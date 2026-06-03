---
title: "Geographically concentrated child poverty"
section: inequality
subpage: child_poverty
order: 2
updated: 2026-04-26
summary: >
  Census income data put roughly 21 percent of Tasman children in low-income households (below 60 percent of median income). The rate is about 26 percent in Motueka and rural farm areas, and roughly 18 percent in Richmond. Limited accessible early-intervention services mean health and developmental disparities begin in early childhood.
status: draft
generated_from: problem.tasman.inequality.child_poverty
---

# Geographically concentrated child poverty

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Where the children are matters

The eight-percentage-point gap between Motueka and Richmond is a service-design problem as well as an income one. Programmes targeted at the regional median miss the rural Motueka cohort that needs them most (claim.tasman.inequality.child_poverty_claim).


## Early disadvantage compounds

Children growing up in low-income households in areas with thin ECE supply, longer school commutes, and more restricted health-service access enter school behind their Richmond peers. Catching up later requires resourcing the school system can rarely muster.


---


## Drivers

The following structural drivers contribute to this problem.


### Wage compression at the bottom, capital inflow at the top



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing inequality challenges.

**Flagship moves:**

- Implement evidence-based inequality policy in Tasman
- Increase investment in inequality services and infrastructure
- Build cross-sector partnerships to address inequality challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for inequality (state variable: `inequality_outcome_index`, sign: +)
- Secondary intervention for inequality (state variable: `inequality_service_access`, sign: +)


---

## Claims cited on this page

- **Census income data (2023) indicates 21% of children in Tasman live in low-income households (below 60% of median income). Motueka and rural farm areas have higher child poverty rates (26%) vs Richmond (18%). Limited accessible early intervention services; health disparities begin in childhood.** [value: 21 percent children in low-income households; 2023] — Income and Inequality in Tasman Census 2023; Stats NZ Census 2023.

---

## Further reading


- **Income and Inequality in Tasman Census 2023** — Stats NZ (Statistics New Zealand), 2023 — <https://www.stats.nz>

- **Stats NZ Census 2023** — Stats NZ / Tatauranga Aotearoa (Statistics New Zealand), 2023 — <https://www.stats.nz/tools/census>


---

## Technical notes

*State variables:* child_low_income_rate, geographic_concentration_index.

*Constraints:* household_income_distribution, rural_service_economics.

*Inputs:* early_intervention_funding, school_decile_resourcing.


*Feedback loops:*

- `Concentrated child poverty produces concentrated cohort underachievement, which entrenches the local labour-market wage floor.`


---

*Generated from `problem.tasman.inequality.child_poverty` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
