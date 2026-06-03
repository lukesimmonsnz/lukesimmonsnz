---
title: "State housing adequacy and access"
section: housing
subpage: state-housing
order: 2
updated: 2026-04-26
summary: >
  Taranaki state housing waiting lists are growing as private rental costs rise. Meth contamination in some Housing NZ properties has required remediation. Tenant support and property management standards vary.
status: draft
generated_from: problem.taranaki.housing.state_housing
---

# State housing adequacy and access

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Waiting Lists

State housing waiting lists in Taranaki have grown to 600+ households (2024), up 35% from 2020.


## Property Condition

Meth contamination remediation has delayed approximately 80 state properties from being reoccupied.


---


## Drivers

The following structural drivers contribute to this problem.


### Oil and gas sector wage volatility



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Housing affordability support

Housing affordability support addresses housing_market.

**Flagship moves:**

- Implement Housing affordability support

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Housing affordability support action (state variable: `housing.affordability_support_index`, sign: +)


---

## Claims cited on this page

- **Housing quality and affordability pressures co-exist in Taranaki, with rental vacancies below 1-2% in urban areas. Essential workers (nurses, teachers, farm laborers) face housing stress, forcing commuting from more distant affordable areas or out-migration.** [value: 600 households; 2024] *(confidence: medium)* — Census 2023: Taranaki Regional Profile.

---

## Further reading


- **Census 2023: Taranaki Regional Profile** (Stats NZ), 2023


---

## Technical notes

*State variables:* state_housing_waiting_list_months, state_housing_condition_index.

*Constraints:* housing_nz_budget_availability.

*Inputs:* rental_market_stress, remediation_backlog.


*Feedback loops:*

- `Waiting lists lengthen; tenant vulnerability increases; support costs rise.`


---

*Generated from `problem.taranaki.housing.state_housing` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
