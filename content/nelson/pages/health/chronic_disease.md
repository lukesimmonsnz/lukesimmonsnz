---
title: "Chronic-disease burden above national average"
section: health
subpage: chronic_disease
order: 3
updated: 2026-04-26
summary: >
  Around 26 percent of Nelson adults have at least one diagnosed chronic condition (against 22 percent nationally). Diabetes affects 8.1 percent (versus 7.2 percent), cardiovascular disease 11.3 percent (versus 10.1), and chronic respiratory disease 6.8 percent (versus 5.9). Maori and Pacific populations show 1.4-1.8x higher prevalence; obesity at around 42 percent of adults is a significant driver.
status: draft
generated_from: problem.nelson.health.chronic_disease
---

# Chronic-disease burden above national average

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## An older population layered on lifestyle drivers

Nelson's age structure skews older than national average, and demographic ageing alone explains part of the elevated chronic-disease prevalence (claim.nelson.health.chronic_disease_claim). Lifestyle factors (diet, activity, smoking and alcohol exposures over decades) account for a further share, with deprivation as the upstream driver of those exposures.


## Primary-care management capacity

Effective chronic-disease management depends on regular primary-care contact, which is undermined by GP shortage and cost barriers in lower-income households. The result is more avoidable hospital admissions and earlier complications than in regions with stronger primary care.


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

- **Chronic disease prevalence in Nelson is above national average. Health NZ data for 2023 reports that 26% of adults have been diagnosed with at least one chronic condition (vs. 22% nationally); diabetes affects 8.1% (vs. 7.2% nationally), cardiovascular disease 11.3% (vs. 10.1%), and chronic respiratory disease 6.8% (vs. 5.9%). Maori and Pacific populations have 1.4–1.8× higher prevalence rates. Rising obesity rates (42% of adults overweight or obese) are a significant driver; lifestyle factors interact with aging demographics.** [value: 26 percent of adults with chronic disease; 2023] — Health Outcomes Nelson Region 2023.

---

## Further reading


- **Health Outcomes Nelson Region 2023** — Health New Zealand (Health New Zealand), 2023 — <https://www.health.govt.nz>


---

## Technical notes

*State variables:* diabetes_prevalence_pct, cvd_prevalence_pct, avoidable_admission_rate.

*Constraints:* gp_workforce, social_determinants.

*Inputs:* primary_care_capacity, screening_programme_coverage.


*Feedback loops:*

- `Access-complication feedback: limited primary-care access reduces early management, raising downstream complications and hospital workload, which crowds out clinic capacity for population-level management.`


---

*Generated from `problem.nelson.health.chronic_disease` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
