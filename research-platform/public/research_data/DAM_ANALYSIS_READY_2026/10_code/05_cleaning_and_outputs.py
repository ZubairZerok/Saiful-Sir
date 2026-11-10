#!/usr/bin/env python3
"""
Phase 7, 8 & 9: Cleaning Protocol, Commodity Classification, and 3-Tier Output Generation
========================================================================================
Implements the formal econometric cleaning protocol and generates three distinct
scientific tiers of datasets:
1. FULL_FLAGGED (3,348 rows with all quality flags)
2. PRIMARY_ANALYSIS (Verified positive prices, clean geography, standardized BDT/kg)
3. STRICT_SENSITIVITY (Balanced panel threshold: >=6 consecutive monthly observations)

Outputs:
- 06_cleaning_rules/CLEANING_PROTOCOL.md
- 06_cleaning_rules/commodity_classification.csv
- 07_outputs/FULL_FLAGGED/ (11 commodity CSVs + DAM_ALL_11_FULL_FLAGGED.csv)
- 07_outputs/PRIMARY_ANALYSIS/ (11 commodity CSVs + DAM_ALL_11_PRIMARY_ANALYSIS.csv)
- 07_outputs/STRICT_SENSITIVITY/ (11 commodity CSVs + DAM_ALL_11_STRICT_SENSITIVITY.csv)
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
RULES_DIR = PROJECT_ROOT / "DAM_ANALYSIS_READY_2026" / "06_cleaning_rules"
OUTPUTS_DIR = PROJECT_ROOT / "DAM_ANALYSIS_READY_2026" / "07_outputs"
FLAGS_PATH = PROJECT_ROOT / "DAM_ANALYSIS_READY_2026" / "03_quality_audit" / "row_level_quality_flags.csv"
CONTINUOUS_PATH = PROJECT_ROOT / "DAM_ANALYSIS_READY_2026" / "05_temporal" / "continuous_series_report.csv"

FILE_COMMODITY_MAP = {
    "DAM_ONION_LOCAL_2010_2026.csv": (831, "DAM_ONION_LOCAL"),
    "DAM_ONION_IMPORTED_2010_2026.csv": (832, "DAM_ONION_IMPORTED"),
    "DAM_ONION_NEW_2010_2026.csv": (833, "DAM_ONION_NEW"),
    "DAM_POTATO_LOCAL_OLD_2010_2026.csv": (942, "DAM_POTATO_LOCAL_OLD"),
    "DAM_POTATO_LOCAL_2010_2026.csv": (943, "DAM_POTATO_LOCAL"),
    "DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv": (944, "DAM_POTATO_HOLLAND_WHITE_OLD"),
    "DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv": (945, "DAM_POTATO_HOLLAND_WHITE_NEW"),
    "DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv": (946, "DAM_POTATO_HOLLAND_RED_OLD"),
    "DAM_POTATO_HOLLAND_RED_2010_2026.csv": (947, "DAM_POTATO_HOLLAND_RED"),
    "DAM_SWEET_POTATO_2010_2026.csv": (948, "DAM_SWEET_POTATO"),
    "DAM_POTATOES_IMPORTED_2010_2026.csv": (21014, "DAM_POTATOES_IMPORTED"),
}


def run_cleaning_and_outputs() -> None:
    RULES_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUTS_DIR / "FULL_FLAGGED").mkdir(parents=True, exist_ok=True)
    (OUTPUTS_DIR / "PRIMARY_ANALYSIS").mkdir(parents=True, exist_ok=True)
    (OUTPUTS_DIR / "STRICT_SENSITIVITY").mkdir(parents=True, exist_ok=True)

    print("Executing Phase 7, 8 & 9: Cleaning Protocol & Output Construction...")

    # 1. Commodity Classification Table (Phase 9)
    classification_records = [
        {
            "commodity_id": 831,
            "commodity_name": "Onion (local)",
            "commodity_family": "ONION",
            "commodity_variant": "Local / Domestic",
            "recommended_use": "PRIMARY_SAMPLE (Paper 1, Paper 2, Paper 3)",
            "reason": "Dominant domestic onion series with largest market footprint (97 markets, 911 obs), strong temporal continuity."
        },
        {
            "commodity_id": 832,
            "commodity_name": "Onion-imported",
            "commodity_family": "ONION",
            "commodity_variant": "Imported",
            "recommended_use": "ROBUSTNESS_SAMPLE (Trade / Import Shock Sensitivity)",
            "reason": "Captures import parity pricing; useful for testing border vs. interior market transmission."
        },
        {
            "commodity_id": 833,
            "commodity_name": "Onion (New)",
            "commodity_family": "ONION",
            "commodity_variant": "New Harvest (Early Season)",
            "recommended_use": "ROBUSTNESS_SAMPLE (Early Harvest Shocks)",
            "reason": "Captures early harvest price dynamics; 29 markets, high seasonal concentration."
        },
        {
            "commodity_id": 943,
            "commodity_name": "Potato (Local)",
            "commodity_family": "POTATO",
            "commodity_variant": "Indigenous / Deshi Local",
            "recommended_use": "PRIMARY_SAMPLE (Paper 1, Paper 2, Paper 3)",
            "reason": "Core domestic potato series; 54 markets, 416 observations, extensive spatial dispersion."
        },
        {
            "commodity_id": 945,
            "commodity_name": "Potato (Holland) - White (New)",
            "commodity_family": "POTATO",
            "commodity_variant": "High Yielding Variety (HYV) White New",
            "recommended_use": "PRIMARY_SAMPLE (Paper 1, Paper 2, Paper 3)",
            "reason": "Largest commercial potato series (82 markets, 688 obs); vital for high-volume commercial market integration."
        },
        {
            "commodity_id": 947,
            "commodity_name": "Potato (Holland) - Red",
            "commodity_family": "POTATO",
            "commodity_variant": "HYV Red",
            "recommended_use": "PRIMARY_SAMPLE (Paper 1, Paper 2, Paper 3)",
            "reason": "Secondary commercial staple (52 markets, 452 obs); strong geographic coverage across Northern production belts."
        },
        {
            "commodity_id": 944,
            "commodity_name": "Potato (Holland) - White (Old)",
            "commodity_family": "POTATO",
            "commodity_variant": "Cold Storage White Old",
            "recommended_use": "ROBUSTNESS_SAMPLE (Storage / Off-Season Analysis)",
            "reason": "Reflects cold storage liquidation prices before new crop arrival (23 markets, 160 obs)."
        },
        {
            "commodity_id": 946,
            "commodity_name": "Potato (Holland) - Red (Old)",
            "commodity_family": "POTATO",
            "commodity_variant": "Cold Storage Red Old",
            "recommended_use": "ROBUSTNESS_SAMPLE (Storage / Off-Season Analysis)",
            "reason": "Cold storage red potato series (26 markets, 145 obs)."
        },
        {
            "commodity_id": 942,
            "commodity_name": "Potato (Local) - Old",
            "commodity_family": "POTATO",
            "commodity_variant": "Local Old Crop",
            "recommended_use": "ROBUSTNESS_SAMPLE (Limited Panel)",
            "reason": "Specialized local old crop; 15 markets, 75 observations."
        },
        {
            "commodity_id": 21014,
            "commodity_name": "Potatoes-imported",
            "commodity_family": "POTATO",
            "commodity_variant": "Imported Potato",
            "recommended_use": "EXCLUDE FROM PRIMARY (Supplementary only)",
            "reason": "Small sample size (3 markets, 24 obs); insufficient for spatial panel modeling."
        },
        {
            "commodity_id": 948,
            "commodity_name": "Sweet Potato",
            "commodity_family": "SWEET_POTATO",
            "commodity_variant": "Tuber / Sweet Potato",
            "recommended_use": "EXCLUDE FROM MAIN PAPERS (Distinct crop biology/market)",
            "reason": "Botanically distinct tuber, very small sample (2 markets, 10 obs); unsuitable for potato panel regressions."
        }
    ]
    df_class = pd.DataFrame(classification_records)
    df_class.to_csv(RULES_DIR / "commodity_classification.csv", index=False)

    # 2. Cleaning Protocol Documentation (Phase 7)
    protocol_md = """# Econometric Cleaning Protocol for Analysis-Ready DAM Price Datasets

