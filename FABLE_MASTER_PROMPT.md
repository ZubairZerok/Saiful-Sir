# 🔬 FABLE 5.2 — MASTER RESEARCH PROMPT
## Paper 1: "Do Pre-Harvest Weather Shocks Affect Agricultural Prices? Evidence from Bangladesh"

---

> [!IMPORTANT]
> This prompt instructs you to complete **every component** of an empirical economics research paper — from raw data to publication-ready analysis and abstract — with **zero tolerance for errors**. You have full access to the GitHub repository. Every output must be reproducible, every statistical claim must be verifiable, and every methodological choice must be defensible in peer review.

---

## 📁 REPOSITORY & DATA ACCESS

**GitHub Repository:** `https://github.com/ZubairZerok/Saiful-Sir`
**Data Root:** The repository root is the project root.

### Critical File Map (Read ALL of these before doing ANY work):

| Purpose | Path |
|---|---|
| Research Questions & Hypotheses | `research-platform/Step123/step1_research_questions_and_hypotheses.md` |
| Literature Review & Method Matrix | `research-platform/Step123/step2_literature_review_and_matrix.md` |
| Data Sources Registry (35+ variables) | `research-platform/Step123/step3_data_sources_and_registry.md` |
| Data Readiness Report (Steps 4-11) | `DAM_ANALYSIS_READY_2026/FINAL_DATA_READINESS_REPORT.md` |
| AI Audit Guide | `DAM_ANALYSIS_READY_2026/STEPS_4_TO_11_AI_AUDIT_GUIDE.md` |
| Project Config | `research-platform/project.yaml` |
| Step Registry | `research-platform/step-registry.yaml` |
| Paper 1 Existing Pipeline | `PAPER_1_PRE_HARVEST_SHOCKS/run_paper_1_pipeline.py` |
| Paper 1 Econometrics (existing) | `PAPER_1_PRE_HARVEST_SHOCKS/run_econometric_models.py` |
| Paper 1 Panel Builder | `PAPER_1_PRE_HARVEST_SHOCKS/build_clean_authoritative_panel.py` |
| Forensic Audit (CRITICAL ISSUES) | `PAPER_1_PRE_HARVEST_SHOCKS/reports/PROJECT_STATE_AUDIT.md` |
| Expanded DAM Dataset (26 years) | `DAM_EXPANDED_2026/` |
| Cleaned Tiered Outputs | `DAM_ANALYSIS_READY_2026/07_outputs/` |
| DAM Extraction Script | `dam_11_commodity_extractor_FINAL.py` |
| DAM Audit | `DAM_AUDIT_2026/FINAL_AUDIT_REPORT.md` |

> [!CAUTION]
> **READ the `PROJECT_STATE_AUDIT.md` forensic report FIRST.** It documents critical flaws in the existing Paper 1 pipeline that MUST be fixed. Do NOT replicate these errors. The existing pipeline is a **starting point with known defects**, not a template to copy.

---

## 🎯 YOUR MISSION

Complete **Paper 1** through every stage before manuscript writing. Specifically, you must deliver:

1. ✅ Final authoritative empirical panel dataset
2. ✅ Complete variable construction with documentation
3. ✅ Rigorous data cleaning with full audit trail
4. ✅ Econometric specification and estimation
5. ✅ Robustness and sensitivity analysis
6. ✅ All tables and figures (publication-ready)
7. ✅ Abstract and structured findings summary
8. ✅ Complete reproducibility package

---

## 📋 PAPER 1 — RESEARCH DESIGN

### Research Question
**"Do pre-harvest weather shocks significantly affect agricultural commodity prices in Bangladesh?"**

### Sub-Questions
1. How quickly do agricultural prices respond to pre-harvest weather anomalies?
2. Does the magnitude of price response vary with the severity and type of weather shock?
3. Do onion and potato markets exhibit systematically different price sensitivities to identical weather shocks?

