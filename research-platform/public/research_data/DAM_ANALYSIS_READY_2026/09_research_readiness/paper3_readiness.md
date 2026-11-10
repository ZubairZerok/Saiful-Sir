# Paper 3 Research Readiness Assessment

**Paper Title:** *Droughts, Floods, and Spatial Agricultural Market Efficiency in Bangladesh*  
**Evaluation Target:** `PRIMARY_ANALYSIS` Dataset  
**Readiness Status:** **READY WITH CONDITIONS (High Quality Vertical & Spatial Spreads)**  

---

## 1. Econometric Requirements & Empirical Alignment

| Requirement | Empirical Status in PRIMARY_ANALYSIS | Research Verdict |
|---|---|---|
| **Vertical Price Spreads** | Both wholesale quote midpoints and retail consumer quotes available for **>3,100 observations**, allowing computation of `wholesale_retail_spread_kg`. | **EXCELLENT** — Enables direct testing of supply chain pass-through and intermediary rent extraction during shock events. |
| **Extreme Event Exposure** | 2025/2026 timeline captures severe Eastern Bangladesh / Sylhet / Feni flash flood events (August 2025) and pre-monsoon heatwaves (April–May 2026). | **EXCELLENT** — Natural quasi-experimental variation in hydrological shocks. |
| **Spatial Market Integration** | High-density co-occurring markets allow testing the Law of One Price (LOOP) and threshold vector error correction models (TVECM). | **SUFFICIENT** — Strong spatial cross-section. |

---

## 2. Recommended Estimation Strategy for Paper 3
- **Model:** Vertical and Spatial Asymmetric Price Transmission:
  $$\Delta P^{\text{retail}}_{it} = \alpha_i + \sum_{L} \beta_L^+ \Delta P^{\text{wholesale},+}_{i,t-L} + \sum_{L} \beta_L^- \Delta P^{\text{wholesale},-}_{i,t-L} + \delta \text{Flood}_{it} + \varepsilon_{it}$$
- **Identification:** Measure how physical infrastructure disruption (floods) and harvest loss (droughts/heat) impact marketing margins and spatial cointegration speeds.
