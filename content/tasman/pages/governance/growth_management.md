---
title: "Lifestyle-migration growth with infrastructure lag"
section: governance
subpage: growth_management
order: 2
updated: 2026-04-26
summary: >
  Tasman District received around 1,200 net migration inflow between 2016 and 2022, mostly lifestyle migration from Auckland and Wellington. The 2024 growth-management plan targets around 18,500 new dwellings by 2050; Richmond and Motueka are planned at 3-4 percent annual population growth, requiring around NZD 156 million of infrastructure investment.
status: draft
generated_from: problem.tasman.governance.growth_management
---

# Lifestyle-migration growth with infrastructure lag

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Growth that arrived without an infrastructure plan

The 2016-2022 migration inflow preceded the matching infrastructure programme. Three-waters, transport, and reserves are now being planned to catch up to a population already in place (claim.tasman.governance.growth_management_claim).


## Sequencing is the policy lever

The 18,500-dwelling target through 2050 only delivers the intended outcome if infrastructure precedes — or at least keeps pace with — subdivision consenting. Sequencing failures show up later as service degradation, contamination events, and stormwater-capacity exceedance.


---


## Drivers

The following structural drivers contribute to this problem.


### Unitary-council scope on a small ratepayer base



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing governance challenges.

**Flagship moves:**

- Implement evidence-based governance policy in Tasman
- Increase investment in governance services and infrastructure
- Build cross-sector partnerships to address governance challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for governance (state variable: `governance_outcome_index`, sign: +)
- Secondary intervention for governance (state variable: `governance_service_access`, sign: +)


---

## Claims cited on this page

- **Tasman District received 1,200+ net migration inflow 2016–2022, driven by lifestyle migration from Auckland and Wellington. TDC's 2024 growth management plan targets 18,500 new dwellings by 2050; Richmond and Motueka expansion is planned at 3-4% annual population growth, requiring NZD 156 million in infrastructure investment.** [value: 1200 net migration inflow; 2016-2022] — Tasman Housing Demand and Lifestyle Migration 2024; Tasman District Council Annual Plan 2024.

---

## Further reading


- **Tasman Housing Demand and Lifestyle Migration 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* annual_net_migration, infrastructure_investment_to_dwelling_ratio.

*Constraints:* lgfa_borrowing_capacity, construction_workforce_supply.

*Inputs:* long_term_plan_capex_pipeline, central_government_growth_co_funding.


*Feedback loops:*

- `Lagging infrastructure investment raises the per-unit cost of catch-up, which crowds out the next round of growth-area investment.`


---

*Generated from `problem.tasman.governance.growth_management` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
