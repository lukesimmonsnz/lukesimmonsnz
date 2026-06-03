---
title: "Fragmented active-transport network"
section: transport
subpage: connectivity_4
order: 4
updated: 2026-04-26
summary: >
  Tasman has roughly 18 km of dedicated cycleway, mostly in Richmond and Motueka, but the network is discontinuous and does not connect schools, employment centres, or rural villages. Tasman District Council's Last Kilometre Plan (2024-2027) aims to add 45 km of urban cycleway and footpath and lift the active-commute share to 35 percent by 2030.
status: draft
generated_from: problem.tasman.transport.connectivity_4
---

# Fragmented active-transport network

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## A network of fragments

The 18 km of existing cycleway in Tasman is a series of fragments: short rail-trail links, recreational waterfront paths, and a few protected lanes. Suburban schools report active-commute rates below 30 percent, partly because parents do not consider the network safe between home and school gate (claim.tasman.transport.connectivity_4_claim).


## Connection is the binding constraint

Building the missing links — particularly between residential growth areas and town centres — is what unlocks modal shift. The Last Kilometre Plan targets that gap, but delivery depends on co-funding from Waka Kotahi and on land negotiations with horticultural blocks that abut planned alignments.


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

- **Active transport (walking, cycling) infrastructure in Tasman is fragmented. Richmond and Motueka have some dedicated cycleways (18 km total); suburban schools have <30% active commute rates. TDC is implementing "Last Kilometre Plan" (2024-2027) to build 45 km of urban cycleways and footpaths, targeting 35% active commute rate by 2030.** [value: 18 km existing cycleways; 2024] — Tasman District Council Annual Plan 2024; Waka Kotahi State Highway Network – Tasman Region 2023.

---

## Further reading


- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>

- **Waka Kotahi State Highway Network – Tasman Region 2023** — Waka Kotahi NZ Transport Agency (Waka Kotahi), 2023 — <https://www.nzta.govt.nz>


---

## Technical notes

*State variables:* active_transport_mode_share, km_protected_cycleway.

*Constraints:* rural_distances, fragmented_existing_network.

*Inputs:* active_modes_capex, school_travel_planning.


*Feedback loops:*

- `Disconnected segments fail to attract riders, which reduces political appetite for the next segment, which keeps the network disconnected.`


---

*Generated from `problem.tasman.transport.connectivity_4` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
