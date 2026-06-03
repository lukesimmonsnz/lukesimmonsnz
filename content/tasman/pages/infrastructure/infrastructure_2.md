---
title: "Waimea water-supply efficiency and metering gaps"
section: infrastructure
subpage: infrastructure_2
order: 2
updated: 2026-04-26
summary: >
  The Waimea reticulated water supply draws around 18,500 cubic metres per day from the Waimea Aquifer, with documented network leakage near 25 percent and around 1,850 connections still unmetered. Estimated capital required for distribution-main upgrades, smart metering, and demand-management retrofits is around NZD 42 million.
status: draft
generated_from: problem.tasman.infrastructure.infrastructure_2
---

# Waimea water-supply efficiency and metering gaps

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Leakage at one in four litres

Roughly 25 percent of treated water put into the Waimea network does not reach a metered customer (claim.tasman.infrastructure.infrastructure_2_claim). At a time of aquifer stress, that physical loss is also a water-allocation loss — the abstracted water counts against the same sustainable-yield envelope as horticultural use.


## Demand management starts at the meter

1,850 unmetered connections cannot be priced or load-shifted; behavioural demand-management tools assume a meter. Metering retrofits are therefore a prerequisite for credible drought response, not just a billing-fairness measure.


---


## Drivers

The following structural drivers contribute to this problem.


### Renewal backlog inherited from a small ratepayer base



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing infrastructure challenges.

**Flagship moves:**

- Implement evidence-based infrastructure policy in Tasman
- Increase investment in infrastructure services and infrastructure
- Build cross-sector partnerships to address infrastructure challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for infrastructure (state variable: `infrastructure_outcome_index`, sign: +)
- Secondary intervention for infrastructure (state variable: `infrastructure_service_access`, sign: +)


---

## Claims cited on this page

- **Waimea water supply system draws 18,500 cubic meters/day from Waimea Aquifer; Waimea Aquifer Study (2023) recommends urgent upgrade of distribution mains (25% leakage), installation of smart metering (1,850 connections unmetered), and demand-management retrofits to horticultural users. Capital investment estimated NZD 42 million.** [value: 25 percent water leakage; 2023] — Waimea Aquifer Stress Study 2023; Tasman District Council Annual Plan 2024.

---

## Further reading


- **Waimea Aquifer Stress Study 2023** — Tasman District Council / Greater Wellington Regional Council (Tasman District Council), 2023 — <https://www.tasman.govt.nz>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* network_leakage_rate, share_connections_metered.

*Constraints:* aquifer_sustainable_yield, rates_funded_capex_ceiling.

*Inputs:* waimea_distribution_capex, demand_management_programme.


*Feedback loops:*

- `Unmetered connections weaken demand response in dry seasons, which forces reliance on supply-side abstraction increases that further stress the aquifer.`


---

*Generated from `problem.tasman.infrastructure.infrastructure_2` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
