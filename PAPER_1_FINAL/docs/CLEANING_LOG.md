# Cleaning Log

All steps are implemented in `src/s03_price_panel.py`; row-level flags are saved in
`data/intermediate/price_rows_historical_flagged.csv`. No price is imputed, interpolated or edited.

## 1. Inputs
* `DAM_EXPANDED_2026/master/DAM_ALL_COMMODITIES_EXPANDED_2000_2026.csv` - historical web-portal segment (2000-01 to 2023-07).
* `DAM_ANALYSIS_READY_2026/07_outputs/FULL_FLAGGED/DAM_ALL_11_FULL_FLAGGED.csv` - API segment (2025-06 to 2026-08) with the audited
  quality flags of Steps 4-11. Its 3,348 rows are the same observations as the API rows of the expanded master.

## 2. Step log
```
# Step 3 - price panel construction log

Expanded master rows: 126,932
  Paper 1 commodities (11 ids): 85,762
  historical web-portal rows: 82,414; API rows in master: 3,348
  historical wholesale+retail rows (grower rows not used): 75,561
  rows with missing district: 1,283; recovered from unique market->district map: 1,283
  exact duplicate rows dropped (identified markets): 0
  cross-sectional outlier bounds (retail): log deviation outside [-0.459, 0.454]
  cross-sectional outlier bounds (wholesale): log deviation outside [-0.519, 0.516]

Historical row-level flag counts (rows can carry several flags):
```
price_type                retail  wholesale
flag_unidentified_market      34         33
flag_duplicate_conflict        0          0
flag_zero                      0         65
flag_inverted                  5         11
flag_range_ratio              30         33
flag_abs_bounds               27         92
flag_outlier_xs              781        646
flag_outlier_level_iqr       476        381
primary                    35259      38620
rows                       36128      39433
```
Literal pooled-IQR rule would delete 351 otherwise valid wholesale rows; 97% of them fall in 2019-2020 (onion price crisis). It is therefore kept as a diagnostic flag and used only in a robustness check.
Historical rows not placeable in the panel (unidentified market or conflicting duplicate key): 67

API FULL_FLAGGED rows: 3,348; ELIGIBLE_PRIMARY_ANALYSIS: 3,177; ELIGIBLE_STRICT_SENSITIVITY: 2,721

Panel accounting (market x commodity x month wholesale observations):
```
                     rows  primary  strict  markets  districts    first     last
source                                                                          
dam_web_historical  39400    38620   30020      127         64  2000-01  2023-07
moa_api              3348     3177    2721      117         64  2025-06  2026-08
TOTAL               42748    41797   32741      244         64  2000-01  2026-08
```

Calendar months with zero PRIMARY wholesale observations (31): 2014-10, 2014-11, 2014-12, 2015-01, 2015-02, 2015-09, 2015-10, 2015-11, 2015-12, 2023-08, 2023-09, 2023-10, 2023-11, 2023-12, 2024-01, 2024-02, 2024-03, 2024-04, 2024-05, 2024-06, 2024-07, 2024-08, 2024-09, 2024-10, 2024-11, 2024-12, 2025-01, 2025-02, 2025-03, 2025-04, 2025-05
Observations dated 2024: 0 (institutional gap confirmed; nothing interpolated).
```

## 3. Rules and their justification
| Flag | Rule | Why |
|---|---|---|
| flag_unidentified_market | market or district name missing and not recoverable | cannot be assigned to a district or a market fixed effect |
| flag_duplicate_conflict | same market-commodity-price type-month with different prices | ambiguous; none found among identified markets |
| flag_zero | low <= 0 or high <= 0 | non-trading / unreported quote (Steps 5-9 rule) |
| flag_inverted | low > high | data-entry error (Steps 5-9 rule) |
| flag_range_ratio | high/low > 4 | a retail (per-kg) figure typed into a per-quintal field or vice versa |
| flag_abs_bounds | midpoint outside 1-400 BDT/kg | impossible magnitudes |
| flag_outlier_xs | ln midpoint more than 3 x IQR from the commodity-month cross-market median (cells with >= 5 markets) | PRIMARY outlier rule: judges a quote against other markets in the same month, so genuine national price spikes are kept |
| flag_outlier_level_iqr | outside Q1-3IQR / Q3+3IQR of the pooled 2000-2026 commodity distribution | the literal rule of the brief; **not used for exclusion** because almost all rows it removes are the genuine 2019-20 onion price crisis; applied in robustness check R12 |

The fixed 15,000 BDT/quintal ceiling of the Steps 4-11 protocol is not applied to the historical segment for the same reason: wholesale
onion prices legitimately exceeded 150 BDT/kg in late 2019.

## 4. Tiers
* **PRIMARY_ANALYSIS** - historical: passes every flag except flag_outlier_level_iqr; API: `ELIGIBLE_PRIMARY_ANALYSIS` from the audit.
* **STRICT_SENSITIVITY** - PRIMARY and inside a run of at least 6 consecutive months of the market x commodity series
  (API: `ELIGIBLE_STRICT_SENSITIVITY`).

## 5. Things that differ from the brief, and why
* The historical data are already monthly (one observation per market-commodity-month, dated the 15th), so there is no daily series to
  take a median of. In that segment the reported average equals the low-high midpoint exactly, so the "DAM average" robustness check
  differs from the baseline only in 2025-26.
* The reporting gap is wider than 2024: there are no observations from 2023-08 to 2025-05.
* Grower-price rows are not used.
* Weather has no missing values, so no imputation was needed; controls are not interpolated.
