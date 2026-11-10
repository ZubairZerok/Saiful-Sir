# Step 2: Comprehensive Literature Review & Methodology Matrix

## 1. Executive Literature Map
The econometric literature on weather anomalies and agricultural market prices is structured across four primary analytical layers:

1. **Macro Climate-Economy Literature:** Broad cross-country and multi-sector econometric estimation of weather shocks on aggregate GDP, agricultural output, and inflation (Dell, Jones & Olken 2014; Carleton & Hsiang 2016).
2. **Pre-Harvest Expectations & Timing Channel:** Moving beyond post-harvest supply shocks to demonstrate that forward-looking market participants adjust prices during the pre-harvest crop growing window before harvest failure materializes (*Letta, Montalbano & Pierre 2022* in India; *Brown & Kshirsagar 2015*).
3. **Spatial Market Integration & Law of One Price:** Econometric models of spatial arbitrage, transportation costs, trade barriers, and price dispersion across subnational market networks (*Fackler & Goodwin 2001*; *Aker 2010*).
4. **Bangladesh Agricultural & Cold Storage Context:** Empirical studies on onion and potato production volatility, cold storage infrastructure capacity, seasonal price spreads, and post-harvest storage liquidation (*BBS, DAM, World Bank*).

---

## 2. Synthesized Literature Review & Methodological Framework

STEP 2

Yes — and the literature search changes the framing of your paper in one very important way.

The core idea is credible, but you should not frame the novelty as “nobody has studied pre-harvest weather shocks and prices.” The strongest direct international paper already does almost exactly that for India: Letta, Montalbano and Pierre (2022) use district-level monthly wholesale prices and crop-specific growing periods to show that drought raises prices before harvest failure materializes, interpreting the pre-harvest movement as an expectations channel. (Wiley Online Library)

Your strongest contribution is therefore Bangladesh-specific external validity plus commodity heterogeneity and a more granular identification of timing/severity, especially for onion and potato, where storage, imports and market structure are particularly important.

1. Executive literature map

The literature falls into four broad layers.

First, there is now convincing international evidence that weather can move agricultural prices. Brown and Kshirsagar find short-run domestic-weather effects across 554 local commodity markets in 51 countries, while Bhanumurthy, Dua and Kumawat show rainfall shocks affect both spot and futures prices in India, with stronger responses in futures markets. (ScienceDirect)

Second, a smaller literature moves from “weather affects prices” to when weather affects prices. Letta et al. is the key paper: it explicitly isolates a pre-harvest response using the timing gap between the weather anomaly and the later supply realization. (Wiley Online Library)

Third, newer work strengthens the timing/severity dimension. Cornejo, Merovich and Merener (2026) examine extreme dry spells, heat and excessive rain during the U.S. Midwest growing season and find significant movements in corn and soybean futures prices. (Nature) Costa Junior and Calef explicitly examine dryness during pre-harvest phenological stages of Brazilian corn using local spot prices. (University of East Anglia)

Fourth, Bangladesh has a substantial literature on climate → production, price integration, price volatility, and storage, but the directly relevant chain pre-harvest weather anomaly → observed local agricultural price response is much less developed in the material I could verify. Bangladesh studies have established that potato prices are shaped by storage, that onion prices are linked asymmetrically to imported onion prices, and that domestic markets exhibit seasonal and spatial price dynamics. (Bangladesh J. Agr. Economics) plus Mila source from prior search, but exact ID not in current final memory? We have from prior. We can cite that. Need likely valid citation IDs from tool results in context. Use known.

The critical methodological point is that crop-calendar construction is not a cosmetic choice. Li and Ortiz-Bobea show that aggregating weather over the wrong “season” can generate nonclassical measurement error and bias estimates in unpredictable directions. (Wiley Online Library)

So your paper should be built around:

weather shock → within-season timing → pre-harvest price response → severity/nonlinearity → onion/potato heterogeneity, while explicitly controlling for alternative price mechanisms such as imports, storage, transport and market integration.

2. Literature / methodology matrix

I am using “Not reported” where the verified material did not give enough information rather than filling gaps from inference.

PaperCountryCommodityData / periodPriceWeather / shockPre-harvest definitionModel / identificationMain findingRelevance

Letta, Montalbano & Pierre (2022), AJAE

India

