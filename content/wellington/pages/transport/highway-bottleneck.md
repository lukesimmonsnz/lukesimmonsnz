---
title: "State highway congestion and single-point failures in Wellington"
section: transport
subpage: highway-bottleneck
order: 3
updated: 2026-04-26
summary: >
  Wellington's state highway network carries volumes far exceeding its design capacity on key urban sections. Transmission Gully (opened 2022) has provided partial relief on the northern corridor but has not resolved congestion in the inner city and Hutt Valley, where tunnels and narrow corridors remain binding constraints.
status: draft
generated_from: problem.wellington.transport.highway_bottleneck
---

# State highway congestion and single-point failures in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Transmission Gully and residual congestion

Transmission Gully opened in 2022 as the major highway investment of the past decade, providing an inland alternative to the coastal SH1 north of Wellington. Initial congestion relief on the northern corridor has been measurable but the inner-city network — particularly the Terrace and Mt Victoria tunnels — remains severely congested (claim.wellington.transport.transmission_gully_opened_2022).


## Congestion costs

Wellington's travel time index on key morning-peak corridors is among the highest in New Zealand relative to city size, reflecting the geometric constraint imposed by the harbour and hills (claim.wellington.transport.state_highway_congestion_index).


---


## Drivers

The following structural drivers contribute to this problem.


### Car-dependent suburban land-use pattern



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Geographic single-corridor constraint



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus

### Induced demand from road capacity additions



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Demand Management and Mode Shift

Road pricing and park-and-ride investment will shift commuters to existing public transport without costly new road infrastructure.

**Flagship moves:**

- Introduce Wellington CBD congestion charge during peak hours
- Expand park-and-ride at Johnsonville, Porirua, and Upper Hutt stations
- Remove free CBD parking in council-owned buildings

**Tensions:**

- Congestion charging is regressive without adequate public transport alternatives for outer-suburb residents
- Political resistance from motorists and suburban retailers is significant

**Interventions on the system:**

- Pilot cordon pricing scheme on SH1 entry points with revenue hypothecated to PT improvement (state variable: `vkt_peak_hour`, sign: -)


### Road Corridor Capacity Expansion

New road tunnels through the Wellington hills are essential to reduce congestion and provide resilient corridors.

**Flagship moves:**

- Progress Mt Victoria second tunnel to construction within this decade
- Advance Terrace Tunnel replacement to four-lane capacity
- Improve SH2 Upper Hutt resilience with alternative alignment

**Tensions:**

- Induced demand will erode congestion benefits within 10–15 years
- Large capital projects crowd out frequent-service public transport investment
- Carbon intensity of construction conflicts with Wellington City's climate commitments

**Interventions on the system:**

- Begin detailed business case for Mt Victoria second tunnel and Terrace Tunnel replacement (state variable: `cross_isthmus_capacity`, sign: +)


---

## Claims cited on this page

- **Transmission Gully motorway opened in March 2022 as a tolled inland alternative to the coastal SH1 between Mackays Crossing and Linden, providing route redundancy for the northern Wellington corridor but not resolving congestion through the inner-city tunnel bottlenecks.** — NZTA Wellington Transport Corridor: State Highway Performance Report 2023.
- **Wellington's morning peak travel time index on key CBD-approach corridors is among the highest in New Zealand relative to city size, reflecting the geometric constraints imposed by harbour coastline and hills on road network capacity expansion.** *(confidence: medium)* — NZTA Wellington Transport Corridor: State Highway Performance Report 2023; Wellington Regional Land Transport Plan 2021–31.

---

## Further reading


- **NZTA Wellington Transport Corridor: State Highway Performance Report 2023** (NZ Transport Agency Waka Kotahi), 2023 — <https://www.nzta.govt.nz/roads-and-rail/roads/state-highways/>

- **Wellington Regional Land Transport Plan 2021–31** (Greater Wellington Regional Council), 2021 — <https://www.gw.govt.nz/transport/regional-land-transport-plan/>


---

## Technical notes

*State variables:* congestion_delay_index, incident_recovery_time.

*Constraints:* inner_city_tunnel_capacity, coastal_corridor_width.

*Inputs:* vehicle_km_travelled, road_capacity_km.


*Feedback loops:*

- `Induced demand loop: road capacity additions attract additional vehicle trips, partially or fully absorbing congestion relief within 5–10 years.`


---

*Generated from `problem.wellington.transport.highway_bottleneck` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
