---
title: "Degraded urban freshwater quality in Wellington streams"
section: environment
subpage: waterway-quality
order: 3
updated: 2026-04-26
summary: >
  Wellington's urban streams — including the Kaiwharawhara, Korokoro, and Waiwhetu — are significantly degraded by urban runoff, stormwater infrastructure, and historical channelisation. Most urban streams fail to meet the water quality and ecological standards set by the Whaitua te Whanganui-a-Tara freshwater planning process.
status: draft
generated_from: problem.wellington.environment.waterway_quality
---

# Degraded urban freshwater quality in Wellington streams

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Whaitua baseline findings

The Whaitua te Whanganui-a-Tara process found that the majority of Wellington's monitored urban streams fail to achieve the desired water quality state for swimming, ecological health, or kai gathering (claim.wellington.environment.stream_water_quality_index).


## Channelisation legacy

Many Wellington urban streams were piped or channelised during mid-twentieth century urban development, eliminating the natural filtering, buffering, and habitat functions that support stream health. Daylighting and restoration is technically feasible but costly in built-up areas (claim.wellington.environment.urban_stream_degradation).


---


## Drivers

The following structural drivers contribute to this problem.


### Channelisation and piping of urban streams



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Urban catchment impervious surface expansion



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus

### Urban stormwater contaminant load



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Stormwater Source Control and Treatment

Low-impact urban design and stormwater treatment trains will reduce contaminant loads to waterways at source.

**Flagship moves:**

- Mandatory rain gardens and permeable paving in all new developments
- Retrofit stormwater treatment in legacy industrial catchments
- Zinc and copper source controls on roofing and brake materials

**Tensions:**

- Retrofit programmes in existing urban areas are expensive and require access to private land
- Source controls on materials require national-level regulation, not just local action

**Interventions on the system:**

- Require low-impact stormwater design for all new development consents in Wellington Region from 2025 (state variable: `stormwater_contaminant_load`, sign: -)


### Urban Stream Riparian Restoration

Daylighting and restoring channelised urban streams will improve freshwater ecology and reduce flood risk.

**Flagship moves:**

- Daylight and restore Korokoro Stream through Lower Hutt industrial zone
- Establish riparian planting corridors (10m minimum) on all urban streams
- Remove concrete channelisation from Kaiwharawhara Stream

**Tensions:**

- Riparian setbacks reduce developable land in flood-prone areas
- Stream daylighting conflicts with existing drainage infrastructure

**Interventions on the system:**

- Fund riparian restoration on the top 10 degraded urban stream reaches identified in GWRC's freshwater plan (state variable: `urban_stream_ecological_health`, sign: +)


---

## Claims cited on this page

- **The Whaitua te Whanganui-a-Tara freshwater planning process found that the majority of Wellington's monitored urban streams fail to achieve the desired state for swimming, ecological health, or kai gathering, with urban contaminants and channelisation as primary causes.** — Whaitua te Whanganui-a-Tara Committee Report 2021.
- **Many Wellington urban streams were piped or channelised during mid-twentieth century urban development, eliminating natural filtering, buffering, and habitat functions; daylighting and ecological restoration is technically feasible but costly in built-up areas.** — Greater Wellington State of the Environment Report 2022; Whaitua te Whanganui-a-Tara Committee Report 2021.

---

## Further reading


- **Whaitua te Whanganui-a-Tara Committee Report 2021** (Greater Wellington Regional Council), 2021 — <https://www.gw.govt.nz/environment/freshwater/whaitua/>

- **Greater Wellington State of the Environment Report 2022** (Greater Wellington Regional Council), 2022 — <https://www.gw.govt.nz/environment/state-of-the-environment/>


---

## Technical notes

*State variables:* stream_water_quality_index, macroinvertebrate_community_index.

*Constraints:* piped_and_channelised_stream_sections, impervious_catchment_surface.

*Inputs:* urban_runoff_contaminant_load, riparian_restoration_investment.


*Feedback loops:*

- `Impervious surface amplification: urban infill increases impervious surface, intensifying stormwater runoff and contaminant pulses into streams.`


---

*Generated from `problem.wellington.environment.waterway_quality` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
