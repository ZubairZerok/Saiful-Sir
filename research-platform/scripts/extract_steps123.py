import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def get_text(docx_path):
    if not os.path.exists(docx_path):
        return []
    with zipfile.ZipFile(docx_path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        return [
            ''.join(t.text for t in p.iterfind('.//w:t', ns) if t.text)
            for p in tree.iterfind('.//w:p', ns)
            if ''.join(t.text for t in p.iterfind('.//w:t', ns) if t.text).strip()
        ]

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Step123'))
p1 = get_text(os.path.join(base_dir, 'Overall_p1.docx'))
p2 = get_text(os.path.join(base_dir, 'Overall_P2.docx'))
p3 = get_text(os.path.join(base_dir, 'Overall_p3.docx'))

# Step 1 Markdown
step1_md = """# Step 1: Research Questions & Hypotheses (Papers 1, 2, and 3)

## Overview & Thematic Architecture
This research program investigates the empirical microeconomics of weather shocks, spatial agricultural market integration, and price transmission in Bangladesh across three complementary papers.

---

## Paper 1: Pre-Harvest Weather Shocks & Agricultural Prices
**Title:** *Do Pre-Harvest Weather Shocks Affect Agricultural Prices? Evidence from Bangladesh*

### Main Research Question
- **RQ1:** Do pre-harvest weather shocks significantly affect agricultural market prices before the corresponding harvest period in Bangladesh?

### Secondary Research Questions
- **RQ1a:** How quickly do prices respond following a pre-harvest weather shock?
- **RQ1b:** Does the magnitude of the price response vary according to the severity of the weather shock?
- **RQ1c:** Does the pre-harvest price response differ between onion and potato?

### Hypotheses
- **Primary Hypothesis (H1):** Pre-harvest adverse weather shocks significantly increase agricultural market prices before harvest.
- **Null Hypothesis (H0):** Pre-harvest adverse weather shocks have no significant effect on agricultural market prices before harvest.
- **Sub-Hypothesis (H1a):** Larger pre-harvest weather anomalies generate larger price responses.
- **Sub-Hypothesis (H1b):** The price response occurs with a measurable lag following the weather shock.

---

## Paper 2: Weather Shocks & Spatial Price Dispersion
**Title:** *Weather Shocks and Spatial Price Dispersion in Agricultural Markets: Evidence from Bangladesh*

### Main Research Question
- **RQ2:** Do localized weather shocks significantly increase spatial price dispersion between agricultural markets in Bangladesh?

### Secondary Research Questions
- **RQ2a:** How quickly does spatial price dispersion increase following a localized weather shock?
- **RQ2b:** Does the magnitude of price dispersion vary according to the severity of the weather shock?
- **RQ2c:** Does the speed of market convergence differ according to the distance or travel cost between market pairs?

### Hypotheses
- **Primary Hypothesis (H2):** Localized adverse weather shocks significantly increase spatial price dispersion between agricultural markets.
- **Null Hypothesis (H0):** Localized adverse weather shocks have no significant effect on spatial price dispersion between agricultural markets.
- **Sub-Hypothesis (H2a):** More severe localized weather shocks generate larger increases in spatial price dispersion.
- **Sub-Hypothesis (H2b):** Market pairs with greater distance or travel costs experience slower convergence following a weather shock.

---

## Paper 3: Asymmetric Climate Shocks & Market Efficiency
**Title:** *Droughts, Floods, and Spatial Agricultural Market Efficiency in Bangladesh*

### Main Research Question
- **RQ3:** Do droughts and floods have significantly different effects on spatial agricultural market efficiency in Bangladesh?

### Secondary Research Questions
- **RQ3a:** Does the magnitude of market-efficiency loss vary between drought and flood shocks?
- **RQ3b:** How quickly do agricultural markets recover following drought and flood shocks?
- **RQ3c:** Does the recovery period differ between drought and flood shocks?

### Hypotheses
- **Primary Hypothesis (H3):** Droughts and floods have significantly asymmetric effects on spatial agricultural market efficiency.
- **Null Hypothesis (H0):** Droughts and floods have no significant difference in their effects on spatial agricultural market efficiency.
- **Sub-Hypothesis (H3a):** Flood shocks generate greater reductions in spatial market efficiency than drought shocks.
- **Sub-Hypothesis (H3b):** Market recovery takes longer following flood shocks than drought shocks.

---

## Cross-Paper Comparison Matrix

| Evaluation Dimension | Paper 1: Pre-Harvest Price Response | Paper 2: Spatial Price Dispersion | Paper 3: Market Efficiency (Droughts vs Floods) |
|---|---|---|---|
| **Core Phenomenon** | Temporal forward-looking price response | Spatial Law of One Price (LOP) violation | Structural asymmetry in climate shock recovery |
| **Unit of Analysis** | Market x Month (i, t) | Bilateral Market Pair x Month (i, j, t) | Market x Month (i, t) & Wholesale-Retail Pairs |
| **Primary Outcome** | Wholesale Price ln(P_it) | Pairwise Price Gap \|ln(P_it) - ln(P_jt)\| | Margin Spread (P_retail - P_wholesale) |
| **Key Climate Variable** | Pre-harvest growing season weather shocks | Inter-market weather differentials (Delta W_ijt) | Extreme flood inundation vs SPEI drought |
| **Identification** | Fixed effects panel with crop growth windows | Dyadic fixed effects & road network distance | Event-study difference-in-differences |
"""

with open(os.path.join(base_dir, 'step1_research_questions_and_hypotheses.md'), 'w', encoding='utf-8') as f:
    f.write(step1_md)

# Step 2 Markdown
step2_text = '\n\n'.join(p1[13:592])
step2_md = f"""# Step 2: Comprehensive Literature Review & Methodology Matrix

## 1. Executive Literature Map
The econometric literature on weather anomalies and agricultural market prices is structured across four primary analytical layers:

1. **Macro Climate-Economy Literature:** Broad cross-country and multi-sector econometric estimation of weather shocks on aggregate GDP, agricultural output, and inflation (Dell, Jones & Olken 2014; Carleton & Hsiang 2016).
2. **Pre-Harvest Expectations & Timing Channel:** Moving beyond post-harvest supply shocks to demonstrate that forward-looking market participants adjust prices during the pre-harvest crop growing window before harvest failure materializes (*Letta, Montalbano & Pierre 2022* in India; *Brown & Kshirsagar 2015*).
3. **Spatial Market Integration & Law of One Price:** Econometric models of spatial arbitrage, transportation costs, trade barriers, and price dispersion across subnational market networks (*Fackler & Goodwin 2001*; *Aker 2010*).
4. **Bangladesh Agricultural & Cold Storage Context:** Empirical studies on onion and potato production volatility, cold storage infrastructure capacity, seasonal price spreads, and post-harvest storage liquidation (*BBS, DAM, World Bank*).

---

## 2. Synthesized Literature Review & Methodological Framework

{step2_text}
"""

with open(os.path.join(base_dir, 'step2_literature_review_and_matrix.md'), 'w', encoding='utf-8') as f:
    f.write(step2_md)

# Step 3 Markdown
step3_text = '\n\n'.join(p1[592:])
step3_md = f"""# Step 3: Data Source Identification & Variable Registry

## 1. Master Data Source Inventory
To execute the empirical estimation across Papers 1, 2, and 3, a multi-source data infrastructure has been inventoried and mapped:

| Source Category | Primary Provider | Spatial Resolution | Temporal Frequency | Access Status | Role in Research |
|---|---|---|---|---|---|
| **Agricultural Prices** | Department of Agricultural Marketing (DAM) | 117 Local Markets, 64 Districts | Daily / Monthly | Extracted & Verified | Primary Outcome Variables |
| **Gridded Weather (ERA5-Land)** | ECMWF / Copernicus CDS | 0.1 deg x 0.1 deg (~9 km grid) | Hourly -> Monthly | Public Open Access | Temperature, Heatwaves, Pre-harvest Rain |
| **Precipitation (CHIRPS)** | UCSB Climate Hazards Group | 0.05 deg x 0.05 deg (~5 km grid) | Daily -> Monthly | Public Open Access | High-resolution Rainfall Anomalies |
| **Station Meteorology** | Bangladesh Meteorological Dept (BMD) | 35 Synoptic Weather Stations | Daily | Official Request | Validation & Ground Truth |
| **Road Network & Distance** | LGED GIS / OpenStreetMap | Road Segments & Centroids | Static / Updated | GIS Layers Verified | Bilateral Market Distance Matrices |
| **Crop Production Geography** | Bangladesh Bureau of Statistics (BBS) | District / Upazila | Annual / Census | Official Reports | Crop Area Weights (Onion / Potato) |
| **Cold Storage Facilities** | DAM Cold Storage Reports | District / Facility Level | Annual (2022-2026) | Verified Reports | Potato Supply Buffering Mechanism |
| **Customs & Trade Imports** | Bangladesh Customs / NBR | National (HS 070310) | Monthly / Annual | Official Statistics | Onion Import Shock Controls |
| **Macro & Exchange Rates** | Bangladesh Bank Open Data | National | Monthly / Daily | Verified Public API | USD/BDT Exchange Rate & Inflation |

---

## 2. Detailed Variable-Level Registry & Field Specifications

{step3_text}
"""

with open(os.path.join(base_dir, 'step3_data_sources_and_registry.md'), 'w', encoding='utf-8') as f:
    f.write(step3_md)

print("Successfully generated Step 1, 2, and 3 Markdown files!")
