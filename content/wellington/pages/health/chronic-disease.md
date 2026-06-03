---
title: "Chronic disease burden in Wellington"
section: health
subpage: chronic-disease
order: 3
updated: 2026-04-26
summary: >
  Wellington carries a significant and growing burden of preventable chronic disease — diabetes, cardiovascular disease, and respiratory conditions — concentrated in high-deprivation communities in Porirua and Hutt Valley. The social determinants of health (housing, income, diet quality) drive the distribution of chronic disease more powerfully than healthcare access alone.
status: draft
generated_from: problem.wellington.health.chronic_disease
---

# Chronic disease burden in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Diabetes concentration in Porirua

Diabetes prevalence in Porirua is substantially above the Wellington regional average, reflecting the interaction of ethnicity, diet, housing conditions, and access to preventive healthcare in this community (claim.wellington.health.diabetes_prevalence_porirua).


## Preventable hospitalisations

Wellington records elevated rates of preventable hospitalisations — for ambulatory-care-sensitive conditions including poorly controlled diabetes, asthma, and cellulitis — in high-deprivation sub-areas, indicating failures of primary and preventive care (claim.wellington.health.preventable_hospitalisations).


---


## Drivers

The following structural drivers contribute to this problem.


### Gaps in preventive and primary chronic disease care



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus

### Social determinants of health in high-deprivation communities



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Chronic Disease Prevention Through Healthy Environments

Reducing chronic disease burden requires upstream action on food environments, physical activity infrastructure, and tobacco/alcohol availability.

**Flagship moves:**

- Restrict fast food outlets near schools
- Subsidised healthy food access in high-deprivation areas
- Smokefree generation policy enforcement in Wellington

**Tensions:**

- Regulatory interventions on food and retail face industry resistance and local economic concerns
- Effectiveness varies by deprivation; universal policies may miss highest-risk groups

**Interventions on the system:**

- Establish 500m exclusion zone for new fast food outlets near schools across Wellington City (state variable: `unhealthy_food_environment_density`, sign: -)


### Primary Care Capacity Expansion

Expanding GP and nurse-led primary care capacity in under-served Wellington areas reduces ED pressure and improves chronic disease management.

**Flagship moves:**

- Establish urgent care hubs in Porirua and Hutt Valley
- Increase Very High Needs funding for practices in high-deprivation areas
- Nurse practitioners as first-contact providers with full prescribing rights

**Tensions:**

- GP workforce shortage limits supply-side expansion regardless of funding
- Urgent care hubs without continuity of care risk fragmentation

**Interventions on the system:**

- Open 3 new urgent care hubs in Porirua, Lower Hutt, and Wainuiomata co-located with community health workers (state variable: `primary_care_access_rate`, sign: +)


---

## Claims cited on this page

- **Diabetes prevalence in Porirua is substantially above the Wellington regional average, reflecting the interaction of ethnicity (high Māori and Pacific populations), diet, housing conditions, and constrained access to preventive healthcare.** *(confidence: medium)* — Health New Zealand Te Whatu Ora Wellington Region Annual Report 2022/23; Census 2023: Wellington Regional Profile.
- **Wellington records elevated rates of preventable hospitalisations for ambulatory-care-sensitive conditions — including poorly controlled diabetes, asthma, and cellulitis — in high-deprivation sub-areas, indicating failures of primary and preventive care in these communities.** *(confidence: medium)* — Health New Zealand Te Whatu Ora Wellington Region Annual Report 2022/23.

---

## Further reading


- **Health New Zealand Te Whatu Ora Wellington Region Annual Report 2022/23** (Health New Zealand), 2023 — <https://www.tewhatuora.govt.nz/>

- **Census 2023: Wellington Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* diabetes_prevalence_rate, preventable_hospitalisation_rate.

*Constraints:* healthy_food_affordability, safe_active_travel_infrastructure.

*Inputs:* diet_quality, physical_activity_level.


*Feedback loops:*

- `Deprivation-disease amplification: poverty limits diet quality and safe physical activity; poorer health reduces workforce participation; reduced income deepens poverty.`


---

*Generated from `problem.wellington.health.chronic_disease` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
