---
title: "Three waters renewal and investment"
section: infrastructure
subpage: three_waters
order: 2
updated: 2026-04-26
summary: >
  Ageing water, wastewater, and stormwater infrastructure requires significant investment across Hamilton and smaller TAs.
status: draft
generated_from: problem.waikato.infrastructure.three_waters
---

# Three waters renewal and investment

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Three waters renewal and investment

Ageing water, wastewater, and stormwater infrastructure requires significant investment across Hamilton and smaller TAs.


---


## Drivers

The following structural drivers contribute to this problem.


### Decades of deferred infrastructure maintenance



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus

### Growth-driven infrastructure demand



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Accelerated infrastructure renewal funding

Increased central and local government funding for infrastructure renewal prevents costly emergency replacement.

**Flagship moves:**

- Establish a Waikato Infrastructure Renewal Fund co-funded by central government
- Implement asset management standards across all Waikato TAs
- Prioritise three-waters renewal in Hamilton and smaller TAs with highest risk

**Tensions:**

- Renewal funding competes with new capital investment for growth
- Rate increases required to fund renewal face community resistance

**Interventions on the system:**

- Establish a Waikato Infrastructure Renewal Fund co-funded by central government (state variable: `infrastructure_condition_index`, sign: +)


### Infrastructure shared services and consolidation

Consolidating infrastructure planning and procurement across Waikato TAs reduces costs and builds capability.

**Flagship moves:**

- Establish Waikato waters shared services entity
- Develop regional procurement framework for infrastructure contracts
- Share asset management systems and GIS across all TAs

**Tensions:**

- Shared services require institutional change and may reduce local accountability
- Smaller councils risk losing infrastructure expertise in consolidation

**Interventions on the system:**

- Establish Waikato waters shared services entity (state variable: `infrastructure_condition_index`, sign: +)


---

## Claims cited on this page

- **Hamilton water supply and wastewater systems face significant renewal backlog. The Waikato River abstraction supplies approximately 170K residents; aging pipe network has high leakage of 17-22% non-revenue water. Wastewater treatment at Ruakura requires capacity expansion to serve Peacocke growth. Three Waters Reform (now Local Water Done Well) created transition costs; small TAs struggle with asset replacement funding.** *(confidence: medium)* — Waikato Regional Council Annual Plan 2024.

---

## Further reading


- **Waikato Regional Council Annual Plan 2024** (Waikato Regional Council), 2024 — <https://waikatoregion.govt.nz>


---

## Technical notes

*State variables:* infrastructure_condition_index.

*Constraints:* implementation_capacity.

*Inputs:* policy_intervention, resource_allocation.


*Feedback loops:*

- `Addressing three waters creates feedback on regional outcomes.`


---

*Generated from `problem.waikato.infrastructure.three_waters` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
