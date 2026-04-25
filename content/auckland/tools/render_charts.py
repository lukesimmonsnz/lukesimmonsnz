"""Render Auckland chart specs to SVG.

Reads YAML specs from ``content/auckland/data/charts/*.yaml`` plus CSVs from
``content/auckland/data/series/*.csv`` and writes styled SVGs to
``static/img/auckland/<id>.svg``.

Pure-Python — no matplotlib / plotly / altair. PyYAML is the only dep.
Styling is deliberately minimal and matches the site CSS (warm accent,
muted rules, site typography inherited via CSS).

Idempotent: skips a spec if the output SVG is newer than both the spec
YAML and the referenced CSV. Exit codes: 0 ok / 1 errors encountered.

Spec shape (v1)::

    id: supply-annual-consents
    title: Annual dwelling consents issued, Auckland region
    type: line | bar | area-stacked | dual-axis | placeholder
    data: series/auckland-annual-consents.csv    # omit for `placeholder`
    x: year                                      # omit for `placeholder`
    y:                                           # omit for `placeholder`
      - column: consents
        label: Consents
    y_label: Count
    source:
      label: Stats NZ — Building consents by territorial authority
      url: https://www.stats.govt.nz/...
    status: placeholder | verified               # drives the stamp in the corner
    note: "To be produced from ..."              # only used by the `placeholder` type

    # Optional: declare an upstream fetcher. When present, and the data file
    # is missing or the fetcher signature changed, the renderer invokes the
    # named fetcher and writes its output to the `data:` path before rendering.
    # Fetchers live at tools/fetchers/<module>.py and expose fetch(params) -> bytes.
    fetcher:
      name: oecd.productivity_by_industry
      params:
        country: NZL
        industries: [CONSTR, MANUF, SERV]
"""
from __future__ import annotations

import csv
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence
from xml.sax.saxutils import escape

import yaml

ROOT = Path(__file__).resolve().parents[3]  # repo root (Current website/)
SPECS_DIR = ROOT / "content" / "auckland" / "data" / "charts"
SERIES_DIR = ROOT / "content" / "auckland" / "data" / "series"
OUT_DIR = ROOT / "static" / "img" / "auckland"

# Palette pulled from static/css/main.css so charts sit in the site visually.
INK = "#1b1b1b"
MUTED = "#6b6b6b"
RULE = "#d8d4cd"
BG = "#faf8f4"
SERIES_COLORS = ["#b45b2e", "#2e6f7b", "#7b5ea3", "#5b8a3a", "#c29a1a"]

CANVAS_W = 720
CANVAS_H = 360
PAD_L = 64
PAD_R = 24
PAD_T = 48
PAD_B = 56

# Embedded in every SVG we generate so the escape-hatch can distinguish our
# output from a hand-produced SVG dropped into static/img/auckland/.
# MUST be valid XML — attribute value has to be quoted.
PIPELINE_SIGNATURE = 'data-pipeline="render_charts"'


@dataclass
class YSeries:
    column: str
    label: str


@dataclass
class Fetcher:
    """Declaration of an upstream data fetcher to run before rendering."""
    name: str = ""                  # e.g. "oecd.productivity_by_industry"
    params: dict = field(default_factory=dict)


@dataclass
class Spec:
    id: str
    title: str
    type: str
    data: str = ""
    x: str = ""
    y: list[YSeries] = field(default_factory=list)
    y_label: str = ""
    subtitle: str = ""
    source_label: str = ""
    source_url: str = ""
    status: str = "placeholder"
    note: str = ""
    manual: bool = False
    fetcher: Fetcher = field(default_factory=Fetcher)
    path: Path = field(default_factory=lambda: Path())

    @classmethod
    def load(cls, spec_path: Path) -> "Spec":
        raw = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
        y_raw = raw.get("y") or []
        y = [YSeries(column=item["column"], label=item.get("label", item["column"])) for item in y_raw]
        source = raw.get("source") or {}
        fetcher_raw = raw.get("fetcher") or {}
        return cls(
            id=raw["id"],
            title=raw["title"],
            type=raw.get("type", "line"),
            data=raw.get("data", ""),
            x=raw.get("x", ""),
            y=y,
            y_label=raw.get("y_label", ""),
            subtitle=raw.get("subtitle", ""),
            source_label=source.get("label", ""),
            source_url=source.get("url", ""),
            status=raw.get("status", "placeholder"),
            note=raw.get("note", ""),
            manual=bool(raw.get("manual", False)),
            fetcher=Fetcher(
                name=fetcher_raw.get("name", ""),
                params=dict(fetcher_raw.get("params") or {}),
            ),
            path=spec_path,
        )

    @property
    def data_path(self) -> Path:
        # data paths are relative to content/auckland/data/
        if not self.data:
            return Path()
        return (SPECS_DIR.parent / self.data).resolve()


