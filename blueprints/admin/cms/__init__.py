"""CMS sub-package — see docs/CMS-SPEC.md and docs/CMS-IMPL-WAVE-1..4.md.

Wave 1 ships the foundation: page resolver, cms.db DAO, draft store API.
Waves 2–4 build the UI (page tree, editor partials, publish pipeline,
media library, settings, search/replace, diff/history) on top.

The two PI mastery gates that this package preserves:
1. The 10 projection ``load``/``save`` bodies in ``resolver.projections``.
2. The preview overlay in ``overlay.py`` (wave 3 / item 4) — not in
   this wave.
"""
