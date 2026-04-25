"""Blog blueprint — reads Markdown posts with YAML front-matter from content/blog/.

Post files are named YYYY-MM-DD-<slug>.md. The URL stem is the full filename
stem (so each post URL contains its date). Front-matter keys:

    title    — required, string
    date     — required, ISO date (YAML auto-parses YYYY-MM-DD)
    author   — "luke" | "agent" (default: "luke")
    summary  — one-line lede shown in the post list
    tags     — list of strings

The blueprint is a pure reader: it does not create, modify, or delete posts.
The agent (under /agent) is the writer.
"""

from collections import OrderedDict
from datetime import date as _date, datetime, timedelta
from pathlib import Path

import frontmatter
import markdown
from flask import Blueprint, abort, make_response, render_template

blog_bp = Blueprint("blog", __name__)

POSTS_DIR = Path(__file__).resolve().parent.parent / "content" / "blog"

# Posts within this window appear full-width on /blog/.
# Older posts move to the archive sidebar, grouped by year.
RECENT_WINDOW_DAYS = 7


def _markdown():
    # Fresh converter per call — Markdown's stateful reset isn't threadsafe.
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
    # Platform-neutral leading-zero strip (Windows strftime lacks %-d).
    return d.strftime("%d %B %Y").lstrip("0")


def _format_date_short(d):
    """Day + abbreviated month, no year (archive sidebar uses year as heading)."""
    if not d:
        return ""
    return d.strftime("%d %b").lstrip("0")


def _load_post(path: Path):
    fm = frontmatter.load(path)
    meta = fm.metadata or {}
    body_html = _markdown().convert(fm.content)
    date = _normalise_date(meta.get("date"))
    return {
        "slug": path.stem,
        "title": meta.get("title") or path.stem,
        "date": date,
        "date_display": _format_date(date),
        "date_display_short": _format_date_short(date),
        "author": (meta.get("author") or "luke").lower(),
        "summary": meta.get("summary"),
        "tags": meta.get("tags") or [],
        "body_html": body_html,
    }


def _all_posts():
    if not POSTS_DIR.exists():
        return []
    posts = [_load_post(p) for p in POSTS_DIR.glob("*.md")]
    posts.sort(key=lambda p: p["date"] or _date.min, reverse=True)
    return posts


def _split_recent_and_archive(posts, today=None):
    """Recent = posts dated within the last RECENT_WINDOW_DAYS.
    Archive = everything older, grouped by year (descending)."""
    if today is None:
        today = _date.today()
    cutoff = today - timedelta(days=RECENT_WINDOW_DAYS)
    recent = [p for p in posts if p["date"] and p["date"] >= cutoff]
    older = [p for p in posts if not p["date"] or p["date"] < cutoff]
    by_year = OrderedDict()
    for p in older:
        year = p["date"].year if p["date"] else "Undated"
        by_year.setdefault(year, []).append(p)
    return recent, by_year


@blog_bp.route("/")
def index():
    posts = _all_posts()
    recent, archive = _split_recent_and_archive(posts)
    return render_template(
        "blog/index.html",
        posts=recent,
        archive=archive,
        window_days=RECENT_WINDOW_DAYS,
    )


@blog_bp.route("/feed.xml")
def feed():
    """Atom feed of the most recent posts (newest first)."""
    posts = _all_posts()[:20]
    last_updated = posts[0]["date"] if posts else _date.today()
    xml = render_template(
        "blog/feed.xml",
        posts=posts,
        last_updated=last_updated,
    )
    resp = make_response(xml)
    resp.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
    return resp


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
