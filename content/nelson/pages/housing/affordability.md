---
title: "Severely unaffordable housing in Nelson city"
section: housing
subpage: affordability
order: 1
updated: 2026-04-26
summary: >
  Nelson is in the Demographia 'severely unaffordable' band: median house price of around $725,000 (April 2024) against median household income of approximately $62,400 produces a price-to-income ratio of 11.6x, well above the national 8.2x. Real prices rose 58 percent between 2018 and 2022, then fell 14 percent by 2024 but remain about 40 percent above the 2018 baseline. Principal-and-interest repayments now consume 32-38 percent of household income for Nelson buyers.
status: draft
generated_from: problem.nelson.housing.affordability
---

# Severely unaffordable housing in Nelson city

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## How Nelson got here

Nelson's affordability deterioration combines three things: lifestyle in-migration during and after COVID, severely constrained buildable land in the basin, and a small rental supply that converts quickly to ownership stock (claim.nelson.housing.affordability_claim). The combined effect was steeper than the national price cycle.


## Distributional impact

The first-home-buyer cohort is the most directly priced out; the next-most-affected group is the long-term renter who cannot save a deposit while paying market rent. Existing owners with mortgages face debt-service stress; mortgage-free owners benefit from the price level. The affordability problem is therefore also an inter-generational wealth-distribution problem.


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic constraint on buildable land in the Nelson basin



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus

### Lifestyle in-migration and short-term rental conversion



- **Category:** demographic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing housing challenges.

**Flagship moves:**

- Implement evidence-based housing policy in Nelson
- Increase investment in housing services and infrastructure
- Build cross-sector partnerships to address housing challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for housing (state variable: `housing_outcome_index`, sign: +)
- Secondary intervention for housing (state variable: `housing_service_access`, sign: +)


### Response: Camp 2

A response strategy addressing housing challenges.

**Flagship moves:**

- Implement evidence-based housing policy in Nelson
- Increase investment in housing services and infrastructure
- Build cross-sector partnerships to address housing challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for housing (state variable: `housing_outcome_index`, sign: +)
- Secondary intervention for housing (state variable: `housing_service_access`, sign: +)


---

## Claims cited on this page

- **Housing affordability in Nelson has deteriorated sharply due to lifestyle migration. Median house price is $725,000 (April 2024) vs. median household income of $62,400, generating a price-to-income ratio of 11.6× (vs. national 8.2×). Real price growth was 58% 2018-2022, then declined 14% 2022-2024 but remains 40% above 2018 baseline. First-home buyers are priced out of the central market; 38% of owner-occupiers have a mortgage, and principal-and-interest repayments consume 32–38% of household income for buyers in 2023-2024 vs. 24% national average.** [value: 11.6 price-to-income ratio; 2024] — Nelson Housing Demand and Development Report 2024; Housing Aotearoa 2023.

---

## Further reading


- **Nelson Housing Demand and Development Report 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>

- **Housing Aotearoa 2023** — Ministry of Housing and Urban Development (Ministry of Housing and Urban Development), 2023 — <https://www.beehive.govt.nz/release/housing-aotearoa>


---

## Technical notes

*State variables:* median_house_price_nzd, price_to_income_ratio, first_home_buyer_share_of_sales.

*Constraints:* buildable_land_hectares, construction_cost_index.

*Inputs:* mortgage_rate, net_migration, consenting_throughput.


*Feedback loops:*

- `Migration-price-supply feedback: in-migration drives prices, prices attract speculative supply but also lock out the entry workforce that supply construction depends on, slowing the supply response.`


---

*Generated from `problem.nelson.housing.affordability` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
