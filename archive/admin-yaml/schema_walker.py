"""Schema walker — implementation of φ̂ (DASHBOARD-SPEC.md §4.1).

Formal contract
---------------
For an entity type T with JSON Schema 𝒮_T, the form 𝓕_T is the direct
sum of widget realisations of each top-level property:

    𝓕_T = ⊕_{p ∈ properties(𝒮_T)}  φ̂(p, 𝒮_T[p])

φ̂ is structural-recursive: nested objects recurse, arrays dispatch on
their item subschema, and ref-typed fields consult the edge registry
(``edges.py``) to obtain (target, arity, scope).

Output type
-----------
``schema_to_form`` returns ``list[FormField]``, where each ``FormField``
is a flat dict the Jinja partial ``_form.html`` consumes. The flat shape
keeps the template trivially loopable and lets nested fieldsets surface
as ``widget == "fieldset"`` records that carry their own children list.

Implementation gap (preserved per CLAUDE.md §2)
-----------------------------------------------
The widget-selection table for primitive leaves is implemented; the two
genuinely interesting cases — (a) the ``oneOf``/``anyOf`` discriminator
collapse, and (b) `intensity_by_region`-style enum-keyed objects — are
left as ``NotImplementedError`` stubs with their contracts documented in
the relevant branches. The PI completes those to retain mastery of the
form-generation logic.
"""
from __future__ import annotations

from typing import Any

from blueprints.admin.edges import edge_for

# Threshold above which `string` fields render as <textarea>.
_TEXTAREA_THRESHOLD = 200


def schema_to_form(
    schema: dict[str, Any],
    *,
    entity_type: str,
    path: tuple[str, ...] = (),
) -> list[dict[str, Any]]:
    """Top-level entry point.

    Parameters
    ----------
    schema : the JSON Schema dict (already loaded; no $ref resolution
        is performed beyond what the schema author wrote — Region and
        Theme refs are surfaced as 'enum-via-ref' fields).
    entity_type : the schema's entity type, e.g. ``"claim"``. Used to
        consult the edge registry for ref-typed array fields.
    path : breadcrumb of property names; populated by recursion. The
        public caller passes ``()``.
    """
    properties = schema.get("properties", {}) or {}
    required = set(schema.get("required", []) or [])
    fields: list[dict[str, Any]] = []
    for name, subschema in properties.items():
        fields.append(
            _phi(
                name=name,
                subschema=subschema,
                required=name in required,
                entity_type=entity_type,
                path=path + (name,),
            )
        )
    return fields


# ---------------------------------------------------------------------------
# φ̂ — widget selection
# ---------------------------------------------------------------------------

