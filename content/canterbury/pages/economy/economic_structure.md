---
title: "Canterbury Economic Diversification & Resilience"
section: economy
subpage: economic_structure
order: 1
updated: 2026-04-26
summary: >
  Canterbury's economy remains heavily dependent on primary production (dairy, arable) and construction (post-earthquake rebuild). High-value-added sectors (tech, professional services, biotech) are emerging but remain small. Earthquake rebuild stimulus is waning; labor productivity growth is slower than national average. Regional economic resilience to commodity price shocks and climate stress is questionable.

status: draft
generated_from: problem.canterbury.economy.economic_structure
---

# Canterbury Economic Diversification & Resilience

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Rebuild boost fading

Post-2011, earthquake rebuild spending ($40B over 15 years) sustained construction employment and related sectors. That stimulus is ending (2024). Canterbury must transition to organic growth; tech/innovation sectors are nascent (Lincoln, UC, EPIC Innovation Precinct).


---


## Drivers

The following structural drivers contribute to this problem.


### Post-Earthquake Rebuild Stimulus Fading (2024+)



- **Category:** economic
- **Timescale:** short
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Economic Diversification Strategy

Diversifying Canterbury economy beyond primary sector and construction toward tech, services, and value-added sectors improves resilience.

**Flagship moves:**

- Support tech sector growth through EPIC Precinct and capital attraction

**Tensions:**

- Transition managing impacts on current primary sector workforce

**Interventions on the system:**

- Sector diversification (state variable: `gvp_composition`, sign: +) (relaxes: `primary_sector_concentration`)


---

## Claims cited on this page

- **Economic vulnerabilities in Canterbury include sector concentration, commodity price exposure, and limited business diversification. Labor market challenges, business investment constraints, and workforce skill mismatches limit employment growth and income stability for residents.** [value: 18 percent primary; 2023] *(confidence: medium)* — Treasury Economic and Financial Overview 2024.
- **Economic vulnerabilities in Canterbury include sector concentration, commodity price exposure, and limited business diversification. Labor market challenges, business investment constraints, and workforce skill mismatches limit employment growth and income stability for residents.** [value: 18 percent agriculture; 2023] — Aotearoa New Zealand 2023 Census Place Summary — Canterbury Region.

---

## Further reading


- **Treasury Economic and Financial Overview 2024** (Treasury), 2024 — <https://www.treasury.govt.nz/>

- **Aotearoa New Zealand 2023 Census Place Summary — Canterbury Region** — Statistics New Zealand Tatauranga Aotearoa (Stats NZ), 2024 — <https://www.stats.govt.nz/tools/2023-census-place-summaries/canterbury-region>


---

## Technical notes

*State variables:* gvp_composition_by_sector, employment_concentration_by_sector, labor_productivity_growth_rate, business_startup_rate.

*Constraints:* labor_force_size, capital_investment_rate, infrastructure_capacity.

*Inputs:* primary_sector_commodity_prices, construction_demand_rebuild, technological_innovation_adoption.


*Feedback loops:*

- `Primary sector risk: commodity price downturns (dairy) reduce household income and investment, dampening broader economy.`


---

*Generated from `problem.canterbury.economy.economic_structure` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
