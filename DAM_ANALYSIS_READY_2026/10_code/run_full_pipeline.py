#!/usr/bin/env python3
"""
Master Orchestration Pipeline: DAM Analysis-Ready 2026
======================================================
Executes all 12 cleaning, auditing, semantic, geographic, temporal,
and panel readiness phases in strict sequence. Verifies end-to-end
reproducibility and non-mutation of source files.
"""

from __future__ import annotations

import os
import sys
import time
import subprocess
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

CODE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CODE_DIR.parent.parent
TARGET_DIR = CODE_DIR.parent

PIPELINE_SCRIPTS = [
    ("Phase 1: Dataset Inventory & Structural Audit", CODE_DIR / "01_inventory.py"),
    ("Phase 2: Price Semantics & Field Definitions", CODE_DIR / "02_price_semantics.py"),
    ("Phase 3 & 4: Numerical Quality Audit & Forensics", CODE_DIR / "03_quality_audit.py"),
    ("Phase 5 & 6: Geography & Temporal Coverage", CODE_DIR / "04_geography_temporal.py"),
    ("Phase 7, 8 & 9: Cleaning Protocol & 3-Tier Outputs", CODE_DIR / "05_cleaning_and_outputs.py"),
    ("Phase 10: Market-Panel Readiness & Overlap Matrix", CODE_DIR / "06_panel_readiness.py"),
    ("Phase 11: Paper-Specific Research Readiness", CODE_DIR / "07_research_readiness.py"),
    ("Phase 12: Manifest & Cryptographic Verification", CODE_DIR / "08_manifest_and_verification.py"),
]


def run_pipeline() -> None:
    print("=" * 80)
    print("STARTING END-TO-END REPRODUCIBLE DAM DATASET CLEANING PIPELINE")
    print("=" * 80)
    start_time = time.time()

    for desc, script_path in PIPELINE_SCRIPTS:
        print(f"\n---> Running: {desc} ({script_path.name})")
        res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, encoding='utf-8')
        if res.returncode != 0:
            print(f"ERROR executing {script_path.name}:")
            print(res.stderr)
            sys.exit(res.returncode)
        print(res.stdout.strip())

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.2f} SECONDS")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()