def _phi(
    *,
    name: str,
    subschema: dict[str, Any],
    required: bool,
    entity_type: str,
    path: tuple[str, ...],
) -> dict[str, Any]:
    """Single-property widget selector. Return shape: see _make_field."""

    # 1. oneOf / anyOf — discriminator collapse.
    #
    # Spec (§4.1): emit a discriminator <select> whose value swaps the
    # inner widget. The PI must decide how to surface the discriminator
    # label (use 'title' on each branch? a sidecar mapping?).
    if "oneOf" in subschema or "anyOf" in subschema:
        raise NotImplementedError(
            f"oneOf/anyOf at {'.'.join(path)} — PI: pick discriminator strategy "
            "(title-based vs sidecar) and implement branch-swap widget."
        )

    # 2. $ref to Region / Theme — these are external enums.
    ref = subschema.get("$ref")
    if ref:
        return _make_field(
            name=name, path=path, required=required,
            widget="ref-enum", target=ref,
            description=subschema.get("description", ""),
        )

    # 3. Type dispatch.
    type_ = subschema.get("type")
    # nullable-by-list, e.g. ["string", "null"]
    if isinstance(type_, list):
        nullable = "null" in type_
        non_null = [t for t in type_ if t != "null"]
        primary = non_null[0] if non_null else "string"
    else:
        nullable = False
        primary = type_

    # 3a. enum (string with enum, or bare).
    if "enum" in subschema:
        return _make_field(
            name=name, path=path, required=required, nullable=nullable,
            widget="select",
            choices=list(subschema["enum"]),
            default=subschema.get("default"),
            description=subschema.get("description", ""),
        )

    # 3b. boolean.
    if primary == "boolean":
        return _make_field(
            name=name, path=path, required=required, nullable=nullable,
            widget="checkbox",
            default=subschema.get("default", False),
            description=subschema.get("description", ""),
        )

    # 3c. integer / number.
    if primary in ("integer", "number"):
        return _make_field(
            name=name, path=path, required=required, nullable=nullable,
            widget="number",
            minimum=subschema.get("minimum"),
            maximum=subschema.get("maximum"),
            step=1 if primary == "integer" else "any",
            default=subschema.get("default"),
            description=subschema.get("description", ""),
        )

    # 3d. string.
    if primary == "string":
        if subschema.get("format") == "date":
            widget = "date"
        elif subschema.get("pattern", "").startswith("^") and not _is_freeform(subschema):
            # Pattern-constrained scalar that points at another entity
            # (e.g. ``methodology_tag`` with pattern ^methodology\.…). The
            # edge registry resolves the target.
            edge = edge_for(entity_type, name)
            if edge:
                return _make_field(
                    name=name, path=path, required=required, nullable=nullable,
                    widget="ref-autocomplete",
                    target=edge["target"], arity=edge["arity"], scope=edge["scope"],
                    description=subschema.get("description", ""),
                )
            widget = "text"
        elif _is_long_string(subschema):
            widget = "textarea"
        else:
            widget = "text"
        return _make_field(
            name=name, path=path, required=required, nullable=nullable,
            widget=widget,
            pattern=subschema.get("pattern"),
            default=subschema.get("default"),
            description=subschema.get("description", ""),
        )

    # 3e. array.
    if primary == "array":
        items = subschema.get("items", {}) or {}
        # Polymorphic items via list (unusual) — surface as JSON textarea.
        if isinstance(items, list):
            return _make_field(
                name=name, path=path, required=required,
                widget="json-array",
                description=subschema.get("description", ""),
            )
        # Array of refs (the typical edge case): tag input with autocomplete.
        item_ref = items.get("$ref")
        item_pattern = items.get("pattern", "")
        edge = edge_for(entity_type, name)
        if edge or item_ref or item_pattern.startswith("^"):
            return _make_field(
                name=name, path=path, required=required,
                widget="tag-autocomplete",
                target=(edge["target"] if edge else item_ref or item_pattern),
                scope=(edge["scope"] if edge else "region"),
                min_items=subschema.get("minItems"),
                unique=subschema.get("uniqueItems", False),
                description=subschema.get("description", ""),
            )
        # Array of enums.
        if "enum" in items:
            return _make_field(
                name=name, path=path, required=required,
                widget="multiselect",
                choices=list(items["enum"]),
                description=subschema.get("description", ""),
            )
        # Array of objects (e.g. Camp.interventions) — recurse on item shape
        # and emit a "repeating-fieldset" widget. Children carried inline.
        if items.get("type") == "object":
            return _make_field(
                name=name, path=path, required=required,
                widget="repeating-fieldset",
                children=schema_to_form(items, entity_type=entity_type, path=path),
                min_items=subschema.get("minItems"),
                description=subschema.get("description", ""),
            )
        # Array of plain strings.
        return _make_field(
            name=name, path=path, required=required,
            widget="tag-input",
            min_items=subschema.get("minItems"),
            unique=subschema.get("uniqueItems", False),
            description=subschema.get("description", ""),
        )

    # 3f. object — nested fieldset (recurse).
    if primary == "object":
        # additionalProperties with a typed value indicates an
        # enum-keyed map (e.g. Driver.intensity_by_region). PI gap:
        # decide whether keys come from a Region enum dropdown plus
        # value input, or from a paired (key, value) row repeater.
        if subschema.get("additionalProperties") and not subschema.get("properties"):
            raise NotImplementedError(
                f"enum-keyed map at {'.'.join(path)} — PI: implement Region-keyed "
                "row repeater for intensity_by_region-style fields."
            )
        return _make_field(
            name=name, path=path, required=required,
            widget="fieldset",
            children=schema_to_form(subschema, entity_type=entity_type, path=path),
            description=subschema.get("description", ""),
        )

    # 3g. fall-through.
    return _make_field(
        name=name, path=path, required=required,
        widget="text",
        description=subschema.get("description", ""),
    )


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _make_field(**kwargs: Any) -> dict[str, Any]:
    """Normalise a field record. Drops keys whose value is None so the
    Jinja template can use {% if field.foo %} cleanly."""
    return {k: v for k, v in kwargs.items() if v is not None}


def _is_long_string(subschema: dict[str, Any]) -> bool:
    max_len = subschema.get("maxLength")
    if isinstance(max_len, int) and max_len > _TEXTAREA_THRESHOLD:
        return True
    description = subschema.get("description", "") or ""
    # Heuristic: fields described as 'paragraph', 'narrative', or 'description'
    # render long-form even without an explicit maxLength.
    return any(k in description.lower() for k in ("paragraph", "narrative", "description text"))


def _is_freeform(subschema: dict[str, Any]) -> bool:
    """A pattern-constrained string is ref-like unless its pattern is
    obviously freeform (e.g. just ``^.*$``)."""
    p = subschema.get("pattern", "") or ""
    return p in ("", "^.*$", ".*")
