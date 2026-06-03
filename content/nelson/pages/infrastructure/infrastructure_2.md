---
title: "Bulk water supply at a binding constraint"
section: infrastructure
subpage: infrastructure_2
order: 2
updated: 2026-04-26
summary: >
  Maitai Dam (built 1957) has a design yield of 38 million cubic metres per year; actual yield has fallen to 33-35 million m3/year from climate-altered snowmelt and rainfall. Demand is rising around 2 percent annually; without demand reduction, deficit will reach 8-12 million m3/year by 2035. The Waimea Plains aquifer (supplying around 70 percent of water) is being drawn down 0.5-0.8 m/year faster than recharge rates, with sustainability thresholds expected 2028-2032.
status: draft
generated_from: problem.nelson.infrastructure.infrastructure_2
---

# Bulk water supply at a binding constraint

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Two stressed sources, one demand curve

Both the surface and aquifer supplies are now operating below their design assumptions (claim.nelson.infrastructure.infrastructure_2_claim). The demand curve has not slowed: population growth and irrigation growth combine.


## Augmentation pathway and risk

Planning for a new bulk-water scheme (Bossons Aquifer, around 80 km north of central Nelson) began in 2023, but consenting, iwi engagement, and capital cost mean the scheme cannot deliver before the projected deficit window. Demand-side management (universal metering, restrictions, pricing) is the only short-term lever available.


---


## Drivers

The following structural drivers contribute to this problem.


### Asset-age and climate-mismatch in core networks



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing infrastructure challenges.

**Flagship moves:**

- Implement evidence-based infrastructure policy in Nelson
- Increase investment in infrastructure services and infrastructure
- Build cross-sector partnerships to address infrastructure challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for infrastructure (state variable: `infrastructure_outcome_index`, sign: +)
- Secondary intervention for infrastructure (state variable: `infrastructure_service_access`, sign: +)


---

## Claims cited on this page

- **Water supply infrastructure in Nelson-Tasman is at a critical juncture. Maitai Dam, built 1957, has a design yield of 38 million m³/year; actual yield has declined to 33–35 million m³/year due to climate-altered snowmelt and rainfall. Population growth forecasts demand increasing 2% annually; without demand reduction, deficit will reach 8–12 million m³/year by 2035. The Waimea Plains aquifer (supplying 70% of water) is being drawn down 0.5–0.8 m/year faster than recharge rates; sustainability thresholds will be crossed 2028–2032 if extraction continues unabated. Planning for a new bulk water scheme (Bossons Aquifer, 80 km north) began 2023 but faces environmental and Iwi concerns; capacity delivery is uncertain.** [value: 35 million m³/year Maitai Dam yield (vs. 38 design); 2023] — Nelson Tasman Water Strategy 2023.

---

## Further reading


- **Nelson Tasman Water Strategy 2023** — Nelson City Council / Tasman District Council (Nelson City Council), 2023 — <https://www.nelsoncitycouncil.co.nz>


---

## Technical notes

*State variables:* annual_yield_million_m3, annual_demand_million_m3, aquifer_drawdown_metres_per_year.

*Constraints:* catchment_size, consenting_lead_time, iwi_partnership_process.

*Inputs:* augmentation_capex, demand_management_policy.


*Feedback loops:*

- `Augmentation-demand feedback: announced augmentation reduces near-term political pressure for demand management, allowing demand to grow into the eventual delivered capacity, deferring rather than resolving the constraint.`


---

*Generated from `problem.nelson.infrastructure.infrastructure_2` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