Maize, rice, wheat

District monthly panel, 2004–2017

Local wholesale prices

SPEI / drought anomalies

Crop growing period using crop calendars

Panel FE; weather timing exploited to separate pre-harvest expectation from later supply realization

Drought significantly raises prices during growing period, before harvest failure; authors estimate expectation channel explains ~85% of total growing-season drought price effect

Closest benchmark

Cornejo, Merovich & Merener (2026), Communications Sustainability

USA Midwest

Corn, soybean

Daily weather / crop / futures, 1971–2019

Futures prices

Extreme dry spells, heat, extreme rain

June–August growing season

Weather-event price-response models with nonlinear specifications

Hot/dry and extreme-rain events increase prices; effects differ by crop/event

Shows modern high-frequency pre-harvest weather-price response

Costa Junior & Calef (2023), working paper

Brazil

Corn

2005–2019

Local corn spot prices

Days without precipitation

Pre-harvest phenological stages

Panel regression, nonlinear dryness term

Corn prices begin responding after sufficiently long dry spells; timing differs across stages

Very close on crop-calendar/phenology logic

Arellano, Juárez-Torres & Zazueta (2023), Banco de México WP

Mexico

White corn, dry beans

20-year market/city panel

Market prices

Temp and precipitation shocks ≥0.5 SD

Growing-period timing

Panel methods with timing/lag effects

Immediate ~2% price increase, with lagged effects ~1–2.5%; mechanism partly via productivity

Strong benchmark for anomaly thresholds and lag structure

Bhanumurthy, Dua & Kumawat (2013), CCE

India

Rice, wheat, pulses and others

Monthly

Spot/futures

Rainfall

Not explicitly crop-calendar pre-harvest identification

Cointegration, dynamics, smooth-transition regression

Rainfall affects spot/futures prices with different lags; stronger response in futures

Expectations / futures transmission

Brown & Kshirsagar (2015), GEC

51 countries

Multiple foods

554 markets, 2008–2012 monthly

Local market food prices

Domestic weather disturbances

Not specifically pre-harvest

Cross-market short-run analysis

Nearly 20% of local prices affected by domestic weather disturbances

Broad developing-country benchmark

Stevens (1991), Journal of Futures Markets

USA

Corn, wheat, soybean

Not fully verified

Futures

Growing-season weather

Growing season

Empirical test of weather-persistence/price dynamics

Tests whether growing-season weather information is incorporated into futures prices

Early expectations benchmark

Mirzabaev & Tsegai (2012/2015)

Central Asia

Wheat, potato

Provincial monthly, 2000–2010

Commodity prices

Temperature, precipitation, irrigation

Not explicitly pre-harvest

FGLS panel

Weather variability and irrigation-water shocks affect prices

Useful potato/weather precedent

Mila et al. (2023), PLOS ONE

Bangladesh

Onion

Monthly, 2006–2020

Wholesale/retail onion

None

None

NARDL + Granger causality

Imported onion prices lead local prices; asymmetric transmission

Essential Bangladesh control structure

Ahamed, Moniruzzaman & Tabassum (2021), BJAE

Bangladesh

Potato

Monthly national wholesale, 1972–2018

Wholesale potato

None

Seasonal-price comparison

Ratio-to-moving-average

Cold-storage capacity reduced seasonal price variation

Essential potato-storage benchmark

Hossain et al. (2025), JBAU

Bangladesh

Onion

10 markets, 2012–2022

Market onion prices

None

Seasonal cycle only

BEKK-GARCH + DCC + cointegration

Strong seasonality and volatility spillovers

Important market/volatility controls

Jannat, Ishikawa-Ishiwata & Furuya (2021), Sustainability

Bangladesh

Potato

District-level, 1988–2013

Modelled farm/equilibrium price

Rainfall, temperature, solar radiation

Crop-production stages

Supply-demand/equilibrium model

Climate changes potato production and modeled prices

Closest Bangladesh climate→potato price paper, but not observed pre-harvest price response

Deb et al. (2020), Agriculture

Bangladesh

Rice

Monthly, 2006–2017

Farm/wholesale/retail

Flooding episode

Harvest timing

Vertical price transmission

2016 flooding reduced harvest and prices rose subsequently

Helps distinguish post-harvest supply channel

