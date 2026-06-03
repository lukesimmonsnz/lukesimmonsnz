---
title: "Higher-than-national chronic-disease burden"
section: health
subpage: chronic_disease
order: 3
updated: 2026-04-26
summary: >
  Type 2 diabetes prevalence in Tasman runs at 6.8 percent of adults, against a national 5.9 percent. Cardiovascular mortality is around 18 percent above the national age-standardised rate, and adult obesity prevalence is roughly 32 percent, concentrated in Motueka and rural farming communities.
status: draft
generated_from: problem.tasman.health.chronic_disease
---

# Higher-than-national chronic-disease burden

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Prevalence above national average

Tasman's chronic-disease numbers are not catastrophically out of line with New Zealand as a whole, but they are consistently on the wrong side of the national average for diabetes, cardiovascular disease, and obesity (claim.tasman.health.chronic_disease_claim).


## Primary-care load follows the prevalence

A higher chronic-disease prevalence translates into a heavier primary-care workload per capita: more long-term-conditions reviews, more medication, more allied-health input. With the GP-to-population ratio sitting around 1:2,200 against a national 1:1,800, the per-clinician burden is meaningfully higher than the headline ratio alone suggests.


---


## Drivers

The following structural drivers contribute to this problem.


### Rural clinician recruitment and retention deficit



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing health challenges.

**Flagship moves:**

- Implement evidence-based health policy in Tasman
- Increase investment in health services and infrastructure
- Build cross-sector partnerships to address health challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for health (state variable: `health_outcome_index`, sign: +)
- Secondary intervention for health (state variable: `health_service_access`, sign: +)


---

## Claims cited on this page

- **Health NZ Tasman (2023) reports Type 2 diabetes prevalence at 6.8% (age 15+), above national average of 5.9%. Cardiovascular disease mortality is 18% above national age-standardised rate. Obesity prevalence stands at 32%, linked to socioeconomic deprivation in Motueka and rural farming communities.** [value: 6.8 percent diabetes prevalence; 2023] — Health Outcomes Tasman Region 2023; Stats NZ Census 2023.

---

## Further reading


- **Health Outcomes Tasman Region 2023** — Health New Zealand (Health New Zealand), 2023 — <https://www.health.govt.nz>

- **Stats NZ Census 2023** — Stats NZ / Tatauranga Aotearoa (Statistics New Zealand), 2023 — <https://www.stats.nz/tools/census>


---

## Technical notes

*State variables:* type2_diabetes_prevalence, cv_mortality_rate.

*Constraints:* deprivation_distribution, rural_food_environment.

*Inputs:* primary_prevention_programmes, screening_coverage.


*Feedback loops:*

- `High chronic-disease load consumes primary-care capacity that would otherwise prevent the next cohort of cases.`


---

*Generated from `problem.tasman.health.chronic_disease` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
