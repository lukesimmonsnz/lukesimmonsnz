# Briefing v0 — Auckland Housing: Homelessness

**Status:** Draft for Luke's review. Not for publication. Figures marked `[verify]` need confirming before anything ships publicly.
**Last updated:** 2026-04-23
**Author:** Claude (drafted), Luke (editor)
**Frame:** 10 / 50 / 100-year structural analysis. Named politicians and present-day policy skirmishes are deliberately minimised.

---

## 1. Purpose and boundaries

Homelessness is the extreme tail of the Auckland housing outcome distribution. Land, Supply Economics, and Affordability describe the system and its aggregate ratios; this page is about the people for whom the system has failed most severely.

Boundaries with neighbouring subpages:

- **Affordability** covers the general outcome ratios and cohort distribution for the housed population.
- **Public Housing** covers state-landlord policy and the register that sits upstream of homelessness.
- **Māori Housing** covers kaupapa-Māori responses and mana-whenua-specific pathways.
- **Mental Health** (in the Health section, later) covers psychiatric comorbidity.

What belongs here: definitions, measurement of severe housing deprivation, the heterogeneous cohorts and pathways that produce and exit homelessness, the services system, and the interventions that act specifically on homelessness as an outcome.

---

## 2. Systems decomposition

```
State variables:   count_in_severe_housing_deprivation,
                   count_without_shelter (rough sleeping, cars, tents),
                   count_in_temporary_accommodation (motels, emergency, transitional),
                   count_in_overcrowded_housing,
                   public_housing_register_size,
                   flow_into_homelessness_per_year,
                   flow_out_of_homelessness_per_year,
                   average_length_of_stay_in_emergency_accommodation,
                   recurrence_rate_after_exit

Inputs:            affordability_outcome (from Affordability page),
                   public_and_community_housing_supply (from Public Housing),
                   mental_health_service_capacity,
                   addiction_service_capacity,
                   family_violence_service_capacity,
                   transitions_from_care_prison_hospital,
                   economic_conditions (employment, real wages),
                   rental_market_conditions,
                   emergency_accommodation_funding_and_places

Constraints:       fiscal_capacity_for_services,
                   workforce_capacity_in_homelessness_sector,
                   political_acceptability_of_visible_rough_sleeping,
                   legal_frameworks (tenancy, mental_health_act, care_transitions),
                   data_system_completeness

Feedback loops:
  - prolonged_homelessness -> health_deterioration -> harder_to_exit
    (hysteresis; people who are homeless for longer become harder to
    house)
  - emergency_accommodation_at_motels -> pipeline_dependence ->
    normalisation_of_motel_as_housing (perverse long-run dynamic)
  - housing_first_placements -> stable_housing -> reduced_emergency_service_use
    (long-run negative cost loop — well-evidenced internationally)
  - affordability_deterioration -> rising_inflow -> service_capacity_breach
    -> longer_stays -> lower_throughput (the system backs up)
  - stigma_and_criminalisation -> reduced_help_seeking -> later_presentation
    -> more_expensive_response (the visible-enforcement loop)
```

Homelessness behaves differently from affordability: it is a **stock-and-flow** problem at the tail, not a ratio problem for the middle. The right questions are about flows in, flows out, lengths of stay, and recurrence — not about averages.

---

## 3. Definitions and measurement

Homelessness is not one thing. The usable definitions operate at different scopes, and mixing them produces incoherent policy.

**Severe housing deprivation** — the Stats NZ / Amore framework used in New Zealand since roughly 2015. Four categories:

1. **Without shelter** — rough sleeping, improvised dwellings, cars, tents.
2. **Temporary accommodation** — motels, emergency and transitional housing, women's refuges.
3. **Sharing severely** — staying with others in overcrowded conditions because there is nowhere else.
4. (Some frameworks add:) **Uninhabitable housing** — technically housed but in conditions unfit for habitation.

The Census produces a point-in-time estimate against this framework. **Flow data** — how many enter and leave homelessness each year — is weaker and depends on administrative sources (public housing register, emergency accommodation grants, social agency records).

