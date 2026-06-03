#!/usr/bin/env python3
"""Validate and render all three regions."""

import subprocess
import sys
from pathlib import Path

def run_lint(region):
    """Run lint for a region."""
    print(f"\nLinting {region}...")
    result = subprocess.run(
        [sys.executable, f"content/{region}/tools/lint.py"],
        cwd="/sessions/blissful-festive-clarke/mnt/Current website",
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    return result.returncode == 0

def run_render(region):
    """Run render for a region."""
    print(f"\nRendering {region}...")
    result = subprocess.run(
        [sys.executable, f"content/{region}/tools/render.py", "--all"],
        cwd="/sessions/blissful-festive-clarke/mnt/Current website",
        capture_output=True,
        text=True,
        timeout=60
    )
    print(result.stdout[:500] if result.stdout else "(no output)")
    if result.stderr:
        print("STDERR:", result.stderr[:500])
    return result.returncode == 0

regions = ["nelson", "tasman", "west-coast"]

print("=" * 60)
print("VALIDATION AND RENDERING")
print("=" * 60)

for region in regions:
    print(f"\n{'='*60}")
    print(f"{region.upper()}")
    print('='*60)

    lint_ok = run_lint(region)
    print(f"Lint: {'PASS' if lint_ok else 'FAIL'}")

    if lint_ok:
        render_ok = run_render(region)
        print(f"Render: {'PASS' if render_ok else 'FAIL'}")

print("\n" + "="*60)
print("VALIDATION COMPLETE")
print("="*60)
