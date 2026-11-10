# Econometric Cleaning Protocol for Analysis-Ready DAM Price Datasets

## 1. Principles of Scientific Data Preparation
This protocol establishes an immutable, defensible cleaning and standardization standard for agricultural market price data collected by the Department of Agricultural Marketing (DAM), Ministry of Agriculture, Bangladesh.

### Core Safeguards:
1. **Zero Raw Mutation:** Raw source CSVs and original JSON responses are permanently read-only.
2. **Zero Price Fabrication:** No missing prices are interpolated, imputed from neighboring markets, or smoothed using synthetic models.
3. **Explicit Row-Level Traceability:** Every transformation and exclusion is tracked by `row_id` and `cpi_market_commodity_price_id`.

---

## 2. Standardized Price Variables
To eliminate unit ambiguity across wholesale (BDT/Quintal = 100 kg) and retail (BDT/kg), the pipeline generates standardized per-kilogram price metrics:

1. **`price_wholesale_raw_mid_kg`** $= \frac{\text{wholesale\_price\_low} + \text{wholesale\_price\_high}}{2 \times 100}$  
   *Primary outcome variable for Papers 1 & 2.* Direct reflection of local market trading quotes.
2. **`price_wholesale_dam_avg_kg`** $= \frac{\text{wholesale\_price\_avg}}{100}$  
   *Official DAM headline wholesale average.* Incorporates central benchmark calibrations.
3. **`price_retail_raw_mid_kg`** $= \frac{\text{retail\_price\_low} + \text{retail\_price\_high}}{2}$  
   *Direct local retail price quote midpoint.*
4. **`price_retail_dam_avg_kg`** $= \text{retail\_price\_avg}$  
   *Official DAM retail headline average.*
5. **`wholesale_retail_spread_kg`** $= \text{price\_retail\_raw\_mid\_kg} - \text{price\_wholesale\_raw\_mid\_kg}$  
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
  1. $\text{wholesale\_price\_low} > 0$ and $\text{wholesale\_price\_high} > 0$ (excludes non-trading zero records).
  2. $\text{wholesale\_price\_low} \le \text{wholesale\_price\_high}$ (excludes inverted data-entry errors).
  3. $\text{retail\_price\_low} \le \text{retail\_price\_high}$ (excludes inverted retail errors).
  4. $\text{wholesale\_price\_low} \le 15,000$ BDT/quintal (150 BDT/kg) and $\text{retail\_price\_low} \le 150$ BDT/kg (excludes extreme typing anomalies such as 19001700 or 350000).
- **Treatment of Adjusted Averages:** Retains observations where raw reported bounds are valid even if DAM's backend adjustment algorithm produced an adjusted spike, because raw price midpoints remain uncontaminated.

### Tier C: STRICT_SENSITIVITY
- **Contents:** Balanced panel subset for dynamic panel regressions and spatial price transmission models.
- **Inclusion Rules:**
  1. Satisfies all Tier B (PRIMARY_ANALYSIS) criteria.
  2. Belongs to a market $\times$ commodity series with **$\ge 6$ consecutive monthly observations**.
  3. Excludes fragmented, sporadic market appearances.
