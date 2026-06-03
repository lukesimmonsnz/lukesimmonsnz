---
title: "Housing market and affordability"
section: housing
subpage: housing-market
order: 1
updated: 2026-04-26
summary: >
  Taranaki housing is more affordable than national average median multiples (~5.2 vs 6.5 nationally), but housing stock quality varies. New Plymouth urban pressure is rising. Oil and gas sector wage dependence creates local housing affordability paradox: good wages but volatile employment.
status: draft
generated_from: problem.taranaki.housing.housing_market
---

# Housing market and affordability

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Affordability

Taranaki median multiple is approximately 5.2 (2024), below the national average of 6.8. However, housing stock quality and performance standards lag, with many older properties requiring insulation and heating upgrades.


## Employment Volatility

Oil and gas sector workers earn $130-150k annually during boom periods, supporting housing debt. Downturns leave workers vulnerable to mortgage stress.


---


## Drivers

The following structural drivers contribute to this problem.


### Oil and gas sector wage volatility



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Housing affordability support

Housing affordability support addresses housing_market.

**Flagship moves:**

- Implement Housing affordability support

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Housing affordability support action (state variable: `housing.affordability_support_index`, sign: +)


---

## Claims cited on this page

- **Housing quality and affordability pressures co-exist in Taranaki, with rental vacancies below 1-2% in urban areas. Essential workers (nurses, teachers, farm laborers) face housing stress, forcing commuting from more distant affordable areas or out-migration.** [value: 5.2 ratio; 2024] *(confidence: medium)* — Census 2023: Taranaki Regional Profile.

---

## Further reading


- **Census 2023: Taranaki Regional Profile** (Stats NZ), 2023


---

## Technical notes

*State variables:* median_multiple_ratio, housing_stock_quality_index.

*Constraints:* housing_construction_capacity, rural_infrastructure_servicing_cost.

*Inputs:* oil_gas_sector_wage_level, employment_volatility.


*Feedback loops:*

- `Sector downturn reduces wages; mortgagees struggle; housing market stagnates; investment defers.`


---

*Generated from `problem.taranaki.housing.housing_market` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
