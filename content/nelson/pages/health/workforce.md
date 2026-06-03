---
title: "Critical health workforce shortages"
section: health
subpage: workforce
order: 4
updated: 2026-04-26
summary: >
  Nelson's GP-to-patient ratio is around 1 per 1,900 against a national target of 1 per 1,400. Nursing vacancies are around 8 percent of funded FTE; specialist shortages mean patients are referred to Christchurch or Wellington. About 14 percent of GPs are over 60 with planned retirement in the next five years, and graduate retention from NMIT health-workforce programmes is around 42 percent against 58 percent nationally.
status: draft
generated_from: problem.nelson.health.workforce
---

# Critical health workforce shortages

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## A retiring core and thin pipeline

The single most important workforce statistic is that 14 percent of Nelson GPs plan to retire within five years with no clear replacement pipeline (claim.nelson.health.workforce_claim). Nursing vacancies are similar in shape: stable demand and a slow-moving supply funnel.


## Retention versus recruitment

NMIT trains health workers competently but only retains around 42 percent in the region after qualification. The drivers are housing affordability, career-path narrowness outside the hospital, and partner-employment opportunities. Recruitment campaigns alone cannot offset the retention gap.


---


## Drivers

The following structural drivers contribute to this problem.


### Demographic ageing and concentrated deprivation



- **Category:** demographic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing health challenges.

**Flagship moves:**

- Implement evidence-based health policy in Nelson
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

- **Health workforce shortages in Nelson are a critical constraint. Nelson only has 1 per 1,900 patients vs. national target of 1 per 1,400; nursing vacancies are 8% of funded FTE positions, and specialist shortages (psychiatrists, cardiologists, geriatricians) mean patients are referred to Christchurch or Wellington, creating delays and access equity issues. Rural and outer-suburb clinics struggle with recruitment; 14% of GPs are >60 years old with planned retirement in the next 5 years. Health workforce development capacity at NMIT is adequate but graduate retention is 42% (vs. 58% nationally).** [value: 8 percent nursing FTE vacancy rate; 2023] *(confidence: medium)* — Health Outcomes Nelson Region 2023.

---

## Further reading


- **Health Outcomes Nelson Region 2023** — Health New Zealand (Health New Zealand), 2023 — <https://www.health.govt.nz>


---

## Technical notes

*State variables:* gp_to_patient_ratio, nursing_vacancy_rate_pct, nmit_health_grad_retention_pct.

*Constraints:* housing_affordability, career_pathway_depth.

*Inputs:* health_nz_workforce_funding, graduate_placement_settings.


*Feedback loops:*

- `Workforce-load feedback: thin workforce raises load on existing staff, accelerating burnout and exit, which deepens the workforce gap.`


---

*Generated from `problem.nelson.health.workforce` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