### Hypotheses to Test
- **H1:** Negative pre-harvest weather shocks (excess rain, heatwave, cold snap) lead to statistically significant increases in commodity prices
- **H2:** Price responses emerge within 1–3 months of the shock and dissipate within 4–6 months
- **H3:** Onion prices are more sensitive to weather shocks than potato prices (due to lower storability)
- **H4:** Markets farther from Dhaka exhibit larger price responses (spatial friction hypothesis)

### Baseline Econometric Model
```
ln(P_mct) = β · W_dct^pre + α_mc + γ_ct + δ_m · t + θ · X_mt + ε_mct
```

Where:
- `P_mct` = wholesale price (BDT/kg) in market `m`, commodity `c`, time `t`
- `W_dct^pre` = crop-calendar-specific pre-harvest weather exposure in district `d`, commodity `c`, time `t`
- `α_mc` = market × commodity fixed effect (absorbs time-invariant market-commodity heterogeneity)
- `γ_ct` = commodity × year-month fixed effect (absorbs commodity-specific seasonal/macro trends)
- `δ_m · t` = market-specific linear time trend
- `X_mt` = time-varying controls (import volume, cold storage capacity, exchange rate, CPI)
- `ε_mct` = idiosyncratic error, clustered at district level (64 clusters)

---

## 📊 PHASE 1: DATA ASSEMBLY & PANEL CONSTRUCTION

### 1.1 Price Data — Use the Expanded DAM Dataset

**DO NOT use only the 15-month API dataset (3,348 obs).** Use the **expanded historical dataset**:

- **Source:** `DAM_EXPANDED_2026/` directory
- **Master file:** `DAM_ALL_COMMODITIES_EXPANDED_2000_2026.csv` (~54MB)
- **District panel:** `DAM_DISTRICT_PANEL_2000_2026.csv` (~36MB)
- **Coverage:** 126,932 observations, 2000–2026, 324 markets, 66 districts, 13 commodities
- **Historical source:** DAM web portal scrape (121,748 records, 2000–2024)
- **Modern source:** MOA REST API (5,184 records, 2025–2026)

**Filter to Paper 1 commodities only (11 varieties):**

| ID | Commodity | Bengali Name |
|----|-----------|-------------|
| 831 | Onion (Local) | পেঁয়াজ- দেশীয় |
| 832 | Onion (Imported) | পেঁয়াজ- আমদানীকৃত |
| 833 | Onion (New) | পেঁয়াজ |
| 942 | Potato Local (Old) | |
| 943 | Potato (Local) | |
| 944 | Potato Holland White (Old) | |
| 945 | Potato Holland White (New) | |
| 946 | Potato Holland Red (Old) | |
| 947 | Potato Holland Red | |
| 948 | Sweet Potato | |
| 21014 | Potatoes (Imported) | |

### 1.2 Primary Price Variable

**Use:** `price_wholesale_raw_mid_kg` = `((w_lowestPrice + w_highestPrice) / 2) / 100`

> [!WARNING]
> **DO NOT use `w_avgPrice` as the primary variable.** The forensic audit (Step 6) proved that `w_avgPrice` is the midpoint of DAM's internally adjusted quotes, NOT the raw midpoint. It introduces opaque institutional smoothing. Use it only as a robustness alternative (`price_wholesale_dam_avg_kg`).

**Dependent variable in regressions:** `ln(price_wholesale_raw_mid_kg)` — natural log transformation.

### 1.3 Weather Data Acquisition

You must acquire and process weather data for **all 64 districts of Bangladesh** at **monthly frequency** for the full sample period (2000–2026).

**Primary weather source: ERA5-Land** (ECMWF Copernicus Climate Data Store)
- Resolution: 0.1° × 0.1° gridded
- Variables needed:
  - `2m_temperature` (hourly → compute monthly mean, min, max)
  - `total_precipitation` (hourly → aggregate to monthly total in mm)
