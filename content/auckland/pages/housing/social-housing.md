---
title: "Public and social housing deficit in Tāmaki Makaurau Auckland"
section: housing
subpage: social-housing
order: 3
updated: 2026-04-26
summary: >
  A structural deficit in public housing stock relative to need, combined with rents that are unaffordable for the lowest-income households, has produced a chronic public housing waitlist concentrated in South and West Auckland. Demand is driven by households whose incomes have not kept pace with market rents, and by the absence of the deposit capital required for ownership. The waitlist functions as a queue for a stock that grows too slowly to clear.
status: draft
generated_from: problem.auckland.housing.social_housing
---

# Public and social housing deficit in Tāmaki Makaurau Auckland

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Scale of the waitlist

Approximately 24,000 households were on the national public housing register as of June 2023, with Auckland carrying the largest regional share (claim.auckland.housing.waitlist_size_2023). The register predominantly comprises households in priority need — those experiencing homelessness, severe overcrowding, or family violence — for whom the private market is either inaccessible or unsafe.


## The emergency housing pressure valve

In the absence of sufficient public tenancies, households in acute need are placed in emergency housing — predominantly motel accommodation funded by MSD special needs grants. The Crown spent over NZD 300 million annually at peak on this substitute (claim.auckland.housing.emergency_housing_cost), a high-cost, low-stability outcome that does not resolve underlying housing need and generates significant harm for children and families in long-term motel placements.


## Structural stock deficit and the delivery debate

New Zealand's public housing stock as a share of total dwellings has not recovered to the level needed since the 1990s sell-off (claim.auckland.housing.public_stock_deficit). Kāinga Ora's build programme has added stock but has not closed the gap. The active debate is between direct Crown expansion of Kāinga Ora's programme and diversification to community housing providers and iwi housing entities, each of which has distinct financing, cultural, and accountability trade-offs.


---

## References



- **Public Housing Register: June 2023 Quarter** (Ministry of Social Development | Te Manatū Whakahiato Ora), 2023 — <https://www.msd.govt.nz/about-msd-and-our-work/publications-resources/statistics/housing/index.html>

- **Housing in Aotearoa: 2023** (Ministry of Housing and Urban Development | Manatū Wāhanga Okioki), 2023 — <https://www.hud.govt.nz/our-work/research-and-evaluation/housing-in-aotearoa-2023/>

- **Kāinga Ora Annual Report 2022/23** (Kāinga Ora – Homes and Communities), 2023 — <https://kaingaora.govt.nz/publications/annual-report/>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Public housing stock shortage



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus

#### Rental affordability gap



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Community and iwi housing provider model

Social housing delivery should be diversified away from Kāinga Ora toward community housing providers and iwi housing entities, which can better match housing design and tenancy support to community needs and access philanthropic and private capital alongside Crown funding.

**Flagship moves:**

- Increase long-term government housing places contracted to registered community housing providers (CHPs)
- Fund iwi housing entities as co-investors in papakāinga and urban Māori housing developments
- Establish a social housing bond mechanism to allow CHPs to access institutional capital for large-scale delivery

**Tensions:**

- Community housing providers have limited balance sheets and cannot scale to the volumes required without a substantial increase in Crown income-related rent subsidy commitments; diversification may substitute for rather than augment direct Crown delivery.

- Contracting complexity and provider quality variation make it difficult to maintain consistent tenancy outcomes across a fragmented provider network; the monitoring and accountability infrastructure is immature.


**Interventions on the system:**

- Contract an additional 2,000 government housing places per year to CHPs through long-term (25-year) lease arrangements backed by income-related rent subsidies.
 (state variable: `public_housing_stock`, sign: +) (relaxes: `crown_capital_programme_cap`)
- Co-invest with iwi housing entities in urban papakāinga developments on Māori-owned land in Auckland, unlocking underutilised land for housing aligned with cultural preferences.
 (state variable: `feasible_development_sites`, sign: +)


#### Direct Crown public housing expansion

The public housing deficit requires a large-scale, Crown-funded build programme delivered primarily through Kāinga Ora; only the Crown's balance sheet and direct commissioning capacity can deliver at the speed and volume that the waitlist requires.

**Flagship moves:**

- Restore and expand the Kāinga Ora capital programme to deliver a minimum 3,000 new public dwellings per year nationally
- Mandate mixed-tenure development on all public land disposals, requiring a minimum public housing component
- Reform Kāinga Ora's balance sheet constraints to allow increased borrowing for housing delivery

**Tensions:**

- Large-scale Crown delivery concentrates financial risk on the public balance sheet and creates procurement bottlenecks when the construction sector is operating near capacity, potentially crowding out private market supply.

- Centralised delivery through a single Crown entity is slower to respond to community-specific housing needs, including those of Māori and Pacific communities where Kāinga Ora's model is a poor cultural fit.


**Interventions on the system:**

- Increase the Kāinga Ora annual delivery target to 3,000+ new dwellings nationally, with Auckland receiving a proportional share reflecting its share of waitlist demand.
 (state variable: `public_housing_stock`, sign: +) (relaxes: `crown_capital_programme_cap`)
- Acquire strategically located urban land for mixed-tenure development combining market, affordable, and public housing on the same site.
 (state variable: `feasible_development_sites`, sign: +)


### Claims cited on this page

- **As of June 2023, approximately 24,000 households were on the New Zealand public housing register nationally, with Auckland accounting for the largest regional share — reflecting the concentration of severe housing need in the city relative to available public housing stock.
** [value: 24000 households; 2023-06] — Public Housing Register: June 2023 Quarter.
- **The New Zealand government's emergency housing expenditure peaked at approximately NZD 300 million per year in 2021-2023, funding motel and transitional accommodation for households unable to access public housing or sustain private rentals. Auckland accounts for the largest share of emergency housing placements nationally, reflecting the city's compressed public housing waitlist and the absence of affordable private-market alternatives for the lowest-income households. Emergency housing is a fiscally costly substitute for the social housing stock not built.
** [value: 300 NZD million (annual government expenditure, approximate peak); 2021-2023] *(confidence: medium)* — Public Housing Register: June 2023 Quarter; Housing in Aotearoa: 2023.
- **New Zealand's public housing stock as a proportion of total dwellings declined sharply following the 1990s sell-off and has not been restored to the level required to house the lowest-income households unable to access the private rental market; Kainga Ora's build programme has added stock but has not closed the structural deficit against the scale of need.
** — Kāinga Ora Annual Report 2022/23; Housing in Aotearoa: 2023.

### Systems-model notes

*State variables:* public_housing_stock, housing_register_size, emergency_housing_placements.

*Constraints:* crown_capital_programme_cap, construction_sector_capacity, land_availability_for_public_housing.

*Inputs:* crown_capital_programme, community_housing_provider_capacity, income_related_rent_subsidy_budget.


*Feedback loops:*

- `Waitlist-to-emergency: households unable to secure a public tenancy flow into emergency housing, increasing fiscal pressure and creating chronic instability that deepens housing need over time.
`
- `Stock-sell-off legacy: the 1990s privatisation of state housing stock removed units from the public portfolio permanently; restoring stock requires new-build capital rather than retrieval of existing assets, making the deficit expensive to close.
`


</details>

---

*Generated from `problem.auckland.housing.social_housing` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
