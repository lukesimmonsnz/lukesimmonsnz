---
title: "Drug-related crime and substance abuse"
section: crime
subpage: drug-crime
order: 2
updated: 2026-04-26
summary: >
  Methamphetamine and synthetic drug markets have expanded in Hawke's Bay. Related property crime, violence, and health harms are rising. Treatment and prevention services are under-resourced.
status: draft
generated_from: problem.hawkes_bay.crime.drug_crime
---

# Drug-related crime and substance abuse

<p class="horizon-band">Analysis horizon: 10yr</p>



## Market Expansion

Police report expanded methamphetamine and fentanyl supply networks in Hawke's Bay since 2018. Seizures have increased 150% over five years.


## Health Impact

Drug-related hospital admissions and overdose deaths in Hawke's Bay have increased 35% over 2018-2023. Limited treatment bed capacity creates long waiting lists.


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

- **Drug seizures in Hawke's Bay increased 150% over the past five years, indicating elevated illicit substance trafficking and use. Rural and remote areas including Wairoa face heightened exposure to drug-related harm with constrained police capacity to monitor and prevent supply chain activities affecting youth and vulnerable populations.** [value: 150 percent increase; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* drug_market_activity_index, drug_treatment_service_coverage_percent.

*Constraints:* rehabilitation_facility_capacity, community_education_resourcing.

*Inputs:* organised_crime_gang_activity, treatment_service_shortage.


*Feedback loops:*

- `Addiction untreated drives property crime; incarceration without treatment causes reoffending; community impacts increase demand for services exceeding supply.`


---

*Generated from `problem.hawkes_bay.crime.drug_crime` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
