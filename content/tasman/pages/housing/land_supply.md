---
title: "Zoned land that is hard to actually build on"
section: housing
subpage: land_supply
order: 2
updated: 2026-04-26
summary: >
  Tasman has roughly 1,850 hectares of residentially zoned land in the Richmond-Motueka belt — a notional 100-year supply at current absorption — but high land prices, heritage overlays, and stormwater capacity limits mean most of it does not become consented dwellings in any given year.
status: draft
generated_from: problem.tasman.housing.land_supply
---

# Zoned land that is hard to actually build on

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Zoned does not mean buildable

Land prices in Richmond's central residential zones run NZD 1.2 to 1.8 million per hectare, which deters greenfield subdivision. Infill is constrained by heritage overlays in older parts of Richmond and by stormwater capacity limits in low-lying Waimea Inlet catchments (claim.tasman.housing.land_supply_claim).


## Absorption is the rate-limiting step

Annual absorption sits at roughly 18 hectares — around 1 percent of the zoned inventory. Because the binding constraints are infrastructure-capacity, land-banking, and consenting throughput rather than zoning, simply rezoning more rural land does not move the dwelling completion rate.


---


## Drivers

The following structural drivers contribute to this problem.


### Lifestyle-migration demand from metropolitan equity



- **Category:** demographic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing housing challenges.

**Flagship moves:**

- Implement evidence-based housing policy in Tasman
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

- **Residential zoned land inventory in Richmond/Motueka stands at 1,850 hectares; current absorption rate is 18 hectares/year, yielding 103-year supply. However, land prices (NZD 1.2–1.8 million/hectare in Richmond CBD zones) and development costs deter greenfield construction; infill development is constrained by heritage overlays and stormwater capacity.** [value: 1850 hectares residential zoned land; 2024] — Tasman Housing Demand and Lifestyle Migration 2024; Tasman District Council Annual Plan 2024.

---

## Further reading


- **Tasman Housing Demand and Lifestyle Migration 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* hectares_residential_zoned, annual_dwellings_consented.

*Constraints:* heritage_overlays, stormwater_capacity_limits.

*Inputs:* three_waters_capacity_upgrade, consenting_throughput.


*Feedback loops:*

- `Slow absorption keeps land prices high, which keeps absorption slow.`


---

*Generated from `problem.tasman.housing.land_supply` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
