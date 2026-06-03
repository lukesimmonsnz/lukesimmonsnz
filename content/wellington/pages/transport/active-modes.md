---
title: "Active travel infrastructure gaps in Wellington"
section: transport
subpage: active-modes
order: 4
updated: 2026-04-26
summary: >
  Despite Wellington's compact geography and moderate climate, cycling mode share remains very low relative to peer cities, held back by disconnected cycling infrastructure, safety concerns on shared roads, and topographic barriers. Walking infrastructure is uneven across the region.
status: draft
generated_from: problem.wellington.transport.active_modes
---

# Active travel infrastructure gaps in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Low cycling mode share

Wellington's cycling mode share stands at approximately 2% of all trips, substantially below comparable compact cities such as Christchurch or international benchmarks for cities with similar topography and climate (claim.wellington.transport.cycling_mode_share_low).


## Infrastructure gaps

Wellington's cycling network is characterised by disconnected segments and high-stress shared-road conditions on key commuter corridors. The absence of protected lanes on major arterials between suburbs and the CBD is the primary deterrent to uptake (claim.wellington.transport.active_travel_infrastructure_gap).


---


## Drivers

The following structural drivers contribute to this problem.


### Car-dependent suburban land-use pattern



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Disconnected and unsafe cycling network



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### E-Bike and Micromobility Access

E-bikes and e-scooters overcome Wellington's topographic barrier; subsidy programmes and secure parking can triple cycling mode share.

**Flagship moves:**

- Low-income e-bike purchase subsidy programme ($500 rebate)
- Secure end-of-trip facilities at employment centres and rail stations
- Integrate shared e-bike scheme with Metlink monthly pass

**Tensions:**

- Without protected infrastructure, e-bikes face same safety risks as conventional cycling
- Micromobility schemes require ongoing subsidisation and have uneven equity outcomes

**Interventions on the system:**

- Partner with e-bike retailers for rebate scheme targeting low-income households and long-distance commuters (state variable: `cycling_mode_share`, sign: +)


### Protected Active Mode Network

A connected, safe cycling and walking network will shift short trips from cars and reduce transport system pressure.

**Flagship moves:**

- Complete the Wellington Urban Cycleways Programme gaps on key arterials
- Install protected intersections at all school zones within 5 years
- Continuous waterfront-to-hills greenway connection

**Tensions:**

- Lane reallocation for cycleways increases vehicle congestion on constrained corridors
- Hilly topography limits cycling uptake to a small share of trips citywide

**Interventions on the system:**

- Fund $30M protected cycleway gap-fill programme across Wellington City's arterial network (state variable: `protected_cycleway_km`, sign: +)


---

## Claims cited on this page

- **Wellington's cycling mode share across all trips is approximately 2%, substantially below comparable compact cities and well below the 8% target set in the Wellington City Spatial Plan, reflecting disconnected cycling infrastructure and high-stress shared-road conditions.** [value: 2 percent of all trips; 2022-2023] *(confidence: medium)* — Wellington Regional Land Transport Plan 2021–31; Wellington City Council Annual Plan 2024/25.
- **Wellington's cycling network consists of largely disconnected segments with significant gaps on major commuter corridors between suburbs and the CBD; the absence of protected lanes on key arterials is the primary deterrent to uptake among potential but cautious cyclists.** — Wellington Regional Land Transport Plan 2021–31; Wellington City Council Annual Plan 2024/25.

---

## Further reading


- **Wellington Regional Land Transport Plan 2021–31** (Greater Wellington Regional Council), 2021 — <https://www.gw.govt.nz/transport/regional-land-transport-plan/>

- **Wellington City Council Annual Plan 2024/25** (Wellington City Council), 2024 — <https://www.wellington.govt.nz/your-council/plans-policies-and-bylaws/annual-plan>


---

## Technical notes

*State variables:* cycling_mode_share, protected_cycling_network_km.

*Constraints:* network_connectivity_gaps, arterial_road_safety_barrier.

*Inputs:* active_travel_investment, land_use_density.


*Feedback loops:*

- `Connectivity loop: isolated cycling lanes without network connectivity fail to attract commuter cyclists; low usage reduces political priority for further investment.`


---

*Generated from `problem.wellington.transport.active_modes` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
