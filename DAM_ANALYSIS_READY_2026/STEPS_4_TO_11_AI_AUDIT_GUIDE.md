# Forensic & Econometric AI Audit Guide: Steps 4 to 11

This document provides an explicit, file-by-file audit blueprint for an AI or external econometric auditor to inspect, verify, and stress-test the completed data preparation pipeline in `DAM_ANALYSIS_READY_2026/` and `dam_output/`.

---

## Executive Summary of Pipeline Accounting

| Step | Phase Name | Primary Files to Audit | What the Auditor/AI Must Verify | Expected Audit Outcome |
|---|---|---|---|---|
| **Step 4** | **Data Extraction** | `dam_output/master/*.csv` (12 files)<br>`dam_output/market_master.csv`<br>`dam_output/coverage_matrix.csv` | 1. 11 commodity varieties + 1 combined master CSV.<br>2. Exactly 3,348 rows across 117 markets.<br>3. 0 duplicate `(market_id, commodity_id, price_date)` keys. | **Verified Raw Baseline:** June 2025 to August 2026 span. No pre-June-2025 data exists in the active DAM endpoint. |
| **Step 5** | **Data Inventory & Structural Audit** | `01_inventory/dataset_inventory.csv`<br>`01_inventory/column_inventory.csv`<br>`01_inventory/duplicate_report.csv`<br>`01_inventory/missingness_report.csv`<br>`01_inventory/structural_issues.csv` | 1. Uniform 39 columns across all files.<br>2. Confirm 0 duplicate rows in `duplicate_report.csv`.<br>3. Missingness check: `district_name` & `upazila_name` are 100% null strings, but integer `district_id` & `upazila_id` are 100% complete. | **Structurally Valid:** All numeric price fields parse into floats; all dates parse into ISO-8601 `YYYY-MM-DD`. |
| **Step 6** | **Price Field Semantics & Forensics** | `02_price_semantics/price_field_semantics.csv`<br>`02_price_semantics/price_field_definition_report.md` | 1. **The Semantic Resolution:** Verify whether `wholesale_price_avg` is the midpoint of raw prices or adjusted prices.<br>2. Mathematical formula verification: `round((a_w_lowestPrice + a_w_highestPrice)/2)`.<br>3. Unit definitions: Wholesale = BDT/Quintal (100 kg); Retail = BDT/kg. | **Proven:** `w_avgPrice` matches adjusted price midpoint in **96.7% of rows** within ±1 Tk rounding tolerance. |
| **Step 7** | **Quality Audit & Anomaly Detection** | `03_quality_audit/row_level_quality_flags.csv`<br>`03_quality_audit/extreme_observation_forensics.csv`<br>`03_quality_audit/zero_price_report.csv`<br>`03_quality_audit/impossible_value_report.csv`<br>`03_quality_audit/outlier_report.csv` | 1. Check all 14 boolean quality flags.<br>2. Audit 171 corrupted observations (144 wholesale zeros, 13 inverted low>high quotes, 14 extreme data entry typos like Gopaldanj `19001700` and Kaptai `350000`).<br>3. Check forensic traces back to raw JSON files. | **100% Traceability:** Exactly 171 rows (5.11%) excluded from primary analysis with documented row-level reasons. |
| **Step 8** | **Geographic & Temporal Validation** | `04_geography/market_master.csv`<br>`04_geography/geography_validation_report.md`<br>`05_temporal/continuous_series_report.csv`<br>`05_temporal/temporal_coverage_by_market.csv`<br>`05_temporal/monthly_coverage.csv` | 1. Division resolution: 8 of 8 divisions (100% complete).<br>2. Market directory: 117 unique markets mapped.<br>3. Temporal coverage: 15 continuous months (June 2025 – August 2026), capturing the full 2025/2026 Rabi cropping cycle. | **Complete Spatial Coverage:** No spatial fabrication or speculative geocoding. |
| **Step 9** | **Cleaning Protocol & Dataset Tiers** | `06_cleaning_rules/CLEANING_PROTOCOL.md`<br>`07_outputs/FULL_FLAGGED/*.csv` (12 files)<br>`07_outputs/PRIMARY_ANALYSIS/*.csv` (12 files)<br>`07_outputs/STRICT_SENSITIVITY/*.csv` (12 files) | 1. Verify exact row counts across tiers:<br>   - `FULL_FLAGGED`: 3,348 rows (100%)<br>   - `PRIMARY_ANALYSIS`: 3,177 rows (94.89%)<br>   - `STRICT_SENSITIVITY`: 2,721 rows (81.27%)<br>2. Standardized price variables: `price_wholesale_raw_mid_kg`, `price_retail_raw_mid_kg`, `wholesale_retail_spread_kg`. | **Econometrically Sound:** 36 output CSVs generated deterministically with zero raw data mutation. |
| **Step 10** | **Panel Readiness & Sample Construction** | `08_panel_readiness/market_pair_overlap.csv`<br>`08_panel_readiness/onion_panel_readiness.csv`<br>`08_panel_readiness/potato_panel_readiness.csv`<br>`08_panel_readiness/paper1_sample_candidates.csv`<br>`08_panel_readiness/paper2_sample_candidates.csv`<br>`08_panel_readiness/paper3_sample_candidates.csv` | 1. Calculate bilateral market pairs with ≥ 6, ≥ 12 co-observed months.<br>2. Confirm sample size for Paper 2: 5,500+ bilateral pairs; 990 local onion pairs with 12-month continuous observations.<br>3. Confirm balanced panel criteria for Paper 1 and Paper 3. | **Analysis Ready for Dyadic Panels:** High statistical power for spatial price dispersion modeling. |
| **Step 11** | **Research Readiness Evaluation & Manifest** | `09_research_readiness/overall_research_readiness.md`<br>`09_research_readiness/paper1_readiness.md`<br>`09_research_readiness/paper2_readiness.md`<br>`09_research_readiness/paper3_readiness.md`<br>`FINAL_DATA_READINESS_REPORT.md`<br>`11_manifest/sha256_checksums.txt`<br>`10_code/run_full_pipeline.py` | 1. Verify answers to the 16 mandatory forensic questions.<br>2. Verify SHA-256 hash match for all 12 raw source files.<br>3. Re-run `python 10_code/run_full_pipeline.py` to test 100% reproducibility in clean runtime (~6.7s). | **Validated:** Paper 2 is "Analysis Ready"; Papers 1 & 3 are "Ready with Conditions" (fixed-effects panel specifications). |

---

## How to Instruct an External AI to Audit These Files

Copy and paste the prompt below into any frontier AI model (such as Claude, ChatGPT, or Gemini) along with the files:

```markdown
You are an expert econometric auditor, agricultural economist, and data forensics specialist.
Audit the following files from the DAM_ANALYSIS_READY_2026 dataset:
1. FINAL_DATA_READINESS_REPORT.md
2. 02_price_semantics/price_field_definition_report.md
3. 03_quality_audit/extreme_observation_forensics.csv
4. 06_cleaning_rules/CLEANING_PROTOCOL.md
5. 08_panel_readiness/market_pair_overlap.csv
6. 11_manifest/sha256_checksums.txt

Check and answer:
- Is the distinction between raw price midpoints and DAM adjusted prices mathematically verified?
- Are the exclusion criteria for the 171 corrupted observations scientifically justified?
- Are the three dataset tiers (FULL_FLAGGED, PRIMARY_ANALYSIS, STRICT_SENSITIVITY) properly stratified?
- Is Paper 2 (Spatial Price Dispersion) genuinely ready with 5,500+ bilateral market pairs?
- Is there any evidence of data fabrication, speculative imputation, or unlogged mutation?
```
"""
