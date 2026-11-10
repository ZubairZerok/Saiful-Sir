# DAM Agricultural Price Data — FINAL AUDIT REPORT

**Generated:** 2026-10-11 11:22:50
**Mode:** READ-ONLY AUDIT (no original files were modified)
**Source:** `D:\datamain\dam_output\master`
**Output:** `D:\datamain\DAM_AUDIT_2026`

---

## A. Dataset Inventory

**Total files audited:** 11
**Total observations (across all files):** 3,348
**Total unique markets (across all files):** 117

| # | Filename | Commodity | Rows | Cols | Markets | Districts | First Date | Last Date | Years |
|---|----------|-----------|------|------|---------|-----------|------------|-----------|-------|
| 1 | `DAM_ONION_LOCAL_2010_2026.csv` | Onion (local) | 911 | 39 | 97 | 0 | 2025-06-04 | 2026-08-13 | 2 |
| 2 | `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | 201 | 39 | 50 | 0 | 2025-06-15 | 2026-08-02 | 2 |
| 3 | `DAM_ONION_NEW_2010_2026.csv` | Onion (New) | 266 | 39 | 29 | 0 | 2025-06-14 | 2026-08-02 | 2 |
| 4 | `DAM_POTATO_LOCAL_2010_2026.csv` | Potato (Local) | 416 | 39 | 54 | 0 | 2025-06-04 | 2026-08-04 | 2 |
| 5 | `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | Potato (Local) - Old | 75 | 39 | 15 | 0 | 2025-06-04 | 2026-08-03 | 2 |
| 6 | `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | 688 | 39 | 82 | 0 | 2025-06-15 | 2026-08-13 | 2 |
| 7 | `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | Potato (Holland) - White (Old) | 160 | 39 | 23 | 0 | 2025-06-14 | 2026-08-02 | 2 |
| 8 | `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | 452 | 39 | 52 | 0 | 2025-06-15 | 2026-08-03 | 2 |
| 9 | `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | Potato (Holland) - Red (Old) | 145 | 39 | 26 | 0 | 2025-06-04 | 2026-08-11 | 2 |
| 10 | `DAM_POTATOES_IMPORTED_2010_2026.csv` | Potatoes-imported | 24 | 39 | 3 | 0 | 2025-06-15 | 2026-08-02 | 2 |
| 11 | `DAM_SWEET_POTATO_2010_2026.csv` | Sweet Potato | 10 | 39 | 2 | 0 | 2025-06-15 | 2026-07-02 | 2 |

### Observations by Commodity

| Commodity | Total Obs |
|-----------|-----------|
| Onion (local) | 911 |
| Onion-imported | 201 |
| Onion (New) | 266 |
| Potato (Local) | 416 |
| Potato (Local) - Old | 75 |
| Potato (Holland) - White (New) | 688 |
| Potato (Holland) - White (Old) | 160 |
| Potato (Holland) - Red | 452 |
| Potato (Holland) - Red (Old) | 145 |
| Potatoes-imported | 24 |
| Sweet Potato | 10 |

## B. Missingness Summary

| Filename | Empty Cols | Empty Col Names | Dup Rows | Dup Market-Commodity-Date |
|----------|-----------|-----------------|----------|--------------------------|
| `DAM_ONION_LOCAL_2010_2026.csv` | 2.0 | district_name; upazila_name | 0.0 | 0.0 |
| `DAM_ONION_IMPORTED_2010_2026.csv` | 2.0 | district_name; upazila_name | 0.0 | 0.0 |
| `DAM_ONION_NEW_2010_2026.csv` | 2.0 | district_name; upazila_name | 0.0 | 0.0 |
| `DAM_POTATO_LOCAL_2010_2026.csv` | 2.0 | district_name; upazila_name | 0.0 | 0.0 |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | 2.0 | district_name; upazila_name | 0.0 | 0.0 |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | 2.0 | district_name; upazila_name | 0.0 | 0.0 |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | 2.0 | district_name; upazila_name | 0.0 | 0.0 |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | 2.0 | district_name; upazila_name | 0.0 | 0.0 |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | 2.0 | district_name; upazila_name | 0.0 | 0.0 |
| `DAM_POTATOES_IMPORTED_2010_2026.csv` | 2.0 | district_name; upazila_name | 0.0 | 0.0 |
| `DAM_SWEET_POTATO_2010_2026.csv` | 2.0 | district_name; upazila_name | 0.0 | 0.0 |

