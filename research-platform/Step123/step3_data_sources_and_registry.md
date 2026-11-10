# Step 3: Data Source Identification & Variable Registry

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

The single biggest methodological mistake to avoid is treating “growing season” as an arbitrary calendar window. The literature gives you a very strong reason to make the crop calendar itself part of the identification strategy. (Wiley Online Library)

Onion wholesale price

Main dependent variable

Market-level local onion wholesale price, date (t)

DAM market price system

Department of Agricultural Marketing

DAM Commodity-wise Report

Historical span exists, but full continuous market-level span not yet verified

Market / district / upazila selectable

Daily report system; historical query frequency requires extraction check

Web report / PDF; historical export format beyond PDF not fully verified

Public web query; 3-year windows per commodity query

Essential

Partially verified — exact historical panel needs direct extraction test

Onion retail price

Secondary outcome / robustness

Market-level local onion retail price

DAM

Department of Agricultural Marketing

DAM Commodity-wise Report

Historical span not fully verified

Market

Daily system; historical continuity needs check

Web/PDF

Public query

Optional but strongly recommended

Partially verified

Potato wholesale price

Main dependent variable

Market-level potato wholesale price

DAM

Department of Agricultural Marketing

DAM Commodity-wise Report

Historical span not fully verified

Market

Daily system; historical continuity needs check

Web/PDF

Public query

Essential

Partially verified

Potato retail price

Secondary outcome / robustness

Market-level potato retail price

DAM

Department of Agricultural Marketing

DAM Commodity-wise Report

Historical span not fully verified

Market

Daily system; historical continuity needs check

Web/PDF

Public query

Optional

Partially verified

Market identifier

Panel key

Stable DAM market identifier/name

DAM Market Directory

Department of Agricultural Marketing

DAM Market Directory

Current directory; historical ID persistence not verified

Market

Static/current

Web / Excel export

Public; Excel export advertised

Essential

Verified as directory field; longitudinal ID stability needs check

Market district/upazila

Weather and spatial matching

Administrative location associated with market

DAM Market Directory

DAM

DAM Market Directory

Current directory

Market → upazila/district

Static/current

Web / Excel

Public

Essential

Verified

Market coordinates

Weather-grid/station matching

Latitude/longitude of market

DAM directory or geocoded market

DAM primary source preferred

DAM Market Directory

Current

Market

Static

Exact coordinate export not verified

DAM directory public, but lat/lon availability not established

Essential

Not verified — requires direct source check

Market communication/accessibility

Transport/confounding control

DAM directory fields such as road linkage, vehicles, distance from district HQ

DAM Market Directory

DAM

DAM Market Directory

Current directory

Market

Static

Web/Excel

Public

Optional

Verified

Rainfall

Primary weather exposure

Daily/hourly precipitation matched to market/production geography

ERA5-Land hourly

Copernicus Climate Data Store / ECMWF

ERA5-Land Hourly

1950–present

Global 0.1° grid

Hourly

GRIB; time-series product NetCDF/CSV

Public, CC-BY

Essential

Verified

Temperature

Primary weather exposure

2-m air temperature; aggregate to relevant daily/stage metric

ERA5-Land hourly

Copernicus/ECMWF

ERA5-Land Hourly

1950–present

Global 0.1° grid

Hourly

GRIB / NetCDF / CSV depending product

Public

Essential

Verified

Extreme rainfall

Severity/shock variable

Indicator such as daily precipitation above a pre-defined extreme threshold; threshold must be chosen before analysis

Derived from ERA5-Land; optionally checked against BMD

ERA5-Land

ERA5-Land

1950–present

0.1°

Hourly → daily derived

Derived

Public source

Essential for RQ1b

Derived and feasible

Dry spell

Severity / adverse shock

Consecutive days below a rainfall threshold

Derived from ERA5-Land

ERA5-Land

ERA5-Land

1950–present

0.1°

Hourly → daily derived

Derived

Public

Essential for robustness / potentially primary shock

Derived and feasible

Drought indicator

Alternative weather shock

SPI/SPEI or standardized precipitation anomaly

BAMIS drought products and/or derived from ERA5 rainfall

BAMIS / ERA5-Land

BAMIS Crop & Weather System

BAMIS historical downloadable span not fully verified; ERA5-derived series 1950–present

BAMIS monitoring / ERA5 grid

BAMIS weekly/monthly products; ERA5 derived

Web/derived

BAMIS public interface; raw historical access not fully verified

Optional robustness

BAMIS product verified; full historical raw access not verified

Heat/extreme temperature

Severity variable

Number of days above pre-defined crop-relevant temperature threshold or high-temperature anomaly

Derived ERA5-Land

ERA5-Land

ERA5-Land

1950–present

0.1°

Hourly → daily

Derived

Public

Essential for robustness; useful for onion

Feasible

Humidity

Agronomic/weather control

Daily/stage humidity measure

ERA5-Land/BAMIS

