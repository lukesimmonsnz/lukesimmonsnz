"""Render Auckland map specs to SVG.

Sibling to ``render_charts.py``. Reads YAML specs from
``content/auckland/data/maps/*.yaml``; fetches GeoJSON from a public ArcGIS
FeatureServer; projects lat/lon to the SVG viewport (equirectangular,
latitude-corrected); emits one ``<path>`` element per feature.

Pure Python — uses the standard library for HTTP, PyYAML for specs, no
shapely/geopandas/GDAL. Good enough for simple Auckland-scale maps rendered
as styled figures, not geodetic tools.

Idempotent in two directions:
- A cached GeoJSON under ``data/maps/cache/<id>.geojson`` is reused until
  the spec changes or ``--refresh`` is passed.
- The output SVG is skipped if it is newer than every input and lacks the
  ``data-pipeline=render_maps`` signature (the same escape-hatch pattern as
  the chart renderer).

Exit codes: 0 ok / 1 errors encountered.

Spec shape (v1)::

    id: volcanic-viewshaft-contours
    title: Locally significant volcanic viewshaft contours, Auckland
    subtitle: Height-sensitive contours radiating from protected cones
    feature_service:
      url: https://services1.arcgis.com/<org>/arcgis/rest/services/<layer>/FeatureServer
      layer: 0
      where: "1=1"                       # optional, default 1=1
      out_fields: [CONTOUR]              # optional, default OBJECTID only
      page_size: 2000                    # optional
    style:
      stroke: "#b45b2e"                  # default palette if omitted
      stroke_width: 0.6
      fill: none
      fill_opacity: 0.4
      category_field: null               # optional; colour by this property
    bounds:                              # optional; auto-computed otherwise
      min_lon: 174.6
      min_lat: -36.95
      max_lon: 175.0
      max_lat: -36.75
    source:
      label: Auckland Council Open Data — ...
      url: https://data-aucklandcouncil.opendata.arcgis.com/...
    status: placeholder | verified
    manual: false                        # same flag as charts
"""
from __future__ import annotations

import json
import math
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

import yaml

ROOT = Path(__file__).resolve().parents[3]
SPECS_DIR = ROOT / "content" / "auckland" / "data" / "maps"
CACHE_DIR = SPECS_DIR / "cache"
OUT_DIR = ROOT / "static" / "img" / "auckland"

INK = "#1b1b1b"
MUTED = "#6b6b6b"
RULE = "#d8d4cd"
BG = "#faf8f4"
PALETTE = ["#b45b2e", "#2e6f7b", "#7b5ea3", "#5b8a3a", "#c29a1a", "#a14a4a", "#496a8d"]

CANVAS_W = 720
CANVAS_H = 480
PAD_L = 24
PAD_R = 24
PAD_T = 48
PAD_B = 56

PIPELINE_SIGNATURE = 'data-pipeline="render_maps"'


@dataclass
class FeatureService:
    url: str
    layer: int = 0
    where: str = "1=1"
    out_fields: list[str] = field(default_factory=list)
    page_size: int = 2000
    # Server-side geometry simplification in degrees (EPSG:4326).
    # 0.0001 ≈ 11 m, 0.001 ≈ 110 m, 0.002 ≈ 220 m. Huge savings for
    # coastline/parcel layers where raw vertices run to millions.
    max_allowable_offset: float = 0.0


@dataclass
class MapStyle:
    stroke: str = ""
    stroke_width: float = 0.6
    fill: str = "none"
    fill_opacity: float = 0.4
    category_field: str = ""
    # For numeric/coded fields: {code: "Human label"} mapping used in legend.
    category_labels: dict = field(default_factory=dict)


@dataclass
class MapBounds:
    min_lon: float | None = None
    min_lat: float | None = None
    max_lon: float | None = None
    max_lat: float | None = None

    def complete(self) -> bool:
        return None not in (self.min_lon, self.min_lat, self.max_lon, self.max_lat)