### Columns with >5% Missing (any file)

| Filename | Column | Missing Count | % Missing |
|----------|--------|---------------|-----------|
| `DAM_ONION_LOCAL_2010_2026.csv` | district_name | 911 | 100.0% |
| `DAM_ONION_LOCAL_2010_2026.csv` | upazila_name | 911 | 100.0% |
| `DAM_ONION_LOCAL_2010_2026.csv` | wholesale_supply | 85 | 9.33% |
| `DAM_ONION_IMPORTED_2010_2026.csv` | district_name | 201 | 100.0% |
| `DAM_ONION_IMPORTED_2010_2026.csv` | upazila_name | 201 | 100.0% |
| `DAM_ONION_IMPORTED_2010_2026.csv` | wholesale_supply | 16 | 7.96% |
| `DAM_ONION_NEW_2010_2026.csv` | district_name | 266 | 100.0% |
| `DAM_ONION_NEW_2010_2026.csv` | upazila_name | 266 | 100.0% |
| `DAM_POTATO_LOCAL_2010_2026.csv` | district_name | 416 | 100.0% |
| `DAM_POTATO_LOCAL_2010_2026.csv` | upazila_name | 416 | 100.0% |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | district_name | 75 | 100.0% |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | upazila_name | 75 | 100.0% |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | wholesale_supply | 16 | 21.33% |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | district_name | 688 | 100.0% |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | upazila_name | 688 | 100.0% |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | district_name | 160 | 100.0% |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | upazila_name | 160 | 100.0% |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | wholesale_supply | 24 | 15.0% |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | district_name | 452 | 100.0% |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | upazila_name | 452 | 100.0% |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | district_name | 145 | 100.0% |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | upazila_name | 145 | 100.0% |
| `DAM_POTATOES_IMPORTED_2010_2026.csv` | district_name | 24 | 100.0% |
| `DAM_POTATOES_IMPORTED_2010_2026.csv` | upazila_name | 24 | 100.0% |
| `DAM_SWEET_POTATO_2010_2026.csv` | district_name | 10 | 100.0% |
| `DAM_SWEET_POTATO_2010_2026.csv` | upazila_name | 10 | 100.0% |

## C. Coverage Analysis

### Market Coverage Summary by Commodity

| Commodity | Markets | ≤2 obs | ≥12 obs | ≥24 obs | ≥36 obs | ≥60 obs | Max Continuous |
|-----------|---------|--------|---------|---------|---------|---------|----------------|
| Onion (local) | 97 | 18 | 45 | 0 | 0 | 0 | 15 |
| Onion-imported | 50 | 20 | 2 | 0 | 0 | 0 | 15 |
| Onion (New) | 29 | 5 | 13 | 0 | 0 | 0 | 15 |
| Potato (Local) | 54 | 9 | 11 | 0 | 0 | 0 | 15 |
| Potato (Local) - Old | 15 | 6 | 1 | 0 | 0 | 0 | 15 |
| Potato (Holland) - White (New) | 82 | 16 | 28 | 0 | 0 | 0 | 15 |
| Potato (Holland) - White (Old) | 23 | 7 | 3 | 0 | 0 | 0 | 15 |
| Potato (Holland) - Red | 52 | 10 | 18 | 0 | 0 | 0 | 15 |
| Potato (Holland) - Red (Old) | 26 | 8 | 2 | 0 | 0 | 0 | 15 |
| Potatoes-imported | 3 | 1 | 1 | 0 | 0 | 0 | 15 |
| Sweet Potato | 2 | 0 | 0 | 0 | 0 | 0 | 7 |

## D. Research Suitability (Paper 1)

