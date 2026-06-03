"""Regenerate docs/SITEMAP.md and refresh auto blocks in README.md / ARCHITECTURE.md.

Deterministic: no AI, no network. Counts, the route table, and the tree are
derived from app.url_map + the filesystem. The narrative prose in SITEMAP.md
is part of the template in this file; the two hand-written docs are touched
only inside <!-- auto:meta:begin --> ... <!-- auto:meta:end --> blocks.

Run directly:

    .venv\\Scripts\\python -m agent.regen_docs

Invoked automatically by agent\\run_daily.bat after the blog agent runs, so
new posts appear in the counts without a manual step.
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

# Force UTF-8 on Windows consoles so macrons / § / box-drawing don't die.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Allow `python agent/regen_docs.py` as well as `-m agent.regen_docs`.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402  — import after sys.path is set


DOCS_DIR = ROOT / "docs"
BLOG_DIR = ROOT / "content" / "blog"
AUCKLAND_ROOT = ROOT / "content" / "auckland"
AUCKLAND_DATA = AUCKLAND_ROOT / "data"
AUCKLAND_PAGES = AUCKLAND_ROOT / "pages"

# Which endpoint belongs to which blueprint / section of the sitemap tree.
# Kept explicit rather than parsed from the endpoint prefix so a refactor
# doesn't silently reshuffle the tree.

MAIN_ROUTES = [
    ("/", "main.home", "Home page."),
    ("/contact/", "main.contact", "Contact form (no email addresses)."),
    ("/sitemap/", "main.sitemap_html", "Human-readable sitemap (renders docs/SITEMAP.md)."),
]

BLOG_ROUTES = [
    ("/blog/", "blog.index", "Blog index (recent + archive)."),
    ("/blog/feed.xml", "blog.feed", "Atom feed (last 20 posts)."),
    ("/blog/<slug>/", "blog.post", "One rendered Markdown post."),
]

# Research subtree: ordered list of (branch_label, [(url, endpoint, desc), ...]).
RESEARCH_BRANCHES = [
    (
        "Computer Science",
        "research.cs_index",
        "/research/computer-science/",
        [
            ("/research/computer-science/python/", "research.cs_python"),
            ("/research/computer-science/rust/", "research.cs_rust"),
            ("/research/computer-science/ai-it-ecosystem/", "research.cs_ai_it"),
            ("/research/computer-science/references/", "research.cs_references"),
            ("/research/computer-science/readme/", "research.cs_readme"),
        ],
    ),
    (
        "Climate Science & AI",
        "research.climate_index",
        "/research/climate-science-and-ai/",
        [
            ("/research/climate-science-and-ai/intro/", "research.climate_intro"),
            ("/research/climate-science-and-ai/history/", "research.climate_history"),
            ("/research/climate-science-and-ai/methods/", "research.climate_methods"),
            ("/research/climate-science-and-ai/applications/", "research.climate_applications"),
            ("/research/climate-science-and-ai/challenges/", "research.climate_challenges"),
            ("/research/climate-science-and-ai/future/", "research.climate_future"),
            ("/research/climate-science-and-ai/references/", "research.climate_references"),
        ],
    ),
    (
        "Medical Science",
        "research.medsci_index",
        "/research/medical-science/",
        [
            ("/research/medical-science/neuroscience-ai/", "research.medsci_neuroscience"),
            ("/research/medical-science/bioinformatics/", "research.medsci_bioinformatics"),
            ("/research/medical-science/medical-imaging/", "research.medsci_imaging"),
            ("/research/medical-science/clinical-ai/", "research.medsci_clinical"),
            ("/research/medical-science/drug-discovery/", "research.medsci_drugs"),
            ("/research/medical-science/references/", "research.medsci_references"),
        ],
    ),
]

DAVID_ROUTES = [
    ("/davidsimmons/", "davidsimmons.index", "Biography home."),
    ("/davidsimmons/about/", "davidsimmons.about", "About."),
    ("/davidsimmons/timeline/", "davidsimmons.timeline", "Timeline of life events."),
    ("/davidsimmons/works/", "davidsimmons.works", "Publications grouped by category."),
    ("/davidsimmons/references/", "davidsimmons.references", "Source references."),
]


# ---------------------------------------------------------------------------
# Filesystem counts
# ---------------------------------------------------------------------------


def _blog_post_paths() -> list[Path]:
    if not BLOG_DIR.exists():
        return []
    return sorted(BLOG_DIR.glob("*.md"), reverse=True)


ENTITY_TYPE_DIRS = {
    "actors", "camps", "drivers", "evidence",
    "metrics", "problems", "responses", "sources",
}


def _auckland_counts() -> dict[str, int]:
    """Count entities by type directory. Returns {type_name: count}.

    Only recognised entity-type directories are counted; non-entity data
    like ``charts/`` and ``series/`` are skipped.
    """
    counts: dict[str, int] = {}
    if AUCKLAND_DATA.exists():
        for sub in sorted(AUCKLAND_DATA.iterdir()):
            if sub.is_dir() and sub.name in ENTITY_TYPE_DIRS:
                counts[sub.name] = len(list(sub.glob("*.yaml")))
    return counts


def _auckland_page_paths() -> list[Path]:
    if not AUCKLAND_PAGES.exists():
        return []
    return sorted(AUCKLAND_PAGES.rglob("*.md"))


def _url_rule_count() -> int:
    return sum(1 for _ in app.url_map.iter_rules())


# ---------------------------------------------------------------------------
# SITEMAP.md rendering
# ---------------------------------------------------------------------------


def _fmt_today() -> str:
    return date.today().isoformat()


_RESEARCH_BRANCH_LABELS_LOWER = {
    "Computer Science": "computer science",
    "Climate Science & AI": "climate science and AI",
    "Medical Science": "medical science",
}


def _tree_block() -> str:
    """The site's page hierarchy, as a nested Markdown list of links. Rendered
    into ordinary prose on the live /sitemap/ page — no code fence, no
    monospace tree drawing."""
    out: list[str] = []

    out.append("- [Home](/)")
    out.append("- [Contact](/contact/)")
    out.append("- [Blog](/blog/) — recent posts and archive")
    out.append("    - [Atom feed](/blog/feed.xml)")
    out.append("- [Research](/research/)")
    slug_label_overrides = {
        "ai-it-ecosystem": "AI & IT ecosystem",
        "neuroscience-ai": "Neuroscience & AI",
        "clinical-ai": "Clinical AI",
        "medical-imaging": "Medical imaging",
        "drug-discovery": "Drug discovery",
        "readme": "Branch readme",
    }
    for label, _index_ep, index_url, pages in RESEARCH_BRANCHES:
        out.append(f"    - [{label}]({index_url})")
        for url, _ep in pages:
            slug = url.rstrip("/").rsplit("/", 1)[-1]
            nice = slug_label_overrides.get(slug) or (slug.replace("-", " ")[:1].upper() + slug.replace("-", " ")[1:])
            out.append(f"        - [{nice}]({url})")
    out.append("    - [Methodology](/research/methodology/)")
    out.append("    - [National summary](/research/nz/) — cross-regional pattern rollup")
    out.append("        - [Solution space](/research/nz/solutions/) — interventions sorted by mechanism")
    # Aotearoa regional research: 16 regional councils, each with 11 themes.
    aotearoa_regions = [
        ("auckland", "Auckland"),
        ("wellington", "Wellington"),
        ("northland", "Northland"),
        ("waikato", "Waikato"),
        ("bay-of-plenty", "Bay of Plenty"),
        ("gisborne", "Gisborne"),
        ("hawkes-bay", "Hawke's Bay"),
        ("taranaki", "Taranaki"),
        ("manawatu-whanganui", "Manawatū-Whanganui"),
        ("nelson", "Nelson"),
        ("tasman", "Tasman"),
        ("marlborough", "Marlborough"),
        ("west-coast", "West Coast"),
        ("canterbury", "Canterbury"),
        ("otago", "Otago"),
        ("southland", "Southland"),
    ]
    aotearoa_themes = [
        ("housing", "Housing"),
        ("transport", "Transport"),
        ("infrastructure", "Infrastructure"),
        ("environment", "Environment"),
        ("climate", "Climate adaptation"),
        ("inequality", "Inequality"),
        ("crime", "Crime & safety"),
        ("health", "Health"),
        ("education", "Education"),
        ("economy", "Economy"),
        ("governance", "Governance"),
    ]
    for slug, region_label in aotearoa_regions:
        out.append(f"    - [{region_label}](/research/{slug}/)")
        for theme_slug, theme_label in aotearoa_themes:
            out.append(f"        - [{theme_label}](/research/{slug}/{theme_slug}/)")
    out.append("- [David Simmons biography](/davidsimmons/)")
    out.append("    - [About](/davidsimmons/about/)")
    out.append("    - [Timeline](/davidsimmons/timeline/)")
    out.append("    - [Works](/davidsimmons/works/)")
    out.append("    - [References](/davidsimmons/references/)")
    out.append("- [Sitemap](/sitemap/) — this page")
    out.append("    - [XML sitemap](/sitemap.xml) — machine-readable, for search engines")

    return "\n".join(out)


def _counts_table(
    blog_count: int,
    auckland_by_type: dict[str, int],
    auckland_pages_count: int,
) -> str:
    """Compact at-a-glance list for the public sitemap. No filesystem links —
    this is a public page, not a dev-facing doc."""
    problems = auckland_by_type.get("problems", 0)
    camps = auckland_by_type.get("camps", 0)
    drivers = auckland_by_type.get("drivers", 0)
    evidence = auckland_by_type.get("evidence", 0)
    sources = auckland_by_type.get("sources", 0)

    lines = [
        f"- **Blog posts:** {blog_count}",
        f"- **Research branches:** 4 (Computer Science, Climate Science & AI, Medical Science, Auckland)",
        f"- **Auckland — Problems published:** {problems} (of an 11-section scope; the rest are in progress)",
        f"- **Auckland — evidence graph:** {drivers} drivers, {camps} camps, {evidence} evidence claims, {sources} cited sources",
        f"- **Auckland — rendered pages:** {auckland_pages_count}",
        f"- **David Simmons biography:** 5 pages, driven from structured data",
    ]
    return "\n".join(lines)

    return "\n".join(f"{i + 1}. " + issue for i, issue in enumerate(issues))


SITEMAP_TEMPLATE = """<!--
  AUTO-GENERATED by agent/regen_docs.py. Do not hand-edit.
  Re-run with:  .venv\\Scripts\\python -m agent.regen_docs
