"""Step 1 - Acquire gridded weather for the Bangladesh bounding box (OPTIONAL, network required).

The outputs of this step are committed under data/raw/weather/, so the pipeline runs offline.
Re-run with:  python src/s01_weather_download.py [n_workers]

Sources (all open, no API key)
------------------------------
1. ERA5-Land 2 m temperature, hourly, 0.1 deg (ECMWF / Copernicus C3S), read from the Open-Meteo
   open-data mirror on AWS S3 (bucket `openmeteo`, prefix data/copernicus_era5_land/temperature_2m/).
   The Copernicus CDS API needs a personal key that was not available; the mirror holds the same
   ERA5-Land fields re-encoded in the `.om` format.
2. ERA5 total precipitation, hourly, 0.25 deg (same mirror, data/copernicus_era5/precipitation/).
   The mirror carries no ERA5-Land precipitation. ERA5-Land precipitation is not an independent
   product: it is the ERA5 precipitation forcing interpolated to the 0.1 deg grid, so district means
   of the two are near-identical.
3. CHIRPS v2.0 monthly precipitation, 0.05 deg (Climate Hazards Center, UCSB), subset through the
   IRI Data Library (iridl.ldeo.columbia.edu).
4. GADM 4.1 level-2 polygons (64 districts) from geodata.ucdavis.edu.

Hourly fields are reduced to UTC-day statistics per grid cell (mean/min/max temperature, precipitation
sum) and then to calendar months. A month is kept only if every day has 24 valid hourly values.
"""
import os
import sys
import time
import warnings
import subprocess
import numpy as np
import pandas as pd
from multiprocessing import Pool
from config import *

CACHE = os.environ.get("P1_WEATHER_CACHE", "/tmp/wx")
DAILY = f"{CACHE}/daily"
# grid index boxes.  ERA5-Land: lat=-90+0.1*i, lon=-180+0.1*j.  ERA5: lat=-90+0.25*i, lon=-180+0.25*j
BOX = {"t2m": (1105, 1168, 2680, 2728, 0.1, "openmeteo/data/copernicus_era5_land/temperature_2m/"),
       "pr": (442, 468, 1072, 1092, 0.25, "openmeteo/data/copernicus_era5/precipitation/")}
YEAR_FILES = range(1991, 2022)          # year_YYYY.om (complete calendar years)
CHUNK_FILES = range(904, 990)           # chunk_N.om: 504 h (21 d) blocks; N*504 h since 1970-01-01
EPOCH = pd.Timestamp("1970-01-01")


def tasks():
    return [(v, f"year_{y}") for v in BOX for y in YEAR_FILES] + [(v, f"chunk_{c}") for v in BOX for c in CHUNK_FILES]


def fetch(args):
    import omfiles, fsspec
    var, tag = args
    fn = f"{DAILY}/{var}_{tag}.npz"
    if os.path.exists(fn):
        return var, tag, "cached"
    i0, i1, j0, j1, _, pre = BOX[var]
    err = ""
    for attempt in range(5):
        try:
            fs = fsspec.filesystem("s3", anon=True)
            if not fs.exists(pre + tag + ".om"):
                return var, tag, "missing"
            r = omfiles.OmFileReader.from_fsspec(fs, pre + tag + ".om")
            nt = r.shape[2]
            a = r[i0:i1, j0:j1, 0:nt]
            break
        except Exception as e:                      # network hiccup -> retry with back-off
            err = repr(e)
            time.sleep(5 * (attempt + 1))
    else:
        return var, tag, "FAILED " + err
    nd = nt // 24
    a = a[:, :, :nd * 24].reshape(a.shape[0], a.shape[1], nd, 24)
    nvalid = (~np.isnan(a)).sum(axis=3).astype(np.int8)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if var == "t2m":
            np.savez_compressed(fn + ".tmp.npz", mean=np.nanmean(a, 3), min=np.nanmin(a, 3), max=np.nanmax(a, 3), nvalid=nvalid)
        else:
            np.savez_compressed(fn + ".tmp.npz", sum=np.nansum(a, 3), nvalid=nvalid)
    os.replace(fn + ".tmp.npz", fn)
    return var, tag, f"ok nt={nt}"