| Commodity | Obs | Markets | ≥6 obs | ≥12 obs | ≥24 obs | Max Run | Span (mo) | Score | Suitability |
|-----------|-----|---------|--------|---------|---------|---------|-----------|-------|-------------|
| Onion (local) | 911 | 97 | 69 | 45 | 0 | 15 | 14 | 7 | **STRONG** |
| Onion-imported | 201 | 50 | 8 | 2 | 0 | 15 | 14 | 5 | **STRONG** |
| Onion (New) | 266 | 29 | 20 | 13 | 0 | 15 | 14 | 7 | **STRONG** |
| Potato (Local) | 416 | 54 | 38 | 11 | 0 | 15 | 14 | 7 | **STRONG** |
| Potato (Local) - Old | 75 | 15 | 7 | 1 | 0 | 15 | 14 | 4 | **MODERATE** |
| Potato (Holland) - White (New) | 688 | 82 | 51 | 28 | 0 | 15 | 14 | 7 | **STRONG** |
| Potato (Holland) - White (Old) | 160 | 23 | 15 | 3 | 0 | 15 | 14 | 5 | **STRONG** |
| Potato (Holland) - Red | 452 | 52 | 39 | 18 | 0 | 15 | 14 | 7 | **STRONG** |
| Potato (Holland) - Red (Old) | 145 | 26 | 13 | 2 | 0 | 15 | 14 | 5 | **STRONG** |
| Potatoes-imported | 24 | 3 | 2 | 1 | 0 | 15 | 14 | 3 | **MODERATE** |
| Sweet Potato | 10 | 2 | 1 | 0 | 0 | 7 | 13 | 2 | **WEAK** |

**Strongest Onion series:** Onion (local) (911 obs, score=7)
**Strongest Potato series:** Potato (Local) (416 obs, score=7)

## E. Market-Pair Feasibility

| Commodity | Markets | Possible Pairs | Overlapping | ≥12 common | ≥24 common | ≥36 common | ≥60 common |
|-----------|---------|----------------|-------------|------------|------------|------------|------------|
| Onion (local) | 97 | 4656 | 4500 | 990 | 0 | 0 | 0 |
| Onion-imported | 50 | 1225 | 1045 | 1 | 0 | 0 | 0 |
| Onion (New) | 29 | 406 | 353 | 78 | 0 | 0 | 0 |
| Potato (Holland) - White (New) | 82 | 3321 | 2979 | 378 | 0 | 0 | 0 |
| Potato (Holland) - Red | 52 | 1326 | 1188 | 153 | 0 | 0 | 0 |
| Potato (Local) | 54 | 1431 | 1272 | 55 | 0 | 0 | 0 |
| Potato (Holland) - White (Old) | 23 | 253 | 222 | 3 | 0 | 0 | 0 |
| Potato (Holland) - Red (Old) | 26 | 325 | 229 | 1 | 0 | 0 | 0 |
| Potato (Local) - Old | 15 | 105 | 63 | 0 | 0 | 0 | 0 |
| Potatoes-imported | 3 | 3 | 3 | 0 | 0 | 0 | 0 |
| Sweet Potato | 2 | 1 | 0 | 0 | 0 | 0 | 0 |

## F. Data Quality Issues

### Issue Summary (All Files)

| Issue Type | Total Count |
|------------|-------------|
| WHOLESALE_AVG_OUTSIDE_RANGE | 1900 |
| RETAIL_AVG_OUTSIDE_RANGE | 1432 |
| ZERO_PRICE | 672 |
| EXTREME_OUTLIER_RETAIL_AVG | 65 |
| EXTREME_OUTLIER_WHOLESALE_AVG | 63 |
| WHOLESALE_LOW_GT_HIGH | 13 |
| RETAIL_LOW_GT_HIGH | 3 |

### Detailed Issues by File

