"""Step 3 - Build the cleaned market x commodity x month price panel.

Sources
-------
* Historical DAM web portal, 2000-01 .. 2023-07 (monthly observations, one row per
  market x commodity x price_type x month) from the expanded master.
* MOA REST API, 2025-06 .. 2026-08: the FULL_FLAGGED tier file of the Steps 4-11 audit
  (identical rows to the API part of the expanded master, plus the audited quality flags).

Cleaning (historical segment; the API segment re-uses the audited ELIGIBLE_* flags)
-----------------------------------------------------------------------------------
Row-level flags, nothing is imputed or interpolated:
  flag_unidentified_market  market or district name missing and not recoverable
  flag_duplicate_conflict   duplicated (market, commodity, price_type, month) key with different prices
  flag_zero                 low <= 0 or high <= 0
  flag_inverted             low > high
  flag_range_ratio          high/low > RANGE_RATIO_MAX (unit mix-up inside a quote pair)
  flag_abs_bounds           midpoint outside ABS_KG_BOUNDS (BDT/kg)
  flag_outlier_xs           log midpoint deviates from the commodity x month cross-market median by more
                            than XS_IQR_MULT x IQR (cells with >= XS_MIN_CELL markets)   [PRIMARY rule]
  flag_outlier_level_iqr    midpoint outside Q1-3IQR / Q3+3IQR of the pooled 2000-2026 commodity
                            distribution (the literal rule of the brief; diagnostic + robustness only,
                            because it deletes the genuine 2019-20 onion price crisis)
Tiers
  PRIMARY_ANALYSIS   = no flag above except flag_outlier_level_iqr
  STRICT_SENSITIVITY = PRIMARY and inside a run of >= STRICT_MIN_RUN consecutive months
"""
import unicodedata
import numpy as np
import pandas as pd
from config import *

KEY = ["market_key", "commodity_id", "ym"]


def _n(s):
    return unicodedata.normalize("NFKC", str(s).strip())


def load_historical(log):
    d = pd.read_csv(EXPANDED_MASTER, low_memory=False, encoding="utf-8-sig")
    log.append(f"Expanded master rows: {len(d):,}")
    d = d[d.commodity_id.isin(COMMODITIES)]
    log.append(f"  Paper 1 commodities (11 ids): {len(d):,}")
    h = d[d.source_system == "market_dam_web_historical"].copy()
    log.append(f"  historical web-portal rows: {len(h):,}; API rows in master: {len(d) - len(h):,}")
    h = h[h.price_type.isin(["wholesale", "retail"])].copy()
    log.append(f"  historical wholesale+retail rows (grower rows not used): {len(h):,}")
    h["ym"] = h.price_date.str[:7]

    # geography: recover a missing district from the market name where the market maps to one district
    h["market_bn"] = h.market_name_bn.where(h.market_name_bn.notna()).map(lambda x: _n(x) if isinstance(x, str) else np.nan)
    h["district_bn"] = h.district_name_bn.map(lambda x: _n(x) if isinstance(x, str) else np.nan)
    m2d = h.dropna(subset=["market_bn", "district_bn"]).groupby("market_bn").district_bn.agg(lambda s: s.unique())
    m2d = m2d[m2d.map(len) == 1].map(lambda a: a[0])
    miss = h.district_bn.isna() & h.market_bn.notna()
    h.loc[miss, "district_bn"] = h.loc[miss, "market_bn"].map(m2d)
    log.append(f"  rows with missing district: {int(miss.sum()):,}; recovered from unique market->district map: "
               f"{int((miss & h.district_bn.notna()).sum()):,}")
    xw = pd.read_csv(RAW / "crosswalks" / "historical_district_bn_to_gadm.csv")
    xw["district_bn"] = xw.district_name_bn.map(_n)
    h = h.merge(xw[["district_bn", "gadm_name_2"]], on="district_bn", how="left")
    h["flag_unidentified_market"] = h.market_bn.isna() | h.gadm_name_2.isna()
    h["market_key"] = "H|" + h.gadm_name_2.fillna("?") + "|" + h.market_bn.fillna("?")
    h["market_name"] = h.market_bn
    h["low"], h["high"], h["avg"] = h.standardized_price_low, h.standardized_price_high, h.standardized_price_avg

    # duplicates on the natural key
    k = ["market_key", "commodity_id", "price_type", "ym"]
    exact = h.duplicated(k + ["low", "high", "avg"], keep="first") & ~h.flag_unidentified_market
    log.append(f"  exact duplicate rows dropped (identified markets): {int(exact.sum()):,}")
    h = h[~exact].copy()
    h["flag_duplicate_conflict"] = h.duplicated(k, keep=False) & ~h.flag_unidentified_market
    return h[["market_key", "market_name", "gadm_name_2", "commodity_id", "price_type", "ym", "low", "high", "avg",
              "flag_unidentified_market", "flag_duplicate_conflict"]]


