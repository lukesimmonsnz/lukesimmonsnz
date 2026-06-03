"""CMS Flask blueprint — wave 3 / ι + ε + v2 routes."""
from __future__ import annotations

import json

from flask import (
    Blueprint, abort, current_app, jsonify, redirect,
    render_template, request, url_for,
)

from blueprints.admin.cms import (
    drafts, history as history_mod, media as media_mod,
    overlay as overlay_mod, publish as publish_mod, search as search_mod,
    settings as settings_mod, tree, theme as theme_mod, seo as seo_mod,
)
from blueprints.admin.cms.resolver import LockKind, PageKind, resolve


cms_bp = Blueprint(
    "cms", __name__,
    url_prefix="/admin",
    template_folder="../../../templates/admin/cms",
)


# ── ι: landing & tree ────────────────────────────────────────────────


@cms_bp.get("/")
def landing():
    root = tree.build_tree()
    dirty = drafts.list_dirty() if hasattr(drafts, "list_dirty") else []
    return render_template("admin/cms/index.html", tree=root, dirty=dirty)


@cms_bp.get("/tree.json")
def tree_json():
    return jsonify(tree.to_dict(tree.build_tree()) if hasattr(tree, "to_dict") else {})


# ── ε: editor + draft API ────────────────────────────────────────────


def _get_page_id() -> str:
    page_id = request.args.get("id", "").strip()
    if not page_id:
        abort(400, description="missing ?id=<page_url>")
    return page_id


def _require_editable_pageref(page_id: str):
    ref = resolve(page_id)
    if ref is None:
        abort(404, description=f"no page for id={page_id!r}")
    if ref.lock != LockKind.EDITABLE:
        abort(403, description=f"page {page_id} is {ref.lock.value}")
    return ref


@cms_bp.get("/edit/")
def edit():
    page_id = _get_page_id()
    ref = _require_editable_pageref(page_id)
    if ref.kind == PageKind.SETTINGS:
        parts = [p for p in page_id.strip("/").split("/") if p]
        if len(parts) >= 3 and parts[0] == "admin" and parts[1] == "settings":
            return redirect(url_for("cms.settings_group", group=parts[2]))
        return redirect(url_for("cms.settings_landing"))

    existing = drafts.get_draft(page_id)
    if existing is not None:
        body = existing.body
        frontmatter = existing.frontmatter or ""
        base_sha = existing.base_sha
        from_draft = True
    else:
        try:
            state = ref.projection.load(ref.source_paths)
        except NotImplementedError as e:
            abort(501, description=str(e))
        body = state.body
        frontmatter = state.frontmatter or ""
        base_sha = drafts.hash_concat(ref.source_paths)
        from_draft = False

    return render_template(
        "admin/cms/editor.html",
        page_id=page_id, ref=ref, body=body,
        frontmatter=frontmatter, base_sha=base_sha, from_draft=from_draft,
    )


@cms_bp.get("/api/draft/")
def api_draft_get():
    page_id = _get_page_id()
    d = drafts.get_draft(page_id)
    if d is None:
        return jsonify(None), 404
    return jsonify({
        "page_id":     d.page_id, "body": d.body,
        "frontmatter": d.frontmatter, "base_sha": d.base_sha,
        "updated":     d.updated.isoformat(), "by_user": d.by_user,
    })


@cms_bp.put("/api/draft/")
def api_draft_put():
    page_id = _get_page_id()
    _require_editable_pageref(page_id)
    payload = request.get_json(silent=True) or {}
    body = payload.get("body", "")
    frontmatter = payload.get("frontmatter")
    base_sha = payload.get("base_sha", "")
    if not isinstance(body, str):
        abort(400, description="body must be string")
    if frontmatter is not None and not isinstance(frontmatter, str):
        abort(400, description="frontmatter must be string or null")
    if not isinstance(base_sha, str) or not base_sha:
        abort(400, description="base_sha required")
    drafts.put_draft(page_id=page_id, body=body, frontmatter=frontmatter,
                    base_sha=base_sha, by_user=None)
    d = drafts.get_draft(page_id)
    if d is None:
        abort(500, description="put_draft did not persist")
    return jsonify({"ok": True, "base_sha": d.base_sha, "updated": d.updated.isoformat()})


@cms_bp.delete("/api/draft/")
def api_draft_delete():
    page_id = _get_page_id()
    drafts.drop_draft(page_id)
    return jsonify({"ok": True})


