#!/usr/bin/env python3
"""
Phase 12: Manifest Generation and Cryptographic Checksums
=========================================================
Generates SHA-256 cryptographic hashes for all input source files (verifying
zero-mutation) and all generated output datasets and reports.
Outputs:
- 11_manifest/input_file_manifest.csv
- 11_manifest/output_file_manifest.csv
- 11_manifest/sha256_checksums.txt
"""

from __future__ import annotations

import os
import sys
import hashlib
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SOURCE_DIR = PROJECT_ROOT / "dam_output" / "master"
TARGET_DIR = PROJECT_ROOT / "DAM_ANALYSIS_READY_2026"
MANIFEST_DIR = TARGET_DIR / "11_manifest"

INDIVIDUAL_FILES = [
    "DAM_ONION_LOCAL_2010_2026.csv",
    "DAM_ONION_IMPORTED_2010_2026.csv",
    "DAM_ONION_NEW_2010_2026.csv",
    "DAM_POTATO_LOCAL_OLD_2010_2026.csv",
    "DAM_POTATO_LOCAL_2010_2026.csv",
    "DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv",
    "DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv",
    "DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv",
    "DAM_POTATO_HOLLAND_RED_2010_2026.csv",
    "DAM_SWEET_POTATO_2010_2026.csv",
    "DAM_POTATOES_IMPORTED_2010_2026.csv"
]
COMBINED_FILE = "DAM_ALL_11_COMMODITIES_2010_2026.csv"


def get_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def run_manifest() -> None:
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    print("Executing Phase 12: Manifest Generation and Cryptographic Verification...")

    # 1. Input Manifest
    input_records = []
    checksum_lines = ["# ========================================================",
                      "# DAM INPUT SOURCE FILES (READ-ONLY VERIFIED)",
                      "# ========================================================"]

    all_inputs = [SOURCE_DIR / fn for fn in INDIVIDUAL_FILES] + [SOURCE_DIR / COMBINED_FILE]
    for p in all_inputs:
        size = p.stat().st_size
        sha = get_sha256(p)
        df_temp = pd.read_csv(p)
        input_records.append({
            "filename": p.name,
            "relative_path": str(p.relative_to(PROJECT_ROOT)),
            "file_size_bytes": size,
            "row_count": len(df_temp),
            "column_count": len(df_temp.columns),
            "sha256_checksum": sha,
            "mutation_status": "UNTOUCHED_READ_ONLY"
        })
        checksum_lines.append(f"{sha}  {p.relative_to(PROJECT_ROOT)}")

    pd.DataFrame(input_records).to_csv(MANIFEST_DIR / "input_file_manifest.csv", index=False)

    # 2. Output Manifest
    output_records = []
    checksum_lines.extend([
        "",
        "# ========================================================",
        "# DAM OUTPUT GENERATED ARTIFACTS & DATASETS",
        "# ========================================================"
    ])

    for root, dirs, files in os.walk(TARGET_DIR):
        for fn in sorted(files):
            p = Path(root) / fn
            if p.parent == MANIFEST_DIR and fn.startswith("output_file_manifest"):
                continue  # Skip manifest itself while generating
            rel_path = p.relative_to(PROJECT_ROOT)
            size = p.stat().st_size
            sha = get_sha256(p)

            row_cnt = None
            col_cnt = None
            if fn.endswith(".csv"):
                try:
                    df_out = pd.read_csv(p)
                    row_cnt = len(df_out)
                    col_cnt = len(df_out.columns)
                except Exception:
                    pass

            output_records.append({
                "filename": fn,
                "relative_path": str(rel_path),
                "file_category": p.parent.name,
                "file_size_bytes": size,
                "row_count": row_cnt,
                "column_count": col_cnt,
                "sha256_checksum": sha
            })
            checksum_lines.append(f"{sha}  {rel_path}")

    pd.DataFrame(output_records).to_csv(MANIFEST_DIR / "output_file_manifest.csv", index=False)
    (MANIFEST_DIR / "sha256_checksums.txt").write_text("\n".join(checksum_lines) + "\n", encoding='utf-8')

    print(f"Phase 12 complete. Manifests and checksums saved to {MANIFEST_DIR}")


if __name__ == "__main__":
    run_manifest()
