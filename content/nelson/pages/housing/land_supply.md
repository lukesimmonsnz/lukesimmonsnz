---
title: "Constrained buildable land in the Nelson basin"
section: housing
subpage: land_supply
order: 2
updated: 2026-04-26
summary: >
  Approximately 800 hectares of zoned residential and mixed-use land are available for development over 15 years (medium-growth scenario), but around 220 hectares are encumbered by heritage overlays, flood-risk zones, or cultural-heritage sites that limit developability. Take-up runs at 45-55 hectares per year; at that rate, competitive supply pressure intensifies from 2026 onward.
status: draft
generated_from: problem.nelson.housing.land_supply
---

# Constrained buildable land in the Nelson basin

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Geography and overlays compound

The Nelson basin is small, hill-bounded, and overlain by fault lines and coastal hazard zones (claim.nelson.housing.land_supply_claim). On top of those physical constraints sit heritage-character overlays that further reduce feasible intensification.


## Cross-boundary supply not in scope

Tasman District has marginally more available residential land but weaker demand. Coordination across the two unitary councils on a joint growth programme is improving but not yet at the level of pooled supply or shared intensification mandates.


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic constraint on buildable land in the Nelson basin



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing housing challenges.

**Flagship moves:**

- Implement evidence-based housing policy in Nelson
- Increase investment in housing services and infrastructure
- Build cross-sector partnerships to address housing challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for housing (state variable: `housing_outcome_index`, sign: +)
- Secondary intervention for housing (state variable: `housing_service_access`, sign: +)


---

## Claims cited on this page

- **Buildable land supply in Nelson is constrained by natural and planning boundaries. Approximately 800 hectares of zoned residential and mixed-use land are available for development over 15 years (medium growth scenario); however, ~220 hectares are encumbered by heritage overlays, flood risk zones, or cultural heritage sites that limit developability. Current take-up is 45–55 hectares/year; at this rate, competitive supply pressure will intensify 2026 onward. Tasman District has marginally more supply (950 hectares) but weaker demand; coordination is weak.** [value: 800 hectares available residential land over 15 years; 2024-2039] *(confidence: medium)* — Nelson Housing Demand and Development Report 2024.

---

## Further reading


- **Nelson Housing Demand and Development Report 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>


---

## Technical notes

*State variables:* zoned_residential_hectares, annual_take_up_hectares, feasible_intensification_capacity.

*Constraints:* fault_lines, elite_soils, heritage_overlays.

*Inputs:* plan_change_throughput, infrastructure_co_funding.


*Feedback loops:*

- `Constraint-overlay feedback: each successive overlay (heritage, hazard, character) defends a specific value but compounds with the others to shrink the practical feasible-supply envelope below what aggregate demand requires.`


---

*Generated from `problem.nelson.housing.land_supply` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
