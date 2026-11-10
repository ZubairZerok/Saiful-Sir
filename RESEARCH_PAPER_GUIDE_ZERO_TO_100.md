# 📖 The Complete Guide to Writing an Empirical Research Paper
## From Absolute Zero to Publication — A Baby-Step Walkthrough

*Using Your Paper as the Running Example:*
*"Do Pre-Harvest Weather Shocks Affect Agricultural Prices? Evidence from Bangladesh"*

---

## Table of Contents

1. [What IS a Research Paper?](#chapter-1-what-is-a-research-paper)
2. [The Big Picture: Anatomy of a Paper](#chapter-2-the-big-picture-anatomy-of-a-paper)
3. [Step 1: Choosing a Research Question](#chapter-3-choosing-a-research-question)
4. [Step 2: Forming Hypotheses](#chapter-4-forming-hypotheses)
5. [Step 3: Literature Review](#chapter-5-literature-review)
6. [Step 4: Identifying Data Sources](#chapter-6-identifying-data-sources)
7. [Step 5: Data Collection](#chapter-7-data-collection)
8. [Step 6: Designing Your Variables](#chapter-8-designing-your-variables)
9. [Step 7: Data Cleaning](#chapter-9-data-cleaning)
10. [Step 8: Descriptive Statistics](#chapter-10-descriptive-statistics)
11. [Step 9: Econometric Methodology](#chapter-11-econometric-methodology)
12. [Step 10: Running the Analysis](#chapter-12-running-the-analysis)
13. [Step 11: Robustness & Sensitivity](#chapter-13-robustness-and-sensitivity)
14. [Step 12: Tables & Figures](#chapter-14-tables-and-figures)
15. [Step 13: Writing the Paper](#chapter-15-writing-the-paper)
16. [Step 14: The Abstract](#chapter-16-the-abstract)
17. [Step 15: Submission & Peer Review](#chapter-17-submission-and-peer-review)
18. [Glossary of Terms](#glossary)
19. [Common Mistakes to Avoid](#common-mistakes)

---

## Chapter 1: What IS a Research Paper?

### The Simplest Explanation

A research paper is a **structured argument backed by evidence**. You're saying:

> "I noticed something interesting about the world. I collected data to test whether my idea is right. Here's what I found."

That's it. Everything else is just making this argument rigorous, transparent, and convincing.

### Why Does It Matter?

Research papers are how humanity builds knowledge. Each paper is a brick in a wall. Your paper asks: *"When bad weather hits Bangladesh before crops are harvested, do food prices go up?"* That question matters because:

- **700 million people** in South Asia depend on agriculture
- Climate change is making weather more extreme
- If we KNOW prices spike after bad weather, governments can prepare (release reserves, adjust imports, warn farmers)

### The Two Types of Claims

1. **Correlation:** "When it rains a lot, prices tend to go up" — things happen together
2. **Causation:** "The rain CAUSED prices to go up" — one thing made the other happen

Your paper tries to get as close to **causation** as possible. This is the hard part.

---

## Chapter 2: The Big Picture — Anatomy of a Paper

Every empirical economics paper follows roughly this structure:

```
┌─────────────────────────────────────┐
│           ABSTRACT                  │  ← 250-word summary of EVERYTHING
├─────────────────────────────────────┤
│     1. INTRODUCTION                 │  ← Why this matters, what you do, what you find
├─────────────────────────────────────┤
│     2. LITERATURE REVIEW            │  ← What others have done before you
├─────────────────────────────────────┤
│     3. DATA                         │  ← Where your data comes from, what it looks like
├─────────────────────────────────────┤
│     4. METHODOLOGY                  │  ← Your statistical approach (the math)
├─────────────────────────────────────┤
│     5. RESULTS                      │  ← What you found
├─────────────────────────────────────┤
│     6. ROBUSTNESS CHECKS            │  ← Proving your results aren't flukes
├─────────────────────────────────────┤
│     7. DISCUSSION                   │  ← What it means, policy implications
├─────────────────────────────────────┤
│     8. CONCLUSION                   │  ← Summary and future work
├─────────────────────────────────────┤
│     REFERENCES                      │  ← Papers you cited
├─────────────────────────────────────┤
│     APPENDIX                        │  ← Extra tables, details
└─────────────────────────────────────┘
```

Think of it like building a house:
- **Introduction** = the blueprint (here's what we're building and why)
- **Literature Review** = the neighborhood survey (what buildings already exist?)
- **Data** = the raw materials (bricks, cement, wood)
- **Methodology** = the construction plan (how we'll assemble the materials)
- **Results** = the finished house (what we built)
- **Robustness** = the safety inspection (is this house sturdy?)
- **Discussion** = the real estate assessment (what is this house worth to the world?)

---

## Chapter 3: Choosing a Research Question

### What Makes a GOOD Research Question?

A good research question has four qualities (remember **FINER**):

1. **Feasible** — Can you actually answer it with available data and methods?
2. **Interesting** — Does anyone care about the answer?
3. **Novel** — Has nobody answered it before (or not in this way)?
4. **Ethical** — Can you do this research without causing harm?
5. **Relevant** — Does the answer matter for policy, theory, or real people?

### Your Research Question

> **"Do pre-harvest weather shocks significantly affect agricultural commodity prices in Bangladesh?"**

Let's check:
- ✅ **Feasible:** Bangladesh's DAM publishes price data. ERA5 provides weather data. Both are accessible.
- ✅ **Interesting:** Climate change + food security is arguably THE defining issue of our century.
- ✅ **Novel:** Letta et al. (2022) did this for India, but nobody has done it for Bangladesh with this granularity of market-level data.
- ✅ **Ethical:** No human subjects, just publicly available price and weather records.
- ✅ **Relevant:** Bangladesh is one of the world's most climate-vulnerable countries.

### How to Refine a Vague Idea into a Research Question

Most people start with a vague thought like: *"I wonder if weather affects food prices."*

The refinement process goes like this:

```
Vague: "Weather affects food prices"
    ↓ What kind of weather? → Bad weather (shocks, extremes)
    ↓ What kind of food? → Agricultural commodities (onion, potato)
    ↓ Where? → Bangladesh (data available, climate vulnerable)
    ↓ When does weather matter? → BEFORE harvest (pre-harvest window)
    ↓ What's the mechanism? → Expected supply reduction → price increase
    ↓ Can I test this causally? → Yes, with panel fixed effects

Precise: "Do pre-harvest weather shocks significantly affect 
          agricultural commodity prices in Bangladesh?"
```

### Sub-Questions: Breaking It Down

Your main question is big. Break it into testable pieces:

1. **Timing:** How quickly do prices respond? (Event-study analysis)
2. **Severity:** Does worse weather → bigger price increase? (Non-linearity test)
3. **Heterogeneity:** Do onion and potato respond differently? (Subsample analysis)
4. **Geography:** Do remote markets respond more? (Spatial friction test)

Each sub-question becomes a separate regression model.

---

## Chapter 4: Forming Hypotheses

### What IS a Hypothesis?

A hypothesis is a **testable prediction**. It's your educated guess about what you'll find, stated in a way that data can either support or reject it.

### The Null vs. Alternative Hypothesis

In statistics, we always test AGAINST a "null hypothesis" (H₀):

- **H₀ (Null):** "Pre-harvest weather shocks have NO effect on prices" (β = 0)
- **H₁ (Alternative):** "Pre-harvest weather shocks DO affect prices" (β ≠ 0)

You're trying to REJECT H₀. If your data shows the relationship is strong enough that it's extremely unlikely to have happened by random chance, you reject H₀ and accept H₁.

### Your Paper's Hypotheses

| Hypothesis | What You're Testing | How You'll Test It |
|-----------|--------------------|--------------------|
| H1: Weather shocks raise prices | Bad weather before harvest → higher prices | Main regression coefficient β > 0 and statistically significant |
| H2: Effects are short-lived | Price response emerges in 1-3 months, fades by 4-6 months | Event-study: coefficients on lags 1-3 significant, lags 4+ insignificant |
| H3: Onion > Potato response | Onion prices respond more because onions can't be stored as well as potatoes | Subsample regressions: onion β > potato β |
| H4: Remote markets respond more | Markets far from Dhaka have bigger price jumps (less import access) | Interaction term: shock × distance > 0 |

### What Makes the Hypothesis Testable?

Notice each hypothesis maps to a specific statistical test. If you can't write down what regression to run, your hypothesis isn't testable yet.

---

## Chapter 5: Literature Review

### Why Bother Reading Other Papers?

Imagine building a new smartphone without knowing that smartphones already exist. You'd waste years reinventing the touchscreen. The literature review tells you:

1. **What's been done** → So you don't repeat it
2. **What hasn't been done** → Your contribution (the "gap")
3. **What methods work** → So you use proven approaches
4. **What to compare against** → Your benchmark for interpreting results

### How to Structure a Literature Review

Think of it as **concentric circles** (zooming in):

```
Layer 1: BROAD — Climate change and agriculture (global studies)
    ↓
Layer 2: FOCUSED — Weather shocks and food prices (country studies)
    ↓
Layer 3: SPECIFIC — Pre-harvest shocks and price transmission (the exact mechanism)
    ↓
Layer 4: YOUR CONTEXT — Bangladesh agricultural markets (your setting)
```

### Your Literature Review Structure

1. **Macro climate-economy nexus** — Dell, Jones & Olken (2014) showed that weather affects entire economies. Burke & Lobell (2017) showed crop yield impacts.

2. **Pre-harvest weather and prices** — Letta, Montalbano & Pierre (2022) is your CLOSEST comparison. They studied India and found that pre-harvest temperature shocks increase staple food prices. YOUR paper does this for Bangladesh with different crops and more granular market data.

3. **Spatial market integration** — How do price shocks spread across markets? Do remote markets behave differently from central markets?

4. **Bangladesh context** — What do we know about Bangladeshi agricultural markets specifically? Government interventions, import policies, cold storage networks.

### The "Gap" — Your Contribution

After reviewing the literature, you identify what's MISSING:

> "While Letta et al. (2022) studied weather-price relationships in India using state-level data, NO study has examined this relationship in Bangladesh using market-level data with crop-calendar-specific pre-harvest windows for onion and potato — two commodities that together represent a significant share of Bangladesh's vegetable expenditure."

This gap is your reason for existing.

---

## Chapter 6: Identifying Data Sources

### What Data Do You Need?

Think about your regression equation. Each variable needs a data source:

```
ln(Price) = β · Weather_Shock + Fixed_Effects + Controls + Error
   ↑              ↑                ↑              ↑
   DAM data    ERA5/CHIRPS     Panel structure   BBS, Bangladesh Bank, etc.
```

### Your Data Sources

| What You Need | Why | Source | Format |
|--------------|-----|--------|--------|
| Daily wholesale/retail prices | Dependent variable (Y) | DAM (Department of Agricultural Marketing) | API + Web scraping |
| Temperature (monthly, by district) | Weather shock construction | ERA5-Land (ECMWF/Copernicus) | NetCDF gridded → CSV |
| Rainfall (monthly, by district) | Weather shock construction | ERA5-Land + CHIRPS (cross-validation) | NetCDF gridded → CSV |
| District boundary polygons | Aggregating gridded weather to districts | GADM / LGED GIS | GeoJSON/Shapefile |
| Crop calendars | Defining "pre-harvest" window | BAMIS (Bangladesh Agricultural MIS) | Manual lookup |
| District crop production | Production weights | BBS (Bangladesh Bureau of Statistics) | PDF → digitized CSV |
| Onion import volumes | Control variable | NBR Customs (HS 070310) | Monthly reports |
| Exchange rate (BDT/USD) | Control variable | Bangladesh Bank | Monthly CSV |
| CPI (food sub-index) | Control variable (inflation) | BBS | Monthly reports |
| Cold storage capacity | Control variable (potato only) | DAM Cold Storage Reports | Annual reports |

### Primary vs. Secondary Data

- **Primary data** = You collected it yourself (surveys, experiments). Your DAM API extraction is essentially primary data collection.
- **Secondary data** = Someone else collected it and you're using it. ERA5, BBS, Bangladesh Bank data are all secondary.

Most economics research uses secondary data. There's no shame in that — the value is in your ANALYSIS, not just data collection.

---

## Chapter 7: Data Collection

### The Practical Reality

Data collection is usually the most TIME-CONSUMING part of research. It involves:

1. **Finding the data** — Where does it live? Is it accessible?
2. **Extracting it** — APIs, web scraping, manual digitization
3. **Organizing it** — Consistent formats, naming conventions
4. **Documenting it** — Where did each number come from?

### Your Data Collection (What Was Done)

#### A. DAM Price Data Extraction

Two methods were used:

**Method 1: API Extraction** (Modern data, 2025-2026)
```python
# The script dam_11_commodity_extractor_FINAL.py does this:
# 1. Authenticates with DAM's backend API (Bearer token)
# 2. Iterates over 11 commodity IDs × 117 market IDs
# 3. Extracts daily price observations
# 4. Saves raw JSON + clean CSV per commodity per market
# Result: 3,348 observations covering June 2025 – August 2026
```

**Method 2: Historical Expansion** (Historical data, 2000-2024)
```python
# The scripts in DAM_EXPANDED_2026/ do this:
# 1. Scrape the DAM historical web portal (2000-2024)
# 2. Pull from modern MOA REST API (2025-2026)
# 3. Harmonize formats into a single master file
# Result: 126,932 observations covering 2000-2026 across 324 markets
```

#### B. Weather Data Collection

Weather data comes from satellite/reanalysis products — NOT from physical weather stations (which have gaps). ERA5-Land is a "reanalysis" — it combines satellite observations with atmospheric physics models to create a complete gridded dataset with no gaps.

**The process:**
```
1. Define Bangladesh bounding box: 20.5°N–26.7°N, 88.0°E–92.7°E
2. Download ERA5-Land monthly data for this box (temperature + precipitation)
3. Load Bangladesh district boundary polygons (64 districts)
4. For each district: compute area-weighted average of all grid cells inside the polygon
5. Result: One temperature and one precipitation value per district per month
```

### Data Collection Best Practices

- **Always save raw data separately** — Never modify your original files
- **Document your extraction code** — Someone else should be able to run it
- **Check for rate limits** — APIs often limit how fast you can download
- **Verify completeness** — Did you get data for ALL markets? ALL months? ALL commodities?
- **Create checksums** — SHA-256 hashes prove your data hasn't been tampered with

---

## Chapter 8: Designing Your Variables

### What IS a Variable?

A variable is a **measurable characteristic that changes** across your observations. In your data:

- Each observation = one **market** selling one **commodity** on one **date**
- Variables describe that observation: what was the price? what was the weather?

### Types of Variables

| Type | What It Is | Your Examples |
|------|-----------|---------------|
| **Dependent Variable (Y)** | What you're trying to explain | `ln(price_wholesale_raw_mid_kg)` — the natural log of the wholesale price |
| **Independent Variable (X)** | What you think explains Y | `PH_shock_intensity` — how many months had bad weather before harvest |
| **Control Variables** | Other things that might affect Y (you want to "hold them constant") | Import volume, exchange rate, CPI, cold storage |
| **Fixed Effects** | Variables that absorb unobserved heterogeneity | Market×Commodity FE, Commodity×Time FE |
| **Instrument (IV)** | Not used in your paper, but: a variable that affects X but not Y directly | (Not applicable here — weather IS the natural experiment) |

### Your Key Variables Explained

#### The Dependent Variable: `ln(price_wholesale_raw_mid_kg)`

**Why wholesale, not retail?**
Wholesale prices respond first to supply shocks. Retail prices have additional markups, transport costs, and retail competition that add noise.

**Why the midpoint of low and high?**
DAM reports a range (lowest and highest price observed). The midpoint is the best estimate of the "typical" price. The DAM's own `avgPrice` contains hidden institutional adjustments — we avoid it.

**Why per kg?**
DAM reports wholesale in BDT per quintal (100 kg). We divide by 100 to get per-kg for comparability with retail.

**Why natural log?**
- Coefficients become **percentage changes**: β = 0.05 means "a one-unit shock increases prices by 5%"
- Reduces the influence of extreme outliers
- Prices are always positive and typically right-skewed — log makes them more symmetric
- Standard in economics

#### The Key Independent Variable: `PH_shock_intensity`

This counts how many months during the pre-harvest growing season had extreme weather:

```
For onion harvested in March 2020:
    Pre-harvest months: Oct 2019, Nov 2019, Dec 2019, Jan 2020, Feb 2020, Mar 2020
    
    If Oct had excessive rain (z > 1.5) → +1
    If Nov was normal → +0
    If Dec had a cold snap (z < -1.5) → +1
    If Jan was normal → +0
    If Feb was normal → +0
    If Mar was normal → +0
    
    PH_shock_intensity = 2 (two months were shocked)
```

**Why count months instead of a single binary?**
The old pipeline used a single 0/1 indicator for the whole year — "was there ANY shock?" This loses information about severity and caused statistical problems (the placebo test failed). Counting months captures intensity: 4 months of bad weather is worse than 1 month.

#### Weather Anomalies (Z-scores)

A **Z-score** measures how unusual something is compared to the historical average:

```
Z = (observed value − historical average) / historical standard deviation
```

- Z = 0 → perfectly normal weather
- Z = +1 → one standard deviation above normal (somewhat unusual)
- Z = +1.5 → quite unusual (our threshold for "shock")
- Z = +2 → very unusual (only happens ~2.5% of the time)
- Z = -1.5 → unusually LOW (drought or cold snap)

**Why not just use raw rainfall in mm?**
Because 200mm of rain means different things in different places. In Sylhet (the wettest division), 200mm is normal. In Rajshahi (the driest), it's a flood. Z-scores normalize this.

#### Fixed Effects: The Invisible Control Variables

**Market × Commodity Fixed Effects (α_mc):**
These absorb everything that's constant about a specific market selling a specific commodity. For example:
- Dhaka's Kawran Bazar always has higher onion prices than a rural Rajshahi market (due to location, infrastructure, competition)
- Potato is always cheaper than onion
- These differences don't change over time, so we "absorb" them with fixed effects

Think of it as: "We're only looking at how prices CHANGE within the same market-commodity pair over time."

**Commodity × Year-Month Fixed Effects (γ_ct):**
These absorb everything that's common to all markets for a given commodity in a given month:
- National onion shortage in January 2022 → all onion prices went up everywhere → absorbed
- General inflation in 2023 → absorbed
- Seasonal patterns (potatoes are always cheaper in March right after harvest) → absorbed

After absorbing these, the ONLY variation left to explain is: **within the same market, for the same commodity, after removing common time effects — did weather shocks cause ADDITIONAL price increases?**

---

## Chapter 9: Data Cleaning

### Why Clean Data?

> "Garbage in, garbage out."

Real-world data is messy. Government databases have typos. Sensors malfunction. Records go missing. If you don't clean your data, your analysis will produce meaningless results.

### Your 14 Quality Flags

Your data underwent a rigorous 11-step audit that identified these issues:

| Flag | What It Catches | How Many | Action |
|------|----------------|----------|--------|
| `flag_zero_wholesale` | Wholesale price = 0 (impossible for onion/potato) | 144 | Exclude |
| `flag_zero_retail` | Retail price = 0 | 150 | Exclude |
| `flag_inverted_wholesale` | Low price > High price (data entry swap) | 13 | Exclude |
| `flag_extreme_wholesale` | Data entry error (e.g., "19001700" concatenation) | 14 | Exclude |
| `flag_outlier_wholesale` | Price is > Q3 + 3×IQR | varies | Flag, keep in robustness |
| `flag_concat_digits` | Two prices accidentally concatenated into one | 14 | Exclude |
| `flag_suspicious_w_avg` | DAM's average doesn't match midpoint calculation | varies | Flag only |

### The Three Data Tiers

After cleaning, your data is split into three tiers:

```
FULL_FLAGGED (3,348 rows — 100%)
    │
    ├── Remove 171 corrupted rows (zeros, inversions, typos)
    │
    ▼
PRIMARY_ANALYSIS (3,177 rows — 94.89%) ← YOUR DEFAULT SAMPLE
    │
    ├── Additional balanced panel filter (≥6 months coverage)
    │
    ▼
STRICT_SENSITIVITY (2,721 rows — 81.27%) ← ROBUSTNESS ONLY
```

### The Cleaning Mindset

- **Be conservative:** When in doubt, flag but don't delete. Let the data tell its story.
- **Be transparent:** Report how many observations you dropped and why.
- **Be consistent:** Apply the same rules to every observation. No cherry-picking.
- **Be documented:** Someone should be able to reproduce your exact cleaning steps.

---

## Chapter 10: Descriptive Statistics

### What Are Descriptive Statistics?

Before running fancy regressions, you need to simply **describe your data**. This tells readers (and yourself) what you're working with.

### Table 1: Summary Statistics

This is ALWAYS the first table in an empirical paper. It looks like:

| Variable | N | Mean | SD | Min | P25 | Median | P75 | Max |
|----------|---|------|----|-----|-----|--------|-----|-----|
| Wholesale price (BDT/kg) | 100,000 | 45.2 | 18.7 | 5.0 | 32.1 | 42.0 | 55.3 | 180.0 |
| Pre-harvest shock intensity | 100,000 | 0.8 | 1.1 | 0 | 0 | 0 | 1 | 6 |
| Precipitation z-score | 100,000 | 0.02 | 1.01 | -3.2 | -0.67 | 0.01 | 0.70 | 4.1 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**What to look for:**
- **N** — How many observations do you have? Are there enough?
- **Mean vs. Median** — If they're very different, the distribution is skewed
- **SD** — How much variation is there? If SD ≈ 0, there's nothing to explain
- **Min/Max** — Any impossible values? (Negative prices? Temperatures of 100°C?)
- **Missing values** — Count and explain them

### Visualizations Before Regression

**Time series plot:** Plot average prices over time (2000–2026). Look for:
- Seasonal patterns (are prices always high in certain months?)
- Structural breaks (did prices permanently shift at some point?)
- The 2024 data gap (is it visible?)

**Box plots by month:** Do prices follow the crop calendar? Potato prices should be lowest right after the February–March harvest.

**Correlation matrix:** How correlated are your independent variables? If two X variables are highly correlated (> 0.8), you may have multicollinearity issues.

**Maps:** Where are your markets? Do prices vary spatially? These are powerful for making your paper visually compelling.

---

## Chapter 11: Econometric Methodology

### What IS Econometrics?

Econometrics = economics + statistics. It's the toolkit for testing economic hypotheses with data.

At its core, you're fitting a line through a cloud of data points:

```
Price = a + b × Weather + noise

If b is large and statistically significant:
    "Weather affects prices" ✓
If b is small or insignificant:
    "No evidence that weather affects prices" ✗
```

### Why Not Just Use Correlation?

Correlation tells you things move together. But:
- **Ice cream sales** and **drowning deaths** are correlated (both increase in summer)
- Does ice cream CAUSE drowning? No! Summer weather causes BOTH.

This is the **omitted variable bias** problem. Something you didn't measure (summer heat) is driving both your X and Y, creating a fake relationship.

### Panel Fixed Effects: Your Secret Weapon

Your paper uses **panel data** — you observe the SAME markets over MANY time periods. This is powerful because you can use **fixed effects** to control for things you can't even measure.

**Imagine two markets:**
- Market A (Dhaka) always has high prices because it's the capital with high demand
- Market B (rural Rangpur) always has low prices because it's remote

If you just compared them, you'd confuse "being in Dhaka" with "weather effects." But with fixed effects:

```
Market A: Price_A(March) − Average_Price_A = weather effect + noise
Market B: Price_B(March) − Average_Price_B = weather effect + noise
```

You're comparing each market TO ITSELF over time. Everything that's constant about Market A (location, infrastructure, population) is differenced away.

### The Identification Strategy

"Identification" means: **how do you know it's weather causing price changes, and not something else?**

Your identification rests on THREE pillars:

1. **Weather is exogenous** — Nobody can control the weather. It's not caused by prices. This gives you a natural experiment.

2. **Crop-calendar timing** — You specifically look at weather BEFORE harvest (pre-harvest window). This eliminates reverse causality: post-harvest prices can't cause pre-harvest weather.

3. **Fixed effects** — Market×commodity FE absorb all time-invariant differences. Commodity×time FE absorb all macro trends. The only remaining variation is the idiosyncratic weather-price relationship.

### Clustering Standard Errors

When you estimate your regression, you get a coefficient (β) and a standard error (SE). The SE tells you how precise your estimate is.

**Why cluster at the district level?**
- Markets in the same district share the same weather → their errors are correlated
- If you ignore this correlation, your SEs are too small → you find "significance" where there isn't any
- Clustering corrects for this by treating correlated observations as providing less information

**You have 64 districts** — this is a comfortable number of clusters (rule of thumb: need ≥30-50 for clustering to work well).

---

## Chapter 12: Running the Analysis

### The Model Hierarchy

Don't just run one regression. Build a sequence that tells a story:

```
Model 1: "Does weather affect prices?" (Baseline)
    ↓ Yes? Continue...
Model 2: "Which type of weather matters?" (Decomposed shocks)
    ↓ Interesting! What about...
Model 3: "Does it differ for onion vs. potato?" (Subsamples)
    ↓ Yes! And...
Model 4: "Does distance to Dhaka matter?" (Spatial friction)
    ↓ Now test dynamics...
Model 5: "When does the effect appear and fade?" (Event study)
    ↓ And the supply chain...
Model 6: "Does it pass through to retail prices?" (Vertical transmission)
    ↓ Finally...
Model 7: "Is the relationship linear or non-linear?" (Severity)
```

Each model adds one new insight. The reader builds understanding step by step.

### Interpreting Regression Output

When you run a regression, you get output like:

```
                            Panel Fixed Effects Regression
==============================================================================
Dep. Variable:              ln(price)   R-squared (within):          0.142
No. Observations:              98,543   No. Groups:                  2,187
==============================================================================
                          coef    std err          t      P>|t|  [95% CI]
------------------------------------------------------------------------------
PH_shock_intensity       0.032    0.011      2.909      0.005   [0.010, 0.054]
==============================================================================
Cluster-robust SEs (64 clusters)
```

**Reading this:**
- **coef = 0.032:** Each additional month of pre-harvest weather shock increases prices by **3.2%** (because dependent variable is in logs)
- **std err = 0.011:** The estimate has a standard error of 1.1 percentage points
- **t = 2.909:** The coefficient is 2.9 standard errors away from zero — quite far!
- **P>|t| = 0.005:** There's only a **0.5% chance** this result happened by random chance → highly significant
- **95% CI = [0.010, 0.054]:** We're 95% confident the true effect is between 1.0% and 5.4%
- **R² within = 0.142:** The model explains 14.2% of the variation in prices AFTER removing fixed effects

### Statistical Significance Conventions

| Symbol | p-value | Meaning | In plain English |
|--------|---------|---------|-----------------|
| *** | p < 0.01 | Highly significant | Less than 1% chance this is random |
| ** | p < 0.05 | Significant | Less than 5% chance this is random |
| * | p < 0.10 | Weakly significant | Less than 10% chance this is random |
| (none) | p ≥ 0.10 | Not significant | Could easily be random noise |

The standard threshold for "significant" is p < 0.05. But in economics, p < 0.01 is the gold standard.

### The Event Study: Your Most Powerful Visual

The event study (Model 5) plots coefficients over time relative to the shock:

```
     coefficient
          |
   0.06   |                        *
   0.04   |                   *         *
   0.02   |              *                   *
   0.00   |----*----*----*------------------------------
  -0.02   |
          |_____|_____|_____|_____|_____|_____|_____|____
           t-3   t-2   t-1   t    t+1   t+2   t+3
                              ↑
                         Shock happens here
                         
  Should be ≈ 0 here        Should be significant here
  (pre-trend test)           (actual effect)
```

**If the pre-trend coefficients (t-3, t-2, t-1) are NOT zero:** Something is wrong. Prices were already changing before the shock → your "effect" might be spurious.

**If they ARE zero and post-shock coefficients are significant:** Strong evidence of a causal effect.

---

## Chapter 13: Robustness and Sensitivity

### Why Robustness Checks?

A single regression result proves nothing. Reviewers will ask: "But what if you used a different sample? A different measure? A different threshold?" If your result only holds under ONE very specific setup, it's probably not real.

Robustness checks show that your findings are **stable across reasonable alternative choices.**

### Types of Robustness Checks

1. **Alternative dependent variable:** Use `price_wholesale_dam_avg_kg` instead of midpoint → same result?
2. **Alternative sample:** Use STRICT_SENSITIVITY tier → same result?
3. **Alternative shock definition:** Use ±1.0 SD or ±2.0 SD thresholds → same result?
4. **Alternative weather data:** Use CHIRPS rainfall instead of ERA5 → same result?
5. **Alternative standard errors:** Two-way clustering (district × time) → still significant?
6. **Placebo tests:**
   - Test imported commodities (should show NO weather effect)
   - Assign wrong crop calendars (should show NO effect)
7. **Functional form:** Use first-differences (ΔY) instead of levels with FE

### How to Report Robustness

Create a table where each row is one check:

| Specification | β | SE | p-value | N | Consistent? |
|--------------|---|-----|---------|---|-------------|
| Baseline | 0.032 | 0.011 | 0.005 | 98,543 | — |
| DAM avg price | 0.029 | 0.012 | 0.018 | 98,543 | ✓ |
| Strict sample | 0.035 | 0.013 | 0.009 | 82,100 | ✓ |
| ±1.0 SD threshold | 0.021 | 0.009 | 0.022 | 98,543 | ✓ |
| Imported commodities (placebo) | 0.004 | 0.015 | 0.789 | 12,400 | ✓ (null) |
| Wrong crop calendar (placebo) | 0.008 | 0.011 | 0.467 | 98,543 | ✓ (null) |

If most rows show "✓", your result is robust. If several show "✗", be honest about it.

---

## Chapter 14: Tables and Figures

### The Art of Academic Tables

Your tables should communicate results **immediately** and **completely**. A reader should be able to understand a table without reading the text.

**Table formatting rules:**
- Column headers describe the sample or specification
- Coefficients are starred for significance (*, **, ***)
- Standard errors are in parentheses below each coefficient
- Bottom rows show: N, R², number of groups, clusters, fixed effects used
- Include a note explaining significance levels and clustering

### The Art of Academic Figures

Figures should:
- Have clear axis labels with units
- Include a descriptive title
- Use a legend when there are multiple series
- Be readable in grayscale (for print journals)
- Be high resolution (300 DPI minimum)
- Include a source note

**Your 5 key figures:**
1. **Map** — Where are your markets? (Establishes geographic context)
2. **Time series** — What do prices and weather look like over time? (Establishes patterns)
3. **Event study** — When does the price respond to weather? (Your KEY causal evidence)
4. **Seasonal boxplots** — How do prices relate to the crop calendar? (Shows mechanism)
5. **Spatial scatter** — Does distance to Dhaka matter? (Tests spatial hypothesis)

---

## Chapter 15: Writing the Paper

### Section-by-Section Guide

#### Introduction (2-3 pages)
**The funnel structure:**
1. Open with the big picture: "Climate change threatens agricultural systems worldwide..."
2. Narrow to the mechanism: "Weather shocks during the growing season can reduce expected crop supply..."
3. State the gap: "Despite extensive research on India and Sub-Saharan Africa, no study has examined..."
4. State YOUR contribution: "This paper uses a novel market-level panel spanning 26 years and 324 markets..."
5. Preview results: "We find that each additional month of pre-harvest weather shock increases wholesale prices by X%..."
6. Roadmap: "The remainder of this paper is organized as follows..."

#### Data (3-4 pages)
- Describe each data source (DAM, ERA5, controls)
- Show Table 1 (descriptive statistics)
- Discuss the sample (how many markets, how many years, how many commodities)
- Show Figure 1 (map) and Figure 2 (time series)
- Discuss the 2024 data gap and how you handle it

#### Methodology (2-3 pages)
- Write out the regression equation with full notation
- Explain each variable
- Justify the identification strategy (why can you claim causation?)
- Explain the fixed effects structure
- Explain clustering choice
- Describe the event-study specification

#### Results (3-4 pages)
- Table 2: Main results (build from simple to complex)
- Table 3: Spatial and non-linearity
- Figure 3: Event study
- Interpret coefficients in economic terms: "A one-standard-deviation increase in pre-harvest rainfall anomaly is associated with a X% increase in wholesale onion prices"

#### Robustness (2-3 pages)
- Table 4: All robustness checks
- Placebo tests (imported commodities, wrong calendars)
- Alternative specifications

#### Discussion (1-2 pages)
- Compare your findings to Letta et al. (2022) and other benchmarks
- Policy implications: Early warning systems? Strategic reserves? Import timing?
- Limitations: What can't your data/method address?

#### Conclusion (1 page)
- Summarize key findings in plain language
- Implications for climate adaptation policy
- Suggestions for future research

---

## Chapter 16: The Abstract

### The Last Thing You Write, the First Thing People Read

The abstract is a **250-word summary** of your ENTIRE paper. Write it LAST, after everything else is done.

### The 6-Part Formula

| Part | Sentences | Your Paper |
|------|-----------|------------|
| **Motivation** | 1-2 | "Climate change is increasing the frequency of extreme weather events, with critical implications for food security in vulnerable countries." |
| **Question** | 1 | "This paper investigates whether pre-harvest weather shocks significantly affect wholesale agricultural commodity prices in Bangladesh." |
| **Data** | 1-2 | "We construct a novel panel of daily wholesale prices for 11 onion and potato varieties across 324 markets from the Bangladesh Department of Agricultural Marketing (2000–2026), merged with ERA5-Land gridded weather data aggregated to 64 districts." |
| **Method** | 1-2 | "Using panel fixed effects with crop-calendar-specific pre-harvest weather exposure and clustering at the district level, we exploit the exogeneity of weather to identify causal price effects." |
| **Findings** | 2-3 | "We find that each additional month of extreme weather during the pre-harvest window increases wholesale prices by X%. [Decomposed effects]. [Onion vs potato]. [Spatial patterns]." |
| **Implications** | 1-2 | "These findings suggest that weather-based early warning systems could help anticipate price spikes, enabling more effective management of strategic food reserves and import timing in climate-vulnerable economies." |

---

## Chapter 17: Submission and Peer Review

### Where to Submit

Target journals based on your topic:
- **Top field journals:** Journal of Development Economics, American Journal of Agricultural Economics, World Development
- **Climate-economics crossover:** Nature Food, Environmental Research Letters, Global Food Security
- **Regional journals:** Journal of South Asian Development, Bangladesh Development Studies

### The Peer Review Process

```
You submit paper
    ↓
Editor reads it (1-2 weeks)
    ↓
Desk reject (30-50% chance) ───→ Submit to another journal
    OR
Sent to 2-3 anonymous reviewers (2-6 months)
    ↓
Reviewers report back:
    ├── "Reject" ───→ Submit elsewhere (try another journal)
    ├── "Major revisions" ───→ Fix issues, resubmit (2-4 months)
    ├── "Minor revisions" ───→ Small fixes (1-2 months)
    └── "Accept" ───→ 🎉 (rare on first submission)
    ↓
After revisions accepted:
    ↓
Published! 🎉 (Total time: 6 months to 2+ years)
```

### Common Reviewer Concerns

Reviewers will likely ask:
1. "How do you know it's causal?" → Your identification strategy section must be airtight
2. "What about [omitted variable]?" → That's what fixed effects and controls are for
3. "Is this robust to [alternative specification]?" → Your robustness checks section
4. "How does this compare to Letta et al.?" → Your literature comparison
5. "What are the policy implications?" → Your discussion section

---

## Glossary

| Term | Simple Definition |
|------|------------------|
| **Panel data** | Same units observed over multiple time periods |
| **Cross-sectional data** | Many units observed at one point in time |
| **Time series data** | One unit observed over many time periods |
| **Fixed effects (FE)** | Statistical technique that controls for all constant characteristics of a unit |
| **Cluster-robust SE** | Standard errors that account for correlation within groups |
| **Endogeneity** | When your X variable is correlated with the error term (biases your results) |
| **Exogeneity** | When your X variable is NOT correlated with the error term (clean identification) |
| **Omitted variable bias** | When a missing variable drives both X and Y, creating a spurious relationship |
| **Z-score** | How many standard deviations away from the mean (measures unusualness) |
| **p-value** | Probability of seeing your result if the true effect were zero |
| **Coefficient (β)** | The estimated relationship between X and Y |
| **R-squared** | Fraction of Y's variation explained by the model (0 to 1) |
| **Heteroskedasticity** | When the variance of errors differs across observations |
| **Multicollinearity** | When two X variables are highly correlated with each other |
| **SPEI** | Standardized Precipitation-Evapotranspiration Index |
| **IQR** | Interquartile Range = Q3 − Q1 (used for outlier detection) |
| **BDT** | Bangladeshi Taka (currency) |
| **Quintal** | 100 kilograms (unit used by DAM for wholesale prices) |
| **DAM** | Department of Agricultural Marketing (Bangladesh) |
| **ERA5-Land** | ECMWF's global reanalysis weather dataset |
| **CHIRPS** | Climate Hazards Center rainfall dataset |
| **Rabi season** | Winter cropping season in Bangladesh (October–March) |
| **Marketing year** | From one harvest to the next (not calendar year) |

---

## Common Mistakes to Avoid

### 🚫 Data Mistakes
1. **Using `w_avgPrice` without understanding it** — It contains hidden institutional adjustments
2. **Not checking for zeros and inversions** — These are data entry errors, not real prices
3. **Interpolating across gaps** — The 2024 data gap is institutional, not random
4. **Treating imported and domestic commodities the same** — They have different price drivers

### 🚫 Methodology Mistakes
5. **Using a single binary shock indicator** — Loses intensity information, causes pre-trend failure
6. **Clustering at the wrong level** — Market-level has too many clusters, national has too few
7. **Reporting overall R² instead of within R²** — Overall R² is inflated by fixed effects
8. **Ignoring the crop calendar** — The ENTIRE identification strategy depends on correctly defining "pre-harvest"

### 🚫 Writing Mistakes
9. **Starting the paper with statistics** — Start with the real-world problem
10. **Hiding unfavorable results** — Reviewers will find them. Report honestly.
11. **Overselling causality** — Be precise: "consistent with a causal interpretation" is safer than "proves"
12. **Not comparing to existing literature** — Your results mean nothing without benchmarks

### 🚫 Presentation Mistakes
13. **Tables without notes** — Always explain significance stars, clustering, and FE structure
14. **Figures without axis labels** — Every figure must be self-contained
15. **Too many decimal places** — 3 decimal places is usually enough for coefficients

---

> [!TIP]
> **The single most important thing:** Your paper is an ARGUMENT. Every section, table, and figure must serve the argument. If it doesn't help answer your research question, cut it. A clear, focused 25-page paper is infinitely better than a sprawling 60-page mess.

---

*This guide was prepared as a companion to the Paper 1 analysis pipeline. For the technical implementation prompt, see `FABLE_MASTER_PROMPT.md`.*
