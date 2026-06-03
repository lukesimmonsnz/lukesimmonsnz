---
title: "Community safety and crime prevalence"
section: crime
subpage: safety
order: 1
updated: 2026-04-26
summary: >
  Hawke's Bay experiences higher crime rates than national average, particularly property crime and family violence. Community safety perception is declining. Limited policing resources hamper prevention and investigation.
status: draft
generated_from: problem.hawkes_bay.crime.safety
---

# Community safety and crime prevalence

<p class="horizon-band">Analysis horizon: 10yr</p>



## Crime Rates

Hawke's Bay crime rate is approximately 7,200 offences per 100,000 population, compared to national average of 6,200. Property crime and violence are elevated.


## Family Violence

Family violence incidents in Hawke's Bay increased 22% over 2020-2024, driven by housing stress, substance abuse, and economic hardship exacerbated by Cyclone Gabrielle.


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

- **Hawke's Bay crime rates (7,200 offences per 100,000 population annually) reflect geographic, economic, and social vulnerabilities. Property crime, family violence, and drug-related offenses impact community safety; police response capacity is constrained in rural and remote areas like Wairoa, limiting prevention effectiveness and victim support services.** [value: 7200 offences per 100k population; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.
- **Family violence call rates in Hawke's Bay increased 22% over 2019-2024, outpacing the national 15% increase. Economic stress from Cyclone Gabrielle recovery, housing insecurity, and deprivation-linked risk factors (alcohol/drug use, unemployment) compound vulnerability in Hastings, Napier, and Wairoa communities.** [value: 22 percent increase; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* crime_rate_per_capita, family_violence_incident_rate.

*Constraints:* police_workforce_allocation, court_capacity.

*Inputs:* deprivation_concentration, substance_abuse_prevalence.


*Feedback loops:*

- `High crime erodes community trust; divestment from neighbourhoods follows; informal social control weakens; crime increases further.`


---

*Generated from `problem.hawkes_bay.crime.safety` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