## 1. Principles of Scientific Data Preparation
This protocol establishes an immutable, defensible cleaning and standardization standard for agricultural market price data collected by the Department of Agricultural Marketing (DAM), Ministry of Agriculture, Bangladesh.

### Core Safeguards:
1. **Zero Raw Mutation:** Raw source CSVs and original JSON responses are permanently read-only.
2. **Zero Price Fabrication:** No missing prices are interpolated, imputed from neighboring markets, or smoothed using synthetic models.
3. **Explicit Row-Level Traceability:** Every transformation and exclusion is tracked by `row_id` and `cpi_market_commodity_price_id`.

---

## 2. Standardized Price Variables
To eliminate unit ambiguity across wholesale (BDT/Quintal = 100 kg) and retail (BDT/kg), the pipeline generates standardized per-kilogram price metrics:

1. **`price_wholesale_raw_mid_kg`** $= \\frac{\\text{wholesale\\_price\\_low} + \\text{wholesale\\_price\\_high}}{2 \\times 100}$  
   *Primary outcome variable for Papers 1 & 2.* Direct reflection of local market trading quotes.
2. **`price_wholesale_dam_avg_kg`** $= \\frac{\\text{wholesale\\_price\\_avg}}{100}$  
   *Official DAM headline wholesale average.* Incorporates central benchmark calibrations.
