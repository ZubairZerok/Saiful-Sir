# Step 2 - district weather log

District-months: 27,520 = 64 districts x 430 months (1991-01 .. 2026-10); no missing ERA5 values.
CHIRPS coverage: 1991-01 .. 2026-09 (27,456 district-months).
Minimum share of district area covered by data cells: tmean_c=0.665, tmin_c=0.665, tmax_c=0.665, precip_mm=1.000, precip_chirps_mm=0.999
ERA5 vs CHIRPS district-month rainfall: corr(levels) = 0.892, corr(z-scores) = 0.703.

Share of district-months (2000+) flagged as shocks at +-1.5 SD, by calendar month:
```
       excess_rain_15  drought_15  heatwave_15  cold_15  any_shock_15  wet_spei  dry_spei
month                                                                                    
1              0.0637      0.0000       0.0475   0.0451        0.1551    0.0712    0.0231
2              0.0799      0.0000       0.0428   0.0810        0.1846    0.0723    0.0052
3              0.0694      0.0000       0.0532   0.0573        0.1562    0.0637    0.0214
4              0.0747      0.0255       0.0810   0.0058        0.1632    0.0631    0.0793
5              0.0648      0.0208       0.0666   0.0596        0.1649    0.0579    0.0544
6              0.0544      0.0538       0.1551   0.0613        0.2720    0.0498    0.0723
7              0.0828      0.0822       0.2014   0.0544        0.3409    0.0764    0.1076
8              0.1059      0.0359       0.1719   0.0231        0.2830    0.1007    0.0966
9              0.0671      0.0226       0.2402   0.0272        0.3131    0.0602    0.0573
10             0.0833      0.0388       0.1788   0.0150        0.2922    0.0781    0.0422
11             0.0835      0.0000       0.0986   0.0475        0.2181    0.0968    0.0210
12             0.1022      0.0000       0.1190   0.0319        0.2434    0.1256    0.0150
```