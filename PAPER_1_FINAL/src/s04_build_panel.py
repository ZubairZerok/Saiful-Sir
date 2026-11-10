"""Step 4 - Pre-harvest exposure (crop-calendar aligned) and the final analysis panel.

Exposure design
---------------
For crop c and district d, season y is the pre-harvest window that ENDS in calendar year y
(onion: Oct(y-1)..Mar(y); potato: Oct(y-1)..Feb(y)). Monthly shock indicators are summed over
the window (Option A, count of shocked months) and the window maximum of |z| is kept (Option B).
A price observed in month t is assigned the season of its marketing year:
    onion : t in Apr(y)..Mar(y+1)  -> season y        potato: t in Mar(y)..Feb(y+1) -> season y
so the exposure of an observation is built ONLY from weather that precedes it (no forward-looking
information enters the treatment).  `*_lead` variables carry season y+1 (strictly future window)
and are used for the placebo-lead test; `*_off` variables count shocks in the six months before
planting (Apr..Sep of y-1, crop not in the ground) for the wrong-window placebo.
"""
import numpy as np
import pandas as pd
from config import *

SHOCKS = {  # exposure name -> monthly indicator column
    "ph_any": "any_shock_15", "ph_excess_rain": "excess_rain_15", "ph_drought": "drought_15",
    "ph_heatwave": "heatwave_15", "ph_cold": "cold_15",
    "ph_any_10": "any_shock_10", "ph_any_20": "any_shock_20",
    "ph_excess_rain_10": "excess_rain_10", "ph_drought_10": "drought_10", "ph_heatwave_10": "heatwave_10", "ph_cold_10": "cold_10",
    "ph_excess_rain_20": "excess_rain_20", "ph_drought_20": "drought_20", "ph_heatwave_20": "heatwave_20", "ph_cold_20": "cold_20",
    "ph_any_chirps": "any_shock_chirps", "ph_excess_rain_chirps": "excess_rain_chirps", "ph_drought_chirps": "drought_chirps",
    "ph_any_spei": "any_shock_spei", "ph_wet_spei": "wet_spei", "ph_dry_spei": "dry_spei",
    "ph_any_pct": "any_shock_pct",
}
OFF_WINDOW = [4, 5, 6, 7, 8, 9]


def season_exposure(w):
    rows = []
    w = w.copy()
    for crop, months in PH_WINDOW.items():
        s = w[w.month.isin(months)].copy()
        s["season"] = np.where(s.month >= 10, s.year + 1, s.year)       # window ends in `season`
        full = s.groupby(["gadm_name_2", "season"]).ym.transform("size") == len(months)
        s = s[full]
        agg = {k: (v, lambda x: x.sum(min_count=len(x))) for k, v in SHOCKS.items()}
        e = s.groupby(["gadm_name_2", "season"]).agg(
            **agg,
            ph_max_abs_z_precip=("z_precip", lambda x: x.abs().max()),
            ph_max_abs_z_temp=("z_temp", lambda x: x.abs().max()),
            ph_mean_z_precip=("z_precip", "mean"), ph_mean_z_temp=("z_temp", "mean"),
            ph_precip_mm=("precip_mm", "sum"), ph_tmean_c=("tmean_c", "mean"),
            ph_min_spei3=("spei3", "min")).reset_index()
        off = w[w.month.isin(OFF_WINDOW)].copy()
        off["season"] = off.year + 1                                     # Apr..Sep(y-1) -> season y
        o = off.groupby(["gadm_name_2", "season"]).any_shock_15.agg(["sum", "size"]).reset_index()
        o = o[o["size"] == len(OFF_WINDOW)].rename(columns={"sum": "ph_any_off"})[["gadm_name_2", "season", "ph_any_off"]]
        e = e.merge(o, on=["gadm_name_2", "season"], how="left")
        e["crop"] = crop
        rows.append(e)
    e = pd.concat(rows, ignore_index=True)
    for c in e.columns:
        if c.startswith("ph_") and c in SHOCKS:
            e[c] = e[c].astype(float)
    # lead (season y+1) of the headline and type-specific exposures; lag (season y-1) of the headline exposure
    k = ["gadm_name_2", "crop", "season"]
    types = ["ph_any", "ph_excess_rain", "ph_drought", "ph_heatwave", "ph_cold"]
    lead = e[k + types].assign(season=e.season - 1).rename(columns={t: t + "_lead" for t in types})
    lag = e[k + ["ph_any"]].assign(season=e.season + 1).rename(columns={"ph_any": "ph_any_lag"})
    return e.merge(lead, on=k, how="left").merge(lag, on=k, how="left")


