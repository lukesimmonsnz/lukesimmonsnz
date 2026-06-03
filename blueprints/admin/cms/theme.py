"""Theme preset loader + composer (CMS v2 wave v2-4)."""
from __future__ import annotations

from pathlib import Path
import yaml


_HERE = Path(__file__).resolve().parents[3]
PRESETS_DIR   = _HERE / "content" / "_themes"
DEFAULTS_PATH = PRESETS_DIR / "defaults.yaml"

KNOWN_PRESETS: tuple[str, ...] = ("editorial", "documentary", "classic")
SPACING_PHI:   tuple[float, ...] = (0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16)


def load_preset(name: str) -> dict:
    """Load a preset YAML into a nested dict."""
    if name not in KNOWN_PRESETS:
        raise ValueError(f"unknown preset: {name!r}")
    path = PRESETS_DIR / f"{name}.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: root must be a mapping")
    return raw


def load_defaults() -> dict:
    """Fall-through token values."""
    raw = yaml.safe_load(DEFAULTS_PATH.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else {}


def compose(base: dict, overlay: dict) -> dict:
    """Right-biased deep merge with the empty-as-inherit rule.

    Mathematical contract:
        compose(base, {})         == base                       (identity)
        compose(a, b)[k] = b[k]   if k in b and b[k] not in {None, ""}
                         = compose(a[k], b[k])  if both dicts
                         = a[k]   otherwise
    """
    out: dict = dict(base)
    for k, v in overlay.items():
        if v is None or v == "":
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = compose(out[k], v)
        else:
            out[k] = v
    return out


def derive_spacing_scale(theme: dict) -> dict:
    """If spacing.unit is set, compute missing spacing.scale-N values
    from u * SPACING_PHI[N], emitted as '<int>px'.

    Returns a new dict (does not mutate input). Explicit scale-N values
    in the input are preserved.
    """
    out = dict(theme)
    spacing = dict(out.get("spacing") or {})
    unit_str = str(spacing.get("unit", "")).strip()
    if not unit_str:
        return out
    # Parse "8px" / "4px" → integer base.
    if unit_str.endswith("px"):
        try:
            u = float(unit_str[:-2])
        except ValueError:
            return out
    else:
        try:
            u = float(unit_str)
        except ValueError:
            return out
    for i, phi in enumerate(SPACING_PHI):
        key = f"scale-{i}"
        if key not in spacing or spacing[key] in (None, ""):
            spacing[key] = f"{u * phi:g}px"
    out["spacing"] = spacing
    return out
