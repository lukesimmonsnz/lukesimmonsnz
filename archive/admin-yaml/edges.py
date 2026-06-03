"""Edge registry loader.

Reads ``content/_schema/edges.yaml`` once at import time and exposes a
typed lookup. Centralising the load avoids repeated disk reads from the
schema walker and the autocomplete endpoint.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal, TypedDict

import yaml

_EDGES_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "content" / "_schema" / "edges.yaml"
)


class EdgeSpec(TypedDict):
    target: str | list[str]
    arity: Literal["one", "many"]
    scope: Literal["region", "union", "nz"]


def _load() -> dict[str, dict[str, EdgeSpec]]:
    with _EDGES_PATH.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    # Light validation — meta-schema is left as a PI delta.
    for entity_type, fields in data.items():
        if not isinstance(fields, dict):
            raise ValueError(f"edges.yaml: {entity_type!r} must map field→spec")
        for field, spec in fields.items():
            for key in ("target", "arity", "scope"):
                if key not in spec:
                    raise ValueError(
                        f"edges.yaml: {entity_type}.{field} missing {key!r}"
                    )
            if spec["arity"] not in ("one", "many"):
                raise ValueError(
                    f"edges.yaml: {entity_type}.{field}.arity invalid"
                )
            if spec["scope"] not in ("region", "union", "nz"):
                raise ValueError(
                    f"edges.yaml: {entity_type}.{field}.scope invalid"
                )
    return data


EDGES: dict[str, dict[str, EdgeSpec]] = _load()


def edge_for(entity_type: str, field: str) -> EdgeSpec | None:
    return EDGES.get(entity_type, {}).get(field)
