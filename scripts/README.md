# scripts/

One-off and recurring CLI tools that operate on the typed-graph corpus
under `content/<region>/data/`. Most of these are mechanical batch
helpers; a few are wired into the deploy / archive / publish loops.

## ingest_external_research.py

Ingests an external research artefact (URL or local PDF) and proposes
**draft** `claim` and `source` YAML stubs for PI review. Drafts are
written to `content/<region>/data/_drafts/<timestamp>/` — the live
`source/` and `claim/` folders are never touched.

### Usage

```bash
python scripts/ingest_external_research.py <URL or PDF path> \
    --region <slug> --theme <slug> [--ollama] [--dry-run] [--max-claims N]
```

Examples:

```bash
# Stats NZ release, dry run (preview only — nothing written):
python scripts/ingest_external_research.py \
    https://www.stats.govt.nz/information-releases/transport-fatalities-year-ended-december-2023 \
    --region wellington --theme transport --dry-run

# RNZ longread, write drafts (heuristic regex extractor):
python scripts/ingest_external_research.py \
    https://www.rnz.co.nz/news/national/<slug> \
    --region auckland --theme housing

# Use the local Ollama qwen2.5:7b for richer claim extraction:
python scripts/ingest_external_research.py paper.pdf \
    --region nz --theme economy --ollama
```

### How it works

1. **Fetch.** URLs go through `requests` with a polite UA. Local PDFs
   need `pypdf` installed (`pip install pypdf`) — clear error if not.
2. **Extract text.** Tries `trafilatura`, then `readability-lxml`+`bs4`,
   then plain `bs4`, then a stdlib `html.parser` fallback.
3. **Source stub.** Heuristic publisher / `type` / `credibility`
   detection from the URL host (Stats NZ → `primary-data`/`official`,
   RNZ → `news-media`/`reputable`, `legislation.govt.nz` →
   `primary-legislation`, etc.). Year is the most-recent 19xx/20xx in
   the title or first 4 KB of body.
4. **Claim stubs.** With `--ollama` and Ollama reachable on
   `localhost:11434`, qwen2.5:7b proposes 1–5 quantitative claims as
   strict JSON. Otherwise (or on failure) a regex heuristic pulls
   sentences containing numbers, percentages, dollar amounts, or
   per-capita rates.
5. **Output.** A `_meta.yaml` sidecar (review checklist, extractor,
   accessed date) plus one `source/` YAML and N `claim/` YAMLs in
   `content/<region>/data/_drafts/<timestamp>/`.

### Schema notes

The brief mentioned a couple of fields that don't exist on the live
schemas (`additionalProperties: false`):

* Source uses `type` (not `kind`) per `content/_schema/source.schema.json`.
* `accessed` and per-claim `theme` aren't valid YAML fields — they're
  stashed in `_meta.yaml` sidecar instead.

The script's emitted YAML is **lint-passable** as-is once moved into
`source/` and `claim/`. Default `methodology_tag` is
`methodology.admin_count_v1` — change before committing if a more
specific methodology fits.

### Limitations

* HTML cleaning falls through to a stdlib parser when none of
  trafilatura / readability-lxml / bs4 are installed; quality
  drops noticeably without them. `pip install trafilatura` recommended.
* PDF parsing requires `pip install pypdf`.
* Ollama extractor expects model `qwen2.5:7b` available locally; if
  Ollama isn't running the script silently falls back to regex with a
  stderr notice (per the brief).
* Regex heuristic over-extracts on number-dense pages and
  under-extracts on prose with spelled-out numbers — always PI-review.
* Source ID slugs are derived from publisher + title + year; there's no
  collision check against existing `source.*` IDs in the live corpus.
  Rename if the slug already exists.
