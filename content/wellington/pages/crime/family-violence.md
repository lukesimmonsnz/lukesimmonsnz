---
title: "Family violence prevalence in Wellington"
section: crime
subpage: family-violence
order: 2
updated: 2026-04-26
summary: >
  Family violence is the most prevalent form of serious crime in Wellington, with high call volumes to police in Porirua and parts of Hutt Valley. Housing stress, economic hardship, alcohol and drug use, and a system that historically underresponds are the dominant drivers. Intergenerational transmission of family violence is a major policy concern.
status: draft
generated_from: problem.wellington.crime.family_violence
---

# Family violence prevalence in Wellington

<p class="horizon-band">Analysis horizon: 10yr</p>



## Police call volumes

Wellington Police District responds to family harm call-outs at a rate substantially above the national average in Porirua sub-areas, reflecting both elevated incidence and a community that has been encouraged to report (claim.wellington.crime.fv_police_call_rate).


## Housing stress and violence nexus

Wellington research consistently finds elevated family violence in households under acute housing cost stress — overcrowded, insecure, or unaffordable housing — indicating that the housing affordability crisis directly compounds family violence incidence (claim.wellington.crime.fv_housing_stress_link).


---


## Drivers

The following structural drivers contribute to this problem.


### Housing stress as family violence driver



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus

### Repeat victimisation concentration in family harm contexts



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus

### Substance use and family violence co-occurrence



- **Category:** cultural
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Family Violence System Reform

An integrated family violence response system with perpetrator accountability and victim support pathways will reduce recurrence.

**Flagship moves:**

- Te Aorerekura (National Strategy) full implementation in Wellington
- Integrated Safety Response (ISR) programme expansion to all Wellington territorial authorities
- Perpetrator-focused intervention programme funding with clear accountability measures

**Tensions:**

- System reform requires sustained cross-agency coordination that is institutionally difficult
- Perpetrator programmes require significant voluntary participation and have variable completion rates

**Interventions on the system:**

- Fully resource Integrated Safety Response in all Wellington TAs with co-location of Police, MSD, and health navigators (state variable: `family_violence_recurrence_rate`, sign: -)


### Safe Housing for Family Violence Survivors

Housing insecurity is a primary barrier to leaving abusive situations; emergency and transitional housing supply must be urgently expanded.

**Flagship moves:**

- 24/7 emergency refuge capacity in all Wellington districts
- Rapid rehousing fund with Kāinga Ora priority allocation for FV survivors
- Landlord engagement programme to reduce discrimination against FV survivors

**Tensions:**

- Housing supply constraints mean priority allocation displaces other vulnerable groups
- Emergency accommodation does not address perpetrator behaviour

**Interventions on the system:**

- Fund 50 additional emergency FV refuge beds across Wellington region with specialist support staffing (state variable: `fv_emergency_housing_capacity`, sign: +)


---

## Claims cited on this page

- **Wellington Police District records family harm callout rates in Porirua sub-areas substantially above the Wellington district average, reflecting elevated incidence driven by housing stress, substance use, and economic hardship in high-deprivation communities.** — New Zealand Police Crime Statistics 2022/23: Wellington District; Family Violence Statistics: New Zealand 2023.
- **Wellington research indicates elevated family violence incidence in households under acute housing cost stress — overcrowded, insecure, or unaffordable housing — directly linking the housing affordability crisis to family violence outcomes.** *(confidence: medium)* — Family Violence Statistics: New Zealand 2023; Stats NZ Household Income and Housing Cost Statistics 2023.

---

## Further reading


- **New Zealand Police Crime Statistics 2022/23: Wellington District** (New Zealand Police), 2023 — <https://www.police.govt.nz/about-us/publications-statistics/data-and-statistics/policedatanz/victimisation-timeseries>

- **Family Violence Statistics: New Zealand 2023** (Ministry of Social Development), 2023 — <https://www.msd.govt.nz/about-msd-and-our-work/publications-resources/research/family-violence/>

- **Stats NZ Household Income and Housing Cost Statistics 2023** (Stats NZ), 2023 — <https://www.stats.govt.nz/information-releases/household-income-and-housing-cost-statistics-new-zealand-year-ended-june-2023>


---

## Technical notes

*State variables:* fv_police_call_rate, repeat_fv_incident_rate.

*Constraints:* police_response_capacity, family_court_throughput.

*Inputs:* housing_stress_level, substance_use_prevalence.


*Feedback loops:*

- `Intergenerational transmission: children exposed to family violence are at elevated risk of perpetrating or experiencing violence in adulthood, sustaining community-level prevalence.`


---

*Generated from `problem.wellington.crime.family_violence` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
