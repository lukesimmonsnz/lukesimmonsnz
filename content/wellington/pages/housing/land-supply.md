---
title: "Constrained residential land supply in Wellington"
section: housing
subpage: land-supply
order: 4
updated: 2026-04-26
summary: >
  Wellington's usable residential land supply is severely restricted by topography, fault-zone setbacks, and planning rules. The combination produces a developable land premium that persists even after NPS-UD upzoning, and which fundamentally limits the supply response to demand.
status: draft
generated_from: problem.wellington.housing.land_supply
---

# Constrained residential land supply in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Topographic constraint

Unlike flat cities, Wellington's developable land is bounded by harbour, hills, and active fault zones. Roughly 60% of Wellington City's land area has slopes exceeding 15 degrees, limiting cost-effective residential construction (claim.wellington.housing.greenfield_constraint_topography).


## Zoned capacity shortfall

The NPS-UD upzoning partially addressed planning constraints in Wellington City, but the practical development pipeline remains limited by infrastructure servicing costs and geotechnical complexity. Modelled zoned capacity overstates deliverable supply when infrastructure investment lags (claim.wellington.housing.zoned_capacity_deficit).


---


## Drivers

The following structural drivers contribute to this problem.


### Earthquake-prone building stock



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus

### Fault zone land-use setback rules



- **Category:** regulatory
- **Timescale:** permanent
- **Consensus:** consensus

### Infrastructure servicing capacity gap



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** mostly-agreed

### Restrictive residential zoning



- **Category:** regulatory
- **Timescale:** long
- **Consensus:** consensus

### Topographic land supply constraint



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Managed Densification with Infrastructure Sequencing

Density increases must be sequenced with infrastructure investment; unmanaged intensification exacerbates flooding, wastewater, and transport stress.

**Flagship moves:**

- Infrastructure-led precinct planning before rezoning approvals
- Developer-funded infrastructure bonds tied to consent capacity
- Strategic growth nodes at Tawa, Porirua, and Hutt Valley rail corridors

**Tensions:**

- Slower rollout delays affordability relief for current renters
- Cost of infrastructure bonds may be passed to purchasers, limiting affordability gains

**Interventions on the system:**

- Require infrastructure capacity certificates before residential rezoning takes effect (state variable: `infrastructure_capacity`, sign: +)


### Upzoning and Intensification

Removing zoning restrictions and enabling medium-density development across Wellington's urban areas is the primary lever to improve affordability.

**Flagship moves:**

- Implement NPS-UD density requirements across all Wellington territorial authorities
- Permit six-storey residential buildings within 800m of rapid transit stops
- Remove minimum car-parking requirements citywide

**Tensions:**

- Intensification in fault-zone and liquefaction-prone land raises safety risks
- Infrastructure capacity (water, wastewater) constrains achievable density in many suburbs
- Heritage character areas create political resistance to blanket upzoning

**Interventions on the system:**

- Rezone residential land within 1km of Wellington CBD and Johnsonville/Porirua centres to allow 6-storey mixed-use (state variable: `zoned_capacity`, sign: +) (relaxes: `height_limit`)
- Mandate development contributions schedule that front-funds infrastructure upgrades for upzoned areas (state variable: `infrastructure_capacity`, sign: +)


---

## Claims cited on this page

- **Wellington City Council identified that 60% of city land area has slopes exceeding 15 degrees, severely constraining greenfield housing expansion. Steep topography forces densification on flat central and eastern suburbs, increasing reliance on infill housing and intensification around transport corridors to meet affordability pressures.** [value: 60 percent of land area with slope >15 degrees; 2022] *(confidence: medium)* — Wellington Housing Market: Constraints, Costs and Consequences; Wellington City Housing and Business Development Capacity Assessment 2022.
- **Wellington City's modelled zoned residential capacity under the NPS-UD upzoning overstates practically deliverable housing supply because a significant share of zoned capacity sits on sites constrained by earthquake-prone building obligations, geotechnical complexity, or inadequate infrastructure reticulation.** *(confidence: medium)* — Wellington City Housing and Business Development Capacity Assessment 2022; Wellington Housing Market: Constraints, Costs and Consequences.

---

## Further reading


- **Wellington Housing Market: Constraints, Costs and Consequences** — Greenaway-McGrevy R, Pacheco G (Motu Economic and Public Policy Research), 2022 — <https://www.motu.nz/our-work/urban-and-regional/housing/>

- **Wellington City Housing and Business Development Capacity Assessment 2022** (Wellington City Council), 2022 — <https://www.wellington.govt.nz/planning-and-environment/urban-growth-and-housing>


---

## Technical notes

*State variables:* zoned_developable_capacity, land_price_per_sqm.

*Constraints:* fault_zone_setback_rules, steep_slope_buildability_limit, infrastructure_servicing_capacity.

*Inputs:* upzoning_policy_change, infrastructure_investment.


*Feedback loops:*

- `Land scarcity premium: constrained supply raises land prices, increasing development viability thresholds and excluding mid-market projects.`


---

*Generated from `problem.wellington.housing.land_supply` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
