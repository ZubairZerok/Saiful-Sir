"""Step 6 - Publication tables (CSV + LaTeX) and figures (PDF + PNG, 300 dpi).

Everything is generated from data/final/paper_1_panel.csv, the weather intermediates and
analysis/models/{results,tests}_registry.csv.  Colour convention: blues = precipitation,
reds = temperature, greens = prices.
"""
import json
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from config import *

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Nimbus Roman", "TeX Gyre Termes", "DejaVu Serif"],
    "mathtext.fontset": "cm", "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9, "legend.fontsize": 8,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e6e6e6", "grid.linewidth": 0.5,
    "axes.axisbelow": True, "savefig.dpi": 300, "savefig.bbox": "tight", "pdf.fonttype": 42})
G_DARK, G_MID, G_LIGHT = "#00441b", "#238b45", "#74c476"       # prices
B_DARK, B_MID = "#08519c", "#6baed6"                           # precipitation
R_DARK, R_MID = "#a50f15", "#fb6a4a"                           # temperature
INK, MUTED = "#222222", "#6b6b6b"
GAP = ("2023-08", "2025-05")


def stars(p):
    return "" if p != p else "***" if p < .01 else "**" if p < .05 else "*" if p < .10 else ""


def save(fig, name, note):
    fig.text(0.01, -0.02, note, ha="left", va="top", fontsize=7, color=MUTED, wrap=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIGS / f"{name}.{ext}")
    plt.close(fig)


def latex_table(df, path, caption, label, note):
    cols = "l" + "c" * (df.shape[1] - 1)
    esc = lambda s: str(s).replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")
    lines = [r"\begin{table}[htbp]\centering\small", rf"\caption{{{esc(caption)}}}\label{{{label}}}",
             rf"\begin{{tabular}}{{{cols}}}", r"\toprule", " & ".join(esc(c) for c in df.columns) + r" \\", r"\midrule"]
    for _, r in df.iterrows():
        if str(r.iloc[0]).startswith("--"):
            lines.append(r"\midrule")
            continue
        lines.append(" & ".join("" if (isinstance(v, float) and v != v) else esc(v) for v in r) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\begin{minipage}{0.95\linewidth}\footnotesize \textit{Notes:} " + esc(note) + r"\end{minipage}",
              r"\end{table}"]
    path.write_text("\n".join(lines), encoding="utf-8")


def reg_table(reg, models, term_labels, name, caption, note, extra_rows=None, col_labels=None):
    """Classic regression table: coefficient with stars, cluster SE in parentheses, bottom rows."""
    rows = []
    for term, lab in term_labels.items():
        b, s = [lab], [""]
        for m in models:
            r = reg[(reg.model == m) & (reg.term == term)]
            if len(r) and r.coef.notna().all():
                r = r.iloc[0]
                b.append(f"{r.coef:.4f}{stars(r.p_cluster)}"); s.append(f"({r.se_cluster:.4f})")
            else:
                b.append(""); s.append("")
        rows += [b, s]
    rows.append(["--"] + [""] * len(models))
    first = {m: reg[reg.model == m].iloc[0] for m in models}
    rows.append(["Observations"] + [f"{int(first[m].n_obs):,}" for m in models])
    rows.append(["R2 within"] + [f"{first[m].r2_within:.4f}" for m in models])
    rows.append(["R2 overall"] + [f"{first[m].r2_overall:.4f}" for m in models])
    rows.append(["Market x commodity FE groups"] + [f"{int(first[m].n_fe_market_commodity):,}" for m in models])
    rows.append(["Commodity x year-month FE groups"] + [f"{int(first[m].n_fe_time):,}" for m in models])
    rows.append(["Clusters (districts)"] + [f"{int(first[m].n_clusters)}" for m in models])
    for lab, vals in (extra_rows or {}).items():
        rows.append([lab] + list(vals))
    cols = [""] + (col_labels or [f"({i + 1})" for i in range(len(models))])
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(TABLES / f"{name}.csv", index=False)
    latex_table(df, TABLES / f"{name}.tex", caption, f"tab:{name}", note)
    return df


