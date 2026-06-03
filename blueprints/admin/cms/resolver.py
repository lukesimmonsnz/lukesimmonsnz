"""Page resolver — wave 1 item 1."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Protocol

try:
    from enum import StrEnum  # type: ignore[attr-defined]
except ImportError:
    class StrEnum(str, Enum):  # type: ignore[no-redef]
        def __str__(self) -> str:
            return self.value


class PageKind(StrEnum):
    DIRECT_MD = "direct_md"
    HYBRID    = "hybrid"
    PROJECTED = "projected"
    SETTINGS  = "settings"


class LockKind(StrEnum):
    EDITABLE      = "editable"
    LAYOUT_LOCKED = "layout_locked"
    NOT_EDITABLE  = "not_editable"


REGIONS: frozenset = frozenset({
    "auckland", "wellington", "northland", "waikato",
    "bay-of-plenty", "gisborne", "hawkes-bay", "taranaki",
    "manawatu-whanganui", "marlborough", "nelson", "tasman",
    "west-coast", "canterbury", "otago", "southland",
})


@dataclass
class EditorState:
    body:        str
    frontmatter: str | None = None
    typed:       dict | None = None
    extras:      dict = field(default_factory=dict)


@dataclass(frozen=True)
class FileWrite:
    path:    Path
    content: bytes


class Projection(Protocol):
    name: str
    def load(self, srcs): ...
    def save(self, state): ...


@dataclass(frozen=True)
class PageRef:
    url:          str
    kind:         PageKind
    source_paths: tuple
    projection:   Projection
    lock:         LockKind
    title:        str
    parent_url:   str | None = None


_ROOT = Path(__file__).resolve().parents[3]
_CONTENT = _ROOT / "content"
_TEMPLATES = _ROOT / "templates"
_DOCS = _ROOT / "docs"


@dataclass(frozen=True)
class _StubProjection:
    name: str
    def load(self, srcs):
        raise NotImplementedError(f"projection {self.name!r}: load() not implemented")
    def save(self, state):
        raise NotImplementedError(f"projection {self.name!r}: save() not implemented")


def _split_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    if text[3:5] == "\r\n":
        nl = "\r\n"
    elif text[3:4] == "\n":
        nl = "\n"
    else:
        return None, text
    rest = text[3 + len(nl):]
    close = nl + "---" + nl
    end = rest.find(close)
    if end == -1:
        return None, text
    return rest[:end], rest[end + len(close):]


def _splice_frontmatter(fm, body):
    if fm is None:
        out = body
        if not out.endswith("\n"):
            out += "\n"
        return out
    nl = "\r\n" if ("\r\n" in fm or "\r\n" in body) else "\n"
    out = "---" + nl + fm + nl + "---" + nl + body
    if not out.endswith("\n"):
        out += nl
    return out


@dataclass(frozen=True)
class _ProblemYamlProjection:
    name: str
    def load(self, srcs):
        if len(srcs) < 1:
            raise ValueError(f"{self.name}: expected >=1 source path")
        problem = srcs[0]
        if not problem.exists():
            return EditorState(body="", frontmatter=None, extras={"path": problem})
        with open(problem, "r", encoding="utf-8", newline="") as f:
            text = f.read()
        return EditorState(body=text, frontmatter=None, extras={"path": problem})
    def save(self, state):
        path = state.extras.get("path")
        if path is None:
            raise ValueError(f"{self.name}: state.extras['path'] required")
        out = state.body or ""
        if not out.endswith("\n"):
            out += "\n"
        return (FileWrite(path=Path(path), content=out.encode("utf-8")),)


@dataclass(frozen=True)
class _FrontmatterMdProjection:
    name: str
    def load(self, srcs):
        if len(srcs) != 1:
            raise ValueError(f"{self.name}: expected exactly 1 source")
        path = srcs[0]
        if not path.exists():
            return EditorState(body="", frontmatter=None, extras={"path": path})
        with open(path, "r", encoding="utf-8", newline="") as f:
            text = f.read()
        fm, body = _split_frontmatter(text)
        return EditorState(body=body, frontmatter=fm, extras={"path": path})
    def save(self, state):
        path = state.extras.get("path")
        if path is None:
            raise ValueError(f"{self.name}: state.extras['path'] required")
        out = _splice_frontmatter(state.frontmatter, state.body or "")
        return (FileWrite(path=Path(path), content=out.encode("utf-8")),)


HOME_SLOTS         = _StubProjection("home_slots")
DAVIDSIMMONS_SLOTS = _StubProjection("davidsimmons_slots")
SLOT_MD            = _FrontmatterMdProjection("slot_md")
BLOG_INDEX         = _FrontmatterMdProjection("blog_index")
DIRECT_MD_PROJ     = _FrontmatterMdProjection("direct_md")
RESEARCH_INDEX     = _StubProjection("research_index")
REGION_INDEX       = _StubProjection("region_index")
SECTION_MD         = _FrontmatterMdProjection("section_md")
CORPUS_LEAF_FORM_A = _ProblemYamlProjection("corpus_leaf_form_A")
PATTERN_FORM_A     = _ProblemYamlProjection("pattern_form_A")
SETTINGS_FORM      = _StubProjection("settings_form")


_REGION_RE = "|".join(sorted(map(re.escape, REGIONS)))


def _build_home(_m):
    slot = _CONTENT / "_pages" / "home.md"
    if slot.exists():
        return PageRef(url="/", kind=PageKind.DIRECT_MD,
                       source_paths=(slot,), projection=DIRECT_MD_PROJ,
                       lock=LockKind.EDITABLE, title="Home")
    return PageRef(url="/", kind=PageKind.HYBRID,
                   source_paths=(_TEMPLATES / "main" / "index.html",),
                   projection=HOME_SLOTS, lock=LockKind.LAYOUT_LOCKED, title="Home")


def _build_davidsimmons_root(_m):
    slot = _CONTENT / "_pages" / "davidsimmons.md"
    if slot.exists():
        return PageRef(url="/davidsimmons/", kind=PageKind.DIRECT_MD,
                       source_paths=(slot,), projection=DIRECT_MD_PROJ,
                       lock=LockKind.EDITABLE, title="About")
    return PageRef(url="/davidsimmons/", kind=PageKind.HYBRID,
                   source_paths=(_TEMPLATES / "davidsimmons" / "index.html",),
                   projection=DAVIDSIMMONS_SLOTS, lock=LockKind.LAYOUT_LOCKED, title="About")


def _build_davidsimmons_slot(m):
    slot = m.group("slot")
    src = _CONTENT / "davidsimmons" / f"{slot}.md"
    if not src.exists():
        return None
    return PageRef(url=f"/davidsimmons/{slot}/", kind=PageKind.HYBRID,
                   source_paths=(src,), projection=SLOT_MD, lock=LockKind.EDITABLE,
                   title=slot.replace("-", " ").title(), parent_url="/davidsimmons/")


def _build_blog_index(_m):
    src = _CONTENT / "blog" / "_index.md"
    return PageRef(url="/blog/", kind=PageKind.DIRECT_MD,
                   source_paths=(src,), projection=BLOG_INDEX,
                   lock=LockKind.EDITABLE, title="Blog")


def _build_blog_post(m):
    slug = m.group("slug")
    src = _CONTENT / "blog" / f"{slug}.md"
    if not src.exists():
        return None
    return PageRef(url=f"/blog/{slug}/", kind=PageKind.DIRECT_MD,
                   source_paths=(src,), projection=DIRECT_MD_PROJ,
                   lock=LockKind.EDITABLE, title=slug.replace("-", " "),
                   parent_url="/blog/")


def _build_research_index(_m):
    slot = _CONTENT / "_pages" / "research-index.md"
    if slot.exists():
        return PageRef(url="/research/", kind=PageKind.DIRECT_MD,
                       source_paths=(slot,), projection=DIRECT_MD_PROJ,
                       lock=LockKind.EDITABLE, title="Research")
    return PageRef(url="/research/", kind=PageKind.HYBRID,
                   source_paths=(_TEMPLATES / "research" / "index.html",
                                 _CONTENT / "research" / "methodology.md"),
                   projection=RESEARCH_INDEX, lock=LockKind.LAYOUT_LOCKED, title="Research")


def _build_research_methodology(_m):
    return PageRef(url="/research/methodology/", kind=PageKind.DIRECT_MD,
                   source_paths=(_DOCS / "METHODOLOGY.md",),
                   projection=DIRECT_MD_PROJ, lock=LockKind.EDITABLE,
                   title="Methodology", parent_url="/research/")


def _build_region_index(m):
    region = m.group("region")
    if region not in REGIONS:
        return None
    intro = _CONTENT / region / "_intro.md"
    if intro.exists():
        return PageRef(url=f"/research/{region}/", kind=PageKind.DIRECT_MD,
                       source_paths=(intro,), projection=DIRECT_MD_PROJ,
                       lock=LockKind.EDITABLE,
                       title=region.replace("-", " ").title(), parent_url="/research/")
    return PageRef(url=f"/research/{region}/", kind=PageKind.HYBRID,
                   source_paths=(_TEMPLATES / region / "index.html",),
                   projection=REGION_INDEX, lock=LockKind.LAYOUT_LOCKED,
                   title=region.replace("-", " ").title(), parent_url="/research/")


def _build_region_section(m):
    region = m.group("region"); theme = m.group("theme")
    if region not in REGIONS:
        return None
    section_md = _CONTENT / region / "pages" / "_sections" / f"{theme}.md"
    if section_md.exists():
        return PageRef(url=f"/research/{region}/{theme}/", kind=PageKind.HYBRID,
                       source_paths=(section_md,), projection=SECTION_MD,
                       lock=LockKind.EDITABLE, title=f"{region} / {theme}",
                       parent_url=f"/research/{region}/")
    return PageRef(url=f"/research/{region}/{theme}/", kind=PageKind.HYBRID,
                   source_paths=(), projection=REGION_INDEX, lock=LockKind.LAYOUT_LOCKED,
                   title=f"{region} / {theme}", parent_url=f"/research/{region}/")


def _build_region_leaf(m):
    region = m.group("region"); theme = m.group("theme"); slug = m.group("slug")
    if region not in REGIONS:
        return None
    problem = _CONTENT / region / "data" / "problem" / f"{theme}.{slug}.yaml"
    if not problem.exists():
        return None
    return PageRef(url=f"/research/{region}/{theme}/{slug}/", kind=PageKind.PROJECTED,
                   source_paths=(problem,), projection=CORPUS_LEAF_FORM_A,
                   lock=LockKind.EDITABLE, title=slug.replace("_", " "),
                   parent_url=f"/research/{region}/{theme}/")


def _build_nz_pattern_theme(m):
    theme = m.group("theme")
    intro = _CONTENT / "nz" / "_intro" / f"{theme}.md"
    if intro.exists():
        return PageRef(url=f"/research/nz/{theme}/", kind=PageKind.DIRECT_MD,
                       source_paths=(intro,), projection=DIRECT_MD_PROJ,
                       lock=LockKind.EDITABLE,
                       title=f"NZ Pattern: {theme}", parent_url="/research/")
    pattern_dir = _CONTENT / "nz" / "data" / "pattern"
    files = tuple(sorted(pattern_dir.glob(f"{theme}.*.yaml")))
    return PageRef(url=f"/research/nz/{theme}/", kind=PageKind.PROJECTED,
                   source_paths=files, projection=PATTERN_FORM_A,
                   lock=LockKind.EDITABLE, title=f"NZ Pattern: {theme}",
                   parent_url="/research/")


def _build_settings_group(m):
    group = m.group("group")
    return PageRef(url=f"/admin/settings/{group}/", kind=PageKind.SETTINGS,
                   source_paths=(_ROOT / "instance" / "site_settings.json",),
                   projection=SETTINGS_FORM, lock=LockKind.EDITABLE,
                   title=f"Settings: {group}")


def _build_contact_page(_m):
    slot = _CONTENT / "_pages" / "contact.md"
    if not slot.exists():
        return None
    return PageRef(url="/contact/", kind=PageKind.DIRECT_MD,
                   source_paths=(slot,), projection=DIRECT_MD_PROJ,
                   lock=LockKind.EDITABLE, title="Contact")


def _build_sitemap_html(_m):
    slot = _CONTENT / "_pages" / "sitemap.md"
    if not slot.exists():
        return None
    return PageRef(url="/sitemap/", kind=PageKind.DIRECT_MD,
                   source_paths=(slot,), projection=DIRECT_MD_PROJ,
                   lock=LockKind.EDITABLE, title="Sitemap")




THEME_SLOTS: frozenset = frozenset({"header", "footer"})


def _build_theme_slot(m):
    slot = m.group("slot")
    if slot not in THEME_SLOTS:
        return None
    src = _CONTENT / "_theme" / f"{slot}.md"
    if not src.exists():
        return None
    return PageRef(url=f"/_theme/{slot}/", kind=PageKind.DIRECT_MD,
                   source_paths=(src,), projection=DIRECT_MD_PROJ,
                   lock=LockKind.EDITABLE, title=f"Theme: {slot}")


_PATTERNS = (
    (re.compile(r"^/$"),                                        _build_home),
    (re.compile(r"^/contact/$"),                                 _build_contact_page),
    (re.compile(r"^/sitemap/$"),                                 _build_sitemap_html),
    (re.compile(r"^/davidsimmons/$"),                           _build_davidsimmons_root),
    (re.compile(r"^/davidsimmons/(?P<slot>[\w-]+)/$"),          _build_davidsimmons_slot),
    (re.compile(r"^/blog/$"),                                   _build_blog_index),
    (re.compile(r"^/blog/(?P<slug>[\w-]+)/$"),                  _build_blog_post),
    (re.compile(r"^/research/$"),                               _build_research_index),
    (re.compile(r"^/research/methodology/$"),                   _build_research_methodology),
    (re.compile(r"^/research/nz/(?P<theme>[\w-]+)/$"),          _build_nz_pattern_theme),
    (re.compile(rf"^/research/(?P<region>{_REGION_RE})/$"),     _build_region_index),
    (re.compile(rf"^/research/(?P<region>{_REGION_RE})/(?P<theme>[\w-]+)/$"), _build_region_section),
    (re.compile(rf"^/research/(?P<region>{_REGION_RE})/(?P<theme>[\w-]+)/(?P<slug>[\w-]+)/$"), _build_region_leaf),
    (re.compile(r"^/_theme/(?P<slot>[\w-]+)/$"),                _build_theme_slot),
    (re.compile(r"^/admin/settings/(?P<group>[\w-]+)/$"),       _build_settings_group),
)


def resolve(url):
    for pattern, builder in _PATTERNS:
        m = pattern.match(url)
        if m is not None:
            return builder(m)
    return None
