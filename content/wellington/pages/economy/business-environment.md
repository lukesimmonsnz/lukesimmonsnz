---
title: "Business environment and economic diversification in Wellington"
section: economy
subpage: business-environment
order: 4
updated: 2026-04-26
summary: >
  Wellington's private sector remains smaller and less diversified than its government sector. Technology, creative industries, and tourism offer growth potential, but business confidence has declined post-2024 restructuring, and Wellington faces cost competitiveness challenges as a business location relative to Auckland and offshore centres.
status: draft
generated_from: problem.wellington.economy.business_environment
---

# Business environment and economic diversification in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Business confidence post-restructuring

Wellington business confidence indices declined sharply following the 2024 public sector restructuring, as reduced government spending contracts and workforce displacement reduced demand in the local service economy (claim.wellington.economy.business_confidence_2024).


## Innovation sector potential

Wellington hosts a cluster of technology, creative, and knowledge-intensive firms including the film and visual effects industry, fintech, and government IT — but this cluster remains smaller than what Wellington's human capital base would suggest (claim.wellington.economy.innovation_sector_employment).


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic distance from export markets



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus

### Limited private sector depth relative to public sector



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus

### Private sector dependence on government procurement



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Agglomeration and CBD Vitality Investment

Wellington's compact urban core is its productivity asset; investment in CBD amenity, housing, and walkability will attract and retain high-productivity workers.

**Flagship moves:**

- CBD housing intensification to increase resident population in central suburbs
- Improved international connectivity through Wellington Airport capacity
- Cultural and event infrastructure investment to sustain Wellington's liveability premium

**Tensions:**

- Airport expansion raises carbon emissions and community noise objections
- Cultural amenity investment may not translate to productivity gains

**Interventions on the system:**

- Approve and fund Wellington CBD intensification overlay to double CBD resident population by 2040 (state variable: `cbd_employment_density`, sign: +)


### Regulatory Environment Improvement

Reducing compliance burden for Wellington businesses through council process improvement and national regulatory reform will improve the business environment.

**Flagship moves:**

- Wellington City Council consent processing time target of 20 working days
- Business liaison officer programme for Wellington CBD businesses
- Reduce cumulative regulatory burden on hospitality and retail sectors

**Tensions:**

- Faster consenting risks inadequate environmental and safety scrutiny
- Regulatory streamlining may benefit large businesses more than SMEs

**Interventions on the system:**

- Implement Wellington City Council Building Consent processing SLA of 20 working days with public dashboard (state variable: `consent_processing_days`, sign: -)


---

## Claims cited on this page

- **Wellington business confidence declined significantly in 2024, following public sector restructuring and reduced government investment. As the nation's capital with ~30% public sector employment, Wellington's business confidence indices are sensitive to central government budget cycles and policy changes affecting departmental locations and headcount.** *(confidence: medium)* — Treasury Budget Economic and Fiscal Update 2024; Wellington City Council Annual Plan 2024/25.
- **Wellington hosts a cluster of technology, creative, and knowledge-intensive firms — including the film and visual effects industry, fintech, and government IT services — but this cluster is smaller than Wellington's human capital base would support if the economy were less government-dependent.** *(confidence: medium)* — Census 2023: Wellington Regional Profile; Wellington City Council Annual Plan 2024/25.

---

## Further reading


- **Treasury Budget Economic and Fiscal Update 2024** (NZ Treasury), 2024 — <https://www.treasury.govt.nz/publications/efu>

- **Wellington City Council Annual Plan 2024/25** (Wellington City Council), 2024 — <https://www.wellington.govt.nz/your-council/plans-policies-and-bylaws/annual-plan>

- **Census 2023: Wellington Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* business_confidence_index, startup_formation_rate.

*Constraints:* distance_from_export_markets, commercial_property_cost.

*Inputs:* government_procurement_policy, innovation_ecosystem_investment.


*Feedback loops:*

- `Government dependence lock-in: a business environment built around government clients is unattractive to export-oriented firms; without export-oriented growth, the economy remains government-dependent.`


---

*Generated from `problem.wellington.economy.business_environment` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
