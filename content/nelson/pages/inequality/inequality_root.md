---
title: "Widening income and wealth inequality in Nelson-Tasman"
section: inequality
subpage: inequality_root
order: 1
updated: 2026-04-26
summary: >
  Nelson-Tasman's income Gini coefficient is around 0.38 (against 0.35 nationally). The top 10 percent earn around 8.2x median household income; the bottom 10 percent earn about 2.1x (a 3.9x ratio). Median household income is around $62,400 against a mean of $78,300, indicating right-skew driven by professional and tourism-sector high earners. Lifestyle in-migration has amplified the property-wealth dimension of inequality.
status: draft
generated_from: problem.nelson.inequality.inequality_root
---

# Widening income and wealth inequality in Nelson-Tasman

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Income, wealth, and lifestyle migration

Nelson's measured income inequality is moderately above national; the larger story is the wealth gap between established homeowners (now often mortgage-free) and first-home and renter households (claim.nelson.inequality.inequality_root_claim). Lifestyle in-migration imported substantial existing wealth into the Nelson property market between 2018 and 2022.


## Geographic concentration

Inequality has a clear geographic shape: deprivation is concentrated in particular suburbs (Tahunanui's eastern edge, parts of Stoke and Tatanui) and in rural pockets, while wealth concentrates in the central-city heritage fringe and the coastal lifestyle belt.


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic isolation of rural communities from specialist services



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus

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


### Response: Camp 2

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

- **Income inequality in Nelson-Tasman is widening. The Gini coefficient is 0.38 (vs. 0.35 nationally); income ratios show the top 10% earn 8.2× median household income while the bottom 10% earn 2.1× (ratio 3.9×). Median household income is $62,400, but mean is $78,300, indicating right-skew driven by high earners in professional and tourism sectors. Median personal income shows larger gaps: top decile $78,000 vs. bottom decile $18,500 (4.2× ratio). Lifestyle migrants with high incomes have amplified inequality in property, professional services, and business ownership sectors.** [value: 0.38 Gini coefficient; 2023] *(confidence: medium)* — Income and Inequality in Nelson Census 2023.

---

## Further reading


- **Income and Inequality in Nelson Census 2023** — Stats NZ (Statistics New Zealand), 2023 — <https://www.stats.nz>


---

## Technical notes

*State variables:* household_income_gini, p90_p10_household_income_ratio, mortgage_free_owner_share.

*Constraints:* wage_structure, labour_market_thinness.

*Inputs:* national_tax_transfer_settings, house_price_growth.


*Feedback loops:*

- `Wealth-rent feedback: rising property wealth pulls rents up, raising cost-of-living for non-owners, which reduces saving capacity and entrenches the ownership gap.`


---

*Generated from `problem.nelson.inequality.inequality_root` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
