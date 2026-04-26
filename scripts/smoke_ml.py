"""
scripts/smoke_ml.py — Layer 0.5b integration smoke test
=========================================================
Hits all three endpoints of the ML daemon and asserts structural
correctness.  Exit 0 on pass, exit 1 on failure.

Usage (daemon must be running):
    .venv-ml/Scripts/python scripts/smoke_ml.py

Requires only `requests` — importable from either venv.
No torch dependency here.
"""

from __future__ import annotations

import math
import sys
from typing import Any

try:
    import requests
except ImportError:
    print("[smoke] ERROR: 'requests' not found. pip install requests", file=sys.stderr)
    sys.exit(1)

BASE_URL = "http://127.0.0.1:5001"
TIMEOUT  = 30   # first call may be slow if warm-up is still running

_failures: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  [PASS] {name}")
    else:
        msg = f"  [FAIL] {name}" + (f" — {detail}" if detail else "")
        print(msg, file=sys.stderr)
        _failures.append(msg)


def post(path: str, payload: dict[str, Any]) -> requests.Response:
    r = requests.post(f"{BASE_URL}{path}", json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    return r


def get(path: str) -> requests.Response:
    r = requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT)
    r.raise_for_status()
    return r


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

def test_health() -> None:
    print("\n── GET / ──")
    r = get("/")
    b = r.json()
    check("status_200",          r.status_code == 200)
    check("status_ok",           b.get("status") == "ok",
          f"got {b.get('status')!r}")
    check("cuda_present",        "cuda" in b)
    check("models_loaded",       b.get("models_loaded") is True,
          "models not yet loaded — retry after warm-up completes")
    print(f"     cuda={b.get('cuda')}  device={b.get('device')!r}")


# ---------------------------------------------------------------------------
# POST /embed
# ---------------------------------------------------------------------------

EMBED_TEXTS = [
    "The court ruled in favour of the defendant.",
    "Neural networks can approximate arbitrary functions.",
    "Kia ora — a greeting in te reo Māori.",
]

def test_embed() -> None:
    print("\n── POST /embed ──")
    r = post("/embed", {"texts": EMBED_TEXTS})
    b = r.json()
    check("status_200",          r.status_code == 200)
    check("field_embeddings",    "embeddings" in b)
    check("field_dim",           "dim" in b)
    check("field_model",         "model" in b)

    vecs = b.get("embeddings", [])
    dim  = b.get("dim", 0)
    check("count_matches_input", len(vecs) == len(EMBED_TEXTS),
          f"expected {len(EMBED_TEXTS)}, got {len(vecs)}")
    check("dim_is_384",          dim == 384,
          f"MiniLM-L6-v2 should be 384-dim, got {dim}")
    check("vec_length_matches",  all(len(v) == dim for v in vecs))
    check("values_are_floats",   all(isinstance(x, float)
                                     for v in vecs for x in v[:4]))

    norms = [math.sqrt(sum(x**2 for x in v)) for v in vecs]
    check("unit_normalised",     all(abs(n - 1.0) < 0.01 for n in norms),
          f"norms={[round(n,4) for n in norms]} — check normalize_embeddings flag")
    print(f"     dim={dim}  n_vecs={len(vecs)}  norm[0]={round(norms[0],5)}")


# ---------------------------------------------------------------------------
# POST /nli
# ---------------------------------------------------------------------------

# §5c pipeline: verifier checks claim against retrieved source passage.
NLI_ENTAIL = {
    "source": "The Auckland High Court dismissed all charges against the defendant on Tuesday.",
    "claim":  "The defendant was not convicted.",
}
NLI_CONTRA = {
    "source": "The company reported record profits of $4.2 billion for the fiscal year.",
    "claim":  "The company suffered a financial loss this year.",
}
VALID_LABELS = {"entailment", "neutral", "contradiction"}

def test_nli() -> None:
    print("\n── POST /nli (entailment pair) ──")
    r = post("/nli", NLI_ENTAIL)
    b = r.json()
    check("status_200",          r.status_code == 200)
    check("field_label",         "label" in b)
    check("field_score",         "score" in b)
    check("field_all_scores",    "all_scores" in b)
    check("field_model",         "model" in b)

    label = b.get("label", "")
    score = b.get("score", 0.0)
    all_s = b.get("all_scores", {})

    check("label_valid",         label in VALID_LABELS, f"got {label!r}")
    check("score_in_range",      0.0 <= score <= 1.0)
    check("all_scores_keys",     set(all_s.keys()) == VALID_LABELS,
          f"got {set(all_s.keys())}")
    check("all_scores_sum_1",    abs(sum(all_s.values()) - 1.0) < 0.01,
          f"sum={sum(all_s.values()):.4f}")

    if label == "entailment":
        print(f"     [INFO] entailment pair → label={label!r}  score={score:.4f}  ✓")
    else:
        print(f"     [WARN] entailment pair → label={label!r}  score={score:.4f} "
              f"(expected 'entailment' — verify _NLI_LABELS order in ml_daemon.py)",
              file=sys.stderr)

    print("\n── POST /nli (contradiction pair) ──")
    r2 = post("/nli", NLI_CONTRA)
    b2 = r2.json()
    label2 = b2.get("label", "")
    score2 = b2.get("score", 0.0)
    check("status_200_contra",   r2.status_code == 200)
    check("label_valid_contra",  label2 in VALID_LABELS)

    if label2 == "contradiction":
        print(f"     [INFO] contradiction pair → label={label2!r}  score={score2:.4f}  ✓")
    else:
        print(f"     [WARN] contradiction pair → label={label2!r}  score={score2:.4f} "
              f"(expected 'contradiction')",
              file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"smoke_ml.py  →  {BASE_URL}")
    print("=" * 50)
    try:
        test_health()
        test_embed()
        test_nli()
    except requests.exceptions.ConnectionError:
        print(f"\n[smoke] FATAL: cannot connect to {BASE_URL}\n"
              "  Make sure start-ml.bat is running and warm-up has completed.",
              file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as exc:
        print(f"\n[smoke] FATAL: HTTP error — {exc}", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 50)
    if _failures:
        print(f"RESULT: {len(_failures)} assertion(s) FAILED", file=sys.stderr)
        sys.exit(1)
    else:
        print("RESULT: all checks passed — Layer 0.5b daemon is healthy")
        sys.exit(0)


if __name__ == "__main__":
    main()
