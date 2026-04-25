# Briefing v0 — Auckland Housing: Affordability

**Status:** Draft for Luke's review. Not for publication. Figures marked `[verify]` need confirming before anything ships publicly.
**Last updated:** 2026-04-23
**Author:** Claude (drafted), Luke (editor)
**Frame:** 10 / 50 / 100-year structural analysis. Named politicians and present-day policy skirmishes are deliberately minimised.

---

## 1. Purpose and boundaries

Land is the stock. Supply Economics is the flow. **Affordability** is the *outcome*: what Aucklanders actually pay for housing, how that relates to what they earn, and who bears the cost when the outcome is poor.

This subpage is about the measurement side, the distribution, and the specific interventions aimed at the outcome rather than the stock or flow. The boundary with neighbouring subpages:

- Land-supply fixes (Compact city, Greenfield, etc.) live in **Land**.
- Production-side fixes (prefab, scale, infrastructure) live in **Supply Economics**.
- State landlord policy lives in **Public Housing** (a dedicated subpage).
- Māori-housing pathways live in **Māori Housing** (a dedicated subpage).
- Tax instruments on land and capital live in **Tax Reform**.
- The lowest-tail outcome — severe deprivation, homelessness — lives in **Homelessness**.

What's left for this page: measurement, distributional incidence, and the demand-side / outcome-level interventions (transfers, rent regulation, first-home pathways, inclusionary zoning, BTR institutional landlord, wages).

---

## 2. Systems decomposition

```
State variables:   median_dwelling_price, median_rent, median_household_income,
                   price_to_income_ratio, rent_to_income_ratio,
                   residual_income_after_housing, housing_cost_burden_share,
                   homeownership_rate_by_cohort, deposit_gap_years,
                   severe_housing_deprivation_count, tenure_mix

Inputs:            supply_rate (from Supply Economics), land_prices (from Land),
                   wage_growth, interest_rates, tax_settings, transfer_settings,
                   migration, demographics (household_formation_rate)

Constraints:       fiscal_capacity_for_transfers, political_acceptability
                   of_rent_regulation, market_willingness_to_supply
                   affordable_product, labour_market_equilibrium

Feedback loops:
  - prices -> investor_demand -> prices (speculative feedback at market level)
  - high_price_to_income -> delayed_household_formation -> lower_household_count
    -> weaker_demand -> ? (mitigating, but on long lag and at the cost of
    quality-of-life outcomes)
  - homeownership_rate -> political_constituency_for_prices -> policy
    stickiness (important 50-year dynamic — owners vote, and a falling
    ownership rate changes the politics of affordability)
  - rent_regulation -> private_landlord_exit -> reduced_rental_supply ->
    rents (contested; evidence mixed across international cases)
  - income_transfers -> landlord_capture -> rents (partial; magnitude
    depends on supply elasticity)
```

Affordability is fundamentally a **ratio problem**, not a level problem. It is the relationship between *what housing costs* and *what households earn*, not either in isolation.

---

## 3. The metrics — measurement is the first engineering choice

Affordability is not one number. It is a family of related measures, each with different policy implications. A public page has to name which measure it is using, because conclusions differ between them.

**Price-to-income ratio (PTI).** Median dwelling price divided by median household income. The Demographia methodology uses ≥5.1 as "severely unaffordable"; Auckland has sat in the 8–10× range for most of the last decade. Simple, widely used, but misleading as a single indicator because it ignores interest rates, deposit requirements, and the option to rent.

**Rent-to-income ratio.** Median weekly rent divided by median weekly household income. For the lower-income quartile, 30% is a standard "cost burden" threshold; 50% is "severe cost burden". The rent-to-income ratio is the more decision-relevant metric for the ~35% of Auckland households who rent. `[verify: MBIE tenancy bond / Stats NZ income data]`

**Residual income approach.** After paying for housing, does the household have enough left to live on (food, transport, utilities, healthcare, essentials)? Academic housing economists (Stone, Kutty) argue this is the most defensible measure — ratios miss that a high-income household paying 40% of income on housing may be less stressed than a low-income one paying 25%.

**Deposit gap.** Years of median savings required to assemble a typical deposit. A PTI of 8 at a 20% deposit implies saving ~1.6× annual income — many years even for disciplined savers. This metric captures what has changed most over 30 years: the *entry barrier* to ownership, rather than the running cost of owning.

