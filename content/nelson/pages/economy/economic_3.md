---
title: "Horticulture under input-cost and water pressure"
section: economy
subpage: economic_3
order: 3
updated: 2026-04-26
summary: >
  Nelson-Tasman horticulture (apples, kiwifruit, pipfruit, hops) generates around $280-320 million in annual revenue across roughly 8,900 hectares and supports more than 2,100 FTE in primary production. Rising input costs (labour, water, pest management), water-availability constraints, and seasonal-labour shortages have left grower incomes flat or declining in real terms since 2019.
status: draft
generated_from: problem.nelson.economy.economic_3
---

# Horticulture under input-cost and water pressure

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Anchor crops and structural margin compression

The Tasman district and Nelson rural fringe host one of New Zealand's densest fruit-growing regions, anchored by apples (particularly the Heretaunga / Motueka growing belt) and supported by hops, kiwifruit, and emerging crops (claim.nelson.economy.economic_3_claim). Margin compression is real: input costs have outpaced farmgate prices for several seasons.


## Labour and water as the binding constraints

Seasonal labour comes mainly through Recognised Seasonal Employer (RSE) workers and working-holiday visa holders, with grower-supplied accommodation an increasingly binding bottleneck. Water reliability through the Waimea Community Dam improves the irrigation outlook but does not remove the longer-run climate risk to yields and pest pressure.


---


## Drivers

The following structural drivers contribute to this problem.


### Constrained skilled labour and absence of research-university anchor



- **Category:** demographic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing economy challenges.

**Flagship moves:**

- Implement evidence-based economy policy in Nelson
- Increase investment in economy services and infrastructure
- Build cross-sector partnerships to address economy challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for economy (state variable: `economy_outcome_index`, sign: +)
- Secondary intervention for economy (state variable: `economy_service_access`, sign: +)


---

## Claims cited on this page

- **Nelson-Tasman horticulture sector generates $280–320 million in annual revenue from apples, kiwifruit, and pipfruit production on approximately 8,900 hectares. Employment in primary production (horticulture, viticulture, aquaculture) is 2,100+ FTE. Rising input costs (labour, water, pest management due to climate stress), water availability constraints, and labour shortages limit expansion; grower incomes have been flat or declining 2019-2024 in real terms.** [value: 300 million NZD annual revenue (horticulture); 2023] *(confidence: medium)* — Nelson Tasman Water Strategy 2023.

---

## Further reading


- **Nelson Tasman Water Strategy 2023** — Nelson City Council / Tasman District Council (Nelson City Council), 2023 — <https://www.nelsoncitycouncil.co.nz>


---

## Technical notes

*State variables:* horticulture_revenue_nzd_m, hectares_in_production, rse_seasonal_workers.

*Constraints:* seasonal_accommodation_capacity, frost_and_heat_events.

*Inputs:* water_allocation, labour_visa_settings, international_fruit_price.


*Feedback loops:*

- `Input-cost-accommodation feedback: rising input costs push growers to accept tighter margins; thin margins discourage capital investment in worker accommodation, deepening the labour bottleneck.`


---

*Generated from `problem.nelson.economy.economic_3` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