def tables(p, w, reg, tests):
    base = p[p.sample_baseline]
    # ------------------------------ Table 1 ------------------------------------------
    def desc(s):
        return [s.mean(), s.std(), s.min(), s.quantile(.25), s.median(), s.quantile(.75), s.max(), int(s.notna().sum())]
    hdr = ["Variable", "Mean", "SD", "Min", "P25", "Median", "P75", "Max", "N"]
    A = []
    prim = p[p.tier_primary]
    for lab, sub in (("Onion, domestic (831, 833)", prim[(prim.crop == "onion") & ~prim.imported]),
                     ("Potato, domestic (942-948)", prim[(prim.crop == "potato") & ~prim.imported]),
                     ("Onion, imported (832)", prim[prim.commodity_id == 832]),
                     ("Potato, imported (21014)", prim[prim.commodity_id == 21014])):
        A.append([f"Wholesale price, BDT/kg - {lab}"] + desc(sub.price_wholesale_raw_mid_kg))
        A.append([f"Retail price, BDT/kg - {lab}"] + desc(sub.price_retail_raw_mid_kg.where(sub.retail_primary)))
    A.append(["ln wholesale price (baseline sample)"] + desc(base.ln_price))
    A = pd.DataFrame(A, columns=hdr)
    ws = w[(w.ym >= "1999-10") & (w.ym <= "2026-08")]
    B = [[lab] + desc(ws[c]) for lab, c in (
        ("Precipitation, mm/month (ERA5)", "precip_mm"), ("Precipitation, mm/month (CHIRPS)", "precip_chirps_mm"),
        ("Mean temperature, C (ERA5-Land)", "tmean_c"), ("Minimum temperature, C", "tmin_c"), ("Maximum temperature, C", "tmax_c"),
        ("Precipitation z-score", "z_precip"), ("Temperature z-score", "z_temp"), ("SPEI-1", "spei1"),
        ("Excess-rain shock (z > 1.5)", "excess_rain_15"), ("Drought shock (z < -1.5)", "drought_15"),
        ("Heat shock (z > 1.5)", "heatwave_15"), ("Cold shock (z < -1.5)", "cold_15"), ("Any shock", "any_shock_15"))]
    for lab, c in (("Pre-harvest shocked months, any (baseline sample)", "ph_any"), ("  excess rain", "ph_excess_rain"),
                   ("  drought", "ph_drought"), ("  heat", "ph_heatwave"), ("  cold", "ph_cold"),
                   ("Distance to Dhaka, km (baseline sample)", "distance_to_dhaka_km")):
        B.append([lab] + desc(base[c]))
    B = pd.DataFrame(B, columns=hdr)
    C = pd.DataFrame([
        ["Market x commodity x month observations, all tiers", f"{len(p):,}"],
        ["PRIMARY_ANALYSIS tier", f"{int(p.tier_primary.sum()):,}"],
        ["STRICT_SENSITIVITY tier", f"{int(p.tier_strict.sum()):,}"],
        ["Baseline estimation sample (PRIMARY, domestic varieties)", f"{len(base):,}"],
        ["  of which onion / potato", f"{int((base.crop == 'onion').sum()):,} / {int((base.crop == 'potato').sum()):,}"],
        ["  of which historical web portal / MOA API", f"{int((base.source == 'dam_web_historical').sum()):,} / {int((base.source == 'moa_api').sum()):,}"],
        ["Imported-variety placebo sample (832 / 21014)", f"{int((p.sample_placebo_imported & (p.commodity_id == 832)).sum()):,} / {int((p.sample_placebo_imported & (p.commodity_id == 21014)).sum()):,}"],
        ["Markets (baseline sample)", f"{base.market_key.nunique()}"],
        ["Districts (clusters)", f"{base.gadm_name_2.nunique()}"],
        ["Domestic commodity varieties", f"{base.commodity_id.nunique()}"],
        ["Market x commodity units", f"{base.mc_id.nunique():,}"],
        ["Time span", f"{base.ym.min()} to {base.ym.max()}"],
        ["Calendar months with data", f"{base.ym.nunique()}"],
        ["Institutional gap (no DAM data)", f"{GAP[0]} to {GAP[1]}; also 2014-10 to 2015-02 and 2015-09 to 2015-12"],
        ["Weather district-months (64 districts)", f"{len(w):,} ({w.ym.min()} to {w.ym.max()})"]], columns=["Item", "Value"])
    for nm, df, cap in (("table1a_descriptives_prices", A, "Descriptive statistics: prices"),
                        ("table1b_descriptives_weather", B, "Descriptive statistics: weather and exposure"),
                        ("table1c_sample_composition", C, "Sample composition")):
        out = df.copy()
        for c in out.columns[1:]:
            out[c] = out[c].map(lambda v: f"{v:,.3f}" if isinstance(v, float) else (f"{v:,}" if isinstance(v, (int, np.integer)) else v))
        out.to_csv(TABLES / f"{nm}.csv", index=False)
        latex_table(out, TABLES / f"{nm}.tex", "Table 1. " + cap, f"tab:{nm}",
                    "Prices are PRIMARY_ANALYSIS-tier wholesale midpoints (low+high)/2 in BDT per kg. Weather statistics cover district-months "
                    "1999-10 to 2026-08. Shock indicators are defined relative to 1991-2020 district-by-calendar-month normals.")

    # ------------------------------ Table 2 ------------------------------------------
    T = {"ph_any": "Pre-harvest shocked months (any)", "ph_excess_rain": "Excess-rain months", "ph_drought": "Drought months",
         "ph_heatwave": "Heat months", "ph_cold": "Cold months"}
    se_note = ("Dependent variable: ln wholesale price (raw midpoint, BDT/kg). All columns include market x commodity and commodity x year-month "
               "fixed effects. Standard errors clustered by district in parentheses. * p<0.10, ** p<0.05, *** p<0.01. R2 within is net of the fixed effects.")
    m = ["M1_baseline", "M2_decomposed", "M3a_onion", "M3b_potato", "M1_trends"]
    reg_table(reg, m, T, "table2_main_results", "Table 2. Pre-harvest weather shocks and wholesale prices", se_note,
              extra_rows={"Sample": ["All", "All", "Onion", "Potato", "All"], "Market-specific linear trends": ["No", "No", "No", "No", "Yes"],
                          "HC1 SE of first coefficient": [f"{reg[reg.model == x].iloc[0].se_hc1:.4f}" for x in m],
                          "Two-way (district, month) SE": [f"{reg[reg.model == x].iloc[0].se_twoway:.4f}" for x in m]})
    # ------------------------------ Table 3 ------------------------------------------
    T3 = {"ph_any": "Pre-harvest shocked months", "ph_x_lndist": "Shocked months x ln distance to Dhaka (centred)",
          "ph_sq": "Shocked months squared", "ph_bin1": "1 shocked month", "ph_bin2": "2 shocked months", "ph_bin3p": "3+ shocked months"}
    reg_table(reg, ["M4_distance", "M7_quadratic", "M47_combined", "M7_bins"], T3, "table3_spatial_nonlinearity",
              "Table 3. Spatial friction and severity non-linearity", se_note + " Column (4): reference category is zero shocked months.")
    # ------------------------------ Table 5 ------------------------------------------
    T5 = {"ln_price": "ln wholesale price", "ph_any": "Pre-harvest shocked months"}
    reg_table(reg, ["M6_passthrough", "M6_retail_reduced_form", "M6_wholesale_same_sample", "M6_margin"], T5, "table5_retail_passthrough",
              "Table 5. Retail pass-through", "Fixed effects and clustering as in Table 2. Sample: observations with a valid retail quote.",
              col_labels=["(1) ln retail", "(2) ln retail", "(3) ln wholesale", "(4) ln retail - ln wholesale"])

    # ------------------------------ Table 4 / 6 / 8: one row per estimate -----------------
    def rowtab(group, name, caption, note):
        r = reg[reg.group == group].copy()
        out = pd.DataFrame({"Specification": r.model, "Term": r.term,
                            "Coef.": r.coef.map(lambda v: "" if v != v else f"{v:.4f}") + r.p_cluster.map(stars),
                            "SE (district)": r.se_cluster.map(lambda v: "" if v != v else f"{v:.4f}"),
                            "p": r.p_cluster.map(lambda v: "" if v != v else f"{v:.3f}"),
                            "p (two-way)": r.p_twoway.map(lambda v: "" if v != v else f"{v:.3f}"),
                            "N": r.n_obs.map(lambda v: f"{int(v):,}"), "Share non-zero": r.share_nonzero.map(lambda v: f"{v:.3f}"),
                            "Notes": r.note.fillna("")})
        out.to_csv(TABLES / f"{name}.csv", index=False)
        latex_table(out.drop(columns="Notes"), TABLES / f"{name}.tex", caption, f"tab:{name}", note)
    b0 = reg[reg.model == "M1_baseline"].iloc[0]
    rowtab("robustness", "table4_robustness", "Table 4. Robustness checks",
           f"Baseline (Table 2, col. 1): coefficient {b0.coef:.4f}, SE {b0.se_cluster:.4f}, N {int(b0.n_obs):,}. Each row is a separate regression of "
           "ln wholesale price with market x commodity and commodity x year-month fixed effects unless stated in the replication notes; "
           "standard errors clustered by district. 'Share non-zero' is the share of observations with a non-zero regressor.")
    rowtab("placebo", "table6_placebo_tests", "Table 6. Placebo tests",
           "P1: next season's exposure (strictly future weather). P2: imported varieties. P3: shocks in the off-season window. See text.")
    rowtab("heat_battery", "table8_heat_robustness", "Table 8. Robustness of the decomposed-shock model", "Variants of Table 2, col. 2.")

    # ------------------------------ Table 7: event study -----------------------------------
    ev = reg[reg.group == "event_study"]
    order = [f"S_lead{k}" for k in (3, 2, 1)] + [f"S_lag{k}" for k in range(7)]
    lab = {**{f"S_lead{k}": f"Shock at t+{k} (lead, placebo)" for k in (1, 2, 3)}, **{f"S_lag{k}": f"Shock at t-{k}" for k in range(7)}}
    lab["S_lag0"] = "Shock at t"
    ms = ["M5a_event_briefFE", "M5b_event_seasonalFE", "M5c_event_districtSeasonFE", "M5b_event_seasonalFE_onion", "M5b_event_seasonalFE_potato"]
    pt = {mm: tests[(tests.model == mm) & tests.test.str.startswith("pre-trend")].p.iloc[0] for mm in ms}
    al = {mm: tests[(tests.model == mm) & (tests.test == "all lags jointly zero")].p.iloc[0] for mm in ms}
    reg_table(ev, ms, {t: lab[t] for t in order}, "table7_event_study", "Table 7. Monthly event study around in-season shocks",
              "Dependent variable: ln wholesale price. Regressors are indicators for an in-window shock month in the district k months before (lags) "
              "or after (leads) the price month. Col. (1): fixed effects of the brief. Col. (2), (4), (5): market x commodity x calendar-month and "
              "commodity x year-month FE. Col. (3): brief FE plus district x crop x calendar-month FE. SE clustered by district.",
              extra_rows={"Pre-trend F-test p-value (leads 1-3)": [f"{pt[x]:.3f}" for x in ms], "All lags = 0, p-value": [f"{al[x]:.3f}" for x in ms],
                          "Sample": ["All", "All", "All", "Onion", "Potato"]},
              col_labels=["(1) Brief FE", "(2) Seasonal FE", "(3) District-season FE", "(4) Onion", "(5) Potato"])
    tests.to_csv(TABLES / "table9_joint_tests.csv", index=False)


