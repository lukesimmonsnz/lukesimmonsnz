"""Tests for CMS v2 wave bodies — v2-4 theme, v2-6 slots, v2-8 SEO.

Handoff item 3.3 (SESSION-HANDOFF-2026-05-02-cms-v2-tier2.md §3.3).
Covers:
  - theme.compose      empty-as-inherit rule
  - derive_spacing_scale Fibonacci derivation
  - seo.splice_seo_into_frontmatter locality property
  - theme_slots.slot_render mtime fall-through
"""
from __future__ import annotations

import os
import time
from pathlib import Path

import pytest


# ========================================================================
# theme.compose
# ========================================================================

from blueprints.admin.cms.theme import compose, derive_spacing_scale, SPACING_PHI


class TestCompose:
    def test_empty_overlay_is_identity(self):
        base = {"color": {"primary": "#fff"}, "font": "serif"}
        assert compose(base, {}) == base

    def test_overlay_shadows_base(self):
        base = {"x": 1, "y": 2}
        result = compose(base, {"x": 99})
        assert result["x"] == 99
        assert result["y"] == 2

    def test_none_in_overlay_inherits_from_base(self):
        base = {"color": {"primary": "#abc"}}
        result = compose(base, {"color": {"primary": None}})
        assert result["color"]["primary"] == "#abc"

    def test_empty_string_in_overlay_inherits_from_base(self):
        base = {"font": "sans-serif"}
        result = compose(base, {"font": ""})
        assert result["font"] == "sans-serif"

    def test_deep_merge_is_recursive(self):
        base    = {"spacing": {"unit": "8px", "scale-0": "4px"}}
        overlay = {"spacing": {"scale-0": "2px"}}
        result  = compose(base, overlay)
        assert result["spacing"]["unit"] == "8px"    # inherited
        assert result["spacing"]["scale-0"] == "2px" # shadowed

    def test_overlay_adds_new_keys(self):
        base = {"a": 1}
        result = compose(base, {"b": 2})
        assert result["a"] == 1
        assert result["b"] == 2

    def test_does_not_mutate_base(self):
        base    = {"x": {"y": 1}}
        overlay = {"x": {"y": 2}}
        original = {"x": {"y": 1}}
        compose(base, overlay)
        assert base == original

    def test_three_level_compose(self):
        # defaults ⊕ preset ⊕ override
        defaults = {"color": {"primary": "#000", "bg": "#fff"}, "radius": {"sm": "2px"}}
        preset   = {"color": {"primary": "#333"}}
        override = {"color": {"primary": "#c00"}}
        result = compose(compose(defaults, preset), override)
        assert result["color"]["primary"] == "#c00"
        assert result["color"]["bg"]      == "#fff"  # from defaults
        assert result["radius"]["sm"]     == "2px"   # from defaults


# ========================================================================
# theme.derive_spacing_scale
# ========================================================================

class TestDeriveSpacingScale:
    def test_no_unit_returns_unchanged(self):
        theme = {"spacing": {}}
        assert derive_spacing_scale(theme) == theme

    def test_unit_8px_fills_all_10_steps(self):
        theme = {"spacing": {"unit": "8px"}}
        result = derive_spacing_scale(theme)
        spacing = result["spacing"]
        for i, phi in enumerate(SPACING_PHI):
            key = f"scale-{i}"
            assert key in spacing, f"missing {key}"
            expected = f"{8 * phi:g}px"
            assert spacing[key] == expected, f"{key}: expected {expected!r}, got {spacing[key]!r}"

    def test_unit_4px_scale0_is_2px(self):
        theme = {"spacing": {"unit": "4px"}}
        result = derive_spacing_scale(theme)
        assert result["spacing"]["scale-0"] == "2px"   # 4 * 0.5

    def test_existing_scale_not_overwritten(self):
        theme = {"spacing": {"unit": "8px", "scale-0": "CUSTOM"}}
        result = derive_spacing_scale(theme)
        assert result["spacing"]["scale-0"] == "CUSTOM"

    def test_does_not_mutate_input(self):
        theme = {"spacing": {"unit": "8px"}}
        original = {"spacing": {"unit": "8px"}}
        derive_spacing_scale(theme)
        assert theme == original

    def test_no_spacing_key_returns_unchanged(self):
        theme = {"color": {"primary": "#fff"}}
        result = derive_spacing_scale(theme)
        assert result == theme

    def test_unit_without_px_suffix_numeric_string(self):
        # "8" (no "px") — also valid per the implementation
        theme = {"spacing": {"unit": "8"}}
        result = derive_spacing_scale(theme)
        assert "scale-0" in result["spacing"]

    def test_fibonacci_multipliers_match_phi(self):
        # SPACING_PHI should have exactly 10 entries (scale-0 … scale-9)
        assert len(SPACING_PHI) == 10
        assert SPACING_PHI[0] == 0.5
        assert SPACING_PHI[1] == 1


