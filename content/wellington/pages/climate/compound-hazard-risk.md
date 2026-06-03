---
title: "Compound earthquake-climate risk in Wellington"
section: climate
subpage: compound-hazard-risk
order: 1
updated: 2026-04-26
summary: >
  Wellington faces an unusual and severe compound hazard profile: high-probability major earthquake risk intersects with climate change impacts including sea-level rise, increased rainfall intensity, and coastal storm surge. These hazards interact: a major earthquake that subsides coastal land permanently increases sea-level-rise exposure; climate-driven flooding may be followed by earthquake-damaged drainage infrastructure.
status: draft
generated_from: problem.wellington.climate.compound_hazard_risk
---

# Compound earthquake-climate risk in Wellington

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Wellington Fault rupture probability

GNS Science estimates that the Wellington Fault has approximately an 8–11% probability of rupturing in the next 100 years, producing a Mw 7.4–7.9 earthquake directly beneath the city — one of the highest-probability major earthquake risks of any capital city in the world (claim.wellington.climate.wellington_fault_rupture_probability).


## Compound hazard amplification

Wellington's compound hazard profile — earthquake plus sea-level rise plus intensified storms — means that standard single-hazard risk assessments underestimate actual exposure. Infrastructure must be designed to function under combinations of hazards that were previously treated as independent (claim.wellington.climate.compound_hazard_infrastructure_risk).


---


## Drivers

The following structural drivers contribute to this problem.


### Earthquake-climate compound hazard interaction



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Wellington Fault major earthquake hazard



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Integrated Multi-Hazard Risk Planning

Wellington's compound hazard profile (earthquake + climate) requires integrated risk planning that cross-references both hazard types in land use and infrastructure decisions.

**Flagship moves:**

- Joint earthquake-climate adaptation planning unit across all Wellington TAs
- Mandatory multi-hazard risk assessment for all major infrastructure consents
- Scenario planning for earthquake + storm compound event with CDEM

**Tensions:**

- Multi-hazard integration requires significant analytical capability not currently in most TAs
- Comprehensive risk planning may paralyse decision-making in the short term

**Interventions on the system:**

- Establish Wellington Multi-Hazard Planning Unit shared across GWRC and all TAs (state variable: `integrated_hazard_planning_coverage`, sign: +)


### Precautionary Land Use Controls for Hazard Zones

Prohibiting new development in compound hazard zones (fault lines + flood plains + liquefaction) is the safest long-term approach.

**Flagship moves:**

- Map all Wellington compound hazard zones in District Plans
- Prohibition on new residential development in category 3 hazard zones
- Incentive-based voluntary relocation from highest-risk existing residential areas

**Tensions:**

- Development prohibitions may worsen housing supply in an already constrained market
- Category boundaries are contested; property owners dispute zone classifications

**Interventions on the system:**

- Require multi-hazard risk overlay in all Wellington District Plan reviews under RMA (state variable: `development_in_hazard_zones`, sign: -)


---

## Claims cited on this page

- **GNS Science estimates the Wellington Fault has approximately an 8–11% probability of producing a Mw 7.4–7.9 earthquake in the next 100 years, representing one of the highest-probability major earthquake risks of any capital city globally.** [value: 9 percent probability of Mw7.4+ rupture in 100 years (midpoint estimate); 2022] — Wellington Fault Earthquake Hazard Assessment.
- **Standard single-hazard risk assessments underestimate Wellington's actual infrastructure exposure because earthquake and sea-level rise hazards interact: fault rupture can permanently subside coastal land, while infrastructure damaged by earthquake reduces climate resilience of the built environment.** — Wellington Fault Earthquake Hazard Assessment; New Zealand Sea Level Rise Guidance: Updated Projections 2023.

---

## Further reading


- **Wellington Fault Earthquake Hazard Assessment** — Van Dissen R et al. (GNS Science), 2022 — <https://www.gns.cri.nz/research/natural-hazards/earthquakes/wellington-fault/>

- **New Zealand Sea Level Rise Guidance: Updated Projections 2023** (Ministry for the Environment), 2023 — <https://environment.govt.nz/publications/coastal-hazards-and-climate-change-guidance/>


---

## Technical notes

*State variables:* compound_hazard_exposure_index, fault_rupture_probability_100yr.

*Constraints:* urban_development_on_reclaimed_land, fault_zone_land_use_planning.

*Inputs:* fault_rupture_magnitude, sea_level_rise_trajectory.


*Feedback loops:*

- `Compound amplification: earthquake land subsidence permanently increases coastal flood exposure; infrastructure damaged by earthquake reduces climate resilience of the built environment.`


---

*Generated from `problem.wellington.climate.compound_hazard_risk` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
