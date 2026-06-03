---
title: "Horticulture labour and RSE scheme dependence"
section: economy
subpage: horticulture-rse
order: 2
updated: 2026-04-26
summary: >
  Hawke's Bay horticulture (apples, kiwifruit, berries) relies on Recognised Seasonal Employer (RSE) scheme workers for 40-50% of harvest labour. Wage suppression, worker exploitation, and policy uncertainty create instability.
status: draft
generated_from: problem.hawkes_bay.economy.horticulture_rse
---

# Horticulture labour and RSE scheme dependence

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Labour Proportion

Approximately 2,500-3,500 RSE workers are employed in Hawke's Bay horticulture during peak season (Jan-March), representing 45-50% of total harvest labour.


## Wage Suppression

Horticulture harvest wages in Hawke's Bay average $22-24/hour, compared to $28/hour in manufacturing. Piece-rate pay systems create income volatility.


---


## Drivers

The following structural drivers contribute to this problem.


### Export commodity price volatility



- **Category:** economic
- **Timescale:** short
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


### Horticulture sector support and value-add

Horticulture sector support and value-add is the primary strategy.

**Flagship moves:**

- Implement Horticulture sector support and value-add across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Horticulture sector support and value-add intervention (state variable: `sector_support_index`, sign: +) (relaxes: `sector_support_constraint`)


---

## Claims cited on this page

- **Horticultural production in Hawke's Bay (apples, kiwifruit, stone fruit, wine grapes) relies on approximately 3,000 seasonal workers via the Recognised Seasonal Employer (RSE) scheme, primarily from Pacific nations. RSE dependency creates labour market rigidity; post-harvest automation gaps and unfamiliarity with workplace rights expose workers to exploitation and wage undercutting.** [value: 3000 RSE workers (approximate); 2023] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* rse_worker_count, horticulture_wage_level_dollars_per_hour.

*Constraints:* accommodation_and_support_capacity, worker_rights_enforcement.

*Inputs:* domestic_labour_supply_shortage, rse_scheme_policy_uncertainty.


*Feedback loops:*

- `RSE scheme suppresses domestic wages; domestic workers cannot compete; exit to services; labour shortage deepens; RSE dependence increases.`


---

*Generated from `problem.hawkes_bay.economy.horticulture_rse` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
