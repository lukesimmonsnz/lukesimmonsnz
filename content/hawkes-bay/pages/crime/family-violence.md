---
title: "Family violence prevalence"
section: crime
subpage: family-violence
order: 2
updated: 2026-04-26
summary: >
  Family violence is a leading cause of death and injury for Hawke's Bay women and children. Housing stress, isolation in rural areas, and substance abuse are risk factors. Service capacity is limited.
status: draft
generated_from: problem.hawkes_bay.crime.family_violence
---

# Family violence prevalence

<p class="horizon-band">Analysis horizon: 10yr</p>



## Incident Rate

Police record approximately 2,100-2,400 family violence incidents annually in Hawke's Bay, affecting approximately 1,500+ households.


## Victim Support Gap

Shortage of women's shelter beds and counselling services limits victim options. Waiting lists for therapy are 6-12 months in some areas.


---


## Drivers

The following structural drivers contribute to this problem.


### Substance abuse and addiction drivers of property crime



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Substance abuse harm reduction and treatment

Substance abuse harm reduction and treatment is the primary strategy.

**Flagship moves:**

- Implement Substance abuse harm reduction and treatment across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Substance abuse harm reduction and treatment intervention (state variable: `harm_reduction_index`, sign: +) (relaxes: `harm_reduction_constraint`)


---

## Claims cited on this page

- **Family violence incidents in Hawke's Bay total approximately 2,250 per annum, with calls to NZ Police exceeding 3,000 annually due to repeat victimisation. Socioeconomic deprivation (particularly in Hastings and Wairoa) correlates with elevated family violence rates; prevention services and survivor support remain under-resourced relative to demand.** [value: 2250 incidents per annum; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* family_violence_incidents_per_annum, domestic_homicide_rate_per_capita.

*Constraints:* women_shelter_bed_capacity, counselling_service_availability.

*Inputs:* housing_stress_and_overcrowding, substance_abuse_correlation.


*Feedback loops:*

- `Violence escalates when victims lack exit options (housing, income); service shortages perpetuate victim trap.`


---

*Generated from `problem.hawkes_bay.crime.family_violence` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
