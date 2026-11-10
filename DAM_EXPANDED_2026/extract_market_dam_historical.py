#!/usr/bin/env python3
"""
Historical Web Extractor (2000-2024) from market.dam.gov.bd commodity_wise_report.
Extracts TRUE MONTHLY agricultural prices nationwide across all 64 districts, upazilas, and markets
for all 12 key commodities and all 3 price tiers (Wholesale, Retail, Grower).
"""

import sys
import io
import os
import time
import calendar
import unicodedata
import threading
import requests
import urllib3
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings()
sys.stdout.reconfigure(encoding='utf-8')

# ── Directories ─────────────────────────────────────────────────────────────
BASE_DIR = Path(r"D:\Desktop 22 8 26\datamain")
OUTPUT_DIR = BASE_DIR / "DAM_EXPANDED_2026"
RAW_HTML_DIR = OUTPUT_DIR / "raw_html_monthly"
CLEAN_DIR = OUTPUT_DIR / "clean_parts"
MONTHLY_PARTS_DIR = CLEAN_DIR / "monthly_slices"

RAW_HTML_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_DIR.mkdir(parents=True, exist_ok=True)
MONTHLY_PARTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Bengali Digit Converter ────────────────────────────────────────────────
BN_DIGIT_MAP = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

def clean_numeric(val):
    if not val:
        return None
    s = str(val).strip().translate(BN_DIGIT_MAP).replace(",", "").replace(" ", "")
    try:
        return float(s)
    except (ValueError, TypeError):
        return None

def norm(s):
    if not s:
        return ""
    return unicodedata.normalize("NFKC", str(s)).strip().replace(" ", "").replace("-", "")

# ── Commodity Configuration & Mappings ──────────────────────────────────────
COMMODITY_MAPPING = {
    norm("বেগুন - উচ্চ মানসম্পন্ন"): (949, "Brinjal - Superior Quality", "বেগুন - উচ্চ মানসম্পন্ন"),
    norm("বেগুন - সাধারণ মানসম্পন্ন"): (950, "Brinjal - Ordinary Quality", "বেগুন- সাধারণ মানসম্পন্ন"),
    norm("বেগুন- সাধারণ মানসম্পন্ন"): (950, "Brinjal - Ordinary Quality", "বেগুন- সাধারণ মানসম্পন্ন"),
    norm("পেঁয়াজ - দেশী"): (831, "Onion (local)", "পেঁয়াজ- দেশীয়"),
    norm("পেঁয়াজ- দেশীয়"): (831, "Onion (local)", "পেঁয়াজ- দেশীয়"),
    norm("পেঁয়াজ - আমদানিকৃত"): (832, "Onion-imported", "পেঁয়াজ- আমদানীকৃত"),
    norm("পেঁয়াজ- আমদানীকৃত"): (832, "Onion-imported", "পেঁয়াজ- আমদানীকৃত"),
    norm("পেঁয়াজ (নতুন)"): (833, "Onion (New)", "পেঁয়াজ"),
    norm("পেঁয়াজ"): (833, "Onion (New)", "পেঁয়াজ"),
    norm("আলু (দেশী)"): (942, "Potato (Local) - Old", "আলু (দেশীয়) - পুরানো"),
    norm("আলু (দেশীয়) - পুরানো"): (942, "Potato (Local) - Old", "আলু (দেশীয়) - পুরানো"),
    norm("আলু (দেশী) - নতুন"): (943, "Potato (Local)", "আলু (দেশীয়)"),
    norm("আলু (দেশীয়)"): (943, "Potato (Local)", "আলু (দেশীয়)"),
    norm("আলু (হল্যান্ড) - সাদা"): (944, "Potato (Holland) - White (Old)", "আলু (হলান্ড)- সাদা (পুরানো)"),
    norm("আলু (হলান্ড)- সাদা (পুরানো)"): (944, "Potato (Holland) - White (Old)", "আলু (হলান্ড)- সাদা (পুরানো)"),
    norm("আলু (হল্যান্ড)"): (945, "Potato (Holland) - White (New)", "আলু (হল্যান্ড) - সাদা"),
    norm("আলু (হল্যান্ড) - লাল (পুরাতন)"): (946, "Potato (Holland) - Red (Old)", "আলু (হল্যান্ড) - লাল (পুরানো)"),
    norm("আলু (হল্যান্ড) - লাল (পুরানো)"): (946, "Potato (Holland) - Red (Old)", "আলু (হল্যান্ড) - লাল (পুরানো)"),
    norm("আলু (হল্যান্ড) - লাল"): (947, "Potato (Holland) - Red", "আলু (হল্যান্ড) - লাল"),
    norm("মিষ্টি আলু"): (948, "Sweet Potato", "মিষ্টি আলু"),
}

