#!/usr/bin/env python3
"""
DAM 11-Commodity Real Data Extractor
====================================

This script uses the DAM backend API directly.

INPUT
-----
common_dropdowns.json
    The DAM common-dropdowns response captured from the browser.
    It contains:
      - marketList (352 markets in the captured file)
      - commodityNameList (447 commodities)
      - measurementUnitList
      - other DAM metadata

AUTH
----
The DAM price endpoint currently requires the browser session's Bearer token.

On first run, the script reads (in this order):
1) DAM_BEARER_TOKEN environment variable
2) dam_token.txt (token only, no "Bearer " prefix)
3) interactive prompt

Optional:
    DAM_ACCESS_USER_ID
    DAM_ACCESS_USERNAME

The script does NOT store the token in source code or output files.

OUTPUT
------
dam_output/
  market_master.csv
  commodity_master_11.csv
  extraction_log.csv
  coverage_matrix.csv
  master/
      DAM_ONION_LOCAL_2010_2026.csv
      DAM_ONION_IMPORTED_2010_2026.csv
      DAM_ONION_NEW_2010_2026.csv
      DAM_POTATO_LOCAL_OLD_2010_2026.csv
      DAM_POTATO_LOCAL_2010_2026.csv
      DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv
      DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv
      DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv
      DAM_POTATO_HOLLAND_RED_2010_2026.csv
      DAM_SWEET_POTATO_2010_2026.csv
      DAM_POTATO_IMPORTED_2010_2026.csv
      DAM_ALL_11_COMMODITIES_2010_2026.csv
  raw_json/
      <market_id>/
          <commodity_id>.json
  clean_parts/
      <market_id>/
          <commodity_id>.csv

IMPORTANT
---------
- These are REAL DAM API responses when the script is run successfully.
- No synthetic values are generated.
- No Gemini API is used or needed.
- Raw JSON is retained unchanged.
- Missing markets/commodity combinations are recorded as NO_DATA.
- Failed requests are recorded as ERROR and can be retried by rerunning.
- The price API response does not include market IDs inside each price row,
  so the script queries one market at a time and attaches market metadata from
  the official marketList.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


API_URL = (
    "https://moa-services.com/agri-service/crop-price-info/"
    "reports/price-report/market-monthly-price-report"
)

REFERER = (
    "https://moa-services.com/market-directory/"
    "mothly-average-market-price-report"
)

YEAR_FROM = 2010
YEAR_TO = 2026

# Explicitly selected real DAM commodity IDs from common_dropdowns.json.
TARGET_COMMODITY_IDS = [
    831, 832, 833,
    942, 943, 944, 945, 946, 947, 948, 21014
]

DIVISION_NAMES = {
    1: "Chattogram",
    2: "Khulna",
    3: "Rajshahi",
    4: "Barishal",
    5: "Sylhet",
    6: "Dhaka",
    7: "Rangpur",
    8: "Mymensingh",
}


def safe_slug(text: str) -> str:
    text = str(text).strip()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s-]+", "_", text).strip("_")
    return text.upper() or "UNKNOWN"


def load_dropdowns(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        obj = json.load(f)
    if not obj.get("success"):
        raise ValueError("common_dropdowns.json does not have success=true")
    data = obj.get("data")
    if not isinstance(data, dict):
        raise ValueError("common_dropdowns.json has no usable data object")
    return data


def find_target_commodities(data: dict[str, Any]) -> pd.DataFrame:
    rows = data.get("commodityNameList", [])
    wanted = []
    by_id = {int(x["value"]): x for x in rows if x.get("value") is not None}

    missing = [cid for cid in TARGET_COMMODITY_IDS if cid not in by_id]
    if missing:
        raise ValueError(
            f"The captured common-dropdowns file does not contain commodity IDs: {missing}"
        )

    for cid in TARGET_COMMODITY_IDS:
        x = by_id[cid]
        wanted.append({
            "commodity_id": int(x["value"]),
            "commodity_group_id": int(x["commodity_group_id"]),
            "commodity_group_name_en": x.get("text_en") if False else None,
            "commodity_sub_group_id": int(x["commodity_sub_group_id"]),
            "commodity_sub_group_name_en": None,
            "commodity_name_en": (x.get("text_en") or x.get("text") or "").strip(),
            "commodity_name_bn": (x.get("text_bn") or "").strip(),
            "unit_id": x.get("unit_id"),
            "unit_grower": x.get("unit_grower"),
            "unit_wholesale": x.get("unit_whole_sale"),
            "unit_retail": x.get("unit_retail"),
        })

    # Fill group/subgroup English names from the corresponding lists.
    groups = {
        int(x["value"]): (x.get("text_en") or x.get("text") or "").strip()
        for x in data.get("commodityGroupList", [])
        if x.get("value") is not None
    }
    subgroups = {
        int(x["value"]): (x.get("text_en") or x.get("text") or "").strip()
        for x in data.get("commoditySubGroupList", [])
        if x.get("value") is not None
    }

    df = pd.DataFrame(wanted)
    df["commodity_group_name_en"] = df["commodity_group_id"].map(groups)
    df["commodity_sub_group_name_en"] = df["commodity_sub_group_id"].map(subgroups)
    return df


def build_market_master(data: dict[str, Any]) -> pd.DataFrame:
    rows = data.get("marketList", [])
    if not rows:
        raise ValueError("No marketList found in common_dropdowns.json")

    records = []
    for x in rows:
        if x.get("value") is None:
            continue
        div_id = int(x["division_id"]) if x.get("division_id") is not None else None
        records.append({
            "division_id": div_id,
            "division_name": DIVISION_NAMES.get(div_id, ""),
            "district_id": int(x["district_id"]) if x.get("district_id") is not None else None,
            "district_name": "",  # marketList does not carry district_name
            "upazila_id": int(x["upazila_id"]) if x.get("upazila_id") is not None else None,
            "upazila_name": "",   # marketList does not carry upazila_name
            "market_id": int(x["value"]),
            "market_name": (x.get("text_en") or x.get("text") or "").strip(),
            "market_name_bn": (x.get("text_bn") or "").strip(),
            "market_parent": x.get("parent"),
        })

    df = pd.DataFrame(records).drop_duplicates("market_id").reset_index(drop=True)
    if df["market_id"].isna().any():
        raise ValueError("Some market records have no market_id")
    return df


def get_token() -> str:
    token = os.environ.get("DAM_BEARER_TOKEN", "").strip()
    if token:
        return token.removeprefix("Bearer ").strip()

    token_file = Path("dam_token.txt")
    if token_file.exists():
        token = token_file.read_text(encoding="utf-8").strip()
        if token:
            return token.removeprefix("Bearer ").strip()

    print("\nDAM Bearer token required.")
    print("Paste ONLY the token text, not the word 'Bearer'.")
    token = getpass.getpass("Bearer token: ").strip()
    if not token:
        raise SystemExit("No DAM token supplied.")
    return token.removeprefix("Bearer ").strip()


def make_session(token: str) -> requests.Session:
    s = requests.Session()

    retry = Retry(
        total=5,
        connect=5,
        read=5,
        status=5,
        backoff_factor=1.25,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(["POST"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=8, pool_maxsize=8)
    s.mount("https://", adapter)

    s.headers.update({
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "https://moa-services.com",
        "Referer": REFERER,
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/148.0.0.0 Safari/537.36"
        ),
    })

    access_id = os.environ.get("DAM_ACCESS_USER_ID", "").strip()
    access_username = os.environ.get("DAM_ACCESS_USERNAME", "").strip()
    if access_id:
        s.headers["accessUserId"] = access_id
    if access_username:
        s.headers["accessUsername"] = access_username
    s.headers["accessMenuName"] = REFERER
    return s


def num(v: Any) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(str(v).replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def int_num(v: Any) -> int | None:
    if v is None or v == "":
        return None
    try:
        return int(float(v))
    except (ValueError, TypeError):
        return None


def unit_name(unit_id: Any, lookup: dict[int, str]) -> str:
    try:
        return lookup.get(int(unit_id), "")
    except (TypeError, ValueError):
        return ""


def request_payload(market: pd.Series, commodity: pd.Series) -> dict[str, Any]:
    return {
        "division_id": [int(market.division_id)],
        "district_id": [int(market.district_id)],
        "upazila_id": [int(market.upazila_id)],
        "market_id": [int(market.market_id)],
        "commodity_group_id": int(commodity.commodity_group_id),
        "commodity_sub_group_id": int(commodity.commodity_sub_group_id),
        "commodity_id": int(commodity.commodity_id),
        "year_from": YEAR_FROM,
        "year_to": YEAR_TO,
        "commodity_group_name_en": str(commodity.commodity_group_name_en or ""),
        "commodity_group_name_bn": "",
        "commodity_sub_group_name_en": str(commodity.commodity_sub_group_name_en or ""),
        "commodity_sub_group_name_bn": "",
        "commodity_name_en": str(commodity.commodity_name_en),
        "commodity_name_bn": str(commodity.commodity_name_bn),
        "year_from_en": YEAR_FROM,
        "year_from_bn": "২০১০",
        "year_to_en": YEAR_TO,
        "year_to_bn": "২০২৬",
    }


def fetch_one(
    market: pd.Series,
    commodity: pd.Series,
    token: str,
    timeout: int,
) -> tuple[str, dict[str, Any]]:
    session = make_session(token)
    payload = request_payload(market, commodity)
    response = session.post(API_URL, json=payload, timeout=timeout)

    try:
        obj = response.json()
    except ValueError:
        return "ERROR", {
            "http_status": response.status_code,
            "error": "API did not return JSON",
            "response_text": response.text[:3000],
            "payload": payload,
        }

    if response.status_code != 200:
        return "ERROR", {
            "http_status": response.status_code,
            "error": obj.get("message", f"HTTP {response.status_code}"),
            "response": obj,
            "payload": payload,
        }

    if not obj.get("success"):
        return "NO_DATA", {
            "http_status": response.status_code,
            "error": obj.get("message", "success=false"),
            "response": obj,
            "payload": payload,
        }

    data = obj.get("data") or []
    if not isinstance(data, list):
        return "ERROR", {
            "http_status": response.status_code,
            "error": "Unexpected API data type",
            "response": obj,
            "payload": payload,
        }

    if len(data) == 0:
        return "NO_DATA", {
            "http_status": response.status_code,
            "response": obj,
            "payload": payload,
        }

    return "DATA", {
        "http_status": response.status_code,
        "response": obj,
        "payload": payload,
    }


def clean_api_rows(
    market: pd.Series,
    commodity: pd.Series,
    wrapper: dict[str, Any],
    measurement_units: dict[int, str],
) -> pd.DataFrame:
    rows = wrapper["response"].get("data") or []
    out = []

    for row in rows:
        dt = pd.to_datetime(row.get("price_date"), errors="coerce")
        if pd.isna(dt):
            continue

        out.append({
            "division_id": int(market.division_id),
            "division_name": market.division_name,
            "district_id": int(market.district_id),
            "district_name": market.district_name,
            "upazila_id": int(market.upazila_id),
            "upazila_name": market.upazila_name,
            "market_id": int(market.market_id),
            "market_name": market.market_name,
            "market_name_bn": market.market_name_bn,

            "commodity_group_id": int(commodity.commodity_group_id),
            "commodity_group_name_en": commodity.commodity_group_name_en,
            "commodity_sub_group_id": int(commodity.commodity_sub_group_id),
            "commodity_sub_group_name_en": commodity.commodity_sub_group_name_en,
            "commodity_id": int(commodity.commodity_id),
            "commodity_name_en": commodity.commodity_name_en,
            "commodity_name_bn": commodity.commodity_name_bn,

            "price_date": dt.strftime("%Y-%m-%d"),
            "price_year": int(dt.year),
            "price_month": int(dt.month),
            "price_month_name": dt.strftime("%B"),

            "wholesale_unit_id": int_num(row.get("unit_whole_sale")),
            "wholesale_unit": unit_name(row.get("unit_whole_sale"), measurement_units),
            "retail_unit_id": int_num(row.get("unit_retail")),
            "retail_unit": unit_name(row.get("unit_retail"), measurement_units),

            "wholesale_price_low": num(row.get("w_lowestPrice")),
            "wholesale_price_high": num(row.get("w_highestPrice")),
            "wholesale_price_avg": num(row.get("w_avgPrice")),
            "retail_price_low": num(row.get("r_lowestPrice")),
            "retail_price_high": num(row.get("r_highestPrice")),
            "retail_price_avg": num(row.get("r_avgPrice")),

            "adjusted_wholesale_price_low": num(row.get("a_w_lowestPrice")),
            "adjusted_wholesale_price_high": num(row.get("a_w_highestPrice")),
            "adjusted_retail_price_low": num(row.get("a_r_lowestPrice")),
            "adjusted_retail_price_high": num(
                row.get("a_r_highestPrice", row.get("a_r_howestPrice"))
            ),

            "wholesale_supply": num(row.get("w_supply")),
            "unit_grower_id": int_num(row.get("unit_grower")),

            "cpi_market_commodity_price_id": int_num(
                row.get("cpi_market_commodity_price_id")
            ),
            "created_at": row.get("created_at"),
            "source_api": API_URL,
        })

    return pd.DataFrame(out)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def sanitize_filename(text: str) -> str:
    s = safe_slug(text)
    return s[:100]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", default="common_dropdowns.json")
    ap.add_argument("--out", default="dam_output")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--delay", type=float, default=0.30)
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--max-markets", type=int, default=0,
                    help="0 = all markets; useful for testing.")
    ap.add_argument("--no-resume", action="store_true")
    args = ap.parse_args()

    if args.workers < 1:
        raise SystemExit("--workers must be >= 1")

    metadata_path = Path(args.metadata)
    if not metadata_path.exists():
        raise SystemExit(
            f"Metadata file not found: {metadata_path}\n"
            "Put common_dropdowns.json beside this script."
        )

    data = load_dropdowns(metadata_path)
    markets = build_market_master(data)
    commodities = find_target_commodities(data)

    units = {
        int(x["value"]): (x.get("text_en") or x.get("text") or "").strip()
        for x in data.get("measurementUnitList", [])
        if x.get("value") is not None
    }

    out = Path(args.out)
    raw_dir = out / "raw_json"
    clean_dir = out / "clean_parts"
    master_dir = out / "master"
    for p in [raw_dir, clean_dir, master_dir]:
        p.mkdir(parents=True, exist_ok=True)

    markets.to_csv(out / "market_master.csv", index=False, encoding="utf-8-sig")
    commodities.to_csv(
        out / "commodity_master_11.csv", index=False, encoding="utf-8-sig"
    )

    if args.max_markets > 0:
        markets = markets.head(args.max_markets).copy()

    token = get_token()

    # Build jobs.
    jobs = []
    for _, market in markets.iterrows():
        for _, commodity in commodities.iterrows():
            jobs.append((market, commodity))

    print(f"\nMarkets: {len(markets):,}")
    print(f"Target commodities: {len(commodities):,}")
    print(f"Requests planned: {len(jobs):,}")
    print(f"Period: {YEAR_FROM}-{YEAR_TO}")
    print(f"Workers: {args.workers}")
    print("\nStarting...\n")

    log_path = out / "extraction_log.csv"

    # Completed set for resume.
    completed = set()
    if log_path.exists() and not args.no_resume:
        old = pd.read_csv(log_path)
        if {"market_id", "commodity_id", "status"}.issubset(old.columns):
            for _, r in old.iterrows():
                if r.status in {"DATA", "NO_DATA"}:
                    completed.add((int(r.market_id), int(r.commodity_id)))

    log_lock = __import__("threading").Lock()

    # Write header if new.
    if not log_path.exists():
        pd.DataFrame(columns=[
            "timestamp_utc", "status", "market_id", "commodity_id",
            "commodity_name_en", "rows", "raw_file", "clean_file", "error"
        ]).to_csv(log_path, index=False, encoding="utf-8-sig")

    def do_job(pair):
        market, commodity = pair
        key = (int(market.market_id), int(commodity.commodity_id))
        if key in completed:
            return {
                "skipped": True,
                "market": market,
                "commodity": commodity,
            }

        # Small randomized delay per worker to avoid synchronized bursts.
        if args.delay > 0:
            time.sleep(args.delay * random.uniform(0.75, 1.25))

        status, wrapper = fetch_one(
            market, commodity, token, args.timeout
        )

        raw_path = raw_dir / str(int(market.market_id)) / (
            f"{int(commodity.commodity_id)}.json"
        )
        save_json(raw_path, wrapper)

        clean_path = clean_dir / str(int(market.market_id)) / (
            f"{int(commodity.commodity_id)}.csv"
        )

        rows = 0
        if status == "DATA":
            df = clean_api_rows(market, commodity, wrapper, units)
            df.to_csv(clean_path, index=False, encoding="utf-8-sig")
            rows = len(df)

        return {
            "skipped": False,
            "status": status,
            "market_id": int(market.market_id),
            "commodity_id": int(commodity.commodity_id),
            "commodity_name_en": commodity.commodity_name_en,
            "rows": rows,
            "raw_file": str(raw_path),
            "clean_file": str(clean_path) if status == "DATA" else "",
            "error": wrapper.get("error", ""),
            "market": market,
            "commodity": commodity,
        }

    total = len(jobs)
    done_counter = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_map = {executor.submit(do_job, job): job for job in jobs}

        for future in as_completed(future_map):
            result = future.result()
            if result.get("skipped"):
                continue

            done_counter += 1
            row = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "status": result["status"],
                "market_id": result["market_id"],
                "commodity_id": result["commodity_id"],
                "commodity_name_en": result["commodity_name_en"],
                "rows": result["rows"],
                "raw_file": result["raw_file"],
                "clean_file": result["clean_file"],
                "error": result["error"],
            }

            # Append one log row at a time.
            log_df = pd.DataFrame([row])
            with log_lock:
                log_df.to_csv(
                    log_path,
                    mode="a",
                    header=False,
                    index=False,
                    encoding="utf-8-sig",
                )

            print(
                f"[{done_counter:,}/{total:,}] "
                f"{result['status']:8s} "
                f"market={result['market_id']} "
                f"commodity={result['commodity_id']} "
                f"rows={result['rows']}"
            )

    # Rebuild each commodity CSV from clean parts.
    all_parts = list(clean_dir.glob("*/*.csv"))
    master_frames = []
    for p in all_parts:
        try:
            master_frames.append(pd.read_csv(p))
        except Exception as exc:
            print(f"WARNING: could not read {p}: {exc}")

    if not master_frames:
        print("\nNo DATA responses were collected.")
        return

    master = pd.concat(master_frames, ignore_index=True)

    master = master.drop_duplicates(
        subset=[
            "market_id", "commodity_id", "price_date",
            "cpi_market_commodity_price_id"
        ],
        keep="first",
    )

    master["price_date"] = pd.to_datetime(
        master["price_date"], errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    master = master.sort_values(
        [
            "commodity_id", "division_id", "district_id",
            "upazila_id", "market_id", "price_date"
        ],
        kind="stable",
    ).reset_index(drop=True)

    # Separate 11 CSVs.
    for cid in TARGET_COMMODITY_IDS:
        sub = master[master["commodity_id"] == cid].copy()
        if sub.empty:
            # Still create an empty CSV with the correct headers.
            sub = master.iloc[0:0].copy()

        name = str(
            commodities.loc[
                commodities["commodity_id"] == cid, "commodity_name_en"
            ].iloc[0]
        )
        file_name = f"DAM_{sanitize_filename(name)}_2010_2026.csv"

        sub.to_csv(
            master_dir / file_name,
            index=False,
            encoding="utf-8-sig",
        )
        print(f"Saved {file_name}: {len(sub):,} rows")

    # Combined file.
    master.to_csv(
        master_dir / "DAM_ALL_11_COMMODITIES_2010_2026.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Coverage matrix.
    coverage = (
        master.groupby(
            ["commodity_id", "commodity_name_en", "market_id", "market_name"],
            dropna=False
        )
        .agg(
            first_date=("price_date", "min"),
            last_date=("price_date", "max"),
            observations=("price_date", "count"),
            years=("price_year", "nunique"),
        )
        .reset_index()
    )
    coverage.to_csv(
        out / "coverage_matrix.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Human-readable summary.
    summary = (
        master.groupby(
            ["commodity_id", "commodity_name_en"], dropna=False
        )
        .agg(
            observations=("price_date", "count"),
            markets=("market_id", "nunique"),
            first_date=("price_date", "min"),
            last_date=("price_date", "max"),
            mean_wholesale=("wholesale_price_avg", "mean"),
            median_wholesale=("wholesale_price_avg", "median"),
            missing_wholesale_avg=("wholesale_price_avg", lambda x: int(x.isna().sum())),
            mean_retail=("retail_price_avg", "mean"),
            median_retail=("retail_price_avg", "median"),
            missing_retail_avg=("retail_price_avg", lambda x: int(x.isna().sum())),
        )
        .reset_index()
    )
    summary.to_csv(
        out / "summary_11_commodities.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\n============================================")
    print("EXTRACTION COMPLETE")
    print("============================================")
    print(f"Master rows: {len(master):,}")
    print(f"Output: {master_dir.resolve()}")
    print("11 separate CSVs + one combined CSV created.")
    print("Raw JSON and extraction logs are preserved.")


if __name__ == "__main__":
    main()
