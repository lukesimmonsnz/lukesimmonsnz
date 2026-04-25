# Auckland data pipeline — Phase 2 plan

This document records the plan for automating figure data across the rest of the
Auckland research pages as they're written. Phase 1 (already landed) is the
three housing subpages — it established the architecture. Phase 2 extends it.

## Current state (Phase 1)

Three pipelines live under [`content/auckland/tools/`](../content/auckland/tools/):

| Tool | Input | Output | Inputs committed? |
|---|---|---|---|
| [`render_charts.py`](../content/auckland/tools/render_charts.py) | `data/charts/*.yaml` + `data/series/*.csv` | `static/img/auckland/<id>.svg` | CSVs: yes |
| [`render_maps.py`](../content/auckland/tools/render_maps.py) | `data/maps/*.yaml` | `static/img/auckland/<id>.svg` via GeoJSON cached to `data/maps/cache/*.geojson` | GeoJSON cache: yes |
| [`lint.py`](../content/auckland/tools/lint.py) | `data/<entity>/*.yaml` | exit code | — |

Both renderers share:

- Deterministic: no LLM, same inputs produce the same SVG.
- Idempotent: an mtime check skips unchanged outputs.
- Escape hatch: every generated SVG embeds a `data-pipeline=<tool>` signature. If an SVG at the target path lacks the signature and is newer than all inputs, the renderer refuses to overwrite. A `manual: true` spec flag makes that permanent.
- Scheduled: both run every 15 minutes via `lukesimmonsnz-regen-docs` (Windows Task Scheduler → [`agent/run_regen_docs.bat`](../agent/run_regen_docs.bat)).

## What's still manual today

1. **Chart CSVs.** Every CSV under `data/series/` that starts with `# PLACEHOLDER` is illustrative. Replacing it with real data is a human step — download the source CSV, match column names, commit.
2. **Most map fetches.** Only `volcanic-cones-viewshafts` currently pulls real data (Auckland Council's Unitary Plan D14 overlay). Land-use and sea-level stay as placeholders until either a QGIS export arrives or a multi-layer map fetcher is built.
3. **New page figures.** Every new Auckland subpage hand-writes `<img>` + `<figure>` tags by hand; there is no lint check that a matching spec exists.

Phase 2 addresses these three gaps.

## Phase 2 — Fetcher registry

### Goal

One Python file per upstream data source, with a stable function signature. Specs
reference a fetcher by dotted name; the renderer calls it to produce or refresh the
data file before rendering. Specs keep their provenance (URL, columns, filters)
declarative in YAML.

### Proposed layout

```
content/auckland/tools/fetchers/
├── __init__.py
├── acouncil.py          # Auckland Council Open Data (ArcGIS Hub, no auth)
├── linz.py              # LINZ Data Service (WFS + API key)
├── statsnz.py           # Stats NZ releases and Infoshare
├── oecd.py              # OECD stat.csv endpoints
├── niwa.py              # NIWA coastal and climate datasets
└── demographia.py       # Annual PTI tables (PDF → tabular)
```

Each module exports functions that take a spec-provided parameter dict and return
either a CSV string (for charts) or a GeoJSON FeatureCollection (for maps). The
renderer is responsible for caching to disk; fetchers are pure.

### Spec extension

A chart spec grows an optional `fetcher:` key:

```yaml
id: supply-annual-consents
type: line
fetcher:
  name: statsnz.building_consents
  params:
    region: Auckland
    aggregate: annual
    measure: new_dwellings
data: series/auckland-annual-consents.csv   # destination, not a precondition
```

If `fetcher:` is present and the destination CSV is older than, say, 24 hours (or
missing), the renderer calls the fetcher, writes the result to `data:`, then
renders. If the fetcher is absent, the current behaviour (require a hand-committed
CSV) applies — so placeholders continue working.

Maps get the same treatment, with `fetcher:` replacing the inline `feature_service:`
block for sources that need more than a single ArcGIS layer query (e.g. joining
LINZ parcels to an Auckland Council classification).

### Scheduling

- `run_regen_docs.bat` stays on its 15-minute tick, but only triggers re-render if
  the cached data or spec changed — no forced refetching.
- A new `run_refresh_data.bat` runs daily (Windows Task Scheduler, e.g. at 03:00),
  invoking every fetcher whose cache is older than its declared TTL. That keeps
  hosted sources honest without spamming them.

### Errors and audit

- Fetchers log to `agent/logs/fetchers.log` with dataset id + HTTP status + row
  counts. A fetch failure does **not** break the render — the last good cache
  continues to serve, with a visible stamp ("data as of 2026-03-14") in the SVG.
- Every dataset's committed CSV/GeoJSON carries a `#` header comment with the
  retrieval URL, timestamp, and fetcher version. Reproducibility matters more
  than elegance; readers should be able to see where a number came from.

## Phase 2 — Figure lint

A small addition to [`lint.py`](../content/auckland/tools/lint.py):

1. Walk `content/auckland/pages/**/*.md`; extract every `<img src="/static/img/auckland/*.svg">` path.
2. For each path, require either a chart spec at `data/charts/<id>.yaml`, a map spec at `data/maps/<id>.yaml`, or a hand-produced SVG with a `manual: true` sibling spec.
3. Exit non-zero with a clear diff if any figure lacks a spec, so the lint task catches missing figures before a page lands.

This closes the loop: every referenced figure has either a pipeline spec or an
explicit acknowledgement that it's hand-produced.

## Phase 2 — New-page workflow

When a new Auckland subpage is drafted:

1. Author writes narrative + figcaptions in the `.md` file as usual.
2. For each new figure, they add a skeleton spec (chart or map) — title, subtitle, source URL, `status: placeholder`, `fetcher:` optional. Placeholder data renders immediately so the page doesn't ship with broken images.
3. Over time, real data replaces placeholders either by committing a real CSV/GeoJSON or by wiring up a fetcher. Status flips to `verified`; the "placeholder" stamp disappears.
4. Figure lint enforces the contract on every render run.

## Sequence

Phase 2 is not a single push — it's incremental. Rough order:

1. **Figure lint** (small; catches problems before they land).
2. **One fetcher — `acouncil.py`** (we already know the pattern; extract the logic from `render_maps.py` into a fetcher module).
3. **`statsnz.py`** — highest-value for the housing pages (consents, productivity, tenure). Start with the Stats NZ building-consents CSV bundle.
4. **`oecd.py`** — SDMX-CSV endpoints; straightforward.
5. **`linz.py`** — WFS + API key; last because it needs the key-management story.
6. **`demographia.py` and `niwa.py`** — more specialised; add when a page needs them.

Each fetcher lands with one real data file committed alongside as the first
consumer.

## Non-goals

- **Live interactive charts.** The site stays static SVG-in-markdown. No
  JavaScript charting libraries.
- **Data-warehouse parity.** The pipeline commits snapshots; it is not a
  replacement for Stats NZ Infoshare or Auckland Council's GIS portal. It
  captures the exact slice a page argues from, not the full upstream.
- **Cross-regional comparison.** Scope is Auckland. LINZ will be used only where
  there is no Auckland-specific equivalent.
