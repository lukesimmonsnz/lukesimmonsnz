---
title: "Wastewater collection and treatment"
section: infrastructure
subpage: wastewater
order: 2
updated: 2026-04-26
summary: >
  Wastewater treatment plants in Napier and Hastings operate near capacity. Aging pipes have high infiltration. Cyclone Gabrielle damaged treatment facilities. Expansion of capacity is deferred due to financing constraints and co-governance delays.
status: draft
generated_from: problem.hawkes_bay.infrastructure.wastewater
---

# Wastewater collection and treatment

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Capacity Constraints

Napier and Hastings wastewater plants currently operate at 85-90% capacity. Development contributions are insufficient to fund expansions.


## Asset Deterioration

Many gravity sewer mains are 50+ years old. Cyclone flooding damaged lining; infiltration rates are rising, overloading treatment plants.


---


## Drivers

The following structural drivers contribute to this problem.


### Aging pipe and infrastructure asset profiles



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Accelerated infrastructure renewal programme

Accelerated infrastructure renewal programme is the primary strategy.

**Flagship moves:**

- Implement Accelerated infrastructure renewal programme across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Accelerated infrastructure renewal programme intervention (state variable: `accelerated_renewal_index`, sign: +) (relaxes: `accelerated_renewal_constraint`)


---

## Claims cited on this page

- **Infrastructure in Hawkes Bay faces aging assets, deferred maintenance, and resilience gaps. Funding constraints limit system upgrades for climate adaptation, population growth, and earthquake/flood preparedness; coordination challenges delay critical projects.** [value: 87.5 percent capacity utilisation; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* treatment_plant_capacity_percent_used, pipe_condition_index.

*Constraints:* treatment_plant_siting_constraints, council_funding_availability.

*Inputs:* urban_intensification_demand, extreme_rainfall_infiltration.


*Feedback loops:*

- `Capacity constraints limit development; growth pressure increases; systems overflow; environmental damage increases regulatory burden.`


---

*Generated from `problem.hawkes_bay.infrastructure.wastewater` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
