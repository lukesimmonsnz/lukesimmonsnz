---
title: "Underdeveloped active and public transport in central Nelson"
section: transport
subpage: connectivity_4
order: 4
updated: 2026-04-26
summary: >
  Cycling mode share is around 6.2 percent of commute trips (against 5 percent nationally), but dedicated cycle-lane coverage is around 18 km of a 280 km inner-city road network (about 6.4 percent). Pedestrian infrastructure in outer suburbs is incomplete. Public transport (NCC city buses plus regional services) covers around 3 percent of commute mode share with 1-2 hourly frequency. Car dependency is around 68 percent of commutes; SH6 northbound and Haven Road peak each weekday.
status: draft
generated_from: problem.nelson.transport.connectivity_4
---

# Underdeveloped active and public transport in central Nelson

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Latent demand without enabling infrastructure

Nelson's cycling mode share is already above national average despite limited dedicated infrastructure, indicating substantial latent demand that better network coverage would activate (claim.nelson.transport.connectivity_4_claim). Topography is moderately favourable in the central basin and challenging on the hill suburbs.


## Public transport thinness

City-bus frequency in Nelson is well below the threshold where non-car households can rely on public transport for everyday trips. Park-and-ride at SH6 is minimal. The result is that even households who would prefer to reduce car use have limited practical alternative.


---


## Drivers

The following structural drivers contribute to this problem.


### Topographic and demographic limits on active and public transport



- **Category:** physical
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

- **Active travel and urban transport infrastructure in Nelson is underdeveloped. Cycling mode share is 6.2% of commute trips (vs. 5% nationally), but dedicated cycle lane coverage is only 18 km of the 280 km inner-city road network (6.4%). Pedestrian infrastructure (footpaths, crossings) in outer suburbs (Tasman Cob, Stoke, Motueka periphery) is incomplete or substandard. Public transport (regional bus operator Motueka Shuttles, plus NCC city buses) covers 3% of commute mode share; service frequency is 1–2 hourly, insufficient for non-car dependence. Park-and-ride facilities at SH6 are minimal. Car dependency is 68% of commute trips; congestion on SH6 northbound and Haven Road peaks 7.30–8.45 am and 4.15–5.30 pm.** [value: 6.2 percent cycling mode share; 2023] *(confidence: medium)* — Waka Kotahi State Highway Network – Nelson Region 2023.

---

## Further reading


- **Waka Kotahi State Highway Network – Nelson Region 2023** — Waka Kotahi NZ Transport Agency (Waka Kotahi), 2023 — <https://www.nzta.govt.nz>


---

## Technical notes

*State variables:* cycling_mode_share_pct, dedicated_cycle_lane_km, city_bus_frequency_per_hour_peak.

*Constraints:* roading_corridor_widths, rates_funded_pt_subsidy.

*Inputs:* ncc_active_transport_capex, nzta_co_funding.


*Feedback loops:*

- `Frequency-demand feedback: low service frequency suppresses ridership, which keeps fare-recovery low, which suppresses council willingness to fund higher frequency.`


---

*Generated from `problem.nelson.transport.connectivity_4` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
