"""Settings library — wave 4 item 9 (ζ).

See docs/CMS-IMPL-WAVE-4.md §9.

Five groups stored as JSON-blob rows in ``cms.db.settings`` (W4-1
ratified). On publish, an atomic export lands in
``instance/site_settings.json`` (W2-3 ratified: untracked path) and the
theme CSS is regenerated to ``static/theme.css`` (W4-2 ratified).

The Flask app's ``before_request`` hook + context processor consume the
exported JSON to populate ``g.site_settings`` and template context
(see app.py).
"""
from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any

from blueprints.admin.cms.db import get_cms_db


# ---------------- group registry ---------------------------------------

GROUPS: tuple[str, ...] = ("site", "nav", "theme", "contact", "footer", "analytics")

GROUP_LABELS: dict[str, str] = {
    "site":      "Site identity",
    "nav":       "Navigation",
    "theme":     "Theme tokens",
    "contact":   "Contact form",
    "footer":    "Footer",
    "analytics": "Analytics",
}

DEFAULTS: dict[str, Any] = {
    "site": {
        "name": "",
        "tagline": "",
        "url": "",
        "favicon": "",
        "og_image": "",
    },
    "nav": [
        # Each item: {"label": "...", "url": "..."}
    ],
    "theme": {
        "color": {
            "primary": "#1a73e8",
            "text":    "#222",
            "bg":      "#fff",
            "muted":   "#777",
        },
        "font_stack": "ui-sans-serif, system-ui, -apple-system, sans-serif",
        "max_width":  "70ch",
    },
    "contact": {
        "turnstile_site_key": "",
        "submit_url":         "",
    },
    "footer": {
        "copyright": "",
        "social":    [],
    },
    "analytics": {
        "provider":   "none",   # none | plausible | umami | ga4
        "site_id":    "",       # domain for Plausible; measurement ID for GA4
        "script_url": "",       # override auto-derived URL
        "honour_dnt": True,     # respect Do-Not-Track header
    },
}


# ---------------- DB-side k/v access -----------------------------------


def get_group(group: str) -> Any:
    """Read JSON-blob row; return DEFAULTS[group] if missing or unparsable."""
    if group not in GROUPS:
        raise ValueError(f"unknown settings group: {group!r}")
    conn = get_cms_db()
    row = conn.execute(
        "SELECT value FROM settings WHERE key = ?",
        (f"group.{group}",),
    ).fetchone()
    if row is None:
        return DEFAULTS[group]
    try:
        return json.loads(row["value"])
    except json.JSONDecodeError:
        return DEFAULTS[group]


def put_group(group: str, value: Any) -> None:
    """Write JSON-blob row. value must serialise to JSON."""
    if group not in GROUPS:
        raise ValueError(f"unknown settings group: {group!r}")
    blob = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    conn = get_cms_db()
    conn.execute(
        "INSERT INTO settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (f"group.{group}", blob),
    )


def all_groups() -> dict[str, Any]:
    """Return {group_name: parsed_blob} for every group, applying DEFAULTS."""
    return {g: get_group(g) for g in GROUPS}


# ---------------- publish (atomic export + theme regen) ----------------


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _site_settings_path() -> Path:
    return _project_root() / "instance" / "site_settings.json"


def _theme_css_path() -> Path:
    return _project_root() / "static" / "theme.css"


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def publish_settings() -> tuple[Path, Path]:
    """Export all groups to instance/site_settings.json + regen theme.css.

    Returns (site_settings_json_path, theme_css_path).
    """
    snapshot = all_groups()
    _atomic_write_text(
        _site_settings_path(),
        json.dumps(snapshot, ensure_ascii=False, indent=2),
    )
    css_path = regenerate_theme_css(snapshot.get("theme", DEFAULTS["theme"]))
    # Invalidate the in-process cache so the next request re-reads.
    _site_cache.invalidate()
    return _site_settings_path(), css_path