-->

<!-- auto:meta:begin -->
**Updated:** {today}
<!-- auto:meta:end -->

## Pages

<!-- auto:tree:begin -->
{tree}
<!-- auto:tree:end -->

---

## At a glance

<!-- auto:counts:begin -->
{counts}
<!-- auto:counts:end -->

---

## How to cite

The Auckland research pages are the part of this site most likely to be cited. A recommended citation form:

> Simmons, L. ({year}). *\u2039Page title\u203a*. Luke Simmons — Research. Retrieved {today} from https://lukesimmonsnz.kiwi/research/auckland/\u2039section\u203a/\u2039subpage\u203a/

For a specific Auckland subpage, prefer the version with the most recent **Updated** date on the page itself. The entity data behind each Auckland page lives under `content/auckland/data/` in the site's source repository; every factual claim on a page carries its Source through that data layer.

For blog posts, the canonical URL is the post page (`/blog/\u2039slug\u203a/`) and the date in the slug is the publication date.

---

## Copyright and license

&copy; Luke Simmons. **All rights reserved.**

There is no open-source license on the site's source code or its written content. The prose, biographical material on David Roy Simmons, and the Auckland research content are all under default copyright — no permission to copy, redistribute, modify, or republish is granted by default. Quotation for the purposes of commentary, criticism, or research is usually permitted under the ordinary fair-dealing rules of New Zealand copyright law, but that is a reader judgement, not a license. If you would like to reuse any part of this work beyond fair dealing, please ask first via the [contact form](/contact/).

