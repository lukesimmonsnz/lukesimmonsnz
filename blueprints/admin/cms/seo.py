"""SEO panel — typed seo: frontmatter sub-tree (CMS v2 wave v2-8)."""
from __future__ import annotations

import json as _json
import re
from dataclasses import dataclass, field

import yaml


# ---------------- view dataclasses (Jinja-side accessor) -------------


@dataclass(frozen=True)
class _OgView:
    title:       str = ""
    description: str = ""
    image:       str = ""
    type:        str = ""


@dataclass(frozen=True)
class _TwitterView:
    card: str = ""


@dataclass(frozen=True)
class SeoView:
    meta_description: str          = ""
    og:               _OgView      = field(default_factory=_OgView)
    twitter:          _TwitterView = field(default_factory=_TwitterView)
    schema_type:      str          = ""
    canonical:        str          = ""
    robots:           str          = ""

    @classmethod
    def from_frontmatter(cls, fm: dict | None) -> "SeoView":
        if not fm or "seo" not in fm:
            return cls()
        s = fm.get("seo") or {}
        if not isinstance(s, dict):
            return cls()
        return cls(
            meta_description = s.get("meta_description", "") or "",
            og               = _OgView(**(s.get("og") or {})),
            twitter          = _TwitterView(**(s.get("twitter") or {})),
            schema_type      = s.get("schema_type", "") or "",
            canonical        = s.get("canonical", "") or "",
            robots           = s.get("robots", "") or "",
        )


# ---------------- JSON-LD emitter ------------------------------------


def jsonld(seo: SeoView, path: str, site_url: str, site_name: str,
           page_title: str = "", page_date: str = "") -> str:
    """Emit a schema.org JSON-LD blob.

    Returns a JSON string suitable for embedding in a <script type="application/ld+json">.
    """
    if not seo.schema_type:
        return "{}"
    base: dict = {
        "@context": "https://schema.org",
        "@type":    seo.schema_type,
        "url":      f"{site_url.rstrip('/')}{path}",
        "name":     page_title or site_name,
    }
    if seo.schema_type in ("BlogPosting", "Article", "TechArticle"):
        base["headline"] = page_title or site_name
        if page_date:
            base["datePublished"] = page_date
        if seo.og.image:
            base["image"] = seo.og.image
        if seo.meta_description:
            base["description"] = seo.meta_description
    elif seo.schema_type == "Person":
        base["name"] = page_title or site_name
    else:
        if seo.meta_description:
            base["description"] = seo.meta_description
    if seo.canonical:
        base["url"] = seo.canonical
    return _json.dumps(base, ensure_ascii=False, separators=(",", ":"))


# ---------------- frontmatter splice (locality-preserving) -----------


_SEO_BLOCK_RE = re.compile(r"^seo:\s*\n", re.MULTILINE)


def splice_seo_into_frontmatter(raw_fm: str, new_seo: dict) -> str:
    """Splice a new seo: sub-tree into raw frontmatter text.

    Locality property: for every top-level key k != 'seo' in raw_fm, the
    bytes contributed by k to the output equal the bytes contributed by
    k in raw_fm.

    Mechanics: locate '^seo:' (line-anchored). If found, find the block
    extent by scanning forward until the next top-level key (a line
    whose first character is in [a-zA-Z_]). Replace that range with the
    re-serialised new_seo. If not found, append at the end.

    new_seo is YAML-serialised with default_flow_style=False, sort_keys=False,
    indent=2, prefixed with 'seo:\\n'.
    """
    # Drop empty / no-op seo block: if new_seo is empty, also remove any
    # existing seo: block so we don't leave a dangling header.
    if not new_seo:
        return _strip_seo_block(raw_fm)

    serialised = yaml.dump(
        {"seo": new_seo},
        default_flow_style=False, sort_keys=False, indent=2,
        allow_unicode=True,
    ).rstrip("\n")

    m = _SEO_BLOCK_RE.search(raw_fm)
    if m is None:
        # Append at end.
        sep = "" if raw_fm == "" or raw_fm.endswith("\n") else "\n"
        return raw_fm + sep + serialised + "\n"

    # Find the end of the seo block: first line at column 0 starting
    # with [a-zA-Z_] AFTER the seo: line itself.
    start = m.start()
    after_header = m.end()
    end = len(raw_fm)
    for line_match in re.finditer(r"^[A-Za-z_][\w-]*:", raw_fm[after_header:], re.MULTILINE):
        end = after_header + line_match.start()
        break

    # Replace [start, end) with serialised seo block.
    # Preserve trailing whitespace before next key (typically "\n").
    return raw_fm[:start] + serialised + "\n" + raw_fm[end:]


def _strip_seo_block(raw_fm: str) -> str:
    """Remove an existing seo: block, keep all other keys verbatim."""
    m = _SEO_BLOCK_RE.search(raw_fm)
    if m is None:
        return raw_fm
    start = m.start()
    after_header = m.end()
    end = len(raw_fm)
    for line_match in re.finditer(r"^[A-Za-z_][\w-]*:", raw_fm[after_header:], re.MULTILINE):
        end = after_header + line_match.start()
        break
    return raw_fm[:start] + raw_fm[end:]