Islam et al. (2022), Environmental Challenges

Bangladesh

Food/cereals

3 longitudinal rounds, 2011–2019

Food consumption

Flood/drought/cyclone/salinity

No price timing

DiD

Extreme climate events reduce food consumption

Bangladesh weather-shock identification precedent

Ahmed (2024), Heliyon

Bangladesh

Agricultural households

2018–19

Income/food security

Flood/extreme rainfall

No price timing

Quantile + ordered probit

Climate shocks reduce agricultural income and increase food insecurity

Bangladesh shock-construction precedent

The most important pattern

The literature is much more crowded for:

Weather → production → later price

than for:

Weather news → price before production/harvest changes.

And the latter is exactly where Letta et al. becomes critical. (Wiley Online Library)

3. Five closest international papers

1. Letta, Montalbano & Pierre (2022) — the benchmark you must download first

“Weather shocks, traders’ expectations, and food prices.” American Journal of Agricultural Economics 104(3):1100–1119. DOI: 10.1111/ajae.12258.

This is the paper that poses the greatest novelty threat.

It uses district-level monthly wholesale prices for maize, rice and wheat in India from 2004–2017, matched with crop-specific growing calendars and weather anomalies. The design exploits the timing gap between the weather shock and the later harvest/supply effect. The paper finds droughts raise prices during the growing period, before harvest failure has materialized. (Wiley Online Library)

Why it matters:

It already establishes the theoretical and empirical proposition that you are trying to test.

Therefore, your paper should not claim:

“This is the first study to show that pre-harvest weather affects agricultural prices.”

Instead:

“This study tests whether the pre-harvest weather-price response documented in other agricultural markets also occurs in Bangladesh, and whether its magnitude and timing differ across onion and potato under Bangladesh’s distinctive storage, import and market conditions.”

That is much more defensible.

2. Cornejo, Merovich & Merener (2026)

“Hot dry spells and extreme rain increased corn and soybean prices in the United States Midwest.” Communications Sustainability 1:17. DOI: 10.1038/s44458-025-00016-4.

This is extremely important because it is even more recent than Letta and works with high-frequency weather and market data. It uses 1971–2019 data for U.S. Midwest corn and soybean markets and examines extreme dry spells, heat and precipitation during the growing season. (Nature)

Its main contribution for you is methodological: it shows that shock definition matters, and that extreme precipitation and dry/hot combinations can have asymmetric price effects.

Your project should therefore test both continuous anomalies and severe-event definitions.

3. Arellano, Juárez-Torres & Zazueta (2023)

“Weather Shocks, Prices and Productivity: Evidence from Staples in Mexico.” Banco de México Working Paper 2023-16.

They find temperature and precipitation shocks of at least 0.5 standard deviations from climate normals generate immediate and lagged price increases in white corn and dry beans. The immediate response is approximately 2%, with lagged effects around 1–2.5%, varying with growing-period timing. (Bank of Mexico)

This is particularly useful for your RQ1a and RQ1b because it provides a natural precedent for:

standardized anomalies,

timing-specific effects,

lagged effects,

severity thresholds.

It is a working paper, so I would use it as a methodological benchmark rather than as your strongest peer-reviewed citation.

4. Bhanumurthy, Dua & Kumawat (2013)

“Weather Shocks and Agricultural Commodity Prices in India.” Climate Change Economics 4(3). DOI: 10.1142/S2010007813500115.

They analyze monthly spot and futures prices and rainfall shocks, using cointegration and dynamic models. Rainfall affects both spot and futures prices with different lags, and the response is larger in futures markets. (IDEAS/RePEc)

This matters because it supports the theoretical possibility that markets can capitalize weather information before physical supply changes are realized.

5. Brown & Kshirsagar (2015)

“Weather and international price shocks on food prices in the developing world.” Global Environmental Change 35:31–40. DOI: 10.1016/j.gloenvcha.2015.08.003.

They examine 554 local markets in 51 countries and find nearly 20% of local market prices were affected by domestic weather disturbances in the short run. (ScienceDirect)

It is not a pre-harvest identification study, but it establishes that local weather-price transmission is especially relevant in developing-country markets where trade and transport constraints limit smoothing.

4. Five closest Bangladesh papers

1. Jannat, Ishikawa-Ishiwata & Furuya (2021)

