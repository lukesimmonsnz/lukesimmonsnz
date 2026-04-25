import json
from datetime import date as _date, datetime, timezone
from pathlib import Path

import markdown
from flask import Blueprint, abort, current_app, make_response, render_template, request, url_for

from data.projects import PROJECTS

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

main_bp = Blueprint("main", __name__)

MESSAGES_FILE = Path(__file__).resolve().parent.parent / "data" / "messages.jsonl"

# Hand-updated when the /now/ page's content meaningfully changes.
NOW_LAST_UPDATED = "21 April 2026"


@main_bp.route("/")
def home():
    return render_template("main/home.html")


@main_bp.route("/now/")
def now():
    return render_template("main/now.html", last_updated=NOW_LAST_UPDATED)


@main_bp.route("/projects/")
def projects():
    return render_template("main/projects.html", projects=PROJECTS)


VALID_TOPICS = {
    "david-simmons",
    "research",
    "projects",
    "blog",
    "correction",
    "other",
}


@main_bp.route("/contact/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        topic = (request.form.get("topic") or "").strip()
        message = (request.form.get("message") or "").strip()

        errors = {}
        if not name:
            errors["name"] = "Please enter your name."
        if not email:
            errors["email"] = "Please enter an email address."
        if not topic:
            errors["topic"] = "Please pick a topic so I can find your message faster."
        elif topic not in VALID_TOPICS:
            errors["topic"] = "Please pick one of the listed topics."
        if not message:
            errors["message"] = "Please write a message."

        if errors:
            return render_template(
                "main/contact.html",
                errors=errors,
                form={"name": name, "email": email, "topic": topic, "message": message},
            )

        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "name": name,
            "email": email,
            "topic": topic,
            "message": message,
        }
        MESSAGES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with MESSAGES_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return render_template("main/contact.html", submitted=True)

    return render_template("main/contact.html")


@main_bp.route("/contact/thanks/")
def contact_thanks():
    """Destination the Cloudflare Pages Function redirects to after send.

    Also reachable in local dev by appending ``?thanks=1`` to the contact
    URL — useful for previewing the template without submitting anything.
    """
    return render_template("main/contact.html", submitted=True)


# --- Live sitemap page ------------------------------------------------------

# Renders docs/SITEMAP.md as an HTML page at /sitemap/. The file is produced
# by agent/regen_docs.py and re-read on every request — no caching, since
# content changes at regen time, not request time.


@main_bp.route("/sitemap/")
def sitemap_html():
    path = DOCS_DIR / "SITEMAP.md"
    if not path.is_file():
        abort(404)
    text = path.read_text(encoding="utf-8")
    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "smarty", "tables"],
        output_format="html5",
    )
    body_html = md.convert(text)
    return render_template("main/sitemap.html", body_html=body_html)


# --- SEO endpoints ----------------------------------------------------------

# Endpoints to exclude from the sitemap (error pages, form POST targets etc.).
# Everything else that's a zero-argument GET route is considered public.
_SITEMAP_EXCLUDED_ENDPOINTS = {"static", "main.robots_txt", "main.sitemap_xml"}


def _public_static_urls():
    """All zero-argument, GET-reachable URLs, excluding SEO + static endpoints."""
    urls = []
    for rule in current_app.url_map.iter_rules():
        if rule.arguments:
            continue
        if rule.endpoint in _SITEMAP_EXCLUDED_ENDPOINTS:
            continue
        if "GET" not in rule.methods:
            continue
        urls.append(url_for(rule.endpoint))
    return sorted(set(urls))


@main_bp.route("/sitemap.xml")
def sitemap_xml():
    """XML sitemap covering every public page, including blog posts."""
    # Imported lazily to avoid circular imports at module load time.
    from blueprints.blog import _all_posts  # type: ignore[attr-defined]

    static_urls = _public_static_urls()
    posts = _all_posts()
    blog_entries = [
        {
            "loc": url_for("blog.post", slug=p["slug"]),
            "lastmod": p["date"].isoformat() if p["date"] else None,
        }
        for p in posts
    ]
    today = _date.today().isoformat()
    xml = render_template(
        "main/sitemap.xml",
        static_urls=static_urls,
        blog_entries=blog_entries,
        today=today,
    )
    resp = make_response(xml)
    resp.headers["Content-Type"] = "application/xml; charset=utf-8"
    return resp


@main_bp.route("/robots.txt")
def robots_txt():
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {current_app.config['SITE_URL']}{url_for('main.sitemap_xml')}\n"
    )
    resp = make_response(body)
    resp.headers["Content-Type"] = "text/plain; charset=utf-8"
    return resp
