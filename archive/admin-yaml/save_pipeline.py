"""Save pipeline (DASHBOARD-SPEC.md §5).

Pipeline stages
---------------
    [1] JSON Schema validate         → 422 on failure (write blocked)
    [2] Atomic write to working tree → tempfile + os.replace
    [3] Run cross-entity invariants  → soft-block (write proceeds, report)
    [4] Re-render affected pages     → via content._render dispatcher
    [5] Per-save git commit          → ratified §0 row 5

Step [2] enforces per-save authorship-stamping (§0 row 6):
    * ``last_verified`` is set to today's date.
    * ``verification_status`` is preserved unless the form's submitted
      value differs (the dropdown only surfaces during transitions).

Step [5] is best-effort — if git is not initialised in the working tree
the commit is silently skipped and the response carries
``status_git: "skipped"`` so the dashboard can warn.
"""
from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import jsonschema
import yaml

_ROOT = Path(__file__).resolve().parent.parent.parent
_SCHEMA_DIR = _ROOT / "content" / "_schema"


# ---------------------------------------------------------------------------
# Schema loading + cross-schema $ref resolver
# ---------------------------------------------------------------------------

def _load_schema(entity_type: str) -> dict[str, Any]:
    path = _SCHEMA_DIR / f"{entity_type}.schema.json"
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _registry() -> jsonschema.RefResolver:
    """Build a RefResolver that can dereference aotearoa://schema/<x> URIs."""
    store: dict[str, dict[str, Any]] = {}
    for path in _SCHEMA_DIR.glob("*.schema.json"):
        with path.open("r", encoding="utf-8") as fh:
            schema = json.load(fh)
        if "$id" in schema:
            store[schema["$id"]] = schema
    # Use any schema as the base; the resolver only needs the store.
    return jsonschema.RefResolver(base_uri="", referrer={}, store=store)


def validate(entity_type: str, body: dict[str, Any]) -> list[str]:
    """Return the list of JSON Schema validation errors. Empty = OK."""
    schema = _load_schema(entity_type)
    resolver = _registry()
    validator = jsonschema.Draft202012Validator(schema, resolver=resolver)
    return [
        f"{'/'.join(str(p) for p in e.absolute_path)}: {e.message}"
        for e in sorted(validator.iter_errors(body), key=lambda e: list(e.absolute_path))
    ]


# ---------------------------------------------------------------------------
# Atomic write
# ---------------------------------------------------------------------------

def _yaml_dump(body: dict[str, Any]) -> str:
    return yaml.safe_dump(body, sort_keys=False, allow_unicode=True, width=100)


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _stamp_authorship(body: dict[str, Any], entity_type: str) -> dict[str, Any]:
    """§0 row 6 — auto-stamp last_verified on Claim. No-op for entities
    that do not declare last_verified in their schema."""
    if entity_type == "claim":
        body = dict(body)
        body["last_verified"] = date.today().isoformat()
    return body


# ---------------------------------------------------------------------------
# Invariants (cross-entity lint)
# ---------------------------------------------------------------------------

def _run_invariants(region: str) -> tuple[list[str], list[str]]:
    """Load the region's graph and run content._schema.invariants.run_all.

    Returns ``(errors, warnings)``. Empty lists = clean.
    """
    tools_dir = _ROOT / "content" / region / "tools"
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    graph_module = importlib.import_module(
        f"content.{region.replace('-', '_')}.tools.graph"
    )
    graph = graph_module.load_graph()
    from content._schema.invariants import run_all
    result = run_all(graph)
    return list(result.errors), list(result.warnings)


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def _render(region: str, entity_id: str) -> tuple[int, str]:
    """Invoke the unified renderer. Returns (return_code, stderr_excerpt)."""
    from content._render import render
    try:
        rc = render(region, entity_id)
    except SystemExit as exc:  # render's argparse may sys.exit on lint
        rc = int(exc.code or 0)
        return rc, "renderer raised SystemExit"
    except Exception as exc:  # pylint: disable=broad-except
        return 1, f"{type(exc).__name__}: {exc}"
    return rc, ""


# ---------------------------------------------------------------------------
# Git commit (best effort)
# ---------------------------------------------------------------------------

