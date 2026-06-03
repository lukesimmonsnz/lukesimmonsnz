---
title: "Population health outcomes and inequities"
section: health
subpage: health-outcomes
order: 1
updated: 2026-04-26
summary: >
  Hawke's Bay has poorer population health outcomes than national average and significant health inequities. Māori experience higher mortality and morbidity. Mental health crisis is acute post-Cyclone Gabrielle. Chronic disease prevalence is high.
status: draft
generated_from: problem.hawkes_bay.health.health_outcomes
---

# Population health outcomes and inequities

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Life Expectancy Gap

Hawke's Bay life expectancy is approximately 79 years, approximately 2 years below national average. Māori life expectancy in Hawke's Bay is 73 years.


## Mental Health Crisis

Cyclone Gabrielle triggered sustained mental health impacts. Anxiety and depression diagnoses increased 40% in 2023. Suicide rates have risen.


---


## Drivers

The following structural drivers contribute to this problem.


### Cyclone-related mental health trauma and sustained stress



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus

### Limited preventive care and health promotion investment



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Community-based mental health and peer support

Expanding community-based mental health services, peer support networks, and social connection reduces reliance on stretched clinical services and improves resilience.

**Flagship moves:**

- Fund community health workers in Flaxmere and rural areas to provide low-barrier mental health support
- Support peer-led recovery groups and kaupapa Maori healing circles
- Integrate mental health screening into primary care and employ therapists in GP practices

**Tensions:**

- Community-based care requires ongoing funding and may be seen as underfunding clinical services
- Peer support is insufficient for acute mental illness or crisis

**Interventions on the system:**

- Fund 20 community mental health workers across the region (state variable: `community_mental_health_access`, sign: +)
- Establish peer support network with 50 trained peer workers (state variable: `mental_health_peer_support_coverage`, sign: +)


### Primary care service expansion

Primary care service expansion is the primary strategy.

**Flagship moves:**

- Implement Primary care service expansion across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Primary care service expansion intervention (state variable: `primary_care_expansion_index`, sign: +) (relaxes: `primary_care_expansion_constraint`)


---

## Claims cited on this page

- **Health service access in Hawkes Bay is constrained by workforce shortage and geographic isolation. Nursing vacancies and GP shortages are acute in rural areas; specialist services require travel, delaying diagnoses and treatment for chronic and acute conditions.** [value: 79 years; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.
- **Mental health diagnoses increased 40% in Hawke's Bay 2019-2023, outpacing national growth (25%), reflecting post-COVID mental health crisis and Cyclone Gabrielle (2023) psychological impacts. Demand for primary mental health services exceeds supply; waitlists in Napier and Hastings exceed 8 weeks; rural Wairoa residents lack local counselling access (requires 90+ min travel to Napier). Māori mental health prevalence and suicide rates significantly elevated.** [value: 40 percent increase; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* life_expectancy_years, amenable_mortality_rate_per_capita.

*Constraints:* health_service_funding, workforce_availability.

*Inputs:* deprivation_concentration, healthcare_access_barriers.


*Feedback loops:*

- `Poor health reduces workforce participation; earnings fall; ability to afford healthcare declines; health worsens.`


---

*Generated from `problem.hawkes_bay.health.health_outcomes` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
