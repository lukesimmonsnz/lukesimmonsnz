---
title: "Cyclone and flood risk"
section: climate
subpage: cyclone-flood-risk
order: 2
updated: 2026-04-26
summary: >
  Hawke's Bay is exposed to tropical cyclone risk and extreme rainfall flooding. Napier, Hastings, and river valleys face inundation risk. Stopbanks and drainage systems are undersized for climate-intensified rainfall. Flood damage costs are rising.
status: draft
generated_from: problem.hawkes_bay.climate.cyclone_flood_risk
---

# Cyclone and flood risk

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Cyclone Gabrielle Impact

Cyclone Gabrielle flooded approximately 2,500 homes and 1,200 businesses in Napier and Hastings. Estimated flood damage was $2-3 billion.


## Repeat Risk

Hawke's Bay will likely experience similar-magnitude cyclone and extreme rainfall events every 15-25 years under current climate trajectory. Probability is rising.


---


## Drivers

The following structural drivers contribute to this problem.


### Rainfall intensification and extreme weather acceleration



- **Category:** physical
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

- **Cyclone Gabrielle (February 2023) caused estimated flood damage of $3-5 billion to Hawke's Bay — the largest civil defence emergency in New Zealand history — devastating Wairoa, Heretaunga Plains, Napier, and rural orchards. The event exposed critical gaps in surface water management and accelerated watershed-scale stormwater infrastructure planning across the region.** [value: 4000 NZD millions (Hawke's Bay regional estimate, midpoint); 2023] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* flood_annual_exceedance_probability, flood_prone_assets_dollars_billions.

*Constraints:* flood_protection_infrastructure_standard, maintenance_and_renewal_funding.

*Inputs:* rainfall_intensification, urban_sprawl_into_flood_zones.


*Feedback loops:*

- `Floods damage infrastructure; repairs consume budgets; deferred maintenance worsens future flood risk.`


---

*Generated from `problem.hawkes_bay.climate.cyclone_flood_risk` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