**ETHOS (European Typology of Homelessness and Housing Exclusion)** is the international reference. Broadly compatible with the NZ framework. The OECD and Eurostat publish cross-country comparisons on this basis.

**Rough sleeping** — the narrowest, most visible definition — is politically over-weighted relative to its share of total severe housing deprivation. It is typically under 10% of the severe deprivation count and is what most policy-makers and media focus on. A defensible public page names this asymmetry.

**The bottom line for measurement:** whatever count you use, declare it. Different numbers mean different things, and mixing them invites misleading comparisons.

---

## 4. Auckland scale and history

- The 2023 Census counted roughly five thousand people in severe housing deprivation in the Auckland region on the night of the count. `[verify: 2023 Census severe housing deprivation release]`
- The public housing register — households waiting for state or community housing — grew from roughly five thousand to roughly twenty-five thousand nationally between 2015 and 2023, with Auckland carrying a large share. `[verify: MSD / HUD register series]`
- Emergency accommodation (mostly motels) scaled rapidly from 2017, peaked in 2022-23, and has been wound down since. The net effect on underlying need is contested; the *register* shrank faster than the underlying inflow slowed.
- Rough sleeping counts in Auckland's city centre have fluctuated with services capacity and enforcement posture. Long-run trend is up since the 1990s.
- Housing First programmes have been operating in Auckland since 2017 (Auckland City Mission, People's Project), with published outcomes that are broadly favourable on retention and cost-offset measures.

Long-run direction of travel: severe housing deprivation has grown faster than the Auckland population since the early 2000s. On a 100-year view the key question is whether this is a secular trend or a deep cycle.

---

## 5. Cohorts and pathways

Homelessness is not one population; it is several overlapping populations with distinct causes, service needs, and pathways. This is the single most important structural observation for policy design.

**Chronic rough sleeping.** Small in absolute number; high in service cost; typically complex needs including mental health, addiction, and disability. The population Housing First is most clearly evidenced to help.

**Families in temporary accommodation.** The large share of the Auckland count, especially since 2017. Drivers are economic — rental unaffordability, relationship breakdown, income loss. Children are substantially over-represented in the Auckland homelessness count.

**Youth and transitions from state care.** A predictable pathway: young people ageing out of care, youth justice, or unstable family situations. Internationally one of the most preventable inflows.

**Women and children escaping family violence.** A distinct service pathway with its own legal and service architecture (refuges, protection orders).

**Severely overcrowded sharers.** The largest category by headcount in NZ measurement — households staying with others because they have nowhere else. Less visible, sometimes disputed as "real" homelessness, but carries serious health and wellbeing consequences.

**Transitions from prison, hospital, mental-health inpatient units.** Discharge without stable housing is a predictable driver of entries into homelessness. Fixable at the system-design level.

**Working poor.** A growing category: households with employment income that is nonetheless insufficient for Auckland rents. Their homelessness looks different — often in cars or couch-surfing while maintaining work — and is less visible to enforcement-centric frames.

A policy response that treats all of these as a single population will underperform. A public page that presents them as distinct cohorts with distinct pathways is the more honest frame.

---

## 6. International comparators

Three archetypes of national homelessness response worth comparing.

**Finland — Housing First at national scale.** Finland adopted Housing First as the national homelessness strategy, systematically replaced emergency shelters with permanent housing, and reduced long-term homelessness by around 70% between 2008 and the early 2020s. The clearest evidence worldwide that Housing First works at scale when backed by housing supply and sustained political commitment.

**United States — Continuum of Care.** Federal funding channelled through local Continuums of Care that coordinate shelters, transitional housing, and permanent supportive housing. Mixed record: reductions in chronic homelessness in some metros; sustained or worsening overall counts in high-cost cities (Los Angeles, Seattle, San Francisco). Demonstrates that services without housing supply is insufficient.

**United Kingdom — duty and prevention.** Statutory duty on local authorities to prevent and relieve homelessness for certain cohorts, with the Homelessness Reduction Act (2017) shifting the system upstream toward prevention. Reduced presentations in some metrics; did not resolve the underlying housing-supply problem.

**Australia — state-by-state Housing First adoption.** Mixed, federalist pattern. Melbourne and Brisbane-led Housing First expansion; varied state-level coordination. Useful comparator because of structural similarity to New Zealand.

**Japan.** Low rough-sleeping counts despite urban density, achieved through very different mechanisms (family and corporate obligation, distinctive housing stock). Outside the Anglo-European frame but worth naming.

The engineering observation: countries that made the largest dents in long-term homelessness did so by combining Housing First with sufficient non-market housing supply. Neither is sufficient alone.

---

## 7. Durable features

Features of the Auckland homelessness system that will still be recognisable in 2076 or 2126.

1. **Heterogeneity.** Homelessness is not one population; any durable response addresses cohorts distinctly.
2. **Tail of the housing distribution.** Homelessness rises and falls with broader housing-system tightness, so structural solutions sit upstream in Affordability and Supply Economics.
3. **Hysteresis.** People homeless for longer become harder to house. Length-of-stay is a first-class outcome variable.
4. **Predictable pathways in.** Transitions from care, prison, hospital, psychiatric units, and family violence are patterned and partially preventable.
5. **Motel accommodation is expensive and ineffective.** Emergency accommodation at motels has higher per-household cost than most permanent-housing alternatives and produces worse outcomes.
6. **Wraparound services matter for the complex tail.** For chronic rough sleeping, housing alone is rarely enough; paired services determine whether tenancies hold.
7. **Data systems are chronically incomplete.** Severe housing deprivation is measured once every five years at Census; flow data is administrative and partial.
8. **Visibility and politics diverge.** Rough sleeping is politically over-weighted relative to its share of the count; sharers and motel-resident families are politically under-weighted.
9. **The homelessness sector workforce is small and precarious.** Capacity is a bottleneck independent of funding level.
10. **Prevention is cheaper than response, but harder to fund.** Because preventive spending produces "events that did not happen", it competes poorly for political and fiscal attention.

---

## 8. The durable long-run questions

- What is the realistic long-run target for Auckland — zero homelessness, functional zero (defined counted-down stability), or bounded acceptability?
- How much of the response should be housing-led (Housing First) versus services-led (staircase, transitional)?
- Where does the balance between prevention (upstream) and response (downstream) sit?
- How should flows from care, prison, and hospital be re-engineered so that discharge without housing stops happening?
- What data and governance system is needed to run this as a real system, rather than a collection of programmes?
- How should the housing response to rough sleeping relate to the enforcement response (public-space rules, trespass, move-on notices)?
- What share of the homelessness response should be delivered by the state, community housing providers, iwi, and faith-based providers on a 50-year horizon?

---

## 9. Solution camps (neutral presentation)

Five camps drafted, each addressing a different binding constraint. I have included the enforcement camp because it is a real international position even where it is not a popular one — excluding it would misrepresent the actual debate.

### A. Housing First
**Core claim:** permanent housing is the precondition for recovery, not the reward for it. Place chronically homeless people into stable tenancies with wraparound services; do not require sobriety, service engagement, or "housing readiness".
**Flagship moves:** scale Housing First programme places, secure long-term funding, supply of suitable permanent housing via state and community providers, paired support services.
**Tensions:** requires sufficient non-market housing supply to land people in; up-front service cost offset only over years; politically difficult to fund preventive spending against visible crises.

### B. Prevention-focused intervention
**Core claim:** the cheapest homelessness intervention is the one that stops someone becoming homeless. Prevent predictable inflows — from care transitions, hospital discharge, family violence, income shocks, rent arrears — through targeted support.
**Flagship moves:** statutory duty to prevent, transitions programmes from state care and prison, family-violence housing response, rent-arrears assistance, youth housing pathways.
**Tensions:** diffuse benefits are politically harder to claim than visible response; requires long-term, cross-agency commitment; hard to counterfactually prove.

### C. Wraparound service integration
**Core claim:** for the complex tail (chronic rough sleeping, mental health, addiction) housing alone is insufficient. The limiting factor is coordinated mental-health, addiction, health, and employment services wrapped around housing tenancies.
**Flagship moves:** integrated multi-agency teams, co-located services, single-case-manager models, stable community-health capacity.
**Tensions:** cross-sector coordination is administratively difficult; mental-health and addiction services are themselves under-resourced; does not address the housing-supply constraint.

### D. Scale public and community housing as exits
**Core claim:** homelessness sits at the bottom of a system that does not have enough housing people can actually afford to live in. The durable fix is a larger non-market housing sector — state, community housing providers, iwi — delivering at the scale that emergency responses cannot.
**Flagship moves:** Kāinga Ora build expansion with a proportion committed to homelessness exits, community housing provider scale-up, funding pipelines for iwi-led housing as exit vectors.
**Tensions:** fiscal cost, build time, cross-referred to Public Housing and Supply Economics subpages; slow to show results.

### E. Enforcement and public-order response
**Core claim:** visible rough sleeping produces real harms (safety, hygiene, amenity, commerce) that a civic response must acknowledge. Use move-on powers, public-space rules, and outreach tied to shelter capacity to manage the visible manifestation.
**Flagship moves:** public-space restrictions, police-outreach pairings, tied-shelter-access policies, rough-sleeping reduction targets.
**Tensions:** contested international evidence on effectiveness; displaces rather than solves; can criminalise a health condition; conflicts with Housing First evidence base; can increase downstream costs through justice-system contact.

In practice, serious homelessness strategies combine A, B, C, and D; E appears in most real systems at some level, and the question is typically its weight rather than its presence. The public page should show the full five and let the reader assess the balance.

---

## 10. Conflict-of-interest flag

The conflict surface for Homelessness is **minimal**. Your disclosed land holdings and conservation preferences do not align directly with any of the five camps. Camp D (scale public and community housing as exits) intersects tangentially with your broader devolution and institutional-reform views but only at the Council-Crown fiscal-architecture layer, which is the Land and Public Housing subpages' job to carry.

No additional precaution required beyond the usual neutral-camps default.

---

## 11. Sources to spot-check

Primary:
- **Stats NZ** — 2023 Census severe housing deprivation; earlier Amore-framework series.
- **MSD and HUD** — public housing register, emergency housing grants, housing-support system.
- **Kāinga Ora** — tenancy and placement data.
- **Local providers** — Auckland City Mission, Lifewise, VisionWest, Salvation Army NZ (state of the nation reports).

Analytic:
- **Kate Amore** (University of Otago / He Kāinga Oranga) — the primary NZ homelessness measurement research programme.
- **The Salvation Army New Zealand** — annual State of the Nation report series.
- **The Helen Clark Foundation** — periodic homelessness and housing-inclusion reports.

International:
- **OECD / Eurostat** — cross-country homelessness indicators.
- **Finnish Y-Foundation** — canonical source on Finland's Housing First programme.
- **US HUD Annual Homeless Assessment Report (AHAR).**
- **UK Ministry of Housing, Communities and Local Government** — rough sleeping and statutory homelessness statistics.
- **Australian Institute of Health and Welfare** — Specialist Homelessness Services data.

---

## 12. Open questions for you

1. **Scope of the cohorts section.** My default (§5) lists seven cohort / pathway types. Keep all, or consolidate to five headline categories?
2. **Enforcement camp (§9E).** Include and balance (my default), or exclude on the grounds that it is an enforcement rather than a housing response?
3. **Housing First as the house-evidenced default.** Internationally Housing First has the strongest evidence base. Do you want the page to say that explicitly (empirical claim) while still presenting camps neutrally (value claim), or do you want even the evidence framing softened to let the reader decide?
4. **Five camps or fewer.** I have five (A–E). Natural further consolidation would merge C (wraparound) and A (Housing First) into a single "housing-plus-services" camp. Your preference?
5. **Charts.** My default five: (a) severe housing deprivation count over time, (b) public housing register over time, (c) emergency accommodation nights or cost, (d) pathway flows into homelessness (sankey-style), (e) international rough-sleeping per-capita comparison. Pick any subset.
6. **Tone on the enforcement camp.** NZ has swung between different postures over decades. Do you want the enforcement camp written crisper (stronger critique of its evidence base) or left as drafted?

Once you've answered I will extract entities, lint, render, and the page will be live at `/research/auckland/housing/homelessness/`.
