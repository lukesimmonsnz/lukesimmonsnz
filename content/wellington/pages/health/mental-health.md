---
title: "Mental health crisis in Wellington"
section: health
subpage: mental-health
order: 2
updated: 2026-04-26
summary: >
  Wellington's mental health system is under severe strain: community mental health services have long waitlists, acute inpatient beds are routinely insufficient for demand, and workforce shortages are worsening. The crisis affects the full spectrum from mild anxiety and depression through to acute psychosis and suicidality.
status: draft
generated_from: problem.wellington.health.mental_health
---

# Mental health crisis in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Waitlist length

Community mental health services in Wellington consistently operate with waitlists of several months for non-urgent presentations, meaning individuals in sub-acute distress receive no support during the period most critical for early intervention (claim.wellington.health.mental_health_waitlist_length).


## Acute bed shortage

Wellington Regional Hospital's acute mental health inpatient unit regularly operates above capacity, with patients in acute crisis sometimes held in emergency department settings for extended periods waiting for an inpatient bed (claim.wellington.health.acute_bed_shortage).


---


## Drivers

The following structural drivers contribute to this problem.


### Acute mental health inpatient capacity ceiling



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus

### Community mental health service underinvestment



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Community Mental Health System Expansion

Investment in community mental health services and kaupapa Māori providers reduces acute crisis presentations and hospitalisations.

**Flagship moves:**

- Double community mental health worker capacity in Wellington region
- Kaupapa Māori mental health service expansion in Porirua and Hutt
- 24/7 community crisis response teams as alternative to police attendance

**Tensions:**

- Community mental health workforce pipeline is constrained by training and retention issues
- Community services require hospital backup; ring-fencing community investment is politically difficult

**Interventions on the system:**

- Fund 50 additional community mental health workers across Wellington region with Māori-led service options (state variable: `mental_health_ed_presentations`, sign: -)


### Mental Health Prevention and Early Intervention

Population-level mental health promotion and school-based early intervention can reduce incident rates before crisis services are needed.

**Flagship moves:**

- School-based wellbeing curriculum in all Wellington secondary schools
- Workforce wellbeing programme for high-stress sectors (health, emergency services)
- Social prescribing programme connecting GPs to community activities

**Tensions:**

- Prevention benefits accrue over long timeframes; political cycles favour acute response
- Wellbeing curriculum risks superficiality without adequate teacher training

**Interventions on the system:**

- Implement evidenced wellbeing curriculum (MindMatters) across 40 Wellington secondary schools (state variable: `youth_mental_health_prevalence`, sign: -)


---

## Claims cited on this page

- **Community mental health services in Wellington consistently operate with waitlists of several months for non-urgent presentations, meaning individuals in sub-acute psychological distress typically receive no support during the period most critical for early intervention.** — Health New Zealand Te Whatu Ora Wellington Region Annual Report 2022/23.
- **Wellington Regional Hospital's acute mental health inpatient unit regularly operates above capacity, with patients in acute crisis sometimes held in emergency department settings for extended periods awaiting an inpatient bed.** — Health New Zealand Te Whatu Ora Wellington Region Annual Report 2022/23.

---

## Further reading


- **Health New Zealand Te Whatu Ora Wellington Region Annual Report 2022/23** (Health New Zealand), 2023 — <https://www.tewhatuora.govt.nz/>


---

## Technical notes

*State variables:* community_mh_waitlist_length, acute_mh_bed_occupancy_rate.

*Constraints:* mh_workforce_supply, acute_bed_count.

*Inputs:* mh_service_investment, population_mental_health_burden.


*Feedback loops:*

- `Crisis escalation loop: inadequate community mental health support allows deterioration to acute levels; acute beds then fill with patients who would not have needed admission under better community support.`


---

*Generated from `problem.wellington.health.mental_health` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
