---
title: "Constrained regional connectivity: no rail, limited air"
section: transport
subpage: connectivity
order: 1
updated: 2026-04-26
summary: >
  Nelson's regional connectivity rests on State Highway 6 (to Blenheim and the Cook Strait ferries) and SH60 (to Tasman); both are single-lane in sections and create bottlenecks at peak and during closures. There is no direct rail to Wellington or Christchurch. Long-distance coach gives 2-3 daily services with 5-7 hour journeys. Nelson Airport handles around 280,000 passengers per year, mostly domestic.
status: draft
generated_from: problem.nelson.transport.connectivity
---

# Constrained regional connectivity: no rail, limited air

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Two-lane geography

Nelson is a two-lane region in a country where every other city its size has either rail, motorway, or major airport redundancy (claim.nelson.transport.connectivity_claim). Every freight tonne and every visitor moves on the same two state highways or through one regional airport.


## Freight, emissions, and resilience

Road dominance imposes three concurrent costs: per-tonne freight cost is higher than rail-served regions, transport emissions per capita are elevated, and the network is exposed to single-point closures (slips, weather, accidents).


---


## Drivers

The following structural drivers contribute to this problem.


### Single-corridor road dependence and absence of rail



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus

### Topographic and demographic limits on active and public transport



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing transport challenges.

**Flagship moves:**

- Build dedicated cycling and walking infrastructure connecting Nelson urban centres
- Expand bus frequency and coverage on key corridors
- Develop park-and-ride facilities at key transport nodes

**Tensions:**

- Transport investment requires sustained funding and may face competing regional priorities.
- Mode shift away from private cars faces social resistance in car-dependent communities.

**Interventions on the system:**

- Improve transport connectivity and mode choice in Nelson (state variable: `transport_accessibility`, sign: +)
- Invest in active transport infrastructure (state variable: `active_mode_share`, sign: +)


---

## Claims cited on this page

- **Nelson's regional connectivity is constrained by the absence of rail and limited air capacity. The region relies on State Highway 6 (to Blenheim/Marlborough and south) and SH60 (to Tasman); both are single-lane in sections, creating bottlenecks during peak travel and poor resilience to closures. No direct rail service to Wellington or Christchurch exists; long-distance coach services (Intercity, regional operators) provide 2–3 daily services, with journey times 5–7 hours. Nelson Airport handles ~280,000 passengers annually (primarily domestic); international routes are limited to seasonal charters. Road transport dominance creates cost, emissions, and resilience vulnerabilities.** — Waka Kotahi State Highway Network – Nelson Region 2023.

---

## Further reading


- **Waka Kotahi State Highway Network – Nelson Region 2023** — Waka Kotahi NZ Transport Agency (Waka Kotahi), 2023 — <https://www.nzta.govt.nz>


---

## Technical notes

*State variables:* sh6_daily_vehicle_km, freight_mode_share_road_pct, regional_air_passengers_per_year.

*Constraints:* absence_of_rail, topography, airport_runway_length.

*Inputs:* nzta_capex_allocation, airport_route_settings.


*Feedback loops:*

- `Road-only feedback: in the absence of mode alternatives, every additional freight or passenger trip lands on the road network, raising congestion and resilience exposure on the same single corridor.`


---

*Generated from `problem.nelson.transport.connectivity` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