TARGET_COMMODITIES = [
    ("43|শাকসবজি", "949|বেগুন - উচ্চ মানসম্পন্ন"),
    ("43|শাকসবজি", "950|বেগুন - সাধারণ মানসম্পন্ন"),
    ("32|মসলা", "831|পেঁয়াজ - দেশী"),
    ("32|মসলা", "832|পেঁয়াজ - আমদানিকৃত"),
    ("32|মসলা", "833|পেঁয়াজ (নতুন)"),
    ("43|শাকসবজি", "942|আলু (দেশী)"),
    ("43|শাকসবজি", "943|আলু (দেশী) - নতুন"),
    ("43|শাকসবজি", "944|আলু (হল্যান্ড) - সাদা"),
    ("43|শাকসবজি", "945|আলু (হল্যান্ড)"),
    ("43|শাকসবজি", "946|আলু (হল্যান্ড) - লাল (পুরাতন)"),
    ("43|শাকসবজি", "947|আলু (হল্যান্ড) - লাল"),
    ("43|শাকসবজি", "948|মিষ্টি আলু"),
]

PRICE_TYPES = [
    "5|পাইকারী",
    "4|খুচরা ",
    "3|উৎপাদক",
]

PRICE_TYPE_MAP = {
    "পাইকারী": "wholesale",
    "পাইকারি": "wholesale",
    "খুচরা": "retail",
    "উৎপাদক": "grower",
}

URL = "https://market.dam.gov.bd/commodity_wise_report"

def create_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
        "Origin": "https://market.dam.gov.bd",
        "Referer": "https://market.dam.gov.bd/commodity_wise_report",
    })
    return s

def get_csrf(session):
    for _ in range(5):
        try:
            r = session.get(URL, verify=False, timeout=30)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                csrf = soup.find("input", {"name": "csrf_webspice_tkn"})
                if csrf and csrf.get("value"):
                    return csrf.get("value")
        except Exception:
            time.sleep(2)
    return None

# Build complete list of monthly tasks: 2000 through 2024
MONTH_TASKS = []
for year in range(2000, 2025):
    for month in range(1, 13):
        last_day = calendar.monthrange(year, month)[1]
        d_from = f"{year}-{month:02d}-01"
        d_to = f"{year}-{month:02d}-{last_day:02d}"
        MONTH_TASKS.append((year, month, d_from, d_to))

print("=" * 80, flush=True)
print("TRUE MONTHLY HISTORICAL DAM EXTRACTOR (2000–2024)", flush=True)
print(f"Total months to extract: {len(MONTH_TASKS)} (25 years * 12 months)", flush=True)
print(f"Target commodities per month: {len(TARGET_COMMODITIES)} (all in single multi-query)", flush=True)
print(f"Target price types per month: 3 (Wholesale, Retail, Grower)", flush=True)
print("=" * 80, flush=True)

lock = threading.Lock()
completed_slices = 0
total_records_extracted = 0

