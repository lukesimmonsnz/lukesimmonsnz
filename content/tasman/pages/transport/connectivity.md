---
title: "Sparse multi-modal transport options across rural Tasman"
section: transport
subpage: connectivity
order: 1
updated: 2026-04-26
summary: >
  Tasman has no rail service and only limited public transport; the region depends almost entirely on two state highways (SH6 between Nelson and Richmond, and SH60 from Richmond to Motueka and Takaka) carrying around 38,000 daily vehicle movements. Bus frequencies are 1-2 services per day on main corridors, and there is no scheduled commercial air service inside the region.
status: draft
generated_from: problem.tasman.transport.connectivity
---

# Sparse multi-modal transport options across rural Tasman

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## A car-dependent region with thin alternatives

Outside Richmond and Motueka, Tasman residents have effectively no public-transport alternative to private vehicles. InterCity coach and a handful of community shuttles run at frequencies that cannot serve commuting, school, or medical-appointment patterns; the result is high private-vehicle mode share and household exposure to fuel-price volatility (claim.tasman.transport.connectivity_claim).


## No regional spine to fall back on

Without a rail option and with only one feasible road corridor connecting most settlements, any disruption on SH6 or SH60 propagates across the whole network. Tasman's geography compounds this: ranges, river valleys, and the Takaka Hill leave few realistic alignments for redundant routes.


---


## Drivers

The following structural drivers contribute to this problem.


### Low population density and dispersed demand



- **Category:** demographic
- **Timescale:** long
- **Consensus:** consensus

### Single-corridor topography of Tasman



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing transport challenges.

**Flagship moves:**

- Build dedicated cycling and walking infrastructure connecting Tasman urban centres
- Expand bus frequency and coverage on key corridors
- Develop park-and-ride facilities at key transport nodes

**Tensions:**

- Transport investment requires sustained funding and may face competing regional priorities.
- Mode shift away from private cars faces social resistance in car-dependent communities.

**Interventions on the system:**

- Improve transport connectivity and mode choice in Tasman (state variable: `transport_accessibility`, sign: +)
- Invest in active transport infrastructure (state variable: `active_mode_share`, sign: +)


---

## Claims cited on this page

- **Tasman has no rail service; SH6 (Nelson-Richmond) and SH60 (Richmond-Motueka-Takaka) are primary state highways serving 38,000 daily vehicle movements. Bus services (InterCity, local shuttles) operate limited routes; frequency is 1-2 services/day on main corridors. No commercial air service; Motueka airfield is private charter only.** [value: 38000 daily vehicle movements (SH6/SH60); 2023] — Waka Kotahi State Highway Network – Tasman Region 2023; Tasman District Council Annual Plan 2024.

---

## Further reading


- **Waka Kotahi State Highway Network – Tasman Region 2023** — Waka Kotahi NZ Transport Agency (Waka Kotahi), 2023 — <https://www.nzta.govt.nz>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* private_vehicle_mode_share, daily_corridor_vehicle_movements.

*Constraints:* low_population_density, topographic_corridor_constraint.

*Inputs:* state_highway_investment, regional_public_transport_subsidy.


*Feedback loops:*

- `Low patronage justifies low service frequency, which reinforces car dependence and further suppresses patronage.`


---

*Generated from `problem.tasman.transport.connectivity` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
