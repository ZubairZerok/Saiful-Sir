# Paper 1 Research Readiness Assessment

**Paper Title:** *Do Pre-Harvest Weather Shocks Affect Agricultural Prices? Evidence from Bangladesh*  
**Evaluation Target:** `PRIMARY_ANALYSIS` Dataset  
**Target Commodities:** Onion (Local, Imported, New) and Potato (Local, HYV White, HYV Red)  
**Readiness Status:** **READY WITH CONDITIONS (High Spatial Breadth, 15-Month Temporal Span)**  

---

## 1. Econometric Requirements & Empirical Alignment

| Requirement | Empirical Status in PRIMARY_ANALYSIS | Research Verdict |
|---|---|---|
| **Commodity Coverage** | Onion (Local: 902 obs, 97 mkts; New: 265 obs, 29 mkts; Imported: 151 obs, 50 mkts). Potato (HYV White New: 660 obs, 82 mkts; HYV Red: 449 obs, 52 mkts; Local: 411 obs, 54 mkts). | **EXCELLENT** — Complete coverage of primary production staples. |
| **Spatial Variation** | 116 active markets across all 8 administrative divisions of Bangladesh. | **EXCELLENT** — Robust cross-sectional exposure to localized weather events. |
| **Temporal Span** | 15 continuous calendar months (June 2025 – August 2026). | **CONDITIONAL** — Ideal for high-frequency (monthly) price response and within-year seasonal shock exposure; cannot estimate multi-year decadal climatic trends. |
| **Pre-Harvest Windows** | Spans full Rabi pre-harvest growing windows (October–December 2025) and harvest arrival periods (January–April 2026). | **SUFFICIENT** — Complete coverage of 2025/2026 cropping cycle. |
| **Unit Consistency** | Fully standardized BDT/kg prices for both raw midpoints and official averages. | **VERIFIED** — Zero unit ambiguity. |

---

## 2. Recommended Estimation Strategy for Paper 1
Given the 15-month panel structure ($N = 116$ markets, $T = 15$ months):
- **Model:** High-frequency Fixed Effects Panel:
  $$\ln(P_{it}) = \alpha_i + \gamma_t + \sum_{k=1}^3 \beta_k \text{WeatherShock}_{i,t-k} + \mathbf{X}_{it}'\boldsymbol{\delta} + \varepsilon_{it}$$
- **Identification:** Exploit spatial heterogeneity in temperature anomalies, excess rainfall days, and standardized precipitation evapotranspiration indices (SPEI) during pre-harvest vegetative and tuber/bulb formation phases.