def assemble(var):
    """Daily per-cell files -> one daily cube -> complete calendar months."""
    i0, i1, j0, j1, res, _ = BOX[var]
    stats = ["mean", "min", "max"] if var == "t2m" else ["sum"]
    days, cubes, valid = [], {s: [] for s in stats}, []
    for y in YEAR_FILES:
        z = np.load(f"{DAILY}/{var}_year_{y}.npz")
        d = pd.date_range(f"{y}-01-01", periods=z["nvalid"].shape[2], freq="D")
        assert d[-1] == pd.Timestamp(f"{y}-12-31")
        days.append(d); valid.append(z["nvalid"])
        for s in stats:
            cubes[s].append(z[s])
    for c in CHUNK_FILES:
        fn = f"{DAILY}/{var}_chunk_{c}.npz"
        if not os.path.exists(fn):
            continue
        z = np.load(fn)
        d = pd.date_range(EPOCH + pd.Timedelta(hours=c * 504), periods=z["nvalid"].shape[2], freq="D")
        keep = d >= pd.Timestamp(f"{YEAR_FILES[-1] + 1}-01-01")
        days.append(d[keep]); valid.append(z["nvalid"][:, :, keep])
        for s in stats:
            cubes[s].append(z[s][:, :, keep])
    days = days[0].append(days[1:])
    assert days.is_monotonic_increasing and days.is_unique and (np.diff(days.values).astype("timedelta64[D]").astype(int) == 1).all()
    valid = np.concatenate(valid, 2)
    cubes = {s: np.concatenate(v, 2) for s, v in cubes.items()}
    land = valid[:, :, :365].max(axis=2) == 24                 # cells that carry data (ERA5-Land is land-only)
    day_ok = (valid[land] == 24).all(axis=0)                   # day complete on every data cell
    per = days.to_period("M")
    months = [m for m in per.unique() if day_ok[per == m].all() and (per == m).sum() == m.days_in_month]
    out = {s: np.full((len(months),) + land.shape, np.nan, np.float32) for s in stats}
    for k, m in enumerate(months):
        sel = per == m
        for s in stats:
            x = cubes[s][:, :, sel]
            out[s][k] = x.sum(axis=2) if s == "sum" else x.mean(axis=2)
            out[s][k][~land] = np.nan
    lat = -90 + res * np.arange(i0, i1)
    lon = -180 + res * np.arange(j0, j1)
    return np.round(lat, 4), np.round(lon, 4), [str(m) for m in months], out


def chirps():
    os.makedirs(f"{CACHE}/chirps", exist_ok=True)
    url = ("https://iridl.ldeo.columbia.edu/SOURCES/.UCSB/.CHIRPS/.v2p0/.monthly/.global/.precipitation/"
           "X/87.9/92.8/RANGEEDGES/Y/20.4/26.8/RANGEEDGES/T/(Jan%20{a})/(Dec%20{b})/RANGEEDGES/data.nc")
    import xarray as xr
    parts = []
    for a in range(1991, 2027, 5):
        fn = f"{CACHE}/chirps/c_{a}.nc"
        if not os.path.exists(fn):
            subprocess.run(["curl", "-sSL", "-m", "280", "--retry", "3", "-o", fn, url.format(a=a, b=min(a + 4, 2026))], check=True)
        parts.append(xr.open_dataset(fn, decode_times=False))
    d = xr.concat(parts, "T")
    t = np.floor(d["T"].values).astype(int)                     # months since 1960-01
    months = [f"{1960 + k // 12}-{k % 12 + 1:02d}" for k in t]
    assert len(set(months)) == len(months)
    return d["Y"].values.astype(float), d["X"].values.astype(float), months, d["precipitation"].values.astype(np.float32)


def main():
    os.makedirs(DAILY, exist_ok=True)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    with Pool(n) as p:
        for res in p.imap_unordered(fetch, tasks()):
            if not res[2].startswith(("ok", "cached", "missing")):
                raise RuntimeError(res)
    out = RAW / "weather"
    lat, lon, months, t = assemble("t2m")
    np.savez_compressed(out / "era5land_t2m_monthly_grid.npz", lat=lat, lon=lon, months=months,
                        tmean=t["mean"], tmin=t["min"], tmax=t["max"])
    print("ERA5-Land t2m:", months[0], months[-1], len(months), t["mean"].shape)
    lat, lon, months, p_ = assemble("pr")
    np.savez_compressed(out / "era5_precip_monthly_grid.npz", lat=lat, lon=lon, months=months, precip=p_["sum"])
    print("ERA5 precip:", months[0], months[-1], len(months), p_["sum"].shape)
    lat, lon, months, c = chirps()
    np.savez_compressed(out / "chirps_v2_precip_monthly_grid.npz", lat=lat, lon=lon, months=months, precip=c)
    print("CHIRPS:", months[0], months[-1], len(months), c.shape)


if __name__ == "__main__":
    main()
