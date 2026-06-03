---
title: "Native biodiversity loss and fragmentation"
section: environment
subpage: biodiversity
order: 2
updated: 2026-04-26
summary: >
  Native forest in Hawke's Bay has been reduced to fragmented remnants. Hawea and Kawekas forests are under pressure from logging, possum damage, and lack of active management. Endemic plant and bird species are endangered.
status: draft
generated_from: problem.hawkes_bay.environment.biodiversity
---

# Native biodiversity loss and fragmentation

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Forest Remnants

Native forest remnants in Hawke's Bay total approximately 45k hectares (24% of regional area), fragmented into isolated patches.


## Conservation Status

Hawea National Reserve is managed actively; Kawekas Forest Park has limited resources for predator control. Many endemic invertebrates and birds are classified as threatened.


---


## Drivers

The following structural drivers contribute to this problem.


### Agricultural irrigation demand exceeding sustainable supply



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Stormwater and runoff pollution control

Stormwater and runoff pollution control is the primary strategy.

**Flagship moves:**

- Implement Stormwater and runoff pollution control across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Stormwater and runoff pollution control intervention (state variable: `pollution_control_index`, sign: +) (relaxes: `pollution_control_constraint`)


---

## Claims cited on this page

- **Environmental degradation in Hawkes Bay includes habitat loss, water quality decline, invasive species pressure, and ecosystem fragmentation. Climate change amplifies these pressures; resource management and restoration efforts are constrained by funding and coordination gaps.** [value: 45000 hectares; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* native_forest_extent_hectares, conservation_predator_control_coverage_percent.

*Constraints:* forest_restoration_funding, land_use_competing_values.

*Inputs:* forest_harvesting_pressure, invasive_mammal_density.


*Feedback loops:*

- `Forest loss removes predator habitat; invasive species explode; native birds decline; ecosystem services degrade; restoration incentive weakens.`


---

*Generated from `problem.hawkes_bay.environment.biodiversity` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