def fetch_month_slice(task):
    global completed_slices, total_records_extracted
    year, month, d_from, d_to = task
    slice_csv = MONTHLY_PARTS_DIR / f"dam_monthly_{year}_{month:02d}.csv"
    
    # Check if slice is already completed and non-empty
    if slice_csv.exists() and slice_csv.stat().st_size > 100:
        try:
            existing_df = pd.read_csv(slice_csv)
            with lock:
                completed_slices += 1
                total_records_extracted += len(existing_df)
                print(f"[{completed_slices}/{len(MONTH_TASKS)}] RESUMED: {d_from}..{d_to} -> {len(existing_df)} rows", flush=True)
            return len(existing_df)
        except Exception:
            pass

    session = create_session()
    csrf_token = get_csrf(session)
    
    post_data = [("csrf_webspice_tkn", csrf_token or "")]
    for grp in sorted(set(g for g, _ in TARGET_COMMODITIES)):
        post_data.append(("CommodityGroup_id[]", grp))
    for _, comm in TARGET_COMMODITIES:
        post_data.append(("Commodity_id[]", comm))
    for pt in PRICE_TYPES:
        post_data.append(("PriceType_id[]", pt))
    post_data.extend([
        ("date_from", d_from),
        ("date_end", d_to),
        ("filter", "Filter Data"),
    ])
    
    records = []
    html_text = ""
    
    for attempt in range(4):
        try:
            if not csrf_token:
                csrf_token = get_csrf(session)
                post_data[0] = ("csrf_webspice_tkn", csrf_token or "")
            
            t0 = time.time()
            resp = session.post(URL, data=post_data, verify=False, timeout=80)
            dur = time.time() - t0
            
            if resp.status_code == 200:
                html_text = resp.text
                sp = BeautifulSoup(html_text, "html.parser")
                new_csrf = sp.find("input", {"name": "csrf_webspice_tkn"})
                if new_csrf and new_csrf.get("value"):
                    csrf_token = new_csrf.get("value")
                
                tbl = sp.find("table")
                if tbl:
                    trs = tbl.find_all("tr")
                    if len(trs) > 1:
                        for tr in trs[1:]:
                            tds = [c.text.strip().replace("\n", " ") for c in tr.find_all(["th", "td"])]
                            if len(tds) >= 10:
                                raw_comm = tds[4]
                                k = norm(raw_comm)
                                mapped_info = COMMODITY_MAPPING.get(k)
                                
                                if mapped_info:
                                    cid, cname_en, cname_bn = mapped_info
                                else:
                                    # Fallback partial matching
                                    matched = False
                                    for map_k, map_v in COMMODITY_MAPPING.items():
                                        if map_k in k or k in map_k:
                                            cid, cname_en, cname_bn = map_v
                                            matched = True
                                            break
                                    if not matched:
                                        continue
                                
                                raw_ptype = tds[5].strip()
                                ptype_code = PRICE_TYPE_MAP.get(raw_ptype, "wholesale")
                                
                                rec = {
                                    "source": "dam_historical_web",
                                    "division_name_bn": tds[0],
                                    "district_name_bn": tds[1],
                                    "upazila_name_bn": tds[2],
                                    "market_name_bn": tds[3],
                                    "commodity_name_raw_bn": raw_comm,
                                    "price_type_raw_bn": raw_ptype,
                                    "price_type": ptype_code,
                                    "commodity_id": cid,
                                    "commodity_name_en": cname_en,
                                    "commodity_name_bn": cname_bn,
                                    "price_date": f"{year}-{month:02d}-15",
                                    "price_year": year,
                                    "price_month": month,
                                    "price_month_name": calendar.month_name[month],
                                    "price_low": clean_numeric(tds[7]),
                                    "price_high": clean_numeric(tds[8]),
                                    "price_avg": clean_numeric(tds[9]),
                                    "query_date_from": d_from,
                                    "query_date_to": d_to,
                                }
                                records.append(rec)
                break
            else:
                csrf_token = get_csrf(session)
                time.sleep(2.0)
        except Exception:
            csrf_token = get_csrf(session)
            time.sleep(3.0)
            
    # Save raw HTML snapshot
    if html_text:
        raw_file = RAW_HTML_DIR / f"dam_raw_{year}_{month:02d}.html"
        raw_file.write_text(html_text, encoding="utf-8")
        
    # Save slice CSV
    if records:
        df_slice = pd.DataFrame(records)
        df_slice.to_csv(slice_csv, index=False, encoding="utf-8-sig")
    else:
        # Save empty file to record completion
        pd.DataFrame(columns=[
            "source", "division_name_bn", "district_name_bn", "upazila_name_bn",
            "market_name_bn", "commodity_name_raw_bn", "price_type_raw_bn",
            "price_type", "commodity_id", "commodity_name_en", "commodity_name_bn",
            "price_date", "price_year", "price_month", "price_month_name",
            "price_low", "price_high", "price_avg", "query_date_from", "query_date_to"
        ]).to_csv(slice_csv, index=False, encoding="utf-8-sig")
        
    with lock:
        completed_slices += 1
        total_records_extracted += len(records)
        print(f"[{completed_slices}/{len(MONTH_TASKS)}] EXTRACTED: {d_from}..{d_to} -> {len(records)} rows (Total: {total_records_extracted:,})", flush=True)
        
    time.sleep(0.5)
    return len(records)

# Run multithreaded extraction with 4 workers
print("\nLaunching multithreaded extraction pool (4 workers)...\n", flush=True)
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(fetch_month_slice, task) for task in MONTH_TASKS]
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as exc:
            print(f"Error in task: {exc}", flush=True)

# Combine all monthly slices
print("\nCombining all monthly clean slices into unified historical dataset...", flush=True)
all_slices = list(MONTHLY_PARTS_DIR.glob("dam_monthly_*.csv"))
all_frames = []
for p in sorted(all_slices):
    try:
        fdf = pd.read_csv(p)
        if not fdf.empty:
            all_frames.append(fdf)
    except Exception as e:
        print(f"Warning reading {p}: {e}")

if all_frames:
    full_historical_df = pd.concat(all_frames, ignore_index=True)
    full_historical_df = full_historical_df.drop_duplicates(
        subset=["division_name_bn", "district_name_bn", "upazila_name_bn", "market_name_bn",
                "commodity_id", "price_type", "price_year", "price_month", "price_avg"]
    )
    full_historical_df = full_historical_df.sort_values(
        ["commodity_id", "price_year", "price_month", "division_name_bn", "district_name_bn"]
    ).reset_index(drop=True)
    
    out_master_csv = CLEAN_DIR / "dam_historical_monthly_2000_2024.csv"
    full_historical_df.to_csv(out_master_csv, index=False, encoding="utf-8-sig")
    
    # Also overwrite the old dam_historical_web_2000_2024.csv so legacy paths have the clean monthly data
    legacy_csv = CLEAN_DIR / "dam_historical_web_2000_2024.csv"
    full_historical_df.to_csv(legacy_csv, index=False, encoding="utf-8-sig")
    
    print("\n" + "=" * 80)
    print("HISTORICAL EXTRACTION SUCCESSFUL!")
    print(f"Total Unique Monthly Observations: {len(full_historical_df):,}")
    print(f"Saved to: {out_master_csv}")
    print(f"Date Span: {full_historical_df['price_date'].min()} -> {full_historical_df['price_date'].max()}")
    print(f"Unique Months Present: {sorted(full_historical_df['price_month'].unique())}")
    print("=" * 80)
else:
    print("No records extracted.")
