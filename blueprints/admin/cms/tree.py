"""Page tree builder — wave 2 item 5.

See docs/CMS-IMPL-WAVE-2.md §5.

Walks the filesystem + uses ``REGIONS`` from resolver, calls ``resolve()``
per discovered URL, emits a recursive ``TreeNode`` for the htmx sidebar.

Per-request rebuild (W2-1 ratified). No cache.

Pure code over the file system + the resolver — no I/O via SQLite, no
Flask-context dependency. The route handler that consumes ``build_tree()``
is wave 3 territory (item 6 / item ι in the implementation graph).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import frontmatter

from blueprints.admin.cms.resolver import (
    LockKind,
    PageKind,
    REGIONS,
    _CONTENT,
    resolve,
)


# Canonical region order for the sidebar — matches CLAUDE.md §6 narrative.
# REGIONS is a frozenset (unordered); this tuple imposes display order.
_REGION_ORDER: tuple[str, ...] = (
    "auckland", "wellington", "northland", "waikato",
    "bay-of-plenty", "gisborne", "hawkes-bay", "taranaki",
    "manawatu-whanganui", "marlborough", "nelson", "tasman",
    "west-coast", "canterbury", "otago", "southland",
)
assert frozenset(_REGION_ORDER) == REGIONS, (
    "REGION display order out of sync with resolver.REGIONS"
)


@dataclass(frozen=True)
class TreeNode:
    label:    str
    url:      str
    kind:     str           # PageKind.value, or "" for the synthetic root
    lock:     str           # LockKind.value, or "" for synthetic
    children: tuple["TreeNode", ...] = ()


# ========================================================================
#  Top-level entry point
# ========================================================================


def build_tree() -> TreeNode:
    """Construct the full page tree. Per-request rebuild — no cache."""
    return TreeNode(
        label="root",
        url="",
        kind="",
        lock="",
        children=(
            _build_home(),
            _build_about(),
            _build_blog(),
            _build_research(),
            _build_settings(),
        ),
    )


def to_dict(node: TreeNode) -> dict[str, Any]:
    """Serialise a TreeNode into a JSON-ready dict for the sidebar."""
    return asdict(node)


# ========================================================================
#  Section builders
# ========================================================================


def _node_from_resolve(
    url: str,
    label: str | None = None,
    children: tuple[TreeNode, ...] = (),
) -> TreeNode | None:
    """Convert resolve(url) into a TreeNode, or None if unresolvable."""
    r = resolve(url)
    if r is None:
        return None
    return TreeNode(
        label=label or r.title,
        url=r.url,
        kind=r.kind.value,
        lock=r.lock.value,
        children=children,
    )


def _synthetic(label: str, url: str, kind: PageKind, lock: LockKind,
               children: tuple[TreeNode, ...] = ()) -> TreeNode:
    """Build a TreeNode without consulting resolve() — used for parent
    grouping nodes whose URL isn't itself in the truth table (e.g.
    ``/research/nz/`` is not a resolvable page)."""
    return TreeNode(
        label=label, url=url,
        kind=kind.value, lock=lock.value,
        children=children,
    )


def _build_home() -> TreeNode:
    n = _node_from_resolve("/", label="Home")
    return n if n is not None else _synthetic(
        "Home", "/", PageKind.HYBRID, LockKind.LAYOUT_LOCKED,
    )


def _build_about() -> TreeNode:
    children: list[TreeNode] = []
    for slot in ("biography", "citations"):
        n = _node_from_resolve(f"/davidsimmons/{slot}/")
        if n is not None:
            children.append(n)
    parent = _node_from_resolve("/davidsimmons/", label="About",
                                children=tuple(children))
    return parent if parent is not None else _synthetic(
        "About", "/davidsimmons/",
        PageKind.HYBRID, LockKind.LAYOUT_LOCKED, tuple(children),
    )


def _build_blog() -> TreeNode:
    blog_dir = _CONTENT / "blog"
    posts: list[tuple[str, str, str]] = []   # (date, slug, label)
    if blog_dir.is_dir():
        for f in sorted(blog_dir.glob("*.md")):
            slug = f.stem
            if slug.startswith("_"):    # skip _index.md, _drafts, etc.
                continue
            try:
                fm = frontmatter.load(f)
                date = str(fm.metadata.get("date", "") or "")
                title = fm.metadata.get("title", slug) or slug
            except Exception:
                date, title = "", slug
            posts.append((date, slug, str(title)))
    posts.sort(key=lambda t: t[0], reverse=True)   # date desc
    children = tuple(
        TreeNode(
            label=f"{date}  {title}" if date else title,
            url=f"/blog/{slug}/",
            kind=PageKind.DIRECT_MD.value,
            lock=LockKind.EDITABLE.value,
        )
        for date, slug, title in posts
    )
    return _synthetic(
        "Blog", "/blog/",
        PageKind.DIRECT_MD, LockKind.EDITABLE, children,
    )


def _build_research() -> TreeNode:
    children: list[TreeNode] = []
    methodology = _node_from_resolve(
        "/research/methodology/", label="Methodology",
    )
    if methodology is not None:
        children.append(methodology)
    for region in _REGION_ORDER:
        children.append(_build_region(region))
    children.append(_build_nz())
    return _synthetic(
        "Research", "/research/",
        PageKind.HYBRID, LockKind.LAYOUT_LOCKED, tuple(children),
    )


def _build_region(region: str) -> TreeNode:
    region_data = _CONTENT / region / "data" / "problem"
    themes: dict[str, list[str]] = {}
    if region_data.is_dir():
        for yaml_file in sorted(region_data.glob("*.yaml")):
            stem = yaml_file.stem      # e.g. "transport.congestion"
            if "." not in stem:
                continue
            theme, _, slug = stem.partition(".")
            themes.setdefault(theme, []).append(slug)

    theme_nodes: list[TreeNode] = []
    for theme in sorted(themes.keys()):
        leaves = []
        for slug in sorted(themes[theme]):
            leaf = _node_from_resolve(
                f"/research/{region}/{theme}/{slug}/",
                label=slug.replace("_", " "),
            )
            if leaf is not None:
                leaves.append(leaf)
        section = _node_from_resolve(
            f"/research/{region}/{theme}/",
            label=theme,
            children=tuple(leaves),
        )
        if section is not None:
            theme_nodes.append(section)

    label = region.replace("-", " ").title()
    n = _node_from_resolve(
        f"/research/{region}/",
        label=label,
        children=tuple(theme_nodes),
    )
    return n if n is not None else _synthetic(
        label, f"/research/{region}/",
        PageKind.HYBRID, LockKind.LAYOUT_LOCKED, tuple(theme_nodes),
    )


def _build_nz() -> TreeNode:
    pattern_dir = _CONTENT / "nz" / "data" / "pattern"
    themes: set[str] = set()
    if pattern_dir.is_dir():
        for yaml_file in pattern_dir.glob("*.yaml"):
            stem = yaml_file.stem
            theme = stem.partition(".")[0] if "." in stem else stem
            themes.add(theme)
    children = tuple(
        TreeNode(
            label=f"Pattern: {theme}",
            url=f"/research/nz/{theme}/",
            kind=PageKind.PROJECTED.value,
            lock=LockKind.EDITABLE.value,
        )
        for theme in sorted(themes)
    )
    # /research/nz/ has no resolver entry; synthetic grouping node.
    return _synthetic(
        "NZ", "/research/nz/",
        PageKind.HYBRID, LockKind.LAYOUT_LOCKED, children,
    )


def _build_settings() -> TreeNode:
    # Five groups per CMS-SPEC §7: site identity, navigation, theme tokens,
    # contact form, footer. URL pattern matched by resolver §1.3 last row.
    groups = ("site", "nav", "theme", "contact", "footer")
    children = tuple(
        TreeNode(
            label=g.capitalize(),
            url=f"/admin/settings/{g}/",
            kind=PageKind.SETTINGS.value,
            lock=LockKind.EDITABLE.value,
        )
        for g in groups
    )
    return _synthetic(
        "Settings", "/admin/settings/",
        PageKind.SETTINGS, LockKind.EDITABLE, children,
    )