def figures(p, w, reg, tests):
    base = p[p.sample_baseline].copy()
    g = gpd.read_file(RAW / "geo" / "gadm41_BGD_2.json").rename(columns={"NAME_2": "gadm_name_2"})
    geo = pd.read_csv(INTER / "district_geography.csv")
    src = "Sources: DAM/MOA wholesale prices; ERA5-Land and ERA5 (ECMWF/C3S); CHIRPS v2.0; GADM 4.1."

    # ---- Figure 1: map --------------------------------------------------------------------
    base["rel"] = base.ln_price - base.groupby("cym_id").ln_price.transform("mean")
    d = base.groupby("gadm_name_2").agg(rel=("rel", "mean"), n=("rel", "size"), markets=("market_key", "nunique")).reset_index()
    d["index"] = 100 * np.exp(d.rel)
    d.to_csv(FIGS / "figure1_data.csv", index=False)
    gg = g.merge(d, on="gadm_name_2", how="left").merge(geo[["gadm_name_2", "centroid_lat", "centroid_lon"]], on="gadm_name_2")
    fig, ax = plt.subplots(figsize=(5.6, 6.6))
    gg.plot(column="index", cmap="Greens", linewidth=0.4, edgecolor="white", ax=ax, legend=True, vmin=gg["index"].min(), vmax=gg["index"].max(),
            legend_kwds={"label": "Relative wholesale price level (national commodity-month mean = 100)", "orientation": "horizontal", "shrink": 0.75, "pad": 0.03})
    ax.scatter(gg.centroid_lon, gg.centroid_lat, s=6 + 5 * gg.markets, facecolor="none", edgecolor=INK, linewidth=0.6)
    ax.scatter([DHAKA_LON], [DHAKA_LAT], marker="*", s=90, color=INK, zorder=5)
    ax.annotate("Dhaka", (DHAKA_LON, DHAKA_LAT), xytext=(-30, 16), textcoords="offset points", fontsize=8, color=INK,
                bbox=dict(facecolor="white", edgecolor="none", pad=1, alpha=0.85), arrowprops=dict(arrowstyle="-", color=INK, lw=0.5))
    for k in (1, 4, 8):
        ax.scatter([], [], s=6 + 5 * k, facecolor="none", edgecolor=INK, linewidth=0.6, label=f"{k} reporting market{'s' if k > 1 else ''}")
    ax.legend(loc="lower left", frameon=False, title="District reporting markets", title_fontsize=8)
    ax.set_axis_off(); ax.grid(False)
    ax.set_title("Figure 1. Districts, reporting markets and relative wholesale price levels, 2000-2026")
    fig.tight_layout()
    save(fig, "figure1_map", "Circles sit at district centroids (market geocodes are not available in the DAM data); size = number of distinct reporting "
         "markets, 2000-2026.\nShading: district mean of ln price deviations from the commodity x month national mean, baseline sample. " + src)

    # ---- Figure 2: time series ----------------------------------------------------------
    months = pd.period_range("2000-01", "2026-08", freq="M")
    x = months.to_timestamp()
    pr = base.groupby(["crop", "ym"]).price_wholesale_raw_mid_kg.mean().unstack(0).reindex(months.astype(str))
    ws = w[w.ym.between("2000-01", "2026-08")].groupby("ym")[["z_precip", "z_temp"]].mean().reindex(months.astype(str))
    pd.concat([pr, ws], axis=1).to_csv(FIGS / "figure2_data.csv", index_label="ym")
    fig, axs = plt.subplots(3, 1, figsize=(7.2, 7.0), sharex=True)
    axs[0].plot(x, pr["onion"].values, color=G_DARK, lw=1.3, label="Onion (domestic varieties)")
    axs[0].plot(x, pr["potato"].values, color=G_LIGHT, lw=1.3, ls="--", label="Potato (domestic varieties)")
    axs[0].set_ylabel("BDT per kg"); axs[0].set_title("A. Monthly mean wholesale price"); axs[0].legend(frameon=False, loc="upper left")
    axs[1].bar(x, ws.z_precip.values, width=25, color=B_DARK); axs[1].set_ylabel("z-score")
    axs[1].set_title("B. Precipitation anomaly, mean across 64 districts (ERA5, 1991-2020 normals)")
    axs[2].bar(x, ws.z_temp.values, width=25, color=R_DARK); axs[2].set_ylabel("z-score")
    axs[2].set_title("C. Temperature anomaly, mean across 64 districts (ERA5-Land, 1991-2020 normals)")
    for a in axs:
        a.axvspan(pd.Timestamp(GAP[0]), pd.Timestamp(GAP[1]) + pd.offsets.MonthEnd(1), color="#bdbdbd", alpha=0.45, lw=0)
        a.axhline(0, color=INK, lw=0.5)
    axs[0].annotate("No DAM data\n2023-08 to 2025-05", (pd.Timestamp("2024-07-01"), axs[0].get_ylim()[1] * 0.93), ha="center", va="top", fontsize=7, color=MUTED)
    fig.suptitle("Figure 2. Prices and weather anomalies, 2000-2026", y=0.995, fontsize=10)
    fig.tight_layout()
    save(fig, "figure2_timeseries", "Grey band: institutional gap in DAM price reporting (nothing interpolated). Shorter gaps in 2014-15 appear as line breaks. " + src)

    # ---- Figure 3: event study -------------------------------------------------------------
    ev = reg[reg.group == "event_study"]
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.5), sharey=True)
    for a, (mm, ttl) in zip(axs, (("M5a_event_briefFE", "A. Fixed effects as specified (pre-trend test fails)"),
                                  ("M5b_event_seasonalFE", "B. Market-specific seasonality absorbed"))):
        r = ev[ev.model == mm].copy()
        r["k"] = r.term.map(lambda t: -int(t[-1]) if "lead" in t else int(t[-1]))
        r = r.sort_values("k")
        pre = r.k < 0
        a.axhline(0, color=INK, lw=0.6); a.axvline(-0.5, color=MUTED, lw=0.6, ls=":")
        for sel, col, lab in ((pre, MUTED, "Leads (placebo)"), (~pre, G_DARK, "Shock month and lags")):
            a.errorbar(r.k[sel], 100 * r.coef[sel], yerr=[100 * (r.coef - r.ci_lo)[sel], 100 * (r.ci_hi - r.coef)[sel]], fmt="o", ms=4.5,
                       color=col, ecolor=col, elinewidth=1, capsize=2, label=lab)
        pv = tests[(tests.model == mm) & tests.test.str.startswith("pre-trend")].p.iloc[0]
        a.set_title(ttl, fontsize=9); a.set_xlabel("Months since shock month")
        a.text(0.97, 0.04, f"Joint test of leads: p = {pv:.3f}\nN = {int(r.n_obs.iloc[0]):,}", transform=a.transAxes, fontsize=8, color=INK, ha="right")
        a.set_xticks(range(-3, 7))
    axs[0].set_ylabel("Effect on wholesale price, per cent"); axs[0].legend(frameon=False, loc="upper left")
    fig.suptitle("Figure 3. Event study: wholesale prices around a pre-harvest shock month", y=1.0, fontsize=10)
    fig.tight_layout()
    ev.to_csv(FIGS / "figure3_data.csv", index=False)
    save(fig, "figure3_event_study", "Points: coefficients x 100; bars: 95% confidence intervals, standard errors clustered by district (64). Panel A: market x commodity "
         "and commodity x year-month FE.\nPanel B: market x commodity x calendar-month and commodity x year-month FE. " + src)

    # ---- Figure 4: seasonality + crop calendar ----------------------------------------------
    base["dev"] = 100 * (base.ln_price - base.groupby(["mc_id", "year"]).ln_price.transform("mean"))
    full = base.groupby(["mc_id", "year"]).ym.transform("size") >= 10
    cal = {"onion": [("Planting", [11], "#d9d9d9"), ("Growth and bulbing", [12, 1, 2], "#c7e9c0"), ("Harvest", [3, 4], "#fdd0a2"), ("Marketing peak", [5, 6], "#f0f0f0")],
           "potato": [("Planting", [11], "#d9d9d9"), ("Growth and tuberisation", [12, 1], "#c7e9c0"), ("Harvest", [2, 3], "#fdd0a2"), ("Marketing peak", [4, 5], "#f0f0f0")]}
    fig, axs = plt.subplots(2, 1, figsize=(7.2, 6.2), sharex=True)
    for a, crop in zip(axs, ("onion", "potato")):
        s = base[full & (base.crop == crop)]
        data = [s.dev[s.month == mth].values for mth in range(1, 13)]
        for lab, ms, col in cal[crop]:
            for mth in ms:
                a.axvspan(mth - 0.5, mth + 0.5, color=col, lw=0, zorder=0)
        a.boxplot(data, positions=range(1, 13), widths=0.55, showfliers=False, patch_artist=True,
                  boxprops=dict(facecolor=G_MID, edgecolor=G_DARK, linewidth=0.8), medianprops=dict(color="white", linewidth=1.4),
                  whiskerprops=dict(color=G_DARK, linewidth=0.8), capprops=dict(color=G_DARK, linewidth=0.8))
        a.axhline(0, color=INK, lw=0.5)
        win = PH_WINDOW[crop]
        a.set_title(f"{'A' if crop == 'onion' else 'B'}. {crop.capitalize()} - pre-harvest exposure window: "
                    f"{'Oct-Mar' if crop == 'onion' else 'Oct-Feb'}; marketing year starts in {'April' if crop == 'onion' else 'March'}", fontsize=9)
        a.set_ylabel("Deviation from market-year mean, per cent")
        a.legend(handles=[Patch(facecolor=c, label=l) for l, _, c in cal[crop]], frameon=False, ncol=4, loc="upper center", fontsize=7)
        a.grid(axis="x", visible=False)
        lo, hi = a.get_ylim(); a.set_ylim(lo, hi + 0.22 * (hi - lo))
    axs[1].set_xticks(range(1, 13)); axs[1].set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    fig.suptitle("Figure 4. Seasonal wholesale price pattern and the rabi crop calendar", y=0.995, fontsize=10)
    fig.tight_layout()
    save(fig, "figure4_seasonality", "Boxes: inter-quartile range and median of 100 x (ln price - market x commodity x calendar-year mean) for series with at least 10 months "
         "in the year; whiskers 1.5 x IQR; outliers not drawn.\nOctober is land preparation (unshaded). " + src)

    # ---- Figure 5: spatial heterogeneity -----------------------------------------------------
    dq = pd.read_csv(MODELS / "distance_quartile_definitions.csv")
    r = reg[reg.model == "M4_distance_quartiles"].reset_index(drop=True)
    m4 = reg[reg.model == "M4_distance"].set_index("term")
    meta = json.loads((MODELS / "model_meta.json").read_text())
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    ax.axhline(0, color=INK, lw=0.6)
    xs = np.linspace(dq["min"].min() + 1, dq["max"].max(), 100)
    ax.plot(xs, 100 * (m4.loc["ph_any", "coef"] + m4.loc["ph_x_lndist", "coef"] * (np.log(xs) - meta["lnd_mean"])), color=G_LIGHT, lw=1.5,
            label="Linear-in-ln(distance) interaction (Table 3, col. 1)")
    ax.errorbar(dq["mean"], 100 * r.coef, yerr=[100 * (r.coef - r.ci_lo), 100 * (r.ci_hi - r.coef)], fmt="o", ms=5, color=G_DARK, ecolor=G_DARK,
                elinewidth=1, capsize=2, label="Distance-quartile estimates, 95% CI")
    ax.set_xlabel("Distance from district centroid to Dhaka, km"); ax.set_ylabel("Effect of one shocked month, per cent")
    ax.set_title("Figure 5. Price response to pre-harvest shocks by distance to Dhaka")
    ax.set_ylim(-1.4, 1.9)
    ax.legend(frameon=False, loc="upper left")
    pd.concat([dq, r[["term", "coef", "se_cluster", "ci_lo", "ci_hi", "p_cluster"]]], axis=1).to_csv(FIGS / "figure5_data.csv", index=False)
    save(fig, "figure5_spatial_heterogeneity", f"Interaction p-value = {m4.loc['ph_x_lndist', 'p_cluster']:.3f}. Quartiles of the 64 districts by geodesic distance; points at the "
         "quartile mean distance.\nStandard errors clustered by district. " + src)


def main():
    p = pd.read_csv(FINAL / "paper_1_panel.csv", low_memory=False)
    w = pd.read_csv(INTER / "weather_district_monthly_anomalies.csv")
    reg = pd.read_csv(MODELS / "results_registry.csv")
    tests = pd.read_csv(MODELS / "tests_registry.csv")
    tables(p, w, reg, tests)
    figures(p, w, reg, tests)
    print("tables:", len(list(TABLES.glob("*"))), "files; figures:", len(list(FIGS.glob("*"))), "files")


if __name__ == "__main__":
    main()
