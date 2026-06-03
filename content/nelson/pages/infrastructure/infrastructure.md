---
title: "Cumulative deferred maintenance across core infrastructure"
section: infrastructure
subpage: infrastructure
order: 1
updated: 2026-04-26
summary: >
  Nelson's core infrastructure carries a cumulative deferred-maintenance and capacity-renewal load. Three Waters assets require around $180-220 million in maintenance and renewal over 10 years against a current allocation of about $120 million. Stormwater is undersized for climate-altered rainfall (three events 2021-2023 caused $8-12 million in damage). The Bells Island wastewater plant requires a $35-45 million upgrade by 2028, and the roading backlog is around $45 million.
status: draft
generated_from: problem.nelson.infrastructure.infrastructure
---

# Cumulative deferred maintenance across core infrastructure

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Backlog versus capacity

Each individual asset class is under pressure; cumulatively the renewal backlog is substantially larger than the council can fund out of rates alone (claim.nelson.infrastructure.infrastructure_claim). Asset-management systems are incomplete, so the headline numbers are themselves uncertain.


## Climate amplification

Stormwater capacity designed for pre-2000 rainfall intensity is repeatedly exceeded by current events. Renewal is therefore not a one-for-one replacement of ageing pipe but an upsizing programme, which carries a different cost curve.


---


## Drivers

The following structural drivers contribute to this problem.


### Asset-age and climate-mismatch in core networks



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus

### Small population scale against high per-unit infrastructure cost



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing infrastructure challenges.

**Flagship moves:**

- Implement evidence-based infrastructure policy in Nelson
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

- Prioritise three-waters infrastructure renewal in Nelson urban centres
- Establish a multi-year capital works programme for wastewater and stormwater upgrades
- Apply for central government infrastructure co-funding to supplement council rates

**Tensions:**

- Infrastructure renewal requires significant capital expenditure that strains small council budgets.
- Prioritising upgrades may delay other community investment needs.

**Interventions on the system:**

- Accelerate infrastructure renewal investment in Nelson (state variable: `infrastructure_condition_index`, sign: +)
- Prioritise water and wastewater upgrades (state variable: `service_coverage`, sign: +)


---

## Claims cited on this page

- **Nelson's core infrastructure faces cumulative deferred maintenance and capacity constraints. Three Waters (water, wastewater, stormwater) assets require $180–220 million in maintenance and renewal over 10 years; current budget allocation is $120 million, creating a backlog. Stormwater management is undersized for climate-altered rainfall intensity; three flood events in 2021-2023 caused $8–12 million in damage. Wastewater treatment plant at Bells Island requires $35–45 million upgrade by 2028. Roading network maintenance backlog is $45 million; SH6 and SH60 are under-resourced for growing traffic. Asset management systems are incomplete; condition data are fragmented across systems.** [value: 200 million NZD infrastructure gap over 10 years; 2024-2034] *(confidence: medium)* — Nelson City Council Annual Plan 2024.

---

## Further reading


- **Nelson City Council Annual Plan 2024** — Nelson City Council (Nelson City Council), 2024 — <https://www.nelsoncitycouncil.co.nz>


---

## Technical notes

*State variables:* three_waters_renewal_backlog_nzd_m, roading_backlog_nzd_m, stormwater_event_damage_5yr_nzd_m.

*Constraints:* debt_covenants, construction_workforce, consenting_lead_time.

*Inputs:* central_co_funding, rates_increase, borrowing_headroom.


*Feedback loops:*

- `Backlog-event feedback: deferred renewal raises failure probability, and each failure event consumes both response budget and political will, leaving less capacity for forward renewal.`


---

*Generated from `problem.nelson.infrastructure.infrastructure` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