def flag_rows(h, log):
    """Row-level flags for the historical long table (one row per price_type)."""
    scale = np.where(h.price_type == "wholesale", 100.0, 1.0)      # Quintal -> kg for wholesale
    h["mid_kg"] = (h.low + h.high) / 2 / scale
    h["avg_kg"] = h.avg / scale
    h["flag_zero"] = (h.low <= 0) | (h.high <= 0) | h.low.isna() | h.high.isna()
    h["flag_inverted"] = h.low > h.high
    h["flag_range_ratio"] = (h.high / h.low.where(h.low > 0)) > RANGE_RATIO_MAX
    h["flag_abs_bounds"] = ~h.mid_kg.between(*ABS_KG_BOUNDS)
    basic = ["flag_unidentified_market", "flag_duplicate_conflict", "flag_zero", "flag_inverted",
             "flag_range_ratio", "flag_abs_bounds"]
    ok = ~h[basic].any(axis=1)
    # cross-sectional rule, computed on rows that pass the basic checks
    h["lp"] = np.log(h.mid_kg.where(h.mid_kg > 0))
    g = h[ok].groupby(["price_type", "commodity_id", "ym"]).lp
    med, n = g.transform("median"), g.transform("size")
    dev = (h.loc[ok, "lp"] - med).where(n >= XS_MIN_CELL)
    h["xs_dev"] = dev
    h["flag_outlier_xs"] = False
    h["flag_outlier_level_iqr"] = False
    for pt, sub in h[ok].groupby("price_type"):
        q1, q3 = sub.xs_dev.quantile([.25, .75])
        lo, hi = q1 - XS_IQR_MULT * (q3 - q1), q3 + XS_IQR_MULT * (q3 - q1)
        log.append(f"  cross-sectional outlier bounds ({pt}): log deviation outside [{lo:.3f}, {hi:.3f}]")
        h.loc[sub.index, "flag_outlier_xs"] = (sub.xs_dev < lo) | (sub.xs_dev > hi)
        for c, s2 in sub.groupby("commodity_id"):
            a, b = s2.mid_kg.quantile([.25, .75])
            h.loc[s2.index, "flag_outlier_level_iqr"] = (s2.mid_kg > b + 3 * (b - a)) | (s2.mid_kg < a - 3 * (b - a))
    h["basic_ok"] = ok
    h["primary"] = ok & ~h.flag_outlier_xs
    return h, basic + ["flag_outlier_xs"]


def run_flag(panel):
    """Rows inside a run of >= STRICT_MIN_RUN consecutive months (per market x commodity)."""
    p = panel.sort_values(KEY).copy()
    t = pd.PeriodIndex(p.ym, freq="M")
    idx = t.year * 12 + t.month
    brk = (idx.to_series(index=p.index).groupby([p.market_key, p.commodity_id]).diff() != 1)
    run = brk.groupby([p.market_key, p.commodity_id]).cumsum()
    size = p.groupby([p.market_key, p.commodity_id, run]).ym.transform("size")
    return (size >= STRICT_MIN_RUN).reindex(panel.index)