@cms_bp.post("/api/publish/")
def api_publish():
    page_id = _get_page_id()
    _require_editable_pageref(page_id)
    payload = request.get_json(silent=True) or {}
    msg = payload.get("commit_message")
    ref = resolve(page_id)
    if ref is not None and drafts.has_conflict(page_id, ref.source_paths):
        return jsonify({"ok": False, "code": "conflict",
                       "message": "on-disk source has changed since draft was opened"}), 409
    result = publish_mod.publish(page_id, commit_message=msg)
    return jsonify({
        "ok": result.ok,
        "written": [str(p) for p in result.written],
        "rendered": [str(p) for p in result.rendered],
        "lint_errors": [{"severity": e.severity, "code": e.code, "path": str(e.path), "message": e.message} for e in result.lint_errors],
        "lint_warnings": [{"severity": w.severity, "code": w.code, "path": str(w.path), "message": w.message} for w in result.lint_warnings],
        "commit_sha": result.commit_sha, "message": result.message,
    }), (200 if result.ok else 422)


# ── settings (wave 4 / ζ) ────────────────────────────────────────────


@cms_bp.get("/settings/")
def settings_landing():
    return render_template("admin/cms/settings/index.html",
        groups=settings_mod.GROUPS,
        labels=settings_mod.GROUP_LABELS,
        snapshot=settings_mod.all_groups())


@cms_bp.get("/settings/<group>/")
def settings_group(group: str):
    if group not in settings_mod.GROUPS:
        abort(404, description=f"unknown settings group: {group}")
    value = settings_mod.get_group(group)
    # v2-7: nav gets its own drag-reorder UI
    if group == "nav":
        return render_template("admin/cms/settings/nav.html",
            group=group, label=settings_mod.GROUP_LABELS[group],
            groups=settings_mod.GROUPS, labels=settings_mod.GROUP_LABELS,
            value_json=json.dumps(value, ensure_ascii=False))
    return render_template("admin/cms/settings/group.html",
        group=group, label=settings_mod.GROUP_LABELS[group],
        groups=settings_mod.GROUPS, labels=settings_mod.GROUP_LABELS,
        value_json=json.dumps(value, ensure_ascii=False, indent=2))


@cms_bp.put("/api/settings/<group>/")
def api_settings_put(group: str):
    if group not in settings_mod.GROUPS:
        abort(404, description=f"unknown settings group: {group}")
    payload = request.get_json(silent=True) or {}
    if "value" not in payload:
        abort(400, description="missing 'value' in body")
    settings_mod.put_group(group, payload["value"])
    return jsonify({"ok": True})


@cms_bp.post("/api/settings/publish/")
def api_settings_publish():
    json_path, css_path = settings_mod.publish_settings()
    return jsonify({"ok": True, "site_settings": str(json_path),
                   "theme_css": str(css_path),
                   "theme_css_bust": settings_mod.theme_css_cache_bust()})


# ── v2-4 — theme customizer ─────────────────────────────────────────


@cms_bp.get("/theme/")
def theme_customizer():
    active_preset = settings_mod.get_active_preset()
    override = settings_mod.get_group("theme")
    defaults = theme_mod.load_defaults()
    if active_preset in theme_mod.KNOWN_PRESETS:
        preset = theme_mod.load_preset(active_preset)
        effective = theme_mod.compose(theme_mod.compose(defaults, preset), override or {})
    else:
        effective = theme_mod.compose(defaults, override or {})
    return render_template("admin/cms/theme/index.html",
        active_preset=active_preset,
        known_presets=theme_mod.KNOWN_PRESETS,
        effective=effective,
        override_json=json.dumps(override, ensure_ascii=False, indent=2))


@cms_bp.put("/api/theme/preset/")
def api_theme_preset():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name", "")
    if not isinstance(name, str) or not name:
        abort(400, description="name required")
    try:
        settings_mod.set_active_preset(name)
    except ValueError as e:
        abort(400, description=str(e))
    return jsonify({"ok": True, "active_preset": name})


@cms_bp.put("/api/theme/override/")
def api_theme_override():
    payload = request.get_json(silent=True) or {}
    override = payload.get("value")
    if not isinstance(override, dict):
        abort(400, description="value must be object")
    settings_mod.put_group("theme", override)
    return jsonify({"ok": True})


@cms_bp.post("/api/theme/publish/")
def api_theme_publish():
    json_path, css_path = settings_mod.publish_settings()
    return jsonify({"ok": True, "site_settings": str(json_path),
                   "theme_css": str(css_path),
                   "theme_css_bust": settings_mod.theme_css_cache_bust()})


# ── v2-8 — SEO panel ────────────────────────────────────────────────


