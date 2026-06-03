---
title: "Economic diversification and sector development"
section: economy
subpage: economic-diversification
order: 2
updated: 2026-04-26
summary: >
  Hawke's Bay has limited success diversifying away from agriculture. Services sector growth is slower than national average. Advanced manufacturing and technology sectors are underdeveloped. Investment in new growth sectors is insufficient.
status: draft
generated_from: problem.hawkes_bay.economy.economic_diversification
---

# Economic diversification and sector development

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Diversification Lag

Services sector in Hawke's Bay is 48% of employment, compared to 56% nationally. Technology and advanced manufacturing account for <3% of employment.


## Investment Gap

Private sector R&D investment in Hawke's Bay is approximately $45 million annually, compared to $200+ million per capita equivalent in Wellington or Auckland.


---


## Drivers

The following structural drivers contribute to this problem.


### Export commodity price volatility



- **Category:** economic
- **Timescale:** short
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Economic diversification into services and technology

Strategic investment in technology, services, and advanced manufacturing sectors reduces commodity dependence and creates sustainable growth.

**Flagship moves:**

- Establish Hawke's Bay Innovation Hub to incubate tech startups and support R&D
- Incentivise remote workers and digital nomads to relocate to Napier and Hastings
- Develop food and wine tourism products as high-margin services

**Tensions:**

- Tech sector development requires workforce upskilling and may attract talent out of traditional industries
- Innovation hubs require sustained public investment with uncertain returns

**Interventions on the system:**

- Invest $50 million in innovation hub infrastructure and business support for emerging sectors (state variable: `services_sector_gdp_share`, sign: +)
- Offer immigration incentives and fast-track visas for digital workers (state variable: `technology_sector_employment_growth`, sign: +)


---

## Claims cited on this page

- **Services sector employment in Hawke's Bay accounts for 48% of total employment, indicating modest diversification beyond agriculture and horticulture. Wholesale and retail, hospitality, and healthcare are growing; however, commodity price exposure (wine, fruit, dairy) remains dominant in gross regional income, limiting economic resilience to market shocks.** [value: 48 percent employment share; 2023] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* services_sector_gdp_share_percent, technology_sector_employment_count.

*Constraints:* infrastructure_and_skills_readiness, market_proximity_distance.

*Inputs:* business_capability_gaps, access_to_capital_constraints.


*Feedback loops:*

- `Skills gaps and capital constraints limit new sector development; entrepreneurs relocate; brain drain follows; diversity prospects dim.`


---

*Generated from `problem.hawkes_bay.economy.economic_diversification` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