def main():
    w = pd.read_csv(INTER / "weather_district_monthly_anomalies.csv")
    geo = pd.read_csv(INTER / "district_geography.csv")
    p = pd.read_csv(INTER / "price_panel_all_tiers.csv")

    exp = season_exposure(w)
    exp.round(5).to_csv(INTER / "preharvest_exposure_district_crop_season.csv", index=False)

    start = p.crop.map(MKT_YEAR_START)
    p["season"] = np.where(p.month >= start, p.year, p.year - 1)        # marketing year -> harvest year
    n0 = len(p)
    p = p.merge(exp, on=["gadm_name_2", "crop", "season"], how="left", validate="m:1")
    p = p.merge(geo[["gadm_name_2", "district_id", "division", "centroid_lat", "centroid_lon", "distance_to_dhaka_km"]],
                on="gadm_name_2", how="left", validate="m:1")
    # contemporaneous district weather (descriptives; not a regressor in the baseline)
    cw = w[["gadm_name_2", "ym", "precip_mm", "tmean_c", "tmin_c", "tmax_c", "z_precip", "z_temp", "spei3"]]
    p = p.merge(cw, on=["gadm_name_2", "ym"], how="left", validate="m:1")
    assert len(p) == n0

    p["ln_price"] = np.log(p.price_wholesale_raw_mid_kg.where(p.price_wholesale_raw_mid_kg > 0))
    p["ln_price_dam_avg"] = np.log(p.price_wholesale_dam_avg_kg.where(p.price_wholesale_dam_avg_kg > 0))
    p["ln_retail"] = np.log(p.price_retail_raw_mid_kg.where((p.price_retail_raw_mid_kg > 0) & p.retail_primary))
    p["ln_dist_dhaka"] = np.log(p.distance_to_dhaka_km)
    t = pd.PeriodIndex(p.ym, freq="M")
    p["t_index"] = (t.year - 2000) * 12 + t.month - 1                    # months since 2000-01
    p["in_ph_window"] = [m in PH_WINDOW[c] for m, c in zip(p.month, p.crop)]
    p["months_since_harvest"] = (p.month - p.crop.map(MKT_YEAR_START)) % 12
    # identifiers for fixed effects / clustering
    p["mc_id"] = p.market_key + "|" + p.commodity_id.astype(str)
    p["mcm_id"] = p.mc_id + "|" + p.month.astype(str)                    # market x commodity x calendar month (local seasonality)
    p["cym_id"] = p.commodity_id.astype(str) + "|" + p.ym
    p["sample_baseline"] = p.tier_primary & ~p.imported & p.ph_any.notna() & p.ln_price.notna()
    p["sample_placebo_imported"] = p.tier_primary & p.imported & p.ph_any.notna() & p.ln_price.notna()

    lead = ["market_key", "market_name", "district_id", "gadm_name_2", "division", "commodity_id", "commodity_name", "crop",
            "imported", "source", "ym", "year", "month", "season"]
    p = p[lead + [c for c in p.columns if c not in lead]].sort_values(["market_key", "commodity_id", "ym"])
    p.to_csv(FINAL / "paper_1_panel.csv", index=False)

    b = p[p.sample_baseline]
    log = ["# Step 4 - final panel log", "",
           f"All-tier panel rows: {len(p):,}",
           f"PRIMARY_ANALYSIS rows: {int(p.tier_primary.sum()):,}; with exposure: {int((p.tier_primary & p.ph_any.notna()).sum()):,}",
           f"Baseline estimation sample (PRIMARY, domestic varieties): {len(b):,} obs, {b.market_key.nunique()} markets, "
           f"{b.mc_id.nunique()} market x commodity units, {b.gadm_name_2.nunique()} districts, {b.cym_id.nunique()} commodity x month cells, "
           f"{b.ym.min()} .. {b.ym.max()}",
           f"Imported-variety placebo sample: {int(p.sample_placebo_imported.sum()):,} obs "
           f"({p[p.sample_placebo_imported].groupby('commodity_id').size().to_dict()})",
           "", "Baseline sample: distribution of pre-harvest shocked months (ph_any):", "```",
           b.ph_any.value_counts().sort_index().to_string(), "```",
           "", "Observations by commodity (baseline sample):", "```", b.groupby("commodity_name").size().to_string(), "```"]
    (INTER / "s04_panel_log.md").write_text("\n".join(log), encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
