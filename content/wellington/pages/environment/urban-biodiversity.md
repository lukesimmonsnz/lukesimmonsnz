---
title: "Urban biodiversity pressures in Wellington"
section: environment
subpage: urban-biodiversity
order: 2
updated: 2026-04-26
summary: >
  Wellington hosts nationally significant urban biodiversity including the Zealandia/Karori wildlife sanctuary, but urban expansion, predator pressure, and habitat fragmentation continue to threaten indigenous species and ecosystem connectivity across the wider city. The success of Zealandia demonstrates what is achievable but also highlights how much of the urban landscape remains hostile to native biodiversity.
status: draft
generated_from: problem.wellington.environment.urban_biodiversity
---

# Urban biodiversity pressures in Wellington

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Zealandia success and its limits

Zealandia has demonstrated that a fenced urban sanctuary can support breeding populations of kākā, kiwi, and tuatara in a city environment. Kākā now range freely across much of suburban Wellington. However, this success is confined to areas near the sanctuary perimeter; the broader urban matrix remains heavily predator-affected (claim.wellington.environment.pest_free_progress).


## Canopy and urban greening gaps

Wellington's urban tree canopy coverage varies significantly across neighbourhoods, with lower-income and higher-density areas having less canopy than affluent hillside suburbs. Loss of urban canopy through infill development is occurring faster than replacement planting in some zones (claim.wellington.environment.urban_tree_canopy_cover).


---


## Drivers

The following structural drivers contribute to this problem.


### Infill development canopy removal



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** mostly-agreed

### Urban predator pressure on native species



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Urban Predator-Free Wellington Expansion

Extending Predator Free Wellington to all urban suburbs will enable native biodiversity recovery across the city.

**Flagship moves:**

- Achieve predator-free status in all Wellington City suburbs by 2030
- Mandatory trap networks in new subdivisions as consent condition
- Community volunteer network expansion with app-based monitoring

**Tensions:**

- Urban predator control requires sustained community engagement; volunteer fatigue is a real risk
- Free-ranging cats are politically contested as predators

**Interventions on the system:**

- Expand Predator Free Wellington programme to cover all remaining suburban gaps with funded trap networks (state variable: `urban_predator_pressure`, sign: -)


### Urban Tree Canopy and Greening Policy

Mandating minimum canopy cover in intensification zones will offset biodiversity loss from infill development.

**Flagship moves:**

- 30% minimum canopy cover requirement in all residential zones
- Street tree replacement at 3:1 ratio for any removal
- Green roof and wall incentives for new commercial builds

**Tensions:**

- Canopy requirements may conflict with intensification goals in constrained sections
- Street tree roots interact poorly with aging water and wastewater pipes

**Interventions on the system:**

- Introduce Urban Tree Canopy Policy requiring 30% canopy coverage in all Wellington City residential zones by 2035 (state variable: `urban_canopy_cover_pct`, sign: +)


---

## Claims cited on this page

- **Zealandia/Karori Wildlife Sanctuary has established a predator-free urban zone supporting breeding populations of kākā, kiwi, tuatara, and kākāriki, with kākā now ranging freely across much of suburban Wellington — demonstrating the viability of urban predator eradication at small-to-medium scale.** — Greater Wellington State of the Environment Report 2022; Wellington City Council Climate Change Action Plan 2023.
- **Wellington's urban tree canopy coverage varies significantly across neighbourhoods, with lower-income and higher-density inner suburbs having lower canopy cover than affluent hillside suburbs, and infill development removing canopy at a faster rate than replacement planting in some zones.** *(confidence: medium)* — Wellington City Council Climate Change Action Plan 2023.

---

## Further reading


- **Greater Wellington State of the Environment Report 2022** (Greater Wellington Regional Council), 2022 — <https://www.gw.govt.nz/environment/state-of-the-environment/>

- **Wellington City Council Climate Change Action Plan 2023** (Wellington City Council), 2023 — <https://www.wellington.govt.nz/environment-and-sustainability/climate-change>


---

## Technical notes

*State variables:* urban_tree_canopy_pct, predator_tracking_tunnel_density.

*Constraints:* cat_and_rodent_pressure_in_urban_matrix, habitat_patch_isolation.

*Inputs:* pest_control_investment, urban_greening_policy.


*Feedback loops:*

- `Predator rebound loop: cessation of community predator control in any neighbourhood allows rat and possum populations to rebound within months, reversing gains.`


---

*Generated from `problem.wellington.environment.urban_biodiversity` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
