---
title: "Economic structure and sector concentration"
section: economy
subpage: economic-structure
order: 1
updated: 2026-04-26
summary: >
  Hawke's Bay economy is heavily concentrated in agriculture, horticulture, and primary industries. Manufacturing and services are underdeveloped. Dependency on primary commodity export prices creates volatility. Economic diversification is slow.
status: draft
generated_from: problem.hawkes_bay.economy.economic_structure
---

# Economic structure and sector concentration

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Sector Dominance

Agriculture, horticulture, and food processing account for approximately 22% of Hawke's Bay GDP and 28% of employment — double the national average.


## Volatility

Apple prices, wine prices, and dairy commodity prices drive Hawke's Bay GDP volatility 1.5x higher than national average. Recent wine industry downturn (2023-2025) cost 400+ jobs.


---


## Drivers

The following structural drivers contribute to this problem.


### Export commodity price volatility



- **Category:** economic
- **Timescale:** short
- **Consensus:** consensus

### High transport costs reducing export competitiveness



- **Category:** institutional
- **Timescale:** long
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


### Horticulture sector support and value-add

Horticulture sector support and value-add is the primary strategy.

**Flagship moves:**

- Implement Horticulture sector support and value-add across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Horticulture sector support and value-add intervention (state variable: `sector_support_index`, sign: +) (relaxes: `sector_support_constraint`)


---

## Claims cited on this page

- **Agriculture and horticulture generate approximately 22% of Hawke's Bay's gross regional product, compared to the national average of 6%. This concentration spanning wine (Gimblett Gravels, Dartmoor), apples, and kiwifruit creates vulnerability to commodity price fluctuations, climatic shocks (drought, flooding), and trade policy disruptions. The wine sector contributes NZD 220M+ to regional income annually.** [value: 22 percent of gross regional product; 2023] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* agricultural_gdp_share_percent, economic_diversity_herfindahl_index.

*Constraints:* transport_cost_to_markets, labour_skill_mismatch.

*Inputs:* primary_industry_capital_intensity, export_price_volatility.


*Feedback loops:*

- `Commodity downturn reduces tax base; business investment falls; diversification deferred; dependency deepens.`


---

*Generated from `problem.hawkes_bay.economy.economic_structure` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