def _git_commit(path: Path, message: str) -> str:
    """Stage and commit one file. Returns 'ok', 'nochange', or 'skipped: <reason>'."""
    if not (_ROOT / ".git").is_dir():
        return "skipped: no .git"
    try:
        rel = path.relative_to(_ROOT)
        subprocess.run(
            ["git", "add", "--", str(rel)],
            cwd=_ROOT, check=True, capture_output=True, text=True,
        )
        # Detect whether anything is staged for this file.
        diff = subprocess.run(
            ["git", "diff", "--cached", "--quiet", "--", str(rel)],
            cwd=_ROOT, capture_output=True, text=True,
        )
        if diff.returncode == 0:
            return "nochange"
        subprocess.run(
            ["git", "commit", "-m", message, "--", str(rel)],
            cwd=_ROOT, check=True, capture_output=True, text=True,
        )
        return "ok"
    except FileNotFoundError:
        return "skipped: git not on PATH"
    except subprocess.CalledProcessError as exc:
        return f"skipped: git error: {exc.stderr.strip()[:200]}"


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

@dataclass
class SaveReport:
    status: str                        # "ok" | "schema_failed" | "lint_failed"
    schema_errors: list[str] = field(default_factory=list)
    lint_errors: list[str]   = field(default_factory=list)
    lint_warnings: list[str] = field(default_factory=list)
    render_status: str = ""
    render_message: str = ""
    git_status: str = ""
    file_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def entity_path(region: str, entity_type: str, entity_id: str) -> Path:
    """Locate the YAML file for an entity.

    The on-disk filename does NOT mechanically equal ``<id>.yaml`` — the
    region slug is usually elided from the filename (e.g. an entity with
    id ``claim.auckland.climate.foo`` lives in ``climate.foo.yaml``).

    Strategy:
      1. Scan ``content/<region>/data/<entity_type>/*.yaml`` and match
         on the ``id:`` field. This is authoritative for existing files.
      2. If no match (new entity), derive the filename by stripping the
         ``<entity_type>.`` prefix and any leading ``<region>.`` segment.
    """
    data_dir = _ROOT / "content" / region / "data" / entity_type
    if data_dir.is_dir():
        for p in data_dir.glob("*.yaml"):
            try:
                with p.open("r", encoding="utf-8") as fh:
                    body = yaml.safe_load(fh) or {}
            except (OSError, yaml.YAMLError):
                continue
            if body.get("id") == entity_id:
                return p

    # New entity — derive a sensible filename.
    prefix = f"{entity_type}."
    stem = entity_id[len(prefix):] if entity_id.startswith(prefix) else entity_id
    region_prefix = f"{region.replace('-', '_')}."
    if stem.startswith(region_prefix):
        stem = stem[len(region_prefix):]
    return data_dir / f"{stem}.yaml"


def save_entity(
    region: str,
    entity_type: str,
    entity_id: str,
    body: dict[str, Any],
    *,
    commit_message: str | None = None,
) -> SaveReport:
    """End-to-end save. Implements §5 of DASHBOARD-SPEC.md."""

    # [1] Schema.
    schema_errors = validate(entity_type, body)
    if schema_errors:
        return SaveReport(status="schema_failed", schema_errors=schema_errors)

    # Authorship stamp pre-write.
    body = _stamp_authorship(body, entity_type)

    # [2] Atomic write.
    path = entity_path(region, entity_type, entity_id)
    _atomic_write(path, _yaml_dump(body))

    # [3] Invariants — soft-block.
    try:
        lint_errors, lint_warnings = _run_invariants(region)
    except Exception as exc:  # pylint: disable=broad-except
        lint_errors = [f"invariant runner crashed: {type(exc).__name__}: {exc}"]
        lint_warnings = []

    # [4] Render.
    rc, msg = _render(region, entity_id)
    render_status = "ok" if rc == 0 else f"failed (rc={rc})"

    # [5] Git commit.
    msg_default = commit_message or f"edit: {region}/{entity_type}/{entity_id}"
    git_status = _git_commit(path, msg_default)

    return SaveReport(
        status="lint_failed" if lint_errors else "ok",
        lint_errors=lint_errors,
        lint_warnings=lint_warnings,
        render_status=render_status,
        render_message=msg,
        git_status=git_status,
        file_path=str(path.relative_to(_ROOT)),
    )