- Temporal: Monthly means/totals, 2000–2026
- Spatial: Aggregate grid cells to 64 Bangladesh districts using district polygon boundaries

**Secondary rainfall: CHIRPS** (Climate Hazards Center, UCSB)
- Resolution: 0.05° × 0.05°
- Variable: Monthly precipitation (mm)
- Use for rainfall robustness cross-validation

**District boundary shapefiles:** Use GADM Level 2 for Bangladesh (64 districts) or the GeoJSON files already in `PAPER_1_PRE_HARVEST_SHOCKS/data/geo/`.

**Processing steps:**
1. Download ERA5-Land monthly data for Bangladesh bounding box (20.5°N–26.7°N, 88.0°E–92.7°E)
2. Clip to Bangladesh national boundary
3. Compute area-weighted district-level monthly averages using district polygons
4. Output: `weather_district_monthly.csv` with columns: `district_id`, `year`, `month`, `precip_mm`, `tmean_c`, `tmin_c`, `tmax_c`

**If ERA5 API access is unavailable**, use the existing weather data in `PAPER_1_PRE_HARVEST_SHOCKS/data/weather/` but document the source and verify coverage for all 64 districts × all months.

### 1.4 Crop Calendar — CRITICAL FOR IDENTIFICATION

The entire identification strategy depends on correctly defining "pre-harvest" windows. These are **crop-specific and region-specific**.

**Bangladesh Rabi Season Crop Calendar (Onion & Potato):**

| Stage | Onion | Potato |
|-------|-------|--------|
| Land Preparation | October | October |
| Planting/Sowing | November | November |
| Vegetative Growth | December–January | December |
| Bulbing/Tuberization | January–February | January |
| Maturation | February–March | February |
| Harvest | March–April | February–March |
| Marketing Peak | April–June | March–May |

**Pre-Harvest Window Definition:**
- **Onion:** October (t) through March (t+1) — 6-month pre-harvest exposure
- **Potato:** October (t) through February (t+1) — 5-month pre-harvest exposure

> [!IMPORTANT]
> **The marketing year runs from Harvest(t) through Harvest(t+1).** For example, onion harvested in March 2020 is marketed from April 2020 through approximately March 2021. The relevant pre-harvest weather is October 2019 through March 2020. You MUST align weather shocks to the correct marketing year, not the calendar year.

### 1.5 Weather Anomaly Construction

**Step 1: Compute Historical Climate Normals (1991–2020 baseline)**
For each district `d` and calendar month `m`:
```
μ_precip(d,m) = mean(precip_mm) over 1991–2020
σ_precip(d,m) = sd(precip_mm) over 1991–2020
μ_temp(d,m) = mean(tmean_c) over 1991–2020
σ_temp(d,m) = sd(tmean_c) over 1991–2020
```

**Step 2: Compute Z-scores for each district-month observation**
```
z_precip(d,t) = (precip(d,t) − μ_precip(d,m(t))) / σ_precip(d,m(t))
z_temp(d,t) = (tmean(d,t) − μ_temp(d,m(t))) / σ_temp(d,m(t))
```

**Step 3: Define Shock Indicators**
```
excess_rain_shock(d,t) = 1 if z_precip(d,t) > +1.5
drought_shock(d,t) = 1 if z_precip(d,t) < −1.5
heatwave_shock(d,t) = 1 if z_temp(d,t) > +1.5
cold_shock(d,t) = 1 if z_temp(d,t) < −1.5
any_shock(d,t) = max(excess_rain, drought, heatwave, cold)
```

