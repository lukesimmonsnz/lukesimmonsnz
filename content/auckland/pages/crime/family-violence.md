---
title: "Family Violence"
section: crime
subpage: family-violence
order: 2
updated: 2026-04-26
summary: >
  Auckland police receive approximately 150,000 family harm calls per year — roughly 40% of all police calls. Family violence is strongly correlated with housing stress and overcrowding. The intergenerational transmission cycle means that children exposed to violence have elevated risk of perpetrating or experiencing it as adults. System response is fragmented across police, social services, and housing agencies, with poor handoffs that leave victims in danger between contacts.

status: draft
generated_from: problem.auckland.crime.family_violence
---

# Family Violence

<p class="horizon-band">Analysis horizon: 10yr</p>



## Scale and concentration

One in three police calls in Auckland is a family harm event. This is not a niche social problem — it is the single largest category of police demand in New Zealand's largest city. The concentration in South and West Auckland reflects both the housing stress-violence link and the resource gap: suburbs with the highest call rates have the fewest support services per capita.


## The housing trap

Victims who want to leave cannot, because there is nowhere to go. Auckland's emergency refuge capacity is chronically below demand; transitional housing waitlists stretch months. The result is that safety planning by social workers is undermined by physical housing reality: victims return because return is the only viable short-run option.


---

## References



- **New Zealand Police Recorded Crime Statistics 2023**, 2023 — <https://www.police.govt.nz/about-us/publications-statistics/data-and-statistics/policedatanz/recorded-crime-offenders-sentenced>

- **Family Violence Data and Statistics 2023**, 2023 — <https://www.msd.govt.nz/about-msd-and-our-work/publications-resources/statistics/index.html>

- **New Zealand Crime and Victims Survey 2023**, 2023 — <https://www.justice.govt.nz/justice-sector-policy/research-data/nzcvs/>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Housing Stress and Overcrowding as Family Violence Amplifier



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus

#### System Underresponse and Victim Entrapment



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Integrated Family Violence Response and Safe Exits

Family violence requires a whole-system response: safe housing for victims as a first step, perpetrator accountability programmes, and child protection wraparound. Currently these are delivered by separate agencies with poor handoffs. Co-location of police, social workers, and housing navigators at family violence specialist units in South and West Auckland would close the gap between first call and sustained safety.

**Flagship moves:**

- Establish family violence specialist co-responder units (police + social worker) in the ten highest-call Auckland stations.
- Fund 200 emergency refuge spaces and 500 longer-term safe houses in Auckland for victim-with-children situations.
- Mandate perpetrator accountability programmes as a bail condition for all repeat family harm offenders.

**Tensions:**

- Safe housing provision for victims is expensive; without sustained investment in refuge capacity, victims return to dangerous situations because there is nowhere else to go.

- Co-responder models require police and social services to share information in real time; privacy frameworks create friction that slows response and risks gaps in victim safety plans.


**Interventions on the system:**

- Fund co-responder pairs (sworn officer + social worker) at all Auckland family harm high-call stations, operational 24 hours.
 (state variable: `fv_repeat_call_rate`, sign: -) (relaxes: `Gap between police attendance and social service follow-up`)
- Create a dedicated Auckland family violence safe housing pathway with 200 emergency and 500 transitional units, managed by a single agency with direct referral from police.
 (state variable: `victim_safe_exit_rate`, sign: +)


#### Perpetrator Accountability as Primary Lever

The most efficient way to reduce family violence is to change perpetrator behaviour, not to manage victim safety in perpetuity. Intensive perpetrator programmes (group cognitive-behavioural, culturally specific for Maori men) combined with electronic monitoring and swift breach consequences reduce recidivism more than victim-support investment alone. Victim safety resources should follow, not substitute for, perpetrator accountability.

**Flagship moves:**

- Mandate and fund perpetrator behaviour change programmes for all first-conviction family violence offenders.
- Deploy electronic monitoring (ankle bracelets) for all protection order holders with prior breaches.
- Develop kaupapa Maori perpetrator programmes with proven cultural safety and efficacy.

**Tensions:**

- Perpetrator programme availability in Auckland is insufficient for mandated participation; courts sentence to programmes that have 12-month waitlists, defeating deterrence.

- Electronic monitoring of perpetrators does not prevent physical proximity violations and may create false security for victims who assume monitored perpetrators will not breach.


**Interventions on the system:**

- Fund 10 additional perpetrator behaviour change programme cohorts in South and West Auckland annually, with Maori-specific delivery for Maori men.
 (state variable: `fv_repeat_call_rate`, sign: -) (relaxes: `Perpetrator programme waitlist and capacity deficit`)
- Legislate electronic monitoring as a mandatory bail condition for repeat protection order respondents with history of breach.
 (state variable: `protection_order_breach_rate`, sign: -)


### Claims cited on this page

- **New Zealand has one of the highest family violence police call rates in the OECD; Auckland police receive approximately 150,000 family harm calls per year (calls received by police, including calls not resulting in attendance), representing roughly 40% of all Auckland police calls. Attended family harm events are a subset of this figure; the majority of incidents involve repeat addresses, reflecting the chronic and cyclical nature of family violence.
** [value: 150000 family harm calls received/year (incl. unattended); 2022-2023] *(confidence: medium)* — New Zealand Police Recorded Crime Statistics 2023; Family Violence Data and Statistics 2023.
- **Children who witness family violence are at substantially elevated risk of becoming either perpetrators or victims of family violence as adults; the intergenerational transmission effect means that interventions which protect children from exposure have both immediate safety and long-run crime reduction value.
** — Family Violence Data and Statistics 2023.
- **Family violence rates in Auckland are positively correlated with housing stress; overcrowded households, insecure tenancies, and recent tenancy loss are associated with elevated family harm call rates, implicating housing instability as an amplifier of violence risk.
** *(confidence: medium)* — Family Violence Data and Statistics 2023; New Zealand Crime and Victims Survey 2023.

### Systems-model notes

*State variables:* fv_repeat_call_rate, victim_safe_exit_rate, protection_order_breach_rate, intergenerational_transmission_rate.

*Constraints:* Housing dependency: victim cannot leave without safe housing alternative, Programme waitlists: perpetrator programme capacity insufficient for mandated referrals, Agency fragmentation: police, MSD, housing, and child protection operate separate systems.

*Inputs:* co_responder_unit_coverage, refuge_capacity, perpetrator_programme_capacity, electronic_monitoring_coverage.


*Feedback loops:*

- `Repeat incidents at same address → escalating severity → eventual homicide or serious injury`
- `Children exposed → intergenerational transmission → next generation of perpetrators and victims`


</details>

---

*Generated from `problem.auckland.crime.family_violence` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
