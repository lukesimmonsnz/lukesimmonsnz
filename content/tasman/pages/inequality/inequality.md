---
title: "Lifestyle-migration-driven income polarisation"
section: inequality
subpage: inequality
order: 1
updated: 2026-04-26
summary: >
  The Gini coefficient for Tasman sits at around 0.38, above the national 0.35. The top 20 percent of earners command around 38 percent of total income; the bottom 20 percent earn around 8 percent. Lifestyle migration has widened the gap by introducing high-equity newcomers without proportionally lifting local wages.
status: draft
generated_from: problem.tasman.inequality.inequality
---

# Lifestyle-migration-driven income polarisation

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Above-national inequality, below-national wages

Tasman is not a wealthy region in median terms, but its income distribution is more stretched than New Zealand as a whole. The combination of horticultural and hospitality wage compression at the bottom and lifestyle-migrant capital at the top produces the observed Gini (claim.tasman.inequality.inequality_claim).


## Capital, not wages, drives the top

Newcomers from Auckland and Wellington are typically arriving with metropolitan housing equity, retirement assets, or consultancy income that travels with them. Their earned income reads like the top decile of Tasman; their wealth reads considerably higher again.


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic concentration of disadvantage



- **Category:** demographic
- **Timescale:** long
- **Consensus:** consensus

### Wage compression at the bottom, capital inflow at the top



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing inequality challenges.

**Flagship moves:**

- Implement evidence-based inequality policy in Tasman
- Increase investment in inequality services and infrastructure
- Build cross-sector partnerships to address inequality challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for inequality (state variable: `inequality_outcome_index`, sign: +)
- Secondary intervention for inequality (state variable: `inequality_service_access`, sign: +)


### Response: Camp 2

A response strategy addressing inequality challenges.

**Flagship moves:**

- Implement evidence-based inequality policy in Tasman
- Increase investment in inequality services and infrastructure
- Build cross-sector partnerships to address inequality challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for inequality (state variable: `inequality_outcome_index`, sign: +)
- Secondary intervention for inequality (state variable: `inequality_service_access`, sign: +)


---

## Claims cited on this page

- **Census income distribution (2023) shows Gini coefficient for Tasman at 0.38, above national average of 0.35. Top 20% of earners command 38% of total income; bottom 20% earn 8%. Lifestyle migration influx has widened the income gap; newcomers from Auckland/Wellington bring capital while displacing lower-income locals.** [value: 0.38 Gini coefficient; 2023] — Income and Inequality in Tasman Census 2023; Tasman Housing Demand and Lifestyle Migration 2024.

---

## Further reading


- **Income and Inequality in Tasman Census 2023** — Stats NZ (Statistics New Zealand), 2023 — <https://www.stats.nz>

- **Tasman Housing Demand and Lifestyle Migration 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>


---

## Technical notes

*State variables:* regional_gini_coefficient, p90_p10_income_ratio.

*Constraints:* primary_sector_wage_floor, national_tax_settings.

*Inputs:* lifestyle_migration_inflow, regional_wage_growth.


*Feedback loops:*

- `Higher inequality raises housing-cost dispersion, which forces lower-wage workers further from employment centres, which raises their effective costs further.`


---

*Generated from `problem.tasman.inequality.inequality` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
