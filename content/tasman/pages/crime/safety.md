---
title: "Property-crime-dominated regional crime profile"
section: crime
subpage: safety
order: 1
updated: 2026-04-26
summary: >
  NZ Police statistics record around 1,247 reported crimes in Tasman in 2023, against a population of roughly 58,000 — a rate of 2.15 reported crimes per 100 residents per year. Property crime, including vehicle theft, accounts for around 58 percent of reports; violent crime around 14 percent.
status: draft
generated_from: problem.tasman.crime.safety
---

# Property-crime-dominated regional crime profile

<p class="horizon-band">Analysis horizon: 10yr</p>



## A property-crime-shaped profile

Tasman's reported-crime mix is dominated by property offences — burglary, theft from cars, and vehicle theft — rather than violent crime. The pattern is consistent with a low-density region with seasonal visitor flux and dispersed dwellings (claim.tasman.crime.safety_claim).


## Reported and actual diverge in low-density areas

Recorded-crime rates are sensitive to reporting behaviour as well as actual incidence. In thinly-policed rural areas, lower clearance rates can lead to lower reporting in steady-state, which underestimates the true incidence of property offending.


---


## Drivers

The following structural drivers contribute to this problem.


### Low-density policing geography



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Service-thinness in rural support and diversion



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing crime challenges.

**Flagship moves:**

- Implement evidence-based crime policy in Tasman
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

- Implement evidence-based crime policy in Tasman
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

- **NZ Police Crime Statistics (2023) record 1,247 reported crimes in Tasman region (population 58,000), yielding a crime rate of 2.15 per 100 residents annually. Property crime (including vehicle theft) comprises 58% of reports; violent crime 14%.** [value: 2.15 crimes per 100 residents/year; 2023] — New Zealand Police Crime Statistics 2023; Stats NZ Census 2023.

---

## Further reading


- **New Zealand Police Crime Statistics 2023** — New Zealand Police (New Zealand Police), 2023 — <https://www.police.govt.nz/about-us/publication/crime-statistics>

- **Stats NZ Census 2023** — Stats NZ / Tatauranga Aotearoa (Statistics New Zealand), 2023 — <https://www.stats.nz/tools/census>


---

## Technical notes

*State variables:* reported_crime_rate_per_100, property_crime_share.

*Constraints:* low_density_response_geography, seasonal_visitor_flux.

*Inputs:* police_resourcing, community_crime_prevention_programmes.


*Feedback loops:*

- `Low clearance rates suppress reporting, which understates the true crime base and weakens the case for additional resourcing.`


---

*Generated from `problem.tasman.crime.safety` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
