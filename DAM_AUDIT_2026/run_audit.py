"""
DAM Agricultural Price Data — Comprehensive Audit Script
=========================================================
READ-ONLY: This script reads original CSVs but NEVER modifies them.
All outputs are written to DAM_AUDIT_2026/ folder.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
MASTER_DIR = BASE_DIR / "dam_output" / "master"
OUTPUT_DIR = BASE_DIR / "DAM_AUDIT_2026"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── The 11 individual commodity files ──────────────────────────────────────
CSV_FILES = [
    "DAM_ONION_LOCAL_2010_2026.csv",
    "DAM_ONION_IMPORTED_2010_2026.csv",
    "DAM_ONION_NEW_2010_2026.csv",
    "DAM_POTATO_LOCAL_2010_2026.csv",
    "DAM_POTATO_LOCAL_OLD_2010_2026.csv",
    "DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv",
    "DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv",
    "DAM_POTATO_HOLLAND_RED_2010_2026.csv",
    "DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv",
    "DAM_POTATOES_IMPORTED_2010_2026.csv",
    "DAM_SWEET_POTATO_2010_2026.csv",
]

print("=" * 80)
print("DAM DATA AUDIT — READ-ONLY MODE")
print("=" * 80)
print(f"Source:  {MASTER_DIR}")
print(f"Output:  {OUTPUT_DIR}")
print(f"Run at:  {datetime.now().isoformat()}")
print()

# ── Load all data ──────────────────────────────────────────────────────────
datasets = {}
for fname in CSV_FILES:
    fpath = MASTER_DIR / fname
    df = pd.read_csv(fpath)
    # Parse dates
    if 'price_date' in df.columns:
        df['price_date'] = pd.to_datetime(df['price_date'], errors='coerce')
    datasets[fname] = df
    print(f"  Loaded {fname}: {len(df)} rows × {len(df.columns)} cols")

print(f"\nTotal files loaded: {len(datasets)}")
print()

# ══════════════════════════════════════════════════════════════════════════
# A. DATASET INVENTORY
# ══════════════════════════════════════════════════════════════════════════
print("─" * 60)
print("A. DATASET INVENTORY")
print("─" * 60)

inventory_rows = []
for fname, df in datasets.items():
    commodity = df['commodity_name_en'].unique() if 'commodity_name_en' in df.columns else ['UNKNOWN']
    commodity_str = "; ".join([str(c) for c in commodity])
    
    unique_markets = df['market_name'].nunique() if 'market_name' in df.columns else 0
    unique_districts = df['district_name'].dropna().nunique() if 'district_name' in df.columns else 0
    unique_upazilas = df['upazila_name'].dropna().nunique() if 'upazila_name' in df.columns else 0
    
    first_date = df['price_date'].min() if 'price_date' in df.columns else None
    last_date = df['price_date'].max() if 'price_date' in df.columns else None
    
    unique_years = sorted(df['price_year'].dropna().unique().tolist()) if 'price_year' in df.columns else []
    unique_months = sorted(df['price_month'].dropna().unique().tolist()) if 'price_month' in df.columns else []
    
    row = {
        'filename': fname,
        'commodity': commodity_str,
        'num_rows': len(df),
        'num_columns': len(df.columns),
        'unique_markets': unique_markets,
        'unique_districts': unique_districts,
        'unique_upazilas': unique_upazilas,
        'first_date': str(first_date.date()) if pd.notna(first_date) else 'N/A',
        'last_date': str(last_date.date()) if pd.notna(last_date) else 'N/A',
        'unique_years': str(unique_years),
        'unique_months': str(unique_months),
        'num_unique_years': len(unique_years),
        'num_unique_months': len(unique_months),
    }
    inventory_rows.append(row)
    print(f"  {fname}: {len(df)} rows, {unique_markets} markets, "
          f"{str(first_date.date()) if pd.notna(first_date) else 'N/A'} to "
          f"{str(last_date.date()) if pd.notna(last_date) else 'N/A'}")

inventory_df = pd.DataFrame(inventory_rows)
inventory_df.to_csv(OUTPUT_DIR / "dataset_inventory.csv", index=False)
print(f"\n  ✓ Saved dataset_inventory.csv")

# ══════════════════════════════════════════════════════════════════════════
# B. MISSINGNESS REPORT
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("B. MISSINGNESS REPORT")
print("─" * 60)

missingness_rows = []
for fname, df in datasets.items():
    total_rows = len(df)
    
    # Missing values by column
    for col in df.columns:
        missing_count = df[col].isna().sum()
        # Also count empty strings
        if df[col].dtype == 'object':
            empty_str = (df[col] == '').sum()
            missing_count += empty_str
        pct_missing = round(100.0 * missing_count / total_rows, 2) if total_rows > 0 else 0
        missingness_rows.append({
            'filename': fname,
            'column': col,
            'missing_count': int(missing_count),
            'total_rows': total_rows,
            'pct_missing': pct_missing,
        })
    
    # Summary stats per file
    empty_cols = [col for col in df.columns if df[col].isna().all()]
    num_duplicates = df.duplicated().sum()
    
    # Duplicate observations by market + commodity + date
    dup_cols = ['market_name', 'commodity_name_en', 'price_date']
    dup_cols_avail = [c for c in dup_cols if c in df.columns]
    dup_market_commodity_date = df.duplicated(subset=dup_cols_avail).sum() if len(dup_cols_avail) == 3 else -1
    
    missingness_rows.append({
        'filename': fname,
        'column': '__SUMMARY__',
        'missing_count': -1,
        'total_rows': total_rows,
        'pct_missing': -1,
        'completely_empty_columns': len(empty_cols),
        'empty_column_names': "; ".join(empty_cols) if empty_cols else "None",
        'duplicate_rows': int(num_duplicates),
        'duplicate_market_commodity_date': int(dup_market_commodity_date),
    })
    
    print(f"  {fname}: {len(empty_cols)} empty cols, "
          f"{num_duplicates} dup rows, {dup_market_commodity_date} dup market-commodity-date")

missingness_df = pd.DataFrame(missingness_rows)
missingness_df.to_csv(OUTPUT_DIR / "missingness_report.csv", index=False)
print(f"\n  ✓ Saved missingness_report.csv")

# ══════════════════════════════════════════════════════════════════════════
# C. COVERAGE
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("C. COVERAGE ANALYSIS")
print("─" * 60)

# ── Market Coverage ────────────────────────────────────────────────────────
market_coverage_rows = []
for fname, df in datasets.items():
    commodity = df['commodity_name_en'].iloc[0] if 'commodity_name_en' in df.columns and len(df) > 0 else 'UNKNOWN'
    
    if 'market_name' not in df.columns:
        continue
    
    market_obs = df.groupby('market_name').size().reset_index(name='obs_count')
    
    for _, mrow in market_obs.iterrows():
        mkt = mrow['market_name']
        obs = mrow['obs_count']
        mkt_data = df[df['market_name'] == mkt]
        
        first = mkt_data['price_date'].min()
        last = mkt_data['price_date'].max()
        
        # Unique year-months
        if 'price_year' in mkt_data.columns and 'price_month' in mkt_data.columns:
            ym = mkt_data[['price_year', 'price_month']].drop_duplicates()
            n_months_covered = len(ym)
        else:
            n_months_covered = 0
        
        # Longest continuous monthly run
        if 'price_year' in mkt_data.columns and 'price_month' in mkt_data.columns:
            ym_sorted = ym.sort_values(['price_year', 'price_month'])
            ym_sorted = ym_sorted.copy()
            ym_sorted['ym_idx'] = ym_sorted['price_year'] * 12 + ym_sorted['price_month']
            ym_sorted = ym_sorted.sort_values('ym_idx')
            diffs = ym_sorted['ym_idx'].diff().fillna(1)
            groups = (diffs != 1).cumsum()
            longest_run = groups.value_counts().max() if len(groups) > 0 else 0
        else:
            longest_run = 0
        
        market_coverage_rows.append({
            'filename': fname,
            'commodity': commodity,
            'market_name': mkt,
            'obs_count': int(obs),
            'first_date': str(first.date()) if pd.notna(first) else 'N/A',
            'last_date': str(last.date()) if pd.notna(last) else 'N/A',
            'months_covered': n_months_covered,
            'longest_continuous_months': int(longest_run),
        })

market_coverage_df = pd.DataFrame(market_coverage_rows)
market_coverage_df.to_csv(OUTPUT_DIR / "market_coverage.csv", index=False)

# Summary by commodity
print("\n  Market Coverage Summary by Commodity:")
for fname, df in datasets.items():
    commodity = df['commodity_name_en'].iloc[0] if 'commodity_name_en' in df.columns and len(df) > 0 else 'UNKNOWN'
    sub = market_coverage_df[market_coverage_df['filename'] == fname]
    if len(sub) == 0:
        continue
    n_markets = len(sub)
    obs_1_2 = len(sub[sub['obs_count'] <= 2])
    obs_ge12 = len(sub[sub['obs_count'] >= 12])
    obs_ge24 = len(sub[sub['obs_count'] >= 24])
    obs_ge36 = len(sub[sub['obs_count'] >= 36])
    obs_ge60 = len(sub[sub['obs_count'] >= 60])
    max_run = sub['longest_continuous_months'].max()
    print(f"    {commodity}: {n_markets} mkts | <=2: {obs_1_2} | >=12: {obs_ge12} | "
          f">=24: {obs_ge24} | >=36: {obs_ge36} | >=60: {obs_ge60} | max_run: {max_run}")

print(f"\n  ✓ Saved market_coverage.csv")

# ── Yearly Coverage ────────────────────────────────────────────────────────
yearly_rows = []
for fname, df in datasets.items():
    commodity = df['commodity_name_en'].iloc[0] if 'commodity_name_en' in df.columns and len(df) > 0 else 'UNKNOWN'
    if 'price_year' in df.columns:
        yc = df.groupby('price_year').agg(
            obs_count=('price_year', 'size'),
            unique_markets=('market_name', 'nunique'),
        ).reset_index()
        for _, yr in yc.iterrows():
            yearly_rows.append({
                'filename': fname,
                'commodity': commodity,
                'year': int(yr['price_year']),
                'obs_count': int(yr['obs_count']),
                'unique_markets': int(yr['unique_markets']),
            })

yearly_df = pd.DataFrame(yearly_rows)
yearly_df.to_csv(OUTPUT_DIR / "yearly_coverage.csv", index=False)
print(f"  ✓ Saved yearly_coverage.csv")

# ── Monthly Coverage ───────────────────────────────────────────────────────
monthly_rows = []
for fname, df in datasets.items():
    commodity = df['commodity_name_en'].iloc[0] if 'commodity_name_en' in df.columns and len(df) > 0 else 'UNKNOWN'
    if 'price_year' in df.columns and 'price_month' in df.columns:
        mc = df.groupby(['price_year', 'price_month']).agg(
            obs_count=('price_month', 'size'),
            unique_markets=('market_name', 'nunique'),
        ).reset_index()
        for _, mr in mc.iterrows():
            monthly_rows.append({
                'filename': fname,
                'commodity': commodity,
                'year': int(mr['price_year']),
                'month': int(mr['price_month']),
                'obs_count': int(mr['obs_count']),
                'unique_markets': int(mr['unique_markets']),
            })

monthly_df = pd.DataFrame(monthly_rows)
monthly_df.to_csv(OUTPUT_DIR / "monthly_coverage.csv", index=False)
print(f"  ✓ Saved monthly_coverage.csv")


# ══════════════════════════════════════════════════════════════════════════
# D. RESEARCH SUITABILITY (Paper 1 commodities)
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("D. RESEARCH SUITABILITY")
print("─" * 60)

paper1_commodities = {
    'Onion (local)': 'DAM_ONION_LOCAL_2010_2026.csv',
    'Onion-imported': 'DAM_ONION_IMPORTED_2010_2026.csv',
    'Onion (New)': 'DAM_ONION_NEW_2010_2026.csv',
    'Potato (Local)': 'DAM_POTATO_LOCAL_2010_2026.csv',
    'Potato (Local) - Old': 'DAM_POTATO_LOCAL_OLD_2010_2026.csv',
    'Potato (Holland) - White (New)': 'DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv',
    'Potato (Holland) - White (Old)': 'DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv',
    'Potato (Holland) - Red': 'DAM_POTATO_HOLLAND_RED_2010_2026.csv',
    'Potato (Holland) - Red (Old)': 'DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv',
    'Potatoes-imported': 'DAM_POTATOES_IMPORTED_2010_2026.csv',
    'Sweet Potato': 'DAM_SWEET_POTATO_2010_2026.csv',
}

research_rows = []
for cname, fname in paper1_commodities.items():
    df = datasets[fname]
    sub = market_coverage_df[market_coverage_df['filename'] == fname]
    
    total_obs = len(df)
    total_markets = df['market_name'].nunique() if 'market_name' in df.columns else 0
    
    obs_ge6 = len(sub[sub['obs_count'] >= 6])
    obs_ge12 = len(sub[sub['obs_count'] >= 12])
    obs_ge24 = len(sub[sub['obs_count'] >= 24])
    
    max_run = sub['longest_continuous_months'].max() if len(sub) > 0 else 0
    median_obs = sub['obs_count'].median() if len(sub) > 0 else 0
    mean_obs = sub['obs_count'].mean() if len(sub) > 0 else 0
    
    # Time span
    first = df['price_date'].min()
    last = df['price_date'].max()
    span_months = 0
    if pd.notna(first) and pd.notna(last):
        span_months = (last.year - first.year) * 12 + (last.month - first.month)
    
    # Panel suitability score (simple heuristic)
    score = 0
    if total_obs >= 100: score += 2
    elif total_obs >= 50: score += 1
    if obs_ge12 >= 10: score += 2
    elif obs_ge12 >= 5: score += 1
    if max_run >= 12: score += 2
    elif max_run >= 6: score += 1
    if span_months >= 12: score += 1
    
    suitability = 'STRONG' if score >= 5 else ('MODERATE' if score >= 3 else 'WEAK')
    
    research_rows.append({
        'commodity': cname,
        'filename': fname,
        'total_obs': total_obs,
        'total_markets': total_markets,
        'markets_ge6_obs': obs_ge6,
        'markets_ge12_obs': obs_ge12,
        'markets_ge24_obs': obs_ge24,
        'median_obs_per_market': round(median_obs, 1),
        'mean_obs_per_market': round(mean_obs, 1),
        'longest_continuous_months': int(max_run),
        'time_span_months': span_months,
        'panel_suitability_score': score,
        'panel_suitability': suitability,
    })
    
    print(f"  {cname}: {total_obs} obs, {total_markets} mkts, "
          f"ge12={obs_ge12}, max_run={max_run}, → {suitability}")

# This goes into the sample recommendation CSV later


# ══════════════════════════════════════════════════════════════════════════
# E. MARKET-PAIR FEASIBILITY (Onion & Potato)
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("E. MARKET-PAIR FEASIBILITY")
print("─" * 60)

pair_results = []

# We check onion and potato files
pair_files = {
    'Onion (local)': 'DAM_ONION_LOCAL_2010_2026.csv',
    'Onion-imported': 'DAM_ONION_IMPORTED_2010_2026.csv',
    'Onion (New)': 'DAM_ONION_NEW_2010_2026.csv',
    'Potato (Holland) - White (New)': 'DAM_POTATO_HOLLAND_WHITE_NEW_2010_2026.csv',
    'Potato (Holland) - Red': 'DAM_POTATO_HOLLAND_RED_2010_2026.csv',
    'Potato (Local)': 'DAM_POTATO_LOCAL_2010_2026.csv',
    'Potato (Holland) - White (Old)': 'DAM_POTATO_HOLLAND_WHITE_OLD_2010_2026.csv',
    'Potato (Holland) - Red (Old)': 'DAM_POTATO_HOLLAND_RED_OLD_2010_2026.csv',
    'Potato (Local) - Old': 'DAM_POTATO_LOCAL_OLD_2010_2026.csv',
    'Potatoes-imported': 'DAM_POTATOES_IMPORTED_2010_2026.csv',
    'Sweet Potato': 'DAM_SWEET_POTATO_2010_2026.csv',
}

for cname, fname in pair_files.items():
    df = datasets[fname]
    
    if 'market_name' not in df.columns or 'price_date' not in df.columns:
        continue
    
    # Build dict of market -> set of year-months
    market_ym = {}
    for mkt, grp in df.groupby('market_name'):
        yms = set()
        for _, r in grp.iterrows():
            if pd.notna(r.get('price_year')) and pd.notna(r.get('price_month')):
                yms.add((int(r['price_year']), int(r['price_month'])))
        market_ym[mkt] = yms
    
    markets_list = list(market_ym.keys())
    n_markets = len(markets_list)
    
    # Count pairs with enough common observations
    pairs_ge12 = 0
    pairs_ge24 = 0
    pairs_ge36 = 0
    pairs_ge60 = 0
    total_pairs = 0
    pairs_any_overlap = 0
    
    for i in range(n_markets):
        for j in range(i + 1, n_markets):
            total_pairs += 1
            common = len(market_ym[markets_list[i]] & market_ym[markets_list[j]])
            if common > 0:
                pairs_any_overlap += 1
            if common >= 12:
                pairs_ge12 += 1
            if common >= 24:
                pairs_ge24 += 1
            if common >= 36:
                pairs_ge36 += 1
            if common >= 60:
                pairs_ge60 += 1
    
    pair_results.append({
        'commodity': cname,
        'filename': fname,
        'total_markets': n_markets,
        'total_possible_pairs': total_pairs,
        'pairs_with_overlap': pairs_any_overlap,
        'pairs_ge12_common_obs': pairs_ge12,
        'pairs_ge24_common_obs': pairs_ge24,
        'pairs_ge36_common_obs': pairs_ge36,
        'pairs_ge60_common_obs': pairs_ge60,
    })
    
    print(f"  {cname}: {n_markets} mkts, {total_pairs} pairs, "
          f"overlap={pairs_any_overlap}, ge12={pairs_ge12}, ge24={pairs_ge24}, ge36={pairs_ge36}, ge60={pairs_ge60}")

pair_df = pd.DataFrame(pair_results)
pair_df.to_csv(OUTPUT_DIR / "market_pair_feasibility.csv", index=False)
print(f"\n  ✓ Saved market_pair_feasibility.csv")


# ══════════════════════════════════════════════════════════════════════════
# F. DATA QUALITY CHECKS
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("F. DATA QUALITY CHECKS")
print("─" * 60)

quality_rows = []

price_cols_ws = ['wholesale_price_low', 'wholesale_price_high', 'wholesale_price_avg']
price_cols_rt = ['retail_price_low', 'retail_price_high', 'retail_price_avg']
all_price_cols = price_cols_ws + price_cols_rt

for fname, df in datasets.items():
    commodity = df['commodity_name_en'].iloc[0] if 'commodity_name_en' in df.columns and len(df) > 0 else 'UNKNOWN'
    
    # 1. Negative prices
    for pc in all_price_cols:
        if pc in df.columns:
            neg = (df[pc] < 0).sum()
            if neg > 0:
                quality_rows.append({
                    'filename': fname, 'commodity': commodity,
                    'issue_type': 'NEGATIVE_PRICE', 'column': pc,
                    'count': int(neg), 'detail': f'{neg} negative values'
                })
    
    # 2. Zero prices
    for pc in all_price_cols:
        if pc in df.columns:
            zeros = (df[pc] == 0).sum()
            if zeros > 0:
                quality_rows.append({
                    'filename': fname, 'commodity': commodity,
                    'issue_type': 'ZERO_PRICE', 'column': pc,
                    'count': int(zeros), 'detail': f'{zeros} zero values'
                })
    
    # 3. Wholesale low > wholesale high
    if 'wholesale_price_low' in df.columns and 'wholesale_price_high' in df.columns:
        ws_inverted = (df['wholesale_price_low'] > df['wholesale_price_high']).sum()
        if ws_inverted > 0:
            quality_rows.append({
                'filename': fname, 'commodity': commodity,
                'issue_type': 'WHOLESALE_LOW_GT_HIGH', 'column': 'wholesale_price_low/high',
                'count': int(ws_inverted), 'detail': f'{ws_inverted} rows where wholesale low > high'
            })
    
    # 4. Retail low > retail high
    if 'retail_price_low' in df.columns and 'retail_price_high' in df.columns:
        rt_inverted = (df['retail_price_low'] > df['retail_price_high']).sum()
        if rt_inverted > 0:
            quality_rows.append({
                'filename': fname, 'commodity': commodity,
                'issue_type': 'RETAIL_LOW_GT_HIGH', 'column': 'retail_price_low/high',
                'count': int(rt_inverted), 'detail': f'{rt_inverted} rows where retail low > high'
            })
    
    # 5. Average outside low-high range (wholesale)
    if all(c in df.columns for c in ['wholesale_price_low', 'wholesale_price_high', 'wholesale_price_avg']):
        ws_outside = ((df['wholesale_price_avg'] < df['wholesale_price_low']) |
                      (df['wholesale_price_avg'] > df['wholesale_price_high'])).sum()
        if ws_outside > 0:
            quality_rows.append({
                'filename': fname, 'commodity': commodity,
                'issue_type': 'WHOLESALE_AVG_OUTSIDE_RANGE', 'column': 'wholesale_price_avg',
                'count': int(ws_outside), 'detail': f'{ws_outside} rows where wholesale avg outside [low, high]'
            })
    
    # 5b. Average outside low-high range (retail)
    if all(c in df.columns for c in ['retail_price_low', 'retail_price_high', 'retail_price_avg']):
        rt_outside = ((df['retail_price_avg'] < df['retail_price_low']) |
                      (df['retail_price_avg'] > df['retail_price_high'])).sum()
        if rt_outside > 0:
            quality_rows.append({
                'filename': fname, 'commodity': commodity,
                'issue_type': 'RETAIL_AVG_OUTSIDE_RANGE', 'column': 'retail_price_avg',
                'count': int(rt_outside), 'detail': f'{rt_outside} rows where retail avg outside [low, high]'
            })
    
    # 6. Invalid dates (NaT after parsing)
    if 'price_date' in df.columns:
        invalid_dates = df['price_date'].isna().sum()
        if invalid_dates > 0:
            quality_rows.append({
                'filename': fname, 'commodity': commodity,
                'issue_type': 'INVALID_DATE', 'column': 'price_date',
                'count': int(invalid_dates), 'detail': f'{invalid_dates} unparseable dates'
            })
    
    # 7. Duplicate market-date
    if 'market_name' in df.columns and 'price_date' in df.columns:
        dup_md = df.duplicated(subset=['market_name', 'price_date']).sum()
        if dup_md > 0:
            quality_rows.append({
                'filename': fname, 'commodity': commodity,
                'issue_type': 'DUPLICATE_MARKET_DATE', 'column': 'market_name+price_date',
                'count': int(dup_md), 'detail': f'{dup_md} duplicate market-date combos'
            })
    
    # 8. Inconsistent commodity IDs
    if 'commodity_id' in df.columns and 'commodity_name_en' in df.columns:
        cid_combos = df[['commodity_id', 'commodity_name_en']].drop_duplicates()
        if len(cid_combos) > 1:
            quality_rows.append({
                'filename': fname, 'commodity': commodity,
                'issue_type': 'INCONSISTENT_COMMODITY_ID', 'column': 'commodity_id/name',
                'count': len(cid_combos),
                'detail': f'{len(cid_combos)} unique commodity_id-name combinations: {cid_combos.values.tolist()}'
            })
    
    # 9. Unit inconsistencies
    for ucol in ['wholesale_unit', 'retail_unit', 'wholesale_unit_id', 'retail_unit_id']:
        if ucol in df.columns:
            uvals = df[ucol].dropna().unique()
            if len(uvals) > 1:
                quality_rows.append({
                    'filename': fname, 'commodity': commodity,
                    'issue_type': 'UNIT_INCONSISTENCY', 'column': ucol,
                    'count': len(uvals),
                    'detail': f'{len(uvals)} unique values: {uvals.tolist()}'
                })
    
    # 10. Suspicious extreme outliers (IQR method on wholesale_price_avg)
    if 'wholesale_price_avg' in df.columns:
        vals = df['wholesale_price_avg'].dropna()
        if len(vals) > 10:
            q1 = vals.quantile(0.25)
            q3 = vals.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 3 * iqr
            upper = q3 + 3 * iqr
            outliers = ((vals < lower) | (vals > upper)).sum()
            if outliers > 0:
                quality_rows.append({
                    'filename': fname, 'commodity': commodity,
                    'issue_type': 'EXTREME_OUTLIER_WHOLESALE_AVG', 'column': 'wholesale_price_avg',
                    'count': int(outliers),
                    'detail': f'{outliers} values outside [Q1-3*IQR, Q3+3*IQR] = [{lower:.0f}, {upper:.0f}]'
                })
    
    # 10b. Outliers on retail_price_avg
    if 'retail_price_avg' in df.columns:
        vals = df['retail_price_avg'].dropna()
        if len(vals) > 10:
            q1 = vals.quantile(0.25)
            q3 = vals.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 3 * iqr
            upper = q3 + 3 * iqr
            outliers = ((vals < lower) | (vals > upper)).sum()
            if outliers > 0:
                quality_rows.append({
                    'filename': fname, 'commodity': commodity,
                    'issue_type': 'EXTREME_OUTLIER_RETAIL_AVG', 'column': 'retail_price_avg',
                    'count': int(outliers),
                    'detail': f'{outliers} values outside [Q1-3*IQR, Q3+3*IQR] = [{lower:.0f}, {upper:.0f}]'
                })

quality_df = pd.DataFrame(quality_rows)
quality_df.to_csv(OUTPUT_DIR / "data_quality_issues.csv", index=False)

# Print summary
issue_summary = quality_df.groupby('issue_type')['count'].sum().sort_values(ascending=False)
print("\n  Quality Issue Summary (across all files):")
for issue, cnt in issue_summary.items():
    print(f"    {issue}: {cnt}")
print(f"\n  ✓ Saved data_quality_issues.csv")


# ══════════════════════════════════════════════════════════════════════════
# G. PAPER 1 SAMPLE RECOMMENDATION
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("G. PAPER 1 SAMPLE RECOMMENDATION")
print("─" * 60)

research_df = pd.DataFrame(research_rows)

# Recommendation logic
rec_rows = []

# Rank commodities by suitability
strong = research_df[research_df['panel_suitability'] == 'STRONG'].sort_values('total_obs', ascending=False)
moderate = research_df[research_df['panel_suitability'] == 'MODERATE'].sort_values('total_obs', ascending=False)
weak = research_df[research_df['panel_suitability'] == 'WEAK'].sort_values('total_obs', ascending=False)

# Recommended thresholds
min_obs = 6
min_consecutive = 6

print(f"\n  STRONG series ({len(strong)}):")
for _, r in strong.iterrows():
    print(f"    → {r['commodity']}: {r['total_obs']} obs, {r['total_markets']} mkts, "
          f"ge12={r['markets_ge12_obs']}, max_run={r['longest_continuous_months']}")
    
    # Expected sample after filtering
    sub = market_coverage_df[market_coverage_df['filename'] == r['filename']]
    filtered = sub[(sub['obs_count'] >= min_obs) & (sub['longest_continuous_months'] >= min_consecutive)]
    
    rec_rows.append({
        'commodity': r['commodity'],
        'suitability': 'STRONG',
        'total_obs': r['total_obs'],
        'total_markets': r['total_markets'],
        'recommended_min_obs_per_market': min_obs,
        'recommended_min_consecutive_months': min_consecutive,
        'markets_after_filter': len(filtered),
        'expected_obs_after_filter': int(filtered['obs_count'].sum()) if len(filtered) > 0 else 0,
        'recommendation': 'INCLUDE in Paper 1 sample',
    })

print(f"\n  MODERATE series ({len(moderate)}):")
for _, r in moderate.iterrows():
    print(f"    → {r['commodity']}: {r['total_obs']} obs, {r['total_markets']} mkts, "
          f"ge12={r['markets_ge12_obs']}, max_run={r['longest_continuous_months']}")
    
    sub = market_coverage_df[market_coverage_df['filename'] == r['filename']]
    filtered = sub[(sub['obs_count'] >= min_obs) & (sub['longest_continuous_months'] >= min_consecutive)]
    
    rec_rows.append({
        'commodity': r['commodity'],
        'suitability': 'MODERATE',
        'total_obs': r['total_obs'],
        'total_markets': r['total_markets'],
        'recommended_min_obs_per_market': min_obs,
        'recommended_min_consecutive_months': min_consecutive,
        'markets_after_filter': len(filtered),
        'expected_obs_after_filter': int(filtered['obs_count'].sum()) if len(filtered) > 0 else 0,
        'recommendation': 'CONSIDER for Paper 1 (supplementary / robustness)',
    })

print(f"\n  WEAK series ({len(weak)}):")
for _, r in weak.iterrows():
    print(f"    → {r['commodity']}: {r['total_obs']} obs, {r['total_markets']} mkts, "
          f"ge12={r['markets_ge12_obs']}, max_run={r['longest_continuous_months']}")
    
    sub = market_coverage_df[market_coverage_df['filename'] == r['filename']]
    filtered = sub[(sub['obs_count'] >= min_obs) & (sub['longest_continuous_months'] >= min_consecutive)]
    
    rec_rows.append({
        'commodity': r['commodity'],
        'suitability': 'WEAK',
        'total_obs': r['total_obs'],
        'total_markets': r['total_markets'],
        'recommended_min_obs_per_market': min_obs,
        'recommended_min_consecutive_months': min_consecutive,
        'markets_after_filter': len(filtered),
        'expected_obs_after_filter': int(filtered['obs_count'].sum()) if len(filtered) > 0 else 0,
        'recommendation': 'EXCLUDE — insufficient data for panel analysis',
    })

rec_df = pd.DataFrame(rec_rows)
rec_df.to_csv(OUTPUT_DIR / "paper1_sample_recommendation.csv", index=False)
print(f"\n  ✓ Saved paper1_sample_recommendation.csv")


# ══════════════════════════════════════════════════════════════════════════
# FINAL AUDIT REPORT (Markdown)
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 60)
print("GENERATING FINAL AUDIT REPORT")
print("─" * 60)

total_all_obs = sum(len(df) for df in datasets.values())
all_markets = set()
for df in datasets.values():
    if 'market_name' in df.columns:
        all_markets.update(df['market_name'].unique())

# Build markdown report
report = []
report.append("# DAM Agricultural Price Data — FINAL AUDIT REPORT")
report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report.append(f"**Mode:** READ-ONLY AUDIT (no original files were modified)")
report.append(f"**Source:** `{MASTER_DIR}`")
report.append(f"**Output:** `{OUTPUT_DIR}`")
report.append("")
report.append("---")
report.append("")

# ── A. Dataset Inventory ──
report.append("## A. Dataset Inventory")
report.append("")
report.append(f"**Total files audited:** {len(datasets)}")
report.append(f"**Total observations (across all files):** {total_all_obs:,}")
report.append(f"**Total unique markets (across all files):** {len(all_markets)}")
report.append("")
report.append("| # | Filename | Commodity | Rows | Cols | Markets | Districts | First Date | Last Date | Years |")
report.append("|---|----------|-----------|------|------|---------|-----------|------------|-----------|-------|")
for i, row in inventory_df.iterrows():
    report.append(f"| {i+1} | `{row['filename']}` | {row['commodity']} | {row['num_rows']} | "
                  f"{row['num_columns']} | {row['unique_markets']} | {row['unique_districts']} | "
                  f"{row['first_date']} | {row['last_date']} | {row['num_unique_years']} |")
report.append("")

# Observations by commodity
report.append("### Observations by Commodity")
report.append("")
report.append("| Commodity | Total Obs |")
report.append("|-----------|-----------|")
for _, row in inventory_df.iterrows():
    report.append(f"| {row['commodity']} | {row['num_rows']:,} |")
report.append("")

# ── B. Missingness ──
report.append("## B. Missingness Summary")
report.append("")
summary_miss = missingness_df[missingness_df['column'] == '__SUMMARY__']
report.append("| Filename | Empty Cols | Empty Col Names | Dup Rows | Dup Market-Commodity-Date |")
report.append("|----------|-----------|-----------------|----------|--------------------------|")
for _, row in summary_miss.iterrows():
    ecols = row.get('completely_empty_columns', 0)
    enames = row.get('empty_column_names', 'N/A')
    drows = row.get('duplicate_rows', 0)
    dmcd = row.get('duplicate_market_commodity_date', 0)
    report.append(f"| `{row['filename']}` | {ecols} | {enames} | {drows} | {dmcd} |")
report.append("")

# High-missingness columns
report.append("### Columns with >5% Missing (any file)")
report.append("")
high_miss = missingness_df[(missingness_df['column'] != '__SUMMARY__') & (missingness_df['pct_missing'] > 5)]
if len(high_miss) > 0:
    report.append("| Filename | Column | Missing Count | % Missing |")
    report.append("|----------|--------|---------------|-----------|")
    for _, row in high_miss.iterrows():
        report.append(f"| `{row['filename']}` | {row['column']} | {row['missing_count']} | {row['pct_missing']}% |")
else:
    report.append("*No columns have >5% missing values (excluding summary rows).*")
report.append("")

# ── C. Coverage ──
report.append("## C. Coverage Analysis")
report.append("")
report.append("### Market Coverage Summary by Commodity")
report.append("")
report.append("| Commodity | Markets | ≤2 obs | ≥12 obs | ≥24 obs | ≥36 obs | ≥60 obs | Max Continuous |")
report.append("|-----------|---------|--------|---------|---------|---------|---------|----------------|")

for fname, df in datasets.items():
    commodity = df['commodity_name_en'].iloc[0] if 'commodity_name_en' in df.columns and len(df) > 0 else 'UNKNOWN'
    sub = market_coverage_df[market_coverage_df['filename'] == fname]
    if len(sub) == 0:
        continue
    n_markets = len(sub)
    obs_1_2 = len(sub[sub['obs_count'] <= 2])
    obs_ge12 = len(sub[sub['obs_count'] >= 12])
    obs_ge24 = len(sub[sub['obs_count'] >= 24])
    obs_ge36 = len(sub[sub['obs_count'] >= 36])
    obs_ge60 = len(sub[sub['obs_count'] >= 60])
    max_run = sub['longest_continuous_months'].max()
    report.append(f"| {commodity} | {n_markets} | {obs_1_2} | {obs_ge12} | {obs_ge24} | "
                  f"{obs_ge36} | {obs_ge60} | {max_run} |")
report.append("")

# ── D. Research Suitability ──
report.append("## D. Research Suitability (Paper 1)")
report.append("")
report.append("| Commodity | Obs | Markets | ≥6 obs | ≥12 obs | ≥24 obs | Max Run | Span (mo) | Score | Suitability |")
report.append("|-----------|-----|---------|--------|---------|---------|---------|-----------|-------|-------------|")
for _, row in research_df.iterrows():
    report.append(f"| {row['commodity']} | {row['total_obs']} | {row['total_markets']} | "
                  f"{row['markets_ge6_obs']} | {row['markets_ge12_obs']} | {row['markets_ge24_obs']} | "
                  f"{row['longest_continuous_months']} | {row['time_span_months']} | "
                  f"{row['panel_suitability_score']} | **{row['panel_suitability']}** |")
report.append("")

# Strongest series
onion_strong = research_df[research_df['commodity'].str.contains('Onion', case=False)].sort_values('panel_suitability_score', ascending=False)
potato_strong = research_df[research_df['commodity'].str.contains('Potato|Holland', case=False)].sort_values('panel_suitability_score', ascending=False)

report.append(f"**Strongest Onion series:** {onion_strong.iloc[0]['commodity']} "
              f"({onion_strong.iloc[0]['total_obs']} obs, score={onion_strong.iloc[0]['panel_suitability_score']})" if len(onion_strong) > 0 else "")
report.append(f"**Strongest Potato series:** {potato_strong.iloc[0]['commodity']} "
              f"({potato_strong.iloc[0]['total_obs']} obs, score={potato_strong.iloc[0]['panel_suitability_score']})" if len(potato_strong) > 0 else "")
report.append("")

# ── E. Market-Pair Feasibility ──
report.append("## E. Market-Pair Feasibility")
report.append("")
report.append("| Commodity | Markets | Possible Pairs | Overlapping | ≥12 common | ≥24 common | ≥36 common | ≥60 common |")
report.append("|-----------|---------|----------------|-------------|------------|------------|------------|------------|")
for _, row in pair_df.iterrows():
    report.append(f"| {row['commodity']} | {row['total_markets']} | {row['total_possible_pairs']} | "
                  f"{row['pairs_with_overlap']} | {row['pairs_ge12_common_obs']} | {row['pairs_ge24_common_obs']} | "
                  f"{row['pairs_ge36_common_obs']} | {row['pairs_ge60_common_obs']} |")
report.append("")

# ── F. Data Quality ──
report.append("## F. Data Quality Issues")
report.append("")
if len(quality_df) > 0:
    report.append("### Issue Summary (All Files)")
    report.append("")
    report.append("| Issue Type | Total Count |")
    report.append("|------------|-------------|")
    for issue, cnt in issue_summary.items():
        report.append(f"| {issue} | {cnt} |")
    report.append("")
    
    report.append("### Detailed Issues by File")
    report.append("")
    report.append("| Filename | Commodity | Issue | Column | Count | Detail |")
    report.append("|----------|-----------|-------|--------|-------|--------|")
    for _, row in quality_df.iterrows():
        report.append(f"| `{row['filename']}` | {row['commodity']} | {row['issue_type']} | "
                      f"{row['column']} | {row['count']} | {row['detail']} |")
else:
    report.append("*No data quality issues detected.*")
report.append("")

# ── G. Sample Recommendation ──
report.append("## G. Paper 1 Sample Recommendation")
report.append("")
report.append("### Selection Rule")
report.append("")
report.append(f"- **Minimum observations per market:** {min_obs}")
report.append(f"- **Minimum consecutive months:** {min_consecutive}")
report.append("")
report.append("### Commodity Recommendations")
report.append("")
report.append("| Commodity | Suitability | Total Obs | Markets | After Filter (mkts) | After Filter (obs) | Recommendation |")
report.append("|-----------|-------------|-----------|---------|--------------------|--------------------|----------------|")
for _, row in rec_df.iterrows():
    report.append(f"| {row['commodity']} | **{row['suitability']}** | {row['total_obs']} | "
                  f"{row['total_markets']} | {row['markets_after_filter']} | "
                  f"{row['expected_obs_after_filter']} | {row['recommendation']} |")
report.append("")

# ── H. Important note ──
report.append("## H. Important Notes")
report.append("")
report.append("> [!IMPORTANT]")
report.append("> This is a DATA-QUALITY and COVERAGE audit ONLY.")
report.append("> NO regression, causal analysis, weather merging, or hypothesis testing was performed.")
report.append("> All original files were treated as READ-ONLY and were NOT modified.")
report.append("")

# ── Concise Summary ──
report.append("---")
report.append("")
report.append("## Executive Summary")
report.append("")
report.append(f"- **Total observations across all 11 CSVs:** {total_all_obs:,}")
report.append(f"- **Total unique markets:** {len(all_markets)}")

report.append("")
report.append("### Observations by Commodity")
report.append("")
for _, row in inventory_df.sort_values('num_rows', ascending=False).iterrows():
    report.append(f"- {row['commodity']}: {row['num_rows']:,} observations")

report.append("")
if len(onion_strong) > 0:
    report.append(f"**Strongest Onion series:** {onion_strong.iloc[0]['commodity']} "
                  f"({onion_strong.iloc[0]['total_obs']:,} obs, {onion_strong.iloc[0]['total_markets']} markets)")
if len(potato_strong) > 0:
    report.append(f"**Strongest Potato series:** {potato_strong.iloc[0]['commodity']} "
                  f"({potato_strong.iloc[0]['total_obs']:,} obs, {potato_strong.iloc[0]['total_markets']} markets)")

report.append("")
report.append("### Biggest Data Quality Problems")
report.append("")
if len(issue_summary) > 0:
    for issue, cnt in issue_summary.head(5).items():
        report.append(f"1. **{issue}**: {cnt} instances")
else:
    report.append("*No major quality issues detected.*")

report.append("")
report.append("### Recommended Next Steps")
report.append("")
report.append("1. **Clean adjusted-price anomalies** — investigate wholesale avg outside [low, high] range cases")
report.append("2. **Handle extreme outliers** — review and decide on winsorizing vs. dropping")
report.append("3. **Construct balanced panel** — apply the minimum obs + consecutive-month filter")
report.append("4. **Merge weather data** — only after panel construction is finalized")
report.append("5. **Begin descriptive statistics** — price distributions, seasonal patterns, market-level summaries")
report.append("")

# Write the report
report_text = "\n".join(report)
with open(OUTPUT_DIR / "FINAL_AUDIT_REPORT.md", "w", encoding="utf-8") as f:
    f.write(report_text)
print(f"  ✓ Saved FINAL_AUDIT_REPORT.md")

# ── Final console summary ─────────────────────────────────────────────────
print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)
print(f"  Total observations:      {total_all_obs:,}")
print(f"  Total unique markets:    {len(all_markets)}")
print(f"  Files generated:         9 (in {OUTPUT_DIR})")
print()
print("  Generated files:")
for f in sorted(OUTPUT_DIR.iterdir()):
    if f.name != 'run_audit.py':
        print(f"    ✓ {f.name}")
print()
print("  ALL ORIGINAL FILES WERE READ-ONLY. NO MODIFICATIONS MADE.")
print("=" * 80)