# ========================================================================
# seo.splice_seo_into_frontmatter
# ========================================================================

from blueprints.admin.cms.seo import splice_seo_into_frontmatter, SeoView


class TestSpliceSeo:
    def test_appends_when_no_existing_seo(self):
        raw = "title: My page\ndate: 2024-01-01\n"
        result = splice_seo_into_frontmatter(raw, {"meta_description": "hello"})
        assert "seo:" in result
        assert "meta_description" in result
        # Other keys unchanged
        assert "title: My page\n" in result
        assert "date: 2024-01-01\n" in result

    def test_replaces_existing_seo_block(self):
        raw = ("title: My page\n"
               "seo:\n"
               "  meta_description: old\n"
               "date: 2024-01-01\n")
        result = splice_seo_into_frontmatter(raw, {"meta_description": "new"})
        assert "old" not in result
        assert "new" in result
        # Locality: title and date unchanged
        assert "title: My page\n" in result
        assert "date: 2024-01-01\n" in result

    def test_locality_unrelated_keys_verbatim(self):
        """Bytes contributed by non-seo keys must be unchanged."""
        raw = "title: A\ntags: [x, y]\nseo:\n  meta_description: x\nauthor: Luke\n"
        result = splice_seo_into_frontmatter(raw, {"meta_description": "y"})
        for key_line in ("title: A\n", "tags: [x, y]\n", "author: Luke\n"):
            assert key_line in result, f"key lost: {key_line!r}"

    def test_empty_seo_dict_removes_existing_block(self):
        raw = "title: T\nseo:\n  meta_description: x\ndate: 2024-01-01\n"
        result = splice_seo_into_frontmatter(raw, {})
        assert "seo:" not in result
        assert "title: T\n" in result
        assert "date: 2024-01-01\n" in result

    def test_empty_frontmatter_string(self):
        result = splice_seo_into_frontmatter("", {"meta_description": "x"})
        assert "seo:" in result
        assert "meta_description" in result

    def test_og_image_roundtrip(self):
        raw = "title: T\n"
        new_seo = {"og": {"image": "/static/cover.jpg", "type": "article"}}
        result = splice_seo_into_frontmatter(raw, new_seo)
        assert "og:" in result
        assert "/static/cover.jpg" in result

    def test_idempotent_on_double_splice(self):
        """Splicing twice with the same data is idempotent."""
        raw = "title: T\n"
        seo = {"meta_description": "hello"}
        once = splice_seo_into_frontmatter(raw, seo)
        twice = splice_seo_into_frontmatter(once, seo)
        # Result should contain exactly one "seo:" header
        assert twice.count("seo:") == 1


# ========================================================================
# SeoView.from_frontmatter
# ========================================================================

class TestSeoViewFromFrontmatter:
    def test_none_returns_empty(self):
        seo = SeoView.from_frontmatter(None)
        assert seo.meta_description == ""
        assert seo.og.title == ""

    def test_no_seo_key_returns_empty(self):
        seo = SeoView.from_frontmatter({"title": "T"})
        assert seo.meta_description == ""

    def test_full_sub_tree_parsed(self):
        fm = {"seo": {
            "meta_description": "desc",
            "og": {"title": "OG T", "image": "/img.jpg", "type": "article"},
            "twitter": {"card": "summary_large_image"},
            "schema_type": "BlogPosting",
            "canonical": "https://example.com/",
            "robots": "index,follow",
        }}
        seo = SeoView.from_frontmatter(fm)
        assert seo.meta_description == "desc"
        assert seo.og.title == "OG T"
        assert seo.og.image == "/img.jpg"
        assert seo.twitter.card == "summary_large_image"
        assert seo.schema_type == "BlogPosting"
        assert seo.canonical == "https://example.com/"
        assert seo.robots == "index,follow"

    def test_missing_og_keys_default_to_empty(self):
        fm = {"seo": {"og": {"title": "T"}}}
        seo = SeoView.from_frontmatter(fm)
        assert seo.og.description == ""
        assert seo.og.image == ""