**Homeownership rate by cohort.** What share of people aged 25–34 own their home today, compared to the same cohort in 1986, 1996, 2006? Auckland homeownership in the under-35 cohort has fallen steeply over 30 years. On a 100-year view, this is probably the most consequential metric.

**Severe housing deprivation.** Living without shelter, in temporary accommodation, or severely crowded. The extreme tail of the distribution. Covered in depth on the Homelessness subpage.

**Affordability vs. "choice" affordability.** Even where average affordability is poor, the well-off can still choose from an affordable price point. For the bottom quartile there is typically *no* affordable choice in the market without transfers. "Affordability" without income specification is an incomplete question.

---

## 4. Historical arc in Auckland

Without exhaustive numbers (verify against primary sources before publication), the direction of travel over the last 40 years is:

- **Prices** rose roughly fivefold in real terms 1985–2022, then fell modestly and are in shallow recovery. Auckland-specific premium over the rest of NZ rose from ~1.2× to ~1.6×.
- **Real wages** roughly doubled over the same period.
- **Price-to-income ratio** therefore rose from roughly 3–4× in the mid-1980s to roughly 8–10× at peak, with partial recent correction.
- **Rents** rose roughly threefold in nominal terms post-2000, with ~25% of the rise concentrated in 2020–23.
- **Homeownership rate** among under-40s fell from ~60% in 1986 to ~40% in the mid-2020s.
- **Deposit gap** expanded from roughly 2–3 years of median saving in the 1990s to roughly 8–12 years at peak in the early 2020s.

These are the long-run facts, and they are what a reader in 2076 will want framed. The year-to-year political fight over whether prices are up 2% or down 3% is noise.

---

## 5. Who bears the affordability problem

Affordability is distributional. The aggregate ratios mask large differences between cohorts, tenures, and populations.

**By generation.** The 30-year decline in young-adult homeownership is the single clearest distributional story. A 30-year-old in 1990 could plausibly buy; a 30-year-old in 2025 typically cannot, without parental or inherited capital. The gap between those who can draw on intergenerational wealth and those who cannot is widening structurally.

**By tenure.** Renters pay more per square metre than owner-occupiers on equivalent properties, receive weaker legal protections, and build no equity. The policy literature on tenure equity is substantial; the political weight given to it historically small.

**By ethnicity.** Māori and Pasifika homeownership rates are materially lower than Pākehā rates across every age cohort, and the gap has widened rather than narrowed. The causes are partly historical (Crown dispossession, see Land), partly contemporary (income, credit, location). The interventions that address this live largely on the Māori Housing subpage.

**By geography within Auckland.** Affordability stress is concentrated in South Auckland and parts of West Auckland, because rents there are not low enough relative to the incomes of the households who live there.

**By household composition.** Single-parent households and older single renters face the worst affordability stress on residual-income measures.

A defensible public page treats this distributional material as first-class, not as a footnote.

---

## 6. Drivers specific to affordability

The Land page named geography, title, and regulation as durable drivers. Supply Economics named cyclicality, productivity, infrastructure, and finance. The drivers that belong specifically on the Affordability page — because they operate at the outcome level rather than on stock or flow — are:

**Wage-to-price decoupling.** Auckland wages have grown, but slower than prices or rents. The ratio is the outcome; the growth-rate differential is the driver.

**Credit expansion.** Household credit availability — macroprudential rules, bank lending practices, interest rates — has a larger short-run effect on affordability than supply changes. The 2021 low-rate credit surge pushed prices up more than the subsequent construction boom pushed them down.

**Tax treatment of housing asset.** The absence of a comprehensive CGT, the treatment of owner-occupier gains, and the effective tax-free status of imputed rent together mean housing is tax-advantaged relative to other assets. This is a compounding driver over 50 years.

**Intergenerational wealth transfer.** Parental assistance and inheritance are now structural features of first-home buying. The gap between heirs and non-heirs is a driver of the distributional pattern and will grow as baby-boomer wealth transfers over the next 30 years.

**Tenure legal architecture.** NZ rental tenure is weaker than in Germany, Sweden, Austria, or Switzerland. Short fixed-terms, ease of no-cause termination, and lack of long-term rent predictability all affect the *quality* of rental affordability (not just the price).

**Migration rate relative to supply rate.** Periods when net migration exceeds supply rate produce rapid affordability deterioration; periods when it is below drive partial recovery. A long-run structural variable.

---

## 7. International comparators

Four archetypes of *affordability regime* worth comparing — distinct from the *supply regimes* discussed in Supply Economics, though related.

