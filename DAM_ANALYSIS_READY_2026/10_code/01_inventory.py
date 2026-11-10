#!/usr/bin/env python3
"""
Phase 1: Dataset Inventory and Structural Audit
==============================================
Audits every input CSV in dam_output/master/ in strictly read-only mode.
Computes row counts, column inventories, missingness, duplicate checks,
and structural integrity diagnostics.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SOURCE_DIR = PROJECT_ROOT / "dam_output" / "master"
TARGET_DIR = PROJECT_ROOT / "DAM_ANALYSIS_READY_2026" / "01_inventory"

INDIVIDUAL_FILES = [
    "DAM_ONION_LOCAL_2010_2026.csv",
    "DAM_ONION_IMPORTED_2010_2026.csv",
    "DAM_ONION_NEW_2010_2026.csv",
    "DAM_POTATO_LOCAL_OLD_2010_2026.csv",
    "DAM_POTATO_LOCAL_2010_2026.csv",
    "DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv",
    "DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv",
    "DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv",
    "DAM_POTATO_HOLLAND_RED_2010_2026.csv",
    "DAM_SWEET_POTATO_2010_2026.csv",
    "DAM_POTATOES_IMPORTED_2010_2026.csv"
]
COMBINED_FILE = "DAM_ALL_11_COMMODITIES_2010_2026.csv"
ALL_FILES = INDIVIDUAL_FILES + [COMBINED_FILE]


def run_inventory() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    print("Executing Phase 1: Dataset Inventory & Structural Audit...")

    dataset_inv = []
    column_inv = []
    duplicate_rows = []
    missingness_rows = []
    structural_issues = []

    for fn in ALL_FILES:
        fp = SOURCE_DIR / fn
        if not fp.exists():
            raise FileNotFoundError(f"Source file not found: {fp}")

        df = pd.read_csv(fp)
        is_combined = (fn == COMBINED_FILE)

        # Basic metadata
        n_rows = len(df)
        n_cols = len(df.columns)
        n_mkts = df['market_id'].nunique()
        n_comms = df['commodity_id'].nunique()
        comm_names = "; ".join(sorted(df['commodity_name_en'].dropna().unique().tolist()))
        comm_ids = "; ".join(map(str, sorted(df['commodity_id'].dropna().unique().tolist())))
        
        # Dates
        dates = df['price_date'].dropna()
        n_dates = dates.nunique()
        first_date = str(dates.min()) if not dates.empty else ""
        last_date = str(dates.max()) if not dates.empty else ""
        years = "; ".join(map(str, sorted(df['price_year'].dropna().unique().tolist())))
        months = "; ".join(map(str, sorted(df['price_month'].dropna().unique().tolist())))

        # Duplicates
        dup_exact = df.duplicated().sum()
        dup_mcd = df.duplicated(subset=['market_id', 'commodity_id', 'price_date']).sum()
        dup_cpi = df.duplicated(subset=['market_id', 'commodity_id', 'cpi_market_commodity_price_id']).sum() if 'cpi_market_commodity_price_id' in df.columns else 0

        dataset_inv.append({
            "filename": fn,
            "is_combined_file": is_combined,
            "row_count": n_rows,
            "column_count": n_cols,
            "unique_markets": n_mkts,
            "unique_commodities": n_comms,
            "commodity_ids": comm_ids,
            "commodity_names": comm_names,
            "unique_dates": n_dates,
            "first_date": first_date,
            "last_date": last_date,
            "unique_years": years,
            "unique_months": months,
            "exact_duplicate_rows": dup_exact,
            "duplicate_market_commodity_date": dup_mcd,
            "duplicate_market_commodity_cpi_id": dup_cpi
        })

        if dup_exact > 0 or dup_mcd > 0 or dup_cpi > 0:
            dup_subset = df[df.duplicated(subset=['market_id', 'commodity_id', 'price_date'], keep=False)]
            for _, r in dup_subset.iterrows():
                duplicate_rows.append({
                    "filename": fn,
                    "market_id": r.get("market_id"),
                    "market_name": r.get("market_name"),
                    "commodity_id": r.get("commodity_id"),
                    "commodity_name_en": r.get("commodity_name_en"),
                    "price_date": r.get("price_date"),
                    "cpi_market_commodity_price_id": r.get("cpi_market_commodity_price_id")
                })

        # Column level inventory & missingness
        for col in df.columns:
            s = df[col]
            null_cnt = s.isnull().sum()
            null_pct = round((null_cnt / n_rows) * 100.0, 4) if n_rows > 0 else 0.0
            n_uniq = s.nunique(dropna=True)
            dtype_str = str(s.dtype)
            is_const = (n_uniq == 1)
            is_empty = (null_cnt == n_rows)

            column_inv.append({
                "filename": fn,
                "column_name": col,
                "data_type": dtype_str,
                "non_null_count": n_rows - null_cnt,
                "null_count": null_cnt,
                "null_percentage": null_pct,
                "unique_values_count": n_uniq,
                "is_constant_column": is_const,
                "is_empty_column": is_empty
            })

            missingness_rows.append({
                "filename": fn,
                "column_name": col,
                "total_rows": n_rows,
                "missing_count": null_cnt,
                "missing_pct": null_pct,
                "status": "COMPLETELY_EMPTY" if is_empty else ("PARTIAL_MISSING" if null_cnt > 0 else "COMPLETE")
            })

            # Check structural issues
            if is_empty:
                structural_issues.append({
                    "filename": fn,
                    "issue_category": "EMPTY_COLUMN",
                    "column_or_field": col,
                    "severity": "WARNING",
                    "detail": f"Column '{col}' is 100% missing ({null_cnt}/{n_rows} rows)."
                })
            elif is_const and col not in ['commodity_id', 'commodity_name_en', 'commodity_name_bn', 'commodity_group_id', 'commodity_group_name_en', 'commodity_sub_group_id', 'commodity_sub_group_name_en', 'source_api']:
                structural_issues.append({
                    "filename": fn,
                    "issue_category": "CONSTANT_COLUMN",
                    "column_or_field": col,
                    "severity": "INFO",
                    "detail": f"Column '{col}' has only 1 unique value across all rows: {s.dropna().iloc[0] if not s.dropna().empty else 'None'}"
                })

        # Check date validity
        parsed_dates = pd.to_datetime(df['price_date'], errors='coerce')
        invalid_dates = parsed_dates.isnull().sum()
        if invalid_dates > 0:
            structural_issues.append({
                "filename": fn,
                "issue_category": "INVALID_DATE_FORMAT",
                "column_or_field": "price_date",
                "severity": "ERROR",
                "detail": f"Found {invalid_dates} unparseable dates in {fn}."
            })

    # Save all tables
    pd.DataFrame(dataset_inv).to_csv(TARGET_DIR / "dataset_inventory.csv", index=False)
    pd.DataFrame(column_inv).to_csv(TARGET_DIR / "column_inventory.csv", index=False)
    pd.DataFrame(duplicate_rows).to_csv(TARGET_DIR / "duplicate_report.csv", index=False)
    pd.DataFrame(missingness_rows).to_csv(TARGET_DIR / "missingness_report.csv", index=False)
    pd.DataFrame(structural_issues).to_csv(TARGET_DIR / "structural_issues.csv", index=False)

    print(f"Phase 1 complete. Saved inventory and structural reports to {TARGET_DIR}")


if __name__ == "__main__":
    run_inventory()
