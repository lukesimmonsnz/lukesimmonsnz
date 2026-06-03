---
title: "Family violence prevalence and response gaps"
section: crime
subpage: family-violence
order: 2
updated: 2026-04-26
summary: >
  Family violence rates in Northland significantly exceed national averages, with inadequate support infrastructure for victims.
status: draft
generated_from: problem.northland.crime.family_violence
---

# Family violence prevalence and response gaps

<p class="horizon-band">Analysis horizon: 10yr</p>



## Scale and distribution

Family violence rates in Northland significantly exceed national averages, with inadequate support infrastructure for victims.


## Key drivers

The primary drivers of family violence prevalence and response gaps are structural and systemic, requiring both investment and institutional reform.


---


## Drivers

The following structural drivers contribute to this problem.


### Deprivation and social disconnection



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus

### Drug supply networks and organised crime



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Enforcement capacity and policing investment

Additional police resourcing and targeted operations are necessary to disrupt organised crime networks and protect communities.

**Flagship moves:**

- Increase police FTEs in Northland district proportional to need
- Establish dedicated organised crime taskforce for drug supply networks
- Invest in CCTV and patrol infrastructure in Kaitāia and Kaikohe

**Tensions:**

- Enforcement without prevention creates revolving-door criminal justice
- Māori overrepresentation in enforcement must be actively managed
- Fiscal cost of staffing remote stations is high per-capita

**Interventions on the system:**

- Increase police FTEs in Northland district proportional to need (state variable: `crime_pressure_index`, sign: +)


### Social prevention and early intervention

Addressing the social determinants of crime — deprivation, family instability, addiction — is more effective than enforcement alone.

**Flagship moves:**

- Fund whānau ora family support services in high-violence areas
- Expand drug treatment and harm reduction services in Northland
- Invest in youth employment and mentoring programmes

**Tensions:**

- Outcomes take years to materialise in crime statistics
- Requires sustained cross-agency coordination difficult to sustain
- Political pressure for immediate enforcement responses

**Interventions on the system:**

- Fund whānau ora family support services in high-violence areas (state variable: `crime_pressure_index`, sign: +)


---

## Claims cited on this page

- **Recorded crime in Northland includes family violence, drug-related offenses, and property crime. Police response in rural areas faces geographic delays; family violence notifications have increased 20-30% since 2015, reflecting stress from economic contraction and geographic isolation.** *(confidence: medium)* — Stats NZ Northland Regional Profile 2023.
- **Family violence victimisation rates in Northland (particularly Muriwhenua/Far** *(confidence: medium)* — Te Tai Tokerau Northland Health Profile 2023.

---

## Further reading


- **Stats NZ Northland Regional Profile 2023** — Statistics New Zealand (Stats NZ), 2023 — <https://www.stats.govt.nz/tools/2018-census-place-summaries/northland-region>

- **Te Tai Tokerau Northland Health Profile 2023** — Health New Zealand Te Whatu Ora (Health New Zealand), 2023 — <https://www.tewhatuora.govt.nz/for-health-professionals/data-and-statistics/nz-health-statistics/health-and-morbidity/>


---

## Technical notes

*State variables:* crime_pressure_index.

*Constraints:* fiscal_capacity.

*Inputs:* policy_intervention, external_shock.


*Feedback loops:*

- `Feedback: deteriorating family violence conditions reinforce systemic disadvantage.`


---

*Generated from `problem.northland.crime.family_violence` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
