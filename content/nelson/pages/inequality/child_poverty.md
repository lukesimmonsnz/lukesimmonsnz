---
title: "Child poverty above national average"
section: inequality
subpage: child_poverty
order: 2
updated: 2026-04-26
summary: >
  Around 18.2 percent of Nelson children live in after-housing-cost poverty (against 14.8 percent nationally); in Tasman the rate is around 16.4 percent. Concentrations are highest in the Tahunanui Cob, Stoke, and Tatanui suburbs. Food insecurity affects 12-14 percent of low-income households with children, and school-based nutrition programmes operate in 7 of 12 primary schools, with demand exceeding capacity.
status: draft
generated_from: problem.nelson.inequality.child_poverty
---

# Child poverty above national average

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Housing-cost-driven child poverty

Most of the gap between Nelson and national child-poverty rates sits in the after-housing-cost measure, indicating that local housing cost is the dominant proximate driver (claim.nelson.inequality.child_poverty_claim). Pre-housing-cost incomes for affected households are not far from national equivalents.


## Health and education spillover

Dental caries, rheumatic fever, and school-readiness indicators all correlate with deprivation quintile. The cost of intervening late (specialist treatment, alternative education, family support) is far higher than addressing the housing-cost driver upstream, but the institutional owners of those costs differ.


---


## Drivers

The following structural drivers contribute to this problem.


### Housing-wealth amplification of income inequality



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing inequality challenges.

**Flagship moves:**

- Implement evidence-based inequality policy in Nelson
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

- **Child poverty rates in Nelson are above national average. Using the after-housing-costs measure, 18.2% of Nelson children live in poverty (vs. 14.8% nationally); in Tasman district, the rate is 16.4%. Absolute deprivation is highest in the Tasman Cob, Stoke, and Tatanui suburbs; food insecurity affects 12–14% of low-income households with children. School-based nutrition programmes (breakfast clubs, lunch provision) operate in 7 of 12 primary schools; demand exceeds capacity. Child health indicators (dental caries, rheumatic fever) correlate closely with deprivation quintile.** [value: 18.2 percent of children in after-housing-costs poverty; 2023] *(confidence: medium)* — Income and Inequality in Nelson Census 2023.

---

## Further reading


- **Income and Inequality in Nelson Census 2023** — Stats NZ (Statistics New Zealand), 2023 — <https://www.stats.nz>


---

## Technical notes

*State variables:* ahc_child_poverty_pct, food_insecurity_pct_low_income, school_lunch_programme_coverage.

*Constraints:* housing_cost_floor, ngo_capacity.

*Inputs:* wff_settings, accommodation_supplement, school_nutrition_funding.


*Feedback loops:*

- `Housing-cost-deprivation feedback: rising housing cost pushes more children below the after-housing-cost threshold, increasing demand for school nutrition and family support, which compete for the same constrained NGO capacity.`


---

*Generated from `problem.nelson.inequality.child_poverty` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
