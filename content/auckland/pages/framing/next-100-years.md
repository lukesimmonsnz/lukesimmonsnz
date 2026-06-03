---
title: "The next 100 years: engineering, CS, and AI as levers"
summary: Where computer science, systems engineering, and applied AI can contribute durably to Auckland's housing, transport, infrastructure, environment, and governance problems over the 2025–2125 horizon.
section: framing
subpage: next-100-years
order: 2
updated: 2026-05-30
status: draft
---

## Why technology on a 100-year frame

Most discussion of "AI for cities" operates on a one-to-five-year horizon — pilots, optimisation, productivity dashboards. A century is longer than the useful life of any current architecture, framework, model family, or company. Framing the question in terms of *durable levers* — what computer science and engineering can do that survives the churn — filters out the hype and surfaces work worth starting now.

Each section below follows the same structure: a measured state from the Auckland data graph (cited by entity ID), then a near-horizon view to roughly 2050 grounded in observable trends, then a far-horizon view to 2125 explicitly marked as speculative scenario reasoning rather than projection.

## Housing: automated design, modular construction, digital permitting

The bottleneck is flow, not stock: Auckland's median multiple was 10.7 in 2023 (`claim.auckland.housing.affordability_ratio_2023`, Demographia), construction cost has outpaced general CPI for two decades (`claim.auckland.housing.construction_cost_rise`), and annual consents have stayed in the 14–18k band across the recent decade. Three levers are now far enough along to track rather than imagine: rule-based generative design tooling producing compliant plans in minutes; factory-built modular components shipping at scale in Sweden and Japan, now entering NZ through firms like Williams Corporation and Box Group; machine-checked building consents (working concept in Singapore's CORENET-X). The 2050 question is whether any of these reaches the scale that flattens the cost curve, or whether industry-structure and regulatory constraints absorb the productivity gain.

**Far horizon, speculative.** A construction industry where design, consent, and assembly are mostly machine-driven looks plausible. The durable bet is the *interfaces* — schema-defined components, machine-legible building code, standard data formats. None of today's named systems will exist in 2125; the standards they pioneer might.

## Transport: networks as the substrate for autonomy

Private vehicles account for 78–82% of Auckland trips, one of the highest car mode shares among comparable OECD cities (`claim.auckland.transport.car_mode_share_2023`). The Crown-Council ATAP programme sequences investment across road, rail, PT, walking and cycling on a 10-year horizon (`claim.auckland.transport.atap_2024_programme`), but the mode split is downstream of four decades of motorway-first investment and low-density development that's structurally slow to reverse. Autonomous vehicles dominate the discourse; the slower and more durable work is the *network layer* — lane discipline, signal coordination, kerb management, real-time multimodal dispatch, freight routing. Each is a CS problem with a long build and long payoff. The 2050 question is whether Auckland's road, rail, ferry, and cycle networks get operated as a single optimisation problem, or five overlapping ones.

**Far horizon, speculative.** The dominant transport mode 100 years out is decided by density, not by AV technology. If Auckland stays low-density, network optimisation buys efficiency without changing mode share. If density rises, the network layer becomes the lever that lets transit and active modes carry most trips. Either path, the durable CS contribution is in the substrate.

## Infrastructure: digital twins, predictive maintenance, sensor networks

Auckland faces a multi-billion-dollar infrastructure investment gap across water, wastewater, stormwater, transport, and digital networks — decades of deferred renewal against a funding model (property rates + development contributions) structurally insufficient for the scale required (`claim.auckland.infrastructure.auckland_investment_gap`). The 1998 CBD power crisis — five weeks of blackout when four transmission cables failed simultaneously — illustrated how invisible decay is until failure (`claim.auckland.infrastructure.auckland_grid_vulnerability`). Dense sensor instrumentation combined with physics-based models and ML-driven anomaly detection turns maintenance from reactive to predictive. The durable lever is the persistent *digital twin* — built once, maintained as a first-class asset, kept current across the lifetime of the physical system. Singapore's Virtual Singapore is the international proof-of-concept. The 2050 question is whether the funding model funds the twin's maintenance, or treats it as a project that ships and then rots.

