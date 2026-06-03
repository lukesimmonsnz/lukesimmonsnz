---
title: "High per-lot infrastructure cost in greenfield development"
section: housing
subpage: infrastructure_cost
order: 4
updated: 2026-04-26
summary: >
  New subdivision in Nelson is constrained by high per-lot infrastructure cost. Water reticulation extension averages $35,000-50,000 per lot (versus $15,000-25,000 nationally), wastewater treatment augmentation $28,000-42,000 per lot, and stormwater plus roading another $20,000-35,000 per lot. Total greenfield development cost runs $83,000-127,000 per lot before land cost, pushing minimum lot values above $180,000 and new-build price points above $800,000.
status: draft
generated_from: problem.nelson.housing.infrastructure_cost
---

# High per-lot infrastructure cost in greenfield development

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Why costs are higher here

Nelson's terrain (steep, dispersed catchments) and the ageing Maitai-anchored bulk-water network mean reticulation extensions have higher per-lot capital cost than flat-metro greenfield (claim.nelson.housing.infrastructure_cost_claim). Wastewater treatment augmentation at Bells Island is at a stage in its asset life where augmentation costs are being capitalised into new connections.


## Cost-shifting versus affordability outcome

Per-lot cost recovery via development contributions is structurally fair (existing ratepayers do not subsidise new arrivals) but pushes the lot-price floor above the level entry buyers can finance. The question is which cost mechanism (development contributions, rates, central co-funding) results in housing actually being built.


---


## Drivers

The following structural drivers contribute to this problem.


### Lifestyle in-migration and short-term rental conversion



- **Category:** demographic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


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

- **Infrastructure cost barriers to housing development are material in Nelson. New subdivision development is constrained by high per-lot infrastructure costs: water reticulation extension averages $35,000–50,000/lot (vs. $15,000–25,000 nationally due to geographic dispersion and aging Maitai Dam dependency); wastewater treatment augmentation costs $28,000–42,000/lot; stormwater and roading add another $20,000–35,000/lot. Total greenfield development cost is $83,000–127,000/lot before land cost, pushing minimum lot values above $180,000 and new-build price points above $800,000.** [value: 100 thousand NZD average infrastructure cost per lot; 2023-2024] *(confidence: medium)* — Nelson Housing Demand and Development Report 2024.

---

## Further reading


- **Nelson Housing Demand and Development Report 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>


---

## Technical notes

*State variables:* per_lot_three_waters_cost, development_contribution_per_lot, minimum_section_price_nzd.

*Constraints:* terrain, asset_age, treatment_plant_capacity.

*Inputs:* central_co_funding, council_capex_envelope.


*Feedback loops:*

- `Cost-affordability feedback: high per-lot cost lifts entry-price floor, suppressing first-home-buyer demand for new builds, which slows uptake and stretches per-lot capex recovery over fewer lots, raising costs further.`


---

*Generated from `problem.nelson.housing.infrastructure_cost` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