def _read_csv(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        lines = [ln for ln in f if ln.strip() and not ln.lstrip().startswith("#")]
    reader = csv.DictReader(lines)
    return [r for r in reader if r and any((v or "").strip() for v in r.values())]


def _to_number(value: str) -> float:
    return float(value.replace(",", "").strip())


def _nice_ticks(lo: float, hi: float, n: int = 5) -> list[float]:
    if hi <= lo:
        return [lo]
    raw = (hi - lo) / n
    mag = 10 ** (len(str(int(raw))) - 1) if raw >= 1 else 10 ** -1
    step = max(1.0, round(raw / mag) * mag)
    start = step * (lo // step)
    ticks: list[float] = []
    v = start
    while v <= hi + step / 2:
        if v >= lo - step / 2:
            ticks.append(v)
        v += step
    return ticks


def _fmt(value: float) -> str:
    if value == int(value):
        iv = int(value)
        # Years look wrong with a thousands separator.
        if 1000 <= abs(iv) <= 9999:
            return str(iv)
        if abs(iv) >= 1000:
            return f"{iv:,}"
        return str(iv)
    return f"{value:.1f}"


def _svg_open() -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
        f'role="img" preserveAspectRatio="xMidYMid meet" {PIPELINE_SIGNATURE}>',
        f'<rect width="100%" height="100%" fill="{BG}"/>',
        '<style>'
        '.title{font:600 16px "Fraunces",Georgia,serif;fill:' + INK + ';}'
        '.subtitle{font:400 11px "Inter",system-ui,sans-serif;fill:' + MUTED + ';}'
        '.axis{font:400 11px "Inter",system-ui,sans-serif;fill:' + MUTED + ';}'
        '.axis-label{font:500 11px "Inter",system-ui,sans-serif;fill:' + INK + ';}'
        '.stamp{font:500 10px "Inter",system-ui,sans-serif;fill:' + MUTED + ';letter-spacing:.06em;text-transform:uppercase;}'
        '.src{font:400 10px "Inter",system-ui,sans-serif;fill:' + MUTED + ';}'
        '.legend{font:400 11px "Inter",system-ui,sans-serif;fill:' + INK + ';}'
        '</style>',
    ]


def _header(parts: list[str], spec: Spec) -> None:
    parts.append(f'<text class="title" x="{PAD_L}" y="24">{escape(spec.title)}</text>')
    if spec.status == "placeholder":
        parts.append(
            f'<text class="stamp" x="{CANVAS_W - PAD_R}" y="24" text-anchor="end">placeholder data</text>'
        )
    if spec.subtitle:
        parts.append(f'<text class="subtitle" x="{PAD_L}" y="40">{escape(spec.subtitle)}</text>')


def _footer(parts: list[str], spec: Spec) -> None:
    if spec.source_label:
        parts.append(
            f'<text class="src" x="{PAD_L}" y="{CANVAS_H - 10}">Source: {escape(spec.source_label)}</text>'
        )


def _plot_area() -> tuple[int, int, int, int]:
    return PAD_L, PAD_T, CANVAS_W - PAD_R, CANVAS_H - PAD_B


def _render_line(spec: Spec, rows: list[dict[str, str]]) -> str:
    xs = [_to_number(r[spec.x]) for r in rows]
    x_lo, x_hi = min(xs), max(xs)
    all_y: list[float] = []
    series_data: list[list[tuple[float, float]]] = []
    for s in spec.y:
        pts = [(xs[i], _to_number(rows[i][s.column])) for i in range(len(rows))]
        series_data.append(pts)
        all_y.extend(v for _, v in pts)
    y_lo = min(0.0, min(all_y))
    y_hi = max(all_y)
    x0, y0, x1, y1 = _plot_area()

    def sx(v: float) -> float:
        return x0 + (v - x_lo) / (x_hi - x_lo) * (x1 - x0) if x_hi != x_lo else x0
    def sy(v: float) -> float:
        return y1 - (v - y_lo) / (y_hi - y_lo) * (y1 - y0) if y_hi != y_lo else y1

    parts = _svg_open()
    _header(parts, spec)

    y_ticks = _nice_ticks(y_lo, y_hi)
    for t in y_ticks:
        y = sy(t)
        parts.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        parts.append(f'<text class="axis" x="{x0 - 8}" y="{y + 4:.1f}" text-anchor="end">{_fmt(t)}</text>')

    x_ticks = _x_ticks(xs)
    for t in x_ticks:
        x = sx(t)
        parts.append(f'<text class="axis" x="{x:.1f}" y="{y1 + 18}" text-anchor="middle">{_fmt(t)}</text>')

    parts.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{INK}" stroke-width="1"/>')

    for idx, pts in enumerate(series_data):
        colour = SERIES_COLORS[idx % len(SERIES_COLORS)]
        d = " ".join(
            ("M" if i == 0 else "L") + f"{sx(x):.1f},{sy(y):.1f}" for i, (x, y) in enumerate(pts)
        )
        parts.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="2" stroke-linejoin="round"/>')

    _legend(parts, spec.y)
    _footer(parts, spec)
    parts.append("</svg>")
    return "\n".join(parts)


def _x_ticks(xs: Sequence[float]) -> list[float]:
    x_lo, x_hi = min(xs), max(xs)
    span = x_hi - x_lo
    if span <= 10:
        step = 1
    elif span <= 30:
        step = 5
    elif span <= 60:
        step = 10
    else:
        step = 20
    ticks: list[float] = []
    v = int(x_lo)
    while v <= x_hi:
        ticks.append(float(v))
        v += step
    if ticks[-1] != x_hi:
        ticks.append(float(x_hi))
    return ticks


def _render_bar(spec: Spec, rows: list[dict[str, str]]) -> str:
    labels = [r[spec.x] for r in rows]
    col = spec.y[0].column
    values = [_to_number(r[col]) for r in rows]
    y_lo = min(0.0, min(values))
    y_hi = max(values)
    x0, y0, x1, y1 = _plot_area()
    n = len(values)
    slot = (x1 - x0) / n if n else 1
    bar_w = slot * 0.65

    def sy(v: float) -> float:
        return y1 - (v - y_lo) / (y_hi - y_lo) * (y1 - y0) if y_hi != y_lo else y1

    parts = _svg_open()
    _header(parts, spec)

    y_ticks = _nice_ticks(y_lo, y_hi)
    for t in y_ticks:
        y = sy(t)
        parts.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        parts.append(f'<text class="axis" x="{x0 - 8}" y="{y + 4:.1f}" text-anchor="end">{_fmt(t)}</text>')

    baseline = sy(0.0)
    parts.append(f'<line x1="{x0}" y1="{baseline:.1f}" x2="{x1}" y2="{baseline:.1f}" stroke="{INK}" stroke-width="1"/>')

    colour = SERIES_COLORS[0]
    for i, v in enumerate(values):
        cx = x0 + slot * (i + 0.5)
        top = sy(v)
        h = max(1.0, baseline - top)
        parts.append(
            f'<rect x="{cx - bar_w / 2:.1f}" y="{top:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{colour}"/>'
        )
        parts.append(
            f'<text class="axis" x="{cx:.1f}" y="{y1 + 18}" text-anchor="middle">{escape(labels[i])}</text>'
        )

    _footer(parts, spec)
    parts.append("</svg>")
    return "\n".join(parts)


def _render_area_stacked(spec: Spec, rows: list[dict[str, str]]) -> str:
    xs = [_to_number(r[spec.x]) for r in rows]
    x_lo, x_hi = min(xs), max(xs)
    n = len(rows)
    series_values = [[_to_number(r[s.column]) for r in rows] for s in spec.y]
    stacks: list[list[float]] = [[0.0] * n for _ in spec.y]
    for i in range(n):
        running = 0.0
        for s_idx, values in enumerate(series_values):
            running += values[i]
            stacks[s_idx][i] = running
    y_lo = 0.0
    y_hi = max(max(stack) for stack in stacks) if stacks else 1.0
    x0, y0, x1, y1 = _plot_area()

    def sx(v: float) -> float:
        return x0 + (v - x_lo) / (x_hi - x_lo) * (x1 - x0) if x_hi != x_lo else x0
    def sy(v: float) -> float:
        return y1 - (v - y_lo) / (y_hi - y_lo) * (y1 - y0) if y_hi != y_lo else y1

    parts = _svg_open()
    _header(parts, spec)

    for t in _nice_ticks(y_lo, y_hi):
        y = sy(t)
        parts.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        parts.append(f'<text class="axis" x="{x0 - 8}" y="{y + 4:.1f}" text-anchor="end">{_fmt(t)}</text>')
    for t in _x_ticks(xs):
        x = sx(t)
        parts.append(f'<text class="axis" x="{x:.1f}" y="{y1 + 18}" text-anchor="middle">{_fmt(t)}</text>')
    parts.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{INK}" stroke-width="1"/>')

    # Draw from topmost stack down so earlier-drawn areas aren't hidden.
    for s_idx in reversed(range(len(spec.y))):
        top = stacks[s_idx]
        bottom = stacks[s_idx - 1] if s_idx > 0 else [0.0] * n
        coords: list[str] = []
        for i in range(n):
            coords.append(f"{sx(xs[i]):.1f},{sy(top[i]):.1f}")
        for i in reversed(range(n)):
            coords.append(f"{sx(xs[i]):.1f},{sy(bottom[i]):.1f}")
        colour = SERIES_COLORS[s_idx % len(SERIES_COLORS)]
        parts.append(f'<polygon points="{" ".join(coords)}" fill="{colour}" fill-opacity="0.85"/>')

    _legend(parts, spec.y)
    _footer(parts, spec)
    parts.append("</svg>")
    return "\n".join(parts)


def _render_dual_axis(spec: Spec, rows: list[dict[str, str]]) -> str:
    if len(spec.y) != 2:
        raise ValueError("dual-axis chart needs exactly two y series")
    xs = [_to_number(r[spec.x]) for r in rows]
    x_lo, x_hi = min(xs), max(xs)
    left_vals = [_to_number(r[spec.y[0].column]) for r in rows]
    right_vals = [_to_number(r[spec.y[1].column]) for r in rows]
    l_lo, l_hi = min(0.0, min(left_vals)), max(left_vals)
    r_lo, r_hi = min(0.0, min(right_vals)), max(right_vals)
    x0, y0, x1, y1 = _plot_area()

    def sx(v: float) -> float:
        return x0 + (v - x_lo) / (x_hi - x_lo) * (x1 - x0) if x_hi != x_lo else x0
    def sy_l(v: float) -> float:
        return y1 - (v - l_lo) / (l_hi - l_lo) * (y1 - y0) if l_hi != l_lo else y1
    def sy_r(v: float) -> float:
        return y1 - (v - r_lo) / (r_hi - r_lo) * (y1 - y0) if r_hi != r_lo else y1

    parts = _svg_open()
    _header(parts, spec)

    for t in _nice_ticks(l_lo, l_hi):
        y = sy_l(t)
        parts.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        parts.append(f'<text class="axis" x="{x0 - 8}" y="{y + 4:.1f}" text-anchor="end" fill="{SERIES_COLORS[0]}">{_fmt(t)}</text>')
    for t in _nice_ticks(r_lo, r_hi):
        y = sy_r(t)
        parts.append(f'<text class="axis" x="{x1 + 8}" y="{y + 4:.1f}" text-anchor="start" fill="{SERIES_COLORS[1]}">{_fmt(t)}</text>')
    for t in _x_ticks(xs):
        parts.append(f'<text class="axis" x="{sx(t):.1f}" y="{y1 + 18}" text-anchor="middle">{_fmt(t)}</text>')
    parts.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{INK}" stroke-width="1"/>')

    for idx, (values, sy_fn) in enumerate([(left_vals, sy_l), (right_vals, sy_r)]):
        colour = SERIES_COLORS[idx]
        d = " ".join(
            ("M" if i == 0 else "L") + f"{sx(xs[i]):.1f},{sy_fn(values[i]):.1f}" for i in range(len(rows))
        )
        parts.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="2" stroke-linejoin="round"/>')

    _legend(parts, spec.y)
    _footer(parts, spec)
    parts.append("</svg>")
    return "\n".join(parts)


def _render_placeholder(spec: Spec, _rows: list[dict[str, str]] | None = None) -> str:
    """A styled 'figure to come' card for maps or any figure without data yet."""
    parts = _svg_open()
    _header(parts, spec)
    x0, y0, x1, y1 = _plot_area()
    parts.append(
        f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
        f'fill="none" stroke="{RULE}" stroke-width="1.5" stroke-dasharray="6 6"/>'
    )
    note = spec.note or "Figure to be produced from the source listed below."
    parts.append(
        f'<text class="axis-label" x="{(x0 + x1) / 2:.0f}" y="{(y0 + y1) / 2 - 4:.0f}" '
        f'text-anchor="middle">Figure placeholder</text>'
    )
    # Wrap note text into up to three lines at ~70 chars.
    lines = _wrap(note, 72)[:3]
    for i, line in enumerate(lines):
        parts.append(
            f'<text class="axis" x="{(x0 + x1) / 2:.0f}" y="{(y0 + y1) / 2 + 16 + i * 16:.0f}" '
            f'text-anchor="middle">{escape(line)}</text>'
        )
    _footer(parts, spec)
    parts.append("</svg>")
    return "\n".join(parts)


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for w in words:
        if not current:
            current = w
        elif len(current) + 1 + len(w) <= width:
            current += " " + w
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def _legend(parts: list[str], series: list[YSeries]) -> None:
    if len(series) <= 1:
        return
    lx = PAD_L
    ly = CANVAS_H - 28
    for idx, s in enumerate(series):
        colour = SERIES_COLORS[idx % len(SERIES_COLORS)]
        parts.append(f'<rect x="{lx}" y="{ly - 8}" width="12" height="12" fill="{colour}"/>')
        parts.append(f'<text class="legend" x="{lx + 18}" y="{ly + 2}">{escape(s.label)}</text>')
        lx += 18 + 7 * len(s.label) + 20


RENDERERS = {
    "line": _render_line,
    "bar": _render_bar,
    "area-stacked": _render_area_stacked,
    "dual-axis": _render_dual_axis,
    "placeholder": _render_placeholder,
}


def _needs_render(spec: Spec) -> bool:
    out_path = OUT_DIR / f"{spec.id}.svg"
    if not out_path.exists():
        return True
    out_mtime = out_path.stat().st_mtime
    inputs = [spec.path, Path(__file__)]
    if spec.data_path and spec.data_path != Path():
        inputs.append(spec.data_path)
    return any(p.stat().st_mtime > out_mtime for p in inputs if p.exists())


_FETCHERS_DIR = Path(__file__).resolve().parent / "fetchers"


def _run_fetcher(spec: Spec) -> None:
    """Invoke the fetcher declared on the spec, writing its bytes to spec.data."""
    import importlib
    import sys as _sys
    module_name, _, func_name = spec.fetcher.name.rpartition(".")
    if not module_name or not func_name:
        raise RuntimeError(f"invalid fetcher name: {spec.fetcher.name!r} (expected 'module.function')")
    if str(_FETCHERS_DIR) not in _sys.path:
        _sys.path.insert(0, str(_FETCHERS_DIR))
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise RuntimeError(f"cannot import fetcher module {module_name!r}: {exc}")
    func = getattr(module, func_name, None)
    if func is None:
        raise RuntimeError(f"fetcher {func_name!r} not found in {module_name}")
    print(f"[render_charts]   running fetcher {spec.fetcher.name}…", flush=True)
    data = func(spec.fetcher.params)
    if not isinstance(data, (bytes, bytearray)):
        raise RuntimeError(f"fetcher {spec.fetcher.name} returned {type(data).__name__}, expected bytes")
    spec.data_path.parent.mkdir(parents=True, exist_ok=True)
    spec.data_path.write_bytes(bytes(data))
    print(f"[render_charts]   wrote {spec.data_path.relative_to(ROOT)} ({len(data):,} bytes)", flush=True)


def render_one(spec: Spec) -> tuple[bool, str]:
    """Render a single spec. Returns (wrote_output, message)."""
    out_path = OUT_DIR / f"{spec.id}.svg"
    if spec.manual:
        return False, "manual: true (leaving hand-produced SVG alone)"
    renderer = RENDERERS.get(spec.type)
    if renderer is None:
        return False, f"unsupported chart type: {spec.type}"
    needs_data = spec.type != "placeholder"
    if needs_data and spec.fetcher.name and not spec.data_path.exists():
        try:
            _run_fetcher(spec)
        except Exception as exc:
            return False, f"fetcher {spec.fetcher.name!r} failed: {exc}"
    if needs_data and not spec.data_path.exists():
        return False, f"missing data file: {spec.data}"
    # mtime-based escape hatch: if the output SVG is newer than every input
    # (spec, CSV, renderer code), something — probably a hand-produced export
    # — is newer than the pipeline would produce. Leave it alone.
    if _is_manual_override(spec, out_path):
        return False, "hand-produced SVG newer than inputs (not overwriting)"
    if not _needs_render(spec):
        return False, "up to date"
    rows = _read_csv(spec.data_path) if needs_data else []
    svg = renderer(spec, rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    return True, f"wrote {out_path.relative_to(ROOT)}"


def _is_manual_override(spec: Spec, out_path: Path) -> bool:
    """The existing SVG is newer than every input, and is not one we produced.

    We distinguish our own output from a hand-produced one by looking for the
    ``data-pipeline-signature`` marker we embed. Anything without it is treated
    as manually maintained.
    """
    if not out_path.exists():
        return False
    content = out_path.read_text(encoding="utf-8", errors="replace")
    if PIPELINE_SIGNATURE in content:
        return False
    out_mtime = out_path.stat().st_mtime
    inputs = [spec.path, Path(__file__)]
    if spec.data_path and spec.data_path != Path():
        inputs.append(spec.data_path)
    return all(p.stat().st_mtime <= out_mtime for p in inputs if p.exists())


def main() -> int:
    if not SPECS_DIR.exists():
        print(f"[render_charts] no spec directory at {SPECS_DIR.relative_to(ROOT)}; nothing to do.")
        return 0
    specs = sorted(SPECS_DIR.glob("*.yaml")) + sorted(SPECS_DIR.glob("*.yml"))
    if not specs:
        print(f"[render_charts] no YAML specs in {SPECS_DIR.relative_to(ROOT)}; nothing to do.")
        return 0

    errors: list[str] = []
    wrote = 0
    for spec_path in specs:
        try:
            spec = Spec.load(spec_path)
        except Exception as exc:
            errors.append(f"{spec_path.name}: load failed — {exc}")
            continue
        ok, msg = render_one(spec)
        label = spec_path.relative_to(ROOT)
        if ok:
            wrote += 1
            print(f"[render_charts] {label}: {msg}")
        elif msg == "up to date":
            print(f"[render_charts] {label}: up to date")
        else:
            errors.append(f"{label}: {msg}")

    if errors:
        print(f"[render_charts] FAIL — {len(errors)} issue(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print(f"[render_charts] OK — {wrote} rendered, {len(specs) - wrote} unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
