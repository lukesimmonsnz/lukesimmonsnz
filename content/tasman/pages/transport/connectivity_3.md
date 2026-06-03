---
title: "Car-dependent town form in Richmond and Motueka"
section: transport
subpage: connectivity_3
order: 3
updated: 2026-04-26
summary: >
  Richmond and Motueka have grown around state highways and low-density residential subdivisions, producing a 92 percent private-vehicle mode share and only 2 percent public-transport share. SH6 bisects Richmond's town centre, creating air quality, severance, and pedestrian-safety issues.
status: draft
generated_from: problem.tasman.transport.connectivity_3
---

# Car-dependent town form in Richmond and Motueka

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Sprawl-by-default in the regional centres

The two main towns expanded as ribbon developments along state highways rather than compact, walkable centres. Public-transport mode share is roughly 2 percent and active-transport share around 4 percent, with the remaining 92 percent of trips taken by private vehicle (claim.tasman.transport.connectivity_3_claim).


## Highway-through-town pattern

SH6 runs straight through Richmond's main retail strip, mixing freight, commuter and pedestrian flows. Tasman District Council is planning a Richmond-Motueka bus-rapid-transit corridor with a 20-minute service frequency, supported by NZD 85 million of central funding committed for 2025-2028, but delivery and patronage lag the population growth the new corridor is meant to absorb.


---


## Drivers

The following structural drivers contribute to this problem.


### Low population density and dispersed demand



- **Category:** demographic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Active Travel and Demand Management

Shifting short trips to walking and cycling reduces vehicle demand, improves liveability, and is the most cost-effective congestion response.

**Flagship moves:**

- Build separated cycling infrastructure on key commuter corridors
- Subsidise e-bike purchase for low-income residents
- Introduce school travel plans to reduce car drop-offs

**Tensions:**

- Active travel requires safety infrastructure investment before behaviour change follows
- Limited budget competes with roading maintenance priorities

**Interventions on the system:**

- Develop connected cycling and walking network linking residential areas to employment and retail centres (state variable: `active_mode_share`, sign: +)


---

## Claims cited on this page

- **Motueka and Richmond town centres have developed around car-dependent sprawl; public transport modal share is 2%, bicycle/pedestrian 4%, private vehicle 92%. SH6 bisects Richmond town centre, creating air quality and safety issues. TDC is planning bus-rapid-transit corridor (Richmond-Motueka, 20-minute service frequency) with NZD 85 million central funding commitment (2025-2028).** [value: 92 percent private vehicle mode share; 2023] *(confidence: medium)* — Waka Kotahi State Highway Network – Tasman Region 2023; Tasman District Council Annual Plan 2024.

---

## Further reading


- **Waka Kotahi State Highway Network – Tasman Region 2023** — Waka Kotahi NZ Transport Agency (Waka Kotahi), 2023 — <https://www.nzta.govt.nz>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* private_vehicle_mode_share, town_centre_pedestrian_severance.

*Constraints:* existing_highway_alignment, low_density_zoning_legacy.

*Inputs:* brt_corridor_capex, urban_form_zoning_settings.


*Feedback loops:*

- `Highway-fronting development draws trips onto the highway, which justifies further road widening, which entrenches highway-fronting development.`


---

*Generated from `problem.tasman.transport.connectivity_3` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