> [!CAUTION]
> **DO NOT use a single static annual shock indicator.** The existing pipeline used one binary `ph_any_shock` per marketing year — this violates the event-study premise and caused the placebo lead test to fail. Instead, construct **monthly** shock indicators and aggregate over the pre-harvest window using:
> 
> **Option A (Preferred): Cumulative pre-harvest shock intensity**
> ```
> PH_shock_intensity(d,c,t) = Σ_{s ∈ pre-harvest months} any_shock(d,s)
> ```
> This counts the NUMBER of shocked months during the pre-harvest window (0 to 5 or 6).
> 
> **Option B: Maximum shock severity**
> ```
> PH_max_z_precip(d,c,t) = max_{s ∈ pre-harvest months} |z_precip(d,s)|
> PH_max_z_temp(d,c,t) = max_{s ∈ pre-harvest months} |z_temp(d,s)|
> ```

### 1.6 Control Variables

Acquire and merge the following:

| Variable | Source | Frequency | Notes |
|----------|--------|-----------|-------|
| Onion import volume (MT) | NBR/Customs (HS 070310) | Monthly | Key supply shifter |
| Potato cold storage capacity | DAM Cold Storage Reports | Annual | Storage buffer proxy |
| Exchange rate (BDT/USD) | Bangladesh Bank | Monthly | Import cost channel |
| CPI (Food sub-index) | BBS | Monthly | General inflation control |
| Distance to Dhaka (km) | Computed from geocoordinates | Time-invariant | Spatial friction variable |
| District crop production (MT) | BBS | Annual | Production weight / exposure |

**For distance_to_Dhaka:** Compute geodesic distance from each market's district centroid to Dhaka (23.8103°N, 90.4125°E). Use the centroid coordinates already available in `PAPER_1_PRE_HARVEST_SHOCKS/data/geo/district_centroids.csv` or compute from GADM polygons.

**If some control variables are unavailable:** Document what was unavailable, use what IS available, and note the omission as a limitation. Do NOT fabricate control data.

### 1.7 Panel Merge

Construct the final panel by merging:

1. **Price panel** (market × commodity × month): From expanded DAM dataset, aggregated to monthly frequency (use monthly median price to reduce noise from daily variation)
2. **Weather panel** (district × month): ERA5-Land derived
3. **Controls** (various frequencies, merged by appropriate key)

**Merge keys:**
- Price ↔ Weather: via `district_id` (each market maps to a district)
- Price ↔ Controls: via `month` or `year` as appropriate

**Final panel structure:**
```
observation = market_id × commodity_id × year_month
```

**Expected dimensions:** ~100,000+ observations (depending on market-commodity-month coverage after cleaning)

---

## 🧹 PHASE 2: DATA CLEANING & QUALITY ASSURANCE

### 2.1 Apply Existing Quality Flags

The 14 boolean quality flags from Steps 5–9 have already been computed and are embedded in the tiered output files:

- `flag_zero_wholesale`, `flag_zero_retail`
- `flag_inverted_wholesale`, `flag_inverted_retail`
- `flag_outlier_wholesale`, `flag_outlier_retail`
- `flag_extreme_wholesale`, `flag_extreme_retail`
- `flag_data_entry_error`
- `flag_concat_digits`
- `flag_suspicious_w_avg`
- (and others defined in the cleaning protocol)

**Use the PRIMARY_ANALYSIS tier** (excludes 171 corrupted rows = 94.89% retention) as the baseline sample.

### 2.2 Additional Cleaning for Expanded Dataset

The expanded 2000–2026 dataset has NOT gone through the same 11-step audit. You must:

1. **Apply the same zero-price, outlier, and extreme value checks** used in Steps 5–9
2. **Flag and exclude** observations where `w_lowestPrice == 0` OR `w_highestPrice == 0`
3. **Flag inversions** where `w_lowestPrice > w_highestPrice`
4. **Detect and flag extreme outliers** using IQR method: flag if price > Q3 + 3×IQR or price < Q1 − 3×IQR (within each commodity)
5. **Check for duplicates** on key `(market_id, commodity_id, price_date)`
6. **Handle the 2024 data gap:** The forensic audit identified a complete institutional gap in DAM data for 2024. Verify this gap exists in the expanded dataset. If confirmed, document it but do NOT interpolate across it — treat 2024 as missing.

