---
title: "Rental market stress"
section: housing
subpage: rental-market
order: 2
updated: 2026-04-26
summary: >
  Vacancy rates in Hawke's Bay rental market have fallen below 2%, with rents rising 8-12% annually. Low-income households face displacement; essential workers (healthcare, aged care, education) struggle to secure housing.
status: draft
generated_from: problem.hawkes_bay.housing.rental_market
---

# Rental market stress

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Vacancy Collapse

Rental vacancy in Napier and Hastings has fallen to 1.5-2%, making it difficult for new residents and displaced tenants to secure housing.


## Rent Growth

Median weekly rent in Hawke's Bay has risen from approximately $400 in 2022 to $550 in 2026 — a 37.5% increase in 4 years.


---


## Drivers

The following structural drivers contribute to this problem.


### Post-Cyclone Gabrielle housing scarcity and repair backlog



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Managed medium-density development

Managed medium-density development is the primary strategy.

**Flagship moves:**

- Implement Managed medium-density development across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Managed medium-density development intervention (state variable: `managed_densification_index`, sign: +) (relaxes: `managed_densification_constraint`)


---

## Claims cited on this page

- **Rental vacancy rates in Hawke's Bay stand at 1.5%, well below the 2.0% functional vacancy threshold. Napier and Hastings city centers report near-zero vacancy (< 0.5%), constraining search time for renters and shifting bargaining power entirely to landlords. Post-Cyclone Gabrielle scarcity has locked in higher rents; investors have deferred repairs to new-build properties, further restricting supply and affordability.** [value: 1.5 percent; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.
- **Median weekly rent in Hawke's Bay reached NZD 550 by 2024, with Napier CBD and Hastings inner suburbs commanding NZD 600-700 per week. The median rent-to-income ratio is 26% (versus the national figure of 23%), indicating elevated rental burden. Cyclone Gabrielle damage reduced available rental stock by an estimated 3-5%, pushing landlords toward rapid rent escalation; low-income families face displacement into emergency housing or informal arrangements.** [value: 550 NZD per week (median rent); 2023] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* rental_vacancy_rate, median_rent_level.

*Constraints:* rental_property_cost_burden, landlord_investment_returns.

*Inputs:* post_cyclone_stock_loss, investor_acquisition.


*Feedback loops:*

- `High rents drive low-income residents out; loss of workers reduces service capacity; wages rise but lag rent growth.`


---

*Generated from `problem.hawkes_bay.housing.rental_market` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
