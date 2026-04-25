"""OECD SDMX fetcher.

Pulls CSV data from the OECD's SDMX REST API:
https://sdmx.oecd.org/public/rest/data/

No auth, no key. Free of charge subject to OECD terms of use. Returns bytes
containing a CSV ready to be consumed by the chart renderer.

Exposed functions (each takes a params dict and returns bytes):

- ``productivity_by_industry(params)`` — labour productivity index (GVAHRS)
  for one country, one or more ISIC rev 4 industry codes, rebased to the
  renderer's choice of year. Returns a wide CSV: ``year,industry_a,industry_b,…``.
"""
from __future__ import annotations

import csv
import io
import urllib.parse
import urllib.request

SDMX_BASE = "https://sdmx.oecd.org/public/rest/data"


def _get_text(url: str, timeout: int = 60) -> str:
    # OECD's SDMX endpoint rejects requests without a User-Agent (returns 403).
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "text/csv",
            "User-Agent": "lukesimmonsnz.kiwi auckland-pipeline (+https://lukesimmonsnz.kiwi/)",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def productivity_by_industry(params: dict) -> bytes:
    """Fetch OECD productivity-by-industry (DSD_PDB@DF_PDB_ISIC4_I4) as wide CSV.

    Parameters (YAML spec ``fetcher.params``):

    - ``country``: ISO-3 country code (default ``NZL``).
    - ``industries``: list of {code, label} dicts. ``code`` is an ISIC rev 4
      letter or group (``F``, ``C``, ``GTI``); ``label`` is the CSV column name
      the spec's ``y[].column`` uses. Example::

          industries:
            - {code: F,   label: construction}
            - {code: C,   label: manufacturing}
            - {code: GTI, label: services}

    - ``start_year``: integer, default ``2000``.
    - ``rebase_year``: integer, default ``2000``. Each series is rebased so
      this year's value = 100. OECD's native base is 2015; rebasing lets the
      chart tell the same story the spec expected.
    """
    country = params.get("country", "NZL")
    industries = list(params.get("industries") or [])
    if not industries:
        raise RuntimeError("oecd.productivity_by_industry: no industries given in params")
    start_year = int(params.get("start_year", 2000))
    rebase_year = int(params.get("rebase_year", 2000))

    codes = "+".join(item["code"] for item in industries)
    key = f"{country}.A.GVAHRS.{codes}.IX.Q._Z._Z._Z"
    query = urllib.parse.urlencode({
        "startPeriod": str(start_year),
        "format": "csvfilewithlabels",
        "dimensionAtObservation": "AllDimensions",
    })
    url = f"{SDMX_BASE}/OECD.SDD.TPS,DSD_PDB@DF_PDB_ISIC4_I4,1.0/{key}?{query}"
    body = _get_text(url)

    # OECD returns long-form CSV; pivot to wide {year: {activity_code: value}}.
    reader = csv.DictReader(io.StringIO(body))
    by_year_activity: dict[int, dict[str, float]] = {}
    for row in reader:
        try:
            year = int(row["TIME_PERIOD"])
            value = float(row["OBS_VALUE"])
        except (ValueError, KeyError):
            continue
        code = row.get("ACTIVITY", "")
        by_year_activity.setdefault(year, {})[code] = value

    # Rebase each series so rebase_year = 100.
    code_to_label = {item["code"]: item["label"] for item in industries}
    bases: dict[str, float] = {}
    for code in code_to_label:
        base = by_year_activity.get(rebase_year, {}).get(code)
        if base is None or base == 0:
            raise RuntimeError(
                f"oecd.productivity_by_industry: no {code} value for rebase year {rebase_year}"
            )
        bases[code] = base

    # Emit wide CSV: year, label_1, label_2, …
    out = io.StringIO()
    out.write(f"# Fetched from OECD SDMX: {url}\n")
    out.write(
        f"# Dataflow: DSD_PDB@DF_PDB_ISIC4_I4 (productivity by industry, ISIC rev 4)\n"
    )
    out.write(f"# Rebased so {rebase_year} = 100 across all series.\n")
    writer = csv.writer(out, lineterminator="\n")
    labels = [item["label"] for item in industries]
    writer.writerow(["year", *labels])
    for year in sorted(by_year_activity):
        row = [year]
        for item in industries:
            value = by_year_activity[year].get(item["code"])
            if value is None:
                row.append("")
            else:
                row.append(f"{value * 100 / bases[item['code']]:.2f}")
        writer.writerow(row)
    return out.getvalue().encode("utf-8")