### 2.3 Missing Data Strategy

- **Price data:** Do NOT impute missing prices. Missing market-commodity-months are simply unobserved (unbalanced panel is fine with FE estimators)
- **Weather data:** Should have no missing values if ERA5-Land is used correctly (gridded reanalysis). If station data has gaps, use spatial interpolation or MICE imputation with 5+ chains (document the method)
- **Controls:** If monthly import data has gaps, use linear interpolation for ≤3 consecutive months. For larger gaps, use annual totals prorated to months.

### 2.4 Sample Construction

**Primary sample (Paper 1):**
- All market × commodity × month observations in PRIMARY_ANALYSIS tier
- Exclude imported commodities (832, 21014) from baseline — they respond to international not local weather
- Include imported commodities in robustness check (expecting null weather effect = placebo)

**Sensitivity sample:**
- STRICT_SENSITIVITY tier (81.27% retention, ≥6 month balanced panel)
- Use for robustness of main results

---

## 📐 PHASE 3: ECONOMETRIC SPECIFICATION & ESTIMATION

### 3.1 Model Hierarchy

Estimate the following models **in sequence**, building complexity:

#### Model 1: Baseline Panel Fixed Effects
```python
# Y = ln(price_wholesale_raw_mid_kg)
# X = pre-harvest shock intensity (count of shocked months)
Y ~ PH_shock_intensity + C(market_id:commodity_id) + C(commodity_id:year_month)
# Cluster SEs at district level (64 clusters)
```

#### Model 2: Decomposed Shock Types
```python
Y ~ PH_excess_rain_intensity + PH_drought_intensity + PH_heatwave_intensity + PH_cold_intensity
  + C(market_id:commodity_id) + C(commodity_id:year_month)
```

#### Model 3: Commodity Subsamples
```python
# Run Model 1 separately for:
# (a) All onion varieties (831, 833) — exclude imported 832
# (b) All potato varieties (942-948) — exclude imported 21014
# (c) Brinjal if included (949, 950)
```

#### Model 4: Spatial Friction Interaction
```python
Y ~ PH_shock_intensity + PH_shock_intensity × ln(distance_to_dhaka_km)
  + C(market_id:commodity_id) + C(commodity_id:year_month)
```

#### Model 5: Distributed Lag (Event Study)
```python
# Include leads and lags of shock:
Y ~ shock(t-3) + shock(t-2) + shock(t-1) + shock(t) + shock(t+1) + shock(t+2) + shock(t+3)
  + C(market_id:commodity_id) + C(commodity_id:year_month)
# Plot coefficients with 95% CI → event-study figure
# Pre-trend leads (t-3, t-2, t-1) should be ≈0 and insignificant
```

#### Model 6: Retail Price Pass-Through
```python
ln(retail_price) ~ ln(wholesale_price) + PH_shock_intensity
  + C(market_id:commodity_id) + C(commodity_id:year_month)
# Tests vertical transmission of weather shock through supply chain
```

#### Model 7: Severity Non-Linearity
```python
Y ~ PH_shock_intensity + PH_shock_intensity² 
  + C(market_id:commodity_id) + C(commodity_id:year_month)
# Or: use binned dummies for 0, 1, 2, 3+ shocked months
```

### 3.2 Estimation Requirements

**Software:** Python with `linearmodels` (for panel FE), `statsmodels`, `numpy`, `pandas`, `scipy`
- If `linearmodels` is unavailable, use `statsmodels` OLS with dummy variables or the Frisch-Waugh-Lovell theorem for absorbing fixed effects
- For very large FE sets, use the `pyhdfe` package for high-dimensional fixed effect absorption

**Standard Errors:**
- **Primary:** Cluster-robust at **district level** (64 clusters). This accounts for spatial correlation within districts.
- **Robustness:** Two-way clustering by district AND year-month (Cameron, Gelbach & Miller, 2011)
- **Report:** Both cluster-robust and heteroskedasticity-robust SEs

