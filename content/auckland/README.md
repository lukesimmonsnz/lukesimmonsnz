# Auckland knowledge base

Engineered content-as-data system for the Auckland problems / solutions
research project. Pages are rendered from a typed entity graph. Prose is
authored inside entities; structural elements (camps, evidence, figures,
further reading) are generated.

## Layout

```
content/auckland/
├── schema/          # JSON Schemas for each entity type
├── data/            # one YAML file per entity, grouped by type
│   ├── problems/    # problem / subpage definitions
│   ├── evidence/    # atomic factual claims
│   ├── drivers/     # causal factors affecting problems
│   ├── responses/   # existing policy / programme responses
│   ├── camps/       # clusters of proposed solutions
│   ├── sources/     # bibliographic entries
│   ├── metrics/     # time-series indicators
│   └── actors/      # institutions / individuals that appear
├── briefings/       # private decision-support documents (not published)
├── pages/           # rendered public Markdown (generated — do not hand-edit)
├── templates/       # Jinja2 page templates
└── tools/           # render, lint, graph loader
```

## Entity ID convention

Dotted namespace prefixed by entity type:

| Type     | Example                                  |
|----------|------------------------------------------|
| Problem  | `problem.housing.land`                   |
| Evidence | `evidence.isthmus_width_km`              |
| Driver   | `driver.physical_geography`              |
| Response | `response.auckland_unitary_plan_2016`    |
| Camp     | `camp.compact_city`                      |
| Source   | `source.linz`                            |
| Metric   | `metric.building_consents_auckland`      |
| Actor    | `actor.ngati_whatua_orakei`              |

Filename under `data/<type>/` is the ID with the type prefix stripped,
e.g. `data/camps/compact_city.yaml` has `id: camp.compact_city`.

## Graph

Relationships between entities:

```
Problem  ── drivers     ─► Driver
         ── camps       ─► Camp
         ── evidence    ─► Evidence   ── source ─► Source
         ── responses   ─► Response
         ── sources     ─► Source
         ── figures     ─► Figure (inline)

Camp     ── interventions   (structured intervention descriptions)
         ── addresses       ─► Problem
         ── tensions_with   ─► Camp
         ── evidence        ─► Evidence

Driver   ── affects         ─► Problem
         ── evidence        ─► Evidence
```

## Workflow

1. **Draft or edit entity YAML** under `data/`. Keep claims atomic —
   one Evidence per fact, one Camp per position.
2. **Run `python tools/lint.py`** from `content/auckland/` to validate
   against schemas and check graph invariants. Nothing renders until lint
   passes.
3. **Run `python tools/render.py <problem.id>`** to generate the public
   Markdown page under `pages/`. Never hand-edit files in `pages/`.
4. **Commit both data/ and pages/** so diffs of rendered output are visible
   in review.
5. The Flask app reads `pages/*.md` the same way it reads blog posts.

## Invariants the lint enforces

- Every referenced ID resolves to an existing entity.
- Every `Problem` has ≥1 driver, ≥1 camp, ≥1 evidence, ≥1 source.
- Every `Camp` has ≥1 flagship move, ≥1 tension, ≥1 intervention, ≥1
  addressed problem.
- Every `Evidence` has ≥1 source.
- Evidence confidence is one of `high / medium / low / disputed`.
- Figure IDs referenced in narrative are defined in the Problem's figures list.
- ID namespace matches entity type (`camp.*` in `data/camps/`, etc.).

## Design notes

- **YAML for data, JSON for schemas.** YAML is human-editable with
  multiline strings and comments; JSON Schema is the tooling standard.
- **One entity per file.** Small files diff well in git and are easy to
  find.
- **Prose lives inside Problem entities** as a `narrative` list of
  `{heading, body, figure?}`. The hard-to-automate part (narrative flow)
  stays hand-authored; the easy-to-automate parts (camps, citations,
  further reading) are generated.
- **Figures are placeholders until a chart pipeline exists.** The
  `status: placeholder` flag is a lint signal.
- **Phase 1 renders narrative verbatim.** Later phases can expand inline
  `{{ev:...}}` markers to citations.
