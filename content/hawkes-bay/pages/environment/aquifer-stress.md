---
title: "Aquifer depletion and groundwater stress"
section: environment
subpage: aquifer-stress
order: 2
updated: 2026-04-26
summary: >
  Napier-Hastings aquifers face unsustainable extraction for irrigation (horticulture, viticulture, dairy pasture). Groundwater tables have declined by 2-4 metres in some catchments over 15 years. Recharge lags extraction.
status: draft
generated_from: problem.hawkes_bay.environment.aquifer_stress
---

# Aquifer depletion and groundwater stress

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Extraction Volume

Irrigation extracts approximately 180-220 million cubic metres annually from Hawke's Bay aquifers — approximately 70% of total water take.


## Groundwater Decline

Groundwater tables in Napier and Hastings aquifers have declined by 2-4 metres in the past 15 years, with some localised areas experiencing 6+ metre declines.


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

- **Environmental degradation in Hawkes Bay includes habitat loss, water quality decline, invasive species pressure, and ecosystem fragmentation. Climate change amplifies these pressures; resource management and restoration efforts are constrained by funding and coordination gaps.** [value: 3 metres decline; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* groundwater_level_decline_metres, irrigation_water_extraction_l_per_sec.

*Constraints:* natural_recharge_rate, environmental_flow_requirements.

*Inputs:* horticulture_expansion, irrigation_intensification.


*Feedback loops:*

- `Extraction lowers water table; users deepen bores; pumping costs rise; marginal farms exit; demand for extraction shrinks (lagged effect).`


---

*Generated from `problem.hawkes_bay.environment.aquifer_stress` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