Copernicus / BAMIS

BAMIS

ERA5 1950–present

Grid / BAMIS stations

Hourly or weekly/monthly product

Derived / web

Public ERA5; BAMIS historical raw access uncertain

Optional

Feasible via ERA5

Sunshine/radiation

Agronomic/weather control

Solar radiation/sunshine duration during crop stages

ERA5-Land/BAMIS

Copernicus / BAMIS

BAMIS

ERA5 1950–present

Grid

Hourly → daily

Derived

Public ERA5

Optional

Feasible

BMD rainfall

Ground-observation validation

Station-level observed rainfall

BMD Climate Data

Bangladesh Meteorological Department

BMD Climate Data Purchase

Official BMD documents show long historical station records; one database description covers 1948–2018, and station metadata in a 2024 report extend to 1961–2021

Station

Raw observation can be high frequency; exact delivery frequency depends requested product

Requested files; exact file format not guaranteed from portal

Paid/request-based, approved rates

Optional but valuable

Verified existence; raw historical access requires purchase/request

BMD temperature

Ground-observation validation

Station temperature observations

BMD

BMD

BMD Climate Data Purchase

Long historical station series documented

Station

Observation frequency depends requested series

Requested files

Paid/request

Optional

Verified existence; access not open bulk

BMD extreme rainfall

Validation of extreme-event classification

Extreme rainfall observed at stations

BMD climate resources / raw precipitation

BMD

BMD Climate Resources

Historical coverage not fully verified for a ready-made extreme series

Station

Daily/other depending requested data

Requested

Paid/request

Optional

Raw series obtainable in principle; ready-made historical product not verified

BMD station coordinates

Weather matching

Latitude/longitude and station identifier

BMD station metadata

BMD

BMD climate documentation

Historical metadata available in BMD reports

Station

Static

PDF/web

Public metadata

Essential if BMD used

Verified in BMD reports

Onion crop calendar

Core timing variable

Region-specific planting → growth stages → harvest window for onion

BAMIS Crop Weather Calendar

Department of Agricultural Extension / BAMIS

BAMIS Crop Weather Calendar

Current calendar products; specific PDF publication dates vary

Regional/district cluster

Weekly stage calendar

PDF/web

Public

Essential

Verified

Potato crop calendar

Core timing variable

Region-specific planting → sprouting/vegetative/tuber stages → maturity/harvest

BAMIS Crop Weather Calendar

DAE / BAMIS

Potato regional calendars

Current regional calendars; specific PDFs available

Regional/district cluster

Weekly

PDF/web

Public

Essential

Verified

Onion Kharif calendar

Additional seasonal crop window

100–110 day regional onion cycle

BAMIS

DAE/BAMIS

Dhaka Kharif Onion Calendar

Calendar published 2023

Regional

Weekly

PDF

Public

Essential where applicable

Verified

Onion Rabi calendar

Additional seasonal crop window

Rabi onion regional cycle and stage timing

BAMIS

DAE/BAMIS

Jashore Rabi Onion Calendar

Calendar published 2023

Regional

Weekly

PDF

Public

Essential where applicable

Verified

Potato crop calendar, Dhaka example

Crop stages

105-day Oct–Jan cycle with sprouting, vegetative growth, tuber initiation/bulking, maturity, harvest

BAMIS

DAE/BAMIS

Dhaka Potato Calendar PDF

PDF published 2019

Regional

Weekly

PDF

Public

Essential

Verified

Crop-region mapping

Determines which calendar applies to which market/production area

Region/district cluster → onion/potato crop calendar

BAMIS

DAE/BAMIS

Potato regional calendar index

Current

District cluster

Static

Web/PDF

Public

Essential

Verified

District crop-production area

Spatial exposure weighting / controls

Onion/potato harvested area or production by district/year

BBS Yearbook of Agricultural Statistics

Bangladesh Bureau of Statistics

BBS Agricultural Statistics Yearbooks

Yearbooks available through 2024

District/national; exact table resolution depends year

Annual

PDF/Excel depending publication

Public publications

Important / Optional

Verified dataset family; exact historical district series needs extraction

Crop production

Post-weather supply mechanism / exposure

Annual crop output

BBS

BBS

BBS Agriculture Statistics

Through recent annual yearbooks

District/national depending table

Annual

PDF/Excel

Public

Optional

Verified

Administrative boundaries

Spatial joins

District/upazila polygons

LGED GIS

Local Government Engineering Department

LGED GIS portal

Current

District/upazila etc.

Static

GIS/web; exact export format not verified

Public GIS map

Essential

Verified; exact download format needs source check

Road network

Transport/accessibility robustness

Road length/type/connectivity between production and market

LGED GIS

LGED

LGED Public Map

Current GIS; historical attribute depth varies

Road/administrative

Static

GIS/web export

Public

Optional

Verified

Weather grid identifier

Spatial join key

ERA5 cell containing market/production location

Derived from ERA5 + market coords