| Filename | Commodity | Issue | Column | Count | Detail |
|----------|-----------|-------|--------|-------|--------|
| `DAM_ONION_LOCAL_2010_2026.csv` | Onion (local) | ZERO_PRICE | wholesale_price_low | 3 | 3 zero values |
| `DAM_ONION_LOCAL_2010_2026.csv` | Onion (local) | ZERO_PRICE | wholesale_price_high | 3 | 3 zero values |
| `DAM_ONION_LOCAL_2010_2026.csv` | Onion (local) | ZERO_PRICE | retail_price_low | 4 | 4 zero values |
| `DAM_ONION_LOCAL_2010_2026.csv` | Onion (local) | ZERO_PRICE | retail_price_high | 4 | 4 zero values |
| `DAM_ONION_LOCAL_2010_2026.csv` | Onion (local) | WHOLESALE_LOW_GT_HIGH | wholesale_price_low/high | 5 | 5 rows where wholesale low > high |
| `DAM_ONION_LOCAL_2010_2026.csv` | Onion (local) | RETAIL_LOW_GT_HIGH | retail_price_low/high | 1 | 1 rows where retail low > high |
| `DAM_ONION_LOCAL_2010_2026.csv` | Onion (local) | WHOLESALE_AVG_OUTSIDE_RANGE | wholesale_price_avg | 600 | 600 rows where wholesale avg outside [low, high] |
| `DAM_ONION_LOCAL_2010_2026.csv` | Onion (local) | RETAIL_AVG_OUTSIDE_RANGE | retail_price_avg | 471 | 471 rows where retail avg outside [low, high] |
| `DAM_ONION_LOCAL_2010_2026.csv` | Onion (local) | EXTREME_OUTLIER_WHOLESALE_AVG | wholesale_price_avg | 7 | 7 values outside [Q1-3*IQR, Q3+3*IQR] = [-5557, 14876] |
| `DAM_ONION_LOCAL_2010_2026.csv` | Onion (local) | EXTREME_OUTLIER_RETAIL_AVG | retail_price_avg | 3 | 3 values outside [Q1-3*IQR, Q3+3*IQR] = [-49, 154] |
| `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | ZERO_PRICE | wholesale_price_low | 42 | 42 zero values |
| `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | ZERO_PRICE | wholesale_price_high | 42 | 42 zero values |
| `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | ZERO_PRICE | wholesale_price_avg | 8 | 8 zero values |
| `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | ZERO_PRICE | retail_price_low | 42 | 42 zero values |
| `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | ZERO_PRICE | retail_price_high | 43 | 43 zero values |
| `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | ZERO_PRICE | retail_price_avg | 8 | 8 zero values |
| `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | RETAIL_LOW_GT_HIGH | retail_price_low/high | 1 | 1 rows where retail low > high |
| `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | WHOLESALE_AVG_OUTSIDE_RANGE | wholesale_price_avg | 129 | 129 rows where wholesale avg outside [low, high] |
| `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | RETAIL_AVG_OUTSIDE_RANGE | retail_price_avg | 107 | 107 rows where retail avg outside [low, high] |
| `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | EXTREME_OUTLIER_WHOLESALE_AVG | wholesale_price_avg | 8 | 8 values outside [Q1-3*IQR, Q3+3*IQR] = [168, 11676] |
| `DAM_ONION_IMPORTED_2010_2026.csv` | Onion-imported | EXTREME_OUTLIER_RETAIL_AVG | retail_price_avg | 8 | 8 values outside [Q1-3*IQR, Q3+3*IQR] = [7, 126] |
| `DAM_ONION_NEW_2010_2026.csv` | Onion (New) | RETAIL_LOW_GT_HIGH | retail_price_low/high | 1 | 1 rows where retail low > high |
| `DAM_ONION_NEW_2010_2026.csv` | Onion (New) | WHOLESALE_AVG_OUTSIDE_RANGE | wholesale_price_avg | 164 | 164 rows where wholesale avg outside [low, high] |
| `DAM_ONION_NEW_2010_2026.csv` | Onion (New) | RETAIL_AVG_OUTSIDE_RANGE | retail_price_avg | 146 | 146 rows where retail avg outside [low, high] |
| `DAM_ONION_NEW_2010_2026.csv` | Onion (New) | EXTREME_OUTLIER_RETAIL_AVG | retail_price_avg | 2 | 2 values outside [Q1-3*IQR, Q3+3*IQR] = [-54, 163] |
| `DAM_POTATO_LOCAL_2010_2026.csv` | Potato (Local) | ZERO_PRICE | wholesale_price_low | 3 | 3 zero values |
| `DAM_POTATO_LOCAL_2010_2026.csv` | Potato (Local) | ZERO_PRICE | wholesale_price_high | 3 | 3 zero values |
| `DAM_POTATO_LOCAL_2010_2026.csv` | Potato (Local) | ZERO_PRICE | retail_price_low | 4 | 4 zero values |
| `DAM_POTATO_LOCAL_2010_2026.csv` | Potato (Local) | ZERO_PRICE | retail_price_high | 4 | 4 zero values |
| `DAM_POTATO_LOCAL_2010_2026.csv` | Potato (Local) | WHOLESALE_LOW_GT_HIGH | wholesale_price_low/high | 2 | 2 rows where wholesale low > high |
| `DAM_POTATO_LOCAL_2010_2026.csv` | Potato (Local) | WHOLESALE_AVG_OUTSIDE_RANGE | wholesale_price_avg | 192 | 192 rows where wholesale avg outside [low, high] |
| `DAM_POTATO_LOCAL_2010_2026.csv` | Potato (Local) | RETAIL_AVG_OUTSIDE_RANGE | retail_price_avg | 134 | 134 rows where retail avg outside [low, high] |
| `DAM_POTATO_LOCAL_2010_2026.csv` | Potato (Local) | EXTREME_OUTLIER_WHOLESALE_AVG | wholesale_price_avg | 6 | 6 values outside [Q1-3*IQR, Q3+3*IQR] = [-1384, 5706] |
| `DAM_POTATO_LOCAL_2010_2026.csv` | Potato (Local) | EXTREME_OUTLIER_RETAIL_AVG | retail_price_avg | 3 | 3 values outside [Q1-3*IQR, Q3+3*IQR] = [-15, 69] |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | Potato (Local) - Old | ZERO_PRICE | wholesale_price_low | 23 | 23 zero values |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | Potato (Local) - Old | ZERO_PRICE | wholesale_price_high | 23 | 23 zero values |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | Potato (Local) - Old | ZERO_PRICE | wholesale_price_avg | 8 | 8 zero values |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | Potato (Local) - Old | ZERO_PRICE | retail_price_low | 24 | 24 zero values |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | Potato (Local) - Old | ZERO_PRICE | retail_price_high | 24 | 24 zero values |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | Potato (Local) - Old | ZERO_PRICE | retail_price_avg | 9 | 9 zero values |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | Potato (Local) - Old | WHOLESALE_AVG_OUTSIDE_RANGE | wholesale_price_avg | 38 | 38 rows where wholesale avg outside [low, high] |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | Potato (Local) - Old | RETAIL_AVG_OUTSIDE_RANGE | retail_price_avg | 28 | 28 rows where retail avg outside [low, high] |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | Potato (Local) - Old | EXTREME_OUTLIER_WHOLESALE_AVG | wholesale_price_avg | 15 | 15 values outside [Q1-3*IQR, Q3+3*IQR] = [-1864, 6592] |
| `DAM_POTATO_LOCAL_OLD_2010_2026.csv` | Potato (Local) - Old | EXTREME_OUTLIER_RETAIL_AVG | retail_price_avg | 15 | 15 values outside [Q1-3*IQR, Q3+3*IQR] = [-16, 75] |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | ZERO_PRICE | wholesale_price_low | 24 | 24 zero values |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | ZERO_PRICE | wholesale_price_high | 24 | 24 zero values |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | ZERO_PRICE | wholesale_price_avg | 8 | 8 zero values |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | ZERO_PRICE | retail_price_low | 25 | 25 zero values |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | ZERO_PRICE | retail_price_high | 25 | 25 zero values |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | ZERO_PRICE | retail_price_avg | 9 | 9 zero values |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | WHOLESALE_LOW_GT_HIGH | wholesale_price_low/high | 3 | 3 rows where wholesale low > high |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | WHOLESALE_AVG_OUTSIDE_RANGE | wholesale_price_avg | 367 | 367 rows where wholesale avg outside [low, high] |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | RETAIL_AVG_OUTSIDE_RANGE | retail_price_avg | 247 | 247 rows where retail avg outside [low, high] |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | EXTREME_OUTLIER_WHOLESALE_AVG | wholesale_price_avg | 7 | 7 values outside [Q1-3*IQR, Q3+3*IQR] = [-158, 3623] |
| `DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv` | Potato (Holland) - White (New) | EXTREME_OUTLIER_RETAIL_AVG | retail_price_avg | 13 | 13 values outside [Q1-3*IQR, Q3+3*IQR] = [1, 43] |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | Potato (Holland) - White (Old) | ZERO_PRICE | wholesale_price_low | 29 | 29 zero values |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | Potato (Holland) - White (Old) | ZERO_PRICE | wholesale_price_high | 29 | 29 zero values |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | Potato (Holland) - White (Old) | ZERO_PRICE | wholesale_price_avg | 8 | 8 zero values |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | Potato (Holland) - White (Old) | ZERO_PRICE | retail_price_low | 29 | 29 zero values |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | Potato (Holland) - White (Old) | ZERO_PRICE | retail_price_high | 29 | 29 zero values |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | Potato (Holland) - White (Old) | ZERO_PRICE | retail_price_avg | 8 | 8 zero values |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | Potato (Holland) - White (Old) | WHOLESALE_AVG_OUTSIDE_RANGE | wholesale_price_avg | 93 | 93 rows where wholesale avg outside [low, high] |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | Potato (Holland) - White (Old) | RETAIL_AVG_OUTSIDE_RANGE | retail_price_avg | 69 | 69 rows where retail avg outside [low, high] |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | Potato (Holland) - White (Old) | EXTREME_OUTLIER_WHOLESALE_AVG | wholesale_price_avg | 15 | 15 values outside [Q1-3*IQR, Q3+3*IQR] = [-843, 4031] |
| `DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv` | Potato (Holland) - White (Old) | EXTREME_OUTLIER_RETAIL_AVG | retail_price_avg | 18 | 18 values outside [Q1-3*IQR, Q3+3*IQR] = [-4, 47] |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | ZERO_PRICE | wholesale_price_low | 2 | 2 zero values |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | ZERO_PRICE | wholesale_price_high | 2 | 2 zero values |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | ZERO_PRICE | wholesale_price_avg | 1 | 1 zero values |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | ZERO_PRICE | retail_price_low | 2 | 2 zero values |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | ZERO_PRICE | retail_price_high | 2 | 2 zero values |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | ZERO_PRICE | retail_price_avg | 1 | 1 zero values |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | WHOLESALE_LOW_GT_HIGH | wholesale_price_low/high | 1 | 1 rows where wholesale low > high |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | WHOLESALE_AVG_OUTSIDE_RANGE | wholesale_price_avg | 232 | 232 rows where wholesale avg outside [low, high] |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | RETAIL_AVG_OUTSIDE_RANGE | retail_price_avg | 166 | 166 rows where retail avg outside [low, high] |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | EXTREME_OUTLIER_WHOLESALE_AVG | wholesale_price_avg | 2 | 2 values outside [Q1-3*IQR, Q3+3*IQR] = [-482, 3835] |
| `DAM_POTATO_HOLLAND_RED_2010_2026.csv` | Potato (Holland) - Red | EXTREME_OUTLIER_RETAIL_AVG | retail_price_avg | 1 | 1 values outside [Q1-3*IQR, Q3+3*IQR] = [0, 42] |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | Potato (Holland) - Red (Old) | ZERO_PRICE | wholesale_price_low | 18 | 18 zero values |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | Potato (Holland) - Red (Old) | ZERO_PRICE | wholesale_price_high | 18 | 18 zero values |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | Potato (Holland) - Red (Old) | ZERO_PRICE | wholesale_price_avg | 8 | 8 zero values |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | Potato (Holland) - Red (Old) | ZERO_PRICE | retail_price_low | 19 | 19 zero values |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | Potato (Holland) - Red (Old) | ZERO_PRICE | retail_price_high | 19 | 19 zero values |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | Potato (Holland) - Red (Old) | ZERO_PRICE | retail_price_avg | 9 | 9 zero values |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | Potato (Holland) - Red (Old) | WHOLESALE_LOW_GT_HIGH | wholesale_price_low/high | 1 | 1 rows where wholesale low > high |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | Potato (Holland) - Red (Old) | WHOLESALE_AVG_OUTSIDE_RANGE | wholesale_price_avg | 72 | 72 rows where wholesale avg outside [low, high] |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | Potato (Holland) - Red (Old) | RETAIL_AVG_OUTSIDE_RANGE | retail_price_avg | 56 | 56 rows where retail avg outside [low, high] |
| `DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv` | Potato (Holland) - Red (Old) | EXTREME_OUTLIER_RETAIL_AVG | retail_price_avg | 1 | 1 values outside [Q1-3*IQR, Q3+3*IQR] = [-8, 48] |
| `DAM_POTATOES_IMPORTED_2010_2026.csv` | Potatoes-imported | WHOLESALE_LOW_GT_HIGH | wholesale_price_low/high | 1 | 1 rows where wholesale low > high |
| `DAM_POTATOES_IMPORTED_2010_2026.csv` | Potatoes-imported | WHOLESALE_AVG_OUTSIDE_RANGE | wholesale_price_avg | 11 | 11 rows where wholesale avg outside [low, high] |
| `DAM_POTATOES_IMPORTED_2010_2026.csv` | Potatoes-imported | RETAIL_AVG_OUTSIDE_RANGE | retail_price_avg | 6 | 6 rows where retail avg outside [low, high] |
| `DAM_POTATOES_IMPORTED_2010_2026.csv` | Potatoes-imported | EXTREME_OUTLIER_WHOLESALE_AVG | wholesale_price_avg | 3 | 3 values outside [Q1-3*IQR, Q3+3*IQR] = [1100, 2500] |
| `DAM_POTATOES_IMPORTED_2010_2026.csv` | Potatoes-imported | EXTREME_OUTLIER_RETAIL_AVG | retail_price_avg | 1 | 1 values outside [Q1-3*IQR, Q3+3*IQR] = [11, 32] |
| `DAM_SWEET_POTATO_2010_2026.csv` | Sweet Potato | WHOLESALE_AVG_OUTSIDE_RANGE | wholesale_price_avg | 2 | 2 rows where wholesale avg outside [low, high] |
| `DAM_SWEET_POTATO_2010_2026.csv` | Sweet Potato | RETAIL_AVG_OUTSIDE_RANGE | retail_price_avg | 2 | 2 rows where retail avg outside [low, high] |

