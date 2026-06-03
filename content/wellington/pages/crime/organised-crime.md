---
title: "Gang activity and drug markets in Wellington"
section: crime
subpage: organised-crime
order: 4
updated: 2026-04-26
summary: >
  Wellington has an established gang presence centred in Porirua, with spillover into Hutt Valley. Gang-organised drug markets — methamphetamine in particular — are linked to both supply-side violence and demand-side property crime across the wider Wellington region.
status: draft
generated_from: problem.wellington.crime.organised_crime
---

# Gang activity and drug markets in Wellington

<p class="horizon-band">Analysis horizon: 10yr</p>



## Gang presence in Porirua

Wellington's gang landscape includes established chapters of major New Zealand gangs concentrated in Porirua. These organisations control significant components of the local drug market and provide income and social identity in communities with limited economic alternatives (claim.wellington.crime.gang_presence_porirua).


## Drug market and deprivation nexus

Wellington research links drug market activity most strongly to areas of concentrated deprivation, where limited legitimate economic opportunity and high social need create conditions for drug use and supply (claim.wellington.crime.drug_market_deprivation_link).


---


## Drivers

The following structural drivers contribute to this problem.


### Concentrated deprivation and crime environment



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus

### Limited legitimate economic alternatives in Porirua



- **Category:** economic
- **Timescale:** long
- **Consensus:** mostly-agreed

### Substance use and family violence co-occurrence



- **Category:** cultural
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Drug Harm Reduction and Treatment

Treating drug dependency as a health issue rather than a criminal one reduces organised crime revenue and reduces harm to users.

**Flagship moves:**

- Drug checking services at Wellington venues and events
- Opioid substitution therapy access without waitlists
- Decriminalise personal-use possession and redirect enforcement to supply

**Tensions:**

- Decriminalisation may face strong political opposition nationally
- Treatment availability is constrained by workforce shortage in addiction medicine

**Interventions on the system:**

- Fund drug checking services and opioid substitution therapy expansion in Wellington, reducing demand-side organised crime revenue (state variable: `drug_related_harm_index`, sign: -)


### Organised Crime Financial Disruption

Targeting the financial infrastructure of organised crime groups is more effective than arrest-focused enforcement.

**Flagship moves:**

- Anti-money laundering audits of Wellington-based cash-intensive businesses
- Proceeds of crime recovery programme targeting property assets
- Cross-agency financial intelligence unit co-located with police

**Tensions:**

- Financial disruption requires significant intelligence and legal resource
- Displacement of organised crime to less-scrutinised jurisdictions is a real risk

**Interventions on the system:**

- Expand Police Financial Intelligence Unit capacity in Wellington with dedicated AML liaison (state variable: `organised_crime_revenue`, sign: -)


---

## Claims cited on this page

- **Wellington's gang landscape includes established chapters of major New Zealand gangs concentrated in Porirua; these organisations control significant components of the local methamphetamine market and provide social identity and income in communities with limited economic alternatives.** *(confidence: medium)* — New Zealand Police Crime Statistics 2022/23: Wellington District.
- **Drug market activity in Wellington is most strongly associated with areas of concentrated deprivation, where limited legitimate economic opportunity and high social need create conditions for both drug supply and demand.** *(confidence: medium)* — New Zealand Police Crime Statistics 2022/23: Wellington District; New Zealand Deprivation Index 2018 (NZDep2018).

---

## Further reading


- **New Zealand Police Crime Statistics 2022/23: Wellington District** (New Zealand Police), 2023 — <https://www.police.govt.nz/about-us/publications-statistics/data-and-statistics/policedatanz/victimisation-timeseries>

- **New Zealand Deprivation Index 2018 (NZDep2018)** — Atkinson J, Salmond C, Crampton P (University of Otago / Ministry of Health), 2019 — <https://www.otago.ac.nz/wellington/departments/publichealth/research/hirp/otago020194.html>


---

## Technical notes

*State variables:* gang_membership_estimate, methamphetamine_market_size.

*Constraints:* economic_alternatives_to_gang_income, prison_cycle_gang_recruitment.

*Inputs:* deprivation_level, policing_enforcement_intensity.


*Feedback loops:*

- `Prison recruitment loop: incarceration increases gang affiliation; reentry into high-deprivation communities without employment support sustains gang membership.`


---

*Generated from `problem.wellington.crime.organised_crime` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
