---
title: "Rental affordability stress in Wellington"
section: housing
subpage: rental-market
order: 3
updated: 2026-04-26
summary: >
  Wellington's rental market is characterised by low vacancy, high rent-to-income ratios for lower-income households, and limited security of tenure. Government-sector workers occupy a disproportionate share of the premium rental stock, squeezing lower-wage households into peripheral suburbs or into severe housing cost burden.
status: draft
generated_from: problem.wellington.housing.rental_market
---

# Rental affordability stress in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Rent burden on low-income households

Wellington rental costs consume approximately 38% of median household income for households in the bottom two income quintiles (claim.wellington.housing.rental_affordability_ratio_2023). This exceeds the 30% affordability threshold widely used in housing policy analysis.


## Structural vacancy tightness

Wellington consistently records rental vacancy rates below 2%, well under the 3–4% level generally considered indicative of a balanced market (claim.wellington.housing.vacancy_rate_low). This structural tightness gives landlords sustained pricing power and limits tenants' ability to negotiate or move.


---


## Drivers

The following structural drivers contribute to this problem.


### Residential property as investment asset



- **Category:** economic
- **Timescale:** medium
- **Consensus:** mostly-agreed

### Structural rental vacancy tightness



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Institutional Build-to-Rent and Social Housing Expansion

Professionalised long-term rental providers and expanded Kāinga Ora stock create stable, affordable rental supply.

**Flagship moves:**

- Tax incentives for build-to-rent institutional investment in Wellington
- Accelerate Kāinga Ora pipeline in Porirua and Hutt Valley
- Community land trust model for perpetual affordability on Crown land

**Tensions:**

- Requires significant Crown capital allocation competing with fiscal consolidation pressures
- Institutional providers may prioritise mid-market returns over deep affordability

**Interventions on the system:**

- Allocate surplus Crown land in Wellington region to community land trusts at below-market value (state variable: `affordable_rental_stock`, sign: +)


### Rent Stabilisation and Tenancy Reform

Rent control mechanisms combined with stronger tenancy security would reduce displacement and rental market volatility.

**Flagship moves:**

- Cap annual rent increases to CPI + 2%
- Extend notice periods for no-cause terminations to 90 days
- Mandate WOF-standard minimum habitability requirements

**Tensions:**

- Rent caps reduce landlord incentives to maintain and invest in rental stock
- Supply-side economists argue rent stabilisation reduces new rental construction

**Interventions on the system:**

- Introduce Residential Tenancies Act amendment capping in-tenancy rent increases to CPI + 2% (state variable: `rent_affordability`, sign: +)


---

## Claims cited on this page

- **Rental costs consume approximately 38% of median household income for households in the bottom two income quintiles in Wellington, exceeding the 30% affordability threshold widely used in housing policy analysis.** [value: 38 percent of median household income; 2023] *(confidence: medium)* — Stats NZ Household Income and Housing Cost Statistics 2023.
- **Wellington's private rental market has consistently recorded vacancy rates below 2%, well under the 3–4% level typically associated with a balanced rental market, giving landlords sustained pricing power and limiting tenant mobility.** *(confidence: medium)* — Aotearoa New Zealand Housing Report 2023.

---

## Further reading


- **Stats NZ Household Income and Housing Cost Statistics 2023** (Stats NZ), 2023 — <https://www.stats.govt.nz/information-releases/household-income-and-housing-cost-statistics-new-zealand-year-ended-june-2023>

- **Aotearoa New Zealand Housing Report 2023** (Ministry of Housing and Urban Development), 2023 — <https://www.hud.govt.nz/housing-and-property/housing-research-and-data/housing-data-and-research/aotearoa-new-zealand-housing-report/>


---

## Technical notes

*State variables:* median_weekly_rent, rent_to_income_ratio, rental_vacancy_rate.

*Constraints:* low_developable_land, investor_return_expectations.

*Inputs:* rental_stock_growth, public_sector_employment_level, social_housing_waitlist.


*Feedback loops:*

- `Vacancy-rent loop: low vacancy rates remove competitive pressure on rents, enabling sustained above-inflation rent increases.`
- `Displacement loop: high rents displace lower-income households to outer suburbs, increasing transport costs and eroding net income gains.`


---

*Generated from `problem.wellington.housing.rental_market` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
