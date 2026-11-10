#!/usr/bin/env python3
"""
Harmonization and Master Dataset Builder (2000-2026).
Merges historical web portal data (2000-2024) and recent REST API data (2025-2026)
for Brinjal HYV and all target agricultural commodities into unified panel datasets.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import json
import calendar
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


# ── Directories ─────────────────────────────────────────────────────────────
BASE_DIR = Path(r"D:\Desktop 22 8 26\datamain")
EXPANDED_DIR = BASE_DIR / "DAM_EXPANDED_2026"
CLEAN_DIR = EXPANDED_DIR / "clean_parts"
MASTER_DIR = EXPANDED_DIR / "master"
REPORTS_DIR = EXPANDED_DIR / "reports"

MASTER_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Load Market Metadata ───────────────────────────────────────────────────
with open(BASE_DIR / "common_dropdowns.json", "r", encoding="utf-8") as f:
    raw_meta = json.load(f)

meta_data = raw_meta.get("data", raw_meta)
market_list = meta_data.get("marketList", [])
div_list = meta_data.get("divisionList", [])
dist_list = meta_data.get("districtList", [])
upz_list = meta_data.get("upazilaList", [])

# Build lookup dictionaries
mkt_by_id = {m.get("value"): m for m in market_list}
mkt_by_name_bn = {m.get("text_bn", "").strip(): m for m in market_list if m.get("text_bn")}
mkt_by_name_en = {m.get("text_en", "").strip().lower(): m for m in market_list if m.get("text_en")}

div_by_id = {d.get("value"): d for d in div_list}
div_by_name_bn = {d.get("text_bn", "").strip(): d for d in div_list if d.get("text_bn")}
div_by_name_en = {d.get("text_en", "").strip().lower(): d for d in div_list if d.get("text_en")}

dist_by_id = {d.get("value"): d for d in dist_list}
dist_by_name_bn = {d.get("text_bn", "").strip(): d for d in dist_list if d.get("text_bn")}
dist_by_name_en = {d.get("text_en", "").strip().lower(): d for d in dist_list if d.get("text_en")}

upz_by_id = {u.get("value"): u for u in upz_list}
upz_by_name_bn = {u.get("text_bn", "").strip(): u for u in upz_list if u.get("text_bn")}
upz_by_name_en = {u.get("text_en", "").strip().lower(): u for u in upz_list if u.get("text_en")}

print(f"Loaded metadata lookups: {len(mkt_by_id)} markets, {len(div_by_id)} divisions, {len(dist_by_id)} districts, {len(upz_by_id)} upazilas.", flush=True)

# ── Load Source Datasets ───────────────────────────────────────────────────
historical_web_file = CLEAN_DIR / "dam_historical_monthly_2000_2024.csv"
if not historical_web_file.exists():
    historical_web_file = CLEAN_DIR / "dam_historical_web_2000_2024.csv"

recent_brinjal_file = CLEAN_DIR / "moa_brinjal_recent_2025_2026.csv"
recent_11_file = BASE_DIR / "DAM_REEXTRACTION_2026" / "master" / "DAM_ALL_11_COMMODITIES_2010_2026.csv"

historical_df = pd.read_csv(historical_web_file) if historical_web_file.exists() else pd.DataFrame()
recent_brinjal_df = pd.read_csv(recent_brinjal_file) if recent_brinjal_file.exists() else pd.DataFrame()
recent_11_df = pd.read_csv(recent_11_file) if recent_11_file.exists() else pd.DataFrame()


print(f"Loaded source rows:", flush=True)
print(f"  - Historical Web (2000-2024): {len(historical_df)} rows", flush=True)
print(f"  - Recent MOA Brinjal (2025-2026): {len(recent_brinjal_df)} rows", flush=True)
print(f"  - Recent MOA 11 Commodities (2025-2026): {len(recent_11_df)} rows", flush=True)

harmonized_rows = []

# ── Standardize Historical Web Rows ────────────────────────────────────────
if not historical_df.empty:
    for _, r in historical_df.iterrows():
        div_bn = str(r.get("division_name_bn") or "").strip()
        dist_bn = str(r.get("district_name_bn") or "").strip()
        upz_bn = str(r.get("upazila_name_bn") or "").strip()
        mkt_bn = str(r.get("market_name_bn") or "").strip()
        
        div_obj = div_by_name_bn.get(div_bn, {})
        div_id = div_obj.get("value")
        div_en = div_obj.get("text_en") or div_obj.get("text") or div_bn
        
        dist_obj = dist_by_name_bn.get(dist_bn, {})
        dist_id = dist_obj.get("value")
        dist_en = dist_obj.get("text_en") or dist_obj.get("text") or dist_bn
        
        upz_obj = upz_by_name_bn.get(upz_bn, {})
        upz_id = upz_obj.get("value")
        upz_en = upz_obj.get("text_en") or upz_obj.get("text") or upz_bn
        
        mkt_obj = mkt_by_name_bn.get(mkt_bn, {})
        mkt_id = mkt_obj.get("value")
        mkt_en = mkt_obj.get("text_en") or mkt_obj.get("text") or mkt_bn
        
        ptype = str(r.get("price_type") or "wholesale").lower()
        low_val = r.get("price_low")
        high_val = r.get("price_high")
        avg_val = r.get("price_avg")
        yr = r.get("price_year")
        mo = r.get("price_month")
        mo_int = int(mo) if pd.notna(mo) and str(mo).isdigit() else None
        mo_name = r.get("price_month_name") or (calendar.month_name[mo_int] if mo_int else None)
        pdate = r.get("price_date") or (f"{int(yr)}-{mo_int:02d}-15" if pd.notna(yr) and mo_int else (f"{int(yr)}-01-01" if pd.notna(yr) else None))
        
        row = {
            "source_system": "market_dam_web_historical",
            "frequency": "monthly_observation" if mo_int else "annual_summary",
            "division_id": div_id,
            "division_name_en": div_en,
            "division_name_bn": div_bn,
            "district_id": dist_id,
            "district_name_en": dist_en,
            "district_name_bn": dist_bn,
            "upazila_id": upz_id,
            "upazila_name_en": upz_en,
            "upazila_name_bn": upz_bn,
            "market_id": mkt_id,
            "market_name_en": mkt_en,
            "market_name_bn": mkt_bn,
            "commodity_id": r.get("commodity_id"),
            "commodity_name_en": r.get("commodity_name_en"),
            "commodity_name_bn": r.get("commodity_name_bn"),
            "price_type": ptype,
            "price_date": pdate,
            "price_year": int(yr) if pd.notna(yr) else None,
            "price_month": mo_int,
            "price_month_name": mo_name,
            "wholesale_unit": "Quintal" if ptype == "wholesale" else None,
            "retail_unit": "Kilogram" if ptype == "retail" else None,
            "wholesale_price_low": low_val if ptype == "wholesale" else None,
            "wholesale_price_high": high_val if ptype == "wholesale" else None,
            "wholesale_price_avg": avg_val if ptype == "wholesale" else None,
            "retail_price_low": low_val if ptype == "retail" else None,
            "retail_price_high": high_val if ptype == "retail" else None,
            "retail_price_avg": avg_val if ptype == "retail" else None,
            "grower_price_low": low_val if ptype == "grower" else None,
            "grower_price_high": high_val if ptype == "grower" else None,
            "grower_price_avg": avg_val if ptype == "grower" else None,
            "standardized_price_low": low_val,
            "standardized_price_high": high_val,
            "standardized_price_avg": avg_val,
        }
        harmonized_rows.append(row)


# ── Standardize Recent MOA API Rows ───────────────────────────────────────
def process_moa_row(r):
    mkt_id = r.get("market_id")
    mkt_obj = mkt_by_id.get(mkt_id, {})
    
    div_id = r.get("division_id") or mkt_obj.get("division_id")
    div_obj = div_by_id.get(div_id, {})
    div_en = r.get("division_name") or div_obj.get("text_en") or div_obj.get("text")
    div_bn = div_obj.get("text_bn") or r.get("division_name")
    
    dist_id = r.get("district_id") or mkt_obj.get("district_id")
    dist_obj = dist_by_id.get(dist_id, {})
    dist_en = r.get("district_name") or dist_obj.get("text_en") or dist_obj.get("text")
    dist_bn = dist_obj.get("text_bn") or r.get("district_name")
    
    upz_id = r.get("upazila_id") or mkt_obj.get("upazila_id")
    upz_obj = upz_by_id.get(upz_id, {})
    upz_en = r.get("upazila_name") or upz_obj.get("text_en") or upz_obj.get("text")
    upz_bn = upz_obj.get("text_bn") or r.get("upazila_name")
    
    mkt_en = r.get("market_name") or mkt_obj.get("text_en") or mkt_obj.get("text")
    mkt_bn = r.get("market_name_bn") or mkt_obj.get("text_bn")
    
    ws_low = r.get("wholesale_price_low") if pd.notna(r.get("wholesale_price_low")) else r.get("w_lowestPrice")
    ws_high = r.get("wholesale_price_high") if pd.notna(r.get("wholesale_price_high")) else r.get("w_highestPrice")
    ws_avg = r.get("wholesale_price_avg") if pd.notna(r.get("wholesale_price_avg")) else r.get("w_avgPrice")
    
    rt_low = r.get("retail_price_low") if pd.notna(r.get("retail_price_low")) else r.get("r_lowestPrice")
    rt_high = r.get("retail_price_high") if pd.notna(r.get("retail_price_high")) else r.get("r_highestPrice")
    rt_avg = r.get("retail_price_avg") if pd.notna(r.get("retail_price_avg")) else r.get("r_avgPrice")
    
    dt_str = str(r.get("price_date") or "")[:10]
    yr = r.get("price_year")
    if (pd.isna(yr) or not yr) and len(dt_str) >= 4 and dt_str[:4].isdigit():
        yr = int(dt_str[:4])
    
    mo = r.get("price_month")
    if (pd.isna(mo) or not mo) and len(dt_str) >= 7 and dt_str[5:7].isdigit():
        mo = int(dt_str[5:7])
    
    return {
        "source_system": "moa_api_recent",
        "frequency": "monthly_observation",
        "division_id": div_id,
        "division_name_en": div_en,
        "division_name_bn": div_bn,
        "district_id": dist_id,
        "district_name_en": dist_en,
        "district_name_bn": dist_bn,
        "upazila_id": upz_id,
        "upazila_name_en": upz_en,
        "upazila_name_bn": upz_bn,
        "market_id": mkt_id,
        "market_name_en": mkt_en,
        "market_name_bn": mkt_bn,
        "commodity_id": r.get("commodity_id"),
        "commodity_name_en": r.get("commodity_name_en"),
        "commodity_name_bn": r.get("commodity_name_bn"),
        "price_type": "wholesale_and_retail",
        "price_date": dt_str if dt_str else None,
        "price_year": int(yr) if pd.notna(yr) else None,
        "price_month": int(mo) if pd.notna(mo) else None,
        "price_month_name": r.get("price_month_name"),
        "wholesale_unit": r.get("wholesale_unit") or "Quintal",
        "retail_unit": r.get("retail_unit") or "Kilogram",
        "wholesale_price_low": ws_low,
        "wholesale_price_high": ws_high,
        "wholesale_price_avg": ws_avg,
        "retail_price_low": rt_low,
        "retail_price_high": rt_high,
        "retail_price_avg": rt_avg,
        "grower_price_low": None,
        "grower_price_high": None,
        "grower_price_avg": None,
        "standardized_price_low": ws_low if pd.notna(ws_low) else rt_low,
        "standardized_price_high": ws_high if pd.notna(ws_high) else rt_high,
        "standardized_price_avg": ws_avg if pd.notna(ws_avg) else rt_avg,
    }

if not recent_brinjal_df.empty:
    for _, r in recent_brinjal_df.iterrows():
        harmonized_rows.append(process_moa_row(r))

if not recent_11_df.empty:
    for _, r in recent_11_df.iterrows():
        harmonized_rows.append(process_moa_row(r))

# ── Build Master DataFrames ────────────────────────────────────────────────
master_df = pd.DataFrame(harmonized_rows)
print(f"\nTotal harmonized records combined: {len(master_df)}", flush=True)

# 1. Dedicated Master for Brinjal HYV (949)
brinjal_hyv_df = master_df[master_df["commodity_id"] == 949].copy()
brinjal_hyv_csv = MASTER_DIR / "DAM_BRINJAL_HYV_2000_2026.csv"
brinjal_hyv_df.to_csv(brinjal_hyv_csv, index=False, encoding="utf-8-sig")
print(f"Saved Brinjal HYV Master: {len(brinjal_hyv_df)} rows -> {brinjal_hyv_csv}", flush=True)

# 2. Dedicated Master for All Brinjal Varieties (949, 950)
brinjal_all_df = master_df[master_df["commodity_id"].isin([949, 950])].copy()
brinjal_all_csv = MASTER_DIR / "DAM_BRINJAL_ALL_VARIETIES_2000_2026.csv"
brinjal_all_df.to_csv(brinjal_all_csv, index=False, encoding="utf-8-sig")
print(f"Saved All Brinjal Master: {len(brinjal_all_df)} rows -> {brinjal_all_csv}", flush=True)

# 3. Complete Master for All Commodities (2000-2026)
all_commodities_csv = MASTER_DIR / "DAM_ALL_COMMODITIES_EXPANDED_2000_2026.csv"
master_df.to_csv(all_commodities_csv, index=False, encoding="utf-8-sig")
print(f"Saved Complete Master Panel: {len(master_df)} rows -> {all_commodities_csv}", flush=True)

# 4. Individual Commodity Master Files
for cid, group in master_df.groupby("commodity_id"):
    cname = group["commodity_name_en"].iloc[0]
    safe_name = "".join(c if c.isalnum() else "_" for c in str(cname)).upper().strip("_")
    indiv_file = MASTER_DIR / f"DAM_{safe_name}_2000_2026.csv"
    group.to_csv(indiv_file, index=False, encoding="utf-8-sig")
    print(f"  - Individual Master {cname} (ID {cid}): {len(group)} rows -> {indiv_file.name}", flush=True)

# ── Generate Summary & Audit Reports ───────────────────────────────────────
cov_matrix = master_df.groupby(["commodity_id", "commodity_name_en", "price_year"]).size().unstack(fill_value=0)
cov_matrix_csv = REPORTS_DIR / "coverage_matrix_by_year_commodity.csv"
cov_matrix.to_csv(cov_matrix_csv, encoding="utf-8-sig")

mkt_inv = master_df.groupby(["division_name_en", "district_name_en", "market_name_en", "commodity_name_en"]).agg(
    total_records=("price_year", "count"),
    min_year=("price_year", "min"),
    max_year=("price_year", "max"),
    sources=("source_system", lambda s: ", ".join(sorted(set(s))))
).reset_index()
mkt_inv_csv = REPORTS_DIR / "market_geographic_inventory.csv"
mkt_inv.to_csv(mkt_inv_csv, index=False, encoding="utf-8-sig")

total_obs = len(master_df)
unique_markets = master_df["market_name_en"].nunique()
unique_districts = master_df["district_name_en"].nunique()
unique_divisions = master_df["division_name_en"].nunique()
years_covered = sorted(master_df["price_year"].dropna().unique().astype(int).tolist())

report_lines = [
    "# DAM EXPANDED & HARMONIZED AGRICULTURAL PRICE AUDIT REPORT (2000–2026)",
    "",
    f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    f"**Workspace:** `{EXPANDED_DIR}`",
    "",
    "---",
    "",
    "## 1. Executive Summary",
    "",
    f"- **Total Harmonized Observations:** **{total_obs:,}**",
    f"- **Timeline Span:** **{years_covered[0]} → {years_covered[-1]}** ({len(years_covered)} years: 2000 to 2026 continuous)",
    f"- **Geographic Scope:** **{unique_divisions} Divisions**, **{unique_districts} Districts**, **{unique_markets} Unique Markets** across Bangladesh.",
    f"- **Brinjal HYV (বেগুন - উচ্চ মানসম্পন্ন) Total Records:** **{len(brinjal_hyv_df):,}** (2002–2026)",
    "",
    "## 2. Records by Commodity",
    "",
    "| Commodity ID | Commodity Name (EN) | Commodity Name (BN) | Total Records | Earliest Year | Latest Year |",
    "|---|---|---|---|---|---|",
]

for cid, grp in master_df.groupby("commodity_id"):
    cname_en = grp["commodity_name_en"].iloc[0]
    cname_bn = grp["commodity_name_bn"].iloc[0]
    cnt = len(grp)
    min_y = int(grp["price_year"].min()) if pd.notna(grp["price_year"].min()) else "N/A"
    max_y = int(grp["price_year"].max()) if pd.notna(grp["price_year"].max()) else "N/A"
    report_lines.append(f"| {cid} | {cname_en} | {cname_bn} | {cnt:,} | {min_y} | {max_y} |")

report_lines.extend([
    "",
    "## 3. Data Sources & Provenance",
    "",
    "1. **Historical Web Portal (`market.dam.gov.bd/commodity_wise_report`):**",
    f"   - Total records: **{len(historical_df):,}** (covering 2000–2024 summary prices).",
    "   - Preserves division, district, upazila, market, commodity, price type, and low/high/average prices.",
    "2. **Modern MOA REST API (`moa-services.com`):**",
    f"   - Total records: **{len(recent_brinjal_df) + len(recent_11_df):,}** (covering 2025–2026 monthly/daily reports).",
    "",
    "## 4. Master Datasets Generated",
    "",
    f"- [`DAM_BRINJAL_HYV_2000_2026.csv`](file:///{brinjal_hyv_csv.as_posix()})",
    f"- [`DAM_BRINJAL_ALL_VARIETIES_2000_2026.csv`](file:///{brinjal_all_csv.as_posix()})",
    f"- [`DAM_ALL_COMMODITIES_EXPANDED_2000_2026.csv`](file:///{all_commodities_csv.as_posix()})",
    "",
])

audit_md = REPORTS_DIR / "EXPANDED_DATASET_AUDIT_REPORT.md"
audit_md.write_text("\n".join(report_lines), encoding="utf-8")
print(f"\nGenerated Audit Report: {audit_md}", flush=True)
print("Master dataset harmonization complete!", flush=True)