@dataclass
class MapSpec:
    id: str
    title: str
    subtitle: str = ""
    fs: FeatureService = field(default_factory=lambda: FeatureService(url=""))
    style: MapStyle = field(default_factory=MapStyle)
    bounds: MapBounds = field(default_factory=MapBounds)
    source_label: str = ""
    source_url: str = ""
    status: str = "placeholder"
    manual: bool = False
    path: Path = field(default_factory=lambda: Path())

    @classmethod
    def load(cls, spec_path: Path) -> "MapSpec":
        raw = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
        fs_raw = raw.get("feature_service") or {}
        style_raw = raw.get("style") or {}
        bounds_raw = raw.get("bounds") or {}
        source = raw.get("source") or {}
        return cls(
            id=raw["id"],
            title=raw["title"],
            subtitle=raw.get("subtitle", ""),
            fs=FeatureService(
                url=fs_raw.get("url", ""),
                layer=int(fs_raw.get("layer", 0)),
                where=fs_raw.get("where", "1=1"),
                out_fields=list(fs_raw.get("out_fields") or []),
                page_size=int(fs_raw.get("page_size", 2000)),
                max_allowable_offset=float(fs_raw.get("max_allowable_offset", 0.0)),
            ),
            style=MapStyle(
                stroke=style_raw.get("stroke", ""),
                stroke_width=float(style_raw.get("stroke_width", 0.6)),
                fill=style_raw.get("fill", "none"),
                fill_opacity=float(style_raw.get("fill_opacity", 0.4)),
                category_field=style_raw.get("category_field", "") or "",
                category_labels=dict(style_raw.get("category_labels") or {}),
            ),
            bounds=MapBounds(
                min_lon=bounds_raw.get("min_lon"),
                min_lat=bounds_raw.get("min_lat"),
                max_lon=bounds_raw.get("max_lon"),
                max_lat=bounds_raw.get("max_lat"),
            ),
            source_label=source.get("label", ""),
            source_url=source.get("url", ""),
            status=raw.get("status", "placeholder"),
            manual=bool(raw.get("manual", False)),
            path=spec_path,
        )


