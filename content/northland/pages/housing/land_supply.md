---
title: "Te Tai Tokerau Northland: constrained residential land supply"
section: housing
subpage: land_supply
order: 3
updated: 2026-04-26
summary: >
  Usable residential land supply is restricted by physical constraints, zoning rules, and infrastructure capacity.
status: draft
generated_from: problem.northland.housing.land_supply
---

# Te Tai Tokerau Northland: constrained residential land supply

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Physical constraint

Northland's geography limits readily developable land, with terrain and infrastructure constraints restricting cost-effective residential construction.


## Zoned capacity shortfall

Planning rules constrain residential development across much of the region, with infrastructure servicing costs and environmental standards limiting practical supply.


---


## Drivers

The following structural drivers contribute to this problem.


### Restrictive residential zoning and planning rules



- **Category:** regulatory
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Supply acceleration and upzoning

Removing zoning restrictions and enabling medium-density development is the primary lever to improve affordability.

**Flagship moves:**

- Rezone residential land to enable 6-storey mixed-use development
- Implement development contributions for infrastructure upgrades
- Remove minimum car-parking requirements citywide

**Tensions:**

- Infrastructure capacity constrains achievable density in many suburbs
- Heritage character areas create political resistance to upzoning
- Environmental and safety considerations in sensitive locations

**Interventions on the system:**

- Rezone residential land within key centres to allow 6-storey mixed-use (state variable: `zoned_capacity`, sign: +) (relaxes: `height_limit`)
- Implement development contributions schedule to front-fund infrastructure (state variable: `infrastructure_capacity`, sign: +)


---

## Claims cited on this page

- **Residential land supply is constrained in Whangārei and surrounding suburbs; developable land either unaffordable or tied up in speculative holdings. Far North (Kaitāia, Kerikeri, Bay of Islands) has land supply but limited development due to financing barriers and small local market demand. Growth in Whangārei CBD requires infill; greenfield options limited by council planning restrictions.** *(confidence: medium)* — Government Housing Market Data 2023.
- **Housing density in Whangārei remains low relative to population growth; sprawl outward creates** *(confidence: medium)* — Government Housing Market Data 2023.

---

## Further reading


- **Government Housing Market Data 2023** — Ministry of Housing and Urban Development (MHUD), 2023 — <https://www.hud.govt.nz/urban-development/housing-assessments/>


---

## Technical notes

*State variables:* zoned_developable_capacity, land_price_per_sqm.

*Constraints:* geographical_constraints, infrastructure_servicing_capacity.

*Inputs:* upzoning_policy_change, infrastructure_investment.


*Feedback loops:*

- `Land scarcity premium: constrained supply raises land prices, increasing development viability thresholds.`


---

*Generated from `problem.northland.housing.land_supply` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
