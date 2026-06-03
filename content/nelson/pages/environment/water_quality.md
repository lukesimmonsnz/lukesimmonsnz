---
title: "Maitai and Waimea river water-quality decline"
section: environment
subpage: water_quality
order: 3
updated: 2026-04-26
summary: >
  Maitai River water quality has declined over the last decade due to forestry sedimentation, pastoral runoff, and urban stormwater. Nitrate concentrations have risen about 28 percent between 2010 and 2023, and pathogenic bacteria exceed safe-swimming thresholds on 12-15 days per summer. The Maitai is also a primary water source; treatment costs have risen around 14 percent.
status: draft
generated_from: problem.nelson.environment.water_quality
---

# Maitai and Waimea river water-quality decline

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Drinking water and recreation in the same catchment

The Maitai is unusual in that it serves both as Nelson's primary recreational waterway and as a key drinking-water source via the Maitai Dam (claim.nelson.environment.water_quality_claim). Pressure on either function shows up immediately in the other: summer E. coli excursions reduce swimming days at the same time treatment plants raise chlorine and coagulant doses.


## Source-attribution and policy lever

Forestry harvest cycles, pastoral land-use intensity, and urban stormwater each contribute meaningful loads, but the policy levers sit across separate regulators -- Nelson City Council (urban), Tasman District Council (pastoral), and central forestry rules. Coordinated catchment-scale management is improving but lags the rate of decline.


---


## Drivers

The following structural drivers contribute to this problem.


### Cumulative land-use and discharge pressure on shared catchments



- **Category:** regulatory
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing environment challenges.

**Flagship moves:**

- Implement evidence-based environment policy in Nelson
- Increase investment in environment services and infrastructure
- Build cross-sector partnerships to address environment challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for environment (state variable: `environment_outcome_index`, sign: +)
- Secondary intervention for environment (state variable: `environment_service_access`, sign: +)


---

## Claims cited on this page

- **Maitai River water quality has declined over the last decade due to increased sedimentation from forestry operations, pastoral runoff, and urban stormwater. Nitrate concentrations have increased 28% 2010-2023; pathogenic bacteria (E. coli) exceed safe swimming thresholds on 12–15 days per summer season. The Maitai is a key recreation asset and primary water source; water treatment costs have increased 14% to manage contamination. Waimea River shows similar pressures.** [value: 28 percent increase in nitrate concentration 2010-2023; 2010-2023] *(confidence: medium)* — Nelson Tasman Water Strategy 2023.

---

## Further reading


- **Nelson Tasman Water Strategy 2023** — Nelson City Council / Tasman District Council (Nelson City Council), 2023 — <https://www.nelsoncitycouncil.co.nz>


---

## Technical notes

*State variables:* nitrate_concentration_mg_per_l, summer_e_coli_exceedance_days, annual_treatment_cost_nzd.

*Constraints:* regulatory_fragmentation, monitoring_density.

*Inputs:* forestry_harvest_intensity, pastoral_n_loss, urban_stormwater_load.


*Feedback loops:*

- `Quality-cost feedback: declining raw-water quality raises treatment cost, but the residual contamination still constrains recreation and ecological function, so total social cost compounds even as drinking water remains safe.`


---

*Generated from `problem.nelson.environment.water_quality` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
