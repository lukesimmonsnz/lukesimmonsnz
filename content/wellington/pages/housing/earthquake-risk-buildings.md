---
title: "Earthquake-prone residential building stock in Wellington"
section: housing
subpage: earthquake-risk-buildings
order: 2
updated: 2026-04-26
summary: >
  Wellington City has one of the highest concentrations of earthquake-prone buildings in New Zealand. Pre-1976 unreinforced masonry and concrete structures dominate the inner-city residential and commercial stock. Seismic retrofit obligations impose large costs on owners, slowing redevelopment and contributing to housing supply constraints.
status: draft
generated_from: problem.wellington.housing.earthquake_risk_buildings
---

# Earthquake-prone residential building stock in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Scale of the problem

Wellington City Council has identified over 3,500 buildings with earthquake-prone ratings under the Building (Earthquake-prone Buildings) Amendment Act 2016 (claim.wellington.housing.earthquake_prone_building_count). The inner city — including large sections of the CBD and surrounding suburbs — contains a high density of pre-1976 unreinforced masonry structures.


## Retrofit cost as supply barrier

Seismic retrofit costs often exceed the redevelopment value of ageing residential buildings, creating a catch-22: compliance is expensive, but non-compliance defers habitability. The result is an elevated vacancy and dereliction rate in earthquake-risk zones and a chilling effect on intensification investment (claim.wellington.housing.seismic_retrofit_cost_barrier).


---


## Drivers

The following structural drivers contribute to this problem.


### Earthquake-prone building stock



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus

### Seismic retrofit financial barrier



- **Category:** economic
- **Timescale:** medium
- **Consensus:** mostly-agreed


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Mandatory Seismic Retrofit Programme

Earthquake-prone buildings must be retrofitted or demolished on statutory timelines; voluntary compliance has failed.

**Flagship moves:**

- Accelerate EPB compliance deadlines to 2032 for all residential buildings
- Crown-subsidised retrofit loan fund for owner-occupiers
- Mandatory disclosure of seismic rating at point of sale and lease

**Tensions:**

- Retrofit costs may be prohibitive for low-income owners, driving displacement
- Demolition of older housing stock reduces rental supply during transition
- Cost socialisation raises moral hazard for future building standard decisions

**Interventions on the system:**

- Establish Wellington Regional Seismic Retrofit Fund with low-interest loans up to $150k per dwelling (state variable: `compliant_building_stock`, sign: +) (relaxes: `retrofit_cost_barrier`)


### Market-Led Seismic Risk Management

Insurance pricing and mandatory disclosure will incentivise voluntary retrofit and redevelopment without public subsidy distortions.

**Flagship moves:**

- Require seismic engineering report at every property sale
- Allow insurers to price earthquake-prone status explicitly in premiums
- Fast-track consent pathways for replacement buildings on EPB sites

**Tensions:**

- Market signals may be too slow relative to earthquake probability windows
- Low-income renters bear disproportionate risk exposure while owners act slowly

**Interventions on the system:**

- Introduce standardised public seismic-rating register for all buildings ≥2 storeys (state variable: `information_transparency`, sign: +)


### Precautionary Land Use Controls for Hazard Zones

Prohibiting new development in compound hazard zones (fault lines + flood plains + liquefaction) is the safest long-term approach.

**Flagship moves:**

- Map all Wellington compound hazard zones in District Plans
- Prohibition on new residential development in category 3 hazard zones
- Incentive-based voluntary relocation from highest-risk existing residential areas

**Tensions:**

- Development prohibitions may worsen housing supply in an already constrained market
- Category boundaries are contested; property owners dispute zone classifications

**Interventions on the system:**

- Require multi-hazard risk overlay in all Wellington District Plan reviews under RMA (state variable: `development_in_hazard_zones`, sign: -)


---

## Claims cited on this page

- **Wellington City Council has identified over 3,500 buildings with earthquake-prone ratings under the Building (Earthquake-prone Buildings) Amendment Act 2016, representing one of the highest concentrations of earthquake-prone stock in any New Zealand city.** [value: 3500 buildings; 2023] — Wellington City Council Earthquake-Prone Buildings Policy 2023.
- **Seismic retrofit costs for pre-1976 unreinforced masonry residential buildings in Wellington often exceed the post-retrofit market value of the building, creating a financial barrier that deters compliance and suppresses residential redevelopment in earthquake-prone zones.** *(confidence: medium)* — Wellington City Council Earthquake-Prone Buildings Policy 2023; Wellington Housing Market: Constraints, Costs and Consequences.

---

## Further reading


- **Wellington City Council Earthquake-Prone Buildings Policy 2023** (Wellington City Council), 2023 — <https://www.wellington.govt.nz/building-and-development/building-consents-and-inspections/earthquake-prone-buildings>

- **Wellington Housing Market: Constraints, Costs and Consequences** — Greenaway-McGrevy R, Pacheco G (Motu Economic and Public Policy Research), 2022 — <https://www.motu.nz/our-work/urban-and-regional/housing/>


---

## Technical notes

*State variables:* earthquake_prone_building_count, remediation_compliance_rate.

*Constraints:* retrofit_cost_per_building, statutory_compliance_timeline.

*Inputs:* building_consent_activity, retrofit_funding_availability.


*Feedback loops:*

- `Cost-barrier loop: high retrofit costs relative to building value deter compliance; owners defer or demolish rather than upgrade, reducing net housing stock.`


---

*Generated from `problem.wellington.housing.earthquake_risk_buildings` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
