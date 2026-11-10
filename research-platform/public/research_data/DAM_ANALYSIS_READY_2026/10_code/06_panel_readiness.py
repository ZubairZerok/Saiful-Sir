#!/usr/bin/env python3
"""
Phase 10: Market-Panel Readiness and Spatial Pairwise Overlap Analysis
=====================================================================
Calculates econometric panel feasibility metrics for Onion and Potato varieties,
computes full market-pair co-observation matrices for spatial dispersion models,
and identifies sample candidate pools for Papers 1, 2, and 3.

Outputs:
- 08_panel_readiness/onion_panel_readiness.csv
- 08_panel_readiness/potato_panel_readiness.csv
- 08_panel_readiness/market_pair_overlap.csv
- 08_panel_readiness/paper1_sample_candidates.csv
- 08_panel_readiness/paper2_sample_candidates.csv
- 08_panel_readiness/paper3_sample_candidates.csv
"""

from __future__ import annotations

import os
import sys
import itertools
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TARGET_DIR = PROJECT_ROOT / "DAM_ANALYSIS_READY_2026" / "08_panel_readiness"
PRIMARY_CSV = PROJECT_ROOT / "DAM_ANALYSIS_READY_2026" / "07_outputs" / "PRIMARY_ANALYSIS" / "DAM_ALL_11_PRIMARY_ANALYSIS.csv"


