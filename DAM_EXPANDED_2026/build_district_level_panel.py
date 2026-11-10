#!/usr/bin/env python3
"""
Build Harmonized 64-District Centroid-Anchored Panel (2000-2026)
Aggregates individual market records into robust district-level observations.
Attaches exact GADM 4.1 polygon centroids (lat, lon) and distance to Dhaka.
Merges NASA MERRA-2 / ERA-5 weather reanalysis and pre-harvest crop stages.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import math
import unicodedata
import pandas as pd
import numpy as np
from pathlib import Path

# Paths
BASE_DIR = Path(r"D:\Desktop 22 8 26\datamain")
PRICE_CSV = BASE_DIR / "DAM_EXPANDED_2026" / "master" / "DAM_ALL_COMMODITIES_EXPANDED_2000_2026.csv"
CENTROIDS_CSV = BASE_DIR / "PAPER_1_PRE_HARVEST_SHOCKS" / "data" / "gis" / "bangladesh_64_district_centroids_verified.csv"
WEATHER_CSV = BASE_DIR / "PAPER_1_PRE_HARVEST_SHOCKS" / "data" / "weather" / "bangladesh_64_districts_weather_2000_2026.csv"

OUT_DISTRICT_MASTER = BASE_DIR / "DAM_EXPANDED_2026" / "master" / "DAM_DISTRICT_PANEL_2000_2026.csv"
OUT_PANEL_V3 = BASE_DIR / "PAPER_1_PRE_HARVEST_SHOCKS" / "data" / "panel" / "paper_1_district_panel_v3.csv"
OUT_PANEL_SHOWCASE = BASE_DIR / "SHOWCASE" / "data" / "paper_1_district_panel_v3.csv"

OUT_PANEL_V3.parent.mkdir(parents=True, exist_ok=True)
OUT_PANEL_SHOWCASE.parent.mkdir(parents=True, exist_ok=True)

# Complete Bengali -> English mapping
def _norm_bn(s):
    if pd.isna(s) or not s:
        return ""
    return unicodedata.normalize("NFKC", str(s).strip())

RAW_BN_TO_EN = {
    # Dhaka Division
    "ঢাকা": "Dhaka", "গাজীপুর": "Gazipur", "মানিকগঞ্জ": "Manikganj",
    "মুন্সিগঞ্জ": "Munshiganj", "মুন্সীগঞ্জ": "Munshiganj", "নারায়ণগঞ্জ": "Narayanganj",
    "নারায়নগঞ্জ": "Narayanganj", "নরসিংদী": "Narsingdi", "ফরিদপুর": "Faridpur",
    "গোপালগঞ্জ": "Gopalganj", "মাদারিপুর": "Madaripur", "রাজবাড়ী": "Rajbari",
    "রাজবাড়ি": "Rajbari", "শরীয়তপুর": "Shariatpur", "শরিয়তপুর": "Shariatpur",
    "কিশোরগঞ্জ": "Kishoreganj", "টাঙ্গাইল": "Tangail",
    # Chattogram Division
    "চট্টগ্রাম": "Chittagong", "কক্সবাজার": "Cox's Bazar", "কক্স বাজার": "Cox's Bazar",
    "কুমিল্লা": "Comilla", "ব্রাহ্মণবাড়িয়া": "Brahmanbaria", "চাঁদপুর": "Chandpur",
    "ফেনী": "Feni", "ফেনি": "Feni", "লক্ষ্মীপুর": "Lakshmipur", "লক্ষীপুর": "Lakshmipur",
    "নোয়াখালী": "Noakhali", "খাগড়াছড়ি": "Khagrachhari", "রাঙ্গামাটি": "Rangamati",
    "বান্দরবান": "Bandarban", "কাপ্তাই": "Rangamati",
    # Rajshahi Division
    "রাজশাহী": "Rajshahi", "রাজশাহি": "Rajshahi", "বগুড়া": "Bogra",
    "জয়পুরহাট": "Joypurhat", "নওগাঁ": "Naogaon", "নাটোর": "Natore",
    "চাঁপাইনবাবগঞ্জ": "Chapainawabganj", "নবাবগঞ্জ": "Chapainawabganj",
    "পাবনা": "Pabna", "সিরাজগঞ্জ": "Sirajganj",
    # Khulna Division
    "খুলনা": "Khulna", "বাগেরহাট": "Bagerhat", "চুয়াডাঙ্গা": "Chuadanga",
    "যশোর": "Jessore", "ঝিনাইদহ": "Jhenaidah", "কুষ্টিয়া": "Kushtia",
    "মাগুরা": "Magura", "মেহেরপুর": "Meherpur", "নড়াইল": "Narail",
    "সাতক্ষীরা": "Satkhira", "সাতক্ষিরা": "Satkhira",
    # Barishal Division
    "বরিশাল": "Barisal", "বরগুনা": "Barguna", "ভোলা": "Bhola",
    "ঝালকাঠি": "Jhalakathi", "পটুয়াখালী": "Patuakhali", "পটুয়াখালি": "Patuakhali",
    "পিরোজপুর": "Pirojpur",
    # Sylhet Division
    "সিলেট": "Sylhet", "হবিগঞ্জ": "Habiganj", "মৌলভীবাজার": "Moulvibazar",
    "সুনামগঞ্জ": "Sunamganj",
    # Rangpur Division
    "রংপুর": "Rangpur", "দিনাজপুর": "Dinajpur", "গাইবান্ধা": "Gaibandha",
    "কুড়িগ্রাম": "Kurigram", "লালমনিরহাট": "Lalmonirhat", "নীলফামারী": "Nilphamari",
    "পঞ্চগড়": "Panchagarh", "ঠাকুরগাঁও": "Thakurgaon", "ঠাকুরগাঁ": "Thakurgaon",
    # Mymensingh Division
    "ময়মনসিংহ": "Mymensingh", "জামালপুর": "Jamalpur", "নেত্রকোণা": "Netrokona",
    "নেত্রকোনা": "Netrokona", "শেরপুর": "Sherpur"
}

BN_TO_EN = {_norm_bn(k): v for k, v in RAW_BN_TO_EN.items()}

def norm_key(s):
    if pd.isna(s):
        return ""
    return str(s).strip().lower().replace("'", "").replace("-", " ").replace(".", "")

def standardize_district(row):
    for col in ["district_name_en", "district_name_bn"]:
        raw = row.get(col)
        if pd.isna(raw):
            continue
        normed = _norm_bn(raw)
        if normed in BN_TO_EN:
            return BN_TO_EN[normed]
    # Substring search
    for col in ["district_name_en", "district_name_bn"]:
        raw = row.get(col)
        if pd.isna(raw):
            continue
        normed = _norm_bn(raw)
        for bn_norm, en_val in BN_TO_EN.items():
            if bn_norm in normed or normed in bn_norm:
                return en_val
    return None

def main():
    print("=" * 80)
    print("BUILDING 64-DISTRICT CENTROID-ANCHORED SPATIAL PANEL (2000-2026)")
    print("=" * 80)

    # 1. Load Raw Prices
    print(f"Loading prices from: {PRICE_CSV}")
    df = pd.read_csv(PRICE_CSV, low_memory=False)
    print(f"Total raw observations: {len(df):,}")

    # Standardize District
    df["std_district"] = df.apply(standardize_district, axis=1)
    df = df[df["std_district"].notna()].copy()
    print(f"Matched to canonical districts: {len(df):,} rows")

    # Clean prices
    for col in ["standardized_price_avg", "standardized_price_low", "standardized_price_high",
                "wholesale_price_avg", "retail_price_avg", "grower_price_avg"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove zero or negative prices
    df = df[df["standardized_price_avg"] > 0].copy()

    # Per-commodity winsorization at 1st and 99th percentile to remove data entry typos
    for cid in df["commodity_id"].unique():
        mask = df["commodity_id"] == cid
        vals = df.loc[mask, "standardized_price_avg"]
        if len(vals) > 20:
            p01 = vals.quantile(0.01)
            p99 = vals.quantile(0.99)
            df.loc[mask, "standardized_price_avg"] = vals.clip(lower=p01, upper=p99)

    # 2. Perform District-Level Aggregation
    df["year"] = df["price_year"].fillna(0).astype(int)
    df["month"] = df["price_month"].fillna(0).astype(int)

    # Grouping keys for pure District Panel
    group_cols = ["std_district", "commodity_id", "commodity_name_en", "commodity_name_bn", "price_type", "year", "month"]

    print("\nAggregating market observations to district-month level...")
    agg_df = df.groupby(group_cols).agg(
        price_mean_bdt_kg=("standardized_price_avg", "mean"),
        price_median_bdt_kg=("standardized_price_avg", "median"),
        price_min_bdt_kg=("standardized_price_avg", "min"),
        price_max_bdt_kg=("standardized_price_avg", "max"),
        price_std_bdt_kg=("standardized_price_avg", "std"),
        reporting_markets_count=("market_name_en", "nunique"),
        total_market_records=("standardized_price_avg", "count"),
        wholesale_price_mean=("wholesale_price_avg", "mean"),
        retail_price_mean=("retail_price_avg", "mean"),
        grower_price_mean=("grower_price_avg", "mean")
    ).reset_index()

    # Round price aggregations
    for p_col in ["price_mean_bdt_kg", "price_median_bdt_kg", "price_min_bdt_kg", "price_max_bdt_kg", "price_std_bdt_kg",
                  "wholesale_price_mean", "retail_price_mean", "grower_price_mean"]:
        agg_df[p_col] = agg_df[p_col].round(2)

    # Fill std with 0 if single market
    agg_df["price_std_bdt_kg"] = agg_df["price_std_bdt_kg"].fillna(0)

    # Log transforms
    agg_df["ln_price_mean"] = np.log(agg_df["price_mean_bdt_kg"])
    agg_df["ln_price_median"] = np.log(agg_df["price_median_bdt_kg"])
    agg_df["ln_wholesale"] = np.where(agg_df["wholesale_price_mean"] > 0, np.log(agg_df["wholesale_price_mean"]), np.nan)
    agg_df["ln_retail"] = np.where(agg_df["retail_price_mean"] > 0, np.log(agg_df["retail_price_mean"]), np.nan)
    agg_df["ln_grower"] = np.where(agg_df["grower_price_mean"] > 0, np.log(agg_df["grower_price_mean"]), np.nan)

    print(f"District-month aggregated panel size: {len(agg_df):,} observations")

    # 3. Merge Exact Centroids & Distances
    print(f"\nMerging verified district centroids from: {CENTROIDS_CSV}")
    df_centroids = pd.read_csv(CENTROIDS_CSV)
    df_centroids["dist_key"] = df_centroids["district_name_en"].apply(norm_key)
    agg_df["dist_key"] = agg_df["std_district"].apply(norm_key)

    agg_df = pd.merge(
        agg_df,
        df_centroids[["dist_key", "district_name_en", "district_name_bn", "division_name_en", 
                      "centroid_lat", "centroid_lon", "distance_to_dhaka_km"]],
        on="dist_key",
        how="left"
    )

    n_missing_centroids = agg_df["centroid_lat"].isna().sum()
    print(f"Centroid merge complete. Missing centroids: {n_missing_centroids} ({n_missing_centroids/len(agg_df)*100:.2f}%)")

    # 4. Merge NASA Weather Reanalysis & Pre-Harvest Shocks
    print(f"\nMerging NASA weather reanalysis from: {WEATHER_CSV}")
    df_weather = pd.read_csv(WEATHER_CSV)
    df_weather["dist_key"] = df_weather["district_name_en"].apply(norm_key)

    # Pre-harvest climate aggregates (Nov-Dec year t-1 + Jan-Feb year t for Rabi crops)
    pre_harvest_rows = []
    for d_key in df_weather["dist_key"].unique():
        w_d = df_weather[df_weather["dist_key"] == d_key]
        for h_year in range(2000, 2027):
            mask_prev = (w_d["year"] == h_year - 1) & (w_d["month"].isin([11, 12]))
            mask_curr = (w_d["year"] == h_year) & (w_d["month"].isin([1, 2]))
            ph_m = pd.concat([w_d[mask_prev], w_d[mask_curr]])
            if len(ph_m) == 0:
                continue
            
            precip_tot = ph_m["precip_total_mm"].sum()
            tmean_avg = ph_m["t_mean_c"].mean()
            tmax_avg = ph_m["t_max_c"].mean()
            precip_z = ph_m["precip_zscore"].mean()
            temp_z = ph_m["temp_zscore"].mean()

            drought_m = (ph_m["precip_zscore"] <= -1.0).sum()
            excess_rain_m = (ph_m["precip_zscore"] >= 1.0).sum()
            heatwave_m = ((ph_m["temp_zscore"] >= 1.0) | (ph_m["t_max_c"] > 33.0)).sum()

            pre_harvest_rows.append({
                "dist_key": d_key,
                "year": h_year,
                "ph_precip_mm": round(precip_tot, 2),
                "ph_tmean_c": round(tmean_avg, 2),
                "ph_tmax_c": round(tmax_avg, 2),
                "ph_precip_z": round(precip_z, 3),
                "ph_temp_z": round(temp_z, 3),
                "ph_drought_months": int(drought_m),
                "ph_excess_rain_months": int(excess_rain_m),
                "ph_heatwave_months": int(heatwave_m),
                "has_drought": int(drought_m > 0),
                "has_excess_rain": int(excess_rain_m > 0),
                "has_heatwave": int(heatwave_m > 0),
                "has_any_shock": int((drought_m + excess_rain_m + heatwave_m) > 0)
            })

    df_ph = pd.DataFrame(pre_harvest_rows)
    agg_df = pd.merge(agg_df, df_ph, on=["dist_key", "year"], how="left")

    # Fill weather missing
    for c in ["has_drought", "has_excess_rain", "has_heatwave", "has_any_shock",
              "ph_precip_z", "ph_temp_z", "ph_drought_months", "ph_excess_rain_months", "ph_heatwave_months"]:
        agg_df[c] = agg_df[c].fillna(0)

    # Commodity group identifiers
    agg_df["is_onion"] = agg_df["commodity_id"].isin([831, 832, 833]).astype(int)
    agg_df["is_potato"] = agg_df["commodity_id"].isin([942, 943, 944, 945, 946, 947]).astype(int)
    agg_df["is_brinjal"] = agg_df["commodity_id"].isin([949, 950]).astype(int)
    agg_df["is_distant"] = (agg_df["distance_to_dhaka_km"] >= 150.0).astype(int)

    agg_df["commodity_group"] = np.where(agg_df["is_onion"] == 1, "Onion",
                                np.where(agg_df["is_potato"] == 1, "Potato",
                                np.where(agg_df["is_brinjal"] == 1, "Brinjal", "Other")))

    # Clean columns ordering
    clean_cols = [
        "dist_key", "district_name_en", "district_name_bn", "division_name_en",
        "centroid_lat", "centroid_lon", "distance_to_dhaka_km", "is_distant",
        "commodity_id", "commodity_name_en", "commodity_name_bn", "commodity_group",
        "is_onion", "is_potato", "is_brinjal",
        "price_type", "year", "month",
        "price_mean_bdt_kg", "price_median_bdt_kg", "price_min_bdt_kg", "price_max_bdt_kg", "price_std_bdt_kg",
        "reporting_markets_count", "total_market_records",
        "ln_price_mean", "ln_price_median", "ln_wholesale", "ln_retail", "ln_grower",
        "ph_precip_mm", "ph_tmean_c", "ph_tmax_c", "ph_precip_z", "ph_temp_z",
        "ph_drought_months", "ph_excess_rain_months", "ph_heatwave_months",
        "has_drought", "has_excess_rain", "has_heatwave", "has_any_shock"
    ]

    final_df = agg_df[[c for c in clean_cols if c in agg_df.columns]].copy()
    final_df.sort_values(by=["district_name_en", "commodity_group", "year", "month"], inplace=True)

    print("\n" + "=" * 80)
    print("DISTRICT PANEL VALIDATION")
    print("=" * 80)
    print(f"Total District Observations: {len(final_df):,}")
    print(f"Unique Districts: {final_df['district_name_en'].nunique()} / 64")
    print(f"Years: {final_df['year'].min()} to {final_df['year'].max()}")
    print(f"Commodity breakdown: {final_df['commodity_group'].value_counts().to_dict()}")
    print(f"Price Types: {final_df['price_type'].value_counts().to_dict()}")
    print(f"Average Reporting Markets per District-Month: {final_df['reporting_markets_count'].mean():.2f}")
    print(f"Max Markets in a District: {final_df['reporting_markets_count'].max()}")
    print(f"Zero missing centroids: {final_df['centroid_lat'].isna().sum() == 0}")

    # Export
    print(f"\nSaving district master panel to:\n - {OUT_DISTRICT_MASTER}\n - {OUT_PANEL_V3}\n - {OUT_PANEL_SHOWCASE}")
    final_df.to_csv(OUT_DISTRICT_MASTER, index=False, encoding="utf-8-sig")
    final_df.to_csv(OUT_PANEL_V3, index=False, encoding="utf-8-sig")
    final_df.to_csv(OUT_PANEL_SHOWCASE, index=False, encoding="utf-8-sig")
    print("DONE! District Centroid-Anchored Panel successfully built.")

if __name__ == "__main__":
    main()
