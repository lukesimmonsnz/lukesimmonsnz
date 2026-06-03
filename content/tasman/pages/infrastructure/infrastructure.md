---
title: "Aging three-waters network entering reform"
section: infrastructure
subpage: infrastructure
order: 1
updated: 2026-04-26
summary: >
  Roughly 38 percent of Tasman's three-waters pipe assets are beyond their nominal design life. National three-waters reform requires regional aggregation by 2026; Tasman District Council is consolidating with Nelson City and Marlborough District Council to form Te Hoiere Three Waters Entity, serving around 350,000 residents.
status: draft
generated_from: problem.tasman.infrastructure.infrastructure
---

# Aging three-waters network entering reform

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## An asset base older than the institutions running it

Much of Tasman's reticulated water and wastewater pipe network was laid in the 1960s-1980s and is now at or beyond its design life. The renewal backlog is the starting condition that any post-reform entity inherits (claim.tasman.infrastructure.infrastructure_claim).


## Reform changes accountability, not the pipes

Aggregation across Tasman, Nelson and Marlborough lifts borrowing capacity and specialist-staffing depth, but does not by itself replace any pipe. The substantive renewal programme still has to be priced, funded, and sequenced against growth demands.


---


## Drivers

The following structural drivers contribute to this problem.


### Renewal backlog inherited from a small ratepayer base



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus

### Single-route exposure to weather and geology



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing infrastructure challenges.

**Flagship moves:**

- Implement evidence-based infrastructure policy in Tasman
- Increase investment in infrastructure services and infrastructure
- Build cross-sector partnerships to address infrastructure challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for infrastructure (state variable: `infrastructure_outcome_index`, sign: +)
- Secondary intervention for infrastructure (state variable: `infrastructure_service_access`, sign: +)


### Response: Camp 2

A response strategy addressing infrastructure challenges.

**Flagship moves:**

- Prioritise three-waters infrastructure renewal in Tasman urban centres
- Establish a multi-year capital works programme for wastewater and stormwater upgrades
- Apply for central government infrastructure co-funding to supplement council rates

**Tensions:**

- Infrastructure renewal requires significant capital expenditure that strains small council budgets.
- Prioritising upgrades may delay other community investment needs.

**Interventions on the system:**

- Accelerate infrastructure renewal investment in Tasman (state variable: `infrastructure_condition_index`, sign: +)
- Prioritise water and wastewater upgrades (state variable: `service_coverage`, sign: +)


---

## Claims cited on this page

- **Tasman's three-waters infrastructure (water supply, wastewater, stormwater) is aging; asset life expectancy maps show 38% of pipes exceed design life. Three-waters reform mandates regional aggregation by 2026; TDC is merging with Nelson City Council and Marlborough District Council to form Te Hoiere Three Waters Entity, serving 350,000 residents.** [value: 38 percent pipes beyond design life; 2024] — Tasman District Council Annual Plan 2024; Waimea Aquifer Stress Study 2023.

---

## Further reading


- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>

- **Waimea Aquifer Stress Study 2023** — Tasman District Council / Greater Wellington Regional Council (Tasman District Council), 2023 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* share_pipes_beyond_design_life, annual_renewal_capex.

*Constraints:* rates_affordability_ceiling, construction_workforce_capacity.

*Inputs:* te_hoiere_entity_borrowing_capacity, asset_management_data_quality.


*Feedback loops:*

- `Deferred renewals raise per-incident cost (mains failures, contamination events), which diverts budget away from planned renewals.`


---

*Generated from `problem.tasman.infrastructure.infrastructure` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
