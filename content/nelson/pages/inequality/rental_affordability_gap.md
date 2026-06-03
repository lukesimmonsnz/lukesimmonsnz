---
title: "Rental affordability gap between income quintiles"
section: inequality
subpage: rental_affordability_gap
order: 3
updated: 2026-04-26
summary: >
  In Nelson, lowest-income households (Q1, median around $22,800) pay 38-52 percent of income on rent; Q2 households (median around $35,200) pay 28-36 percent; Q3+ households (median above $55,000) pay 18-22 percent. Median rent of around $510 per week is unaffordable at market rates for households earning under $30,000 without housing assistance. Community and state housing covers about 8 percent of rental demand; waitlists number 240+ households with average wait around 18 months.
status: draft
generated_from: problem.nelson.inequality.rental_affordability_gap
---

# Rental affordability gap between income quintiles

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Affordability, not just supply

Even at Nelson's tight overall vacancy rate, the binding issue for the bottom quintile is unit price, not unit availability (claim.nelson.inequality.rental_affordability_gap_claim). Accommodation Supplement and Income-Related Rent Subsidies stretch the bottom quintile's rent capacity to part of the way, but the social-housing waitlist absorbs the residual.


## Social-housing supply gap

Public and community housing in Nelson covers only around 8 percent of rental demand. Where this share is higher in comparable regions (around 12-15 percent), the same private-market price pressure produces less downstream child poverty and family-violence escalation.


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic isolation of rural communities from specialist services



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


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

- **The rental affordability gap in Nelson is substantial between income quintiles. Lowest-income households (Q1, median $22,800) pay 38–52% of income on rent; Q2 households (median $35,200) pay 28–36%; Q3+ households (median >$55,000) pay 18–22%. Median rent of $510/week is unaffordable at market rates for households earning <$30,000/year without housing assistance. Community housing and state housing stock cover ~8% of rental demand; waitlists number 240+ households, with average wait time of 18 months. Private landlord rental assistance programs cover <100 households/year.** [value: 45 percent of Q1 income spent on median rent; 2024] *(confidence: medium)* — Income and Inequality in Nelson Census 2023.

---

## Further reading


- **Income and Inequality in Nelson Census 2023** — Stats NZ (Statistics New Zealand), 2023 — <https://www.stats.nz>


---

## Technical notes

*State variables:* q1_rent_to_income_ratio, social_housing_waitlist_n, social_housing_share_of_stock.

*Constraints:* build_pipeline_capacity, land_availability.

*Inputs:* accommodation_supplement, kainga_ora_pipeline, community_housing_funding.


*Feedback loops:*

- `Subsidy-rent feedback: accommodation supplement increases recipients' rent capacity in a tight market, raising the price floor and partially offsetting the subsidy's net affordability gain.`


---

*Generated from `problem.nelson.inequality.rental_affordability_gap` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
