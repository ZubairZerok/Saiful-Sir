# Paper 1 - Do Pre-Harvest Weather Shocks Affect Agricultural Prices? Evidence from Bangladesh

Complete, reproducible empirical package: data assembly, cleaning, estimation, tables, figures, abstract and findings.

## Result in one paragraph
Local pre-harvest weather shocks have **no detectable effect** on local wholesale onion and potato prices. The estimate is a tightly
bounded zero, robust across samples, thresholds, weather sources and inference methods. Heat is the only shock type with a significant
coefficient and it fails its placebo test (imported onion responds more). Read `docs/PAPER_1_FINDINGS.md` first.

## Run
```bash
pip install -r requirements.txt
python run_complete_pipeline.py                      # offline, about 3 minutes
python run_complete_pipeline.py --download-weather   # also rebuilds the gridded weather inputs (network, about 40 minutes)
```
The pipeline is deterministic (fixed seed for the randomisation inference); a re-run reproduces `SHA256_MANIFEST.txt`
(PDF/PNG figure files can differ in embedded metadata across matplotlib versions).

## Layout
```
run_complete_pipeline.py     orchestrator (steps 1-8)
src/                         one module per step; config.py holds every design constant
data/raw/weather/            monthly grids: ERA5-Land t2m (0.1 deg), ERA5 precipitation (0.25 deg), CHIRPS (0.05 deg)
data/raw/geo/                GADM 4.1 level-2 polygons (64 districts)
data/raw/crosswalks/         district-name / district-id -> GADM crosswalks
data/raw/controls/           World Bank WDI and UN Comtrade downloads
data/raw/README.md           provenance of every raw input (price inputs are referenced in the repository, not copied)
data/intermediate/           cleaned price rows with flags, district weather, exposures, step logs
data/final/paper_1_panel.csv analysis-ready panel (all tiers; use sample_baseline for the baseline sample)
analysis/models/             results_registry.csv (every coefficient), tests_registry.csv (joint tests)
analysis/tables/             Tables 1-9, CSV + LaTeX
analysis/figures/            Figures 1-5, PDF + PNG (300 dpi) + plotted data
robustness/                  robustness and placebo estimates, randomisation-inference draws
docs/                        ABSTRACT, PAPER_1_FINDINGS, VARIABLE_CODEBOOK, CLEANING_LOG, METHODOLOGY_NOTES
SHA256_MANIFEST.txt          checksums of every file in this folder
```

## Tables and figures
| Output | File |
|---|---|
| Table 1 descriptives (A prices, B weather, C sample) | `analysis/tables/table1{a,b,c}_*.csv/.tex` |
| Table 2 main results | `table2_main_results` |
| Table 3 spatial friction and non-linearity | `table3_spatial_nonlinearity` |
| Table 4 robustness | `table4_robustness` |
| Table 5 retail pass-through | `table5_retail_passthrough` |
| Table 6 placebo tests | `table6_placebo_tests` |
| Table 7 event study | `table7_event_study` |
| Table 8 robustness of the decomposed model | `table8_heat_robustness` |
| Table 9 joint tests | `table9_joint_tests.csv` |
| Figures 1-5 | `analysis/figures/figure{1..5}_*.pdf/.png` |

## Where this departs from the project brief (details in `docs/METHODOLOGY_NOTES.md`)
* The baseline sample is about 34,000 observations, not 100,000+: that is what the expanded DAM file contains for wholesale onion and potato.
* `PAPER_1_PRE_HARVEST_SHOCKS/` is an empty submodule pointer in this repository, so the earlier pipeline, its forensic audit, and its weather
  and geography files were not available. Weather and boundaries were acquired afresh from open sources.
* ERA5-Land precipitation was not obtainable without a Copernicus key; ERA5 precipitation is used, CHIRPS as the cross-check.
* Monthly imports, cold-storage capacity, food CPI and district production could not be obtained and are listed as limitations.
* The pooled 3xIQR outlier rule is a robustness check, not the primary rule, because it deletes the genuine 2019-20 onion price crisis.
* The event-study pre-trend test fails under the fixed effects of the brief and passes once market-specific seasonality is absorbed; both are reported.