## G. Paper 1 Sample Recommendation

### Selection Rule

- **Minimum observations per market:** 6
- **Minimum consecutive months:** 6

### Commodity Recommendations

| Commodity | Suitability | Total Obs | Markets | After Filter (mkts) | After Filter (obs) | Recommendation |
|-----------|-------------|-----------|---------|--------------------|--------------------|----------------|
| Onion (local) | **STRONG** | 911 | 97 | 68 | 831 | INCLUDE in Paper 1 sample |
| Potato (Holland) - White (New) | **STRONG** | 688 | 82 | 51 | 601 | INCLUDE in Paper 1 sample |
| Potato (Holland) - Red | **STRONG** | 452 | 52 | 38 | 418 | INCLUDE in Paper 1 sample |
| Potato (Local) | **STRONG** | 416 | 54 | 36 | 360 | INCLUDE in Paper 1 sample |
| Onion (New) | **STRONG** | 266 | 29 | 19 | 238 | INCLUDE in Paper 1 sample |
| Onion-imported | **STRONG** | 201 | 50 | 6 | 66 | INCLUDE in Paper 1 sample |
| Potato (Holland) - White (Old) | **STRONG** | 160 | 23 | 15 | 143 | INCLUDE in Paper 1 sample |
| Potato (Holland) - Red (Old) | **STRONG** | 145 | 26 | 13 | 118 | INCLUDE in Paper 1 sample |
| Potato (Local) - Old | **MODERATE** | 75 | 15 | 7 | 60 | CONSIDER for Paper 1 (supplementary / robustness) |
| Potatoes-imported | **MODERATE** | 24 | 3 | 2 | 23 | CONSIDER for Paper 1 (supplementary / robustness) |
| Sweet Potato | **WEAK** | 10 | 2 | 1 | 7 | EXCLUDE — insufficient data for panel analysis |

