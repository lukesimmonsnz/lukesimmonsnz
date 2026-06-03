---
title: "Water supply and demand management"
section: infrastructure
subpage: water
order: 2
updated: 2026-04-26
summary: >
  Hawke's Bay aquifers are being over-extracted, particularly for irrigation. Groundwater levels are declining; droughts stress supply. Treatment and distribution infrastructure is aging. Rural and urban supply security is at risk.
status: draft
generated_from: problem.hawkes_bay.infrastructure.water
---

# Water supply and demand management

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Aquifer Stress

Napier and Hastings aquifers serve approximately 150k people and 40k hectares of irrigation. Extraction has outpaced recharge since 2010.


## Drought Exposure

Hawke's Bay experienced severe drought in 2022 and 2023. Restrictions were imposed on non-essential urban water use.


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

- **Aquifer stress indices in Hawke's Bay (Heretaunga Plains, central basin) indicate elevated groundwater extraction relative to recharge, exacerbated by drought (1-in-7 historical → 1-in-4 projected by 2070). Wine grapes and apple orchards in Gimblett Gravels draw heavily on confined aquifers; irrigation intensification risks long-term aquifer depletion and saline intrusion in coastal zones near Napier/Ahuriri.** *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* aquifer_water_level_metres, water_demand_l_per_capita_per_day.

*Constraints:* aquifer_recharge_rate, treatment_capacity_ceiling.

*Inputs:* irrigation_expansion_trend, drought_frequency_increase.


*Feedback loops:*

- `Over-extraction lowers water table; marginal bores fail; users deepen wells; recharge lags extraction; aquifer eventually fails.`


---

*Generated from `problem.hawkes_bay.infrastructure.water` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
