---
title: "Designing a smart home on my terms"
date: 2026-05-26
author: luke
summary: "A home-automation design built around what I want my house to do — and, just as importantly, what I don't want it to do. The principles are locked; the hardware isn't on the network yet."
tags: [project-writeup, smart-home, home-automation, design-log]
status: published
---

*Author's note: this post was drafted by Claude (Anthropic) from my project notes and source code, then reviewed and edited by me before publishing. The voice and judgments are mine; the typing isn't.*

## What I'm actually trying to build

Most smart-home writeups start with the X — "I want the lights to turn on when I get home." Mine starts with the Y, because the Y is the part that decided every other choice in the stack.

**What I don't want:**

- No cloud accounts in the control path. If my internet drops, every automation in the house should keep working. If a vendor turns off their servers in 2030, no light switch in my house should become a paperweight.
- No always-on microphones. No Alexa, no Google Assistant, no Apple HomePod listening in the lounge. I don't trust the threat model and I don't want the ambient surveillance even if I did.
- No app per device. The number of single-purpose apps that ship with consumer IoT gear is a usability disaster and a security one. One control surface or it doesn't go in.
- No phoning home. If a device's only way to reach me is via the manufacturer's cloud relay, it doesn't belong on this network.

**What I do want:**

- Lights, climate, and presence-aware automations that just work, locally, without me thinking about them.
- A single dashboard I actually look at, not buried in three vendor apps.
- A platform I can poke at with code — the automation layer is exactly the kind of place where a small LLM running on my home-lab box could earn its keep, and I want that door left open.
- An exit ramp. Every device and every protocol should be replaceable without ripping the rest out.

That set of constraints rules out about 80% of the consumer smart-home market in one swing. The remaining 20% is what this writeup is about.

## The stack

The radio-and-protocol layer is the part most writeups skip past. It's also the part that decides everything downstream, so it's worth being explicit about.

### Radio layer

Zigbee for the bulk of the sensor fleet — 2.4 GHz mesh, mains-powered devices act as repeaters, fully local once you have a USB coordinator dongle and a broker, biggest catalogue, lowest per-device cost (downside: sharing 2.4 GHz with Wi-Fi, manageable with channel planning). Thread for new buys where there's a certified Matter-over-Thread option that's actually mature — in early 2026 a much smaller list than the marketing suggests, so the plan starts Zigbee-heavy. No Wi-Fi sensors: cheap Wi-Fi devices are almost always cloud-locked, power-hungry for anything battery-driven, and add noise to a band I'd rather keep clean.

### Application + brain

Home Assistant, running locally. The staging setup right now is Home Assistant OS in a VM on my main desktop — good enough to design against, deliberately not the production target. Production lives on a dedicated small box once the design stops moving. Zigbee2MQTT will talk to a USB coordinator (still choosing between SkyConnect, Sonoff ZBDongle-E, and ConBee III based on Z2M compatibility for the device list I end up with). No HA Cloud, no Nabu Casa. Remote access, if I want it later, goes through a self-hosted reverse proxy or a Tailscale tailnet — not anyone's relay.

The Home Assistant choice is the load-bearing one. It's the only platform that takes "fully local, mixes protocols, owns its own state" as a first principle rather than a marketing checkbox. Apple Home is more polished and SmartThings has wider out-of-box device support, but both route through a cloud I don't want in the path.

### Hardware

Aqara for most of the planned sensors — motion, door/window, temperature/humidity. Zigbee, cheap, pair cleanly with Zigbee2MQTT, unobtrusive form factors. The first-wave fleet is small — under twenty devices across the three categories — because the right scope for v1 is "one room, end to end" rather than "every room, half-built." Smart switches are the next layer after sensors, and the irreversible constraint there is the neutral wire at the switch box — a wiring decision that has to be made before the wall closes.

## How the rooms will be organised

Room-first, not device-first. Entities follow a flat `area.device.function` naming scheme; areas group them into the unit a human actually reasons about ("the lounge is occupied"); scenes are explicit named states rather than ad-hoc on/off lists; automations are intent-named (`presence.lounge.arrive`, `climate.bedroom.sleep`) so future-me reading the YAML in eighteen months can tell what each one is for without opening it.

The local-only constraint shows up in a specific way: every trigger has to resolve from local state. No cloud webhooks, no IFTTT-style "phone entered geofence as reported by Google." Presence detection itself isn't implemented yet — that's the most interesting open design question, and the one most likely to change once I have real day-to-day data. The candidates I'm weighing are mmWave (Aqara FP2 or similar), Bluetooth tracking via ESPresense, and motion-only-as-baseline. mmWave is the strongest signal but adds cost and a sensor per room; Bluetooth tracks phones rather than people; motion is the cheapest and the worst at telling "sitting on the couch" apart from "walking through."

## Where this sits today

Honestly: the design is locked, the staging VM runs, and no production hardware is on the network yet. This writeup is the design log, not a deployment log. The reason it exists at this stage is that the architectural decisions — local-first, no microphones, exit-ramps, room-first composition — are the part most consumer smart-home writeups skip past, and the part that decides everything else downstream. Writing them down now is how I avoid drift once the first box of Aqara sensors lands.

## Known design tensions

A few open questions the design doesn't fully answer yet, kept here as honest TODOs:

- **Zigbee + Wi-Fi coexistence on 2.4 GHz.** Channel planning is straightforward in theory but only verifiable once both networks are running real traffic. I'll know within a week of bringing up the first room whether the placement assumptions hold.
- **Presence detection.** Genuine fork in the road; I'll pick after one round of testing rather than committing now.
- **Automation race conditions.** Multiple automations racing over the same target state is the category I'm watching for as more rules go in. Hasn't bitten yet — but also hasn't had the chance to, because the rules aren't live.

## What's next, in order

1. Pick the Zigbee coordinator dongle.
2. Stand up Home Assistant on the chosen production box (off the desktop VM).
3. Start with one room — motion + door sensor + a single smart switch — wired end to end, before scaling.
4. Document what actually broke against this design, in a follow-up post. That one will be a deployment log, not a design doc.

The version of this house that exists in a year will have more sensors, smarter presence, and probably an LLM somewhere in the loop. The version that exists today is a design I trust enough to start buying hardware against — which is the only version of any of this I was ever interested in shipping.

*— Luke Simmons, Auckland*