**Germany / Switzerland — regulated long-term rental.** A majority-rental society, with strong tenant protections and rent predictability across decades. Affordability is primarily managed through the **rental regime**, not through ownership subsidy. Stable for a century; not easily transplanted to NZ's single-family ownership culture.

**Vienna / Nordic social housing.** Large-scale public and cooperative housing with income-related rents absorbs the lower half of the income distribution out of the market. Affordability is managed by **market share of non-market housing**.

**Singapore HDB.** Affordability via central delivery: the state builds, the state allocates, homeownership is widespread but on regulated terms. Singular political economy.

**Anglo-American "ownership society".** Australia, US, UK, Canada, NZ. Affordability managed (poorly) through first-home subsidies, low-interest-rate regimes, and expectations of capital-gain-driven wealth accumulation. The system Auckland sits inside.

**France.** Hybrid — substantial social housing (~17%), inclusionary-zoning rules (the SRU law), and active government intervention in the private market. Useful middle-ground reference.

The engineering question: which archetype is Auckland's long-run trajectory drifting toward? The current answer is probably "still Anglo, with gradual drift toward the French hybrid as non-market builders grow." But the trajectory is not locked in.

---

## 8. Durable features

Ten features of the Auckland affordability system that will still be recognisable in 2076.

1. **Ratio-based constraint.** Affordability is always a ratio between cost and earnings, not either in isolation.
2. **Distributional, not aggregate.** Aggregate affordability hides large variance between cohorts, tenures, ethnicities, geographies.
3. **Tenure law shapes outcomes.** The legal framework for renting — length of tenure, grounds for termination, rent increase rules — materially affects what affordability *feels* like, independent of headline rents.
4. **Homeownership rate is a political commons.** A falling homeownership rate changes the political constituency for price stability over decades.
5. **Intergenerational wealth is now a structural prerequisite.** The gap between inheritors and non-inheritors is part of the system, not a transient feature.
6. **Demand-side transfers risk landlord capture.** In a supply-inelastic market, income transfers push up rents more than they increase net welfare.
7. **Rent regulation has empirically mixed effects.** Academic literature shows both short-run tenant protection and long-run supply distortion; the balance depends on design.
8. **Credit cycles dominate short-run.** Short-run price moves are driven more by credit than by supply.
9. **Tax advantages compound.** Untaxed capital gains on owner-occupied housing compound into generational wealth and political resistance to change.
10. **Climate exposure will reshape affordability geography.** Over 50 years, affordable housing in flood-prone or sea-level-exposed areas will become uninsurable and eventually unlivable, shifting the affordability map.

---

## 9. The durable long-run questions

- What target affordability ratio (PTI, rent-to-income, residual income) should Auckland aim for, and is it realistic?
- How much of the affordability outcome should be delivered by the market vs. by non-market housing at scale?
- What rental tenure architecture produces durable affordability without suppressing supply?
- How should New Zealand manage the widening gap between heirs and non-heirs?
- Should affordability be primarily income-side (wages, transfers) or housing-side (supply, regulation, subsidy)?
- What is the right balance between owner-occupier and renter protection in the long run?
- How should the climate-driven shift in where housing is viable be managed without concentrating affordability stress in unsafe areas?
- Can Auckland afford its own affordability policy without national-level tax and transfer reform?

---

## 10. Solution camps on affordability (neutral presentation)

Drafted with six camps. On the public page I'd suggest consolidating to **five** to match Supply Economics (e.g. merging wage-side into transfers-and-wages). Say which.
Luke: Merge as suggested. 

### A. Income support and accommodation transfers
**Core claim:** the affordability problem is fundamentally an income problem at the lower end; the cleanest lever is direct income support — an Accommodation Supplement uprated to current rents, income-related rents on state tenancies, and universal basic housing support.
**Weakness:** landlord capture — in supply-inelastic markets, income transfers flow partially into rents. Fiscal cost.

### B. Rent regulation and tenure protection
**Core claim:** affordability for the 35% who rent is not just about rent levels but about security — predictable rents, genuine long-term tenure, constrained termination. German/Swiss-style protections would change renters' experience materially.
**Weakness:** private landlord exit at the margin; contested international evidence on long-run rent effects.

### C. First-home-buyer pathways and alternative tenure
**Core claim:** the rungs between renting and owning are missing. Shared-equity schemes, rent-to-own, KiwiSaver access, state-backed low-deposit pathways, and institutional build-to-rent expand the set of viable tenure options.
**Weakness:** policies of this kind often end up capitalising into prices (benefit to sellers, not buyers); BTR displaces individual-landlord supply with different characteristics.