“Assessing the Impacts of Climate Variations on the Potato Production in Bangladesh: A Supply and Demand Model Approach.” Sustainability 13(9):5011. DOI: 10.3390/su13095011.

This is probably the Bangladesh paper closest in substantive mechanism to yours.

It explicitly links temperature, rainfall and solar radiation to potato production and then feeds the production effects into a supply-demand/equilibrium framework to assess price implications. (MDPI)

But the crucial distinction is:

Their price response is modeled through a production/supply-demand framework. Yours would estimate observed market-price responses to actual weather shocks at the subannual level.

That distinction is valuable.

2. Mila et al. (2023)

“Spatial price transmission in the onion markets of Bangladesh: An application of NARDL approach.” PLOS ONE. DOI: 10.1371/journal.pone.0284555.

Monthly local/imported wholesale and retail onion prices, 2006–2020; NARDL and Granger causality.

They find imported onion prices lead local onion prices and that transmission is asymmetric.

This makes imported onion prices a non-negotiable control/alternative channel in your onion model.

Your paper should explicitly acknowledge that a weather-induced price movement could otherwise be falsely attributed to domestic weather when it is actually reflecting international/import-price movements.

3. Ahamed, Moniruzzaman & Tabassum (2021)

“Can Cold Storage Reduce Seasonal Variation in Prices of Agricultural Commodities? A Case of Potato in Bangladesh.” Bangladesh Journal of Agricultural Economics 42(1):19–36.

They use monthly national wholesale potato prices, 1972–2018, from DAM and show that sufficient cold-storage capacity reduced seasonal price variation. (Bangladesh J. Agr. Economics)

This is hugely important for your interpretation.

A potato price response to weather may be mediated by inventory decisions and storage capacity, rather than immediate physical scarcity.

That actually makes potato very interesting for your paper rather than making it a bad choice.

4. Hossain et al. (2025)

“Onion Price Volatility and Market Integration of Different Markets in Bangladesh.” Journal of Bangladesh Agricultural University 23(3):386–397. DOI: 10.3329/jbau.v23i3.84457.

It uses 10 Bangladesh onion markets, 2012–2022, and GARCH/BEKK/DCC methods to examine volatility and market relationships.

The key use for your study is not causal methodology. It tells you that your price series have meaningful seasonal patterns, cross-market correlations and volatility spillovers.

So your baseline model needs to account for market-level dependence.

5. Deb et al. (2020)

“Market Integration and Price Transmission in the Vertical Supply Chain of Rice: An Evidence from Bangladesh.” Agriculture 10(7):271.

This is useful because it provides a Bangladesh example where a major flood event affected harvest conditions and prices.

Its causal direction, however, is much closer to:

flood → realized supply/harvest → price

than:

pre-harvest weather news → price expectation.

That distinction is exactly what your design needs to preserve.

5. Five methodological benchmarks

1. Li & Ortiz-Bobea (2022)

“On the timing of relevant weather conditions in agriculture.” Journal of the Agricultural and Applied Economics Association. DOI: 10.1002/jaa2.21.

This paper may be the most important methodology paper for your project.

It shows that researchers often aggregate weather over an assumed “season,” but using the wrong season creates nonclassical measurement error and potentially biases estimates in either direction. They propose searching over candidate seasons using out-of-sample model fit. (Wiley Online Library)

For you:

Do not simply say “May–September is the growing season.”

The crop-calendar definition needs to be documented and ideally validated.

2. Gasparrini, Armstrong & Kenward (2010)

“Distributed lag non-linear models.” Statistics in Medicine 29:2224–2234. DOI: 10.1002/sim.3940.

DLNM explicitly models nonlinear exposure-response relationships together with lag structure. (DOI)

This is directly relevant to:

“How quickly do prices respond?”

and

“Does response magnitude increase with shock severity?”

because a simple one-period weather coefficient cannot answer those questions adequately.

3. Adjemian (2012)

“Quantifying the WASDE Announcement Effect.” American Journal of Agricultural Economics 94:238–256. DOI: 10.1093/ajae/aar131.

This is a major expectations/information benchmark. It shows how information released to commodity-market participants can be rapidly incorporated into prices and how the effect varies with inventory conditions, month and contract horizon. (Wiley Online Library)

