#!/usr/bin/env python3
"""
MOA Services REST API Extractor (2025-2026) for Brinjal and Target Commodities.
Extracts market-monthly price reports across all nationwide markets.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import json
import time
import hashlib
import requests
import urllib3
from pathlib import Path
from datetime import datetime

urllib3.disable_warnings()

# ── Directories ─────────────────────────────────────────────────────────────
BASE_DIR = Path(r"D:\Desktop 22 8 26\datamain")
OUTPUT_DIR = BASE_DIR / "DAM_EXPANDED_2026"
RAW_JSON_DIR = OUTPUT_DIR / "raw_json"
CLEAN_DIR = OUTPUT_DIR / "clean_parts"

RAW_JSON_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# ── Load Token and Metadata ────────────────────────────────────────────────
with open(BASE_DIR / "dam_11_commodity_extractor.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
token_match = re.search(r'Bearer\s+([a-zA-Z0-9\.\-_]+)', text)
token = token_match.group(1) if token_match else ""

with open(BASE_DIR / "common_dropdowns.json", "r", encoding="utf-8") as f:
    d = json.load(f)

metadata = d.get('data', d)
market_list = metadata.get('marketList', [])

print(f"Loaded {len(market_list)} markets from metadata.", flush=True)

# ── Target Commodities for MOA Extractor ───────────────────────────────────
# We extract Brinjal HYV (949) and Brinjal Ordinary (950)
TARGET_COMMODITIES = [
    {
        "commodity_id": 949,
        "commodity_name_en": "Brinjal - Superior Quality",
        "commodity_name_bn": "বেগুন - উচ্চ মানসম্পন্ন",
        "commodity_group_id": 43,
        "commodity_sub_group_id": 266,
        "filename": "DAM_BRINJAL_HYV_RECENT_2025_2026.csv"
    },
    {
        "commodity_id": 950,
        "commodity_name_en": "Brinjal - Ordinary Quality",
        "commodity_name_bn": "বেগুন- সাধারণ মানসম্পন্ন",
        "commodity_group_id": 43,
        "commodity_sub_group_id": 266,
        "filename": "DAM_BRINJAL_ORDINARY_RECENT_2025_2026.csv"
    }
]

API_URL = "https://moa-services.com/agri-service/crop-price-info/reports/price-report/market-monthly-price-report"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
}

session = requests.Session()
session.headers.update(headers)

all_extracted_rows = []

print("=" * 70, flush=True)
print("STARTING MOA RECENT (2025-2026) EXTRACTION FOR BRINJAL VARIETIES", flush=True)
print("=" * 70, flush=True)

total_jobs = len(TARGET_COMMODITIES) * len(market_list)
job_idx = 0
data_found_count = 0
total_records = 0

for comm in TARGET_COMMODITIES:
    comm_id = comm["commodity_id"]
    comm_name = comm["commodity_name_en"]
    print(f"\n--- Extracting {comm_name} (ID: {comm_id}) ---", flush=True)
    
    for m in market_list:
        job_idx += 1
        mkt_id = m.get("value")
        mkt_name = m.get("text_en") or m.get("text")
        mkt_name_bn = m.get("text_bn")
        div_id = m.get("division_id")
        dist_id = m.get("district_id")
        upz_id = m.get("upazila_id")
        
        payload = {
            "division_id": [div_id] if div_id else [],
            "district_id": [dist_id] if dist_id else [],
            "upazila_id": [upz_id] if upz_id else [],
            "market_id": [mkt_id],
            "commodity_group_id": [comm["commodity_group_id"]],
            "commodity_sub_group_id": [comm["commodity_sub_group_id"]],
            "commodity_id": [comm_id],
            "year_from": 2010,
            "year_to": 2026,
            "month_from": None,
            "month_to": None,
            "page": 1,
            "per_page": 50000,
        }
        
        retries = 3
        records = []
        for attempt in range(retries):
            try:
                r = session.post(API_URL, json=payload, verify=False, timeout=25)
                if r.status_code == 200:
                    resp_data = r.json()
                    # Save raw evidence
                    raw_dir = RAW_JSON_DIR / str(mkt_id) / str(comm_id)
                    raw_dir.mkdir(parents=True, exist_ok=True)
                    stamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
                    raw_file = raw_dir / f"moa_{stamp}.json"
                    raw_file.write_text(r.text, encoding="utf-8")
                    
                    data_field = resp_data.get("data")
                    if isinstance(data_field, list):
                        records = data_field
                    elif isinstance(data_field, dict):
                        records = data_field.get("data", [])
                    break
                else:
                    time.sleep(0.5)
            except Exception as e:
                time.sleep(1.0)
        
        if records:
            data_found_count += 1
            total_records += len(records)
            print(f"[{job_idx}/{total_jobs}] DATA ({len(records)} rows) -> Market {mkt_id} ({mkt_name})", flush=True)
            for rec in records:
                row = {
                    "source": "moa_api",
                    "division_id": div_id,
                    "district_id": dist_id,
                    "upazila_id": upz_id,
                    "market_id": mkt_id,
                    "market_name": mkt_name,
                    "market_name_bn": mkt_name_bn,
                    "commodity_group_id": comm["commodity_group_id"],
                    "commodity_group_name_en": "Vegetable",
                    "commodity_sub_group_id": comm["commodity_sub_group_id"],
                    "commodity_sub_group_name_en": "Brinjal",
                    "commodity_id": comm_id,
                    "commodity_name_en": comm_name,
                    "commodity_name_bn": comm["commodity_name_bn"],
                    "price_date": rec.get("price_date"),
                    "price_year": rec.get("price_year") or (str(rec.get("price_date"))[:4] if rec.get("price_date") else None),
                    "price_month": rec.get("price_month"),
                    "price_month_name": rec.get("price_month_name"),
                    "wholesale_unit": rec.get("wholesale_unit"),
                    "retail_unit": rec.get("retail_unit"),
                    "wholesale_price_low": rec.get("wholesale_price_low"),
                    "wholesale_price_high": rec.get("wholesale_price_high"),
                    "wholesale_price_avg": rec.get("wholesale_price_avg"),
                    "retail_price_low": rec.get("retail_price_low"),
                    "retail_price_high": rec.get("retail_price_high"),
                    "retail_price_avg": rec.get("retail_price_avg"),
                    "created_at": rec.get("created_at"),
                }
                all_extracted_rows.append(row)
        else:
            if job_idx % 25 == 0:
                print(f"[{job_idx}/{total_jobs}] Progress: {data_found_count} markets with data so far ({total_records} total records)...", flush=True)
        
        time.sleep(0.1)

# Save intermediate clean CSV
import pandas as pd
if all_extracted_rows:
    df = pd.DataFrame(all_extracted_rows)
    out_csv = CLEAN_DIR / "moa_brinjal_recent_2025_2026.csv"
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print(f"\nSaved {len(df)} recent records to {out_csv}", flush=True)
else:
    print("No records extracted from MOA API.", flush=True)

print("MOA Recent Extraction Finished!", flush=True)
