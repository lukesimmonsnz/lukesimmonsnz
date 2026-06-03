---
title: "Income and wealth polarisation"
section: inequality
subpage: income-polarisation
order: 3
updated: 2026-04-26
summary: >
  The gap between top and bottom income deciles in Auckland has widened substantially since the 1990s, driven primarily by housing-cost growth absorbing an increasing share of low-income household budgets. Wealth concentration is more extreme than income concentration: the top 10% of households hold approximately 60% of net household wealth, with housing equity as the primary vehicle. Households without intergenerational property wealth face compounding exclusion from the main asset class driving wealth accumulation.

status: draft
generated_from: problem.auckland.inequality.income_polarisation
---

# Income and wealth polarisation

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## The housing-cost channel

Income inequality in New Zealand is moderate by OECD standards before housing costs, but Auckland's rental market transforms this picture substantially. When housing costs are deducted, the bottom two income deciles have experienced near-zero real income growth over three decades. The mechanism is straightforward: rents have risen faster than wages for low-wage workers, and the share of income absorbed by rent has grown from roughly 25% in the mid-1990s to 40-50% for low-income renters in the 2020s. This is not a distribution story about who earns what; it is a story about who owns what and who bears the cost when the housing market inflates.


## Wealth versus income

Wealth inequality is structurally more extreme and more durable than income inequality. The top 10% of New Zealand households own approximately 60% of net household wealth; the bottom 50% own less than 5%. This distribution is self-reinforcing: home equity is the primary savings vehicle for middle- and upper-income households, and households who entered the housing market before 2000 have accumulated equity inaccessible to renters of equivalent income. Intergenerational transfer now extends this divide: parental equity provides deposit assistance that is structurally unavailable to the majority without family ownership.


---

## References



- **Ministry of Social Development — Household Incomes Report 2023** (Ministry of Social Development (New Zealand)), 2023 — <https://www.msd.govt.nz/about-msd-and-our-work/publications-resources/monitoring/household-incomes/>

- **Statistics New Zealand — 2023 Census of Population and Dwellings** (Statistics New Zealand (Stats NZ)), 2023 — <https://www.stats.govt.nz/tools/2023-census-place-summaries/auckland-region>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Residential segregation by income and ethnicity



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Progressive transfers and benefit adequacy

The most direct intervention for child poverty and low-income hardship is adequate income support: benefits set at levels that cover actual housing and living costs, Working for Families parameters that reach the lowest-income households, and a minimum wage indexed to inflation and productivity. Structural redistribution through the tax-transfer system is faster and more certain in its poverty-reduction effect than supply-side reforms that take years to deliver.

**Flagship moves:**

- Index core benefit rates to a cost-of-living basket that includes current Auckland rents, closing the gap between benefit levels and actual housing costs
- Extend the Best Start payment to all children regardless of parental income for the first three years of life
- Raise the minimum wage to 70% of the median wage and index it to median wage growth, narrowing the income floor gap

**Tensions:**

- Transfer increases without housing supply reform can capitalise into rents in a low-vacancy market, with landlords capturing part of the income gain through rent increases.

- Universal or near-universal benefit increases are expensive; targeting transfers to the poorest households maximises poverty reduction per dollar but creates marginal tax rate traps at income thresholds.


**Interventions on the system:**

- Rebase the core benefit to 80% of the minimum wage, replacing the 2021 indexation freeze, and index it to wage growth thereafter.
 (state variable: `child_poverty_rate`, sign: -) (relaxes: `benefit level below actual housing and living costs`)
- Extend Working for Families abatement threshold to ensure all households with children below 130% of median household income receive some payment.
 (state variable: `income_decile_bottom_real`, sign: +)


### Claims cited on this page

- **The gap between the top and bottom income deciles in Auckland has widened over the past three decades. Households in the top income decile have seen real income growth substantially above those in the bottom two deciles, where real incomes (after housing costs) have been largely stagnant. Housing costs are the primary driver of widening after-housing-cost inequality: rental cost increases have absorbed a growing share of lower-income household budgets.
** — Ministry of Social Development — Household Incomes Report 2023.
- **Wealth concentration in New Zealand — and Auckland — is substantially higher than income concentration. The top 10% of households own approximately 60% of net household wealth, with housing equity being the primary wealth-building vehicle for the top half and largely inaccessible to the bottom half. The intergenerational transfer of housing equity is compounding this concentration: households with owning parents have access to deposit assistance unavailable to those without.
** *(confidence: medium)* — Ministry of Social Development — Household Incomes Report 2023; Statistics New Zealand — 2023 Census of Population and Dwellings.

### Systems-model notes

*State variables:* income_decile_bottom_real, wealth_share_top10pct, after_housing_cost_inequality_ratio.

*Constraints:* No capital gains tax on housing equity, concentrating returns in owning households, Working for Families abatement structure limits effective income gains for households entering work at low wages, Wealth data published at national level only; Auckland-specific estimates rely on modelling.

*Inputs:* rental_cost_share_of_low_income_budget, capital_gains_realised_top_decile, tax_transfer_redistribution_rate, intergenerational_wealth_transfer_access.


*Feedback loops:*

- `Rising wealth concentration -> greater intergenerational transfer -> fewer first-home buyers from non-owning households -> widening homeownership gap -> further wealth concentration`
- `After-housing-cost income squeeze on low deciles -> reduced savings capacity -> inability to accumulate non-housing assets -> permanent exclusion from wealth accumulation`


</details>

---

*Generated from `problem.auckland.inequality.income_polarisation` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
