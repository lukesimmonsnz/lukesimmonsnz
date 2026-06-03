---
title: "Per-dwelling infrastructure cost in a low-density region"
section: housing
subpage: infrastructure_cost
order: 4
updated: 2026-04-26
summary: >
  Tasman District Council's growth-management modelling projects development contributions of around NZD 28,500 per new dwelling — three-waters, roading and reserves combined — and around NZD 156 million of infrastructure investment to deliver 450 dwellings per year through to 2050.
status: draft
generated_from: problem.tasman.housing.infrastructure_cost
---

# Per-dwelling infrastructure cost in a low-density region

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Sprawl is expensive per house

Low-density growth pushes pipes and roads further per dwelling than compact development. With a development contribution near NZD 28,500 per new dwelling, much of that cost is either capitalised into section prices or back-loaded onto the rates base (claim.tasman.housing.infrastructure_cost_claim).


## Funding model under pressure

Tasman District Council's NZD 287 million annual budget is already absorbing three-waters reform transition costs and a maintenance backlog. Funding the growth programme from rates, development contributions, and Crown co-investment without displacing renewals is the binding fiscal constraint.


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

- **TDC infrastructure capacity analysis (2024) projects development contributions for new housing at NZD 28,500 per dwelling (including three-waters, roading, reserves). Growth management strategy targets 450 dwellings/year through 2050; total infrastructure investment required is NZD 156 million (rate or subsidy-funded).** [value: 28500 NZD per dwelling development contribution; 2024] — Tasman District Council Annual Plan 2024; Tasman Housing Demand and Lifestyle Migration 2024.

---

## Further reading


- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>

- **Tasman Housing Demand and Lifestyle Migration 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>


---

## Technical notes

*State variables:* development_contribution_per_dwelling, growth_capex_pipeline.

*Constraints:* lgfa_borrowing_caps, renewal_backlog.

*Inputs:* rates_base_growth, crown_co_investment.


*Feedback loops:*

- `High per-dwelling infrastructure cost raises section prices, which raises end-house prices, which suppresses demand for the very dwellings the infrastructure was sized for.`


---

*Generated from `problem.tasman.housing.infrastructure_cost` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
