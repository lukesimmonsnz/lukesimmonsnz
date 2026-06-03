---
title: "Housing unaffordability in Tāmaki Makaurau Auckland"
section: housing
subpage: affordability
order: 1
updated: 2026-04-26
summary: >
  Auckland's housing market is among the least affordable globally relative to household incomes. A structural supply deficit accumulated across the 2010s despite strong population growth, driven by restrictive zoning and infrastructure financing constraints. The active policy debate centres on whether supply-side liberalisation, demand-side management, or a combination of both is the appropriate response.

status: draft
generated_from: problem.auckland.housing.affordability
---

# Housing unaffordability in Tāmaki Makaurau Auckland

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Scale of the problem

Auckland consistently ranks among the most unaffordable major housing markets globally by the median multiple measure. A ratio of 10.7 in 2023 (claim.auckland.housing.affordability_ratio_2023) means a median-income household must devote more than a decade of gross income to purchase a median-priced dwelling — a ceiling that structurally excludes the majority of renter households from home ownership at current income and price levels.


## Structural supply deficit of the 2010s

The decade preceding the NPS-UD was characterised by a structural supply deficit: annual building consents consistently fell short of the dwelling additions required to match population growth and household formation (claim.auckland.housing.supply_deficit_2010s). Restrictive zoning, a tightly drawn Metropolitan Urban Limit, mandatory minimum lot sizes, and constrained infrastructure funding combined to limit developable land and suppress the supply response to rising prices.


## Policy response: NPS-UD and the consent surge

The National Policy Statement on Urban Development 2021 (NPS-UD) mandated significant upzoning of Auckland's residential land, enabling intensification near transit corridors as-of-right. Building consents reached record volumes by 2022, indicating the supply response that previous planning rules had suppressed was latent in the market (claim.auckland.housing.nps_ud_upzoning). Whether this correction is sufficient — and whether demand-side complementary measures are needed — is the active policy debate between the supply-reform and demand-management camps.


---

## References



- **17th Annual Demographia International Housing Affordability Survey** — Wendell Cox and Hugh Pavletich (Demographia), 2024 — <http://www.demographia.com/dhi.pdf>

- **Housing in Aotearoa: 2023** (Ministry of Housing and Urban Development | Manatū Wāhanga Okioki), 2023 — <https://www.hud.govt.nz/our-work/research-and-evaluation/housing-in-aotearoa-2023/>

- **Building Consents Issued: December 2023** (Stats NZ | Tatauranga Aotearoa), 2023 — <https://www.stats.govt.nz/information-releases/building-consents-issued-december-2023>

- **Better Urban Planning - Final Report** — New Zealand Productivity Commission (New Zealand Productivity Commission), 2017 — <https://www.treasury.govt.nz/publications/better-urban-planning-final-report>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Population and household growth



- **Category:** demographic
- **Timescale:** medium
- **Consensus:** consensus

#### Restrictive land-use regulation



- **Category:** regulatory
- **Timescale:** long
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Demand management

Speculative investor demand, tax incentives, and financialisation of residential property have materially amplified Auckland's affordability problem; demand-side interventions are necessary complements to any supply-side programme.

**Flagship moves:**

- Reform tax treatment of residential investment property: extend bright-line tests, remove negative-gearing advantages
- Introduce a land value tax to impose holding costs on underdeveloped zoned land, countering land-banking

**Tensions:**

- Demand-side interventions risk chilling private-sector development finance and reducing rental supply in the short run, worsening conditions for renters before the medium-term benefits materialise.

- Removing investor tax advantages may reduce build-to-rent and boarding-house investment, increasing pressure on the lowest-income rental segment that public supply cannot absorb quickly.


**Interventions on the system:**

- Extend the bright-line property tax to 10+ years to deter speculative short-term churn and reduce the premium bid for non-owner-occupied residential assets.
 (state variable: `median_house_price`, sign: -)
- Introduce an annual land value tax on the unimproved value of residential land to impose holding costs on underdeveloped parcels in high-demand zones, accelerating supply response from existing owners.
 (state variable: `housing_stock_per_capita`, sign: +)


#### Supply-side reform

Auckland's housing unaffordability is primarily a supply-side failure; expanding housing supply through planning liberalisation and infrastructure investment is the primary lever for restoring affordability.

**Flagship moves:**

- Upzone residential land to allow medium and high-density development as-of-right
- Remove density restrictions and height limits within walkable distance of frequent-transit stops
- Fast-track infrastructure funding to unlock greenfield and brownfield capacity

**Tensions:**

- Rapid intensification generates neighbour opposition and can strain existing infrastructure networks if not sequenced with capital investment; the planning and infrastructure funding reforms are coupled problems.

- Supply-side liberalisation alone may not deliver affordable housing if land-banking and construction-cost barriers absorb the price signal; landowners capturing windfall gains from upzoning reduces the fiscal headroom for accompanying public investment.


**Interventions on the system:**

- Enable as-of-right 3–6 storey residential development within 1.5 km of frequent-transit stops.
 (state variable: `housing_stock_per_capita`, sign: +) (relaxes: `restrictive_residential_zoning`)
- Reform developer-contribution regimes to lower the marginal infrastructure cost of infill and medium-density development.
 (state variable: `annual_building_consents`, sign: +) (relaxes: `infrastructure_provision_capacity`)


### Claims cited on this page

- **Auckland's median multiple (median dwelling price divided by median annual household income) was 10.7 in 2023, placing it among the five least affordable major urban markets globally by this measure.
** [value: 10.7 ratio (dimensionless); 2023] — 17th Annual Demographia International Housing Affordability Survey.
- **Auckland experienced a structural housing supply deficit throughout the 2010s, with annual building consents consistently falling short of the dwelling additions required to keep pace with population growth and household formation.
** — Housing in Aotearoa: 2023.
- **Following the National Policy Statement on Urban Development 2021 (NPS-UD), Auckland upzoned substantial residential land to permit medium and high-density development as-of-right, and annual building consents reached record volumes by 2022, indicating a latent supply response that previous planning rules had suppressed.
** *(confidence: medium)* — Building Consents Issued: December 2023; Housing in Aotearoa: 2023.
- **The New Zealand Productivity Commission's 2017 Better Urban Planning inquiry recommended replacing the Resource Management Act's land-use provisions with a more permissive, goal-based urban-planning framework, separating environmental protection from urban development decisions, and broadening infrastructure funding tools (including targeted rates and value capture) to enable Auckland and other high-growth cities to fund growth-supporting infrastructure. The 2017 report has been widely cited as the analytical foundation for subsequent NPS-UD and RMA reform debates affecting Auckland.
** — Better Urban Planning - Final Report.

### Systems-model notes

*State variables:* housing_stock_per_capita, median_house_price, housing_affordability_ratio.

*Constraints:* restrictive_residential_zoning, infrastructure_provision_capacity, construction_sector_capacity.

*Inputs:* annual_building_consents, net_migration, household_dissolution_rate.


*Feedback loops:*

- `Price-signal-to-supply: high prices should incentivise development, but planning constraints and land-banking attenuate the market response, creating a regime where price rises do not clear into commensurate new supply.
`
- `Affordability-migration loop: sustained unaffordability drives outmigration of working households, providing partial and lagged demand relief but at the cost of labour-market thinning in high-wage sectors.
`
- `Investor-demand amplification: in a low-affordability regime, residential property becomes attractive as a yield-bearing asset; investor entry bids up prices at the margin, reinforcing unaffordability.
`


</details>

---

*Generated from `problem.auckland.housing.affordability` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