def regenerate_theme_css(override: dict | None = None) -> Path:
    """Compose preset ⊕ override and emit CSS (CMS v2 wave v2-4).

    Falls back to legacy behaviour (single-dict theme) when theme_preset
    is unset.
    """
    from blueprints.admin.cms import theme as theme_mod
    override = override if override is not None else get_group("theme")
    preset_name = get_active_preset()
    if preset_name in theme_mod.KNOWN_PRESETS:
        defaults = theme_mod.load_defaults()
        preset = theme_mod.load_preset(preset_name)
        composed = theme_mod.compose(theme_mod.compose(defaults, preset), override or {})
        composed = theme_mod.derive_spacing_scale(composed)
    else:
        composed = override or {}
    rules = list(_emit_css_vars(composed, prefix=""))
    body = ":root {\n" + "\n".join(f"  {r}" for r in rules) + "\n}\n"
    _atomic_write_text(_theme_css_path(), body)
    return _theme_css_path()


def get_active_preset() -> str:
    """Read the active preset name from cms.db.settings.theme_preset."""
    conn = get_cms_db()
    row = conn.execute(
        "SELECT value FROM settings WHERE key = ?",
        ("theme_preset",),
    ).fetchone()
    if row is None:
        return "classic"
    try:
        return json.loads(row["value"])
    except (json.JSONDecodeError, TypeError):
        return "classic"


def set_active_preset(name: str) -> None:
    """Persist the active preset name. Must be in KNOWN_PRESETS or 'custom'."""
    if name not in ("editorial", "documentary", "classic", "custom"):
        raise ValueError(f"unknown preset: {name!r}")
    conn = get_cms_db()
    conn.execute(
        "INSERT INTO settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        ("theme_preset", json.dumps(name)),
    )


def _emit_css_vars(value: Any, prefix: str):
    """Walk a nested dict and yield ``--<path>: <value>;`` lines.

    Hyphens replace dots in the CSS variable name. Lists are skipped at
    this level (theme tokens are k/v, not array-shaped). Non-strings
    are coerced via ``str()``.
    """
    if isinstance(value, dict):
        for k, v in value.items():
            sub_prefix = f"{prefix}-{k}" if prefix else k
            yield from _emit_css_vars(v, sub_prefix)
    elif isinstance(value, (str, int, float)) and not isinstance(value, bool):
        yield f"--{prefix.replace('.', '-')}: {value};"
    # else (list, bool, None): skip


def theme_css_cache_bust() -> str:
    """mtime-derived querystring fragment for cache busting (W4-2)."""
    p = _theme_css_path()
    if not p.is_file():
        return "0"
    return str(int(p.stat().st_mtime))


# ---------------- runtime cache for the Flask before_request hook ------


class _SiteSettingsCache:
    """Module-level mtime-keyed cache of the exported JSON snapshot."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._mtime: float | None = None
        self._snapshot: dict = {}

    def get_or_load(self) -> dict:
        path = _site_settings_path()
        if not path.is_file():
            return {}
        mtime = path.stat().st_mtime
        with self._lock:
            if mtime != self._mtime:
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        self._snapshot = json.load(f)
                except (OSError, json.JSONDecodeError):
                    self._snapshot = {}
                self._mtime = mtime
            return self._snapshot

    def invalidate(self) -> None:
        with self._lock:
            self._mtime = None
            self._snapshot = {}


_site_cache = _SiteSettingsCache()


def load_site_settings() -> dict:
    """Public entry point for the Flask before_request hook."""
    return _site_cache.get_or_load()


def effective(key: str, group: str = "contact",
              env_key: str | None = None) -> str | None:
    snapshot = load_site_settings()
    g = snapshot.get(group) or {}
    if isinstance(g, dict) and key in g and g[key] not in (None, ""):
        return str(g[key])
    return os.environ.get(env_key or key.upper())


def theme_css_cache_bust() -> str:
    """Return mtime of static/theme.css as a cache-bust string."""
    p = Path(__file__).resolve().parent.parent.parent.parent / "static" / "theme.css"
    try:
        return str(int(p.stat().st_mtime))
    except OSError:
        return "0"
