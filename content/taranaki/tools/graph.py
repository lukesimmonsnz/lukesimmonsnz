"""Entity graph loader for the Wellington knowledge base.

Loads all JSON schemas from ``content/_schema/`` and YAML entity files
from ``content/wellington/data/``, validates each entity against its schema,
and returns a WellingtonGraph object satisfying the Graph Protocol defined in
``content/_schema/invariants.py``.

Run as a script to dump a summary of the loaded graph::

    python content/wellington/tools/graph.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

# ---------------------------------------------------------------------------
# Entity type configuration
# ---------------------------------------------------------------------------

# Recognised entity types, in load order (affects report output only).
ENTITY_TYPES: tuple[str, ...] = (
    "source",
    "methodology",
    "claim",
    "driver",
    "camp",
    "problem",
    # future: "actor", "indicator", "ibis_node", "pattern", "response"
)

# Entity type → data/ sub-directory (all regular plurals for new schema).
ENTITY_DIRS: dict[str, str] = {
    "source": "source",
    "methodology": "methodology",
    "claim": "claim",
    "driver": "driver",
    "camp": "camp",
    "problem": "problem",
}

# Known ID-bearing fields across all entity types.
# Single-value ID fields (str | None) and list-of-ID fields (list[str]).
_SINGLE_ID_FIELDS: frozenset[str] = frozenset({
    "methodology_tag",   # claim
    "supersedes_id",     # claim
    "parent",            # problem (references another problem)
})

_LIST_ID_FIELDS: frozenset[str] = frozenset({
    "source_ids",        # claim
    "claim_ids",         # driver, camp, problem
    "problem_ids",       # driver
    "addresses",         # camp
    "tensions_with",     # camp
    "invokes_ids",       # claim (optional cross-claim relation)
    "actor_ids",         # camp (future)
})

# Prefixes that identify a string as an entity ID (not a plain string).
_ID_PREFIXES: tuple[str, ...] = (
    "actor.", "camp.", "claim.", "driver.", "ibis.", "indicator.",
    "methodology.", "pattern.", "problem.", "response.", "source.",
)


# ---------------------------------------------------------------------------
# Graph dataclass
# ---------------------------------------------------------------------------

@dataclass
class WellingtonGraph:
    """In-memory graph satisfying ``content._schema.invariants.Graph`` Protocol.

    Attributes
    ----------
    root : Path
        Root directory of the Wellington content (contains ``data/`` and
        ``tools/``).
    schema_root : Path
        Shared schema directory (``content/_schema/``).
    schemas : dict[str, dict]
        Loaded JSON Schema objects, keyed by entity type.
    entities : dict[str, dict]
        All loaded entities, keyed by ``id``.
    entities_by_type : dict[str, list[dict]]
        Same entities partitioned by type prefix.
    validation_errors : list[str]
        Schema validation errors accumulated during loading.
    """

    root: Path
    schema_root: Path
    schemas: dict[str, dict[str, Any]] = field(default_factory=dict)
    entities: dict[str, dict[str, Any]] = field(default_factory=dict)
    entities_by_type: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    validation_errors: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Graph Protocol implementation
    # ------------------------------------------------------------------

    def all_of_type(self, entity_type: str) -> list[dict[str, Any]]:
        """Return all entities whose ``id`` prefix matches *entity_type*.

        E.g. ``all_of_type("claim")`` returns every entity whose id starts
        with ``"claim."``.
        """
        return list(self.entities_by_type.get(entity_type, []))

    def referenced_ids(self, entity: dict[str, Any]) -> set[str]:
        """Return the set of all entity IDs referenced by *entity*.

        Implements ``refs(v)`` from the schema design: collects every value
        matching ``^<type>\\.`` pattern from all known ID-bearing fields.
        """
        refs: set[str] = set()

        for fname in _SINGLE_ID_FIELDS:
            val = entity.get(fname)
            if isinstance(val, str) and any(val.startswith(p) for p in _ID_PREFIXES):
                refs.add(val)

        for fname in _LIST_ID_FIELDS:
            val = entity.get(fname)
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, str) and any(item.startswith(p) for p in _ID_PREFIXES):
                        refs.add(item)

        return refs

    def populated_region_count(self) -> int:
        """Return the number of distinct Region values present in the graph.

        A region is "populated" if it appears in at least one entity's
        ``scoped_to``, ``manifests_in``, or ``applicable_in`` field.
        """
        regions: set[str] = set()
        region_fields = ("scoped_to", "manifests_in", "applicable_in")
        for entity in self.entities.values():
            for fname in region_fields:
                val = entity.get(fname)
                if isinstance(val, list):
                    regions.update(val)
                elif isinstance(val, str):
                    regions.add(val)
        return len(regions)

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------

    def get(self, entity_id: str) -> dict[str, Any] | None:
        return self.entities.get(entity_id)

    def require(self, entity_id: str) -> dict[str, Any]:
        entity = self.entities.get(entity_id)
        if entity is None:
            raise KeyError(f"Unknown entity id: {entity_id!r}")
        return entity


# ---------------------------------------------------------------------------
# Loading helpers
# ---------------------------------------------------------------------------

def _load_schemas(schema_root: Path) -> dict[str, dict[str, Any]]:
    """Load all *.schema.json files from schema_root; key by entity type."""
    schemas: dict[str, dict[str, Any]] = {}
    for path in sorted(schema_root.glob("*.schema.json")):
        with path.open("r", encoding="utf-8") as fh:
            schema = json.load(fh)
        # Derive entity type from filename stem: "camp.schema.json" → "camp"
        entity_type = path.stem.split(".", 1)[0]
        schemas[entity_type] = schema
    return schemas


def _entity_type_from_id(entity_id: str) -> str:
    return entity_id.split(".", 1)[0]


def _load_entity_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: YAML root must be a mapping, got {type(data).__name__}")
    if "id" not in data:
        raise ValueError(f"{path}: entity is missing required 'id' field")
    return data


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_graph(root: Path | str | None = None,
               schema_root: Path | str | None = None) -> WellingtonGraph:
    """Load schemas and entities; return a validated WellingtonGraph.

    Parameters
    ----------
    root : Path, optional
        Wellington content root (directory containing ``data/`` and
        ``tools/``).  Defaults to the parent of this file.
    schema_root : Path, optional
        Shared schema directory.  Defaults to
        ``<repo_root>/content/_schema/``.

    Schema validation failures are recorded in
    ``WellingtonGraph.validation_errors`` rather than raised, so callers
    can decide how to surface them.
    """
    if root is None:
        root = Path(__file__).resolve().parent.parent
    root = Path(root)

    if schema_root is None:
        # Derive: content/wellington/ → content/ → content/_schema/
        schema_root = root.parent / "_schema"
    schema_root = Path(schema_root)

    data_dir = root / "data"
    graph = WellingtonGraph(root=root, schema_root=schema_root)
    graph.schemas = _load_schemas(schema_root)

    for entity_type in ENTITY_TYPES:
        type_dir = data_dir / ENTITY_DIRS[entity_type]
        if not type_dir.is_dir():
            continue

        schema = graph.schemas.get(entity_type)
        # Build a validator with URI resolution disabled (schemas use
        # aotearoa:// URIs that don't resolve to http; we validate
        # individual entities against the top-level schema only).
        validator: Draft202012Validator | None = None
        if schema is not None:
            # Strip $ref URIs we can't resolve (region/theme sub-schemas)
            # by using a resolver that silently accepts all URIs.
            from jsonschema import RefResolver
            store: dict[str, Any] = {}
            # Pre-load all sibling schemas into the store so $ref resolution
            # works for in-directory cross-references.
            for sibling in sorted(schema_root.glob("*.schema.json")):
                with sibling.open("r", encoding="utf-8") as fh:
                    sib_schema = json.load(fh)
                sib_id = sib_schema.get("$id", sibling.name)
                store[sib_id] = sib_schema

            resolver = RefResolver(
                base_uri=schema.get("$id", ""),
                referrer=schema,
                store=store,
            )
            validator = Draft202012Validator(schema, resolver=resolver)

        for path in sorted(type_dir.glob("*.yaml")):
            try:
                entity = _load_entity_file(path)
            except (yaml.YAMLError, ValueError) as exc:
                graph.validation_errors.append(f"{path}: {exc}")
                continue

            derived_type = _entity_type_from_id(entity["id"])
            if derived_type != entity_type:
                graph.validation_errors.append(
                    f"{path}: id {entity['id']!r} does not match "
                    f"expected type {entity_type!r}"
                )
                continue

            if validator is not None:
                for error in validator.iter_errors(entity):
                    seg = "/".join(str(p) for p in error.absolute_path) or "<root>"
                    graph.validation_errors.append(
                        f"{path.name}: schema error at {seg}: {error.message}"
                    )

            if entity["id"] in graph.entities:
                graph.validation_errors.append(
                    f"{path}: duplicate entity id {entity['id']!r}"
                )
                continue

            graph.entities[entity["id"]] = entity
            graph.entities_by_type.setdefault(entity_type, []).append(entity)

    return graph


# ---------------------------------------------------------------------------
# CLI summary
# ---------------------------------------------------------------------------

def _summarise(graph: WellingtonGraph) -> str:
    lines = [f"Wellington knowledge base at {graph.root}", ""]
    total = 0
    for entity_type in ENTITY_TYPES:
        count = len(graph.entities_by_type.get(entity_type, []))
        total += count
        lines.append(f"  {entity_type:<12} {count:>4}")
    lines.append(f"  {'TOTAL':<12} {total:>4}")
    lines.append(f"  populated regions: {graph.populated_region_count()}")
    if graph.validation_errors:
        lines.append("")
        lines.append(f"Schema validation errors ({len(graph.validation_errors)}):")
        for msg in graph.validation_errors[:40]:
            lines.append(f"  - {msg}")
        if len(graph.validation_errors) > 40:
            lines.append(f"  ... and {len(graph.validation_errors) - 40} more")
    return "\n".join(lines)


if __name__ == "__main__":
    _graph = load_graph()
    print(_summarise(_graph))
    sys.exit(1 if _graph.validation_errors else 0)
