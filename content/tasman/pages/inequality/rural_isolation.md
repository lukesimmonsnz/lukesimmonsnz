---
title: "Mohua relative-poverty profile despite cheaper housing"
section: inequality
subpage: rural_isolation
order: 4
updated: 2026-04-26
summary: >
  Golden Bay is geographically isolated — the nearest supermarket is in Motueka, around 45 minutes over the Takaka Hill. Population sits around 3,200, with one medical practice, one secondary school, and no tertiary provision. Rental and purchase prices are lower than Richmond, but local incomes are roughly 12 percent below the regional median, producing relative poverty despite lower housing costs.
status: draft
generated_from: problem.tasman.inequality.rural_isolation
---

# Mohua relative-poverty profile despite cheaper housing

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Cheaper houses, more expensive lives

Lower house prices in Mohua are partly compensation for the additional cost of living there: longer drives to specialist services, more expensive groceries, more exposure to road closures. The net effect is relative poverty inside a community that looks affordable on a price-only metric (claim.tasman.inequality.rural_isolation_claim).


## Service thinning is the underlying mechanism

A single medical practice, a single secondary school, and no tertiary provider give residents very narrow choice sets. Each service withdrawal — a closing branch, a retiring GP, a discontinued bus route — has outsized effects because there is no parallel option.


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic concentration of disadvantage



- **Category:** demographic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing inequality challenges.

**Flagship moves:**

- Implement evidence-based inequality policy in Tasman
- Increase investment in inequality services and infrastructure
- Build cross-sector partnerships to address inequality challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for inequality (state variable: `inequality_outcome_index`, sign: +)
- Secondary intervention for inequality (state variable: `inequality_service_access`, sign: +)


---

## Claims cited on this page

- **Golden Bay is geographically isolated, accessible only via SH60 over Takaka Hill (45-minute drive to nearest supermarket in Motueka). Population 3,200; limited services (one medical practice, one secondary school, no tertiary). Rental/purchase prices lower than Richmond but incomes average 12% below regional median, creating relative poverty despite lower housing costs.** [value: 45 minutes to nearest supermarket; 2024] *(confidence: medium)* — Tasman Housing Demand and Lifestyle Migration 2024; Tasman District Council Annual Plan 2024.

---

## Further reading


- **Tasman Housing Demand and Lifestyle Migration 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* minutes_to_nearest_supermarket, local_income_vs_regional_median.

*Constraints:* single_road_corridor, low_density_service_economics.

*Inputs:* rural_service_subsidies, telehealth_and_online_service_capacity.


*Feedback loops:*

- `Each service withdrawal accelerates outmigration of working-age residents, which weakens the demand case for the next service, which accelerates withdrawal.`


---

*Generated from `problem.tasman.inequality.rural_isolation` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
