"""Tiny .env loader for the agent and scripts/.

Reads ``KEY=value`` lines from the project root's ``.env`` (gitignored)
and merges them into ``os.environ`` without overwriting variables that
are already set in the real environment. Real env vars win.

Lines starting with ``#`` and blank lines are ignored. Quoted values
have surrounding single or double quotes stripped. No interpolation,
no multi-line values — keep it simple.

Usage::

    from agent._env import load_dotenv
    load_dotenv()
    api_key = os.environ.get("RESEND_API_KEY")
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENV_PATH = ROOT / ".env"


def load_dotenv(path: Path | str | None = None) -> dict[str, str]:
    """Merge KEY=value lines from .env into os.environ. Real env wins.

    Returns the dict of keys this function set (i.e. those that were
    not already present in the environment) — useful for logging.
    Silently no-ops if the file doesn't exist.
    """
    target = Path(path) if path else DEFAULT_ENV_PATH
    if not target.exists():
        return {}
    set_keys: dict[str, str] = {}
    for raw in target.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if (value.startswith("\"") and value.endswith("\"")) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        if not key or key in os.environ:
            continue
        os.environ[key] = value
        set_keys[key] = value
    return set_keys
