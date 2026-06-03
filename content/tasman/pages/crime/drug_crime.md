---
title: "Methamphetamine supply via SH6/SH60 corridor"
section: crime
subpage: drug_crime
order: 4
updated: 2026-04-26
summary: >
  NZ Police statistics show drug-related offences in Tasman up around 12 percent year-on-year in 2023. Methamphetamine supply via SH6 and SH60 and the relative isolation of Golden Bay are identified police priorities in the Tasman District Council community-safety plan.
status: draft
generated_from: problem.tasman.crime.drug_crime
---

# Methamphetamine supply via SH6/SH60 corridor

<p class="horizon-band">Analysis horizon: 10yr</p>



## Supply geography matches access geography

The same single-corridor structure that constrains legitimate transport also structures the methamphetamine supply chain: SH6 from the north and SH60 to Mohua. Police interdiction effort concentrates on those routes (claim.tasman.crime.drug_crime_claim).


## Demand-side picture less visible

Recorded supply-side offences are easier to count than demand-side use. The 12 percent year-on-year rise in offences may reflect a real rise in supply, a real rise in enforcement effort, or some mix; the underlying demand prevalence is harder to infer from offence statistics alone.


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

- **NZ Police Crime Statistics (2023) show drug-related offences in Tasman region increased 12% year-on-year. Methamphetamine supply through regional highways (SH6, SH60) and Golden Bay isolation are identified police priorities in Tasman District Council community safety plan.** [value: 12 percent increase YoY; 2023] — New Zealand Police Crime Statistics 2023; Tasman District Council Annual Plan 2024.

---

## Further reading


- **New Zealand Police Crime Statistics 2023** — New Zealand Police (New Zealand Police), 2023 — <https://www.police.govt.nz/about-us/publication/crime-statistics>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* drug_offence_count_yoy, supply_route_seizure_volume.

*Constraints:* single_corridor_supply_geography, rural_treatment_service_thinness.

*Inputs:* police_interdiction_effort, addiction_treatment_capacity.


*Feedback loops:*

- `Successful supply interdiction without matching demand-side capacity shifts use to alternative substances, displacing rather than reducing harm.`


---

*Generated from `problem.tasman.crime.drug_crime` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
