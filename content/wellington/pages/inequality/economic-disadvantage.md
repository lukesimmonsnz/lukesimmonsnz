---
title: "Working poverty and economic disadvantage in Wellington"
section: inequality
subpage: economic-disadvantage
order: 4
updated: 2026-04-26
summary: >
  Wellington's high cost of living — driven primarily by housing — has expanded the working poor: households in formal employment but unable to meet basic living costs. Income inequality in Wellington is growing as high-wage professional employment expands while low-wage service sector work stagnates in real terms.
status: draft
generated_from: problem.wellington.inequality.economic_disadvantage
---

# Working poverty and economic disadvantage in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Growing income inequality

Wellington's income Gini coefficient reflects a widening gap between high-wage professional and government employees and low-wage service, retail, and hospitality workers, with the latter group particularly exposed to housing cost inflation (claim.wellington.inequality.gini_coefficient_wellington).


## Working poverty

A growing share of Wellington workers in full-time employment cannot afford market-rate housing without spending more than 40% of income on rent — qualifying as severely housing-cost-burdened even while in work (claim.wellington.inequality.working_poverty_prevalence).


---


## Drivers

The following structural drivers contribute to this problem.


### Employment sector stratification by ethnicity



- **Category:** cultural
- **Timescale:** long
- **Consensus:** consensus

### Housing cost burden and child poverty spiral



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus

### Limited transport access to high-wage employment



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** mostly-agreed

### Wage and housing cost divergence



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Labour Market Equity and Living Wage Policy

Living wage mandates and pay equity enforcement across public sector contracts will reduce Wellington's ethnic and gender wealth gaps.

**Flagship moves:**

- Extend Wellington City Council living wage requirement to all council contractors
- Accelerate pay equity settlements in care and education sectors
- Ethnic pay gap reporting requirement for all Wellington employers >50 FTE

**Tensions:**

- Living wage mandates may reduce employment for marginal workers through labour substitution
- Pay equity process is slow; administrative burden on smaller employers is high

**Interventions on the system:**

- Mandate living wage ($26.50/hr 2024) for all Wellington City Council service contracts from 2025 (state variable: `low_wage_employment_share`, sign: -)


### Strengthened Income Floor and Benefit Adequacy

Child poverty in Wellington is primarily driven by inadequate benefit levels; raising the income floor directly reduces deprivation faster than service investment.

**Flagship moves:**

- Raise main benefit rates by 15% above CPI indexation
- Extend Working for Families eligibility to beneficiary families
- Expand Best Start payments to all children for first 3 years

**Tensions:**

- Benefit increases require fiscal headroom conflicting with 2024 consolidation direction
- Critics argue income transfers without services do not address root causes of poverty

**Interventions on the system:**

- Index Jobseeker and Sole Parent Support benefits to 50% of median household income (state variable: `child_poverty_after_housing_costs`, sign: -)


---

## Claims cited on this page

- **Wellington's income Gini coefficient reflects a widening gap between high-wage professional and government employees and low-wage service workers, with housing cost inflation amplifying net income inequality beyond what gross income figures suggest.** *(confidence: medium)* — Stats NZ Household Income and Housing Cost Statistics 2023; Census 2023: Wellington Regional Profile.
- **A growing share of Wellington workers in full-time employment cannot afford market-rate housing without spending more than 40% of income on rent, qualifying as severely housing-cost-burdened even while in paid work.** *(confidence: medium)* — Stats NZ Household Income and Housing Cost Statistics 2023.

---

## Further reading


- **Stats NZ Household Income and Housing Cost Statistics 2023** (Stats NZ), 2023 — <https://www.stats.govt.nz/information-releases/household-income-and-housing-cost-statistics-new-zealand-year-ended-june-2023>

- **Census 2023: Wellington Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* gini_coefficient, working_poverty_rate.

*Constraints:* minimum_wage_relative_to_living_cost, collective_bargaining_coverage.

*Inputs:* wage_growth_rate, housing_cost_growth_rate.


*Feedback loops:*

- `Cost-wage divergence: housing cost inflation exceeding wage growth expands the working-poor population even during periods of nominal employment growth.`


---

*Generated from `problem.wellington.inequality.economic_disadvantage` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
