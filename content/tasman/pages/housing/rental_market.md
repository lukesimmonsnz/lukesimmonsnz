---
title: "Rental market with near-zero vacancy"
section: housing
subpage: rental_market
order: 3
updated: 2026-04-26
summary: >
  Tasman's rental vacancy rate sits near 1 percent, with median three-bedroom rents around NZD 420 per week in Motueka and Richmond. Sole earners on median wages are spending 35-40 percent of gross income on rent, and Golden Bay has almost no rental stock at all.
status: draft
generated_from: problem.tasman.housing.rental_market
---

# Rental market with near-zero vacancy

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## A market that does not clear

A 1 percent vacancy rate means renters cannot move without an existing tenant first leaving, and landlords face no competitive pressure on price or quality. Three-month waitlists are routine in Golden Bay (claim.tasman.housing.rental_market_claim).


## Seasonal labour competes for the same houses

Apple, kiwifruit and hops harvests bring seasonal RSE and backpacker labour into the same rental pool used by year-round residents. Where employer-provided accommodation is undersupplied, the seasonal demand spike pushes rents up further during precisely the months when low-income households can least absorb the cost.


---


## Drivers

The following structural drivers contribute to this problem.


### Infrastructure-constrained land absorption



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


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

- **Rental market in Tasman is extremely tight; vacancy rate hovers near 1% (2023). Median rent for a three-bedroom property is NZD 420/week in Motueka and Richmond, consuming 35-40% of median income for sole earners. Golden Bay has almost no rental stock; waitlists extend 3+ months.** [value: 1 percent vacancy rate; 2023] *(confidence: medium)* — Tasman Housing Demand and Lifestyle Migration 2024; Housing Aotearoa 2023.

---

## Further reading


- **Tasman Housing Demand and Lifestyle Migration 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>

- **Housing Aotearoa 2023** — Ministry of Housing and Urban Development (Ministry of Housing and Urban Development), 2023 — <https://www.beehive.govt.nz/release/housing-aotearoa>


---

## Technical notes

*State variables:* rental_vacancy_rate, median_weekly_rent_3br.

*Constraints:* landlord_consolidation, tenancy_legal_settings.

*Inputs:* new_rental_supply, rse_employer_accommodation_supply.


*Feedback loops:*

- `Tight rental market drives some workers out of the region, which reduces labour supply for the very employers whose accommodation strategies set part of the rental pressure.`


---

*Generated from `problem.tasman.housing.rental_market` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