**Fixed Effects Absorption:**
- Market × Commodity FE: ~324×11 = 3,564 potential groups (fewer in practice)
- Commodity × Year-Month FE: ~11×312 = 3,432 potential groups (26 years × 12 months)
- These are HIGH-DIMENSIONAL — use absorption/demeaning, not dummy variable OLS

### 3.3 Placebo & Pre-Trend Tests

> [!CAUTION]
> **The existing pipeline's placebo lead test FAILED** (lead shock significant at 1%, β=+0.0232, p=0.0018). This is a FATAL flaw for causal identification. You MUST fix this.

**Diagnosis of the failure:**
The failure was caused by using a **static annual binary** shock indicator that mechanically correlates with lead prices because it pools across the entire marketing year. Switching to **monthly cumulative shock intensity** with correct crop-calendar alignment should resolve this.

**Required tests:**
1. **Event-study leads test:** In Model 5, coefficients on shock(t-1), shock(t-2), shock(t-3) must be jointly insignificant (F-test p > 0.10)
2. **Placebo commodity test:** Run Model 1 on imported onion (832) and imported potato (21014). These should show NO significant weather effect (they respond to international supply, not local weather).
3. **Placebo season test:** Assign random pre-harvest windows (wrong crop calendar) and re-estimate. Should show no significant effect.
4. **If pre-trend test still fails after fixing the shock specification:** This is a serious problem. Report it honestly and consider:
   - Adding market-specific linear trends
   - Using first-differences instead of levels
   - Checking for anticipatory price adjustment through futures/forward markets

### 3.4 Robustness & Sensitivity Checks

Run ALL of these:

| Check | Description |
|-------|-------------|
| Alternative price variable | Use `price_wholesale_dam_avg_kg` instead of midpoint |
| Alternative sample | Use STRICT_SENSITIVITY tier |
| Alternative shock threshold | Use ±1.0 SD and ±2.0 SD instead of ±1.5 SD |
| Alternative weather source | CHIRPS rainfall instead of ERA5 |
| Including imported varieties | Should show null effect (placebo) |
| Two-way clustering | District × Year-Month clusters |
| Winsorized prices | Winsorize at 1st/99th percentile instead of trimming |
| Excluding 2024 gap | Verify results hold excluding observations near the gap |
| Adding market-specific trends | Test sensitivity to trend specification |
| First-differences | ΔY ~ ΔShock + ... instead of levels with FE |
| SPEI instead of z-scores | Standardized Precipitation-Evapotranspiration Index (following Letta et al. 2022) |

---

## 📊 PHASE 4: TABLES & FIGURES

### Required Tables

**Table 1: Descriptive Statistics**
- Panel A: Price variables (mean, SD, min, p25, median, p75, max, N) by commodity group
- Panel B: Weather variables (mean, SD, min, max) by district-month
- Panel C: Sample composition (markets, districts, commodities, time span, total obs)

**Table 2: Main Results — Baseline and Decomposed Shocks**
- Column 1: Model 1 (aggregate shock intensity)
- Column 2: Model 2 (decomposed: excess rain, drought, heatwave, cold)
- Column 3: Model 1 on onion subsample
- Column 4: Model 1 on potato subsample
- Bottom rows: N, R², number of FE groups, cluster count

**Table 3: Spatial Friction and Non-Linearity**
- Column 1: Model 4 (distance interaction)
- Column 2: Model 7 (severity non-linearity)
- Column 3: Combined

**Table 4: Robustness Checks**
- Each row = one robustness variant
- Columns: coefficient, SE, p-value, N, notes

**Table 5: Retail Pass-Through (Model 6)**

### Required Figures

**Figure 1: Map of Bangladesh markets and districts**
- Choropleth map of Bangladesh showing district boundaries, market locations, and average price levels
- Use the GeoJSON files in the repo

