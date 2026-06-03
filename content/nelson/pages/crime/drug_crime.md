---
title: "Methamphetamine supply driving acquisitive crime"
section: crime
subpage: drug_crime
order: 4
updated: 2026-04-26
summary: >
  Drug-related offending in Nelson rose around 18 percent between 2019 and 2023, with methamphetamine and synthetic-opioid availability now the primary driver of acquisitive crime. About 340 drug offences were recorded in 2023, with synthetic drugs comprising roughly 62 percent of seizures.
status: draft
generated_from: problem.nelson.crime.drug_crime
---

# Methamphetamine supply driving acquisitive crime

<p class="horizon-band">Analysis horizon: 10yr</p>



## Supply, demand, and downstream offending

Methamphetamine is now reliably available across Nelson, with retail networks active in outer suburbs and rural fringe (claim.nelson.crime.drug_crime_claim). Police, ED, and corrections data all point to a substantial and growing share of property offending and family-violence escalation linked to dependence.


## Treatment capacity vs supply intensity

Specialist addiction treatment in Nelson-Tasman is configured for moderate caseloads and has long waiting lists. The capacity gap between supply intensity and treatment throughput pushes more cases into the criminal-justice and emergency-health systems instead, where unit costs are far higher and rehabilitation outcomes weaker.


---


## Drivers

The following structural drivers contribute to this problem.


### Methamphetamine supply network and treatment-capacity gap



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing crime challenges.

**Flagship moves:**

- Implement evidence-based crime policy in Nelson
- Increase investment in crime services and infrastructure
- Build cross-sector partnerships to address crime challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for crime (state variable: `crime_outcome_index`, sign: +)
- Secondary intervention for crime (state variable: `crime_service_access`, sign: +)


---

## Claims cited on this page

- **Drug-related offending in Nelson has increased 18% 2019-2023, with methamphetamine availability and use becoming the primary driver of acquisitive crime. NZ Police data shows 340+ drug-related offences recorded in Nelson district in 2023, with synthetic drugs (methamphetamine, fentanyl derivatives) comprising 62% of seizures. Retail supply networks are increasingly active in outer suburbs.** [value: 18 percent increase in drug offences 2019-2023; 2019-2023] — New Zealand Police Crime Statistics 2023.

---

## Further reading


- **New Zealand Police Crime Statistics 2023** — New Zealand Police (New Zealand Police), 2023 — <https://www.police.govt.nz/about-us/publication/crime-statistics>


---

## Technical notes

*State variables:* drug_offences_per_year, meth_seizure_grams_per_year, addiction_treatment_waitlist.

*Constraints:* specialist_clinician_workforce, border_interdiction_capacity.

*Inputs:* national_supply_pressure, treatment_funding.


*Feedback loops:*

- `Supply-treatment feedback: rising supply pulls more users into dependence faster than treatment slots open, expanding the dependent population and the acquisitive-crime base.`


---

*Generated from `problem.nelson.crime.drug_crime` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
