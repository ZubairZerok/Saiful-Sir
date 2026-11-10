# Raw inputs and provenance

| Input | Location | Source |
|---|---|---|
| Historical DAM prices 2000-2023 | `../../../DAM_EXPANDED_2026/master/DAM_ALL_COMMODITIES_EXPANDED_2000_2026.csv` (referenced, not copied) | DAM web portal scrape |
| API prices 2025-2026 with audited flags | `../../../DAM_ANALYSIS_READY_2026/07_outputs/FULL_FLAGGED/DAM_ALL_11_FULL_FLAGGED.csv` (referenced) | MOA REST API, Steps 4-11 audit |
| `weather/era5land_t2m_monthly_grid.npz` | here | ERA5-Land hourly 2 m temperature, 0.1 deg (ECMWF/Copernicus C3S), read from the Open-Meteo open-data mirror (AWS S3 bucket `openmeteo`, `data/copernicus_era5_land/temperature_2m/`). Arrays: lat, lon, months, tmean, tmin, tmax (deg C); 1991-01 to 2026-10 |
| `weather/era5_precip_monthly_grid.npz` | here | ERA5 hourly total precipitation, 0.25 deg, same mirror (`data/copernicus_era5/precipitation/`). Arrays: lat, lon, months, precip (mm/month) |
| `weather/chirps_v2_precip_monthly_grid.npz` | here | CHIRPS v2.0 monthly precipitation, 0.05 deg (Climate Hazards Center, UCSB), subset via the IRI Data Library; 1991-01 to 2026-09 |
| `geo/gadm41_BGD_2.json` | here | GADM 4.1 level 2, https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_BGD_2.json.zip |
| `crosswalks/historical_district_bn_to_gadm.csv` | here | hand-built: 65 Bengali district labels of the historical data -> 64 GADM districts |
| `crosswalks/api_district_id_to_gadm.csv` | here | hand-built: API numeric district ids -> GADM districts, each verified by the name of a district-town market in the API data |
| `controls/wb_PA.NUS.FCRF.json`, `controls/wb_FP.CPI.TOTL.json` | here | World Bank WDI API: official exchange rate, CPI (annual, 1999-2025) |
| `controls/comtrade/*.json` | here | UN Comtrade public preview API: Bangladesh-reported imports of HS 070310, annual 2000-2025 (incomplete; not used in any regression) |

Download date: 2026-11-10. `src/s01_weather_download.py` regenerates the three weather grids.
The 2026 ERA5/ERA5-Land months are from the preliminary (ERA5T) stream.
