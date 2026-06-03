---
title: "Sharply rising mental-health demand"
section: health
subpage: mental_health
order: 2
updated: 2026-04-26
summary: >
  About 28 percent of Nelson residents report symptoms of depression or anxiety against around 20 percent nationally, with primary-care presentations up 34 percent between 2019 and 2023. Specialist mental-health waiting times average 12-14 weeks; crisis-line volumes rose 42 percent year-on-year in 2022-2023. Youth (18-24) anxiety symptom prevalence is around 38 percent, and the age-standardised suicide rate of 16.2 per 100,000 is well above the national 12.8.
status: draft
generated_from: problem.nelson.health.mental_health
---

# Sharply rising mental-health demand

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Demand growth and capacity wall

Nelson's mental-health system was already running at capacity before COVID and has absorbed a step-change in demand since (claim.nelson.health.mental_health_claim). The waitlist for specialist assessment is now the binding operational constraint, with primary care effectively holding crisis cases that would historically have moved into specialist care.


## Suicide rate and youth pressure

An age-standardised suicide rate well above national average is a serious regional pattern, concentrated in younger cohorts and in deprivation-affected areas. Youth mental health intersects with school disengagement and alcohol-and-drug use; isolated rural settings amplify exposure.


---


## Drivers

The following structural drivers contribute to this problem.


### Health-workforce supply gap in a small region



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

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

- **Mental health service demand in Nelson has increased sharply post-COVID. Health NZ reports 28% of Nelson residents reporting symptoms of depression or anxiety (vs. 20% nationally), with presentation rates to primary care increasing 34% 2019-2023. Waiting times for specialist mental health assessment average 12–14 weeks; crisis line call volumes increased 42% year-on-year 2022-2023. Youth mental health presentation rates are particularly acute; 18–24 age group shows 38% prevalence of anxiety symptoms. Suicide rate (age-standardized) is 16.2 per 100,000 population (national 12.8).** [value: 28 percent reporting depression or anxiety; 2023] *(confidence: medium)* — Health Outcomes Nelson Region 2023.

---

## Further reading


- **Health Outcomes Nelson Region 2023** — Health New Zealand (Health New Zealand), 2023 — <https://www.health.govt.nz>


---

## Technical notes

*State variables:* specialist_mh_waitlist_weeks, crisis_call_volume_per_month, age_std_suicide_rate_per_100k.

*Constraints:* specialist_workforce_supply, rural_service_reach.

*Inputs:* mh_funding_envelope, youth_mh_navigator_capacity.


*Feedback loops:*

- `Waitlist-deterioration feedback: long waits push moderate cases toward acute presentation, which absorbs more crisis capacity, which lengthens the waitlist for moderate cases.`


---

*Generated from `problem.nelson.health.mental_health` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
