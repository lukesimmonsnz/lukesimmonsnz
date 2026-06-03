# scripts/archive/2026-Q2-corpus-build/

One-off corpus build/fix utilities authored during CLAUDE.md layers
4a–4q (the 16-region corpus rebuild, 2026-04-26 to 2026-04-27).

These are not referenced from any live entry point (`.bat`, CI, or
production code) and are kept here as historical provenance only.
The corpus they produced is the live `content/` tree; if you need to
re-derive any region, prefer reading the relevant `tools/` modules
inside `content/<region>/tools/` rather than re-running these scripts —
schemas have evolved since they were written.

| Script | Provenance |
|---|---|
| `add_missing_drivers_camps.py` | layer 4a placeholder fill |
| `add_remaining_camps.py`       | layer 4a follow-up |
| `add_root_camps.py`            | layer 4a root-camp injection |
| `build_corpora.py`             | layer 4a/4b mass build |
| `build_drivers_camps_claims.py`| layer 4a structural seed |
| `check_yaml.py`                | smoke parser |
| `count_entities.py`            | gate diagnostic |
| `final_fixes.py`               | layer 4q tail repairs |
| `fix_nelson.py`                | layer 4k Nelson-specific repair |
| `fix_schemas.py`               | schema-evolution backfill |
| `gen_all_regions.py`           | layer 4c–4p batch generator |
| `generate_nelson.py`           | layer 4k generator |
| `generate_regions.py`          | layer 4c–4p driver |
| `regenerate_claims.py`         | wave-3 boilerplate rewrite driver |
| `test_lint.py`                 | smoke for lint pipeline |
| `validate_and_render.py`       | gate harness |
| `validate_edits.py`            | post-edit verification |
| `wire_entities.py`             | claim↔problem wiring |

If any of these proves load-bearing later, lift it back to `scripts/`
proper (not `archive/`).