# ========================================================================
# theme_slots.slot_render  (mtime fall-through)
# ========================================================================

from blueprints.admin.cms.theme_slots import (
    slot_render, regenerate_slot_cache,
    CONTENT_DIR, RENDERED_DIR,
)


class TestSlotRender:
    """Tests use tmp_path to avoid touching the real content/_theme/.

    We monkey-patch the module-level CONTENT_DIR / RENDERED_DIR via
    monkeypatching the functions directly since they close over the
    module-level paths; instead we call regenerate_slot_cache directly
    after writing real files.
    """

    def _write_slot(self, tmp_path: Path, name: str, md: str) -> Path:
        src = tmp_path / "content" / "_theme" / f"{name}.md"
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text(md, encoding="utf-8")
        return src

    def _rendered(self, tmp_path: Path, name: str) -> Path:
        return tmp_path / "templates" / "rendered" / "_theme" / f"{name}.html"

    def test_regenerate_slot_cache_produces_html(self, tmp_path, monkeypatch):
        import blueprints.admin.cms.theme_slots as ts
        monkeypatch.setattr(ts, "CONTENT_DIR",  tmp_path / "content" / "_theme")
        monkeypatch.setattr(ts, "RENDERED_DIR", tmp_path / "templates" / "rendered" / "_theme")

        src = self._write_slot(tmp_path, "header", "# Hello\n\nNav item.\n")
        out = regenerate_slot_cache("header")
        html = out.read_text(encoding="utf-8")
        assert "<h1>" in html
        assert "Hello" in html

    def test_slot_render_returns_cached_when_fresh(self, tmp_path, monkeypatch):
        import blueprints.admin.cms.theme_slots as ts
        monkeypatch.setattr(ts, "CONTENT_DIR",  tmp_path / "content" / "_theme")
        monkeypatch.setattr(ts, "RENDERED_DIR", tmp_path / "templates" / "rendered" / "_theme")

        self._write_slot(tmp_path, "footer", "Footer text.\n")
        regenerate_slot_cache("footer")
        html = slot_render("footer")
        assert "Footer text" in html

    def test_slot_render_falls_through_on_stale_cache(self, tmp_path, monkeypatch):
        import blueprints.admin.cms.theme_slots as ts
        monkeypatch.setattr(ts, "CONTENT_DIR",  tmp_path / "content" / "_theme")
        monkeypatch.setattr(ts, "RENDERED_DIR", tmp_path / "templates" / "rendered" / "_theme")

        src = self._write_slot(tmp_path, "header", "# Old\n")
        regenerate_slot_cache("header")

        # Make cache appear stale: advance src mtime past cache mtime
        rendered = self._rendered(tmp_path, "header")
        future = rendered.stat().st_mtime + 2
        os.utime(src, (future, future))

        # Write new content — slot_render should pick it up
        src.write_text("# New content\n", encoding="utf-8")
        os.utime(src, (future + 1, future + 1))

        html = slot_render("header")
        assert "New content" in html

    def test_slot_render_empty_when_slot_missing(self, tmp_path, monkeypatch):
        import blueprints.admin.cms.theme_slots as ts
        monkeypatch.setattr(ts, "CONTENT_DIR",  tmp_path / "content" / "_theme")
        monkeypatch.setattr(ts, "RENDERED_DIR", tmp_path / "templates" / "rendered" / "_theme")

        assert slot_render("nonexistent") == ""

    def test_slot_render_strips_frontmatter(self, tmp_path, monkeypatch):
        import blueprints.admin.cms.theme_slots as ts
        monkeypatch.setattr(ts, "CONTENT_DIR",  tmp_path / "content" / "_theme")
        monkeypatch.setattr(ts, "RENDERED_DIR", tmp_path / "templates" / "rendered" / "_theme")

        self._write_slot(tmp_path, "header",
                         "---\ntitle: Header slot\n---\n# Real content\n")
        html = slot_render("header")
        assert "Real content" in html
        assert "title: Header slot" not in html
