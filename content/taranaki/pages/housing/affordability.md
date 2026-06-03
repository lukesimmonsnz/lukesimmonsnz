---
title: "Housing affordability and debt stress"
section: housing
subpage: affordability
order: 2
updated: 2026-04-26
summary: >
  High household debt relative to income in Taranaki due to oil and gas sector wage expectations. Economic volatility creates mortgage stress during downturns.
status: draft
generated_from: problem.taranaki.housing.affordability
---

# Housing affordability and debt stress

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Debt Levels

Average household debt in Taranaki is approximately $280k (2024), reflecting high borrowing during oil boom years.


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

- **Housing pressures in Taranaki include affordability constraints and quality issues. Rental market tightness, investor concentration, and inadequate supply force households into unaffordable situations; essential workers face displacement or commuting burden.** [value: 280000 NZD; 2024] *(confidence: medium)* — Census 2023: Taranaki Regional Profile.

---

## Further reading


- **Census 2023: Taranaki Regional Profile** (Stats NZ), 2023


---

## Technical notes

*State variables:* mortgage_stress_ratio, household_debt_to_income_ratio.

*Constraints:* household_income_variability.

*Inputs:* sector_employment_volatility, interest_rate_changes.


*Feedback loops:*

- `Downturn increases defaults; property values decline; equity erodes.`


---

*Generated from `problem.taranaki.housing.affordability` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
