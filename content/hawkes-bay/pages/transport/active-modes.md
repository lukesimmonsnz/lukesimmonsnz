---
title: "Active transport mode accessibility and uptake"
section: transport
subpage: active-modes
order: 2
updated: 2026-04-26
summary: >
  Cycling and walking infrastructure is fragmented and unsafe. Pedestrian and cycle networks in Napier and Hastings do not connect efficiently to schools, shops, or workplaces. Low mode share reflects lack of investment and suburban sprawl.
status: draft
generated_from: problem.hawkes_bay.transport.active_modes
---

# Active transport mode accessibility and uptake

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Low Mode Share

Walking and cycling account for less than 5% of commute trips in Hawke's Bay, well below national averages.


## Network Fragmentation

Cycling routes in Napier CBD are disconnected from suburban residential areas and schools, making it impractical for families.


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic isolation and dispersed population



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Public transport investment and subsidies

Public transport investment and subsidies is the primary strategy.

**Flagship moves:**

- Implement Public transport investment and subsidies across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Public transport investment and subsidies intervention (state variable: `public_investment_index`, sign: +) (relaxes: `public_investment_constraint`)


---

## Claims cited on this page

- **Transport connectivity in Hawkes Bay is limited outside major urban centers, forcing private vehicle dependence. Public transit is sparse; road freight reliance increases logistics costs; geographic isolation constrains workforce mobility and business access to markets.** [value: 5 percent mode share; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* active_mode_share_percent, cycle_network_km_connected.

*Constraints:* hilly_terrain_cycle_barriers, weather_rainfall_days.

*Inputs:* suburban_land_use_patterns, pedestrian_safety_perception.


*Feedback loops:*

- `Low uptake justifies lower investment; poor network deters new users; car dependence entrenches.`


---

*Generated from `problem.hawkes_bay.transport.active_modes` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
