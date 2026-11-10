#!/usr/bin/env python3
"""
Master Runner for DAM Dual-Source Historical & Recent Price Extraction (2000-2026).
Executes all extraction and harmonization stages.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import subprocess
import time
from pathlib import Path

BASE_DIR = Path(r"D:\Desktop 22 8 26\datamain\DAM_EXPANDED_2026")

print("=" * 80, flush=True)
print("DAM DUAL-SOURCE EXTRACTION & HARMONIZATION PIPELINE (2000-2026)", flush=True)
print("=" * 80, flush=True)

# Stage 1: Recent MOA Extraction for Brinjal
print("\n>>> STAGE 1: Extracting Recent Brinjal Data (2025-2026) from MOA REST API...", flush=True)
t0 = time.time()
subprocess.run([sys.executable, str(BASE_DIR / "extract_moa_recent.py")], check=True)
print(f"Stage 1 completed in {time.time()-t0:.1f}s\n", flush=True)

# Stage 2: Historical Web Extraction from market.dam.gov.bd (2000-2024)
print("\n>>> STAGE 2: Extracting Historical Data (2000-2024) from market.dam.gov.bd...", flush=True)
t0 = time.time()
subprocess.run([sys.executable, str(BASE_DIR / "extract_market_dam_historical.py")], check=True)
print(f"Stage 2 completed in {time.time()-t0:.1f}s\n", flush=True)

# Stage 3: Harmonize and Build Master Panels
print("\n>>> STAGE 3: Harmonizing Datasets & Building 2000-2026 Master Panels...", flush=True)
t0 = time.time()
subprocess.run([sys.executable, str(BASE_DIR / "build_harmonized_master.py")], check=True)
print(f"Stage 3 completed in {time.time()-t0:.1f}s\n", flush=True)

print("=" * 80, flush=True)
print("ALL PIPELINE STAGES COMPLETED SUCCESSFULLY!", flush=True)
print("=" * 80, flush=True)