The conceptual implication for Bangladesh is strong:

price movement can reflect information about future supply rather than current supply.

4. Su, Liao & Chang (2025)

“How does food market respond to natural disaster shocks? Evidence from the cabbage wholesale market.” World Development 190:106950. DOI: 10.1016/j.worlddev.2025.106950.

This uses daily wholesale cabbage data and DiD/event-study models around typhoons. They find prices rise even when market quantities are relatively stable, with evidence pointing toward expectations/stockpiling rather than purely contemporaneous supply effects. (ScienceDirect)

It is one of your best methodological warnings:

an early price response does not automatically prove a production-loss channel.

5. Dell, Jones & Olken (2014)

“What Do We Learn from the Weather? The New Climate-Economy Literature.” Journal of Economic Literature 52(3):740. DOI: 10.1257/JEL.52.3.740.

This is the broad methodological foundation for weather-as-within-location-shock designs: exploit temporal weather variation within spatial units, use panel methods, and consider nonlinear responses and heterogeneous effects.

6. Pre-harvest identification evidence

This is the most important section for your eventual paper.

Has anyone shown prices respond before harvest?

Yes. Very clearly.

Letta et al. explicitly find that drought conditions increase prices during the growing period before harvest failure has materialized. Their identification relies on the temporal gap between weather conditions and the subsequent supply shock. (Wiley Online Library)

So the empirical proposition is established internationally.

Did they use crop calendars?

Yes. The growing period is crop-specific rather than treating every crop as having the same calendar.

This is exactly why Li & Ortiz-Bobea matters: incorrectly defining a weather “season” can contaminate the exposure measure. (Wiley Online Library)

Were expectations directly measured?

Not literally.

The expectation channel is inferred from the timing of the price response relative to the eventual supply response.

That distinction should be retained in your paper.

You should write:

“consistent with an expectations channel”

rather than:

“we observe traders’ expectations.”

Unless you obtain an actual trader-expectation measure.

Were leads/lags tested?

The closest papers use temporal structure and lagged responses in various forms.

The Mexico paper finds immediate and lagged effects depending on the shock’s timing in the growing period. (Bank of Mexico)

How is anticipation distinguished from post-harvest supply effects?

The cleanest strategy in the literature is:

weather shock occurs during crop growth;

price responds before harvest;

harvest/production outcome occurs later;

post-harvest timing becomes a comparison/placebo;

dynamic effects reveal when the response starts.

That is much stronger than simply regressing annual prices on annual weather.

7. Bangladesh gap audit

LinkAssessmentReason

Climate → Production

Well studied

Bangladesh has substantial climate/production literature, including potato-specific work

Climate → Food Security

Well studied

Multiple household and food-security studies use weather shocks

Production → Price

Moderate

Strong price-transmission/seasonality literature; less consistently causal

Weather → Price

Limited

I found climate/production-price modeling and flood episodes, but not a strong Bangladesh analogue to Letta’s local weather-anomaly price design

Weather → Price Volatility

Very limited

Volatility studies exist, but the direct weather-volatility mechanism is not well established

Weather → Market Integration/Transmission

Limited

Market integration is heavily studied, but weather is rarely the causal treatment

Pre-harvest Weather → Agricultural Price

Very limited / no directly comparable Bangladesh evidence found in this search

This is the closest genuine gap

The wording matters.

Do not say:

“No Bangladesh study has ever examined weather and prices.”

Say:

“In the verified literature searched for this study, I found no directly comparable Bangladesh empirical design identifying pre-harvest weather shocks as a determinant of contemporaneous agricultural-market prices.”

That is defensible.

8. Method comparison for your exact RQ

MethodWhat it identifiesMain assumptionStrength for your studyMain weaknessVerdict

Panel FE

Within-market/crop association between weather deviations and prices

Conditional exogeneity of weather shocks after FE/time controls

Simple, credible, directly comparable to weather-economics literature

Dynamic timing must be added

Baseline

Event Study

Dynamic price response around discrete shock events

Valid untreated counterfactual / no differential pre-trends

Excellent visualization of anticipation and timing

Weather is continuous/recurrent, so event definition can be artificial

Secondary

DiD

Differential post-shock change in treated vs untreated units

Parallel trends + no spillovers

Strong for clearly discrete localized disasters

