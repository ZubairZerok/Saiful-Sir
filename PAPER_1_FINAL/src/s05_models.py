"""Step 5 - Econometric estimation: model hierarchy, placebo tests, robustness.

Every estimate is appended to a long-format registry (analysis/models/results_registry.csv);
all tables, figures and documents are generated from that registry.

Estimator: OLS with high-dimensional fixed effects absorbed by alternating projections (pyfixest).
Fixed effects: market x commodity (mc_id) and commodity x year-month (cym_id).
Inference: cluster-robust (CRV1) at the district level - 64 clusters; HC1 and two-way
(district, year-month) reported alongside. Singleton FE groups are removed iteratively before
estimation so that N, FE-group and cluster counts refer to the effective sample.
"""
import json
import warnings
import numpy as np
import pandas as pd
import pyfixest as pf
from scipy import stats
from config import *

warnings.filterwarnings("ignore")
FE = ("mc_id", "cym_id")
CL = "gadm_name_2"
REG = []          # coefficient registry
TESTS = []        # joint / auxiliary tests


def drop_singletons(d, fes):
    while True:
        n = len(d)
        for fe in fes:
            d = d[d.groupby(fe)[fe].transform("size") > 1]
        if len(d) == n:
            return d


def est(model, df, y, xs, fes=FE, extra="", group="main", note="", keep=None):
    """Fit one model, store its coefficients under three variance estimators, return the fit."""
    need = [y] + list(xs)
    d = drop_singletons(df.dropna(subset=need), fes).copy()
    fml = f"{y} ~ {' + '.join(xs)}{extra} | {' + '.join(fes)}"
    fit = pf.feols(fml, d, vcov={"CRV1": CL}, fixef_rm="none")
    assert fit._N == len(d)
    b, se, p, ci = fit.coef(), fit.se(), fit.pvalue(), fit.confint()
    se_hc = pf.feols(fml, d, vcov="HC1", fixef_rm="none").se()
    se_tw = pf.feols(fml, d, vcov={"CRV1": f"{CL} + ym"}, fixef_rm="none")
    p_tw, se_tw = se_tw.pvalue(), se_tw.se()
    G = d[CL].nunique()
    for x in (keep or xs):
        if x not in b.index:       # regressor with no variation in the estimation sample (dropped as collinear)
            REG.append(dict(model=model, group=group, depvar=y, term=x, n_obs=fit._N, n_clusters=G, share_nonzero=float((d[x] != 0).mean()),
                            note="DROPPED: no variation in the estimation sample. " + note))
            continue
        REG.append(dict(model=model, group=group, depvar=y, term=x, coef=b[x], se_cluster=se[x], t=b[x] / se[x], p_cluster=p[x],
                        ci_lo=ci.loc[x].iloc[0], ci_hi=ci.loc[x].iloc[1], se_hc1=se_hc[x], se_twoway=se_tw[x], p_twoway=p_tw[x],
                        n_obs=fit._N, r2_within=fit._r2_within, r2_overall=fit._r2, n_clusters=G,
                        n_fe_market_commodity=d[fes[0]].nunique(), n_fe_time=d[fes[1]].nunique(), fe=" + ".join(fes),
                        n_markets=d.market_key.nunique(), share_nonzero=float((d[x] != 0).mean()),
                        extra_terms=extra.strip(" +"), note=note))
    fit._est_sample = d
    return fit


def wald(fit, terms, label, model):
    """Joint Wald/F test that `terms` are all zero, cluster-robust, F(q, G-1) reference distribution."""
    names = list(fit._coefnames)
    idx = [names.index(t) for t in terms]
    b = np.asarray(fit.coef())[idx]
    V = np.asarray(fit._vcov)[np.ix_(idx, idx)]
    q = len(idx)
    G = fit._est_sample[CL].nunique()
    F = float(b @ np.linalg.solve(V, b)) / q
    pval = float(stats.f.sf(F, q, G - 1))
    TESTS.append(dict(model=model, test=label, terms=";".join(terms), F=F, df1=q, df2=G - 1, p=pval))
    return F, pval


