---
title: "Coastal erosion and sea-level rise"
section: climate
subpage: coastal-hazard
order: 2
updated: 2026-04-26
summary: >
  Napier and Hastings coastlines are eroding. Sea-level rise accelerates inundation risk for coastal properties, infrastructure, and Port of Napier. Coastal protection decisions (hard defenses vs. retreat) lack strategic consensus.
status: draft
generated_from: problem.hawkes_bay.climate.coastal_hazard
---

# Coastal erosion and sea-level rise

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Erosion Rate

Napier coastline is eroding at 0.3-0.5 metres per year in some locations. Some beaches have retreated 40+ metres over 20 years.


## Sea-Level Rise Risk

Port of Napier and low-lying residential areas face inundation risk from 0.5-1.5 metre sea-level rise by 2100. Adaptation options include seawalls or managed retreat.


---


## Drivers

The following structural drivers contribute to this problem.


### Urban development in hazard-exposed zones



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Flood resilience and protection infrastructure

Investing in upgraded stopbanks, stormwater systems, and natural flood defences reduces inundation risk from climate-intensified rainfall and sea-level rise.

**Flagship moves:**

- Upgrade Napier and Hastings stopbanks to 1-in-100-year standard within 10 years
- Invest in stormwater storage and retention ponds across urban areas
- Establish wetland and riparian buffers for flood attenuation

**Tensions:**

- Infrastructure upgrades require $2+ billion investment over 10 years
- Protection infrastructure may increase settlement in flood-prone areas (moral hazard)
- Natural solutions (wetlands, riparian) require land acquisition at high cost

**Interventions on the system:**

- Upgrade Napier and Hastings stopbanks to 1-in-100-year rainfall standard (state variable: `flood_protection_standard_exceedance_days`, sign: -)
- Build stormwater retention ponds and wetland buffers in urban flood-prone zones (state variable: `flood_attenuation_capacity_litres`, sign: +)


---

## Claims cited on this page

- **Napier coastline is eroding at 0.3-0.5 metres per year in some locations (Ahuriri, Westshore), accelerated by sea-level rise and increased stormwater discharge. Coastal retreat threatens municipal infrastructure and necessitates managed realignment planning.** [value: 0.4 metres per year erosion; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* coastal_erosion_rate_metres_per_year, sea_level_rise_mm_per_year.

*Constraints:* coastal_protection_cost_per_km, land_use_planning_and_zoning.

*Inputs:* eustatic_sea_level_rise, local_land_subsidence.


*Feedback loops:*

- `Erosion threatens property values; owners relocate; property values drop more; adaptation investment seems pointless.`


---

*Generated from `problem.hawkes_bay.climate.coastal_hazard` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
