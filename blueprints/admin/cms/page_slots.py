"""Page slots — promoted Jinja pages as MD (CMS v3 wave v3-1..3).

Generalisation of theme_slots.py for v3 page promotion.

When jinja_env is available (passed from app.jinja_env at startup, or
sourced from flask.current_app at request time), Markdown bodies are
rendered through blocks/renderer.py::render_md_with_blocks so v2-1
directive blocks (::section-hero, ::callout, etc.) dispatch through the
templates/blocks/<kind>.html partials. When jinja_env is None, falls
through to plain markdown.markdown for back-compat.
"""
from __future__ import annotations

import os
from pathlib import Path

import markdown


_HERE = Path(__file__).resolve().parents[3]
PAGES_CONTENT_DIR  = _HERE / "content" / "_pages"
PAGES_RENDERED_DIR = _HERE / "templates" / "rendered" / "_pages"
NZ_INTRO_CONTENT_DIR  = _HERE / "content" / "nz" / "_intro"
NZ_INTRO_RENDERED_DIR = _HERE / "templates" / "rendered" / "nz_intro"
REGION_INTRO_RENDERED_DIR = _HERE / "templates" / "rendered" / "region_intro"

KNOWN_PAGES: tuple = (
    "home", "davidsimmons", "research-index",
    "projects", "contact", "now", "sitemap",
)


def _strip_frontmatter(text: str) -> str:
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


def _md_to_html(text: str, jinja_env=None) -> str:
    """Render Markdown body to HTML, block-aware when jinja_env is supplied."""
    if jinja_env is not None:
        try:
            from blueprints.admin.cms.blocks.renderer import render_md_with_blocks
            return render_md_with_blocks(text, jinja_env)
        except Exception:
            pass
    return markdown.markdown(text, extensions=["fenced_code", "tables"])


def _atomic_write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)
    return path


def _je_from_current_app():
    try:
        from flask import current_app
        return current_app.jinja_env
    except Exception:
        return None


# ---------------- /_pages/<name> -------------------------------------


def _page_content_path(name: str) -> Path:
    return PAGES_CONTENT_DIR / f"{name}.md"


def _page_rendered_path(name: str) -> Path:
    return PAGES_RENDERED_DIR / f"{name}.html"


def page_slot_render(name: str) -> str:
    src = _page_content_path(name)
    if not src.exists():
        return ""
    cache = _page_rendered_path(name)
    if not cache.exists() or cache.stat().st_mtime < src.stat().st_mtime:
        try:
            regenerate_page_cache(name, jinja_env=_je_from_current_app())
        except Exception:
            return ""
    try:
        return cache.read_text(encoding="utf-8")
    except OSError:
        return ""


def regenerate_page_cache(name: str, jinja_env=None) -> Path:
    src = _page_content_path(name)
    if not src.exists():
        raise FileNotFoundError(f"no page slot at {src}")
    body = _strip_frontmatter(src.read_text(encoding="utf-8"))
    return _atomic_write(_page_rendered_path(name), _md_to_html(body, jinja_env))


# ---------------- region intro --------------------------------------


def _region_intro_content_path(region: str) -> Path:
    return _HERE / "content" / region / "_intro.md"


def _region_intro_rendered_path(region: str) -> Path:
    return REGION_INTRO_RENDERED_DIR / f"{region}.html"


def region_intro_render(region: str) -> str:
    src = _region_intro_content_path(region)
    if not src.exists():
        return ""
    cache = _region_intro_rendered_path(region)
    if not cache.exists() or cache.stat().st_mtime < src.stat().st_mtime:
        try:
            regenerate_region_intro(region, jinja_env=_je_from_current_app())
        except Exception:
            return ""
    try:
        return cache.read_text(encoding="utf-8")
    except OSError:
        return ""


def regenerate_region_intro(region: str, jinja_env=None) -> Path:
    src = _region_intro_content_path(region)
    if not src.exists():
        raise FileNotFoundError(f"no region intro at {src}")
    body = _strip_frontmatter(src.read_text(encoding="utf-8"))
    return _atomic_write(_region_intro_rendered_path(region), _md_to_html(body, jinja_env))


# ---------------- nz pattern theme intro ----------------------------