def run_panel_readiness() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    print("Executing Phase 10: Market-Panel Readiness Analysis...")

    df = pd.read_csv(PRIMARY_CSV)
    df['dt'] = pd.to_datetime(df['price_date'])
    df['year_month'] = df['dt'].dt.to_period('M')

    # 1. Market panel metrics by commodity
    def compute_commodity_panel_metrics(comm_df: pd.DataFrame) -> list[dict]:
        records = []
        for cid, group in comm_df.groupby('commodity_id'):
            cname = group['commodity_name_en'].iloc[0]
            n_obs = len(group)
            mkt_counts = group.groupby('market_id').size()
            n_mkts = len(mkt_counts)

            ge_6 = int((mkt_counts >= 6).sum())
            ge_12 = int((mkt_counts >= 12).sum())
            ge_18 = int((mkt_counts >= 18).sum())
            ge_24 = int((mkt_counts >= 24).sum())
            ge_36 = int((mkt_counts >= 36).sum())
            ge_60 = int((mkt_counts >= 60).sum())

            records.append({
                "commodity_id": cid,
                "commodity_name": cname,
                "total_observations": n_obs,
                "total_markets": n_mkts,
                "mean_obs_per_market": round(mkt_counts.mean(), 2),
                "median_obs_per_market": round(mkt_counts.median(), 2),
                "min_obs_per_market": int(mkt_counts.min()),
                "max_obs_per_market": int(mkt_counts.max()),
                "markets_ge_6_obs": ge_6,
                "markets_ge_12_obs": ge_12,
                "markets_ge_18_obs": ge_18,
                "markets_ge_24_obs": ge_24,
                "markets_ge_36_obs": ge_36,
                "markets_ge_60_obs": ge_60,
                "suitability_assessment": "STRONG_PANEL" if ge_12 >= 10 else ("MODERATE_PANEL" if ge_6 >= 5 else "WEAK_PANEL")
            })
        return records

    onion_df = df[df['commodity_family'] == 'ONION']
    potato_df = df[df['commodity_family'] == 'POTATO']

    pd.DataFrame(compute_commodity_panel_metrics(onion_df)).to_csv(TARGET_DIR / "onion_panel_readiness.csv", index=False)
    pd.DataFrame(compute_commodity_panel_metrics(potato_df)).to_csv(TARGET_DIR / "potato_panel_readiness.csv", index=False)

    # 2. Market-Pair Pairwise Overlap Matrix for Paper 2 & Paper 3
    pair_records = []
    for cid, group in df.groupby('commodity_id'):
        cname = group['commodity_name_en'].iloc[0]
        cfam = group['commodity_family'].iloc[0]

        # Group dates by market
        market_dates = group.groupby('market_id')['year_month'].unique().to_dict()
        market_names = group.groupby('market_id')['market_name'].first().to_dict()
        market_divs = group.groupby('market_id')['division_name'].first().to_dict()
        all_markets = sorted(list(market_dates.keys()))

        n_possible_pairs = len(all_markets) * (len(all_markets) - 1) // 2
        overlap_ge_6 = 0
        overlap_ge_12 = 0
        overlap_ge_18 = 0
        overlap_ge_24 = 0
        overlap_ge_36 = 0
        overlap_ge_60 = 0

        for m1, m2 in itertools.combinations(all_markets, 2):
            dates1 = set(market_dates[m1])
            dates2 = set(market_dates[m2])
            common = dates1.intersection(dates2)
            n_common = len(common)

            if n_common >= 6: overlap_ge_6 += 1
            if n_common >= 12: overlap_ge_12 += 1
            if n_common >= 18: overlap_ge_18 += 1
            if n_common >= 24: overlap_ge_24 += 1
            if n_common >= 36: overlap_ge_36 += 1
            if n_common >= 60: overlap_ge_60 += 1

            if n_common >= 6:
                pair_records.append({
                    "commodity_id": cid,
                    "commodity_name": cname,
                    "commodity_family": cfam,
                    "market_id_1": m1,
                    "market_name_1": market_names[m1],
                    "division_1": market_divs[m1],
                    "market_id_2": m2,
                    "market_name_2": market_names[m2],
                    "division_2": market_divs[m2],
                    "is_inter_division": (market_divs[m1] != market_divs[m2]),
                    "common_months_count": n_common
                })

    df_pairs = pd.DataFrame(pair_records)
    df_pairs.to_csv(TARGET_DIR / "market_pair_overlap.csv", index=False)

    # 3. Paper-Specific Candidate Sample Tables
    # Paper 1: Markets with >=6 continuous monthly observations for weather response
    paper1_candidates = []
    for cid, group in df.groupby('commodity_id'):
        cname = group['commodity_name_en'].iloc[0]
        cfam = group['commodity_family'].iloc[0]
        for mid, mgroup in group.groupby('market_id'):
            if len(mgroup) >= 6:
                paper1_candidates.append({
                    "commodity_id": cid,
                    "commodity_name": cname,
                    "commodity_family": cfam,
                    "market_id": mid,
                    "market_name": mgroup['market_name'].iloc[0],
                    "division_name": mgroup['division_name'].iloc[0],
                    "observation_count": len(mgroup),
                    "first_date": str(mgroup['dt'].min().date()),
                    "last_date": str(mgroup['dt'].max().date()),
                    "paper1_suitability": "HIGH_CONFIDENCE_SAMPLE" if len(mgroup) >= 12 else "ACCEPTABLE_SAMPLE"
                })
    pd.DataFrame(paper1_candidates).to_csv(TARGET_DIR / "paper1_sample_candidates.csv", index=False)

    # Paper 2: Market pairs with >=10 common observation periods for spatial dispersion
    paper2_candidates = df_pairs[df_pairs['common_months_count'] >= 10].copy()
    paper2_candidates.to_csv(TARGET_DIR / "paper2_sample_candidates.csv", index=False)

    # Paper 3: Markets with both wholesale and retail quotes and >=6 periods for efficiency/spreads
    paper3_candidates = []
    for cid, group in df.groupby('commodity_id'):
        cname = group['commodity_name_en'].iloc[0]
        cfam = group['commodity_family'].iloc[0]
        for mid, mgroup in group.groupby('market_id'):
            valid_spreads = mgroup['wholesale_retail_spread_kg'].dropna()
            if len(valid_spreads) >= 6:
                paper3_candidates.append({
                    "commodity_id": cid,
                    "commodity_name": cname,
                    "commodity_family": cfam,
                    "market_id": mid,
                    "market_name": mgroup['market_name'].iloc[0],
                    "division_name": mgroup['division_name'].iloc[0],
                    "valid_spread_observations": len(valid_spreads),
                    "mean_spread_bdt_kg": round(valid_spreads.mean(), 2),
                    "paper3_suitability": "HIGH_CONFIDENCE_MARGIN_SAMPLE"
                })
    pd.DataFrame(paper3_candidates).to_csv(TARGET_DIR / "paper3_sample_candidates.csv", index=False)

    print(f"Phase 10 complete. Saved panel readiness reports and pairwise overlap tables to {TARGET_DIR}")


if __name__ == "__main__":
    run_panel_readiness()
