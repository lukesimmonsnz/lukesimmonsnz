---
title: "High youth-reoffending rate in service-thin areas"
section: crime
subpage: youth_offending
order: 3
updated: 2026-04-26
summary: >
  NZ Police data identify around 156 youth offenders aged 10-16 in Tasman in 2023, with approximately 68 percent re-offending within 12 months. Limited youth diversion and mentoring in Golden Bay and rural areas contributes to higher re-offending compared with Richmond and Motueka.
status: draft
generated_from: problem.tasman.crime.youth_offending
---

# High youth-reoffending rate in service-thin areas

<p class="horizon-band">Analysis horizon: 10yr</p>



## Reoffending tracks programme availability

The Tasman youth-offender cohort is small enough that diversion programmes can plausibly cover it — except where geography and staffing thin out coverage. Mohua and rural blocks have meaningfully fewer diversion-programme options than Richmond (claim.tasman.crime.youth_offending_claim).


## Small numbers, large per-case stakes

Because the cohort is small, individual youth-justice trajectories are highly visible to community and services. Each successful diversion has outsized population-level effect; each missed one feeds the long-tail crime statistics.


---


## Drivers

The following structural drivers contribute to this problem.


### Service-thinness in rural support and diversion



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


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

- **Police youth offending statistics (2023) indicate 156 youth offenders (aged 10-16) in Tasman, with 68% engaging in repeat offending within 12 months. Limited youth diversion and mentoring programs in Golden Bay and rural areas contribute to higher reoffending rates compared to Richmond/Motueka.** [value: 68 percent reoffending rate; 2023] *(confidence: medium)* — New Zealand Police Crime Statistics 2023; Tasman District Council Annual Plan 2024.

---

## Further reading


- **New Zealand Police Crime Statistics 2023** — New Zealand Police (New Zealand Police), 2023 — <https://www.police.govt.nz/about-us/publication/crime-statistics>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* youth_offender_count, 12_month_reoffending_rate.

*Constraints:* rural_programme_economics, specialist_workforce_supply.

*Inputs:* diversion_programme_coverage, mentoring_capacity.


*Feedback loops:*

- `Reoffending trajectories solidify between ages 14-17; each year of inadequate diversion raises the long-run cost of intervention disproportionately.`


---

*Generated from `problem.tasman.crime.youth_offending` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
