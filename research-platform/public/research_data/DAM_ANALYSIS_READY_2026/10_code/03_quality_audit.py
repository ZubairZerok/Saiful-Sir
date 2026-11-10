#!/usr/bin/env python3
"""
Phase 3 & 4: Numerical Quality Audit and Extreme Observation Forensics
======================================================================
Performs row-level statistical and structural audits on all 3,348 observations.
Generates exhaustive flags, checks raw JSON payloads for extreme values,
and documents all quality anomalies without modifying source data.
Outputs:
- 03_quality_audit/row_level_quality_flags.csv
- 03_quality_audit/quality_summary.csv
- 03_quality_audit/outlier_report.csv
- 03_quality_audit/range_consistency_report.csv
- 03_quality_audit/zero_price_report.csv
- 03_quality_audit/impossible_value_report.csv
- 03_quality_audit/extreme_observation_forensics.csv
"""

from __future__ import annotations

import os
import sys
import json
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SOURCE_DIR = PROJECT_ROOT / "dam_output" / "master"
RAW_JSON_DIR = PROJECT_ROOT / "dam_output" / "raw_json"
TARGET_DIR = PROJECT_ROOT / "DAM_ANALYSIS_READY_2026" / "03_quality_audit"

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


def run_quality_audit() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    print("Executing Phase 3 & 4: Quality Audit and Forensics...")

    # Load all observations
    dfs = []
    for fn in INDIVIDUAL_FILES:
        d = pd.read_csv(SOURCE_DIR / fn)
        d['source_filename'] = fn
        dfs.append(d)
    df = pd.concat(dfs, ignore_index=True)
    n_total = len(df)

    # 1. Flag Definitions
    # Negative prices
    has_neg_w = (df['wholesale_price_low'] < 0) | (df['wholesale_price_high'] < 0) | (df['wholesale_price_avg'] < 0)
    has_neg_r = (df['retail_price_low'] < 0) | (df['retail_price_high'] < 0) | (df['retail_price_avg'] < 0)
    flag_negative_price = has_neg_w | has_neg_r

    # Zero prices
    w_zero = (df['wholesale_price_low'] == 0) & (df['wholesale_price_high'] == 0)
    r_zero = (df['retail_price_low'] == 0) & (df['retail_price_high'] == 0)
    flag_all_price_zero = (w_zero & r_zero)
    flag_wholesale_zero = (df['wholesale_price_low'] == 0) | (df['wholesale_price_high'] == 0)
    flag_retail_zero = (df['retail_price_low'] == 0) | (df['retail_price_high'] == 0)
    flag_any_price_zero = (flag_wholesale_zero | flag_retail_zero | (df['wholesale_price_avg'] == 0) | (df['retail_price_avg'] == 0))

    # Inversions (low > high)
    flag_wholesale_raw_inverted = (df['wholesale_price_low'] > df['wholesale_price_high'])
    flag_retail_raw_inverted = (df['retail_price_low'] > df['retail_price_high'])
    flag_wholesale_adj_inverted = (df['adjusted_wholesale_price_low'] > df['adjusted_wholesale_price_high'])
    flag_retail_adj_inverted = (df['adjusted_retail_price_low'] > df['adjusted_retail_price_high'])
    flag_any_inversion = flag_wholesale_raw_inverted | flag_retail_raw_inverted | flag_wholesale_adj_inverted | flag_retail_adj_inverted

    # Averages outside range
    flag_wholesale_avg_outside_raw = (df['wholesale_price_avg'] < df['wholesale_price_low']) | (df['wholesale_price_avg'] > df['wholesale_price_high'])
    flag_wholesale_avg_outside_adj = (df['wholesale_price_avg'] < df['adjusted_wholesale_price_low']) | (df['wholesale_price_avg'] > df['adjusted_wholesale_price_high'])
    flag_retail_avg_outside_raw = (df['retail_price_avg'] < df['retail_price_low']) | (df['retail_price_avg'] > df['retail_price_high'])
    flag_retail_avg_outside_adj = (df['retail_price_avg'] < df['adjusted_retail_price_low']) | (df['retail_price_avg'] > df['adjusted_retail_price_high'])

    # Statistical Extreme Outliers per Commodity (using IQR method on positive values)
    flag_extreme_wholesale_outlier = pd.Series(False, index=df.index)
    flag_extreme_retail_outlier = pd.Series(False, index=df.index)
    outlier_records = []

    for cid, group in df.groupby('commodity_id'):
        cname = group['commodity_name_en'].iloc[0]
        # Wholesale positive values
        pos_w = group[group['wholesale_price_high'] > 0]['wholesale_price_high']
        if len(pos_w) >= 10:
            q1_w = pos_w.quantile(0.25)
            q3_w = pos_w.quantile(0.75)
            iqr_w = q3_w - q1_w
            upper_w = q3_w + 3.0 * iqr_w
            lower_w = max(0, q1_w - 3.0 * iqr_w)

            mask_w = (group['wholesale_price_high'] > upper_w) | ((group['wholesale_price_low'] < lower_w) & (group['wholesale_price_low'] > 0)) | (group['wholesale_price_low'] > upper_w)
            flag_extreme_wholesale_outlier.loc[group[mask_w].index] = True

            for idx in group[mask_w].index:
                r = df.loc[idx]
                outlier_records.append({
                    "row_index": idx,
                    "market_id": r['market_id'],
                    "market_name": r['market_name'],
                    "commodity_id": cid,
                    "commodity_name": cname,
                    "price_date": r['price_date'],
                    "cpi_market_commodity_price_id": r['cpi_market_commodity_price_id'],
                    "price_type": "WHOLESALE",
                    "observed_low": r['wholesale_price_low'],
                    "observed_high": r['wholesale_price_high'],
                    "observed_avg": r['wholesale_price_avg'],
                    "q1": q1_w,
                    "q3": q3_w,
                    "upper_bound_3iqr": upper_w,
                    "lower_bound_3iqr": lower_w,
                    "reason": f"Value exceeds 3xIQR upper threshold ({upper_w:.1f} BDT/quintal)"
                })

        # Retail positive values
        pos_r = group[group['retail_price_high'] > 0]['retail_price_high']
        if len(pos_r) >= 10:
            q1_r = pos_r.quantile(0.25)
            q3_r = pos_r.quantile(0.75)
            iqr_r = q3_r - q1_r
            upper_r = q3_r + 3.0 * iqr_r
            lower_r = max(0, q1_r - 3.0 * iqr_r)

            mask_r = (group['retail_price_high'] > upper_r) | ((group['retail_price_low'] < lower_r) & (group['retail_price_low'] > 0)) | (group['retail_price_low'] > upper_r)
            flag_extreme_retail_outlier.loc[group[mask_r].index] = True

            for idx in group[mask_r].index:
                r = df.loc[idx]
                outlier_records.append({
                    "row_index": idx,
                    "market_id": r['market_id'],
                    "market_name": r['market_name'],
                    "commodity_id": cid,
                    "commodity_name": cname,
                    "price_date": r['price_date'],
                    "cpi_market_commodity_price_id": r['cpi_market_commodity_price_id'],
                    "price_type": "RETAIL",
                    "observed_low": r['retail_price_low'],
                    "observed_high": r['retail_price_high'],
                    "observed_avg": r['retail_price_avg'],
                    "q1": q1_r,
                    "q3": q3_r,
                    "upper_bound_3iqr": upper_r,
                    "lower_bound_3iqr": lower_r,
                    "reason": f"Value exceeds 3xIQR upper threshold ({upper_r:.1f} BDT/kg)"
                })

    # Impossible values (e.g. 19001700 or retail > 1000 or wholesale > 100000)
    flag_impossible_value = (df['wholesale_price_low'] > 100000) | (df['wholesale_price_high'] > 100000) | \
                            (df['retail_price_low'] > 1000) | (df['retail_price_high'] > 1000) | \
                            (df['adjusted_wholesale_price_low'] > 100000) | (df['adjusted_wholesale_price_high'] > 100000)

    # Compile row level quality flags dataframe
    df_flags = pd.DataFrame({
        "row_id": df.index,
        "source_filename": df['source_filename'],
        "market_id": df['market_id'],
        "market_name": df['market_name'],
        "commodity_id": df['commodity_id'],
        "commodity_name_en": df['commodity_name_en'],
        "price_date": df['price_date'],
        "cpi_market_commodity_price_id": df['cpi_market_commodity_price_id'],
        
        # Raw prices
        "wholesale_price_low": df['wholesale_price_low'],
        "wholesale_price_high": df['wholesale_price_high'],
        "wholesale_price_avg": df['wholesale_price_avg'],
        "retail_price_low": df['retail_price_low'],
        "retail_price_high": df['retail_price_high'],
        "retail_price_avg": df['retail_price_avg'],
        
        # Adjusted prices
        "adjusted_wholesale_price_low": df['adjusted_wholesale_price_low'],
        "adjusted_wholesale_price_high": df['adjusted_wholesale_price_high'],
        "adjusted_retail_price_low": df['adjusted_retail_price_low'],
        "adjusted_retail_price_high": df['adjusted_retail_price_high'],
        
        # Quality Flags (Boolean)
        "FLAG_NEGATIVE_PRICE": flag_negative_price,
        "FLAG_ALL_PRICE_ZERO": flag_all_price_zero,
        "FLAG_ANY_PRICE_ZERO": flag_any_price_zero,
        "FLAG_WHOLESALE_RAW_INVERTED": flag_wholesale_raw_inverted,
        "FLAG_RETAIL_RAW_INVERTED": flag_retail_raw_inverted,
        "FLAG_WHOLESALE_ADJ_INVERTED": flag_wholesale_adj_inverted,
        "FLAG_RETAIL_ADJ_INVERTED": flag_retail_adj_inverted,
        "FLAG_WHOLESALE_AVG_OUTSIDE_RAW": flag_wholesale_avg_outside_raw,
        "FLAG_WHOLESALE_AVG_OUTSIDE_ADJ": flag_wholesale_avg_outside_adj,
        "FLAG_RETAIL_AVG_OUTSIDE_RAW": flag_retail_avg_outside_raw,
        "FLAG_RETAIL_AVG_OUTSIDE_ADJ": flag_retail_avg_outside_adj,
        "FLAG_EXTREME_WHOLESALE_OUTLIER": flag_extreme_wholesale_outlier,
        "FLAG_EXTREME_RETAIL_OUTLIER": flag_extreme_retail_outlier,
        "FLAG_IMPOSSIBLE_VALUE": flag_impossible_value,
        
        # Suitability flags
        "ELIGIBLE_PRIMARY_ANALYSIS": (~flag_any_price_zero) & (~flag_impossible_value) & (~flag_wholesale_raw_inverted) & (~flag_retail_raw_inverted) & (df['wholesale_price_low'] <= 15000) & (df['retail_price_low'] <= 150),
    })

    df_flags.to_csv(TARGET_DIR / "row_level_quality_flags.csv", index=False)

    # 2. Quality Summary Table
    summary_data = [
        {"metric": "Total Audited Observations", "count": n_total, "percentage": 100.0, "interpretation": "Total records extracted from DAM"},
        {"metric": "Negative Price Count", "count": int(flag_negative_price.sum()), "percentage": round(flag_negative_price.mean()*100, 3), "interpretation": "Observations with negative prices (none exist)"},
        {"metric": "All Prices Zero (W & R)", "count": int(flag_all_price_zero.sum()), "percentage": round(flag_all_price_zero.mean()*100, 3), "interpretation": "Observations where both wholesale and retail are 0.00"},
        {"metric": "Any Price Zero", "count": int(flag_any_price_zero.sum()), "percentage": round(flag_any_price_zero.mean()*100, 3), "interpretation": "Observations with at least one zero among low/high/avg"},
        {"metric": "Wholesale Raw Inverted (Low > High)", "count": int(flag_wholesale_raw_inverted.sum()), "percentage": round(flag_wholesale_raw_inverted.mean()*100, 3), "interpretation": "Enumerator entered higher price in low field or retail price in wholesale field"},
        {"metric": "Retail Raw Inverted (Low > High)", "count": int(flag_retail_raw_inverted.sum()), "percentage": round(flag_retail_raw_inverted.mean()*100, 3), "interpretation": "Enumerator entered higher retail price in low field"},
        {"metric": "Wholesale Adj Inverted", "count": int(flag_wholesale_adj_inverted.sum()), "percentage": round(flag_wholesale_adj_inverted.mean()*100, 3), "interpretation": "DAM backend adjustment produced inverted lower/upper values"},
        {"metric": "Retail Adj Inverted", "count": int(flag_retail_adj_inverted.sum()), "percentage": round(flag_retail_adj_inverted.mean()*100, 3), "interpretation": "DAM backend adjustment produced inverted lower/upper values"},
        {"metric": "Wholesale Avg Outside Raw Range", "count": int(flag_wholesale_avg_outside_raw.sum()), "percentage": round(flag_wholesale_avg_outside_raw.mean()*100, 3), "interpretation": "Expected institutional behavior (avg is computed from adjusted, not raw)"},
        {"metric": "Wholesale Avg Outside Adjusted Range", "count": int(flag_wholesale_avg_outside_adj.sum()), "percentage": round(flag_wholesale_avg_outside_adj.mean()*100, 3), "interpretation": "Anomalies where DAM backend average deviates from adjusted band"},
        {"metric": "Retail Avg Outside Raw Range", "count": int(flag_retail_avg_outside_raw.sum()), "percentage": round(flag_retail_avg_outside_raw.mean()*100, 3), "interpretation": "Expected institutional behavior (avg is computed from adjusted, not raw)"},
        {"metric": "Retail Avg Outside Adjusted Range", "count": int(flag_retail_avg_outside_adj.sum()), "percentage": round(flag_retail_avg_outside_adj.mean()*100, 3), "interpretation": "Anomalies where DAM backend retail average deviates from adjusted band"},
        {"metric": "Extreme Wholesale Outliers (>3xIQR)", "count": int(flag_extreme_wholesale_outlier.sum()), "percentage": round(flag_extreme_wholesale_outlier.mean()*100, 3), "interpretation": "Severe statistical anomalies in wholesale prices"},
        {"metric": "Extreme Retail Outliers (>3xIQR)", "count": int(flag_extreme_retail_outlier.sum()), "percentage": round(flag_extreme_retail_outlier.mean()*100, 3), "interpretation": "Severe statistical anomalies in retail prices"},
        {"metric": "Impossible Values (e.g. >100,000 W / >1,000 R)", "count": int(flag_impossible_value.sum()), "percentage": round(flag_impossible_value.mean()*100, 3), "interpretation": "Severe data-entry typos (e.g. 19001700, 350000)"},
        {"metric": "Eligible for PRIMARY_ANALYSIS", "count": int(df_flags['ELIGIBLE_PRIMARY_ANALYSIS'].sum()), "percentage": round(df_flags['ELIGIBLE_PRIMARY_ANALYSIS'].mean()*100, 3), "interpretation": "Observations meeting all primary econometric validity criteria"}
    ]
    pd.DataFrame(summary_data).to_csv(TARGET_DIR / "quality_summary.csv", index=False)

    # 3. Outlier Report
    pd.DataFrame(outlier_records).to_csv(TARGET_DIR / "outlier_report.csv", index=False)

    # 4. Range Consistency Report
    range_df = df[flag_any_inversion | flag_wholesale_avg_outside_adj | flag_retail_avg_outside_adj][[
        'market_id', 'market_name', 'commodity_id', 'commodity_name_en', 'price_date',
        'cpi_market_commodity_price_id', 'wholesale_price_low', 'wholesale_price_high',
        'wholesale_price_avg', 'adjusted_wholesale_price_low', 'adjusted_wholesale_price_high',
        'retail_price_low', 'retail_price_high', 'retail_price_avg',
        'adjusted_retail_price_low', 'adjusted_retail_price_high'
    ]]
    range_df.to_csv(TARGET_DIR / "range_consistency_report.csv", index=False)

    # 5. Zero Price Report
    zero_df = df[flag_any_price_zero][[
        'market_id', 'market_name', 'commodity_id', 'commodity_name_en', 'price_date',
        'cpi_market_commodity_price_id', 'wholesale_price_low', 'wholesale_price_high',
        'wholesale_price_avg', 'retail_price_low', 'retail_price_high', 'retail_price_avg'
    ]]
    zero_df.to_csv(TARGET_DIR / "zero_price_report.csv", index=False)

    # 6. Impossible Value Report
    imp_df = df[flag_impossible_value][[
        'market_id', 'market_name', 'commodity_id', 'commodity_name_en', 'price_date',
        'cpi_market_commodity_price_id', 'wholesale_price_low', 'wholesale_price_high',
        'wholesale_price_avg', 'retail_price_low', 'retail_price_high', 'retail_price_avg'
    ]]
    imp_df.to_csv(TARGET_DIR / "impossible_value_report.csv", index=False)

    # 7. Forensic Audit of Extreme Observations
    # Trace all records with W > 15,000 or R > 150 or impossible value back to raw JSON
    forensic_subset = df[flag_impossible_value | (df['wholesale_price_low'] > 15000) | (df['wholesale_price_high'] > 15000) | (df['retail_price_low'] > 150) | (df['retail_price_high'] > 150) | flag_wholesale_raw_inverted | flag_retail_raw_inverted]

    forensic_rows = []
    for idx, r in forensic_subset.iterrows():
        m_id = int(r['market_id'])
        c_id = int(r['commodity_id'])
        cpi_id = r['cpi_market_commodity_price_id']

        json_path = RAW_JSON_DIR / str(m_id) / f"{c_id}.json"
        raw_json_match = None
        raw_json_str = ""
        diagnosis = "GENUINE_DAM_INPUT_ANOMALY"

        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                jdata = json.load(f)
            data_arr = jdata.get('response', {}).get('data', [])
            matched = [x for x in data_arr if x.get('cpi_market_commodity_price_id') == cpi_id]
            if matched:
                raw_json_match = matched[0]
                raw_json_str = json.dumps(raw_json_match, ensure_ascii=False)

        # Diagnose root cause
        w_l = r['wholesale_price_low']
        w_h = r['wholesale_price_high']
        r_l = r['retail_price_low']
        r_h = r['retail_price_high']

        if w_l > 1000000:
            diagnosis = "DATA_ENTRY_CONCATENATION_TYPO (e.g. 19001700 entered instead of 1900/1700)"
        elif w_l > 100000:
            diagnosis = "DATA_ENTRY_EXTRA_ZEROS (e.g. 350000 entered instead of 3500)"
        elif w_l > 0 and w_h > 0 and w_h < 100 and w_l > 1000:
            diagnosis = "UNIT_MISMATCH_ENUMERATOR_TYPO (Retail Tk/kg entered into wholesale high field)"
        elif r_l > 1000:
            diagnosis = "WHOLESALE_PRICE_ENTERED_IN_RETAIL_FIELD (Wholesale quintal price typed into retail kg field)"
        elif w_l > w_h:
            diagnosis = "INVERTED_INPUT_PRICE_RANGE (Enumerator swapped low and high price quotes)"
        elif r_l > r_h:
            diagnosis = "INVERTED_INPUT_RETAIL_RANGE (Enumerator swapped retail low and high)"
        elif r['adjusted_retail_price_low'] > 200 or r['adjusted_retail_price_high'] > 200:
            diagnosis = "DAM_BACKEND_ADJUSTMENT_ALGORITHM_SPIKE (Raw prices normal, but adjusted field distorted)"

        forensic_rows.append({
            "row_index": idx,
            "market_id": m_id,
            "market_name": r['market_name'],
            "commodity_id": c_id,
            "commodity_name_en": r['commodity_name_en'],
            "price_date": r['price_date'],
            "cpi_market_commodity_price_id": cpi_id,
            "raw_csv_w_low": w_l,
            "raw_csv_w_high": w_h,
            "raw_csv_w_avg": r['wholesale_price_avg'],
            "raw_csv_r_low": r_l,
            "raw_csv_r_high": r_h,
            "raw_csv_r_avg": r['retail_price_avg'],
            "raw_csv_adj_w_low": r['adjusted_wholesale_price_low'],
            "raw_csv_adj_w_high": r['adjusted_wholesale_price_high'],
            "raw_csv_adj_r_low": r['adjusted_retail_price_low'],
            "raw_csv_adj_r_high": r['adjusted_retail_price_high'],
            "raw_json_present": (raw_json_match is not None),
            "raw_api_payload": raw_json_str,
            "root_cause_diagnosis": diagnosis,
            "recommended_action": "EXCLUDE_FROM_PRIMARY_RETAIN_IN_FULL_FLAGGED"
        })

    pd.DataFrame(forensic_rows).to_csv(TARGET_DIR / "extreme_observation_forensics.csv", index=False)
    print(f"Phase 3 & 4 complete. Saved quality audit and forensics to {TARGET_DIR}")


if __name__ == "__main__":
    run_quality_audit()
