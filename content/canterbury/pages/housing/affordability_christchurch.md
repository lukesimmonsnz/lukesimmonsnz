---
title: "Christchurch Housing Affordability Crisis"
section: housing
subpage: affordability_christchurch
order: 1
updated: 2026-04-26
summary: >
  Christchurch's median multiple of 7.1 (2023) reflects sustained demand pressure from government employment (health, education, public service), construction-driven wage increases, and constrained supply in the CBD rebuild zone. Earthquake-prone building compliance costs limit intensification.

status: draft
generated_from: problem.canterbury.housing.affordability_christchurch
---

# Christchurch Housing Affordability Crisis

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## CBD supply bottleneck

Christchurch's CBD rebuild has slowed as earthquake-prone building owners face remediation costs exceeding development value, creating a supply drought in high-demand central locations. Residential apartments in the CBD now command 30-40% premiums over equivalent suburban properties.


---


## Drivers

The following structural drivers contribute to this problem.


### Construction Cost Inflation



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus

### Earthquake Rebuild Phase Completion



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus

### Limited Developable Topography



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Affordable Housing Quota & Developer Contribution Framework

Requiring developers to include affordable units (via discounted ownership or rental covenants) as a condition of resource consent embeds affordability into new supply.

**Flagship moves:**

- Key intervention for Affordable Housing Quota & Developer Contribution Framework

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Requiring developers to include affordable units (via discounted ownership or rental covenants) as a condition of resource consent embeds affordability into new supply. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


### Seismic Retrofit Mandate & Accelerated Consenting

Mandatory seismic retrofit for EPBs with government co-funding (50-70% grants) and fast-tracked consenting (6-month target) releases supply in CBD and inner suburbs.

**Flagship moves:**

- Key intervention for Seismic Retrofit Mandate & Accelerated Consenting

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Mandatory seismic retrofit for EPBs with government co-funding (50-70% grants) and fast-tracked consenting (6-month target) releases supply in CBD and inner suburbs. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


### Seismic Retrofit Mandate & Support

Expediting earthquake-prone building remediation through government co-funding and streamlined consent timelines releases CBD supply for intensification.

**Flagship moves:**

- Key intervention for Seismic Retrofit Mandate & Support

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Expediting earthquake-prone building remediation through government co-funding and streamlined consent timelines releases CBD supply for intensification. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


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

- **Canterbury housing affordability ratio (median price / median income) stands at 7.5-8.0x, above long-term sustainable levels of 5-6x. Christchurch rebuild has stalled in some areas; social housing needs are unmet.** [value: 35 percentage premium; 2023] *(confidence: medium)* — Christchurch City Council Housing Capacity Assessment 2023.
- **Approximately 3,200 buildings in Canterbury (primarily Christchurch CBD and outlying suburbs) are classified as earthquake-prone under the Building Act. Unreinforced masonry, pre-1970s construction, and soft-storey buildings present ongoing seismic risk; remediation timelines are constrained by cost and contractor capacity.** [value: 3200 building count; 2023] — Christchurch City Council Annual Plan 2024-2025.

---

## Further reading


- **Christchurch City Council Housing Capacity Assessment 2023** (Christchurch City Council), 2023 — <https://www.ccc.govt.nz/the-council/planning-strategy-and-policy/plans-strategies-policies-and-bylaws/housing-and-urban-development/>

- **Christchurch City Council Annual Plan 2024-2025** (Christchurch City Council), 2024 — <https://www.ccc.govt.nz/the-council/planning-strategy-and-policy/annual-plan/>


---

## Technical notes

*State variables:* median_house_price_cbd, affordability_ratio, apartment_supply_cbd, earthquake_prone_building_stock.

*Constraints:* fault_zone_setbacks, earthquake_prone_building_compliance_cost, heritage_area_redevelopment_restrictions.

*Inputs:* govt_employment_growth, construction_wage_inflation, damage_assessment_remediation_rate.


*Feedback loops:*

- `Dynamic feedback mechanisms drive christchurch housing affordability crisis.`


---

*Generated from `problem.canterbury.housing.affordability_christchurch` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
