"""Admin namespace package — currently contains only the CMS subpackage.

The typed-entity YAML editor that used to live at ``/admin/yaml/`` was
shelved 2026-05-30 and the implementation files (``blueprint.py``,
``edges.py``, ``save_pipeline.py``, ``schema_walker.py``) were moved to
``archive/admin-yaml/``. See ``docs/DASHBOARD-SPEC.md`` for the original
spec and the 2026-05-30 changelog entry for why.

This ``__init__`` deliberately re-exports nothing — it exists only so
that ``blueprints.admin.cms.*`` remains a valid import path.
"""
