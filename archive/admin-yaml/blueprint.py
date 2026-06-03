"""Admin blueprint — DASHBOARD-SPEC.md §3 URL surface, §11 routes.

Localhost-gated per §0 row 1 (topology B).
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml
from flask import (
    Blueprint, abort, jsonify, render_template, request, url_for,
)

from blueprints.admin.edges import EDGES
from blueprints.admin.save_pipeline import (
    SaveReport, entity_path, save_entity, validate,
)
from blueprints.admin.schema_walker import schema_to_form
from content._render import REGIONS, render

admin_bp = Blueprint(
    "admin", __name__,
    url_prefix="/admin",
    template_folder="../../templates/admin",
)

_ROOT = Path(__file__).resolve().parent.parent.parent
_SCHEMA_DIR = _ROOT / "content" / "_schema"

# Entity types whose data lives under content/<region>/data/<type>/.
ENTITY_TYPES: tuple[str, ...] = (
    "claim", "problem", "driver", "camp",
    "source", "methodology", "response",
    "actor", "indicator", "ibis_node",
)

# Pretty labels for the home grid.
REGION_LABEL: dict[str, str] = {
    "auckland": "Auckland",
    "bay-of-plenty": "Bay of Plenty",
    "canterbury": "Canterbury",
    "gisborne": "Gisborne",
    "hawkes-bay": "Hawke's Bay",
    "manawatu-whanganui": "Manawatū-Whanganui",
    "marlborough": "Marlborough",
    "nelson": "Nelson",
    "northland": "Northland",
    "otago": "Otago",
    "southland": "Southland",
    "taranaki": "Taranaki",
    "tasman": "Tasman",
    "waikato": "Waikato",
    "wellington": "Wellington",
    "west-coast": "West Coast",
}


# ---------------------------------------------------------------------------
# Localhost gate (§0 row 1).
# ---------------------------------------------------------------------------

@admin_bp.before_request
def _localhost_only():
    if request.remote_addr not in {"127.0.0.1", "::1"}:
        abort(404)


# ---------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _load_schema(entity_type: str) -> dict:
    path = _SCHEMA_DIR / f"{entity_type}.schema.json"
    if not path.is_file():
        abort(404, description=f"unknown entity type {entity_type!r}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _list_entities(region: str, entity_type: str) -> list[dict]:
    data_dir = _ROOT / "content" / region / "data" / entity_type
    if not data_dir.is_dir():
        return []
    out = []
    for p in sorted(data_dir.glob("*.yaml")):
        body = _load_yaml(p)
        if not body:
            continue
        out.append({
            "id": body.get("id", p.stem),
            "title": body.get("title") or body.get("name") or body.get("statement", "")[:80],
            "theme": body.get("theme") or body.get("section") or "",
            "filename": p.name,
        })
    return out


def _region_themes(region: str) -> list[str]:
    """Themes are derived from entity ID prefixes under data/problem/."""
    problems_dir = _ROOT / "content" / region / "data" / "problem"
    if not problems_dir.is_dir():
        return []
    themes = set()
    for p in problems_dir.glob("*.yaml"):
        # Filename convention: <theme>.<slug>.yaml
        parts = p.stem.split(".")
        if parts:
            themes.add(parts[0])
    return sorted(themes)


def _form_from_yaml(body: dict, fields: list[dict]) -> list[dict]:
    """Bind current YAML values onto the φ̂ field list for rendering."""
    bound = []
    for f in fields:
        # Path is a tuple of property names; for top-level fields path[-1]
        # equals the YAML key.
        key = f["name"]
        f = dict(f)
        f["value"] = body.get(key)
        bound.append(f)
    return bound


# ---------------------------------------------------------------------------
# Routes.
# ---------------------------------------------------------------------------

@admin_bp.route("/")
def home():
    return render_template(
        "admin/home.html",
        regions=[(r, REGION_LABEL[r]) for r in REGIONS],
        entity_types=ENTITY_TYPES,
    )


@admin_bp.route("/region/<region>/")
def region_view(region: str):
    if region not in REGIONS:
        abort(404)
    themes = _region_themes(region)
    counts = {
        et: len(list((_ROOT / "content" / region / "data" / et).glob("*.yaml")))
        if (_ROOT / "content" / region / "data" / et).is_dir() else 0
        for et in ENTITY_TYPES
    }
    return render_template(
        "admin/region.html",
        region=region,
        region_label=REGION_LABEL[region],
        themes=themes,
        counts=counts,
        entity_types=ENTITY_TYPES,
    )


@admin_bp.route("/region/<region>/<entity_type>/")
def list_view(region: str, entity_type: str):
    if region not in REGIONS or entity_type not in ENTITY_TYPES:
        abort(404)
    entities = _list_entities(region, entity_type)
    theme_filter = request.args.get("theme")
    if theme_filter:
        entities = [
            e for e in entities
            if e["id"].startswith(f"{entity_type}.{theme_filter}.")
            or e["theme"] == theme_filter
        ]
    return render_template(
        "admin/theme.html",
        region=region,
        region_label=REGION_LABEL[region],
        entity_type=entity_type,
        entities=entities,
        theme_filter=theme_filter or "",
    )


@admin_bp.route("/entity/<region>/<entity_type>/<path:entity_id>/", methods=["GET", "POST"])
def edit_entity(region: str, entity_type: str, entity_id: str):
    if region not in REGIONS or entity_type not in ENTITY_TYPES:
        abort(404)
    schema = _load_schema(entity_type)
    path = entity_path(region, entity_type, entity_id)
    body = _load_yaml(path)

    if request.method == "POST":
        # Form submission posts a JSON blob in field "_yaml" to sidestep
        # form-encoding ambiguity for arrays/objects. v1 contract: the
        # client serialises the assembled body as YAML or JSON text.
        raw = request.form.get("_yaml", "").strip()
        try:
            new_body = yaml.safe_load(raw) or {}
        except yaml.YAMLError as exc:
            return render_template(
                "admin/entity.html",
                region=region, region_label=REGION_LABEL[region],
                entity_type=entity_type, entity_id=entity_id,
                fields=_form_from_yaml(body, schema_to_form(schema, entity_type=entity_type)),
                raw_yaml=raw,
                report=SaveReport(status="schema_failed",
                                  schema_errors=[f"YAML parse error: {exc}"]),
            )
        report = save_entity(region, entity_type, entity_id, new_body)
        return render_template(
            "admin/entity.html",
            region=region, region_label=REGION_LABEL[region],
            entity_type=entity_type, entity_id=entity_id,
            fields=_form_from_yaml(new_body, schema_to_form(schema, entity_type=entity_type)),
            raw_yaml=yaml.safe_dump(new_body, sort_keys=False, allow_unicode=True),
            report=report,
        )

    fields = schema_to_form(schema, entity_type=entity_type)
    return render_template(
        "admin/entity.html",
        region=region, region_label=REGION_LABEL[region],
        entity_type=entity_type, entity_id=entity_id,
        fields=_form_from_yaml(body, fields),
        raw_yaml=yaml.safe_dump(body, sort_keys=False, allow_unicode=True) if body else "",
        report=None,
    )


@admin_bp.route("/api/validate", methods=["POST"])
def api_validate():
    """L1 lint depth (§6) — schema-only, called per-edit by the client."""
    payload = request.get_json(silent=True) or {}
    entity_type = payload.get("entity_type", "")
    body = payload.get("body", {})
    if entity_type not in ENTITY_TYPES:
        return jsonify({"errors": [f"unknown entity_type {entity_type!r}"]}), 400
    return jsonify({"errors": validate(entity_type, body)})


@admin_bp.route("/api/autocomplete")
def api_autocomplete():
    """Reference autocomplete for ref-typed fields. Query string:
        ?entity_type=claim&field=source_ids&region=auckland&q=hous
    """
    entity_type = request.args.get("entity_type", "")
    field = request.args.get("field", "")
    region = request.args.get("region", "")
    query = request.args.get("q", "").lower()
    edge = EDGES.get(entity_type, {}).get(field)
    if not edge:
        return jsonify([])
    target = edge["target"] if isinstance(edge["target"], str) else edge["target"][0]
    scope = edge["scope"]
    candidates: list[dict] = []
    if scope == "region":
        candidates.extend(_list_entities(region, target))
    elif scope == "nz":
        # Pattern lives at content/nz/data/pattern/.
        nz_dir = _ROOT / "content" / "nz" / "data" / target
        if nz_dir.is_dir():
            for p in nz_dir.glob("*.yaml"):
                body = _load_yaml(p)
                candidates.append({
                    "id": body.get("id", p.stem),
                    "title": body.get("title") or body.get("name") or "",
                    "filename": p.name,
                })
    else:  # union
        for r in REGIONS:
            candidates.extend(_list_entities(r, target))
    if query:
        candidates = [
            c for c in candidates
            if query in c["id"].lower() or query in (c.get("title") or "").lower()
        ]
    return jsonify(candidates[:30])


@admin_bp.route("/api/render", methods=["POST"])
def api_render():
    payload = request.get_json(silent=True) or {}
    region = payload.get("region", "")
    entity_id = payload.get("entity_id")
    if region not in REGIONS:
        return jsonify({"status": "error", "message": "unknown region"}), 400
    rc = render(region, entity_id)
    return jsonify({"status": "ok" if rc == 0 else "failed", "rc": rc})