### A note on AI assistance

Some content on this site is produced with assistance from large language models. Two channels are in use.

- **Blog** — a two-stage local-agent pipeline running on the site owner's hardware via Ollama (`qwen2.5:14b`). A **daily agent** writes private working notes from Hacker News and arXiv cs.AI; those notes are **not published** and stay on disk. Once a week, usually Sundays, a **weekly agent** synthesises the week of notes plus that week's top HN and arXiv stories into a single public blog post with inline citations to the original sources. Posts signed `agent` are agent-authored; posts signed `luke` are hand-written.
- **Longer-form prose** — including research pages under `/research/` and documentation such as the README and architecture notes — is drafted with **Claude AI via Anthropic's hosted API**. Prompts and drafts transit Anthropic's infrastructure under their terms.

What "edited" means varies by surface, and is disclosed on the page itself. The three research branches under Computer Science, Climate Science & AI, and Medical Science are AI-drafted reference notes that the site owner has not edited; they are published as-is for orientation, not as authoritative references. The Auckland research branch is AI-drafted in iterative dialogue with the site owner, and its typed entity graph enforces structural source citations on every factual claim — but independent per-claim fact-checking by the owner is a step that should sit between drafting and publication and is not yet formally in place.

---

## Privacy and tracking

The site does not add its own tracking. The ingress layer does some of its own, and that is disclosed here honestly rather than glossed over.

