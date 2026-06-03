---
title: "Crime rate and perceived safety in Nelson district"
section: crime
subpage: safety
order: 1
updated: 2026-04-26
summary: >
  Nelson district recorded approximately 3,650 notifiable offences in 2023, equivalent to about 66 offences per 1,000 residents against a national rate of around 60. Property crime concentrated in the central city and high-turnover rental suburbs is the dominant driver, and community safety perception has fallen by roughly 14 percent since 2020, particularly at night.
status: draft
generated_from: problem.nelson.crime.safety
---

# Crime rate and perceived safety in Nelson district

<p class="horizon-band">Analysis horizon: 10yr</p>



## Headline rate and composition

Nelson's recorded-crime rate sits modestly above the national average and is dominated by property offences -- burglary, theft, and unlawful taking of motor vehicles -- concentrated around the central city, Stoke, and the transient-population fringe (claim.nelson.crime.safety_claim). Violent offending is a smaller share but is rising in line with the family-violence trend.


## Perception, transient population, and visibility

Perception of safety is shaped less by the headline rate than by visible disorder: rough sleeping in central streets, alcohol-related incidents around the bar district, and burglary clusters in particular streets. The lack of after-hours activity and CBD foot-traffic outside summer tourism months amplifies both actual opportunity and perceived risk.


---


## Drivers

The following structural drivers contribute to this problem.


### Concentrated socioeconomic deprivation



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus

### Methamphetamine supply network and treatment-capacity gap



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing crime challenges.

**Flagship moves:**

- Implement evidence-based crime policy in Nelson
- Increase investment in crime services and infrastructure
- Build cross-sector partnerships to address crime challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for crime (state variable: `crime_outcome_index`, sign: +)
- Secondary intervention for crime (state variable: `crime_service_access`, sign: +)


### Response: Camp 2

A response strategy addressing crime challenges.

**Flagship moves:**

- Implement evidence-based crime policy in Nelson
- Increase investment in crime services and infrastructure
- Build cross-sector partnerships to address crime challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for crime (state variable: `crime_outcome_index`, sign: +)
- Secondary intervention for crime (state variable: `crime_service_access`, sign: +)


---

## Claims cited on this page

- **Nelson's overall crime rate is 9% above the national average, with burglary and vehicle crime as highest-volume property offences. 2023 NZ Police data reports 3,650 total notifiable offences in Nelson district (rate 66 per 1,000 population vs. national 60 per 1,000), driven by property crime in high-turnover transient areas (city centre, rental suburbs). Community perception of safety has declined 14% since 2020, particularly at night.** [value: 66 notifiable offences per 1,000 population (2023); 2023] — New Zealand Police Crime Statistics 2023.

---

## Further reading


- **New Zealand Police Crime Statistics 2023** — New Zealand Police (New Zealand Police), 2023 — <https://www.police.govt.nz/about-us/publication/crime-statistics>


---

## Technical notes

*State variables:* notifiable_offences_per_1000, perception_of_safety_index, burglary_rate_per_1000_dwellings.

*Constraints:* police_funding_envelope, court_throughput.

*Inputs:* police_staffing_levels, cctv_coverage, alcohol_outlet_density.


*Feedback loops:*

- `Perception-spending feedback: declining safety perception drives demand for more visible policing and lighting, but the underlying property-crime drivers (transience, deprivation, drug supply) sit outside the policing lever.`


---

*Generated from `problem.nelson.crime.safety` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
