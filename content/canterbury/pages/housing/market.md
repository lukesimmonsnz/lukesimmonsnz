---
title: "Canterbury Housing Market Dysfunction"
section: housing
subpage: market
order: 1
updated: 2026-04-26
summary: >
  Canterbury's housing market exhibits chronic unaffordability across Christchurch, Waimakariri, and Selwyn districts, driven by post-earthquake rebuild dynamics, rapid greenfield-led growth in outer districts, and constrained density development in Christchurch CBD. Median multiples have stabilized around 6.5-7.0 regionally while local pressure zones (Selwyn, Waimakariri) face affordability crises for first-time buyers.

status: draft
generated_from: problem.canterbury.housing.market
---

# Canterbury Housing Market Dysfunction

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## The Canterbury earthquake dislocation

The 2010-2011 Canterbury earthquakes destroyed or damaged significant portions of the residential stock, with CERA demolishing over 8,000 red-zone homes. The rebuild phase (2012-2020) created one of NZ's strongest construction booms, but concentrated replacement housing in suburban greenfields (Waimakariri, Selwyn) rather than CBD intensification, raising long-run infrastructure servicing costs and suburban sprawl dependencies.


## Current affordability pressure

Despite earthquake-driven supply expansion, Christchurch's median multiple reached 7.1 in 2023 (claim.canterbury.housing.median_multiple_2023). Waimakariri and Selwyn face sharper affordability crises—first-time buyer deposits require 8-12 years of combined household savings—as in-migration from higher-cost centres (Auckland, Wellington) sustains demand while greenfield development runs ahead of infrastructure capacity (claim.canterbury.housing.infrastructure_gap_2024).


---


## Drivers

The following structural drivers contribute to this problem.


### Construction Cost Inflation



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus

### Government Employment Sector Concentration



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus

### Interest Rate Volatility & Mortgage Stress



- **Category:** economic
- **Timescale:** short
- **Consensus:** consensus

### Limited Developable Topography



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus

### Net Internal Migration (Auckland/Wellington to Christchurch)



- **Category:** demographic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Accelerated Greenfield Release & Growth Boundary Expansion

Expanding greenfield release in Waimakariri and Selwyn, if coordinated with infrastructure, offers affordable supply to meet demand.

**Flagship moves:**

- Key intervention for Accelerated Greenfield Release & Growth Boundary Expansion

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Expanding greenfield release in Waimakariri and Selwyn, if coordinated with infrastructure, offers affordable supply to meet demand. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


### Affordable Housing Quota & Developer Contribution Framework

Requiring developers to include affordable units (via discounted ownership or rental covenants) as a condition of resource consent embeds affordability into new supply.

**Flagship moves:**

- Key intervention for Affordable Housing Quota & Developer Contribution Framework

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Requiring developers to include affordable units (via discounted ownership or rental covenants) as a condition of resource consent embeds affordability into new supply. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


### Upzoning & Urban Intensification

Relaxing zoning restrictions and enabling medium-density development in Christchurch is the primary lever to improve affordability.

**Flagship moves:**

- Key intervention for Upzoning & Urban Intensification

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Relaxing zoning restrictions and enabling medium-density development in Christchurch is the primary lever to improve affordability. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


---

## Claims cited on this page

- **Canterbury's median multiple (median dwelling price divided by median annual household income) was 7.1 in 2023, an increase from 6.8 in 2020, reflecting sustained demand pressure from government employment and limited supply growth.** [value: 7.1 ratio (dimensionless); 2023] — Stats NZ Household Income and Housing Cost Statistics 2023; Demographia International Housing Affordability Survey 2024.
- **Canterbury housing affordability ratio (median price / median income) stands at 7.5-8.0x, above long-term sustainable levels of 5-6x. Christchurch rebuild has stalled in some areas; social housing needs are unmet.** [value: 2.5 NZD billions; 2024] *(confidence: medium)* — Waimakariri District Council Long-Term Plan 2024-2034; Selwyn District Council Long-Term Plan 2024-2034.
- **Following the 2010-2011 Canterbury earthquake sequence, the Crown offered to purchase approximately 8,000 residential properties on flat land within Christchurch where ground conditions were judged not economically viable to repair (the residential red zone). The red-zone offer programme transferred land ownership to the Crown, with subsequent stewardship moving to Otakaro Limited following CERA's disestablishment in 2016. Decisions on long-term reuse of red-zone land (recreation, conservation, residential redevelopment) remain a contested local-governance question.
** [value: 8000 residential properties offered Crown purchase; 2011-2017] — Canterbury Residential Red Zone - Programme Closure and Land Future Use.
- **QuakeCoRE - New Zealand's Centre of Research Excellence for earthquake resilience, hosted at the University of Canterbury - has produced the post-2011 evidence base on building performance during the Canterbury earthquake sequence. Its peer-reviewed research underpins current Building Code seismic provisions for unreinforced masonry, multi-storey reinforced concrete, and geotechnical liquefaction design - with Christchurch's residential and commercial rebuild serving as the working dataset for revised national standards.
** — QuakeCoRE - Centre of Research Excellence Annual Report.

---

## Further reading


- **Stats NZ Household Income and Housing Cost Statistics 2023** (Stats NZ), 2023 — <https://www.stats.govt.nz/information-releases/household-income-and-housing-cost-statistics-new-zealand-year-ended-june-2023>

- **Demographia International Housing Affordability Survey 2024** (Demographia), 2024 — <https://www.demographia.com/>

- **Waimakariri District Council Long-Term Plan 2024-2034** (Waimakariri District Council), 2024 — <https://www.waimakariri.govt.nz/our-council/planning/long-term-plan/>

- **Selwyn District Council Long-Term Plan 2024-2034** (Selwyn District Council), 2024 — <https://www.selwyn.govt.nz/our-council/planning/long-term-plan/>

- **Canterbury Residential Red Zone - Programme Closure and Land Future Use** — Otakaro Limited (Crown company) (New Zealand Government), 2017 — <https://www.otakaroltd.co.nz/>

- **QuakeCoRE - Centre of Research Excellence Annual Report** — QuakeCoRE (hosted by University of Canterbury) (University of Canterbury), 2023 — <https://www.quakecore.nz/>


---

## Technical notes

*State variables:* median_house_price_christchurch, median_house_price_waimakariri, median_house_price_selwyn, housing_affordability_ratio_regional, greenfield_release_uptake.

*Constraints:* earthquake_prone_building_remediation_cost, cera_red_zone_housing_loss, horizontal_infrastructure_debt, rural_land_availability.

*Inputs:* net_internal_migration, residential_building_consents, infrastructure_investment_rate, interest_rates.


*Feedback loops:*

- `Post-earthquake greenfield release: large suburban land release post-2011 temporarily dampened prices but growth management infrastructure costs now feedback into outer-district affordability.`
- `Rebuild momentum attenuation: strong construction sector capacity from earthquake rebuild sustains supply response but labour cost inflation erodes gains.`


---

*Generated from `problem.canterbury.housing.market` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
