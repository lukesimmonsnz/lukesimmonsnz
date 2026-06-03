"""Theme-slot rendering — header / footer as MD (CMS v2 wave v2-6)."""
from __future__ import annotations

import os
from pathlib import Path

import markdown


_HERE = Path(__file__).resolve().parents[3]
CONTENT_DIR  = _HERE / "content" / "_theme"
RENDERED_DIR = _HERE / "templates" / "rendered" / "_theme"

KNOWN_SLOTS: tuple[str, ...] = ("header", "footer")


def _content_path(name: str) -> Path:
    return CONTENT_DIR / f"{name}.md"


def _rendered_path(name: str) -> Path:
    return RENDERED_DIR / f"{name}.html"


def _strip_frontmatter(text: str) -> str:
    """Strip leading --- ... --- frontmatter; return body."""
    if not text.startswith("---"):
        return text
    nl_pos = text.find("\n", 3)
    if nl_pos == -1:
        return text
    close = text.find("\n---\n", nl_pos)
    if close == -1:
        close = text.find("\n---\r\n", nl_pos)
        if close == -1:
            return text
        return text[close + len("\n---\r\n"):]
    return text[close + len("\n---\n"):]


def slot_render(name: str) -> str:
    """Return rendered HTML for slot `name`.

    Reads from the rendered cache when fresh; falls through to a
    runtime md→html convert if the cache is missing or stale.
    Returns "" when the slot is not defined.
    """
    src = _content_path(name)
    if not src.exists():
        return ""
    cache = _rendered_path(name)
    if not cache.exists() or cache.stat().st_mtime < src.stat().st_mtime:
        try:
            regenerate_slot_cache(name)
        except Exception:
            return ""
    try:
        return cache.read_text(encoding="utf-8")
    except OSError:
        return ""


def regenerate_slot_cache(name: str) -> Path:
    """Re-emit templates/rendered/_theme/<name>.html from <name>.md.

    Atomic write via os.replace.
    """
    src = _content_path(name)
    if not src.exists():
        raise FileNotFoundError(f"no theme slot at {src}")
    text = src.read_text(encoding="utf-8")
    body = _strip_frontmatter(text)
    html = markdown.markdown(body, extensions=["fenced_code", "tables"])
    out = _rendered_path(name)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text(html, encoding="utf-8")
    os.replace(tmp, out)
    return out


def regenerate_all_slots() -> dict[str, Path]:
    """Regenerate every slot's rendered cache. Used at app startup."""
    out: dict[str, Path] = {}
    for slot in KNOWN_SLOTS:
        if _content_path(slot).exists():
            try:
                out[slot] = regenerate_slot_cache(slot)
            except Exception:
                pass
    return out
