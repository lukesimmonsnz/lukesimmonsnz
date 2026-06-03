"""Blog blueprint — reads Markdown posts with YAML front-matter from content/blog/.

Post files are named YYYY-MM-DD-<slug>.md. The URL stem is the full filename
stem (so each post URL contains its date). Front-matter keys:

    title          — required, string
    date           — required, ISO date (YAML auto-parses YYYY-MM-DD)
    author         — "luke" | "agent" (default: "luke")
    summary        — one-line lede shown in the post list
    excerpt        — 1-2 sentence summary for cards; falls back to summary
    featured_image — dict: src, alt, focal (v2-10)
    tags           — list of strings

The blueprint is a pure reader: it does not create, modify, or delete posts.
The agent (under /agent) is the writer.
"""

import re
from collections import OrderedDict
from datetime import date as _date, datetime
from pathlib import Path

import frontmatter
import markdown
from flask import Blueprint, abort, current_app, make_response, render_template

from blueprints.admin.cms.blocks.renderer import render_md_with_blocks

blog_bp = Blueprint("blog", __name__)

POSTS_DIR = Path(__file__).resolve().parent.parent / "content" / "blog"

# Number of most-recent posts shown full-width on /blog/. Older posts
# move to the archive sidebar, grouped by year.
RECENT_POST_COUNT = 3

_FIRST_P_RE = re.compile(r"<p>(.*?)</p>", re.DOTALL)


def _markdown():
    return markdown.Markdown(
        extensions=["extra", "codehilite", "sane_lists", "smarty"],
        output_format="html5",
    )


def _normalise_date(value):
    if isinstance(value, _date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).date()
        except ValueError:
            return None
    return None


def _format_date(d):
    if not d:
        return ""
    return d.strftime("%d %B %Y").lstrip("0")


def _format_date_short(d):
    if not d:
        return ""
    return d.strftime("%d %b").lstrip("0")


def _first_paragraph(html: str) -> str:
    """Extract plain text of the first <p> from rendered HTML."""
    m = _FIRST_P_RE.search(html)
    if not m:
        return ""
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()


def _load_post(path: Path):
    fm = frontmatter.load(path)
    meta = fm.metadata or {}
    body_html = render_md_with_blocks(fm.content, current_app.jinja_env)
    date = _normalise_date(meta.get("date"))
    # featured_image: dict with keys src, alt, focal
    fi_raw = meta.get("featured_image") or {}
    featured_image = (
        {
            "src":   fi_raw.get("src", ""),
            "alt":   fi_raw.get("alt", ""),
            "focal": fi_raw.get("focal", "0.5,0.5"),
        }
        if fi_raw and fi_raw.get("src")
        else None
    )
    # excerpt: explicit > summary > first paragraph
    excerpt = meta.get("excerpt") or meta.get("summary") or _first_paragraph(body_html)
    return {
        "slug":           path.stem,
        "title":          meta.get("title") or path.stem,
        "date":           date,
        "date_display":   _format_date(date),
        "date_display_short": _format_date_short(date),
        "author":         (meta.get("author") or "luke").lower(),
        "summary":        meta.get("summary"),
        "excerpt":        excerpt,
        "featured_image": featured_image,
        "tags":           [str(t) for t in (meta.get("tags") or [])],
        "body_html":      body_html,
    }


def _all_posts():
    if not POSTS_DIR.exists():
        return []
    posts = [_load_post(p) for p in POSTS_DIR.glob("*.md")]
    posts.sort(key=lambda p: p["date"] or _date.min, reverse=True)
    return posts


def _split_recent_and_archive(posts, today=None):
    """Take the N most recent posts as 'recent', the rest as 'archive'
    grouped by year. `posts` must already be date-sorted descending."""
    recent = posts[:RECENT_POST_COUNT]
    older  = posts[RECENT_POST_COUNT:]
    by_year = OrderedDict()
    for p in older:
        year = p["date"].year if p["date"] else "Undated"
        by_year.setdefault(year, []).append(p)
    return recent, by_year


def _all_tags(posts):
    """Return sorted list of (tag, count) tuples, descending by count."""
    counts: dict[str, int] = {}
    for p in posts:
        for tag in p.get("tags") or []:
            counts[tag] = counts.get(tag, 0) + 1
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))


# ── Routes ─────────────────────────────────────────────────────────────────

@blog_bp.route("/")
def index():
    posts = _all_posts()
    recent, archive = _split_recent_and_archive(posts)
    return render_template(
        "blog/index.html",
        posts=recent,
        archive=archive,
        recent_count=RECENT_POST_COUNT,
    )


@blog_bp.route("/feed.xml")
def feed():
    posts = _all_posts()[:20]
    last_updated = posts[0]["date"] if posts else _date.today()
    xml = render_template("blog/feed.xml", posts=posts, last_updated=last_updated)
    resp = make_response(xml)
    resp.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
    return resp


@blog_bp.route("/tag/")
def tag_index():
    posts = _all_posts()
    tags = _all_tags(posts)
    return render_template("blog/tag_index.html", tags=tags)


@blog_bp.route("/tag/<slug>/")
def tag_archive(slug):
    posts = _all_posts()
    matching = [p for p in posts if slug in (p.get("tags") or [])]
    if not matching:
        abort(404)
    return render_template("blog/tag_archive.html", tag=slug, posts=matching)


@blog_bp.route("/<slug>/")
def post(slug):
    path = POSTS_DIR / f"{slug}.md"
    if not path.exists() or not path.is_file():
        abort(404)
    all_posts = _all_posts()
    current = next((p for p in all_posts if p["slug"] == slug), None)
    if current is None:
        abort(404)
    idx = all_posts.index(current)
    newer = all_posts[idx - 1] if idx > 0 else None
    older = all_posts[idx + 1] if idx + 1 < len(all_posts) else None
    return render_template("blog/post.html", post=current, newer=newer, older=older)