3. **`price_retail_raw_mid_kg`** $= \\frac{\\text{retail\\_price\\_low} + \\text{retail\\_price\\_high}}{2}$  
   *Direct local retail price quote midpoint.*
4. **`price_retail_dam_avg_kg`** $= \\text{retail\\_price\\_avg}$  
   *Official DAM retail headline average.*
5. **`wholesale_retail_spread_kg`** $= \\text{price\\_retail\\_raw\\_mid\\_kg} - \\text{price\\_wholesale\\_raw\\_mid\\_kg}$  
   *Marketing margin / spatial intermediary spread for Paper 3.*

---

## 3. Dataset Tier Definitions

### Tier A: FULL_FLAGGED
- **Contents:** Every single observation successfully extracted from the verified DAM API (3,348 observations).
- **Modifications:** None. All 14 boolean quality audit flags and standardized price variables are appended as new columns.
- **Purpose:** Full transparency, forensic audit trail, and complete data accounting.

### Tier B: PRIMARY_ANALYSIS
- **Contents:** Validated empirical observations suitable for baseline econometric estimations.
- **Inclusion Rules:**
  1. $\\text{wholesale\\_price\\_low} > 0$ and $\\text{wholesale\\_price\\_high} > 0$ (excludes non-trading zero records).
  2. $\\text{wholesale\\_price\\_low} \\le \\text{wholesale\\_price\\_high}$ (excludes inverted data-entry errors).
  3. $\\text{retail\\_price\\_low} \\le \\text{retail\\_price\\_high}$ (excludes inverted retail errors).
  4. $\\text{wholesale\\_price\\_low} \\le 15,000$ BDT/quintal (150 BDT/kg) and $\\text{retail\\_price\\_low} \\le 150$ BDT/kg (excludes extreme typing anomalies such as 19001700 or 350000).
- **Treatment of Adjusted Averages:** Retains observations where raw reported bounds are valid even if DAM's backend adjustment algorithm produced an adjusted spike, because raw price midpoints remain uncontaminated.

### Tier C: STRICT_SENSITIVITY
- **Contents:** Balanced panel subset for dynamic panel regressions and spatial price transmission models.
- **Inclusion Rules:**
  1. Satisfies all Tier B (PRIMARY_ANALYSIS) criteria.
  2. Belongs to a market $\\times$ commodity series with **$\\ge 6$ consecutive monthly observations**.
  3. Excludes fragmented, sporadic market appearances.
