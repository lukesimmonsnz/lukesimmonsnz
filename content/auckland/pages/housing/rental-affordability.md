---
title: "Rental affordability"
section: housing
subpage: rental-affordability
order: 4
updated: 2026-04-26
summary: >
  Auckland renter households — particularly those in the lower two income quintiles — face median rents consuming more than 30% of gross income, with a significant share exceeding 40%. The cost burden is compounded by structural tenure insecurity: short fixed-term tenancies and the absence of rent stabilisation prevent renters from planning around stable housing costs. Low rental vacancy rates sustain landlord pricing power regardless of wage growth, locking households in a self-reinforcing cycle of high cost and constrained exit options.

status: draft
generated_from: problem.auckland.housing.rental_affordability
---

# Rental affordability

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## The cost burden threshold

Auckland renters spending above 30% of gross income on rent are classified as housing-stressed; those above 40% face severe cost burden. The 2021–2023 MBIE affordability indicators show median rent in Auckland consuming approximately 33% of median renter household income, placing the median renter household at the threshold of housing stress. Households in the lower two income quintiles — those earning too much for income-related rent subsidy but too little to absorb market rents without financial stress — are disproportionately exposed.


## Tenure insecurity as a cost amplifier

High rent is more damaging when tenants cannot plan around stable housing costs. New Zealand's tenancy norms — historically dominated by 6–12 month fixed-term tenancies with no rent stabilisation — have made renting structurally less secure than in comparable OECD countries. The 2020 Residential Tenancies Amendment Act removed no-cause termination for periodic tenancies but left rent increases uncapped, meaning tenants remain exposed to speculative uplift at each renewal and cannot credibly budget beyond the current term.


## Vacancy tightness and market power

Persistently low rental vacancy rates give landlords pricing power independent of broader cost-of-living dynamics. When fewer than 2–3% of rental properties are vacant, renters competing for available stock face upward rent pressure at every transition. Vacancy tightness also reduces tenants' ability to exit poor-quality or unaffordable tenancies, weakening bargaining position and making both the cost and quality dimensions of the problem mutually reinforcing.


---

## References



- **Rental Affordability Indicators: New Zealand 2023** (Ministry of Business, Innovation and Employment | Hīkina Whakatutuki), 2023 — <https://www.mbie.govt.nz/building-and-energy/building-and-construction/sector-information-and-data/rental-affordability/>

- **Tenancy Bond Data: Rental Price Statistics 2023** (Ministry of Business, Innovation and Employment | Hīkina Whakatutuki), 2023 — <https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/>

- **Housing in Aotearoa: 2023** (Ministry of Housing and Urban Development | Manatū Wāhanga Okioki), 2023 — <https://www.hud.govt.nz/our-work/research-and-evaluation/housing-in-aotearoa-2023/>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Rental market tightness



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus

#### Weak rental tenure norms and renter precarity



- **Category:** institutional
- **Timescale:** long
- **Consensus:** mostly-agreed


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Build-to-rent institutional investment

Institutional development of purpose-built rental housing at scale — with professional management, longer tenancy terms, and stable rents structured around yield rather than capital gain — addresses rental affordability by expanding supply and raising tenure quality without requiring legislative rent caps.

**Flagship moves:**

- Establish a dedicated build-to-rent planning pathway with streamlined consent processes and density allowances for institutional-scale rental developments
- Introduce tax treatment parity between build-to-rent and build-to-sell to reduce the structural bias toward owner-occupier supply
- Enable long-term fixed-rent lease structures (3–5 years) as a standard institutional product to reduce renter cost uncertainty

**Tensions:**

- Institutional build-to-rent is viable only above a minimum yield threshold; rent stabilisation legislation (as proposed by the tenancy law reform camp) compresses yield, reducing institutional investor appetite and potentially shrinking the pipeline it depends on.

- Without an affordable component requirement, build-to-rent delivers primarily mid-to-upper-market product, leaving the households most exposed to cost burden unserved by the new supply.


**Interventions on the system:**

- Create a build-to-rent consent fast-track for developments of ≥50 units with at least 10% below-market units, targeting a 12-month consent-to-build pipeline.
 (state variable: `median_rent_level`, sign: -) (relaxes: `planning consent bottleneck for large-scale rental development`)