@cms_bp.get("/api/seo/")
def api_seo_get():
    page_id = _get_page_id()
    d = drafts.get_draft(page_id)
    seo_dict = {}
    if d and d.frontmatter:
        try:
            import yaml
            parsed = yaml.safe_load(d.frontmatter) or {}
            seo_dict = parsed.get("seo") or {}
        except yaml.YAMLError:
            seo_dict = {}
    return jsonify({"ok": True, "seo": seo_dict})


@cms_bp.put("/api/seo/")
def api_seo_put():
    page_id = _get_page_id()
    _require_editable_pageref(page_id)
    payload = request.get_json(silent=True) or {}
    new_seo = payload.get("seo")
    if not isinstance(new_seo, dict):
        abort(400, description="seo must be object")
    d = drafts.get_draft(page_id)
    if d is None:
        abort(404, description="no active draft for this page")
    raw_fm = d.frontmatter or ""
    spliced = seo_mod.splice_seo_into_frontmatter(raw_fm, new_seo)
    drafts.put_draft(page_id=page_id, body=d.body, frontmatter=spliced,
                    base_sha=d.base_sha, by_user=None)
    return jsonify({"ok": True, "frontmatter": spliced})


# ── media library page (wave 2 item 8 — page wrapper) ───────────────


@cms_bp.get("/media/")
def media_landing():
    return render_template("admin/cms/media/index.html")


# ── history / diff / restore (wave 4 / θ) ────────────────────────────


@cms_bp.get("/history/")
def history_landing():
    page_id = _get_page_id()
    ref = resolve(page_id)
    if ref is None:
        abort(404, description=f"no page for id={page_id!r}")
    commits = history_mod.commits_for_page(page_id, limit=50)
    return render_template(
        "admin/cms/history/index.html",
        page_id=page_id, ref=ref,
        commits=[c.to_dict() for c in commits],
    )


@cms_bp.get("/api/history/")
def api_history():
    page_id = _get_page_id()
    commits = history_mod.commits_for_page(page_id, limit=50)
    return jsonify({"ok": True, "commits": [c.to_dict() for c in commits]})


@cms_bp.get("/diff/")
def history_diff():
    page_id = _get_page_id()
    ref = resolve(page_id)
    if ref is None:
        abort(404, description=f"no page for id={page_id!r}")
    from_sha = (request.args.get("from") or "").strip()
    to_sha = (request.args.get("to") or "").strip() or None
    if not from_sha:
        abort(400, description="missing ?from=<sha>")
    try:
        diff_text = history_mod.diff(page_id, from_sha, to_sha)
    except ValueError as e:
        abort(400, description=str(e))
    return render_template(
        "admin/cms/history/diff.html",
        page_id=page_id, ref=ref,
        from_sha=from_sha, to_sha=to_sha,
        diff_text=diff_text,
    )


@cms_bp.post("/api/restore/")
def api_restore():
    page_id = _get_page_id()
    sha = (request.args.get("sha") or "").strip()
    if not sha:
        abort(400, description="missing ?sha=<sha>")
    try:
        history_mod.restore_to_draft(page_id, sha)
    except history_mod.RestoreError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    return jsonify({"ok": True, "edit_url": url_for("cms.edit", id=page_id)})


# ── search & replace (wave 4 item 10 / η) ────────────────────────────


@cms_bp.get("/search/")
def search_landing():
    q = (request.args.get("q") or "").strip()
    whole_word = request.args.get("whole_word", "1") not in ("0", "false", "")
    matches = search_mod.find_matches(q, whole_word=whole_word) if q else []
    by_page: dict[str, list] = {}
    for m in matches:
        by_page.setdefault(m.page_id, []).append(m)
    return render_template(
        "admin/cms/search/index.html",
        q=q, whole_word=whole_word,
        matches=matches, by_page=by_page,
        total_matches=len(matches), total_pages=len(by_page),
    )


@cms_bp.post("/api/search/replace/")
def api_search_replace():
    payload = request.get_json(silent=True) or {}
    find = payload.get("find", "")
    replace = payload.get("replace", "")
    page_ids = payload.get("page_ids", [])
    whole_word = bool(payload.get("whole_word", True))
    if not isinstance(find, str) or not find:
        abort(400, description="find required")
    if not isinstance(replace, str):
        abort(400, description="replace must be string")
    if not isinstance(page_ids, list):
        abort(400, description="page_ids must be array")
    try:
        results = search_mod.apply_replaces(
            find=find, replace=replace,
            page_ids=page_ids, whole_word=whole_word,
        )
    except search_mod.ReplaceError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    return jsonify({
        "ok":             True,
        "drafts_created": len(results),
        "results":        results,
    })



# ── v2-2: block parse / serialize API ───────────────────────────────


