---
title: "Water availability under sustained pressure"
section: climate
subpage: climate_4
order: 4
updated: 2026-04-26
summary: >
  Nelson-Tasman water supply is approaching a binding constraint. The Waimea Plains aquifer supplies roughly 70 percent of municipal and agricultural water; summer restrictions are now standard. Maitai Dam yield is running 8-12 percent below its design assumptions, and demand is projected to exceed sustainable yield by around 2035 without active demand reduction.
status: draft
generated_from: problem.nelson.climate.climate_4
---

# Water availability under sustained pressure

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## A small region, two squeezed supplies

Nelson City draws from the Maitai Dam and the Roding River; Tasman District draws heavily on the Waimea aquifer through an irrigation-and-supply scheme augmented by the recently completed Waimea Community Dam (claim.nelson.climate.climate_4_claim). Both sources show climate-altered yield: snowmelt timing and rainfall pattern shifts have reduced reliable yield even before population growth is layered in.


## Demand-management policy gap

Nelson and Tasman councils operate independent water networks, and demand-management instruments (universal metering, restrictions, pricing) are unevenly applied. Without coordinated demand management, the projected 2035 supply gap will arrive earlier in dry years.


---


## Drivers

The following structural drivers contribute to this problem.


### Land-use intensification and wildland-urban interface expansion



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing climate challenges.

**Flagship moves:**

- Implement evidence-based climate policy in Nelson
- Increase investment in climate services and infrastructure
- Build cross-sector partnerships to address climate challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for climate (state variable: `climate_outcome_index`, sign: +)
- Secondary intervention for climate (state variable: `climate_service_access`, sign: +)


---

## Claims cited on this page

- **Nelson-Tasman water availability is under sustained pressure. The Waimea Plains aquifer supplies 70% of municipal and agricultural water; summer restrictions are now standard (last five years all had seasonal restrictions July-February). Maitai Dam yield has declined 8-12% relative to design assumptions due to climate-altered snowmelt and rainfall patterns; demand is projected to exceed sustainable yield by 2035 without demand reduction.** [value: 70 percent of water supply from Waimea aquifer; 2019-2024] — Nelson Tasman Water Strategy 2023.

---

## Further reading


- **Nelson Tasman Water Strategy 2023** — Nelson City Council / Tasman District Council (Nelson City Council), 2023 — <https://www.nelsoncitycouncil.co.nz>


---

## Technical notes

*State variables:* annual_yield_million_m3, summer_demand_million_m3, aquifer_drawdown_metres_per_year.

*Constraints:* catchment_size, aquifer_safe_yield, interagency_coordination.

*Inputs:* population_growth, irrigation_demand, rainfall_anomaly.


*Feedback loops:*

- `Yield-demand feedback: as climate-altered yield falls and growth-driven demand rises, the headroom for restrictions narrows year-on-year, accelerating the date of binding shortage.`


---

*Generated from `problem.nelson.climate.climate_4` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
