---
title: "Problem: Affordability"
section: housing
subpage: affordability
order: 1
updated: 2026-04-26
summary: >
  Description of affordability in west-coast.
status: draft
generated_from: problem.west_coast.housing.affordability
---

# Problem: Affordability

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Housing challenge

Problem: Affordability is a key dimension of the broader housing challenge facing the region.


---


## Drivers

The following structural drivers contribute to this problem.


### Driver: Driver 1



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus

### Driver: Driver 2



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Housing Quality Improvement and Warm Homes

West Coast's cold, wet climate combined with poor housing stock quality creates significant health risk; targeted retrofit programmes address both energy poverty and health outcomes.

**Flagship moves:**

- Fund West Coast Warm Homes programme targeting pre-1980 housing stock
- Establish mould remediation support programme for rental properties
- Co-fund insulation and heating upgrades for low-income owner-occupiers

**Tensions:**

- Landlords resist mandatory retrofit requirements without subsidy
- Low property values reduce retrofit investment incentive

**Interventions on the system:**

- Fund West Coast Warm Homes retrofit programme targeting 500 homes (state variable: `cold_home_proportion`, sign: -)


### Stabilising Housing Supply in Depopulating Communities

West Coast's depopulation creates vacant and deteriorating housing stock in some towns alongside genuine unmet need for quality affordable housing in Greymouth and Hokitika.

**Flagship moves:**

- Establish West Coast Housing Trust to acquire, remediate, and manage affordable rental stock
- Create land banking mechanism for strategic housing sites in Greymouth
- Fund emergency housing provision for people leaving unsafe situations

**Tensions:**

- Population decline limits long-term demand for new social housing
- Vacant housing in depopulating towns is hard to repurpose without demolition costs

**Interventions on the system:**

- Establish West Coast Housing Trust for affordable rental provision (state variable: `social_housing_waitlist`, sign: -)


---

## Claims cited on this page

- **West Coast house prices are among the lowest in New Zealand (median ~$280,000 in Westport, ~$320,000 in Greymouth), yet local median household income is only $52,000 annually. Price-to-income ratio exceeds 5:1, making homeownership unaffordable for local workers. Post-flood insurance withdrawal has collapsed property values further, trapping owners in negative equity.** [value: 280000 NZD median house price (Westport); 2023-2024] — West Coast Housing Market and Depopulation 2024; Income and Inequality in West Coast Census 2023.

---

## Further reading


- **West Coast Housing Market and Depopulation 2024** — Real Estate Institute NZ (Real Estate Institute of New Zealand), 2024 — <https://www.reinz.co.nz>

- **Income and Inequality in West Coast Census 2023** — Stats NZ (Statistics New Zealand), 2023 — <https://www.stats.nz>


---

## Technical notes

*State variables:* housing_affordability_index.

*Constraints:* implementation_capacity.



---

*Generated from `problem.west_coast.housing.affordability` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
