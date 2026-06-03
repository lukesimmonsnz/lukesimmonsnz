---
title: "Compounding climate risk in the Nelson basin"
section: climate
subpage: climate_risk
order: 1
updated: 2026-04-26
summary: >
  Nelson sits at the confluence of several climate-amplified hazards: elevated wildfire risk in dry summer hill country, rainfall-runoff flooding in the Maitai and Brook catchments, and creeping coastal inundation around Port Nelson. Mean annual temperature has risen about 1.1 degrees C since the 1970-1999 baseline, and rainfall variability is intensifying, stressing water, agriculture, and infrastructure systems simultaneously.
status: draft
generated_from: problem.nelson.climate.climate_risk
---

# Compounding climate risk in the Nelson basin

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## A multi-hazard climate envelope

Nelson's small size and concentrated valley geography mean a single weather pattern can stress water supply, fire risk, and stormwater systems at once. The August 2022 storm produced concentrated rainfall and slips across the Maitai and Brook catchments and damaged hundreds of properties, while just months earlier the region had been managing through a long summer drought. Climate change is projected to widen this swing between extremes.


## Adaptation gap and institutional load

Adaptation planning is led by Nelson City Council and Tasman District Council, with statutory obligations under the Climate Change Response Act and the National Adaptation Plan. Capital renewals for stormwater and three-waters infrastructure already lag the maintenance baseline; additional adaptation investment competes against deferred maintenance and growth-driven capacity upgrades within the same constrained rates base (claim.nelson.climate.climate_2_claim).


---


## Drivers

The following structural drivers contribute to this problem.


### Anthropogenic climate change in the Tasman-Nelson region



- **Category:** climate
- **Timescale:** long
- **Consensus:** consensus

### Land-use intensification and wildland-urban interface expansion



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

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

- **Nelson city is exposed to sea level rise and coastal inundation. Port Nelson and the central city lie 0–1.5 m above mean high water spring tide. MBIE climate projections estimate 0.75 m mean sea level rise by 2100 under RCP 4.5 scenario; combined with storm surge and subsidence risk from the Waimea Fault zone, routine high-tide flooding of port infrastructure and CBD fringe zones is likely by 2055–2070.** [value: 0.75 m sea level rise by 2100; to 2100; critical window 2055-2070] *(confidence: medium)* — Nelson City Council Annual Plan 2024.

---

## Further reading


- **Nelson City Council Annual Plan 2024** — Nelson City Council (Nelson City Council), 2024 — <https://www.nelsoncitycouncil.co.nz>


---

## Technical notes

*State variables:* mean_annual_temperature_anomaly_c, high_fire_danger_days_per_year, stormwater_capacity_utilisation_ratio.

*Constraints:* rates_base_capacity, valley_topography, consenting_lead_time.

*Inputs:* national_emissions_trajectory, council_adaptation_capex, land_use_change.


*Feedback loops:*

- `Damage-investment feedback: visible damage events (2019 fire, 2022 flood) raise short-term political will for adaptation, but capital programmes lag electoral cycles and revert to baseline within 2-3 years.`


---

*Generated from `problem.nelson.climate.climate_risk` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
