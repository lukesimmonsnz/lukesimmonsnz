"""Pre-render the Flask app to static HTML for Cloudflare Pages.

Walks ``app.url_map``, hits every route via Flask's test client, and writes
the response to ``_site/``. Dynamic routes (blog posts, Auckland pages)
are enumerated from their source data and rendered one instance at a time.
The ``static/`` folder is mirrored verbatim into ``_site/static/``.

Design notes:

- Pure Python, no Frozen-Flask dependency. Uses ``app.test_client()`` so
  every rendering path (blueprints, context processors, after-request
  hooks) fires exactly as it would for a real visitor.
- Writes to ``<path>/index.html`` for trailing-slash URLs so static
  hosts serve them cleanly (Cloudflare Pages understands this).
- Skips POST-only routes; the contact form POST is handled by a
  Cloudflare Pages Function, not the frozen static output.
- Idempotent: full rebuild each run. ``_site/`` is wiped first.

Env vars consumed at freeze time:

- ``SITE_URL``           base URL (e.g. ``https://lukesimmonsnz.kiwi``).
- ``CONTACT_SUBMIT_URL`` where the contact form POSTs — for Pages this
                         is the Pages Function path (``/api/contact``).
- ``TURNSTILE_SITE_KEY`` Cloudflare Turnstile site key for bot protection.

Typical invocation::

    set SITE_URL=https://lukesimmonsnz.kiwi
    set CONTACT_SUBMIT_URL=/api/contact
    set TURNSTILE_SITE_KEY=0x4AAAAA...
    python scripts/freeze.py
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
STATIC_SRC = ROOT / "static"

# Routes whose paths start with any of these prefixes are excluded from the
# static build. The admin blueprint is a localhost-only editor — its UI
# would be inert on Pages anyway (no Flask backend), but we don't want it
# discoverable, indexable, or hint at the source architecture.
EXCLUDED_PATH_PREFIXES = ("/admin",)

# Make the project root importable as ``app`` etc.
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402


def _url_to_output_path(url: str) -> Path:
    """Map a URL path to the file on disk where its HTML should land.

    - ``/``            → ``_site/index.html``
    - ``/now/``        → ``_site/now/index.html``
    - ``/blog/feed.xml`` → ``_site/blog/feed.xml``
    - ``/robots.txt``  → ``_site/robots.txt``
    - ``/sitemap.xml`` → ``_site/sitemap.xml``
    """
    assert url.startswith("/")
    path = url.lstrip("/")
    if not path:
        return OUT / "index.html"
    if path.endswith("/"):
        return OUT / path / "index.html"
    if "." in Path(path).name:
        return OUT / path                      # file with extension
    return OUT / path / "index.html"           # treat as a pretty URL


def _enumerate_dynamic_urls() -> list[str]:
    """Enumerate the URL instances for dynamic routes."""
    urls: list[str] = []

    # Blog posts — read filenames under content/blog/
    blog_dir = ROOT / "content" / "blog"
    if blog_dir.exists():
        import frontmatter
        for md in sorted(blog_dir.glob("*.md")):
            # Skip draft posts — they shouldn't ship to production.
            try:
                fm = frontmatter.load(md)
                if (fm.metadata or {}).get("status") == "draft":
                    continue
            except Exception:
                pass
            # The blog blueprint derives slug from frontmatter or filename.
            slug = fm.metadata.get("slug") if fm.metadata.get("slug") else md.stem
            urls.append(f"/blog/{slug}/")

    # Per-region section + leaf URLs — derived from each region's page tree.
    # Skip underscore-prefixed directories (e.g. ``_sections/``) and stems —
    # these are internal aggregations consumed by the section route, not
    # standalone URLs.
    AOTEAROA_REGIONS = (
        "auckland", "wellington", "northland", "waikato", "bay-of-plenty",
        "gisborne", "hawkes-bay", "taranaki", "manawatu-whanganui",
        "nelson", "tasman", "marlborough", "west-coast", "canterbury",
        "otago", "southland",
    )
    for region in AOTEAROA_REGIONS:
        pages_dir = ROOT / "content" / region / "pages"
        if not pages_dir.exists():
            continue
        # Sections come from two sources: (a) consolidated essays at
        # pages/_sections/<theme>.md, and (b) legacy per-section directories
        # pages/<section>/. Either gives us a section URL to render.
        sections: set[str] = set()
        sections_dir = pages_dir / "_sections"
        if sections_dir.is_dir():
            for md in sections_dir.glob("*.md"):
                if not md.stem.startswith("_"):
                    sections.add(md.stem)
        for child in pages_dir.iterdir():
            if child.is_dir() and not child.name.startswith("_"):
                sections.add(child.name)
        for section in sorted(sections):
            urls.append(f"/research/{region}/{section}/")
            section_dir = pages_dir / section
            if section_dir.is_dir():
                for md in sorted(section_dir.glob("*.md")):
                    if md.stem.startswith("_"):
                        continue
                    urls.append(f"/research/{region}/{section}/{md.stem}/")

    # NZ pattern theme rollups — derived from content/nz/data/pattern/<theme>.*.yaml
    nz_pattern_dir = ROOT / "content" / "nz" / "data" / "pattern"
    if nz_pattern_dir.is_dir():
        nz_themes: set[str] = set()
        # Filenames are <theme>.<slug>.yaml; the theme prefix is an
        # entity-id-safe slug (e.g. "climate"), but the NZ theme URL uses the
        # full theme enum (e.g. "climate-adaptation"). Re-map known aliases.
        _NZ_THEME_URL = {"climate": "climate-adaptation"}
        for yml in nz_pattern_dir.glob("*.yaml"):
            head = yml.stem.split(".", 1)[0]
            if head:
                nz_themes.add(_NZ_THEME_URL.get(head, head))
        for theme in sorted(nz_themes):
            urls.append(f"/research/nz/{theme}/")

    return urls


def _enumerate_static_urls(app) -> list[str]:
    """Routes in app.url_map that have no arguments and support GET.

    Routes under EXCLUDED_PATH_PREFIXES are filtered out — see the
    constant's docstring for why.
    """
    urls: list[str] = []
    for rule in app.url_map.iter_rules():
        if rule.arguments:
            continue
        if "GET" not in (rule.methods or set()):
            continue
        if rule.endpoint == "static":
            continue
        if any(rule.rule.startswith(p) for p in EXCLUDED_PATH_PREFIXES):
            continue
        urls.append(rule.rule)
    return urls


def _scrub_excluded_from_sitemap() -> None:
    """Remove `<url>...</url>` blocks for excluded paths from sitemap.xml.

    The sitemap is generated by Flask itself (it walks the URL map) so it
    still mentions admin routes after freezing. Strip them post-hoc so the
    sitemap stops advertising paths we've decided to hide.
    """
    sitemap = OUT / "sitemap.xml"
    if not sitemap.exists():
        return
    text = sitemap.read_text(encoding="utf-8")
    import re
    pattern = re.compile(
        r"\s*<url>\s*<loc>\s*[^<]*?("
        + "|".join(re.escape(p) for p in EXCLUDED_PATH_PREFIXES)
        + r")[^<]*?</loc>.*?</url>",
        flags=re.DOTALL,
    )
    new_text, n = pattern.subn("", text)
    if n:
        sitemap.write_text(new_text, encoding="utf-8")
        print(f"[freeze] scrubbed {n} excluded URLs from sitemap.xml")


def _write_redirects() -> None:
    """Write a Cloudflare Pages _redirects file that 404s excluded paths.

    Belt-and-braces with the freeze-skip: even if some admin file slips
    into _site/ (or someone hand-drops a file there), Cloudflare itself
    will return 404 for /admin and /admin/anything at the edge.

    The trailing ``!`` is the *force* operator — Cloudflare's
    static-files-win behaviour normally lets a real file at the path
    override the redirect. Force makes the redirect win unconditionally.
    Three variants per prefix because Cloudflare matches paths exactly:
    ``/admin``, ``/admin/``, and ``/admin/anything`` are three distinct
    cases the wildcard alone doesn't cover reliably.
    """
    lines = []
    for prefix in EXCLUDED_PATH_PREFIXES:
        lines.append(f"{prefix} /404 404!")
        lines.append(f"{prefix}/ /404 404!")
        lines.append(f"{prefix}/* /404 404!")
    (OUT / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[freeze] wrote _redirects ({len(lines)} rules)")


def _freeze_url(client, url: str) -> tuple[bool, str]:
    out_path = _url_to_output_path(url)
    resp = client.get(url, follow_redirects=False)
    if resp.status_code in (301, 302, 308):
        # Flask is redirecting — usually a trailing-slash normalisation.
        target = resp.headers.get("Location", "")
        if target.startswith("http"):
            # Same host? strip.
            from urllib.parse import urlparse
            target = urlparse(target).path
        return _freeze_url(client, target)
    if resp.status_code != 200:
        return False, f"HTTP {resp.status_code}"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(resp.data)
    return True, f"{len(resp.data):,}B"


def main() -> int:
    import os

    # Load .env so values reach the Flask app regardless of which shell
    # invoked us. Real OS env vars still win — .env only fills gaps.
    sys.path.insert(0, str(ROOT))
    try:
        from agent._env import load_dotenv as _load_env
        _load_env()
    except Exception:
        pass

    # Enforce production-ish defaults when freezing; overridden by env vars.
    os.environ.setdefault("SITE_URL", "https://lukesimmonsnz.kiwi")
    os.environ.setdefault("CONTACT_SUBMIT_URL", "/api/contact")

    # Warn loudly if Turnstile key is missing — silent empty-string would
    # build a contact form without bot protection, which is what we just
    # spent a session debugging.
    if not os.environ.get("TURNSTILE_SITE_KEY", "").strip():
        print(
            "[freeze] WARNING — TURNSTILE_SITE_KEY is empty.\n"
            "         The contact form will deploy WITHOUT bot protection.\n"
            "         Add it to .env or your shell environment and re-run.",
            file=sys.stderr,
        )

    # Sanity check — when running under git-bash/MSYS, a leading slash in an
    # env value gets converted to a Windows path (e.g. "/api/contact" becomes
    # "C:/Program Files/Git/api/contact"). Detect that and refuse to build a
    # broken contact form.
    submit_url = os.environ.get("CONTACT_SUBMIT_URL", "")
    if submit_url and not (submit_url.startswith("/") or submit_url.startswith("http")):
        print(
            f"[freeze] FAIL — CONTACT_SUBMIT_URL looks mangled: {submit_url!r}.\n"
            "  If you're running from git-bash, prefix the command with "
            "`MSYS_NO_PATHCONV=1` or set the var from cmd.exe instead.",
            file=sys.stderr,
        )
        return 2

    app = create_app()
    # After-request rewrites rely on a RequestContext; the test client
    # pushes one for us per request.
    client = app.test_client()

    if OUT.exists():
        # Windows occasionally holds file handles briefly after a previous
        # run — retry with permission fix-up on denied entries.
        import stat
        def _handle_denied(func, path, exc_info):
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except Exception:
                pass
        shutil.rmtree(OUT, onerror=_handle_denied)
    OUT.mkdir(parents=True, exist_ok=True)

    # Copy the static folder wholesale.
    if STATIC_SRC.exists():
        shutil.copytree(STATIC_SRC, OUT / "static")
        print(f"[freeze] copied static/ ({sum(1 for _ in (OUT / 'static').rglob('*') if _.is_file())} files)")

    static_urls = _enumerate_static_urls(app)
    dynamic_urls = _enumerate_dynamic_urls()
    all_urls = sorted(set(static_urls + dynamic_urls))

    print(f"[freeze] {len(all_urls)} URLs to render "
          f"({len(static_urls)} static + {len(dynamic_urls)} dynamic)")

    failures: list[tuple[str, str]] = []
    for url in all_urls:
        ok, msg = _freeze_url(client, url)
        status = "OK" if ok else "FAIL"
        if ok:
            pass  # quiet; uncomment for verbose
        else:
            failures.append((url, msg))
            print(f"  {status}  {url}  ({msg})")

    # Freeze a 404 page by hitting a known-bad URL; the error handler
    # renders 404.html.
    resp = client.get("/__does_not_exist__")
    if resp.status_code == 404:
        (OUT / "404.html").write_bytes(resp.data)
        print("[freeze] wrote 404.html")

    # Post-build: strip excluded paths from sitemap, drop _redirects.
    _scrub_excluded_from_sitemap()
    _write_redirects()

    print(f"[freeze] done. {len(all_urls) - len(failures)} OK, {len(failures)} failed.")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