**Figure 2: Time series of prices and weather**
- Panel A: Monthly average wholesale price by commodity group (onion vs potato), 2000–2026
- Panel B: Monthly average precipitation anomaly (z-score) across districts
- Panel C: Monthly average temperature anomaly (z-score) across districts
- Highlight the 2024 data gap with shading

**Figure 3: Event-Study Plot (Model 5)**
- X-axis: months relative to shock (t-3 to t+3)
- Y-axis: coefficient estimates with 95% CI
- Reference line at 0
- Pre-trend coefficients should be ≈0 (visual parallel trends test)

**Figure 4: Seasonal price patterns and crop calendar**
- Monthly boxplots of prices by calendar month, overlaid with crop calendar annotations (planting, growth, harvest, marketing seasons)

**Figure 5: Spatial heterogeneity**
- Scatter plot or binned plot: distance to Dhaka vs. shock coefficient (from Model 4)
- Or: Map with district-level estimated shock effects

### Formatting Requirements
- All figures: 300 DPI, PDF + PNG format
- All tables: CSV + LaTeX format
- Use consistent color scheme: Blues for precipitation, Reds for temperature, Greens for price
- Font: Computer Modern or Times New Roman for LaTeX compatibility
- All figures must include axis labels, titles, legends, and source notes

---

## 📝 PHASE 5: ABSTRACT & FINDINGS SUMMARY

### Write a Publication-Quality Abstract

**Structure (250 words max):**
1. **Motivation** (2 sentences): Why this matters — climate change + food security + Bangladesh vulnerability
2. **Research question** (1 sentence): State the precise causal question
3. **Data** (2 sentences): Describe the DAM panel (years, markets, commodities, weather source)
4. **Method** (2 sentences): Panel fixed effects with crop-calendar-specific pre-harvest weather exposure, identification strategy
5. **Key findings** (3–4 sentences): Main coefficient interpretation, commodity heterogeneity, spatial patterns
6. **Implications** (1–2 sentences): Policy relevance — early warning systems, strategic reserves, import timing

### Structured Findings Summary

Create a detailed findings document (`PAPER_1_FINDINGS.md`) with:

1. **Key Result 1:** Overall pre-harvest shock effect on prices (magnitude, significance, interpretation)
2. **Key Result 2:** Decomposed shock effects (which type matters most?)
3. **Key Result 3:** Onion vs. potato differential response
4. **Key Result 4:** Spatial friction (distance to Dhaka interaction)
5. **Key Result 5:** Event-study dynamics (timing of price response)
6. **Key Result 6:** Retail pass-through rate
7. **Placebo tests:** Report results honestly
8. **Robustness:** Summary of which results survive and which are fragile
9. **Comparison to Letta et al. (2022):** How do your Bangladesh results compare to their India findings?

---

## 🔧 PHASE 6: REPRODUCIBILITY PACKAGE

### Create a Complete Pipeline Script

Create `PAPER_1_FINAL/run_complete_pipeline.py` that:
1. Loads raw data from `DAM_EXPANDED_2026/` and weather sources
2. Constructs all variables
3. Applies all cleaning steps
4. Builds the final panel
5. Runs all econometric models
6. Generates all tables and figures
7. Writes the abstract and findings summary
8. Produces a SHA-256 manifest of all output files

**Directory structure for outputs:**
```
PAPER_1_FINAL/
├── run_complete_pipeline.py
├── data/
│   ├── raw/                  # Symlinks or references to source data
│   ├── intermediate/         # Cleaned and merged panels
│   └── final/               # Analysis-ready panel
│       └── paper_1_panel.csv
├── analysis/
│   ├── models/              # Saved model objects / results
│   ├── tables/              # CSV + LaTeX tables
│   └── figures/             # PDF + PNG figures
├── docs/
│   ├── ABSTRACT.md
│   ├── PAPER_1_FINDINGS.md
│   ├── VARIABLE_CODEBOOK.md
│   ├── CLEANING_LOG.md
│   └── METHODOLOGY_NOTES.md
├── robustness/
│   ├── alternative_specs/
│   └── placebo_tests/
├── requirements.txt
├── SHA256_MANIFEST.txt
└── README.md
```

