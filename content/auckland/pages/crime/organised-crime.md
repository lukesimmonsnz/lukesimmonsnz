---
title: "Organised Crime and Gang Activity"
section: crime
subpage: organised-crime
order: 3
updated: 2026-04-26
summary: >
  Auckland is the primary hub of New Zealand organised crime, with gang structures in South Auckland controlling retail drug distribution. Methamphetamine is the primary revenue source; its harms (family violence, child neglect, acquisitive crime) are concentrated in high-deprivation communities. Suppression-only enforcement has not reduced gang membership or drug availability; the debate centres on whether harm reduction and exit pathways or supply disruption and gang legislation is the more effective primary lever.

status: draft
generated_from: problem.auckland.crime.organised_crime
---

# Organised Crime and Gang Activity

<p class="horizon-band">Analysis horizon: 10yr</p>



## The economic structure of organised crime

Auckland gangs are not primarily ideological organisations; they are enterprises operating in a prohibited market. Drug prohibition creates the price premium that makes the business viable; the territorial enforcement that produces violence is a substitute for contract law in an illegal industry. Understanding organised crime as a market structure rather than a moral failure suggests that enforcement targeting supply is less effective than demand reduction and revenue base disruption.


## Community harm concentration

The communities most harmed by organised crime are also the communities most harmed by the poverty that fuels gang recruitment. Methamphetamine harms are not distributed across Auckland; they fall on children in overcrowded South and West Auckland households. Any effective response has to address both the supply side and the conditions that make drug use prevalent.


---

## References



- **New Zealand Police Organised Crime Threat Assessment 2023**, 2023 — <https://www.police.govt.nz/about-us/publications-statistics/strategic-assessments>

- **New Zealand Crime and Victims Survey 2023**, 2023 — <https://www.justice.govt.nz/justice-sector-policy/research-data/nzcvs/>

- **Family Violence Data and Statistics 2023**, 2023 — <https://www.msd.govt.nz/about-msd-and-our-work/publications-resources/statistics/index.html>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Deprivation and Gang Recruitment Pipeline



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus

#### Illicit Drug Market as Organised Crime Anchor



- **Category:** regulatory
- **Timescale:** long
- **Consensus:** contested


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Harm Reduction, Drug Reform, and Gang Exit Pathways

Organised crime in Auckland is sustained by drug prohibition and deprivation; enforcement cannot disrupt an industry with this level of demand and margin. Reducing harm requires treating drug use as a health issue, investing in gang exit programmes, and addressing the economic conditions that make gang membership rational. Drug law reform would shift revenue from organised crime to regulated businesses while reducing criminal justice costs.

**Flagship moves:**

- Expand residential and community drug treatment capacity in South and West Auckland by 50%.
- Fund gang exit programmes with employment and housing support as off-ramps from organised crime.
- Commission independent review of drug scheduling and consider decriminalisation of personal possession.

**Tensions:**

- Drug law reform is politically constrained; incremental harm reduction measures (treatment, naloxone, needle exchanges) are more achievable but do not address the supply-side organised crime revenue base.

- Gang exit programmes require sustained multi-year investment; the same gang member may access an exit programme and return to gang activity multiple times before leaving permanently.


**Interventions on the system:**

- Fund 400 additional residential drug treatment places in Auckland with priority access for methamphetamine-dependent parents with children in care.
 (state variable: `meth_harm_index`, sign: -) (relaxes: `Treatment capacity gap in South and West Auckland`)
- Establish a dedicated Auckland gang exit programme with employment partners, housing guarantee, and 2-year case management for 50 participants per year.
 (state variable: `gang_membership_rate`, sign: -)


#### Organised Crime Suppression and Gang Legislation

Organised crime requires direct law enforcement suppression: targeting the financial flows of gang enterprises, prosecuting leadership, and using gang-specific legislation to disrupt organisational capacity. Harm reduction without supply disruption allows organised crime to continue extracting revenue from communities; enforcement creates the conditions in which exit programmes can work.

**Flagship moves:**

- Expand financial crime enforcement targeting gang asset accumulation and money laundering in Auckland.
- Use gang association legislation to constrain public gang activity and recruitment.
- Increase Border Force and Customs intelligence capacity to intercept drug precursors.

**Tensions:**

- Gang association legislation raises civil liberties concerns; broad provisions risk criminalising association rather than proven criminal activity, with disproportionate impact on Maori communities.

- Supply-side drug enforcement has not reduced drug availability or price in New Zealand despite decades of effort; seizures are replaced by new supply chains rapidly.


**Interventions on the system:**

- Fund an Auckland-based organised crime financial intelligence unit with Police, Inland Revenue, and FENZ coordination to target gang-linked property and business assets.
 (state variable: `gang_asset_value`, sign: -)
- Increase Border Force staffing at Auckland Airport and Port of Auckland for drug and precursor interception.
 (state variable: `drug_market_supply_index`, sign: -)


### Claims cited on this page

- **Auckland is the primary entry point and distribution hub for methamphetamine and other illicit drugs in New Zealand; organised crime groups operating in South Auckland control the majority of retail drug distribution, using gang structures to manage territory and enforce contracts in the absence of legal enforcement mechanisms.
** *(confidence: medium)* — New Zealand Police Organised Crime Threat Assessment 2023.
- **Gang membership in Auckland is heavily concentrated in high-deprivation areas; gangs provide economic opportunity, social belonging, and protection in contexts where legitimate alternatives are scarce. Suppression-only approaches historically increase gang cohesion rather than reduce membership.
** *(confidence: medium)* — New Zealand Police Organised Crime Threat Assessment 2023; New Zealand Crime and Victims Survey 2023.
- **Methamphetamine use is disproportionately concentrated in high-deprivation Auckland communities; meth-related harm (family violence, child neglect, acquisitive crime) imposes costs borne primarily by those communities, not by users alone. Treatment capacity in South and West Auckland is substantially below assessed need.
** *(confidence: medium)* — New Zealand Police Organised Crime Threat Assessment 2023; Family Violence Data and Statistics 2023.

### Systems-model notes

*State variables:* gang_membership_rate, meth_harm_index, drug_market_supply_index, gang_asset_value.

*Constraints:* Prohibition rents: drug illegality creates high margins that sustain organised crime, Recruitment pipeline: deprivation and school disengagement sustain gang membership supply, Political constraint: drug law reform faces public opposition despite evidence base.

*Inputs:* drug_treatment_capacity, gang_exit_programme_places, financial_crime_enforcement, border_interception_rate.


*Feedback loops:*

- `Gang revenue → community investment → local legitimacy → easier recruitment`
- `Meth harm → child neglect → intergenerational disadvantage → next generation recruitment`


</details>

---

*Generated from `problem.auckland.crime.organised_crime` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
