# Variable Codebook - `data/final/paper_1_panel.csv`

42,748 rows (all tiers), 88 columns. One row per market x commodity x month. Ranges are computed from the file.

| Variable | Definition | Source | Unit | Type | Observed range | Non-missing | Notes |
|---|---|---|---|---|---|---|---|
| `market_key` | Market identifier. 'H|district|market name' for the historical web-portal segment, 'A|market_id' for the API segment | DAM | - | categorical | 244 distinct | 42,748 | Historical and API markets cannot be linked and are separate units |
| `market_name` | Market name as reported (Bengali in the historical segment) | DAM | - | categorical | 244 distinct | 42,748 |  |
| `district_id` | GADM 4.1 GID_2 code of the district | GADM | - | categorical | 64 distinct | 42,748 |  |
| `gadm_name_2` | District name (GADM NAME_2 spelling); cluster variable | GADM | - | categorical | 64 distinct | 42,748 | 64 districts |
| `division` | Division (GADM NAME_1) | GADM | - | categorical | 8 distinct | 42,748 |  |
| `commodity_id` | DAM commodity code | DAM | - | categorical | 831 to 2.101e+04 | 42,748 | 831, 832, 833, 942-948, 21014 |
| `commodity_name` | Commodity variety name | DAM | - | categorical | 11 distinct | 42,748 |  |
| `crop` | onion or potato; selects the crop calendar | derived | - | categorical | 2 distinct | 42,748 | sweet potato uses the potato calendar |
| `imported` | True for 832 and 21014 | derived | - | binary | share true 0.172 | 42,748 | excluded from baseline |
| `source` | dam_web_historical or moa_api | DAM | - | categorical | 2 distinct | 42,748 |  |
| `ym` | Year-month of the price observation | DAM | YYYY-MM | date | 289 distinct | 42,748 |  |
| `year` | Calendar year | derived | - | integer | 2000 to 2026 | 42,748 |  |
| `month` | Calendar month | derived | 1-12 | integer | 1 to 12 | 42,748 |  |
| `season` | Harvest year y of the marketing year containing ym (onion: Apr y-Mar y+1; potato: Mar y-Feb y+1) | derived | year | integer | 1999 to 2026 | 42,748 | links prices to the window ending in y |
| `wholesale_low` | Lowest wholesale quote | DAM | BDT/quintal | continuous | 0 to 1.9e+07 | 42,748 |  |
| `wholesale_high` | Highest wholesale quote | DAM | BDT/quintal | continuous | 0 to 7.298e+05 | 42,748 |  |
| `price_wholesale_raw_mid_kg` | (wholesale_low + wholesale_high) / 2 / 100 | derived | BDT/kg | continuous | 0 to 9.502e+04 | 42,604 | PRIMARY price variable |
| `price_wholesale_dam_avg_kg` | DAM reported wholesale average / 100 | DAM | BDT/kg | continuous | 0 to 1.585e+04 | 42,707 | equals the midpoint before 2025; robustness only |
| `wholesale_primary` | Wholesale quote passes all PRIMARY cleaning rules | derived | - | binary | share true 0.978 | 42,748 |  |
| `wholesale_basic_ok` | Positive, non-inverted, plausible quote before the cross-sectional outlier rule | derived | - | binary | share true 0.993 | 42,748 | used for winsorising check R11 |
| `wholesale_flag_level_iqr` | Outside pooled 3xIQR bounds of the commodity | derived | - | binary | share true 0.009 | 42,748 | diagnostic; R12 |
| `retail_low` | Lowest retail quote | DAM | BDT/kg | continuous | 0 to 1e+04 | 30,647 |  |
| `retail_high` | Highest retail quote | DAM | BDT/kg | continuous | 0 to 4614 | 30,647 |  |
| `price_retail_raw_mid_kg` | (retail_low + retail_high) / 2 | derived | BDT/kg | continuous | 3.365 to 5052 | 30,497 |  |
| `price_retail_dam_avg_kg` | DAM reported retail average | DAM | BDT/kg | continuous | 3.36 to 2332 | 30,603 |  |
| `retail_primary` | Retail quote passes the cleaning rules | derived | - | binary | share true 0.700 | 42,748 |  |
| `retail_basic_ok` | Retail analogue of wholesale_basic_ok | derived | - | binary | share true 0.712 | 42,748 |  |
| `retail_flag_level_iqr` | Retail analogue of wholesale_flag_level_iqr | derived | - | binary | share true 0.015 | 30,647 |  |
| `tier_primary` | PRIMARY_ANALYSIS tier membership | derived | - | binary | share true 0.978 | 42,748 | default sample |
| `tier_strict` | STRICT_SENSITIVITY tier: PRIMARY and in a run of >= 6 consecutive months | derived | - | binary | share true 0.766 | 42,748 | robustness |
| `ph_any` | Number of months in the pre-harvest window with any shock (|z_precip| > 1.5 or |z_temp| > 1.5) | ERA5 / ERA5-Land | months | count | 0 to 4 | 42,748 | HEADLINE exposure; 0-6 onion, 0-5 potato |
| `ph_excess_rain` | Window months with z_precip > 1.5 | ERA5 | months | count | 0 to 3 | 42,748 |  |
| `ph_drought` | Window months with z_precip < -1.5 | ERA5 | months | count | 0 to 1 | 42,748 | can only be non-zero through October |
| `ph_heatwave` | Window months with z_temp > 1.5 | ERA5-Land | months | count | 0 to 4 | 42,748 |  |
| `ph_cold` | Window months with z_temp < -1.5 | ERA5-Land | months | count | 0 to 3 | 42,748 |  |
| `ph_any_10` | As ph_any with a 1.0 SD threshold | ERA5 / ERA5-Land | months | count | 0 to 6 | 42,748 |  |
| `ph_any_20` | As ph_any with a 2.0 SD threshold | ERA5 / ERA5-Land | months | count | 0 to 3 | 42,748 |  |
| `ph_excess_rain_10` | Window months with z_precip > 1.0 | ERA5 / ERA5-Land | months | count | 0 to 4 | 42,748 | threshold robustness |
| `ph_drought_10` | Window months with z_precip < - 1.0 | ERA5 / ERA5-Land | months | count | 0 to 2 | 42,748 | threshold robustness |
| `ph_heatwave_10` | Window months with z_temp > 1.0 | ERA5 / ERA5-Land | months | count | 0 to 6 | 42,748 | threshold robustness |
| `ph_cold_10` | Window months with z_temp < - 1.0 | ERA5 / ERA5-Land | months | count | 0 to 4 | 42,748 | threshold robustness |
| `ph_excess_rain_20` | Window months with z_precip > 2.0 | ERA5 / ERA5-Land | months | count | 0 to 3 | 42,748 | threshold robustness |
| `ph_drought_20` | Window months with z_precip < - 2.0 | ERA5 / ERA5-Land | months | count | 0 to 0 | 42,748 | threshold robustness |
| `ph_heatwave_20` | Window months with z_temp > 2.0 | ERA5 / ERA5-Land | months | count | 0 to 3 | 42,748 | threshold robustness |
| `ph_cold_20` | Window months with z_temp < - 2.0 | ERA5 / ERA5-Land | months | count | 0 to 1 | 42,748 | threshold robustness |
| `ph_any_chirps` | As ph_any with CHIRPS rainfall z-scores (temperature from ERA5-Land) | CHIRPS / ERA5-Land | months | count | 0 to 4 | 42,748 |  |
| `ph_excess_rain_chirps` | Window months with CHIRPS z_precip > 1.5 | CHIRPS | months | count | 0 to 3 | 42,748 |  |
| `ph_drought_chirps` | Window months with CHIRPS z_precip < -1.5 | CHIRPS | months | count | 0 to 1 | 42,748 | almost never non-zero |
| `ph_any_spei` | Window months with |SPEI-1| > 1.5 or a temperature shock | derived | months | count | 0 to 5 | 42,748 |  |
| `ph_wet_spei` | Window months with SPEI-1 > 1.5 | derived | months | count | 0 to 3 | 42,748 |  |
| `ph_dry_spei` | Window months with SPEI-1 < -1.5 | derived | months | count | 0 to 3 | 42,748 |  |
| `ph_any_pct` | Window months with rainfall or temperature outside the 10th-90th percentile of 1991-2020 | derived | months | count | 0 to 6 | 42,748 |  |
| `ph_max_abs_z_precip` | Maximum |z_precip| over the window (Option B) | ERA5 | SD | continuous | 0.2332 to 5.542 | 42,748 |  |
| `ph_max_abs_z_temp` | Maximum |z_temp| over the window (Option B) | ERA5-Land | SD | continuous | 0.4079 to 3.196 | 42,748 |  |
| `ph_mean_z_precip` | Mean z_precip over the window | ERA5 | SD | continuous | -0.6964 to 1.759 | 42,748 |  |
| `ph_mean_z_temp` | Mean z_temp over the window | ERA5-Land | SD | continuous | -1.398 to 2.153 | 42,748 |  |
| `ph_precip_mm` | Total precipitation over the window | ERA5 | mm | continuous | 34.29 to 901.1 | 42,748 |  |
| `ph_tmean_c` | Mean temperature over the window | ERA5-Land | deg C | continuous | 19.57 to 24.45 | 42,748 |  |
| `ph_min_spei3` | Minimum SPEI-3 over the window | derived | SD | continuous | -2.91 to 1.343 | 42,748 |  |
| `ph_any_off` | Shocked months in Apr-Sep before planting (off-season placebo) | derived | months | count | 0 to 6 | 42,748 |  |
| `ph_any_lead` | ph_any of the NEXT season (placebo) | derived | months | count | 0 to 4 | 41,311 | likewise ph_*_lead for each type |
| `ph_excess_rain_lead` | ph_excess_rain of the next season (placebo) | derived | months | count | 0 to 3 | 41,311 |  |
| `ph_drought_lead` | ph_drought of the next season (placebo) | derived | months | count | 0 to 1 | 41,311 |  |
| `ph_heatwave_lead` | ph_heatwave of the next season (placebo) | derived | months | count | 0 to 4 | 41,311 |  |
| `ph_cold_lead` | ph_cold of the next season (placebo) | derived | months | count | 0 to 3 | 41,311 |  |
| `ph_any_lag` | ph_any of the previous season | derived | months | count | 0 to 4 | 42,748 |  |
| `centroid_lat` | District centroid latitude | GADM | deg | continuous | 21.48 to 26.28 | 42,748 |  |
| `centroid_lon` | District centroid longitude | GADM | deg | continuous | 88.26 to 92.36 | 42,748 |  |
| `distance_to_dhaka_km` | WGS84 geodesic distance from district centroid to Dhaka (23.8103, 90.4125) | derived | km | continuous | 16.68 to 330.8 | 42,748 | time-invariant |
| `precip_mm` | District precipitation in month ym | ERA5 | mm/month | continuous | 0 to 1419 | 42,748 |  |
| `tmean_c` | District mean 2 m temperature | ERA5-Land | deg C | continuous | 15.98 to 32.08 | 42,748 |  |
| `tmin_c` | Monthly mean of daily minimum temperature | ERA5-Land | deg C | continuous | 9.891 to 27.9 | 42,748 | UTC days |
| `tmax_c` | Monthly mean of daily maximum temperature | ERA5-Land | deg C | continuous | 21.61 to 38.07 | 42,748 | UTC days |
| `z_precip` | (precip - 1991-2020 district-month mean) / SD | derived | SD | continuous | -2.984 to 5.542 | 42,748 |  |
| `z_temp` | (tmean - 1991-2020 district-month mean) / SD | derived | SD | continuous | -2.523 to 5.577 | 42,748 |  |
| `spei3` | 3-month SPEI | derived | SD | continuous | -3.719 to 3.719 | 42,748 |  |
| `ln_price` | ln(price_wholesale_raw_mid_kg) | derived | log BDT/kg | continuous | -2.207 to 11.46 | 42,539 | DEPENDENT VARIABLE |
| `ln_price_dam_avg` | ln(price_wholesale_dam_avg_kg) | derived | log BDT/kg | continuous | -2.207 to 9.671 | 42,642 |  |
| `ln_retail` | ln(price_retail_raw_mid_kg) where retail_primary | derived | log BDT/kg | continuous | 1.592 to 5.472 | 29,915 |  |
| `ln_dist_dhaka` | ln(distance_to_dhaka_km) | derived | log km | continuous | 2.814 to 5.802 | 42,748 |  |
| `t_index` | Months since 2000-01 | derived | months | integer | 0 to 319 | 42,748 | trend variable |
| `in_ph_window` | Price month falls inside the crop's pre-harvest window | derived | - | binary | share true 0.437 | 42,748 |  |
| `months_since_harvest` | Months since the start of the marketing year | derived | 0-11 | integer | 0 to 11 | 42,748 |  |
| `mc_id` | Market x commodity identifier (fixed effect) | derived | - | categorical | 1,289 distinct | 42,748 |  |
| `mcm_id` | Market x commodity x calendar-month identifier (seasonal fixed effect) | derived | - | categorical | 9,977 distinct | 42,748 |  |
| `cym_id` | Commodity x year-month identifier (fixed effect) | derived | - | categorical | 2,165 distinct | 42,748 |  |
| `sample_baseline` | PRIMARY tier, domestic variety, exposure and price observed | derived | - | binary | share true 0.809 | 42,748 | baseline estimation sample |
| `sample_placebo_imported` | PRIMARY tier, imported variety | derived | - | binary | share true 0.169 | 42,748 | placebo sample |

## Weather file `data/intermediate/weather_district_monthly.csv`

| Variable | Definition | Unit |
|---|---|---|
| `district_id`, `gadm_name_2` | GADM district code and name | - |
| `ym`, `year`, `month` | month | - |
| `precip_mm` | ERA5 total precipitation, area-weighted district mean | mm/month |
| `tmean_c`, `tmin_c`, `tmax_c` | ERA5-Land 2 m temperature: monthly mean, mean daily minimum, mean daily maximum | deg C |
| `precip_chirps_mm` | CHIRPS v2.0 precipitation | mm/month |

`weather_district_monthly_anomalies.csv` adds normals, SDs, z-scores, percentile ranks, PET, SPEI-1/3 and the monthly shock indicators (`excess_rain_*`, `drought_*`, `heatwave_*`, `cold_*`, `any_shock_*` at thresholds 10/15/20 = 1.0/1.5/2.0 SD; `*_chirps`; `*_spei`; `any_shock_pct`).