- **No site-owned analytics.** No Google Analytics, Plausible, Fathom, or any other analytics service is loaded by the site.
- **No site-owned third-party scripts** beyond Google Fonts. No ad networks, no tag managers, no pixels, no beacons.
- **No accounts, no logins, no newsletter.** The site has no user database.
- **Cloudflare is in front of the site** as the public ingress while the owner transitions to dedicated self-hosting hardware. That means every request you make is visible to Cloudflare at the edge (they terminate TLS), and Cloudflare sets its own `__cf_bm` bot-management cookie on responses by default. Cloudflare also retains request logs (IP, user-agent, URL, status) according to their own retention policy. This is Cloudflare's processing, not the site's, and is governed by Cloudflare's [privacy policy](https://www.cloudflare.com/privacypolicy/).
- **Fonts are loaded from Google Fonts** via a `<link>` tag. Your browser will make a request to `fonts.googleapis.com` and `fonts.gstatic.com` for stylesheet and font files. Google may log that request in accordance with their own policies.
- **The contact form** writes submissions to a flat file at the origin (`data/messages.jsonl`). Once the site is publicly live, submissions will also be emailed to an address on this site's own domain (`@lukesimmonsnz.kiwi`), which the site owner reads via ordinary mail forwarding. The submissions are not sent to any third-party form-handling service (Formspree, Basin, etc.). The only person who reads contact-form submissions is the site owner.
- **Origin server logs** (URL, status code, timestamp) are retained on the origin machine for debugging. They are not shared. They will continue to exist once the origin moves off Cloudflare's proxy.

---

## Accessibility

The site aims to be readable and navigable without assistive technology, and usable with it:

- **Keyboard navigation.** Every link and form control is reachable by tab order. The contact form validates with visible text, not colour alone.
- **Landmarks.** Each page uses a single `<main>` region, a top `<nav>`, a section-level subnav where relevant, and a `<footer>`.
- **Breadcrumbs** on every content page indicate location within the site hierarchy.
- **Headings** follow a strict `h1` → `h2` → `h3` order; no heading levels are skipped for visual effect.
- **Typography.** Body text is set in Inter; headings in Fraunces. Both load from Google Fonts; if they fail to load, the site falls back to the system's default sans-serif and serif faces without loss of content.
- **Contrast.** Text and background meet WCAG AA contrast at normal body size; this is a goal, not an audit claim.
- **Images** on biography pages carry descriptive `alt` text. Placeholder SVGs for figures under construction are labelled as such.
- **No JavaScript is required** to read any content on this site. A single script adds `§` anchor links to prose headings as a convenience; disabling it does not hide content.

