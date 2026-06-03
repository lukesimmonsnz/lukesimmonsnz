---
title: "Drought and water stress"
section: climate
subpage: drought-water-stress
order: 2
updated: 2026-04-26
summary: >
  Hawke's Bay faces increased drought risk and water stress. Horticulture, dairy, and municipal supplies are vulnerable. Aquifer recharge is declining relative to extraction. Seasonal water restrictions will become more frequent.
status: draft
generated_from: problem.hawkes_bay.climate.drought_water_stress
---

# Drought and water stress

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Recent Droughts

Hawke's Bay experienced severe drought in 2022-2023. Water restrictions were imposed on non-essential use. Some irrigation was rationed.


## Frequency Increase

Dry years are projected to increase from 1-in-7 years (historical) to 1-in-4 years by 2050. Summer irrigation demand will exceed reliable supply.


---


## Drivers

The following structural drivers contribute to this problem.


### Agricultural irrigation demand exceeding sustainable supply



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Aquifer recharge management and extraction limits

Implementing science-based limits on groundwater extraction and investing in aquifer recharge infrastructure sustains water supply for horticulture and urban use.

**Flagship moves:**

- Set annual extraction limits for Napier and Hastings aquifers based on recharge rates
- Invest in stormwater harvesting and aquifer injection to boost recharge
- Phase out over-allocated irrigation consents and consolidate to sustainable allocations

**Tensions:**

- Extraction limits threaten horticulture expansion and farm profitability
- Consolidation requires large growers to purchase allocation from smaller farmers, consolidating land ownership

**Interventions on the system:**

- Lower annual extraction ceiling for Napier and Hastings aquifers to match recharge rate (state variable: `aquifer_extraction_sustainability_ratio`, sign: +)
- Build stormwater harvesting and aquifer recharge systems (state variable: `recharge_infrastructure_coverage`, sign: +)


---

## Claims cited on this page

- **Dry years are projected to increase from 1-in-7 years (historical, 1960-2020) to 1-in-4 years under RCP 6.0 by 2070 in Hawke's Bay. Horticulture (apples, wine grapes in Gimblett Gravels) and dairy face heightened irrigation demand and aquifer depletion risk.** *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* drought_duration_days_per_year, water_deficit_index.

*Constraints:* groundwater_recharge_rate, water_storage_capacity.

*Inputs:* rainfall_seasonality_shift, irrigation_demand_growth.


*Feedback loops:*

- `Drought increases water demand; over-extraction lowers aquifer; crop failures follow; agricultural viability declines; diversification becomes urgent.`


---

*Generated from `problem.hawkes_bay.climate.drought_water_stress` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
