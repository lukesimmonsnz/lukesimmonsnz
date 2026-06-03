---
title: "Productivity challenges in Wellington's economy"
section: economy
subpage: productivity
order: 3
updated: 2026-04-26
summary: >
  Wellington's labour productivity is moderate by OECD standards and is held back by the high share of public sector activity — which is measured by inputs rather than outputs — and by limited private sector innovation investment. Compared to Auckland, Wellington's private sector has a narrower economic base for productivity-enhancing investment.
status: draft
generated_from: problem.wellington.economy.productivity
---

# Productivity challenges in Wellington's economy

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Productivity relative to OECD peers

Wellington's labour productivity index is below comparable capital-city regions in Australia and Western Europe, reflecting both the structure of the local economy and Wellington's distance from large markets (claim.wellington.economy.labour_productivity_index).


## Public sector measurement drag

The high share of public sector employment in Wellington's GDP contributes to measured productivity stagnation, since government services are measured at input cost rather than market value — understating real economic output but inflating the apparent productivity gap (claim.wellington.economy.productivity_public_sector_drag).


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic distance from export markets



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus

### Input-cost GDP measurement of government output



- **Category:** institutional
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Agglomeration and CBD Vitality Investment

Wellington's compact urban core is its productivity asset; investment in CBD amenity, housing, and walkability will attract and retain high-productivity workers.

**Flagship moves:**

- CBD housing intensification to increase resident population in central suburbs
- Improved international connectivity through Wellington Airport capacity
- Cultural and event infrastructure investment to sustain Wellington's liveability premium

**Tensions:**

- Airport expansion raises carbon emissions and community noise objections
- Cultural amenity investment may not translate to productivity gains

**Interventions on the system:**

- Approve and fund Wellington CBD intensification overlay to double CBD resident population by 2040 (state variable: `cbd_employment_density`, sign: +)


### Innovation and Productivity Investment

Targeted R&D investment and technology adoption support for Wellington SMEs will lift productivity and reduce the public sector dependency risk.

**Flagship moves:**

- R&D tax credit uptake campaign for Wellington businesses
- Digital transformation support fund for SMEs through NZTE
- University-industry research partnership fund at Victoria University of Wellington

**Tensions:**

- R&D tax credits disproportionately benefit larger firms with existing R&D capability
- SME digital transformation requires management capability, not just capital

**Interventions on the system:**

- Wellington SME Digital Transformation Fund providing $30k matching grants to 200 Wellington businesses (state variable: `wellington_sme_productivity_index`, sign: +)


---

## Claims cited on this page

- **Wellington's labour productivity index is below comparable capital-city regions in Australia and Western Europe, reflecting the structure of the local economy, distance from large export markets, and the measurement drag of the large public sector.** *(confidence: medium)* — Treasury Budget Economic and Fiscal Update 2024.
- **The high share of public sector employment in Wellington's economy contributes to measured productivity stagnation, because government services are measured at input cost rather than market value — understating real economic output but inflating the apparent productivity gap relative to private-sector-dominated cities.** *(confidence: medium)* — Treasury Budget Economic and Fiscal Update 2024.

---

## Further reading


- **Treasury Budget Economic and Fiscal Update 2024** (NZ Treasury), 2024 — <https://www.treasury.govt.nz/publications/efu>


---

## Technical notes

*State variables:* labour_productivity_index, private_sector_rd_intensity.

*Constraints:* small_domestic_market, public_sector_gdp_measurement_drag.

*Inputs:* innovation_investment, digital_transformation_rate.


*Feedback loops:*

- `Productivity-investment loop: low productivity limits retained earnings and investment capacity; low investment sustains low productivity.`


---

*Generated from `problem.wellington.economy.productivity` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