"""
    (RULES_DIR / "CLEANING_PROTOCOL.md").write_text(protocol_md, encoding='utf-8')

    # 3. Load quality flags and continuous series info
    df_flags = pd.read_csv(FLAGS_PATH)
    df_cont = pd.read_csv(CONTINUOUS_PATH)
    consec_6_keys = set(zip(
        df_cont[df_cont['has_ge_6_consecutive']]['market_id'],
        df_cont[df_cont['has_ge_6_consecutive']]['commodity_id']
    ))

    # Build Master Augmented DataFrame
    dfs_augmented = []
    for fn, (cid, prefix) in FILE_COMMODITY_MAP.items():
        src_df = pd.read_csv(SOURCE_DIR / fn)
        src_df['source_filename'] = fn
        src_df['commodity_family'] = "ONION" if "ONION" in prefix else ("POTATO" if "POTATO" in prefix else "SWEET_POTATO")
        dfs_augmented.append(src_df)

    master_df = pd.concat(dfs_augmented, ignore_index=True)
    master_df['row_id'] = master_df.index

    # Add Standardized Prices (Tk / kg)
    master_df['price_wholesale_raw_mid_kg'] = np.where(
        (master_df['wholesale_price_low'] > 0) & (master_df['wholesale_price_high'] > 0),
        ((master_df['wholesale_price_low'] + master_df['wholesale_price_high']) / 2.0) / 100.0,
        np.nan
    )
    master_df['price_wholesale_dam_avg_kg'] = np.where(
        master_df['wholesale_price_avg'] > 0,
        master_df['wholesale_price_avg'] / 100.0,
        np.nan
    )
    master_df['price_retail_raw_mid_kg'] = np.where(
        (master_df['retail_price_low'] > 0) & (master_df['retail_price_high'] > 0),
        (master_df['retail_price_low'] + master_df['retail_price_high']) / 2.0,
        np.nan
    )
    master_df['price_retail_dam_avg_kg'] = np.where(
        master_df['retail_price_avg'] > 0,
        master_df['retail_price_avg'],
        np.nan
    )
    master_df['wholesale_retail_spread_kg'] = master_df['price_retail_raw_mid_kg'] - master_df['price_wholesale_raw_mid_kg']

    # Merge Quality Flags
    flag_cols = [
        'FLAG_NEGATIVE_PRICE', 'FLAG_ALL_PRICE_ZERO', 'FLAG_ANY_PRICE_ZERO',
        'FLAG_WHOLESALE_RAW_INVERTED', 'FLAG_RETAIL_RAW_INVERTED',
        'FLAG_WHOLESALE_ADJ_INVERTED', 'FLAG_RETAIL_ADJ_INVERTED',
        'FLAG_WHOLESALE_AVG_OUTSIDE_RAW', 'FLAG_WHOLESALE_AVG_OUTSIDE_ADJ',
        'FLAG_RETAIL_AVG_OUTSIDE_RAW', 'FLAG_RETAIL_AVG_OUTSIDE_ADJ',
        'FLAG_EXTREME_WHOLESALE_OUTLIER', 'FLAG_EXTREME_RETAIL_OUTLIER',
        'FLAG_IMPOSSIBLE_VALUE', 'ELIGIBLE_PRIMARY_ANALYSIS'
    ]
    master_df = master_df.merge(df_flags[['row_id'] + flag_cols], on='row_id', how='left')

    # Add Strict Sensitivity Flag
    master_df['key_m_c'] = list(zip(master_df['market_id'], master_df['commodity_id']))
    master_df['ELIGIBLE_STRICT_SENSITIVITY'] = master_df['ELIGIBLE_PRIMARY_ANALYSIS'] & master_df['key_m_c'].isin(consec_6_keys)
    master_df.drop(columns=['key_m_c'], inplace=True)

    # 4. Generate Tier Outputs
    # Tier A: FULL_FLAGGED
    full_df = master_df.copy()
    full_df.to_csv(OUTPUTS_DIR / "FULL_FLAGGED" / "DAM_ALL_11_FULL_FLAGGED.csv", index=False)

    for fn, (cid, prefix) in FILE_COMMODITY_MAP.items():
        sub = full_df[full_df['commodity_id'] == cid]
        out_fn = f"{prefix}_FULL_FLAGGED.csv"
        sub.to_csv(OUTPUTS_DIR / "FULL_FLAGGED" / out_fn, index=False)

    # Tier B: PRIMARY_ANALYSIS
    primary_df = master_df[master_df['ELIGIBLE_PRIMARY_ANALYSIS']].copy()
    primary_df.to_csv(OUTPUTS_DIR / "PRIMARY_ANALYSIS" / "DAM_ALL_11_PRIMARY_ANALYSIS.csv", index=False)

    for fn, (cid, prefix) in FILE_COMMODITY_MAP.items():
        sub = primary_df[primary_df['commodity_id'] == cid]
        out_fn = f"{prefix}_PRIMARY_ANALYSIS.csv"
        sub.to_csv(OUTPUTS_DIR / "PRIMARY_ANALYSIS" / out_fn, index=False)

    # Tier C: STRICT_SENSITIVITY
    strict_df = master_df[master_df['ELIGIBLE_STRICT_SENSITIVITY']].copy()
    strict_df.to_csv(OUTPUTS_DIR / "STRICT_SENSITIVITY" / "DAM_ALL_11_STRICT_SENSITIVITY.csv", index=False)

    for fn, (cid, prefix) in FILE_COMMODITY_MAP.items():
        sub = strict_df[strict_df['commodity_id'] == cid]
        out_fn = f"{prefix}_STRICT_SENSITIVITY.csv"
        sub.to_csv(OUTPUTS_DIR / "STRICT_SENSITIVITY" / out_fn, index=False)

    print(f"Generated 3 Dataset Tiers:")
    print(f"  FULL_FLAGGED:       {len(full_df):,} rows | {full_df['market_id'].nunique()} markets | 11 commodities")
    print(f"  PRIMARY_ANALYSIS:   {len(primary_df):,} rows | {primary_df['market_id'].nunique()} markets | 11 commodities (Excluded {len(full_df)-len(primary_df)} corrupted/zero rows)")
    print(f"  STRICT_SENSITIVITY: {len(strict_df):,} rows | {strict_df['market_id'].nunique()} markets | 11 commodities (Excluded {len(primary_df)-len(strict_df)} non-consecutive rows)")


if __name__ == "__main__":
    run_cleaning_and_outputs()