**Far horizon, speculative.** Infrastructure decisions track centuries — pipes laid in 1925 are still in service. The bet is that the next 100 years' decisions get made with vastly better forward-looking models: climate-conditioned demand curves, AI-assisted failure-mode reasoning, automated reconciliation between asset state and intervention plans. The institutional shift required is treating data infrastructure as load-bearing rather than auxiliary.

## Environment: climate modelling, coastal adaptation, energy

Auckland accounts for ~30% of NZ's transport emissions and ~25% of total energy emissions; current policy trajectory falls short of the 2050 net-zero contribution from the transport sector (`claim.auckland.climate.auckland_emissions_profile`). Under SSP2-4.5, the city faces 0.3–0.5m of sea-level rise by 2070 and 0.5–1.0m by 2120, with roughly 12,000 coastal properties exposed at the 0.5m threshold — Tāmaki Estuary, the central isthmus, and Manukau Harbour margins most acutely (`claim.auckland.climate.auckland_sea_level_exposure`). ML surrogates for expensive climate simulators are already standard in research; Auckland-specific applications — satellite-derived flood-plain tracking, building-level adaptation scoring, distributed-renewable-grid optimisation — are concrete CS work on problems the city will demonstrably keep facing.

**Far horizon, speculative.** Sea-level rise is monotonic over the horizon — the question isn't whether but where, and the answer is governance, not science. Who decides which streets and suburbs get defended and which get retreated; what happens to insurable land values when the bill arrives; how the trade-offs are made visible. The technology to model these at fine geographic resolution already exists. The institutions to act on it do not.

## Governance and participation

Auckland local-body election turnout has fallen from ~52% in 2010 to ~35% in 2022, with some wards under 20% (`claim.auckland.governance.auckland_voter_turnout`). The Council's seven Council-Controlled Organisations (AT, Watercare, Eke Panuku, ATEED, others) operate at significant arm's length, with limited public scrutiny of strategic decisions and persistent loss-making operations that don't reliably trigger democratic accountability mechanisms (`claim.auckland.governance.cco_accountability_gap`). The accountability infrastructure is thinner than the formal structure suggests. The less visible but possibly most important technical lever: tools that let large groups of residents produce decisions that hold up to adversarial scrutiny — open structured-data pipelines (of which this Auckland project is a small example), participatory budgeting, machine-legible policy. The 2050 question is whether a city of three or four million can be governed through something more accountable than the current mix of public consultation forms and elected-member discretion.

**Far horizon, speculative.** The durable governance question is whether civic-tech infrastructure becomes load-bearing — citable in legal proceedings, depended on for budget decisions, treated as core public infrastructure with maintenance and replacement plans. If it does, the city's accountability surface grows. If it doesn't, the tools stay marginal regardless of how good the technology is.

## What *not* to rely on

A durable 100-year list also requires honesty about what is likely to be ephemeral. Specific model families, specific vendors, specific programming languages, specific frameworks — none of these will survive the horizon. The work that compounds is in *interfaces*, *standards*, *data formats*, and *institutional capacity to maintain systems*. This page is an argument for betting long on the unglamorous layer, not on whichever chatbot is fashionable in any given year.

## How this site fits in

The Auckland research project itself is a small experiment in one of these levers — content-as-data with schema validation and lint-checkable citations — applied to public-policy argument. It is one data point for what the durable governance layer might look like when built in the open. If that experiment holds up, the patterns used here should be transferable to other cities and other domains, which is part of the point.

---

*Forward-looking content. Near-horizon (2026–2050) reasoning is grounded in cited entity-graph claims and observable trends. Far-horizon (2050–2125) sections are explicitly speculative scenario reasoning and should be read as such — they describe what might compound, not what will happen.*
