---
title: "Narrow but high-value primary-sector base"
section: economy
subpage: economic_structure
order: 1
updated: 2026-04-26
summary: >
  Tasman's economy rests on horticulture (around 22 percent of regional GDP), hops and viticulture (around 8 percent), tourism and recreation (around 11 percent), and aquaculture and forestry (around 6 percent), with manufacturing and services making up the remaining 45 percent. Headline unemployment is around 3.1 percent, below the national 3.8 percent.
status: draft
generated_from: problem.tasman.economy.economic_structure
---

# Narrow but high-value primary-sector base

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## A primary-sector economy with secondary support

Tasman's GDP is concentrated in a small number of land- and water-using industries: apples, kiwifruit, cherries, hops, wine, salmon, and tourism. Manufacturing largely exists to process the primary outputs (juice, packing, brewing, wine, smoked fish) (claim.tasman.economy.economic_structure_claim).


## Low headline unemployment is partly a labour-supply story

The 3.1 percent unemployment rate reflects a tight regional labour market in which horticulture and hospitality cannot find enough seasonal workers locally and depend on Recognised Seasonal Employer (RSE) and working-holiday inflows. The ratio is good news on the supply side and a constraint on the demand side.


---


## Drivers

The following structural drivers contribute to this problem.


### Primary-sector concentration in horticulture and viticulture



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus

### Seasonal labour dependence



- **Category:** demographic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing economy challenges.

**Flagship moves:**

- Implement evidence-based economy policy in Tasman
- Increase investment in economy services and infrastructure
- Build cross-sector partnerships to address economy challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for economy (state variable: `economy_outcome_index`, sign: +)
- Secondary intervention for economy (state variable: `economy_service_access`, sign: +)


### Response: Camp 2

A response strategy addressing economy challenges.

**Flagship moves:**

- Implement evidence-based economy policy in Tasman
- Increase investment in economy services and infrastructure
- Build cross-sector partnerships to address economy challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for economy (state variable: `economy_outcome_index`, sign: +)
- Secondary intervention for economy (state variable: `economy_service_access`, sign: +)


---

## Claims cited on this page

- **Tasman's economy rests on four primary pillars: horticulture (22% of regional GDP), hops and viticulture (8%), tourism and recreation (11%), and aquaculture/forestry (6%). Manufacturing and services comprise 45%; unemployment stands at 3.1% (2023), below national average of 3.8%.** [value: 3.1 percent unemployment; 2023] — Stats NZ Census 2023; Tasman District Council Annual Plan 2024.

---

## Further reading


- **Stats NZ Census 2023** — Stats NZ / Tatauranga Aotearoa (Statistics New Zealand), 2023 — <https://www.stats.nz/tools/census>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* primary_sector_gdp_share, regional_unemployment_rate.

*Constraints:* land_and_water_allocation_limits, single_export_corridor_dependence.

*Inputs:* rse_worker_intake, primary_processing_investment.


*Feedback loops:*

- `Primary-sector concentration raises regional exposure to commodity-price and biosecurity shocks, which periodically depresses investment in diversification.`


---

*Generated from `problem.tasman.economy.economic_structure` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