def _fetch_geojson(spec: MapSpec) -> dict[str, Any]:
    """Fetch the full FeatureCollection, paginating until transfer limit clears."""
    base = f"{spec.fs.url.rstrip('/')}/{spec.fs.layer}/query"
    all_features: list[dict[str, Any]] = []
    offset = 0
    out_fields = ",".join(spec.fs.out_fields) if spec.fs.out_fields else "OBJECTID"
    while True:
        params = {
            "where": spec.fs.where,
            "outFields": out_fields,
            "f": "geojson",
            "resultOffset": str(offset),
            "resultRecordCount": str(spec.fs.page_size),
            "returnGeometry": "true",
            "outSR": "4326",
        }
        if spec.fs.max_allowable_offset > 0:
            params["maxAllowableOffset"] = str(spec.fs.max_allowable_offset)
        url = f"{base}?{urllib.parse.urlencode(params)}"
        print(f"[render_maps]   fetching page offset={offset}…", flush=True)
        with urllib.request.urlopen(url, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        features = data.get("features") or []
        all_features.extend(features)
        print(f"[render_maps]   got {len(features)} features (total {len(all_features)})", flush=True)
        exceeded = bool(data.get("properties", {}).get("exceededTransferLimit"))
        if not exceeded or not features:
            break
        offset += len(features)
        if offset > 200_000:
            raise RuntimeError(f"{spec.id}: feature count exceeded 200k, aborting")
    return {"type": "FeatureCollection", "features": all_features}


def _fetch_signature(spec: MapSpec) -> str:
    """A stable string uniquely identifying the fetch parameters.

    Baked into the cache file so a spec URL/query change invalidates the cache
    even if a stale background fetch finishes after the spec was edited.
    """
    parts = [
        spec.fs.url.rstrip("/"),
        str(spec.fs.layer),
        spec.fs.where,
        ",".join(spec.fs.out_fields),
        f"offset={spec.fs.max_allowable_offset}",
    ]
    return "|".join(parts)


def _load_or_fetch(spec: MapSpec, refresh: bool) -> dict[str, Any]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{spec.id}.geojson"
    want_sig = _fetch_signature(spec)
    if cache_path.exists() and not refresh:
        try:
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            cache_sig = cached.get("_pipeline", {}).get("fetch_signature", "")
            if cache_sig == want_sig and cache_path.stat().st_mtime >= spec.path.stat().st_mtime:
                return cached
        except (json.JSONDecodeError, OSError):
            pass  # fall through to fetch
    if not spec.fs.url:
        raise RuntimeError(f"{spec.id}: no cached GeoJSON and no feature_service.url to fetch")
    data = _fetch_geojson(spec)
    data["_pipeline"] = {"fetch_signature": want_sig}
    cache_path.write_text(json.dumps(data), encoding="utf-8")
    return data


def _compute_bounds(features: list[dict[str, Any]]) -> MapBounds:
    min_lon = min_lat = math.inf
    max_lon = max_lat = -math.inf
    for feat in features:
        geom = feat.get("geometry") or {}
        for lon, lat in _iter_coords(geom):
            if lon < min_lon: min_lon = lon
            if lat < min_lat: min_lat = lat
            if lon > max_lon: max_lon = lon
            if lat > max_lat: max_lat = lat
    if math.isinf(min_lon):
        raise RuntimeError("empty geometry — nothing to project")
    return MapBounds(min_lon=min_lon, min_lat=min_lat, max_lon=max_lon, max_lat=max_lat)


def _iter_coords(geom: dict[str, Any]):
    t = geom.get("type")
    coords = geom.get("coordinates")
    if coords is None:
        return
    if t == "Point":
        yield coords[0], coords[1]
    elif t in ("MultiPoint", "LineString"):
        for c in coords:
            yield c[0], c[1]
    elif t in ("MultiLineString", "Polygon"):
        for ring in coords:
            for c in ring:
                yield c[0], c[1]
    elif t == "MultiPolygon":
        for poly in coords:
            for ring in poly:
                for c in ring:
                    yield c[0], c[1]


def _make_projector(bounds: MapBounds):
    """Equirectangular projection with latitude-corrected longitude scaling.

    Returns a function (lon, lat) -> (svg_x, svg_y) that fits the data into
    the plot area while preserving the local aspect ratio.
    """
    inner_w = CANVAS_W - PAD_L - PAD_R
    inner_h = CANVAS_H - PAD_T - PAD_B
    dlon = bounds.max_lon - bounds.min_lon
    dlat = bounds.max_lat - bounds.min_lat
    mid_lat = (bounds.min_lat + bounds.max_lat) / 2
    lon_scale = math.cos(math.radians(mid_lat))
    map_w = dlon * lon_scale
    map_h = dlat
    if map_w / inner_w > map_h / inner_h:
        ppu = inner_w / map_w
    else:
        ppu = inner_h / map_h
    x_px = map_w * ppu
    y_px = map_h * ppu
    x_off = PAD_L + (inner_w - x_px) / 2
    y_off = PAD_T + (inner_h - y_px) / 2

    def project(lon: float, lat: float) -> tuple[float, float]:
        x = x_off + (lon - bounds.min_lon) * lon_scale * ppu
        y = y_off + (bounds.max_lat - lat) * ppu
        return x, y
    return project


def _path_from_geom(geom: dict[str, Any], project) -> str:
    t = geom.get("type")
    coords = geom.get("coordinates") or []
    parts: list[str] = []
    def ring(r):
        pts = [project(lon, lat) for lon, lat in r]
        if not pts:
            return ""
        d = "M" + f"{pts[0][0]:.2f},{pts[0][1]:.2f}"
        for x, y in pts[1:]:
            d += f" L{x:.2f},{y:.2f}"
        return d + " Z"
    def line(r):
        pts = [project(lon, lat) for lon, lat in r]
        if not pts:
            return ""
        d = "M" + f"{pts[0][0]:.2f},{pts[0][1]:.2f}"
        for x, y in pts[1:]:
            d += f" L{x:.2f},{y:.2f}"
        return d

    if t == "Polygon":
        parts.extend(ring(r) for r in coords)
    elif t == "MultiPolygon":
        for poly in coords:
            parts.extend(ring(r) for r in poly)
    elif t == "LineString":
        parts.append(line(coords))
    elif t == "MultiLineString":
        parts.extend(line(r) for r in coords)
    elif t == "Point":
        x, y = project(coords[0], coords[1])
        return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.5" />'
    elif t == "MultiPoint":
        return " ".join(
            f'<circle cx="{project(c[0], c[1])[0]:.2f}" cy="{project(c[0], c[1])[1]:.2f}" r="2.5" />'
            for c in coords
        )
    return " ".join(p for p in parts if p)


def _categorise(features: list[dict[str, Any]], field_name: str) -> tuple[dict[Any, str], list[tuple[Any, str]]]:
    """Map distinct category values to palette colours. Returns (value→colour, legend)."""
    distinct: list[Any] = []
    for feat in features:
        v = (feat.get("properties") or {}).get(field_name)
        if v not in distinct:
            distinct.append(v)
    mapping: dict[Any, str] = {}
    legend: list[tuple[Any, str]] = []
    for i, v in enumerate(distinct):
        colour = PALETTE[i % len(PALETTE)]
        mapping[v] = colour
        legend.append((v, colour))
    return mapping, legend


def _render(spec: MapSpec, geojson: dict[str, Any]) -> str:
    features = geojson.get("features") or []
    if not features:
        raise RuntimeError(f"{spec.id}: GeoJSON has no features")

    bounds = spec.bounds if spec.bounds.complete() else _compute_bounds(features)
    project = _make_projector(bounds)

    style = spec.style
    use_category = bool(style.category_field)
    cat_map: dict[Any, str] = {}
    legend: list[tuple[Any, str]] = []
    if use_category:
        cat_map, legend = _categorise(features, style.category_field)

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
        f'role="img" preserveAspectRatio="xMidYMid meet" {PIPELINE_SIGNATURE}>',
        f'<rect width="100%" height="100%" fill="{BG}"/>',
        '<style>'
        '.title{font:600 16px "Fraunces",Georgia,serif;fill:' + INK + ';}'
        '.subtitle{font:400 11px "Inter",system-ui,sans-serif;fill:' + MUTED + ';}'
        '.stamp{font:500 10px "Inter",system-ui,sans-serif;fill:' + MUTED + ';letter-spacing:.06em;text-transform:uppercase;}'
        '.src{font:400 10px "Inter",system-ui,sans-serif;fill:' + MUTED + ';}'
        '.legend{font:400 11px "Inter",system-ui,sans-serif;fill:' + INK + ';}'
        '</style>',
        f'<text class="title" x="{PAD_L}" y="24">{escape(spec.title)}</text>',
    ]
    if spec.status == "placeholder":
        parts.append(f'<text class="stamp" x="{CANVAS_W - PAD_R}" y="24" text-anchor="end">placeholder</text>')
    if spec.subtitle:
        parts.append(f'<text class="subtitle" x="{PAD_L}" y="40">{escape(spec.subtitle)}</text>')

    default_stroke = style.stroke or PALETTE[0]
    parts.append('<g>')
    for feat in features:
        geom = feat.get("geometry")
        if not geom:
            continue
        props = feat.get("properties") or {}
        colour = cat_map.get(props.get(style.category_field), default_stroke) if use_category else default_stroke
        path_markup = _path_from_geom(geom, project)
        if not path_markup:
            continue
        if path_markup.startswith("<circle"):
            parts.append(path_markup.replace("<circle", f'<circle fill="{colour}"'))
        else:
            parts.append(
                f'<path d="{path_markup}" fill="{style.fill}" fill-opacity="{style.fill_opacity}" '
                f'stroke="{colour}" stroke-width="{style.stroke_width}" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>'
            )
    parts.append('</g>')

    if legend:
        lx = PAD_L
        ly = CANVAS_H - 28
        max_x = CANVAS_W - PAD_R
        for value, colour in legend[:8]:
            raw_label = style.category_labels.get(value) if style.category_labels else None
            if raw_label is None:
                raw_label = str(value) if value is not None else "—"
            label = str(raw_label)
            if len(label) > 22:
                label = label[:20] + "…"
            approx_w = 18 + 7 * len(label) + 18
            if lx + approx_w > max_x:
                break
            parts.append(f'<rect x="{lx}" y="{ly - 8}" width="12" height="12" fill="{colour}"/>')
            parts.append(f'<text class="legend" x="{lx + 18}" y="{ly + 2}">{escape(label)}</text>')
            lx += approx_w

    if spec.source_label:
        parts.append(
            f'<text class="src" x="{PAD_L}" y="{CANVAS_H - 10}">Source: {escape(spec.source_label)}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def _is_manual_override(spec: MapSpec, out_path: Path) -> bool:
    if not out_path.exists():
        return False
    content = out_path.read_text(encoding="utf-8", errors="replace")
    if PIPELINE_SIGNATURE in content:
        return False
    out_mtime = out_path.stat().st_mtime
    inputs = [spec.path, Path(__file__)]
    return all(p.stat().st_mtime <= out_mtime for p in inputs if p.exists())


def _needs_render(spec: MapSpec, out_path: Path) -> bool:
    if not out_path.exists():
        return True
    out_mtime = out_path.stat().st_mtime
    inputs = [spec.path, Path(__file__)]
    cache_path = CACHE_DIR / f"{spec.id}.geojson"
    if cache_path.exists():
        inputs.append(cache_path)
    return any(p.stat().st_mtime > out_mtime for p in inputs if p.exists())


def render_one(spec: MapSpec, refresh: bool) -> tuple[bool, str]:
    out_path = OUT_DIR / f"{spec.id}.svg"
    if spec.manual:
        return False, "manual: true (leaving hand-produced SVG alone)"
    if _is_manual_override(spec, out_path):
        return False, "hand-produced SVG newer than inputs (not overwriting)"
    try:
        data = _load_or_fetch(spec, refresh=refresh)
    except Exception as exc:
        return False, f"fetch/cache failed: {exc}"
    if not _needs_render(spec, out_path) and not refresh:
        return False, "up to date"
    try:
        svg = _render(spec, data)
    except Exception as exc:
        return False, f"render failed: {exc}"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    return True, f"wrote {out_path.relative_to(ROOT)}"


def main(argv: list[str]) -> int:
    refresh = "--refresh" in argv
    if not SPECS_DIR.exists():
        print(f"[render_maps] no spec directory at {SPECS_DIR.relative_to(ROOT)}; nothing to do.")
        return 0
    specs = sorted(SPECS_DIR.glob("*.yaml")) + sorted(SPECS_DIR.glob("*.yml"))
    if not specs:
        print(f"[render_maps] no YAML specs in {SPECS_DIR.relative_to(ROOT)}; nothing to do.")
        return 0
    errors: list[str] = []
    wrote = 0
    for spec_path in specs:
        try:
            spec = MapSpec.load(spec_path)
        except Exception as exc:
            errors.append(f"{spec_path.name}: load failed — {exc}")
            continue
        ok, msg = render_one(spec, refresh=refresh)
        label = spec_path.relative_to(ROOT)
        if ok:
            wrote += 1
            print(f"[render_maps] {label}: {msg}")
        elif msg.startswith("up to date") or msg.startswith("manual") or "not overwriting" in msg:
            print(f"[render_maps] {label}: {msg}")
        else:
            errors.append(f"{label}: {msg}")
    if errors:
        print(f"[render_maps] FAIL — {len(errors)} issue(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print(f"[render_maps] OK — {wrote} rendered, {len(specs) - wrote} unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
