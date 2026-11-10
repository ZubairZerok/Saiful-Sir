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