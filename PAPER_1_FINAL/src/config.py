"""Shared configuration for the Paper 1 pipeline. Every design constant lives here."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # PAPER_1_FINAL/
REPO = ROOT.parent                                   # repository root
RAW = ROOT / "data" / "raw"
INTER = ROOT / "data" / "intermediate"
FINAL = ROOT / "data" / "final"
MODELS = ROOT / "analysis" / "models"
TABLES = ROOT / "analysis" / "tables"
FIGS = ROOT / "analysis" / "figures"
DOCS = ROOT / "docs"
ROB_ALT = ROOT / "robustness" / "alternative_specs"
ROB_PLA = ROOT / "robustness" / "placebo_tests"

EXPANDED_MASTER = REPO / "DAM_EXPANDED_2026" / "master" / "DAM_ALL_COMMODITIES_EXPANDED_2000_2026.csv"
API_FULL_FLAGGED = REPO / "DAM_ANALYSIS_READY_2026" / "07_outputs" / "FULL_FLAGGED" / "DAM_ALL_11_FULL_FLAGGED.csv"

# ---- commodities -------------------------------------------------------------------------
COMMODITIES = {
    831: ("Onion (Local)", "onion", False),
    832: ("Onion (Imported)", "onion", True),
    833: ("Onion (New)", "onion", False),
    942: ("Potato Local (Old)", "potato", False),
    943: ("Potato (Local)", "potato", False),
    944: ("Potato Holland White (Old)", "potato", False),
    945: ("Potato Holland White (New)", "potato", False),
    946: ("Potato Holland Red (Old)", "potato", False),
    947: ("Potato Holland Red", "potato", False),
    948: ("Sweet Potato", "potato", False),
    21014: ("Potatoes (Imported)", "potato", True),
}

# ---- crop calendar (Bangladesh rabi season) ------------------------------------------------
# Pre-harvest exposure window (calendar months). The window that ENDS in calendar year y
# determines the exposure of the marketing year that starts right after it.
#   onion : Oct(y-1) .. Mar(y)  -> marketing year Apr(y) .. Mar(y+1)
#   potato: Oct(y-1) .. Feb(y)  -> marketing year Mar(y) .. Feb(y+1)
PH_WINDOW = {"onion": [10, 11, 12, 1, 2, 3], "potato": [10, 11, 12, 1, 2]}
MKT_YEAR_START = {"onion": 4, "potato": 3}          # first calendar month of the marketing year

# ---- weather --------------------------------------------------------------------------------
BASELINE_YEARS = (1991, 2020)                        # WMO climate normal period
SHOCK_SD = 1.5                                       # primary threshold; 1.0 and 2.0 in robustness
WEATHER_START, WEATHER_END = "1991-01", "2026-10"    # last complete ERA5-Land month at download time

# ---- geography ------------------------------------------------------------------------------
DHAKA_LAT, DHAKA_LON = 23.8103, 90.4125

# ---- cleaning -------------------------------------------------------------------------------
XS_IQR_MULT = 3.0        # cross-sectional outlier rule: 3 x IQR of log deviations from commodity-month median
XS_MIN_CELL = 5          # minimum markets in a commodity-month cell for the cross-sectional rule
RANGE_RATIO_MAX = 4.0    # high/low quote ratio above which a row is treated as a unit/typing error
ABS_KG_BOUNDS = (1.0, 400.0)   # absolute plausibility bounds, BDT/kg (wholesale and retail)
STRICT_MIN_RUN = 6       # consecutive months required for the STRICT_SENSITIVITY tier

SEED = 20261110
