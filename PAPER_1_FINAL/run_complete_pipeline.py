#!/usr/bin/env python3
"""Paper 1 - complete reproducible pipeline.

    python run_complete_pipeline.py                 # everything from committed raw inputs (offline, ~5 min)
    python run_complete_pipeline.py --download-weather   # also re-download the gridded weather (network, ~40 min)
    python run_complete_pipeline.py --from 5        # resume from a step number

Steps
  1  s01_weather_download   gridded ERA5-Land / ERA5 / CHIRPS -> data/raw/weather/*.npz   (only with --download-weather)
  2  s02_weather_district   district x month weather, normals, z-scores, shocks, SPEI
  3  s03_price_panel        cleaning, flags, tiers -> market x commodity x month price panel
  35 s035_controls          annual macro controls from the downloaded World Bank / Comtrade files
  4  s04_build_panel        crop-calendar exposure + merge -> data/final/paper_1_panel.csv
  5  s05_models             model hierarchy, placebo tests, robustness -> analysis/models/*.csv
  6  s06_tables_figures     tables (CSV + LaTeX) and figures (PDF + PNG)
  7  s07_documents          abstract, findings, codebook, cleaning log, methodology notes
  8  SHA-256 manifest of every input and output file under PAPER_1_FINAL/
"""
import argparse
import hashlib
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEPS = [(1, "s01_weather_download"), (2, "s02_weather_district"), (3, "s03_price_panel"), (35, "s035_controls"),
         (4, "s04_build_panel"), (5, "s05_models"), (6, "s06_tables_figures"), (7, "s07_documents")]
ORDER = [1, 2, 3, 35, 4, 5, 6, 7, 8]


def manifest():
    lines = []
    for f in sorted(ROOT.rglob("*")):
        rel = f.relative_to(ROOT).as_posix()
        if f.is_file() and rel != "SHA256_MANIFEST.txt" and "__pycache__" not in rel and not rel.startswith("logs/"):
            lines.append(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {rel}")
    (ROOT / "SHA256_MANIFEST.txt").write_text("\n".join(lines) + "\n")
    print(f"SHA256_MANIFEST.txt: {len(lines)} files")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download-weather", action="store_true")
    ap.add_argument("--from", dest="start", type=int, default=1)
    a = ap.parse_args()
    for d in ("data/intermediate", "data/final", "analysis/models", "analysis/tables", "analysis/figures", "docs",
              "robustness/alternative_specs", "robustness/placebo_tests", "logs"):
        (ROOT / d).mkdir(parents=True, exist_ok=True)
    begin = ORDER.index(a.start)
    for num, mod in STEPS:
        if ORDER.index(num) < begin or (num == 1 and not a.download_weather):
            continue
        t = time.time()
        print(f"[step {num}] {mod} ...", flush=True)
        with open(ROOT / "logs" / f"{mod}.log", "w") as log:
            rc = subprocess.run([sys.executable, f"{mod}.py"], cwd=ROOT / "src", stdout=log, stderr=subprocess.STDOUT).returncode
        if rc:
            sys.exit(f"step {num} ({mod}) failed - see logs/{mod}.log")
        print(f"          done in {time.time() - t:.0f}s", flush=True)
    manifest()


if __name__ == "__main__":
    main()
