---
title: "Variation in health outcomes by ethnicity and deprivation"
section: health
subpage: health_outcomes
order: 1
updated: 2026-04-26
summary: >
  Life expectancy in Nelson is 79.2 years for Pakeha and 74.1 years for Maori (a 5.1-year gap). Infant mortality runs around 6.2 per 1,000 live births overall but 9.4 per 1,000 for Maori infants in Nelson district. Hospital admissions for acute and preventable conditions are around 12 percent above national average, and access is constrained by GP shortages and elective-procedure waiting times averaging 16 weeks.
status: draft
generated_from: problem.nelson.health.health_outcomes
---

# Variation in health outcomes by ethnicity and deprivation

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Headline outcomes mask within-region gaps

Average outcomes for Nelson are reasonable on a national comparison but conceal substantial gaps by deprivation decile and ethnicity (claim.nelson.health.health_outcomes_claim). The 5-year life-expectancy gap is the most visible single indicator and is structurally similar to the national Maori-Pakeha gap.


## Access as a structural limit

GP-to-patient ratios in Nelson sit around 1:1,900 against a national target of 1:1,400. That access constraint shows up downstream as later presentation, more acute admissions, and worse outcomes for chronic conditions that benefit from early management.


---


## Drivers

The following structural drivers contribute to this problem.


### Demographic ageing and concentrated deprivation



- **Category:** demographic
- **Timescale:** long
- **Consensus:** consensus

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

- **Overall health outcomes in Nelson show variation by ethnicity and deprivation. Life expectancy is 79.2 years for Pakeha and 74.1 years for Maori (5.1-year gap); infant mortality is 6.2 per 1,000 live births nationally but 9.4 per 1,000 for Maori infants in Nelson district. Hospital admission rates for acute and preventable conditions are 12% above national average. Health service access is constrained by GP shortages (ratios 1:1,900 patients vs. 1:1,400 nationally) and waiting times for elective procedures averaging 16 weeks.** [value: 5.1 year life expectancy gap (Maori vs Pakeha); 2023] — Health Outcomes Nelson Region 2023.

---

## Further reading


- **Health Outcomes Nelson Region 2023** — Health New Zealand (Health New Zealand), 2023 — <https://www.health.govt.nz>


---

## Technical notes

*State variables:* life_expectancy_years_total, life_expectancy_gap_years, asis_admission_rate_per_1000.

*Constraints:* gp_supply, elective_capacity.

*Inputs:* primary_care_funding, specialist_workforce_supply.


*Feedback loops:*

- `Access-acuity feedback: limited primary-care access raises the share of conditions presenting acutely, increasing hospital load and crowding out the elective capacity that would relieve primary care.`


---

*Generated from `problem.nelson.health.health_outcomes` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