def _tree_to_json(tree):
    """BlockTree → JSON-serialisable list (recursive).

    Wire format: span:[start, end] (aligned with json_adapter.py).
    """
    from .blocks.tree import Block as _Block, RawSpan as _RawSpan
    out = []
    for node in tree:
        if isinstance(node, _RawSpan):
            out.append({'type': 'raw', 'text': node.text,
                        'span': [node.span.start, node.span.end]})
        elif isinstance(node, _Block):
            body = node.body if isinstance(node.body, str) else _tree_to_json(node.body)
            out.append({'type': 'block', 'kind': node.kind,
                        'attrs': [list(p) for p in node.attrs],
                        'level': node.level, 'dirty': node.dirty,
                        'span': [node.span.start, node.span.end],
                        'body': body})
    return out


def _json_to_tree(nodes_json):
    """JSON list → BlockTree (recursive).

    Accepts span:[start, end] wire format (aligned with json_adapter.py).
    """
    from .blocks.tree import Block as _Block, RawSpan as _RawSpan, SourceSpan as _SS
    out = []
    for n in nodes_json:
        if n.get('type') == 'raw':
            sp = n.get('span', [0, len(n.get('text', ''))])
            out.append(_RawSpan(text=n['text'], span=_SS(sp[0], sp[1])))
        elif n.get('type') == 'block':
            raw = n.get('body', '')
            body = raw if isinstance(raw, str) else tuple(_json_to_tree(raw))
            sp = n.get('span', [0, 0])
            out.append(_Block(
                kind=n['kind'],
                attrs=tuple(tuple(p) for p in n.get('attrs', [])),
                body=body,
                span=_SS(sp[0], sp[1]),
                level=n.get('level', 0),
                dirty=bool(n.get('dirty', False)),
            ))
    return tuple(out)


@cms_bp.post("/api/blocks/parse/")
def api_blocks_parse():
    """POST {body} → {ok, nodes}  — parse Markdown into block tree JSON."""
    from .blocks import parse as _parse
    data = request.get_json(force=True) or {}
    try:
        tree = _parse(data.get('body', ''))
        return jsonify({'ok': True, 'nodes': _tree_to_json(tree)})
    except Exception as exc:
        return jsonify({'ok': False, 'error': str(exc)}), 400


@cms_bp.post("/api/blocks/serialize/")
def api_blocks_serialize():
    """POST {nodes, source} → {ok, body}  — serialize block tree to Markdown."""
    from .blocks import serialize as _serialize
    data = request.get_json(force=True) or {}
    try:
        tree = _json_to_tree(data.get('nodes', []))
        body = _serialize(tree, data.get('source', ''))
        return jsonify({'ok': True, 'body': body})
    except Exception as exc:
        return jsonify({'ok': False, 'error': str(exc)}), 400


@cms_bp.get("/api/blocks/registry/")
def api_blocks_registry():
    """GET -> {ok, blocks: {kind: spec}}  -- registered block kind specs."""
    from .blocks.registry import load_registry
    import dataclasses
    reg = load_registry()
    blocks = {k: dataclasses.asdict(v) for k, v in reg.items()}
    return jsonify({'ok': True, 'blocks': blocks})


# ── preview iframe ───────────────────────────────────────────────────


@cms_bp.get("/preview/")
def preview():
    page_id = _get_page_id()
    ref = resolve(page_id)
    if ref is None:
        abort(404)
    if ref.kind == PageKind.PROJECTED:
        return render_template(
            "admin/cms/preview_stub.html",
            page_id=page_id, ref=ref, public_url=page_id,
        )
    draft = drafts.get_draft(page_id)
    if draft is None:
        return render_template(
            "admin/cms/preview_stub.html",
            page_id=page_id, ref=ref, public_url=page_id,
        )
    try:
        from blueprints.admin.cms.resolver import EditorState
        state = EditorState(
            body=draft.body,
            frontmatter=draft.frontmatter,
            extras={"path": ref.source_paths[0] if ref.source_paths else None},
        )
        writes = ref.projection.save(state)
    except Exception:
        return render_template(
            "admin/cms/preview_stub.html",
            page_id=page_id, ref=ref, public_url=page_id,
        )
    intercepts = {}
    for w in writes:
        try:
            intercepts[w.path.resolve()] = w.content
        except OSError:
            continue
    overlay = overlay_mod.Overlay(intercepts=intercepts)
    with overlay_mod.overlay_active(overlay):
        client = current_app.test_client()
        resp = client.get(page_id, follow_redirects=True)
    return resp.data, resp.status_code, dict(resp.headers)