- Align GST and depreciation rules for build-to-rent with commercial asset classes to correct the tax asymmetry that favours build-to-sell.
 (state variable: `institutional_rental_supply`, sign: +)
- Mandate a minimum habitability specification (heating, insulation, ventilation) as a condition of the build-to-rent consent pathway, raising baseline rental_housing_quality in new institutional stock.
 (state variable: `rental_housing_quality`, sign: +)


#### Tenancy law reform and rent stabilisation

Renter households need stronger legal protections — including caps or limits on rent increases, longer notice periods, and greater security against no-cause eviction — to make renting a viable long-term tenure independent of homeownership constraints.

**Flagship moves:**

- Introduce annual rent increase caps linked to CPI or a fixed percentage to limit speculative rent uplift
- Extend minimum notice periods and restrict termination grounds to further protect long-term tenants
- Establish a rental warrant of fitness to ensure minimum habitability standards as a condition of tenancy

**Tensions:**

- Rent stabilisation reduces the return on investment for landlords and risks accelerating the exit of private landlords from the market, reducing rental supply in the short run — particularly for smaller landlords with thin margins who cross-subsidise below-market rents for long-term tenants.

- Habitability standards enforcement requires adequate inspection capacity and legal aid for tenants; without these, minimum standards on paper do not translate to improved conditions in practice.


**Interventions on the system:**

- Cap annual rent increases at CPI + 2% with a two-year phase-in to prevent pre-cap speculative increases.
 (state variable: `median_rent_level`, sign: -)
- Mandate a rental warrant of fitness covering heating, insulation, moisture control, and ventilation as a condition of bond lodgement.
 (state variable: `rental_housing_quality`, sign: +)


### Claims cited on this page

- **Auckland renter households paid approximately 33 percent of median gross household income in rent in 2023, placing the median renter household above the 30 percent affordability threshold and indicating widespread rental cost burden across the income distribution of renters.
** [value: 33 percent of median renter household income; 2023] *(confidence: medium)* — Rental Affordability Indicators: New Zealand 2023; Tenancy Bond Data: Rental Price Statistics 2023.
- **A significant proportion of Auckland renter households in the lower two income quintiles spend more than 40 percent of gross income on rent, indicating severe rental cost burden concentrated among those least able to absorb it — households who earn too much for income-related rent subsidy but too little to sustain market rents without financial stress.
** *(confidence: medium)* — Rental Affordability Indicators: New Zealand 2023; Housing in Aotearoa: 2023.
- **New Zealand renters have historically had weaker tenure security than renters in comparable OECD countries: short fixed-term tenancies of 6-12 months were the norm, landlords could terminate periodic tenancies without cause, and tenants faced structural barriers to personalising or stabilising their home. The Residential Tenancies Amendment Act 2020 removed no-cause termination for periodic tenancies but did not introduce rent stabilisation, meaningful minimum tenancy lengths, or a right to renew fixed-term tenancies. Auckland renters — who make up a larger and growing share of the city's households — retain materially weaker security of tenure than counterparts in Germany, the Netherlands, France, or Vienna's regulated rental sector, sustaining a structural asymmetry between landlord and tenant that compounds affordability stress. stabilising their home. The Residential Tenancies Amendment Act 2020 removed no-cause termination for periodic tenancies but did not introduce rent stabilisation.
** — Rental Affordability Indicators: New Zealand 2023; Housing in Aotearoa: 2023.

### Systems-model notes

*State variables:* median_rent_level, renter_cost_burden, rental_housing_quality, institutional_rental_supply.

*Constraints:* No statutory rent increase cap — landlords can increase rents to market at each tenancy renewal, Low vacancy rate (< 2%) eliminates practical exit options and sustains pricing power, Tax and planning settings structurally favour build-to-sell over build-to-rent, suppressing institutional supply.

*Inputs:* rental_vacancy_rate, wage_growth_rate, new_rental_supply_rate, tenure_security_index.


*Feedback loops:*

- `High renter_cost_burden depresses household savings, preventing purchase transition and prolonging rental demand — which sustains high median_rent_level`
- `Low rental_housing_quality combined with insecure tenure reduces tenants' willingness to invest in maintenance or negotiate improvements, perpetuating quality floor`


</details>

---

*Generated from `problem.auckland.housing.rental_affordability` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
