---
title: "Housing unaffordability in Te Whanganui-a-Tara Wellington"
section: housing
subpage: affordability
order: 1
updated: 2026-04-26
summary: >
  Wellington's housing market has become structurally unaffordable by global measures. Constrained topography, restrictive zoning, and strong demand from government-sector employment combine to limit supply while sustaining price pressure. The policy debate centres on supply liberalisation, demand management, and the seismic dimension unique to Wellington.
status: draft
generated_from: problem.wellington.housing.affordability
---

# Housing unaffordability in Te Whanganui-a-Tara Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Scale of unaffordability

Wellington's median multiple reached approximately 8.7 in 2023 (claim.wellington.housing.median_multiple_2023), placing it among the least affordable mid-size cities globally by this measure. The severity is compounded by Wellington's role as the national capital: government-sector employment sustains demand while the physical geography severely limits where new housing can be built.


## Structural supply constraints

Unlike Auckland, where supply has surged following the NPS-UD, Wellington's consent pipeline remains constrained by the combination of steep terrain, fault-zone setbacks, and a large stock of earthquake-prone buildings that require costly remediation before residential redevelopment is viable (claim.wellington.housing.supply_consent_shortfall).


---


## Drivers

The following structural drivers contribute to this problem.


### Fault zone land-use setback rules



- **Category:** regulatory
- **Timescale:** permanent
- **Consensus:** consensus

### Residential property as investment asset



- **Category:** economic
- **Timescale:** medium
- **Consensus:** mostly-agreed

### Restrictive residential zoning



- **Category:** regulatory
- **Timescale:** long
- **Consensus:** consensus

### Topographic land supply constraint



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Institutional Build-to-Rent and Social Housing Expansion

Professionalised long-term rental providers and expanded Kāinga Ora stock create stable, affordable rental supply.

**Flagship moves:**

- Tax incentives for build-to-rent institutional investment in Wellington
- Accelerate Kāinga Ora pipeline in Porirua and Hutt Valley
- Community land trust model for perpetual affordability on Crown land

**Tensions:**

- Requires significant Crown capital allocation competing with fiscal consolidation pressures
- Institutional providers may prioritise mid-market returns over deep affordability

**Interventions on the system:**

- Allocate surplus Crown land in Wellington region to community land trusts at below-market value (state variable: `affordable_rental_stock`, sign: +)


### Managed Densification with Infrastructure Sequencing

Density increases must be sequenced with infrastructure investment; unmanaged intensification exacerbates flooding, wastewater, and transport stress.

**Flagship moves:**

- Infrastructure-led precinct planning before rezoning approvals
- Developer-funded infrastructure bonds tied to consent capacity
- Strategic growth nodes at Tawa, Porirua, and Hutt Valley rail corridors

**Tensions:**

- Slower rollout delays affordability relief for current renters
- Cost of infrastructure bonds may be passed to purchasers, limiting affordability gains

**Interventions on the system:**

- Require infrastructure capacity certificates before residential rezoning takes effect (state variable: `infrastructure_capacity`, sign: +)


### Upzoning and Intensification

Removing zoning restrictions and enabling medium-density development across Wellington's urban areas is the primary lever to improve affordability.

**Flagship moves:**

- Implement NPS-UD density requirements across all Wellington territorial authorities
- Permit six-storey residential buildings within 800m of rapid transit stops
- Remove minimum car-parking requirements citywide

**Tensions:**

- Intensification in fault-zone and liquefaction-prone land raises safety risks
- Infrastructure capacity (water, wastewater) constrains achievable density in many suburbs
- Heritage character areas create political resistance to blanket upzoning

**Interventions on the system:**

- Rezone residential land within 1km of Wellington CBD and Johnsonville/Porirua centres to allow 6-storey mixed-use (state variable: `zoned_capacity`, sign: +) (relaxes: `height_limit`)
- Mandate development contributions schedule that front-funds infrastructure upgrades for upzoned areas (state variable: `infrastructure_capacity`, sign: +)


---

## Claims cited on this page

- **Wellington's median house price to median household income ratio (median multiple) was approximately 8.7 in 2023, placing it in the severely unaffordable band by Demographia's international measure and substantially above the 3.0 threshold considered affordable. A median-income household would require nearly nine years of gross income to purchase a median-priced dwelling.** [value: 8.7 ratio (dimensionless); 2023] — 17th Annual Demographia International Housing Affordability Survey; Stats NZ Household Income and Housing Cost Statistics 2023.
- **Wellington's annual residential building consent volumes have consistently fallen short of the dwelling additions needed to keep pace with household formation, with the consent pipeline constrained by topographic complexity, earthquake-prone building compliance costs, and limited development-ready flat land.** — Aotearoa New Zealand Housing Report 2023; Wellington City Housing and Business Development Capacity Assessment 2022.

---

## Further reading


- **17th Annual Demographia International Housing Affordability Survey** — Wendell Cox and Hugh Pavletich (Demographia), 2024 — <http://www.demographia.com/dhi.pdf>

- **Stats NZ Household Income and Housing Cost Statistics 2023** (Stats NZ), 2023 — <https://www.stats.govt.nz/information-releases/household-income-and-housing-cost-statistics-new-zealand-year-ended-june-2023>

- **Aotearoa New Zealand Housing Report 2023** (Ministry of Housing and Urban Development), 2023 — <https://www.hud.govt.nz/housing-and-property/housing-research-and-data/housing-data-and-research/aotearoa-new-zealand-housing-report/>

- **Wellington City Housing and Business Development Capacity Assessment 2022** (Wellington City Council), 2022 — <https://www.wellington.govt.nz/planning-and-environment/urban-growth-and-housing>


---

## Technical notes

*State variables:* median_house_price, housing_affordability_ratio, housing_stock_per_capita.

*Constraints:* topographic_developable_land_limit, restrictive_residential_zoning, earthquake_prone_building_compliance_cost.

*Inputs:* annual_building_consents, net_migration, public_sector_employment.


*Feedback loops:*

- `Price-signal-to-supply attenuation: high prices should incentivise development, but topographic constraints and planning rules limit the supply response, sustaining elevated prices.`
- `Affordability-retention loop: sustained unaffordability drives out-migration of workers priced out of homeownership, thinning the labour market.`


---

*Generated from `problem.wellington.housing.affordability` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
