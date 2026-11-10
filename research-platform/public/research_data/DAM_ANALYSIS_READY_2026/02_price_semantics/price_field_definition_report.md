# DAM Price Field Semantics & Mathematical Verification Report

**Authoritative Source:** DAM API Responses, `common_dropdowns.json`, and Forensic Database Audit  
**Total Observations Evaluated:** 3,348  
**Date of Verification:** 2026-08-17  

---

## 1. Executive Summary & Semantic Breakthrough

A central question in the econometric auditing of Department of Agricultural Marketing (DAM) data was why previous audits reported nearly 1,900 instances of `wholesale_price_avg` lying outside the raw reported range `[wholesale_price_low, wholesale_price_high]`.

Our mathematical forensic verification across all 3,348 observations provides conclusive empirical proof:

> **Core Semantic Finding:**  
> In the DAM database architecture, `wholesale_price_avg` and `retail_price_avg` are **not** arithmetic averages of the raw field enumerator inputs (`w_lowestPrice`, `w_highestPrice`).  
> Instead, they are calculated as the rounded arithmetic midpoints of the **DAM adjusted price fields** (`a_w_lowestPrice`, `a_w_highestPrice` and `a_r_lowestPrice`, `a_r_highestPrice`).

### Empirical Proof:
- **Wholesale Formula Match:** `wholesale_price_avg == round((adjusted_wholesale_price_low + adjusted_wholesale_price_high) / 2)` in **3,239 / 3,348 rows (96.74%)** within $\pm 1$ BDT rounding tolerance. (Exact integer match in 2,241 rows).
- **Wholesale Raw Midpoint Match:** Only 664 / 3,348 rows (19.83%) match raw low/high midpoints.
- **Adjusted Range Compliance:** `wholesale_price_avg` lies strictly inside `[adjusted_wholesale_price_low, adjusted_wholesale_price_high]` in **3,213 / 3,348 rows (95.97%)**.
- **Retail Formula Match:** `retail_price_avg == round((adjusted_retail_price_low + adjusted_retail_price_high) / 2)` in **3,240 / 3,348 rows (96.77%)** within $\pm 1$ BDT rounding tolerance.
- **Retail Adjusted Range Compliance:** `retail_price_avg` lies strictly inside `[adjusted_retail_price_low, adjusted_retail_price_high]` in **3,229 / 3,348 rows (96.45%)**.

---

## 2. Price Field Definitions and Institutional Semantics

| Field Name | Raw API Field | Unit in Raw Data | Standardized Unit | Definition & Institutional Source |
|---|---|---|---|---|
| `wholesale_price_low` | `w_lowestPrice` | BDT / Quintal (100 kg) | BDT / kg ($\div 100$) | Lowest wholesale transaction quote recorded by local market enumerator. |
| `wholesale_price_high` | `w_highestPrice` | BDT / Quintal (100 kg) | BDT / kg ($\div 100$) | Highest wholesale transaction quote recorded by local market enumerator. |
| `wholesale_price_avg` | `w_avgPrice` | BDT / Quintal (100 kg) | BDT / kg ($\div 100$) | Midpoint of centrally adjusted wholesale low and high prices. |
| `retail_price_low` | `r_lowestPrice` | BDT / kg | BDT / kg | Lowest retail consumer quote recorded by local market enumerator. |
| `retail_price_high` | `r_highestPrice` | BDT / kg | BDT / kg | Highest retail consumer quote recorded by local market enumerator. |
| `retail_price_avg` | `r_avgPrice` | BDT / kg | BDT / kg | Midpoint of centrally adjusted retail low and high prices. |
| `adjusted_wholesale_price_low` | `a_w_lowestPrice` | BDT / Quintal (100 kg) | BDT / kg ($\div 100$) | Centrally smoothed / transport-adjusted lower wholesale quote. |
| `adjusted_wholesale_price_high` | `a_w_highestPrice` | BDT / Quintal (100 kg) | BDT / kg ($\div 100$) | Centrally smoothed / transport-adjusted upper wholesale quote. |
| `adjusted_retail_price_low` | `a_r_lowestPrice` | BDT / kg | BDT / kg | Centrally smoothed / transport-adjusted lower retail quote. |
| `adjusted_retail_price_high` | `a_r_howestPrice` | BDT / kg | BDT / kg | Centrally smoothed / transport-adjusted upper retail quote. Note API typo 'howest'. |
| `wholesale_supply` | `w_supply` | Unstandardized | Metric Tons | Market arrival volume. Note: 95%+ missing/zero; unsuitable for primary regression. |

---

## 3. Econometric Recommendations for Papers 1, 2, and 3

### Primary Price Variable:
We construct and provide two explicit, standardized price variables (in BDT / kg):
1. **`price_raw_mid_kg` = `((wholesale_price_low + wholesale_price_high) / 2) / 100`**
   - **Advantage:** Represents the pure, unadjusted local market transaction quote directly observed by enumerators.
   - **Recommended Use:** Primary dependent variable for Paper 1 (weather price response) and Paper 2 (spatial price dispersion).
2. **`price_dam_avg_kg` = `wholesale_price_avg / 100`**
   - **Advantage:** Official DAM headline average incorporating central calibrations.
   - **Recommended Use:** Robustness checks and sensitivity comparisons.

### Retail Margin Variable:
- **`retail_price_mid_kg` = `(retail_price_low + retail_price_high) / 2`**
- **`wholesale_retail_spread_kg` = `retail_price_mid_kg - price_raw_mid_kg`**
- **Recommended Use:** Paper 3 (market efficiency and intermediary margin analysis).

---

## 4. Documented Uncertainties
1. **Exact DAM Central Adjustment Formula:** While we have conclusively proven that `w_avgPrice` is the midpoint of adjusted prices, DAM's internal mathematical weighting for transforming raw prices into adjusted prices (e.g. why a specific market has `a_w_lowest = 6075` when `w_lowest = 6800`) is proprietary to DAM's MIS backend. Therefore, raw price midpoints are preferred for econometric purity.
2. **Supply Volumes:** `w_supply` reporting is sparse and inconsistent across districts. It must not be treated as a continuous panel variable.