Hard to justify when weather varies continuously across many areas

Not baseline

DLNM

Nonlinear exposure-response across lags

Functional-form/spline assumptions; adequate variation

Excellent for RQ1a + RQ1b simultaneously

Harder to explain causally; can become over-parameterized

Secondary/extension

My recommendation

Do not build a paper that runs FE + DiD + event study + DLNM just because all four are available.

The strongest design is:

Panel fixed effects + crop-calendar-specific distributed weather exposure, with an event-study-style lead/lag visualization and a DLNM/nonlinear specification as a robustness/extension analysis.

That is a much cleaner paper.

9. Recommended baseline empirical design

I would make this your conceptual backbone:

[\ln(P_{mct}) =\beta W_{mct}^{pre}+\alpha_{mc}+\gamma_{ct}+\delta_m t+\theta X_{mt}+\epsilon_{mct}]

where:

(P_{mct}) = price in market (m), crop (c), time (t)

(W^{pre}) = crop-calendar-specific adverse weather exposure occurring before harvest

(\alpha_{mc}) = market × crop fixed effect

(\gamma_{ct}) = crop-specific seasonal/time controls

(\delta_m t) = market-specific trend if supported by the data

(X) = important time-varying alternative drivers

But the real value comes from replacing one (W) coefficient with a structured exposure:

[W^{pre}_{mct,k}]

for different pre-harvest lags/stages.

For example:

current week → 1–2 weeks lag → 3–4 weeks lag → 5–8 weeks lag

or better, biologically meaningful crop stages.

This lets you answer RQ1a directly.

Then test severity with nonlinear bins or splines:

[Price = f(Weather\ Shock)]

That answers RQ1b.

Then interact weather exposure with crop:

[Weather \times Onion]

to answer RQ1c.

10. Methodological decisions you need to lock before data collection

Weather-shock definition

Use multiple concepts, but preregister the hierarchy.

Primary: crop-specific standardized anomalies relative to a historical climate normal.

Alternative: SPEI, following Letta.

Robustness: physical extremes such as consecutive dry days, extreme heat days, or excessive-rain events.

Do not choose one threshold because “it looks good.”

Anomaly threshold

There are legitimate options in the literature:

0.5 SD: used by Arellano et al. (Bank of Mexico)

percentile-based severe anomalies: useful for tail events

physically meaningful agronomic thresholds

continuous standardized shocks

My recommendation is continuous standardized shocks as the baseline, then 0.5-SD and severe-tail definitions as robustness.

Harvest window

This is one of your most important decisions.

Define the crop-specific window using:

planting → growing stages → commercial harvest, not just one generic “monsoon season.”

And validate the theoretical calendar against observed arrival/harvest patterns if possible.

Li & Ortiz-Bobea strongly support treating this as a methodological choice rather than an arbitrary coding decision. (Wiley Online Library)

Price frequency

For your actual research question:

Daily > weekly > monthly.

Monthly data are workable, but they make “before harvest” much less precise.

A weekly design would be a very good compromise if daily BAMIS/DAM data are noisy.

Market level

I would make wholesale the primary outcome.

It is closer to production and inventory/trading decisions and matches the strongest literature, including Letta.

Retail can be a robustness outcome.

Weather-market matching

Do not simply attach the nearest BMD station.

Prefer:

production-area/crop-area weighted gridded weather → market catchment

or a carefully defined district-production area.

ERA5-Land can give you consistent spatial coverage; BMD stations can provide a ground-observation robustness layer.

Lag structure

Do not dump 20 highly correlated lags into OLS.

Use theoretically motivated lag windows, for example:

0, 1–2, 3–4, 5–8 weeks

and then a flexible distributed-lag model as a robustness analysis.

Treatment/control

I would not construct a conventional DiD treatment/control as your main design.

Weather is continuous.

Your main identification should come from within-market deviations in weather exposure.

Onion vs potato

Do both if the data quality permits.

But treat the comparison as a substantive contribution rather than a cosmetic second crop.

The markets are structurally different:

Onion: strong import-price transmission.

Potato: major storage/cold-storage dimension.

Those differences give you a mechanism-rich comparison. The Bangladesh literature already demonstrates the relevance of these two channels. (Bangladesh J. Agr. Economics)

11. A major identification warning: storage

This may become one of the coolest parts of the paper.