### D. Inclusionary zoning and affordable-housing quotas
**Core claim:** large developments should be required to include a share of affordable housing at below-market prices or rents, delivered through planning rules — the French SRU model adapted to NZ.
**Weakness:** increases cost of market housing at the margin; small share of total supply; administrative complexity.

### E. Intergenerational and tax reform
**Core claim:** the widening gap between those with inherited capital and those without is structurally corrosive. A comprehensive capital gains tax (including on owner-occupied housing), inheritance tax, or land value tax would narrow the gap over decades.
**Weakness:** political third rail; transition effects on current owners; practical design challenges. Substantial overlap with the Tax Reform subpage.

### F. Wages and the income side
**Core claim:** the most durable affordability policy is higher incomes, not lower housing costs. Living wage, productivity growth, labour-market reform. If wages rose faster than prices for a decade, the ratio problem would self-resolve.
**Weakness:** wages are the outcome of an economy, not a policy dial; NZ productivity growth is a separate, hard, decade-scale problem.

In practice real programmes combine three or four. A serious public page shows them all and lets the reader see which address the distributional problem vs. the average-level problem.

---

## 11. Conflict-of-interest flag

The conflict surface for Affordability is **smaller** than Land or Supply:

- Camp E (Tax reform) touches land-value and capital-gains taxation, which could affect your land holdings. The Tax Reform subpage will carry this flag more directly.
- Camps A, B, C, D, F are demand-side or wage-side and don't align directly with your disclosed positions.

You have not disclosed a view on affordability, tenure, or income policy. Drafting in the neutral pattern works here without special precaution — the reader-decides default is already enough.

---

## 12. Sources to spot-check

Primary:
- **Stats NZ** — household income, dwelling price (QV), tenure, demographics
- **MBIE** — tenancy bond data (rents), public housing register
- **REINZ / CoreLogic** — dwelling prices
- **RIMU** — Auckland-specific affordability monitoring
- **Treasury** — housing affordability analysis

Analytic:
- **Demographia International Housing Affordability Survey** — PTI framework
- **Stone, Kutty** — residual income affordability literature
- **The Helen Clark Foundation** — affordability work
- **Max Rashbrooke** — inequality and affordability
- **Infometrics** — regional housing analysis

International:
- **OECD Affordable Housing Database**
- **UN-Habitat Urban Indicators**
- **Eurostat** — housing cost overburden rate
- **Joint Center for Housing Studies (Harvard)** — US affordability research
- **Mietrecht (German rent law)** — Germany regulation reference

---

## 13. Open questions for you

1. **Scope of the distribution section.** My default (§5) includes generation, tenure, ethnicity, geography, household composition. Full treatment or tighter to generation + ethnicity only?
Luke: Remove ethnicity, all humans are equal and it will get looked at in household composition anyways. 
2. **Measurement depth.** How much of the methodological material in §3 should make it to the public page? Full taxonomy, or a shorter "which measure we use and why"?
Luke: Probably shorter will work better here. 
3. **Five camps or six?** Draft has six — A through F. Natural consolidations: A+B ("Income and tenure protection"), C+D ("Alternative tenure and quotas"), E, F. Or A+F ("Income-side"), B, C, D, E. Your preference?
Luke: Reduce down to 3 camps for simplicity.
4. **Rent regulation stance.** This is a contentious area with contested international evidence. Is the briefing fair to both sides, or are you seeing bias?
Luke: It's okay considering it is using international evidence, but I have a feeling New Zealand and especially Auckland will not work well under those types of structures. 
5. **Intergenerational wealth framing.** The "heirs vs. non-heirs" framing is important but rhetorically charged. Keep as drafted, soften, or sharpen?
Luke: Yeah, it read as a use vs them set of statements, creating a class war. Overseas intergenerational families have been around for centuries, in New Zealand a couple hundred years for Europeans and a bit longer for Maori but considerably more fragmented. 
6. **Charts.** My default five: (a) Auckland PTI over 40 years, (b) homeownership rate by age cohort over 40 years, (c) rent-to-income by income quartile, (d) deposit gap over time, (e) international PTI comparison. Pick any subset.
Luke: Go with those since I don't know what too remove. 
Once you've answered I'll extract entities, lint, render, and the page will be live at `/auckland/housing/affordability/`.