def main():
    log = ["# Step 3 - price panel construction log", ""]
    h = load_historical(log)
    h, flags = flag_rows(h, log)
    acct = h.groupby("price_type")[flags + ["flag_outlier_level_iqr", "primary"]].sum().T
    acct.loc["rows"] = h.groupby("price_type").size()
    acct.to_csv(INTER / "cleaning_flag_counts_historical.csv")
    log += ["", "Historical row-level flag counts (rows can carry several flags):", "```", acct.to_string(), "```"]
    lv = h[(h.price_type == "wholesale") & h.flag_outlier_level_iqr & h.primary]
    log.append(f"Literal pooled-IQR rule would delete {len(lv):,} otherwise valid wholesale rows; "
               f"{(lv.ym.str[:4].isin(['2019', '2020'])).mean():.0%} of them fall in 2019-2020 (onion price crisis). "
               "It is therefore kept as a diagnostic flag and used only in a robustness check.")
    h.to_csv(INTER / "price_rows_historical_flagged.csv", index=False)

    # ---- historical: long -> wide (one row per market x commodity x month) ------------------
    def wide(sub, pre):
        s = sub[["market_key", "market_name", "gadm_name_2", "commodity_id", "ym", "low", "high", "mid_kg", "avg_kg",
                 "primary", "basic_ok", "flag_outlier_level_iqr"]].copy()
        return s.rename(columns={"low": f"{pre}_low", "high": f"{pre}_high", "mid_kg": f"price_{pre}_raw_mid_kg",
                                 "avg_kg": f"price_{pre}_dam_avg_kg", "primary": f"{pre}_primary", "basic_ok": f"{pre}_basic_ok",
                                 "flag_outlier_level_iqr": f"{pre}_flag_level_iqr"})
    # rows with conflicting duplicate keys / unidentified markets cannot be placed in the panel
    placeable = ~(h.flag_unidentified_market | h.flag_duplicate_conflict)
    log.append(f"Historical rows not placeable in the panel (unidentified market or conflicting duplicate key): "
               f"{int((~placeable).sum()):,}")
    hw = wide(h[placeable & (h.price_type == "wholesale")], "wholesale")
    hr = wide(h[placeable & (h.price_type == "retail")], "retail").drop(columns=["market_name", "gadm_name_2"])
    hist = hw.merge(hr, on=KEY, how="left")
    hist["source"] = "dam_web_historical"

    # ---- API segment (audited tiers) ---------------------------------------------------------
    a = pd.read_csv(API_FULL_FLAGGED, low_memory=False)
    log += ["", f"API FULL_FLAGGED rows: {len(a):,}; ELIGIBLE_PRIMARY_ANALYSIS: {int(a.ELIGIBLE_PRIMARY_ANALYSIS.sum()):,}; "
            f"ELIGIBLE_STRICT_SENSITIVITY: {int(a.ELIGIBLE_STRICT_SENSITIVITY.sum()):,}"]
    xa = pd.read_csv(RAW / "crosswalks" / "api_district_id_to_gadm.csv")
    a = a.merge(xa[["api_district_id", "gadm_name_2"]], left_on="district_id", right_on="api_district_id", how="left")
    assert a.gadm_name_2.notna().all(), "unmapped API district id"
    a["ym"] = a.price_date.str[:7]
    assert not a.duplicated(["market_id", "commodity_id", "ym"]).any()
    api = pd.DataFrame({
        "market_key": "A|" + a.market_id.astype(str), "market_name": a.market_name, "gadm_name_2": a.gadm_name_2,
        "commodity_id": a.commodity_id, "ym": a.ym,
        "wholesale_low": a.wholesale_price_low, "wholesale_high": a.wholesale_price_high,
        "price_wholesale_raw_mid_kg": a.price_wholesale_raw_mid_kg, "price_wholesale_dam_avg_kg": a.price_wholesale_dam_avg_kg,
        "wholesale_primary": a.ELIGIBLE_PRIMARY_ANALYSIS.astype(bool),
        "wholesale_basic_ok": (a.wholesale_price_low > 0) & (a.wholesale_price_high > 0) & (a.wholesale_price_low <= a.wholesale_price_high),
        "wholesale_flag_level_iqr": False,
        "retail_low": a.retail_price_low, "retail_high": a.retail_price_high,
        "price_retail_raw_mid_kg": a.price_retail_raw_mid_kg, "price_retail_dam_avg_kg": a.price_retail_dam_avg_kg,
        "retail_primary": a.ELIGIBLE_PRIMARY_ANALYSIS.astype(bool) & (a.retail_price_low > 0) & (a.retail_price_high > 0),
        "retail_basic_ok": (a.retail_price_low > 0) & (a.retail_price_high > 0) & (a.retail_price_low <= a.retail_price_high),
        "retail_flag_level_iqr": False, "source": "moa_api",
        "api_strict": a.ELIGIBLE_STRICT_SENSITIVITY.astype(bool)})

    full = pd.concat([hist, api], ignore_index=True)
    for c in ("retail_primary", "retail_basic_ok", "wholesale_basic_ok"):
        full[c] = full[c].fillna(False).astype(bool)
    full["tier_primary"] = full.wholesale_primary.astype(bool)
    prim = full[full.tier_primary].copy()
    strict = run_flag(prim)
    full["tier_strict"] = False
    full.loc[prim.index, "tier_strict"] = strict.values
    # API segment: keep the audited STRICT flag
    is_api = full.source == "moa_api"
    full.loc[is_api, "tier_strict"] = full.loc[is_api, "api_strict"].astype(bool)
    full = full.drop(columns="api_strict")

    full["commodity_name"] = full.commodity_id.map(lambda c: COMMODITIES[c][0])
    full["crop"] = full.commodity_id.map(lambda c: COMMODITIES[c][1])
    full["imported"] = full.commodity_id.map(lambda c: COMMODITIES[c][2])
    full["year"] = full.ym.str[:4].astype(int)
    full["month"] = full.ym.str[5:7].astype(int)
    full = full.sort_values(KEY).reset_index(drop=True)
    full.to_csv(INTER / "price_panel_all_tiers.csv", index=False)

    t = full.groupby("source").agg(rows=("ym", "size"), primary=("tier_primary", "sum"), strict=("tier_strict", "sum"),
                                   markets=("market_key", "nunique"), districts=("gadm_name_2", "nunique"),
                                   first=("ym", "min"), last=("ym", "max"))
    t.loc["TOTAL"] = [len(full), full.tier_primary.sum(), full.tier_strict.sum(), full.market_key.nunique(),
                      full.gadm_name_2.nunique(), full.ym.min(), full.ym.max()]
    t.to_csv(INTER / "price_panel_tier_accounting.csv")
    log += ["", "Panel accounting (market x commodity x month wholesale observations):", "```", t.to_string(), "```"]

    # coverage by month -> documents the institutional gaps
    cov = full[full.tier_primary].groupby("ym").size().reindex(
        pd.period_range("2000-01", "2026-08", freq="M").astype(str), fill_value=0)
    cov.rename("primary_obs").to_csv(INTER / "price_coverage_by_month.csv", index_label="ym")
    gaps = cov[cov == 0].index.tolist()
    log += ["", f"Calendar months with zero PRIMARY wholesale observations ({len(gaps)}): " + ", ".join(gaps),
            f"Observations dated 2024: {int((full.year == 2024).sum())} (institutional gap confirmed; nothing interpolated)."]
    (INTER / "s03_price_panel_log.md").write_text("\n".join(log), encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