A pre-harvest weather shock does not necessarily imply:

“physical supply suddenly disappeared.”

A trader may observe abnormal weather and revise expected future availability.

For storable commodities, inventory optimization can translate that information into a current price response.

That is precisely the conceptual logic behind Letta et al. and the storage literature. (Wiley Online Library)

For Bangladesh potato, cold storage is empirically important enough that you should explicitly model or at least discuss it. Ahamed et al. find that expanded storage capacity materially reduced seasonal price variation. (Bangladesh J. Agr. Economics)

This means:

weather × storage capacity

could become an excellent heterogeneity test.

For example:

Does the pre-harvest weather-price response become weaker where storage capacity is greater?

That would move your paper beyond a simple reduced-form weather-price regression.

12. Another major identification warning: onion imports

For onion, imported prices are not a minor control.

Mila et al. find asymmetric transmission from imported onion prices to local onion prices in Bangladesh. (PLOS)

Therefore, an onion-weather regression that excludes:

imported onion price,

exchange-rate/major import-price shocks,

relevant policy/import controls

risks attributing an international-price movement to local weather.

This is especially important because Bangladesh onion markets are unusually exposed to India-related trade conditions.

13. What NOT to control for

This is a subtle but important causal issue.

Do not automatically put realized post-harvest production/yield/arrivals into the main pre-harvest price equation.

Why?

Because your hypothesized pathway is:

weather → expected future supply → price

and another pathway is:

weather → realized yield → future supply → price.

If realized production is a mediator, controlling for it can remove part of the effect you are trying to estimate.

Instead, use production/yield as a separate mechanism analysis.

This gives you a cleaner decomposition:

pre-harvest price response

versus

post-harvest realized supply response.

14. Proposed study vs existing literature

DimensionExisting closest literatureYour study

Country

India, Mexico, USA, Brazil, global

Bangladesh

Commodity

Mainly grains/corn/soy/beans

Onion + potato

Weather

Rainfall/temp/drought/extreme events

BMD + ERA5-Land crop-specific anomalies

Price

Wholesale/spot/futures

Bangladesh local wholesale market prices

Timing

Growing/pre-harvest in some closest studies

Explicit crop-calendar pre-harvest identification

Crop calendar

Strong in Letta / weather-agriculture literature

Central design element

Spatial level

District/market/state

Bangladesh market/district structure

Identification

FE / dynamic weather-price / event models

FE + distributed pre-harvest exposure

Lag effects

Present in several international papers

Explicit RQ1a

Severity

Present in several studies

Explicit RQ1b

Crop comparison

Usually separate crops

Onion vs potato heterogeneity

Storage

Often theoretically relevant

Explicit Bangladesh storage dimension

Transport

Less central in closest papers

Potential Bangladesh mechanism/confounder

Imports

Particularly relevant to onion

Explicit control/mechanism

Expectations

Mostly inferred

Explicitly tested via timing/placebo logic

This is a real contribution.

But it is an extension and contextual/mechanism contribution, not the invention of the pre-harvest weather-price idea.

15. Novelty threat check

🔴 Threat 1 — Very high: Letta et al. (2022)

This is the largest threat.

Their title itself is:

“Weather shocks, traders’ expectations, and food prices.”

They explicitly investigate pre-harvest price fluctuations and use temporal separation between weather anomalies and supply shocks. (Wiley Online Library)

You must cite this early and explicitly.

🟠 Threat 2 — Cornejo et al. (2026)

The newest peer-reviewed evidence shows weather events during the growing season can move crop prices in U.S. futures markets. (Nature)

This makes any “first evidence of pre-harvest weather-price response” claim unsafe.

🟠 Threat 3 — Costa & Calef (2023)

They explicitly study pre-harvest weather and corn price formation across phenological stages. (University of East Anglia)

🟡 Threat 4 — Taiwan cabbage (2025)

Su et al. show that food prices can respond before/around natural-disaster events through expectations and stockpiling mechanisms, using DiD/event study. (ScienceDirect)

Not a weather-anomaly analogue, but conceptually important.

🟡 Threat 5 — Mexico (2023)

Arellano et al. already connect timing within the growing period to immediate and lagged price responses. (Bank of Mexico)

So your novelty has to be:

