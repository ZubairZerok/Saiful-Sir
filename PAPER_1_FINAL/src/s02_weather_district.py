"""Step 2 - Gridded weather -> district x month panel, climate normals, anomalies, shocks, SPEI.

District means are area-weighted: the weight of a grid cell in a district is the area of the
cell-polygon intersection (computed in an equal-area projection). Cells without data (sea cells
in ERA5-Land) get zero weight and the weights are renormalised.
"""
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import box
from scipy.stats import norm
from config import *

EA = "+proj=aea +lat_1=21 +lat_2=26 +lat_0=23.7 +lon_0=90.3 +datum=WGS84"   # Albers equal-area for Bangladesh


def district_weights(g, lat, lon, valid):
    """rows = districts, cols = flattened grid cells; row sums = 1 over valid cells."""
    dlat, dlon = abs(lat[1] - lat[0]), abs(lon[1] - lon[0])
    cells, idx = [], []
    for i, la in enumerate(lat):
        for j, lo in enumerate(lon):
            if valid[i, j]:
                cells.append(box(lo - dlon / 2, la - dlat / 2, lo + dlon / 2, la + dlat / 2))
                idx.append(i * len(lon) + j)
    cg = gpd.GeoDataFrame({"cell": idx}, geometry=cells, crs=4326).to_crs(EA)
    inter = gpd.overlay(g[["gadm_name_2", "geometry"]].to_crs(EA), cg, how="intersection")
    inter["a"] = inter.geometry.area
    W = np.zeros((len(g), len(lat) * len(lon)))
    pos = {n: k for k, n in enumerate(g.gadm_name_2)}
    for n, c, a in zip(inter.gadm_name_2, inter.cell, inter.a):
        W[pos[n], c] = a
    cover = W.sum(1) / g.to_crs(EA).geometry.area.values       # share of district area covered by data cells
    return W / W.sum(1, keepdims=True), cover


def to_district(g, npz, var, label, cov_log):
    z = np.load(npz, allow_pickle=False)
    lat, lon, months = z["lat"], z["lon"], [str(m) for m in z["months"]]
    x = z[var]                                                   # (month, lat, lon)
    valid = ~np.isnan(x).any(axis=0)
    W, cover = district_weights(g, lat, lon, valid)
    cov_log[label] = cover
    flat = np.where(valid.ravel()[None, :], x.reshape(len(months), -1), 0.0)
    d = flat @ W.T                                               # (month, district)
    return pd.DataFrame(d, index=months, columns=g.gadm_name_2).rename_axis("ym").reset_index().melt(
        id_vars="ym", var_name="gadm_name_2", value_name=label)


def hargreaves_pet(tmean, tmin, tmax, lat_deg, year, month):
    """Monthly reference evapotranspiration (mm/month), Hargreaves & Samani (1985)."""
    doy = pd.to_datetime(dict(year=year, month=month, day=15)).dt.dayofyear.values
    phi = np.deg2rad(lat_deg)
    dr = 1 + 0.033 * np.cos(2 * np.pi * doy / 365)
    dec = 0.409 * np.sin(2 * np.pi * doy / 365 - 1.39)
    ws = np.arccos(-np.tan(phi) * np.tan(dec))
    ra = 24 * 60 / np.pi * 0.0820 * dr * (ws * np.sin(phi) * np.sin(dec) + np.cos(phi) * np.cos(dec) * np.sin(ws))  # MJ m-2 d-1
    ndays = pd.to_datetime(dict(year=year, month=month, day=1)).dt.days_in_month.values
    return 0.0023 * (ra / 2.45) * (tmean + 17.8) * np.sqrt(np.clip(tmax - tmin, 0, None)) * ndays


def spei_from_balance(d, base):
    """Standardise a water-balance series (P - PET) as in the SPEI of Vicente-Serrano et al. (2010):
    a three-parameter log-logistic distribution fitted to the baseline sample by L-moments.  The fit
    uses Hosking's generalised-logistic parameterisation (shape k = -tau3), which is the same family
    and stays valid when the baseline sample is symmetric or negatively skewed."""
    x = np.sort(d[base]); n = len(x); i = np.arange(1, n + 1)
    a0 = x.mean()
    a1 = np.sum((n - i) / (n - 1) * x) / n
    a2 = np.sum((n - i) * (n - i - 1) / ((n - 1) * (n - 2)) * x) / n
    l1, l2, l3 = a0, a0 - 2 * a1, a0 - 6 * a1 + 6 * a2
    k = -l3 / l2
    if abs(k) < 1e-6:
        y = (d - l1) / l2
    else:
        a = l2 * np.sin(k * np.pi) / (k * np.pi)
        xi = l1 - a * (1 / k - np.pi / np.sin(k * np.pi))
        arg = 1 - k * (d - xi) / a
        with np.errstate(all="ignore"):
            y = -np.log(arg) / k
        y = np.where(arg <= 0, np.inf if k > 0 else -np.inf, y)       # outside the fitted support
    F = np.clip(1 / (1 + np.exp(-y)), 1e-4, 1 - 1e-4)                 # caps SPEI at +-3.72
    return norm.ppf(F)


