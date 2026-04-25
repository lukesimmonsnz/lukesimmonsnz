"""Entity graph loader for the Auckland knowledge base.

Loads all JSON schemas and YAML entity files under ``content/auckland/``,
validates each entity against its schema, and returns a Graph object that
render.py and lint.py consume. The loader is the single point of truth for
what entities exist and how they are typed.

Run as a script to dump a summary of the loaded graph:

    python tools/graph.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator


# Entity types recognised by the knowledge base, in load order.
# The order influences report output; it does not affect validation.
ENTITY_TYPES: tuple[str, ...] = (
    "source",
    "evidence",
    "driver",
    "response",
    "camp",
    "metric",
    "actor",
    "problem",
)

# Explicit mapping from entity type → data/ subdirectory name. Explicit because
# English pluralisation is irregular (evidence is a mass noun, not "evidences").
ENTITY_DIRS: dict[str, str] = {
    "source": "sources",
    "evidence": "evidence",
    "driver": "drivers",
    "response": "responses",
    "camp": "camps",
    "metric": "metrics",
    "actor": "actors",
    "problem": "problems",
}


@dataclass
class Graph:
    """In-memory representation of the loaded knowledge base."""

    root: Path
    schemas: dict[str, dict[str, Any]] = field(default_factory=dict)
    entities: dict[str, dict[str, Any]] = field(default_factory=dict)
    entities_by_type: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    validation_errors: list[str] = field(default_factory=list)

    def get(self, entity_id: str) -> dict[str, Any] | None:
        return self.entities.get(entity_id)

    def require(self, entity_id: str) -> dict[str, Any]:
        entity = self.entities.get(entity_id)
        if entity is None:
            raise KeyError(f"Unknown entity id: {entity_id}")
        return entity

    def all_of_type(self, entity_type: str) -> list[dict[str, Any]]:
        return list(self.entities_by_type.get(entity_type, []))

    def referenced_ids(self, entity: dict[str, Any]) -> Iterable[str]:
        """Yield every entity ID referenced by ``entity`` via *_ids fields and
        ``tensions_with`` / ``addresses`` / ``affects`` / ``measures`` fields."""
        id_fields = (
            "driver_ids",
            "camp_ids",
            "evidence_ids",
            "response_ids",
            "source_ids",
            "tensions_with",
            "addresses",
            "affects",
            "measures",
        )
        for field_name in id_fields:
            value = entity.get(field_name)
            if isinstance(value, list):
                yield from value


def _load_schemas(schema_dir: Path) -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    for path in sorted(schema_dir.glob("*.schema.json")):
        with path.open("r", encoding="utf-8") as handle:
            schema = json.load(handle)
        # Derive entity type from filename: "problem.schema.json" -> "problem"
        entity_type = path.stem.split(".", 1)[0]
        schemas[entity_type] = schema
    return schemas


def _entity_type_from_id(entity_id: str) -> str:
    return entity_id.split(".", 1)[0]


def _load_entity_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: YAML root must be a mapping, got {type(data).__name__}")
    if "id" not in data:
        raise ValueError(f"{path}: entity is missing required 'id' field")
    return data


def load_graph(root: Path | str | None = None) -> Graph:
    """Load schemas and entities from ``root`` (defaults to the parent of
    this tools/ directory). Validates each entity against the schema matching
    its type prefix; validation failures are recorded on ``Graph.validation_errors``
    rather than raised, so callers can choose how to surface them.
    """
    if root is None:
        root = Path(__file__).resolve().parent.parent
    root = Path(root)

    schema_dir = root / "schema"
    data_dir = root / "data"

    graph = Graph(root=root)
    graph.schemas = _load_schemas(schema_dir)

    for entity_type in ENTITY_TYPES:
        type_dir = data_dir / ENTITY_DIRS[entity_type]
        if not type_dir.is_dir():
            continue
        schema = graph.schemas.get(entity_type)
        validator = Draft202012Validator(schema) if schema else None
        for path in sorted(type_dir.glob("*.yaml")):
            try:
                entity = _load_entity_file(path)
            except (yaml.YAMLError, ValueError) as exc:
                graph.validation_errors.append(f"{path}: {exc}")
                continue

            derived_type = _entity_type_from_id(entity["id"])
            if derived_type != entity_type:
                graph.validation_errors.append(
                    f"{path}: id '{entity['id']}' does not match type directory '{entity_type}s'"
                )
                continue

            if validator is not None:
                for error in validator.iter_errors(entity):
                    path_segments = "/".join(str(p) for p in error.absolute_path) or "<root>"
                    graph.validation_errors.append(
                        f"{path}: schema error at {path_segments}: {error.message}"
                    )

            if entity["id"] in graph.entities:
                graph.validation_errors.append(
                    f"{path}: duplicate entity id '{entity['id']}'"
                )
                continue

            graph.entities[entity["id"]] = entity
            graph.entities_by_type.setdefault(entity_type, []).append(entity)

    return graph


def _summarise(graph: Graph) -> str:
    lines = [f"Auckland knowledge base at {graph.root}", ""]
    for entity_type in ENTITY_TYPES:
        count = len(graph.entities_by_type.get(entity_type, []))
        lines.append(f"  {entity_type:<10} {count:>4}")
    lines.append(f"  {'TOTAL':<10} {len(graph.entities):>4}")
    if graph.validation_errors:
        lines.append("")
        lines.append(f"Validation errors ({len(graph.validation_errors)}):")
        for msg in graph.validation_errors:
            lines.append(f"  - {msg}")
    return "\n".join(lines)


if __name__ == "__main__":
    graph = load_graph()
    print(_summarise(graph))
    sys.exit(1 if graph.validation_errors else 0)