### Variable Codebook

Create `VARIABLE_CODEBOOK.md` documenting EVERY variable in the final panel:
- Variable name
- Definition (precise formula)
- Source
- Unit
- Type (continuous/binary/categorical)
- Expected range
- Notes/caveats

---

## ⚠️ CRITICAL RULES — DO NOT VIOLATE

1. **NEVER fabricate data.** If a data source is unavailable, document it as a limitation. Do NOT generate synthetic weather data, fake control variables, or placeholder values.

2. **NEVER ignore the placebo test failure.** If the pre-trend test still fails after fixing the shock specification, you must report this honestly and discuss implications for causal interpretation.

3. **ALWAYS use the correct crop calendar.** The entire identification strategy depends on this. Onion and potato have DIFFERENT pre-harvest windows.

4. **ALWAYS cluster standard errors at the district level (64 clusters).** Do not use market-level clustering (too many clusters → over-rejection) or national-level (too few → under-powered).

5. **ALWAYS use PRIMARY_ANALYSIS tier** as the default sample. STRICT_SENSITIVITY is for robustness only.

6. **ALWAYS compute and report the R² WITHIN** (within fixed effects), not the overall R² which is inflated by FE absorption.

7. **ALWAYS report the number of observations, number of FE groups, and number of clusters** in every regression table.

8. **DO NOT use `w_avgPrice` as the primary price variable.** It contains opaque DAM institutional adjustments.

9. **DO NOT treat imported commodities (832, 21014) the same as domestic.** They should be excluded from baseline and used as placebos.

10. **DO NOT interpolate across the 2024 data gap.** Treat it as institutional missing data.

11. **EVERY number you report must be traceable** to a specific line in a specific data file through the pipeline script.

12. **Use Python for ALL analysis.** The existing pipeline is Python-based. Maintain consistency.

13. **Save ALL intermediate outputs** so every step is independently verifiable.

14. **Document EVERY methodological choice** — why that threshold, why that sample restriction, why that specification.

---

## 🚀 EXECUTION ORDER

1. **Read ALL reference documents** listed in the file map above
2. **Verify and extend the price panel** from expanded DAM data
3. **Acquire/verify weather data** for all 64 districts
4. **Construct weather anomalies** with correct crop-calendar alignment
5. **Merge price + weather + controls** into final panel
6. **Apply cleaning and construct sample tiers**
7. **Run descriptive statistics** (Table 1, Figures 1-2, 4)
8. **Estimate baseline model** (Model 1) and verify pre-trends
9. **If pre-trends pass:** proceed with full model hierarchy
10. **If pre-trends fail:** diagnose, fix specification, re-estimate
11. **Run all robustness checks**
12. **Generate all tables and figures**
13. **Write abstract and findings summary**
14. **Create reproducibility package with manifest**
15. **Final self-audit:** Re-read the forensic audit report and verify you have not replicated any of the documented flaws

---

## 📚 KEY LITERATURE BENCHMARKS

Your results should be interpretable in context of:

1. **Letta, Montalbano & Pierre (2022)** — Temperature shocks and agricultural prices in India. This is the closest methodological comparison.
2. **Burke & Lobell (2017)** — Satellite-based yield impacts of climate change
3. **Dell, Jones & Olken (2014)** — Weather shocks and economic outcomes (methodological framework)
4. **Auffhammer & Schlenker (2014)** — Empirical studies on weather and agriculture
5. **Guiteras (2009)** — Climate change impacts on Indian agriculture

Compare your effect sizes, significance levels, and patterns to these benchmarks.

---

**END OF PROMPT. Begin execution.**