def lincom(fit, weights, label, model):
    names = list(fit._coefnames)
    w = np.zeros(len(names))
    for t, v in weights.items():
        w[names.index(t)] = v
    b = float(w @ np.asarray(fit.coef()))
    se = float(np.sqrt(w @ np.asarray(fit._vcov) @ w))
    G = fit._est_sample[CL].nunique()
    pval = float(2 * stats.t.sf(abs(b / se), G - 1))
    TESTS.append(dict(model=model, test=label, terms=json.dumps(weights), F=np.nan, df1=1, df2=G - 1, p=pval, estimate=b, se=se))
    return b, se, pval


def event_study_frame(w):
    """District x crop x month table of in-window shock indicators and their leads/lags."""
    out = []
    for crop, months in PH_WINDOW.items():
        s = w[["gadm_name_2", "ym", "month", "any_shock_15"]].sort_values(["gadm_name_2", "ym"]).copy()
        s["S"] = s.any_shock_15 * s.month.isin(months)
        g = s.groupby("gadm_name_2").S
        for k in range(1, 7):
            s[f"S_lag{k}"] = g.shift(k)              # shock k months BEFORE the price month
        for k in range(1, 4):
            s[f"S_lead{k}"] = g.shift(-k)            # shock k months AFTER the price month (placebo)
        s["S_lag0"] = s.S
        s["crop"] = crop
        out.append(s.drop(columns=["month", "any_shock_15", "S"]))
    return pd.concat(out, ignore_index=True)


