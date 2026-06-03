---
title: "Active Transport Network Fragmentation"
section: transport
subpage: active_modes
order: 3
updated: 2026-04-26
summary: >
  Canterbury's cycling and walking networks are fragmented, with Major Cycle Routes incomplete in Christchurch metro. Cycling commute share remains ~5%, far below target of 20%. Safety concerns and connectivity gaps deter mode shift.

status: draft
generated_from: problem.canterbury.transport.active_modes
---

# Active Transport Network Fragmentation

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Incomplete Major Cycle Routes

Christchurch's Major Cycle Routes programme targets 280 km by 2030, but only ~40% complete (2024). Gaps in key corridor connections (e.g., SH73 bridge crossing, arterial parallels) force cyclists onto high-traffic roads, deterring uptake. Cycling commute share stuck at 5%.


---


## Drivers

The following structural drivers contribute to this problem.


### Safety Perception Barriers to Active Transport



- **Category:** demographic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Last-Mile Micromobility Solutions (E-Scooters, E-Bikes, Bikeshare)

Expanded micromobility networks (shared e-scooters/bikes, charge stations) fill gaps between transit stops and destinations, improving mode shift to public transport.

**Flagship moves:**

- Key intervention for Last-Mile Micromobility Solutions (E-Scooters, E-Bikes, Bikeshare)

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Expanded micromobility networks (shared e-scooters/bikes, charge stations) fill gaps between transit stops and destinations, improving mode shift to public transport. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


### Major Cycle Routes & Active Transport Network Completion

Rapid completion of Major Cycle Routes and pedestrian-friendly streetscapes (protected infrastructure) will shift 5-10% of short trips to active modes.

**Flagship moves:**

- Key intervention for Major Cycle Routes & Active Transport Network Completion

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Rapid completion of Major Cycle Routes and pedestrian-friendly streetscapes (protected infrastructure) will shift 5-10% of short trips to active modes. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


---

## Claims cited on this page

- **Cycling commute share in Christchurch remains 2-3% despite flat terrain and post-earthquake planning opportunities. Recent cycleways (Willow-Avon, Cashmere) show promise; further investment requires $50-100M; integration with rapid transit is planned.** [value: 5.2 percent; 2023] — Aotearoa New Zealand 2023 Census Place Summary — Canterbury Region; Christchurch Transport Strategy 2024-2044.
- **Christchurch's Major City Rail project rebuild progressed to 35% completion (2023), with ongoing resource and funding constraints. Delays compound congestion pressures; full completion is 2026-2027; rail restoration is essential for post-earthquake economic recovery.** [value: 40 percent completion; 2023] *(confidence: medium)* — Christchurch Transport Strategy 2024-2044.

---

## Further reading


- **Aotearoa New Zealand 2023 Census Place Summary — Canterbury Region** — Statistics New Zealand Tatauranga Aotearoa (Stats NZ), 2024 — <https://www.stats.govt.nz/tools/2023-census-place-summaries/canterbury-region>

- **Christchurch Transport Strategy 2024-2044** (Christchurch City Council), 2023 — <https://www.ccc.govt.nz/the-council/planning-strategy-and-policy/plans-strategies-policies-and-bylaws/transport/>


---

## Technical notes

*State variables:* cycling_commute_share, network_connectivity_index, cycling_crash_rate, walking_commute_share.

*Constraints:* topography_flat_vs_hilly_suburbs, motor_vehicle_dominance_cultural.

*Inputs:* cycling_infrastructure_investment, land_use_density, weather_seasonality.


*Feedback loops:*

- `Dynamic feedback mechanisms drive active transport network fragmentation.`


---

*Generated from `problem.canterbury.transport.active_modes` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
