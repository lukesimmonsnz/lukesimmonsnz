---
title: "Alpine Ecosystem Biodiversity Stress"
section: environment
subpage: alpine_biodiversity
order: 3
updated: 2026-04-26
summary: >
  Canterbury's alpine and subalpine ecosystems (Mt. Cook, Craigieburn, Arthur's Pass regions) face climate-driven pressure from invasive species (possums, pigs, stoats), changing precipitation patterns, and conservation funding constraints. Endemic alpine species (kea, takin, endemic plants) show range contractions.

status: draft
generated_from: problem.canterbury.environment.alpine_biodiversity
---

# Alpine Ecosystem Biodiversity Stress

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## High-altitude climate transition under way

Alpine grassland is shifting toward low scrub and tussock as temperatures warm and moisture regimes change. Invasive predators (stoats, possums) expand range, outcompeting native species. Kea and takin populations are declining.


---


## Drivers

The following structural drivers contribute to this problem.


### Climate Warming & Alpine Vegetation Shift



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Invasive Species (Stoats, Possums) Range Expansion



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Alpine Conservation & Invasive Predator Control

Integrated pest control (stoats, possums) and alpine habitat restoration maintain endemic species populations in face of climate change.

**Flagship moves:**

- Key intervention for Alpine Conservation & Invasive Predator Control

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Integrated pest control (stoats, possums) and alpine habitat restoration maintain endemic species populations in face of climate change. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


---

## Claims cited on this page

- **Alpine glaciers in the Southern Alps (Tasman, Franz Josef, Fox) are retreating at an accelerated pace, with elevation contraction reaching approximately 50 metres per decade. Tasman Glacier, visible from Lake Pukaki, has receded >3 km since the 1970s. This contraction threatens alpine water storage, hydroelectric generation (Manapouri, Waitaki scheme, Pukaki), and the ecological viability of braided river systems dependent on glacial melt runoff (Rakaia, Rangitata, Waitaki).** [value: 50 meters elevation per decade; 2023] *(confidence: medium)* — GNS Science Alpine Fault Hazard Assessment 2022.
- **Invasive predator populations (stoats, rats, possums) in Canterbury's braided river and alpine ecosystems have expanded, with stoat densities in some braided river zones reaching 2 per hectare. This expansion threatens critically endangered species endemic to Canterbury braided rivers: black stilts (kakī, ~150 remaining globally, 80% in Canterbury braided rivers), plovers, and oystercatchers. Predator control efforts by DOC and community groups remain insufficient to reverse population trends.** [value: 2 stoats per hectare; 2023] *(confidence: medium)* — State of the Environment Report—Freshwater and Land 2023.

---

## Further reading


- **GNS Science Alpine Fault Hazard Assessment 2022** (GNS Science), 2022 — <https://www.gns.cri.nz/>

- **State of the Environment Report—Freshwater and Land 2023** (Environment Canterbury), 2023 — <https://www.ecan.govt.nz/about-us/planning/state-of-the-environment/>


---

## Technical notes

*State variables:* endemic_species_distribution_area, invasive_predator_density, alpine_vegetation_composition_change.

*Constraints:* conservation_area_size_limitation, DOC_budget_constraints.

*Inputs:* temperature_increase_rate, precipitation_pattern_shift, conservation_funding_per_hectare.


*Feedback loops:*

- `Dynamic feedback mechanisms drive alpine ecosystem biodiversity stress.`


---

*Generated from `problem.canterbury.environment.alpine_biodiversity` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
