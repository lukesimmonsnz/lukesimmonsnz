---
title: "Digital infrastructure gap, urban-rural and household-income"
section: infrastructure
subpage: infrastructure_4
order: 4
updated: 2026-04-26
summary: >
  Fibre-to-the-home coverage is around 72 percent in Nelson city and 38 percent in Tasman district (against 79 percent nationally). Rural coverage (Golden Bay, upper valleys) is below 20 percent. Mobile 4G coverage is around 78 percent in urban Nelson with rural gaps significant. Broadband uptake among low-income households is around 62 percent against 84 percent nationally; cost ($89-124 per month) and data limits are barriers.
status: draft
generated_from: problem.nelson.infrastructure.infrastructure_4
---

# Digital infrastructure gap, urban-rural and household-income

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Two digital divides

Nelson has both an urban-rural digital divide and a household-income digital divide (claim.nelson.infrastructure.infrastructure_4_claim). Rural coverage gaps are addressable through Rural Broadband Initiative extensions; the income-based gap is more about price and service rather than coverage.


## Distance-learning and remote-work amplification

The pandemic permanently raised the floor on what counts as adequate household connectivity. Schools rely on online platforms; remote work requires reliable upload speeds. The 12 percent of teachers reporting inadequate technology and the 38 percent of low-income households without home broadband are the same cohort that bears the largest cost from the gap.


---


## Drivers

The following structural drivers contribute to this problem.


### Small population scale against high per-unit infrastructure cost



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing infrastructure challenges.

**Flagship moves:**

- Prioritise three-waters infrastructure renewal in Nelson urban centres
- Establish a multi-year capital works programme for wastewater and stormwater upgrades
- Apply for central government infrastructure co-funding to supplement council rates

**Tensions:**

- Infrastructure renewal requires significant capital expenditure that strains small council budgets.
- Prioritising upgrades may delay other community investment needs.

**Interventions on the system:**

- Accelerate infrastructure renewal investment in Nelson (state variable: `infrastructure_condition_index`, sign: +)
- Prioritise water and wastewater upgrades (state variable: `service_coverage`, sign: +)


---

## Claims cited on this page

- **Digital infrastructure in Nelson lags urban centers. Fibre-to-the-home coverage is 72% in Nelson city and 38% in Tasman district (vs. 79% nationally). Rural areas (Golden Bay, upper valleys) have coverage <20%, limiting remote work and education options. Mobile network coverage is 94% (voice) and 78% (4G data) in urban areas, with rural gaps significant. Broadband uptake among low-income households is 62% vs. 84% nationally; cost ($89–124/month) and data limits are barriers. Distance learning infrastructure at schools is limited; 12% of teachers lack adequate technology for online teaching delivery. Digital divide is amplifying with remote work expansion.** [value: 72 percent fibre-to-home coverage in Nelson city; 2024] *(confidence: medium)* — Nelson City Council Annual Plan 2024.

---

## Further reading


- **Nelson City Council Annual Plan 2024** — Nelson City Council (Nelson City Council), 2024 — <https://www.nelsoncitycouncil.co.nz>


---

## Technical notes

*State variables:* fibre_coverage_pct, low_income_broadband_uptake_pct, mobile_4g_coverage_pct.

*Constraints:* rural_population_density, household_disposable_income.

*Inputs:* rbi_extension_funding, retail_price_competition.


*Feedback loops:*

- `Coverage-uptake feedback: low rural coverage suppresses local digital-business formation, reducing local demand-pull for further coverage extension.`


---

*Generated from `problem.nelson.infrastructure.infrastructure_4` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
