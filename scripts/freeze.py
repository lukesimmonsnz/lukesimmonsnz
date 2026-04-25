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

    # Auckland sections + pages — derived from the page tree.
    pages_dir = ROOT / "content" / "auckland" / "pages"
    if pages_dir.exists():
        sections = {p.parent.name for p in pages_dir.rglob("*.md")}
        for section in sorted(sections):
            urls.append(f"/research/auckland/{section}/")
            for md in sorted((pages_dir / section).glob("*.md")):
                urls.append(f"/research/auckland/{section}/{md.stem}/")

    return urls


def _enumerate_static_urls(app) -> list[str]:
    """Routes in app.url_map that have no arguments and support GET."""
    urls: list[str] = []
    for rule in app.url_map.iter_rules():
        if rule.arguments:
            continue
        if "GET" not in (rule.methods or set()):
            continue
        if rule.endpoint == "static":
            continue
        urls.append(rule.rule)
    return urls


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
    # Enforce production-ish defaults when freezing; overridden by env vars.
    os.environ.setdefault("SITE_URL", "https://lukesimmonsnz.kiwi")
    os.environ.setdefault("CONTACT_SUBMIT_URL", "/api/contact")

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

    print(f"[freeze] done. {len(all_urls) - len(failures)} OK, {len(failures)} failed.")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