If anything on this site is inaccessible to you, please say so via the [contact form](/contact/).

---

## About this document

This page is regenerated from the site's source whenever a new blog post is published. It reflects the site as of the **Updated** date at the top. Historical versions are not retained.
"""


# ---------------------------------------------------------------------------
# Auto-block rewriting in hand-written docs
# ---------------------------------------------------------------------------

AUTO_BLOCK_RE = re.compile(
    r"(<!-- auto:(?P<name>[a-z_:]+):begin -->)(.*?)(<!-- auto:(?P=name):end -->)",
    flags=re.DOTALL,
)


def _rewrite_auto_blocks(path: Path, blocks: dict[str, str]) -> bool:
    """Overwrite the content of each named auto block in `path`. Returns True if
    the file changed. Blocks not present in `blocks` are left alone. An unknown
    block marker in the file is an error — we refuse to silently miss one."""
    text = path.read_text(encoding="utf-8")

    missing_in_file = [name for name in blocks if f"<!-- auto:{name}:begin -->" not in text]
    if missing_in_file:
        raise RuntimeError(
            f"{path}: expected auto-block(s) not found: {', '.join(missing_in_file)}"
        )

    def _replace(match: re.Match[str]) -> str:
        name = match.group("name")
        begin = match.group(1)
        end = match.group(4)
        if name not in blocks:
            return match.group(0)
        body = blocks[name]
        return f"{begin}\n{body}\n{end}"

    new_text = AUTO_BLOCK_RE.sub(_replace, text)
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def regenerate() -> None:
    today = _fmt_today()
    blog_paths = _blog_post_paths()
    blog_count = len(blog_paths)
    auckland_by_type = _auckland_counts()
    auckland_pages = _auckland_page_paths()
    auckland_pages_count = len(auckland_pages)
    total_entities = sum(auckland_by_type.values())
    url_rules = _url_rule_count()

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    sitemap_text = SITEMAP_TEMPLATE.format(
        today=today,
        year=date.today().year,
        tree=_tree_block(),
        counts=_counts_table(
            blog_count=blog_count,
            auckland_by_type=auckland_by_type,
            auckland_pages_count=auckland_pages_count,
        ),
    )

    sitemap_path = DOCS_DIR / "SITEMAP.md"
    prev = sitemap_path.read_text(encoding="utf-8") if sitemap_path.exists() else None
    sitemap_path.write_text(sitemap_text, encoding="utf-8")
    print(f"[regen_docs] {'updated' if prev != sitemap_text else 'unchanged'}: {sitemap_path.relative_to(ROOT)}")

    readme_meta = (
        f"**Updated:** {today}\n"
        f"**Blog posts:** {blog_count} · "
        f"**Auckland entities:** {total_entities} · "
        f"**Auckland generated pages:** {auckland_pages_count}"
    )
    arch_meta = (
        f"**Updated:** {today}\n"
        f"**Blog posts:** {blog_count} · "
        f"**Auckland entities:** {total_entities} · "
        f"**Auckland generated pages:** {auckland_pages_count} · "
        f"**URL rules:** {url_rules}"
    )

    readme_path = ROOT / "README.md"
    if readme_path.exists():
        changed = _rewrite_auto_blocks(readme_path, {"meta": readme_meta})
        print(f"[regen_docs] {'updated' if changed else 'unchanged'}: {readme_path.relative_to(ROOT)}")

    arch_path = DOCS_DIR / "ARCHITECTURE.md"
    if arch_path.exists():
        changed = _rewrite_auto_blocks(arch_path, {"meta": arch_meta})
        print(f"[regen_docs] {'updated' if changed else 'unchanged'}: {arch_path.relative_to(ROOT)}")


def main() -> int:
    try:
        regenerate()
    except Exception as exc:
        print(f"[regen_docs] FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
