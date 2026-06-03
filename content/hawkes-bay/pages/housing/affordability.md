---
title: "Housing affordability in Hawke's Bay"
section: housing
subpage: affordability
order: 1
updated: 2026-04-26
summary: >
  Hawke's Bay faces growing supply-demand imbalance and cost-income divergence. Median house prices have risen significantly relative to incomes, exacerbated by Cyclone Gabrielle damage, limited new supply, and investor demand. Agricultural workers and seasonal labourers particularly affected.
status: draft
generated_from: problem.hawkes_bay.housing.affordability
---

# Housing affordability in Hawke's Bay

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Median Multiple Rising

Hawke's Bay median multiple (price-to-income ratio) has risen to approximately 6.8 in 2024, indicating severely unaffordable housing by Demographia standards. Average house prices exceed $600k while median incomes are approximately $90k annual.


## Post-Cyclone Damage and Supply Crunch

Cyclone Gabrielle damaged or destroyed thousands of homes in February 2023. Repair and rebuild backlogs have compressed available rental and owned stock, pushing prices higher.


---


## Drivers

The following structural drivers contribute to this problem.


### Flood hazard and terrain limitations on developable land



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus

### Post-Cyclone Gabrielle housing scarcity and repair backlog



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus

### Restrictive residential zoning and development constraints



- **Category:** regulatory
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Managed medium-density development

Managed medium-density development is the primary strategy.

**Flagship moves:**

- Implement Managed medium-density development across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Managed medium-density development intervention (state variable: `managed_densification_index`, sign: +) (relaxes: `managed_densification_constraint`)


### Upzoning and intensification

Removing zoning restrictions and enabling medium-density development across Napier and Hastings urban areas is the primary lever to improve housing affordability.

**Flagship moves:**

- Implement NPS-UD density requirements across all territorial authorities
- Permit 6-storey residential buildings within 800m of Napier CBD and Hastings CBD
- Remove minimum car-parking requirements in city centres

**Tensions:**

- Intensification in flood-prone and post-cyclone-damaged land raises safety risks
- Infrastructure capacity (water, wastewater) is strained in rebuilt areas
- Heritage character areas create political resistance to blanket upzoning

**Interventions on the system:**

- Amend district plans to allow 3-6 storey residential development in urban zones (state variable: `residential_density_allowance`, sign: +)
- Fast-track resource consent for developments meeting design standards (state variable: `housing_consent_processing_time`, sign: -)


---

## Claims cited on this page

- **Housing affordability in Hawke's Bay has deteriorated; median house price-to-income ratio reached 6.8× in 2024 (up from 5.2× in 2019), entering severely-unaffordable territory (Demographia threshold > 6.0). Napier and Hastings see investor-driven demand; construction lags population growth; rental yields attract offshore capital, reducing owner-occupier access for young families and essential workers.** [value: 6.8 ratio (dimensionless); 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.
- **Cyclone Gabrielle (February 2023) damaged approximately 3,600 dwellings in Hawke's Bay, with Heretaunga Plains hit hardest (Napier, Hastings, surrounding rural areas). Damage severity ranged from minor slips to total loss; emergency housing shortages persisted 6-12 months post-event. Repair timeline stretches to 3-5 years, straining insurance, building contractor capacity, and displacement impacts on vulnerable families.** [value: 3600 dwellings; 2023] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* median_multiple_ratio, price_to_income_gap.

*Constraints:* topographic_and_flood_limitations, post_cyclone_repair_backlog.

*Inputs:* housing_supply_constraint, investor_demand_pressure.


*Feedback loops:*

- `Affordability decline reduces labour supply attraction; worker shortages raise business costs; investment in growth slows.`


---

*Generated from `problem.hawkes_bay.housing.affordability` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