def _nz_intro_content_path(theme: str) -> Path:
    return NZ_INTRO_CONTENT_DIR / f"{theme}.md"


def _nz_intro_rendered_path(theme: str) -> Path:
    return NZ_INTRO_RENDERED_DIR / f"{theme}.html"


def nz_intro_render(theme: str) -> str:
    src = _nz_intro_content_path(theme)
    if not src.exists():
        return ""
    cache = _nz_intro_rendered_path(theme)
    if not cache.exists() or cache.stat().st_mtime < src.stat().st_mtime:
        try:
            regenerate_nz_intro(theme, jinja_env=_je_from_current_app())
        except Exception:
            return ""
    try:
        return cache.read_text(encoding="utf-8")
    except OSError:
        return ""


def regenerate_nz_intro(theme: str, jinja_env=None) -> Path:
    src = _nz_intro_content_path(theme)
    if not src.exists():
        raise FileNotFoundError(f"no nz intro at {src}")
    body = _strip_frontmatter(src.read_text(encoding="utf-8"))
    return _atomic_write(_nz_intro_rendered_path(theme), _md_to_html(body, jinja_env))


# ---------------- bulk regenerate ------------------------------------


def regenerate_all_v3(jinja_env=None) -> dict:
    """Regenerate every available page / region / theme slot cache.
    Idempotent — same source plus same jinja_env ⇒ same output.
    Called at app startup with app.jinja_env to pre-bake block-aware HTML.
    """
    out = {}
    for name in KNOWN_PAGES:
        if _page_content_path(name).exists():
            try: out[f"page:{name}"] = regenerate_page_cache(name, jinja_env=jinja_env)
            except Exception: pass
    if PAGES_CONTENT_DIR.exists():
        for f in PAGES_CONTENT_DIR.glob("*.md"):
            n = f.stem
            if n not in KNOWN_PAGES:
                try: out[f"page:{n}"] = regenerate_page_cache(n, jinja_env=jinja_env)
                except Exception: pass
    for region_dir in (_HERE / "content").iterdir():
        if region_dir.is_dir() and (region_dir / "_intro.md").exists():
            try: out[f"region:{region_dir.name}"] = regenerate_region_intro(region_dir.name, jinja_env=jinja_env)
            except Exception: pass
    if NZ_INTRO_CONTENT_DIR.exists():
        for f in NZ_INTRO_CONTENT_DIR.glob("*.md"):
            try: out[f"nz:{f.stem}"] = regenerate_nz_intro(f.stem, jinja_env=jinja_env)
            except Exception: pass
    if DAVIDSIMMONS_CONTENT_DIR.exists():
        for f in DAVIDSIMMONS_CONTENT_DIR.glob("*.md"):
            try: out[f"ds:{f.stem}"] = regenerate_davidsimmons_slot(f.stem, jinja_env=jinja_env)
            except Exception: pass
    return out


# ---------------- /davidsimmons/<slot> ------------------------------


DAVIDSIMMONS_CONTENT_DIR  = _HERE / "content" / "davidsimmons"
DAVIDSIMMONS_RENDERED_DIR = _HERE / "templates" / "rendered" / "davidsimmons"


def _ds_content_path(slot: str) -> Path:
    return DAVIDSIMMONS_CONTENT_DIR / f"{slot}.md"


def _ds_rendered_path(slot: str) -> Path:
    return DAVIDSIMMONS_RENDERED_DIR / f"{slot}.html"


def davidsimmons_slot_render(slot: str) -> str:
    src = _ds_content_path(slot)
    if not src.exists():
        return ""
    cache = _ds_rendered_path(slot)
    if not cache.exists() or cache.stat().st_mtime < src.stat().st_mtime:
        try:
            regenerate_davidsimmons_slot(slot, jinja_env=_je_from_current_app())
        except Exception:
            return ""
    try:
        return cache.read_text(encoding="utf-8")
    except OSError:
        return ""


def regenerate_davidsimmons_slot(slot: str, jinja_env=None) -> Path:
    src = _ds_content_path(slot)
    if not src.exists():
        raise FileNotFoundError(f"no davidsimmons slot at {src}")
    body = _strip_frontmatter(src.read_text(encoding="utf-8"))
    return _atomic_write(_ds_rendered_path(slot), _md_to_html(body, jinja_env))
