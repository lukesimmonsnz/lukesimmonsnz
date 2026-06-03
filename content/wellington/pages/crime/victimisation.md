---
title: "Crime and victimisation in Wellington"
section: crime
subpage: victimisation
order: 1
updated: 2026-04-26
summary: >
  Wellington's overall crime rate is moderate by New Zealand standards, but victimisation is heavily concentrated in high-deprivation communities in Porirua and Hutt Valley. Repeat victimisation — where a small share of the population accounts for a disproportionate share of incidents — is a structural feature of Wellington's crime landscape.
status: draft
generated_from: problem.wellington.crime.victimisation
---

# Crime and victimisation in Wellington

<p class="horizon-band">Analysis horizon: 10yr</p>



## Victimisation rates

Wellington Police District records a personal victimisation rate of approximately 6% annually, but this average masks acute concentration in Porirua and parts of Lower Hutt, where rates are two to three times the Wellington City average (claim.wellington.crime.victimisation_rate_2023).


## Repeat victimisation

Repeat victimisation — where the same households or individuals are victimised multiple times in a year — accounts for a disproportionate share of total incidents in Wellington, concentrated in high-deprivation areas and family violence contexts (claim.wellington.crime.repeat_victimisation_concentration).


---


## Drivers

The following structural drivers contribute to this problem.


### Concentrated deprivation and crime environment



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus

### Repeat victimisation concentration in family harm contexts



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Social Crime Prevention Investment

Investing in youth opportunity, mental health, and housing stability in high-deprivation areas will reduce crime rates more sustainably than enforcement.

**Flagship moves:**

- Expand youth mentoring and alternative education pathways in Porirua and Hutt
- Co-locate mental health crisis services at police stations
- Alcohol management zones in areas with high assault concentrations

**Tensions:**

- Prevention benefits accrue over 10–20 year horizons, while enforcement shows faster short-term results
- Measuring effectiveness of prevention programmes is methodologically complex

**Interventions on the system:**

- Fund 5-year social crime prevention programme in Porirua and Hutt Valley integrated with housing and mental health services (state variable: `victimisation_rate`, sign: -)


### Targeted Enforcement and Deterrence

Hot-spot policing and targeted enforcement against repeat offenders reduces victimisation for communities most at risk.

**Flagship moves:**

- Increase police presence in identified crime hot-spots in Porirua and Lower Hutt
- Recidivist management programme with intensive supervision for high-harm offenders
- CCTV and environmental design improvements in high-crime locations

**Tensions:**

- Hot-spot policing risks displacing crime to adjacent areas
- Intensive supervision of recidivists requires significant corrections resourcing

**Interventions on the system:**

- Deploy dedicated hot-spot policing teams to 5 identified Wellington high-crime areas with 12-month evaluation (state variable: `crime_hot_spot_frequency`, sign: -)


---

## Claims cited on this page

- **Wellington Police District records a personal victimisation rate of approximately 6% annually, with rates in Porirua and parts of Lower Hutt two to three times the Wellington City average, indicating highly concentrated rather than uniformly elevated victimisation.** [value: 6 percent personal victimisation rate; 2022-2023] *(confidence: medium)* — New Zealand Police Crime Statistics 2022/23: Wellington District.
- **Repeat victimisation — the same households or individuals victimised multiple times in a year — accounts for a disproportionate share of total incidents in Wellington's high-deprivation areas, particularly in family harm contexts in Porirua.** *(confidence: medium)* — New Zealand Police Crime Statistics 2022/23: Wellington District.

---

## Further reading


- **New Zealand Police Crime Statistics 2022/23: Wellington District** (New Zealand Police), 2023 — <https://www.police.govt.nz/about-us/publications-statistics/data-and-statistics/policedatanz/victimisation-timeseries>


---

## Technical notes

*State variables:* personal_victimisation_rate, repeat_victimisation_proportion.

*Constraints:* economic_disadvantage, housing_instability.

*Inputs:* deprivation_level, policing_resource_allocation.


*Feedback loops:*

- `Deprivation-crime feedback: concentrated deprivation creates conditions for higher crime; high crime rates further depress area desirability and property values, deepening deprivation.`


---

*Generated from `problem.wellington.crime.victimisation` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
