---
title: "Ethnic wealth and income gap in Wellington"
section: inequality
subpage: ethnic-wealth-gap
order: 3
updated: 2026-04-26
summary: >
  Wellington has a significant structural wealth and income gap between high-deprivation communities and the regional average. Homeownership rates in Porirua and southern Hutt Valley are substantially below Wellington City; median incomes are lower; material hardship rates are higher. These disparities reflect occupational concentration in lower-wage sectors, limited intergenerational asset transfer, and housing affordability barriers that income alone cannot overcome.
status: draft
generated_from: problem.wellington.inequality.ethnic_wealth_gap
---

# Ethnic wealth and income gap in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Homeownership gap

Māori homeownership in Wellington is approximately 40% compared to 65% for European households — a gap that reflects both current affordability barriers and the historical exclusion of Māori from land and asset accumulation following colonisation (claim.wellington.inequality.maori_homeownership_gap).


## Pacific income gap

Pacific households in Wellington earn substantially less than the regional median income, concentrated in lower-wage service-sector employment with limited access to the high-wage government and professional roles that dominate Wellington's labour market (claim.wellington.inequality.pacific_income_gap).


---


## Drivers

The following structural drivers contribute to this problem.


### Employment sector stratification by ethnicity



- **Category:** cultural
- **Timescale:** long
- **Consensus:** consensus

### Intergenerational Māori and Pacific asset gap



- **Category:** institutional
- **Timescale:** long
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


### Māori Wealth-Building and Homeownership Pathways

Targeted homeownership programmes and papakāinga housing on Māori land will close the ethnic wealth gap over a generation.

**Flagship moves:**

- Expand Kāinga Whenua loans for papakāinga on Māori freehold land
- Māori housing authority with direct development mandate in Wellington region
- First-home grant boosted for Māori and Pasifika purchasers in Wellington

**Tensions:**

- Homeownership pathway requires deposits that remain inaccessible to very low-income households
- Papakāinga development is constrained by multiple-ownership complexities on Māori freehold land

**Interventions on the system:**

- Establish Wellington Māori Housing Authority with $50M Crown equity to develop papakāinga across the region (state variable: `maori_homeownership_rate`, sign: +)


---

## Claims cited on this page

- **Homeownership in Wellington's high-deprivation communities — primarily Porirua and southern Hutt Valley — is approximately 40% compared to 65% in lower-deprivation areas. This gap reflects current affordability barriers — particularly deposit requirements relative to income — and the long-run effects of historical exclusion from the mid-twentieth-century property wealth accumulation period for communities that did not participate in it.** [value: 40 percent homeownership rate (Māori); 2023] *(confidence: medium)* — Census 2023: Wellington Regional Profile; Stats NZ Household Income and Housing Cost Statistics 2023.
- **Households in Wellington's high-deprivation communities — primarily Porirua and southern Hutt Valley — earn substantially below the regional median income, concentrated in lower-wage service, retail, and hospitality employment with limited access to the high-wage government and professional roles that dominate Wellington's employment base.** — Census 2023: Wellington Regional Profile.

---

## Further reading


- **Census 2023: Wellington Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>

- **Stats NZ Household Income and Housing Cost Statistics 2023** (Stats NZ), 2023 — <https://www.stats.govt.nz/information-releases/household-income-and-housing-cost-statistics-new-zealand-year-ended-june-2023>


---

## Technical notes

*State variables:* maori_homeownership_rate, pacific_median_income_ratio.

*Constraints:* intergenerational_asset_gap, employment_discrimination.

*Inputs:* wage_equity_policy, housing_programme_targeting.


*Feedback loops:*

- `Asset accumulation gap: lower homeownership among Māori and Pacific households means less intergenerational wealth transfer, perpetuating income inequality across generations.`


---

*Generated from `problem.wellington.inequality.ethnic_wealth_gap` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