CDS/ECMWF

ERA5-Land

1950–present

0.1° grid

Static mapping

Derived

Public

Essential

Feasible once coordinates exist

Crop-weighted weather

Preferred exposure

Weather averaged across crop-production area relevant to market

Derived from ERA5 + BBS crop areas + GIS

ERA5 + BBS + GIS

Same official sources

Sample-period dependent

Grid weighted to production geography

Daily/hourly → study frequency

Derived

Public

Important

Feasible if crop-area data are adequate

Market-to-production distance

Transport/spatial mechanism

Geographic or road-network distance from relevant producing area to market

Derived from GIS

LGED + market/crop data

LGED GIS

Static or historical if road layer supports it

Market-production pair

Static / potentially time varying

Derived

Public

Optional

Feasible; exact production centroid definition must be established

Cold-storage locations

Potato mechanism

Location of operating cold-storage facilities

DAM cold-storage reports

DAM

DAM cold-storage reports

Recent reports verified (2022–2026); older series partly documented

Facility/district

Annual/seasonal

PDF/report

Public reports

Optional

Partially verified

Cold-storage capacity

Potato mechanism

Storage capacity by facility/district/year

DAM cold-storage reports

DAM

DAM reports

Annual reports verified; complete historical panel not verified

Facility/district/national

Annual/seasonal

Report/PDF

Public reports

Optional

Partially verified

Historical cold-storage aggregate capacity

Structural control

Number/capacity of cold stores over time

DAM annual reports

DAM

DAM reports

Historical annual values documented in DAM reporting; exact machine-readable series not verified

National, potentially regional

Annual

PDF

Public

Optional

Verified concept; extraction needed

Onion import quantity

Onion market control

Imported fresh/chilled onions, HS 070310, quantity over time

Bangladesh Customs/NBR trade statistics

NBR / Bangladesh Customs

Bangladesh Customs HS Chapter 07

Historical trade-stat series exist, but monthly market-level public extract not yet verified

National/importing country

Exact frequency available publicly not yet verified

Customs/statistics tables

Public statistics exist

Important for onion

HS definition verified; usable monthly historical panel not verified

Onion import value

Onion market control

Import value for HS 070310

NBR/Bangladesh Customs

NBR

Bangladesh Customs HS Chapter 07

Historical statistics exist

National

Exact usable frequency not yet verified

Trade-stat tables

Public statistics

Important

Partially verified

Onion import unit value

Stronger import control

Import value ÷ import quantity for HS 070310

Derived from NBR/customs

NBR / Customs

Bangladesh Customs

Depends on underlying import series

National

Monthly ideal; not yet verified

Derived

Public if component series available

Important

Derived; underlying monthly series requires check

USD/BDT exchange rate

Onion import control

Taka per USD reference/market exchange rate

Bangladesh Bank Open Data

Bangladesh Bank

Bangladesh Bank Open Data

Historical dataset reaches back to 1972

National

Historical / monthly and other series

Excel

Free public download

Important

Verified

India onion price

External-price control

Representative Indian onion price relevant to Bangladesh imports

Official India source would be required

Not yet securely verified in this inventory

—

—

Indian market

Ideally daily/weekly

—

—

Optional/important

Not verified — requires direct source check

Import-policy shock

Onion confounder

Indicator/date for tariff, restrictions, bans, quotas etc. affecting onion imports

NBR/Ministry of Commerce/Gazette

GoB

—

Historical dates not yet assembled

National

Event

PDF/gazette

Public notices but consolidated series not verified

Important robustness

Not verified — requires direct source check

Market arrivals

Supply mechanism / control

Volume arriving at market by date

DAM or market data source

DAM primary source preferred

—

—

Market

Daily/weekly desired

—

—

Optional

Not verified — requires direct source check

Market integration measure

Confounding / mechanism

Pre-period market-price linkage/integration measure

Derived from DAM price panel

DAM

DAM price system

Same as price panel

Market pair/network

Derived

Derived

No extra dataset

Optional

Feasible if price panel exists

Season/week-of-year

Essential calendar control

Week/month indicators

Derived from date

—

—

Full sample

Time

Weekly/daily

Derived

Free

Essential

Trivially feasible

Major holidays / Ramadan / Eid

Calendar control

Event-date indicators

Official calendar source or derived national calendar

Not separately verified here

—

Sample-dependent

National/date

Daily

Derived

—

Optional

Not required for baseline; can use calendar FE

CPI/inflation

General macro control

National consumer-price inflation

Bangladesh Bank/BBS

Bangladesh Bank Open Data

Bangladesh Bank Open Data

Long historical series

National

Monthly

Excel

Free

Optional

Verified dataset family

Fuel/transport-price index

Transport-cost control

Fuel/transport cost movement

Bangladesh Bank/BBS/official price series

Source family verified, exact preferred series not selected

—

—

National

Monthly

—

—

Optional

Not yet locked; not necessary for core