Bangladesh + local market + onion/potato + crop-calendar timing + severity + heterogeneous storage/import mechanisms.

16. Strongest defensible contribution

Here is the framing I would eventually use in the introduction:

Existing international evidence indicates that weather anomalies can affect agricultural prices before harvest through expectations about future supply. However, this evidence is concentrated in other agricultural markets, particularly cereals and major commodity-producing countries. Bangladesh provides a substantively different setting in which domestic production is combined with strong market segmentation, heterogeneous storage capacity, import dependence for selected commodities, and substantial seasonal price variation. This study tests whether pre-harvest weather shocks affect local agricultural prices in Bangladesh and quantifies the timing and severity of those responses, while comparing onion and potato markets and separating pre-harvest anticipatory movements from post-harvest supply effects.

That is substantially stronger than:

“No one has studied this before.”

17. The strongest empirical design

My preferred design is:

Primary model: crop-calendar-aware panel FE.

Weather exposure: continuous standardized anomaly, calculated only over the relevant crop stage/window.

Temporal identification: distributed leads/lags of weather exposure, focused on the pre-harvest period.

Main outcome: log wholesale price or weekly percentage price change.

Fixed effects: market × crop FE, plus carefully selected calendar/time controls.

Dynamic analysis: event-study-style lead/lag graph around severe weather events, treated as a secondary specification rather than the primary identification.

Nonlinearity: severity bins/splines and interaction terms.

Mechanism: separate weather → realized production/yield → price pathway.

Heterogeneity: onion vs potato; storage capacity; rainfed/irrigated exposure if available; import exposure for onion.

Robustness: alternative anomaly definitions, crop-calendar windows, BMD vs ERA5-Land, alternate lag windows, wholesale vs retail, placebo post-harvest windows, spatial clustering/HAC, and market-specific trends.

This design is much more coherent than running four unrelated estimators and picking whichever produces the strongest significance.

18. Final download/read list

I would put these at the top of your actual PDF-reading queue:

Tier 1 — read extremely carefully

Letta, Montalbano & Pierre (2022), Weather shocks, traders’ expectations, and food prices — your primary benchmark. (Wiley Online Library)

Li & Ortiz-Bobea (2022), On the timing of relevant weather conditions in agriculture — crop-calendar identification. (Wiley Online Library)

Arellano, Juárez-Torres & Zazueta (2023), Weather Shocks, Prices and Productivity — shock severity and lag effects. (Bank of Mexico)

Cornejo, Merovich & Merener (2026), Hot dry spells and extreme rain increased corn and soybean prices — latest high-frequency benchmark. (Nature)

Jannat, Ishikawa-Ishiwata & Furuya (2021), Assessing the Impacts of Climate Variations on the Potato Production in Bangladesh. (MDPI)

Tier 2 — absolutely important for your Bangladesh model

Mila et al. (2023), onion price transmission.

Ahamed et al. (2021), potato cold storage and seasonal prices. (Bangladesh J. Agr. Economics)

Hossain et al. (2025), onion volatility/market integration.

Deb et al. (2020), Bangladesh rice supply/price transmission.

Brown & Kshirsagar (2015), developing-country local weather-price effects. (ScienceDirect)

Tier 3 — methods

Gasparrini, Armstrong & Kenward (2010), DLNM. (DOI)

Adjemian (2012), USDA information/event-study methodology. (Wiley Online Library)

Su, Liao & Chang (2025), DiD/event-study and expectation mechanisms. (ScienceDirect)

Dell, Jones & Olken (2014), weather econometrics.

Bhanumurthy, Dua & Kumawat (2013), weather → spot/futures price transmission. (IDEAS/RePEc)

Bottom line

The strongest defensible contribution is not discovering that pre-harvest weather can move prices. That has already been demonstrated internationally, most directly by Letta et al.

Your strongest contribution is to provide a Bangladesh-specific, market-level test of the pre-harvest weather-price expectation channel, using crop-calendar-based identification and higher-frequency weather/price data, while showing whether the response differs between onion and potato and whether storage, imports and market structure alter the response.

And the strongest empirical test is:

crop-specific panel FE + pre-harvest distributed weather lags + nonlinear shock severity + explicit post-harvest placebo/temporal separation, with event-study and DLNM specifications used as supporting evidence rather than as four competing main models.
