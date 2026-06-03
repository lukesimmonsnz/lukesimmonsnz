---
title: "Lifestyle-migration housing-cost pressure"
section: housing
subpage: affordability
order: 1
updated: 2026-04-26
summary: >
  Tasman's median house price rose roughly 68 percent between 2016 and 2022 (NZD 385,000 to NZD 647,000) while median household income grew far more slowly, pushing the price-to-income ratio to 7.4 — well above the conventional affordability threshold of 5.0 and squeezing first-home buyers out of Richmond and Motueka.
status: draft
generated_from: problem.tasman.housing.affordability
---

# Lifestyle-migration housing-cost pressure

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## External demand sets local prices

Lifestyle migration from Auckland and Wellington has been the dominant driver of house-price inflation in Richmond, Motueka and parts of Mohua. Buyers arriving with metropolitan equity outbid local first-home purchasers, raising the effective entry price into Tasman's housing market (claim.tasman.housing.affordability_claim).


## Local incomes do not track local prices

Median household income in Tasman is around NZD 87,400, anchored by horticulture, tourism, and small-business work. With prices reaching 7.4 times that figure, only high-equity or dual-high-income buyers can transact at current prices, and the ownership rate among 25-34-year-olds is falling.


---


## Drivers

The following structural drivers contribute to this problem.


### Infrastructure-constrained land absorption



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus

### Lifestyle-migration demand from metropolitan equity



- **Category:** demographic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing housing challenges.

**Flagship moves:**

- Implement evidence-based housing policy in Tasman
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

- Implement evidence-based housing policy in Tasman
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

- **Tasman Housing Demand and Lifestyle Migration (2024) documents median house price rise 68% (2016-2022), from NZD 385,000 to NZD 647,000. Median household income is NZD 87,400; price-to-income ratio stands at 7.4, above the 5.0 affordability threshold. First-home buyers squeezed out of Richmond and Motueka markets.** [value: 7.4 price-to-income ratio; 2024] — Tasman Housing Demand and Lifestyle Migration 2024; Income and Inequality in Tasman Census 2023.

---

## Further reading


- **Tasman Housing Demand and Lifestyle Migration 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>

- **Income and Inequality in Tasman Census 2023** — Stats NZ (Statistics New Zealand), 2023 — <https://www.stats.nz>


---

## Technical notes

*State variables:* median_house_price, price_to_income_ratio.

*Constraints:* land_supply_pipeline, construction_capacity.

*Inputs:* external_buyer_demand, consented_dwellings_per_year.


*Feedback loops:*

- `Capital-gain expectations attract more lifestyle buyers, which raises prices, which reinforces capital-gain expectations.`


---

*Generated from `problem.tasman.housing.affordability` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
