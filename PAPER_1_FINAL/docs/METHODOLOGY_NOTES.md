# Methodology Notes

## 1. Estimating equation
ln P(m,c,t) = beta * W(d,c,s(t)) + alpha(m,c) + gamma(c,t) + e(m,c,t)

* P: wholesale price, midpoint of the low and high quotes, BDT/kg. m market, c commodity variety, t year-month, d district of m.
* W: number of shocked months in the pre-harvest window of the season s(t) whose harvest opens the marketing year containing t.
* alpha: market x commodity fixed effects (1,000 groups in the estimation sample); gamma: commodity x year-month fixed effects (1,759 groups).
* Standard errors clustered by district (64 clusters); HC1 and two-way (district, year-month) reported alongside.
* Market-specific linear trends (delta_m * t in the brief) are added in column 5 of Table 2.
* X(m,t): the controls listed in the brief are either national (collinear with gamma) or unavailable at district level - see Limitations.
* Estimation: `pyfixest.feols`, fixed effects absorbed by alternating projections; singleton groups removed iteratively, so N refers to the
  effective sample (34,341 of 34,586 baseline observations).

## 2. Crop calendar and timing (the identification-critical choice)
| | Onion | Potato |
|---|---|---|
| Pre-harvest window | Oct(y-1) - Mar(y) | Oct(y-1) - Feb(y) |
| Marketing year assigned that exposure | Apr(y) - Mar(y+1) | Mar(y) - Feb(y+1) |

The exposure of every observation is built only from weather that precedes it. The previous pipeline's binary indicator per marketing
year is replaced by a count of shocked months (Option A of the brief); the window maximum of |z| (Option B) is a robustness check.
Sweet potato follows the potato calendar; dropping it changes nothing (R15).

## 3. Weather
* ERA5-Land 2 m temperature (0.1 deg, hourly) and ERA5 total precipitation (0.25 deg, hourly) read from the Open-Meteo open-data mirror of
  the Copernicus archives; CHIRPS v2.0 monthly precipitation (0.05 deg) via the IRI Data Library; GADM 4.1 district polygons.
* Hourly values -> UTC-day mean/min/max (temperature) or sum (precipitation) -> calendar months; a month is kept only if complete.
* District values are area-weighted means over the polygon-cell intersections (Albers equal-area). ERA5-Land has no values over sea cells;
  coverage of district area is at least 66% (Bhola) and above 84% elsewhere.
* Normals: mean and sample SD by district and calendar month over 1991-2020. Shocks: |z| > 1.5 (1.0 and 2.0 in robustness).
* ERA5 and CHIRPS district-month rainfall correlate 0.89 in levels
  and 0.70 in z-scores.
* SPEI: water balance P - PET with Hargreaves-Samani PET, standardised by a three-parameter log-logistic (generalised logistic) distribution
  fitted by L-moments to 1991-2020, at 1- and 3-month scales.

### Shock frequency by calendar month (share of district-months, 2000 onward)
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
Drought shocks cannot occur from November to March: dry-season rainfall is near zero, so the mean is less than 1.5 SD above zero.

## 4. Why each choice
| Choice | Reason |
|---|---|
| Raw midpoint rather than the DAM average | the audit shows the average embeds DAM's adjusted quotes |
| Imported varieties excluded from the baseline | priced by international supply; used as placebo |
| 1.5 SD threshold | conventional "severe anomaly" cut-off (about 7% of months per tail under normality); 1.0 and 2.0 reported |
| 1991-2020 normals | current WMO standard normal period; fixed, so later anomalies are out-of-sample |
| District clustering | treatment varies at district level; 64 clusters |
| Count of shocked months | uses monthly information and severity; avoids the static binary of the earlier pipeline |
| Cross-sectional outlier rule | keeps genuine national spikes that a pooled-level rule deletes |
| Seasonal FE in the event study | the brief's FE do not absorb market-specific seasonality, which biases any treatment that only occurs in certain calendar months |

## 5. Deviations from the brief
1. ERA5 (not ERA5-Land) precipitation - see section 3.
2. Monthly median aggregation not needed (data are monthly).
3. Pooled 3xIQR outlier rule demoted to a robustness check.
4. Brinjal is outside the 11 Paper 1 varieties and is not estimated.
5. Controls: only annual exchange rate and CPI (World Bank WDI) and annual Comtrade onion imports (incomplete: missing 2011, 2014, 2019+;
   not used in any regression) could be acquired.
6. The event study is reported under both the brief's fixed effects (pre-trend test fails) and the corrected ones.

## 6. Self-audit against the defects named in the brief
| Defect | Status |
|---|---|
| Static annual binary shock | replaced by monthly indicators aggregated over the crop-specific window |
| Placebo lead significant | season-level lead: p = 0.76; event-study leads fail under the brief's FE (p = 0.010) and pass once seasonality is absorbed (p = 0.738) - both reported |
| w_avgPrice as primary price | not used; robustness only |
| Imported varieties pooled with domestic | excluded from baseline; placebo |
| Interpolation across the gap | none |
| Overall R2 reported as fit | within R2 reported in every table |
| Fabricated or placeholder data | none; unavailable inputs are listed as limitations |