def main():
    g = gpd.read_file(RAW / "geo" / "gadm41_BGD_2.json")[["GID_2", "NAME_1", "NAME_2", "geometry"]]
    g = g.rename(columns={"NAME_2": "gadm_name_2", "GID_2": "district_id", "NAME_1": "division"})
    assert len(g) == 64

    # ---- district centroids and distance to Dhaka ---------------------------------------------
    cen = g.to_crs(EA).geometry.centroid.to_crs(4326)
    geo = pd.DataFrame({"district_id": g.district_id, "gadm_name_2": g.gadm_name_2, "division": g.division,
                        "centroid_lat": cen.y.round(5), "centroid_lon": cen.x.round(5),
                        "area_km2": (g.to_crs(EA).geometry.area / 1e6).round(1)})
    from pyproj import Geod
    _, _, dist = Geod(ellps="WGS84").inv(geo.centroid_lon.values, geo.centroid_lat.values,
                                         np.full(64, DHAKA_LON), np.full(64, DHAKA_LAT))
    geo["distance_to_dhaka_km"] = (dist / 1000).round(2)
    geo.to_csv(INTER / "district_geography.csv", index=False)

    # ---- area-weighted district means ------------------------------------------------------------
    cov = {}
    w = RAW / "weather"
    parts = [to_district(g, w / "era5land_t2m_monthly_grid.npz", v, f"{v}_c", cov) for v in ("tmean", "tmin", "tmax")]
    parts.append(to_district(g, w / "era5_precip_monthly_grid.npz", "precip", "precip_mm", cov))
    chirps = to_district(g, w / "chirps_v2_precip_monthly_grid.npz", "precip", "precip_chirps_mm", cov)
    d = parts[0]
    for p in parts[1:]:
        d = d.merge(p, on=["ym", "gadm_name_2"], how="inner")
    d = d.merge(chirps, on=["ym", "gadm_name_2"], how="left")
    d = d[(d.ym >= WEATHER_START) & (d.ym <= WEATHER_END)]
    d["year"], d["month"] = d.ym.str[:4].astype(int), d.ym.str[5:7].astype(int)
    d = d.merge(geo[["district_id", "gadm_name_2", "centroid_lat"]], on="gadm_name_2")
    pd.DataFrame(cov, index=g.gadm_name_2).round(4).to_csv(INTER / "weather_district_cell_coverage.csv")

    # completeness: balanced district x month grid, no missing values in the ERA5 fields
    months = pd.period_range(WEATHER_START, WEATHER_END, freq="M").astype(str)
    assert len(d) == 64 * len(months), (len(d), 64 * len(months))
    assert not d[["precip_mm", "tmean_c", "tmin_c", "tmax_c"]].isna().any().any()

    # ---- normals (1991-2020) and z-scores ------------------------------------------------------------
    base = d.year.between(*BASELINE_YEARS)
    d = d.sort_values(["gadm_name_2", "ym"]).reset_index(drop=True)
    base = d.year.between(*BASELINE_YEARS)
    for v, z in (("precip_mm", "z_precip"), ("tmean_c", "z_temp"), ("precip_chirps_mm", "z_precip_chirps")):
        st = d[base].groupby(["gadm_name_2", "month"])[v].agg(["mean", "std"])      # sample SD (ddof=1), n=30
        st.columns = [f"{v}_normal", f"{v}_sd"]
        d = d.merge(st, left_on=["gadm_name_2", "month"], right_index=True, how="left")
        d[z] = (d[v] - d[f"{v}_normal"]) / d[f"{v}_sd"]
        # empirical percentile rank in the baseline distribution (for the percentile-based robustness shocks)
        ref = d[base].groupby(["gadm_name_2", "month"])[v].apply(lambda s: np.sort(s.values))
        keys = list(zip(d.gadm_name_2, d.month))
        d[z.replace("z_", "pct_")] = [np.searchsorted(ref[k], x, side="right") / len(ref[k]) if x == x else np.nan
                                      for k, x in zip(keys, d[v])]

    # ---- SPEI (Hargreaves PET; log-logistic; 1- and 3-month scales) ------------------------------------
    d["pet_mm"] = hargreaves_pet(d.tmean_c.values, d.tmin_c.values, d.tmax_c.values, d.centroid_lat.values, d.year, d.month)
    d["wb1"] = d.precip_mm - d.pet_mm
    d["wb3"] = d.groupby("gadm_name_2").wb1.transform(lambda s: s.rolling(3).sum())
    for k in (1, 3):
        d[f"spei{k}"] = np.nan
        for (_, _), s in d.groupby(["gadm_name_2", "month"]):
            ok = s[f"wb{k}"].notna().values
            b = (s.year.between(*BASELINE_YEARS).values) & ok
            out = np.full(len(s), np.nan)
            out[ok] = spei_from_balance(s[f"wb{k}"].values[ok], b[ok])
            d.loc[s.index, f"spei{k}"] = out

    # ---- monthly shock indicators ---------------------------------------------------------------------
    for thr, tag in ((1.0, "10"), (1.5, "15"), (2.0, "20")):
        d[f"excess_rain_{tag}"] = (d.z_precip > thr).astype(int)
        d[f"drought_{tag}"] = (d.z_precip < -thr).astype(int)
        d[f"heatwave_{tag}"] = (d.z_temp > thr).astype(int)
        d[f"cold_{tag}"] = (d.z_temp < -thr).astype(int)
        d[f"any_shock_{tag}"] = d[[f"excess_rain_{tag}", f"drought_{tag}", f"heatwave_{tag}", f"cold_{tag}"]].max(axis=1)
    # CHIRPS rainfall shocks (temperature shocks stay ERA5-Land; CHIRPS has no temperature)
    d["excess_rain_chirps"] = (d.z_precip_chirps > SHOCK_SD).astype("Int64").where(d.z_precip_chirps.notna())
    d["drought_chirps"] = (d.z_precip_chirps < -SHOCK_SD).astype("Int64").where(d.z_precip_chirps.notna())
    d["any_shock_chirps"] = d[["excess_rain_chirps", "drought_chirps", "heatwave_15", "cold_15"]].max(axis=1).where(d.z_precip_chirps.notna())
    # SPEI-1 moisture shocks + temperature shocks
    d["wet_spei"] = (d.spei1 > SHOCK_SD).astype(int)
    d["dry_spei"] = (d.spei1 < -SHOCK_SD).astype(int)
    d["any_shock_spei"] = d[["wet_spei", "dry_spei", "heatwave_15", "cold_15"]].max(axis=1)
    # percentile shocks: outside the 10th-90th percentile band of the 1991-2020 district-month distribution
    d["any_shock_pct"] = ((d.pct_precip > 0.9) | (d.pct_precip <= 0.1) | (d.pct_temp > 0.9) | (d.pct_temp <= 0.1)).astype(int)

    cols = ["district_id", "gadm_name_2", "ym", "year", "month", "precip_mm", "tmean_c", "tmin_c", "tmax_c", "precip_chirps_mm"]
    d[cols].round(4).to_csv(INTER / "weather_district_monthly.csv", index=False)
    d.drop(columns=["centroid_lat", "wb1", "wb3"]).round(5).to_csv(INTER / "weather_district_monthly_anomalies.csv", index=False)

    # ---- diagnostics ------------------------------------------------------------------------------
    s = d[d.year >= 2000]
    freq = s.groupby("month")[[c for c in d.columns if c.endswith("_15")] + ["wet_spei", "dry_spei"]].mean().round(4)
    freq.to_csv(INTER / "weather_shock_frequency_by_calendar_month.csv")
    ok = d.dropna(subset=["precip_chirps_mm"])
    r_lvl = np.corrcoef(ok.precip_mm, ok.precip_chirps_mm)[0, 1]
    r_z = np.corrcoef(ok.z_precip, ok.z_precip_chirps)[0, 1]
    log = ["# Step 2 - district weather log", "",
           f"District-months: {len(d):,} = 64 districts x {len(months)} months ({months[0]} .. {months[-1]}); no missing ERA5 values.",
           f"CHIRPS coverage: {ok.ym.min()} .. {ok.ym.max()} ({len(ok):,} district-months).",
           f"Minimum share of district area covered by data cells: " + ", ".join(f"{k}={v.min():.3f}" for k, v in cov.items()),
           f"ERA5 vs CHIRPS district-month rainfall: corr(levels) = {r_lvl:.3f}, corr(z-scores) = {r_z:.3f}.",
           "", "Share of district-months (2000+) flagged as shocks at +-1.5 SD, by calendar month:", "```", freq.to_string(), "```"]
    (INTER / "s02_weather_log.md").write_text("\n".join(log), encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