## H. Important Notes

> [!IMPORTANT]
> This is a DATA-QUALITY and COVERAGE audit ONLY.
> NO regression, causal analysis, weather merging, or hypothesis testing was performed.
> All original files were treated as READ-ONLY and were NOT modified.

---

## Executive Summary

- **Total observations across all 11 CSVs:** 3,348
- **Total unique markets:** 117

### Observations by Commodity

- Onion (local): 911 observations
- Potato (Holland) - White (New): 688 observations
- Potato (Holland) - Red: 452 observations
- Potato (Local): 416 observations
- Onion (New): 266 observations
- Onion-imported: 201 observations
- Potato (Holland) - White (Old): 160 observations
- Potato (Holland) - Red (Old): 145 observations
- Potato (Local) - Old: 75 observations
- Potatoes-imported: 24 observations
- Sweet Potato: 10 observations

**Strongest Onion series:** Onion (local) (911 obs, 97 markets)
**Strongest Potato series:** Potato (Local) (416 obs, 54 markets)

### Biggest Data Quality Problems

1. **WHOLESALE_AVG_OUTSIDE_RANGE**: 1900 instances
1. **RETAIL_AVG_OUTSIDE_RANGE**: 1432 instances
1. **ZERO_PRICE**: 672 instances
1. **EXTREME_OUTLIER_RETAIL_AVG**: 65 instances
1. **EXTREME_OUTLIER_WHOLESALE_AVG**: 63 instances

### Recommended Next Steps

1. **Clean adjusted-price anomalies** — investigate wholesale avg outside [low, high] range cases
2. **Handle extreme outliers** — review and decide on winsorizing vs. dropping
3. **Construct balanced panel** — apply the minimum obs + consecutive-month filter
4. **Merge weather data** — only after panel construction is finalized
5. **Begin descriptive statistics** — price distributions, seasonal patterns, market-level summaries
