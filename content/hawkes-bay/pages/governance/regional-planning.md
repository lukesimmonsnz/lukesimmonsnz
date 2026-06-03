---
title: "Regional planning and long-term strategic direction"
section: governance
subpage: regional-planning
order: 2
updated: 2026-04-26
summary: >
  Hawke's Bay lacks integrated long-term regional strategy. Individual council long-term plans are siloed. Climate adaptation, economic diversification, and population projections are not coordinated. Investment priorities conflict.
status: draft
generated_from: problem.hawkes_bay.governance.regional_planning
---

# Regional planning and long-term strategic direction

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Planning Fragmentation

Each council has separate long-term plans with different timeframes. Regional Council regional plans exist but lack enforcement mechanisms.


## Climate Adaptation

No integrated regional climate adaptation strategy exists. Individual councils are developing separate climate action plans at different paces.


---


## Drivers

The following structural drivers contribute to this problem.


### Limited council capacity and three-way fragmentation



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Consider regional council unification

Consider regional council unification is the primary strategy.

**Flagship moves:**

- Implement Consider regional council unification across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Consider regional council unification intervention (state variable: `council_merger_index`, sign: +) (relaxes: `council_merger_constraint`)


### Treaty partnership and co-governance implementation

Genuine partnership with Ngāti Kahungunu through decision-making power-sharing, resource transfers, and mana whenua recognition improves governance outcomes and addresses historical injustice.

**Flagship moves:**

- Establish Ngāti Kahungunu co-governance seats on all councils with genuine veto authority
- Transfer natural resource management decision-making to iwi-council partnerships
- Fund Ngāti Kahungunu to lead long-term planning and strategy

**Tensions:**

- Co-governance is contested politically and may face resistance from some ratepayers
- Power-sharing requires councils to accept decisions they might otherwise oppose

**Interventions on the system:**

- Establish joint decision-making committees for resource management and long-term planning with Ngāti Kahungunu veto authority (state variable: `iwi_decision_making_authority_index`, sign: +)
- Transfer resource management budgets to joint iwi-council control (state variable: `iwi_resource_allocation_dollars`, sign: +)


---

## Claims cited on this page

- **Governance structures in Hawkes Bay are fragmented across multiple councils and agencies, creating coordination challenges. Limited council capacity constrains strategic planning, infrastructure delivery, and climate adaptation; funding gaps prevent implementation of identified priorities.** *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* regional_strategy_alignment_percent, infrastructure_investment_coordination_index.

*Constraints:* strategic_planning_capacity, funding_integration_barriers.

*Inputs:* territorial_fragmentation, short_term_political_cycles.


*Feedback loops:*

- `Uncoordinated planning leads to infrastructure duplication and gaps; efficiency is lost; regional competitiveness declines.`


---

*Generated from `problem.hawkes_bay.governance.regional_planning` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