def main():
    p = pd.read_csv(FINAL / "paper_1_panel.csv", low_memory=False)
    w = pd.read_csv(INTER / "weather_district_monthly_anomalies.csv")
    rng = np.random.default_rng(SEED)

    base = p[p.sample_baseline].copy()
    base["lnd_c"] = base.ln_dist_dhaka - base.ln_dist_dhaka.mean()
    base["ph_x_lndist"] = base.ph_any * base.lnd_c
    base["ph_sq"] = base.ph_any ** 2
    base["onion"] = (base.crop == "onion").astype(int)
    base["ph_x_onion"] = base.ph_any * base.onion
    for k, lab in ((1, "ph_bin1"), (2, "ph_bin2")):
        base[lab] = (base.ph_any == k).astype(int)
    base["ph_bin3p"] = (base.ph_any >= 3).astype(int)
    meta = dict(lnd_mean=float(base.ln_dist_dhaka.mean()), lnd_sd=float(base.ln_dist_dhaka.std()),
                ph_any_mean=float(base.ph_any.mean()), ph_any_sd=float(base.ph_any.std()))
    TYPES = ["ph_excess_rain", "ph_drought", "ph_heatwave", "ph_cold"]

    # ============================ MODEL HIERARCHY ======================================
    m1 = est("M1_baseline", base, "ln_price", ["ph_any"])
    est("M1_trends", base, "ln_price", ["ph_any"], extra=" + i(market_key, t_index)", note="market-specific linear trends")
    m2 = est("M2_decomposed", base, "ln_price", TYPES)
    wald(m2, TYPES, "all four shock types jointly zero", "M2_decomposed")
    est("M3a_onion", base[base.crop == "onion"], "ln_price", ["ph_any"])
    est("M3b_potato", base[base.crop == "potato"], "ln_price", ["ph_any"])
    est("M3a_onion_decomposed", base[base.crop == "onion"], "ln_price", TYPES)
    est("M3b_potato_decomposed", base[base.crop == "potato"], "ln_price", TYPES)
    m3 = est("M3_pooled_interaction", base, "ln_price", ["ph_any", "ph_x_onion"], note="H3: onion minus potato")
    lincom(m3, {"ph_any": 1, "ph_x_onion": 1}, "onion effect (potato + difference)", "M3_pooled_interaction")
    m4 = est("M4_distance", base, "ln_price", ["ph_any", "ph_x_lndist"], note="ln distance centred at sample mean")
    est("M7_quadratic", base, "ln_price", ["ph_any", "ph_sq"])
    m7b = est("M7_bins", base, "ln_price", ["ph_bin1", "ph_bin2", "ph_bin3p"], note="reference: 0 shocked months")
    wald(m7b, ["ph_bin1", "ph_bin2", "ph_bin3p"], "bins jointly zero", "M7_bins")
    est("M47_combined", base, "ln_price", ["ph_any", "ph_sq", "ph_x_lndist"])

    # distance terciles (Figure 5)
    ddist = base.drop_duplicates("gadm_name_2").set_index("gadm_name_2").distance_to_dhaka_km
    q = pd.qcut(ddist, 4, labels=False)
    base["dist_q"] = base.gadm_name_2.map(q)
    for k in range(4):
        base[f"ph_dq{k}"] = base.ph_any * (base.dist_q == k)
    est("M4_distance_quartiles", base, "ln_price", [f"ph_dq{k}" for k in range(4)], group="heterogeneity")
    dq = base.groupby("dist_q").distance_to_dhaka_km.agg(["min", "max", "mean"]).round(1)
    dq.to_csv(MODELS / "distance_quartile_definitions.csv")

    # marketing-year dynamics: effect by months since harvest
    base["msh_bin"] = base.months_since_harvest // 3
    for k in range(4):
        base[f"ph_msh{k}"] = base.ph_any * (base.msh_bin == k)
    md = est("H2_marketing_year_dynamics", base, "ln_price", [f"ph_msh{k}" for k in range(4)], group="dynamics",
             note="months since start of marketing year: 0-2, 3-5, 6-8, 9-11")
    wald(md, [f"ph_msh{k}" for k in range(4)], "all quarter-of-marketing-year effects zero", "H2_marketing_year_dynamics")

    # ============================ MODEL 5: EVENT STUDY ================================
    ev = event_study_frame(w)
    b5 = base.merge(ev, on=["gadm_name_2", "crop", "ym"], how="left", validate="m:1")
    LAGS = [f"S_lag{k}" for k in range(0, 7)]
    LEADS = [f"S_lead{k}" for k in (3, 2, 1)]
    SEAS = ("mcm_id", "cym_id")        # market x commodity x calendar-month FE nest the market x commodity FE

    def event(model, sub, fes, terms, note, extra="", group="event_study"):
        f5 = est(model, sub, "ln_price", terms, fes=fes, group=group, note=note, extra=extra)
        wald(f5, LEADS, "pre-trend: leads 1-3 jointly zero", model)
        lg = [t for t in terms if t.startswith("S_lag")]
        wald(f5, lg[:4], "lags 0-3 jointly zero", model)
        if len(lg) > 4:
            wald(f5, lg[4:], "lags 4-6 jointly zero", model)
        wald(f5, lg, "all lags jointly zero", model)
        lincom(f5, {t: 1 for t in lg}, "cumulative effect over all lags", model)

    n5 = "monthly in-window shock; lead k = shock k months AFTER the price month (placebo)"
    # (a) fixed effects exactly as in the brief -> pre-trend test FAILS
    event("M5a_event_briefFE", b5, FE, LEADS + LAGS, n5 + "; FE as in brief")
    event("M5a_event_briefFE_short", b5, FE, LEADS + LAGS[:4], n5 + "; window -3..+3; FE as in brief")
    # (b) corrected: market-specific seasonality absorbed -> pre-trend test passes
    event("M5b_event_seasonalFE", b5, SEAS, LEADS + LAGS, n5 + "; market x commodity x calendar-month FE")
    event("M5b_event_seasonalFE_short", b5, SEAS, LEADS + LAGS[:4], n5 + "; window -3..+3; seasonal FE")
    event("M5b_event_seasonalFE_onion", b5[b5.crop == "onion"], SEAS, LEADS + LAGS, n5 + "; seasonal FE")
    event("M5b_event_seasonalFE_potato", b5[b5.crop == "potato"], SEAS, LEADS + LAGS, n5 + "; seasonal FE")
    # (c) alternative correction that keeps every observation: district x crop x calendar-month FE added
    b5["dcm_id"] = b5.gadm_name_2 + "|" + b5.crop + "|" + b5.month.astype(str)
    event("M5c_event_districtSeasonFE", b5, ("mc_id", "cym_id", "dcm_id"), LEADS + LAGS, n5 + "; + district x crop x calendar-month FE")
    # (d) diagnostics of the pre-trend failure: candidates that do NOT remove it
    b5["dcs_id"] = b5.gadm_name_2 + "|" + b5.crop + "|" + b5.season.astype(str)
    dg = "event_study_diagnostic"
    event("M5d_diag_market_trends", b5, FE, LEADS + LAGS, "brief FE + market-specific linear trends", extra=" + i(market_key, t_index)", group=dg)
    event("M5d_diag_district_season_fe", b5, ("mc_id", "cym_id", "dcs_id"), LEADS + LAGS, "brief FE + district x crop x season FE", group=dg)
    event("M5d_diag_continuous_anomalies", b5, FE, LEADS + LAGS, "brief FE + contemporaneous z_temp and z_precip", extra=" + z_temp + z_precip", group=dg)

    # ============================ MODEL 6: RETAIL PASS-THROUGH =========================
    r = base[base.ln_retail.notna()].copy()
    r["ln_margin"] = r.ln_retail - r.ln_price
    est("M6_passthrough", r, "ln_retail", ["ln_price", "ph_any"], group="retail")
    est("M6_retail_reduced_form", r, "ln_retail", ["ph_any"], group="retail")
    est("M6_wholesale_same_sample", r, "ln_price", ["ph_any"], group="retail")
    est("M6_margin", r, "ln_margin", ["ph_any"], group="retail", note="ln retail - ln wholesale")

    # ============================ PLACEBO TESTS ========================================
    est("P1_lead_full", base, "ln_price", ["ph_any", "ph_any_lead"], group="placebo",
        note="next season's exposure; all marketing-year months")
    clean = base[~base.in_ph_window]
    est("P1_lead_clean", clean, "ln_price", ["ph_any", "ph_any_lead"], group="placebo",
        note="months before the next pre-harvest window opens (next season's weather entirely in the future)")
    est("P1_lead_only_clean", clean, "ln_price", ["ph_any_lead"], group="placebo", note="lead only, clean months")
    imp = p[p.sample_placebo_imported].copy()
    est("P2_imported_all", imp, "ln_price", ["ph_any"], group="placebo", note="imported onion (832) + imported potato (21014)")
    est("P2_imported_onion_832", imp[imp.commodity_id == 832], "ln_price", ["ph_any"], group="placebo")
    try:
        est("P2_imported_potato_21014", imp[imp.commodity_id == 21014], "ln_price", ["ph_any"], group="placebo")
    except Exception as e:
        TESTS.append(dict(model="P2_imported_potato_21014", test="not estimable", terms=repr(e)[:200],
                          n_obs=int((imp.commodity_id == 21014).sum())))
    # imported onion vs local onion in the same market-months (differential response)
    both = p[p.tier_primary & (p.crop == "onion") & p.ph_any.notna() & p.ln_price.notna()].copy()
    both["ph_x_imported"] = both.ph_any * both.imported
    est("P2_onion_imported_differential", both, "ln_price", ["ph_any", "ph_x_imported"], group="placebo")
    est("P3_off_window", base, "ln_price", ["ph_any_off"], group="placebo", note="shocks in Apr-Sep before planting (crop not in the ground)")
    est("P3_off_window_joint", base, "ln_price", ["ph_any", "ph_any_off"], group="placebo")

    # randomisation inference: (a) reassign seasons (same permutation for all districts), (b) reassign districts
    expo = pd.read_csv(INTER / "preharvest_exposure_district_crop_season.csv")[["gadm_name_2", "crop", "season", "ph_any"]]
    d0 = drop_singletons(base, FE)
    b_true = float(m1.coef()["ph_any"])
    ri = []
    seasons = np.sort(expo.season.unique()); dists = np.sort(expo.gadm_name_2.unique())
    for kind in ("season_shuffle", "district_shuffle"):
        for rep in range(500):
            e = expo.copy()
            if kind == "season_shuffle":
                e["season"] = e.season.map(dict(zip(seasons, rng.permutation(seasons))))
            else:
                e["gadm_name_2"] = e.gadm_name_2.map(dict(zip(dists, rng.permutation(dists))))
            x = d0[["gadm_name_2", "crop", "season"]].merge(e, on=["gadm_name_2", "crop", "season"], how="left").ph_any.values
            dd = d0.assign(ph_perm=x).dropna(subset=["ph_perm"])
            ri.append(dict(kind=kind, rep=rep, coef=float(pf.feols("ln_price ~ ph_perm | mc_id + cym_id", dd, vcov="iid", fixef_rm="none").coef()["ph_perm"])))
    ri = pd.DataFrame(ri)
    ri.to_csv(ROB_PLA / "randomization_inference_draws.csv", index=False)
    for kind, s in ri.groupby("kind"):
        TESTS.append(dict(model="P4_randomization_inference", test=kind, terms="ph_any", estimate=b_true, se=float(s.coef.std()),
                          p=float((np.sum(np.abs(s.coef) >= abs(b_true)) + 1) / (len(s) + 1)), df1=len(s),
                          F=float(s.coef.mean())))

    # ============================ ROBUSTNESS ===========================================
    R = "robustness"
    est("R01_alt_price_dam_avg", base, "ln_price_dam_avg", ["ph_any"], group=R, note="DAM headline average (identical to midpoint before 2025)")
    est("R02_strict_tier", base[base.tier_strict], "ln_price", ["ph_any"], group=R, note="STRICT_SENSITIVITY: runs >= 6 consecutive months")
    est("R03_threshold_1.0sd", base, "ln_price", ["ph_any_10"], group=R)
    est("R04_threshold_2.0sd", base, "ln_price", ["ph_any_20"], group=R)
    est("R05_chirps_rainfall", base, "ln_price", ["ph_any_chirps"], group=R, note="CHIRPS rain shocks + ERA5-Land temperature shocks")
    est("R05b_rain_only_era5", base, "ln_price", ["ph_excess_rain", "ph_drought"], group=R)
    est("R05c_rain_only_chirps", base, "ln_price", ["ph_excess_rain_chirps", "ph_drought_chirps"], group=R)
    allv = p[p.tier_primary & p.ph_any.notna() & p.ln_price.notna()]
    est("R06_incl_imported", allv, "ln_price", ["ph_any"], group=R)
    est("R07_spei", base, "ln_price", ["ph_any_spei"], group=R, note="SPEI-1 moisture shocks (|SPEI|>1.5) + temperature shocks")
    est("R07b_spei_decomposed", base, "ln_price", ["ph_wet_spei", "ph_dry_spei", "ph_heatwave", "ph_cold"], group=R)
    est("R08_percentile_shocks", base, "ln_price", ["ph_any_pct"], group=R, note="outside 10-90th percentile of 1991-2020")
    est("R09_max_abs_z", base, "ln_price", ["ph_max_abs_z_precip", "ph_max_abs_z_temp"], group=R, note="Option B")
    est("R10_mean_z", base, "ln_price", ["ph_mean_z_precip", "ph_mean_z_temp"], group=R, note="continuous window-mean anomalies")
    # winsorising instead of trimming the cross-sectional outliers
    wz = p[p.wholesale_basic_ok & ~p.imported & p.ph_any.notna() & (p.price_wholesale_raw_mid_kg > 0)].copy()
    g = wz.groupby(["commodity_id", "year"]).price_wholesale_raw_mid_kg
    wz["ln_price_w"] = np.log(wz.price_wholesale_raw_mid_kg.clip(g.transform(lambda s: s.quantile(.01)), g.transform(lambda s: s.quantile(.99))))
    est("R11_winsorized", wz, "ln_price_w", ["ph_any"], group=R, note="no outlier trimming; prices winsorised at p1/p99 within commodity-year")
    est("R12_level_iqr_trim", base[~base.wholesale_flag_level_iqr], "ln_price", ["ph_any"], group=R, note="literal pooled 3xIQR rule applied in addition")
    near = base.ym.between("2023-02", "2023-07") | base.ym.between("2025-06", "2025-11")
    est("R13_excl_near_gap", base[~near], "ln_price", ["ph_any"], group=R, note="drops 6 months on each side of the 2023-08..2025-05 gap")
    est("R14_historical_only", base[base.source == "dam_web_historical"], "ln_price", ["ph_any"], group=R, note="2000-2023 web-portal segment")
    est("R14b_api_only", base[base.source == "moa_api"], "ln_price", ["ph_any"], group=R, note="2025-2026 API segment")
    est("R15_excl_sweet_potato", base[base.commodity_id != 948], "ln_price", ["ph_any"], group=R)
    est("R16_lagged_season", base, "ln_price", ["ph_any", "ph_any_lag"], group=R, note="adds previous season's exposure")
    # first differences (consecutive months only)
    fd = base.sort_values(["mc_id", "t_index"]).copy()
    gb = fd.groupby("mc_id")
    cons = gb.t_index.diff() == 1
    fd["d_ln_price"] = gb.ln_price.diff().where(cons)
    fd["d_ph_any"] = gb.ph_any.diff().where(cons)
    est("R17_first_difference", fd, "d_ln_price", ["d_ph_any"], fes=("gadm_name_2", "cym_id"), group=R,
        note="month-to-month differences; FE: district + commodity x month")
    # macro controls instead of commodity x month FE
    ctl = pd.read_csv(INTER / "controls_annual.csv")
    mc = base.merge(ctl, on="year", how="left")
    mc["cmonth_id"] = mc.commodity_id.astype(str) + "|" + mc.month.astype(str)
    for c in mc.commodity_id.unique():
        mc[f"tr_{c}"] = mc.t_index * (mc.commodity_id == c)
    tr = " + " + " + ".join(f"tr_{c}" for c in sorted(mc.commodity_id.unique()))
    est("R18_macro_controls", mc, "ln_price", ["ph_any", "ln_exchange_rate", "ln_cpi"], fes=("mc_id", "cmonth_id"), extra=tr, group=R,
        note="commodity x calendar-month FE + commodity trends + annual macro controls; uses national time-series variation")

    est("R19_seasonal_fe", base, "ln_price", ["ph_any"], fes=SEAS, group=R, note="market x commodity x calendar-month FE")

    # ---- battery for the decomposed model (the heat result) ------------------------------------------
    Hh = "heat_battery"
    est("H01_trends", base, "ln_price", TYPES, extra=" + i(market_key, t_index)", group=Hh, note="market-specific linear trends")
    est("H02_seasonal_fe", base, "ln_price", TYPES, fes=SEAS, group=Hh, note="market x commodity x calendar-month FE")
    est("H03_strict", base[base.tier_strict], "ln_price", TYPES, group=Hh)
    est("H04_threshold_1.0sd", base, "ln_price", [t + "_10" for t in TYPES], group=Hh)
    est("H05_threshold_2.0sd", base, "ln_price", [t + "_20" for t in TYPES], group=Hh)
    est("H06_lead_placebo_clean", clean, "ln_price", TYPES + [t + "_lead" for t in TYPES], group=Hh,
        note="adds next season's type-specific exposure; months before the next window opens")
    est("H07_imported_onion_placebo", imp[imp.commodity_id == 832], "ln_price", TYPES, group=Hh)
    est("H08_historical_only", base[base.source == "dam_web_historical"], "ln_price", TYPES, group=Hh)
    est("H09_excl_near_gap", base[~near], "ln_price", TYPES, group=Hh)
    est("H10_heat_x_distance", base.assign(heat_x_lndist=base.ph_heatwave * base.lnd_c), "ln_price", TYPES + ["heat_x_lndist"], group=Hh)

    reg = pd.DataFrame(REG)
    reg.to_csv(MODELS / "results_registry.csv", index=False)
    pd.DataFrame(TESTS).to_csv(MODELS / "tests_registry.csv", index=False)
    reg[reg.group.isin(["robustness", "heat_battery"])].to_csv(ROB_ALT / "robustness_estimates.csv", index=False)
    reg[reg.group == "placebo"].to_csv(ROB_PLA / "placebo_estimates.csv", index=False)
    (MODELS / "model_meta.json").write_text(json.dumps(meta, indent=2))
    pd.set_option("display.width", 220); pd.set_option("display.max_rows", 300)
    print(reg[["model", "term", "coef", "se_cluster", "p_cluster", "p_twoway", "n_obs", "r2_within", "n_clusters", "share_nonzero"]].round(4).to_string())
    print(pd.DataFrame(TESTS).round(4).to_string())


if __name__ == "__main__":
    main()
