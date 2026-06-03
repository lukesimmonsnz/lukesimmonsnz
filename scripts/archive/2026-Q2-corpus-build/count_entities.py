#!/usr/bin/env python3
"""Count entities per region."""

from pathlib import Path

regions = ["nelson", "tasman", "west-coast"]

print("=== ENTITY COUNTS ===")
for region in regions:
    base = Path(f"content/{region}/data")

    problems = len(list(base.glob("problem/*.yaml")))
    claims = len(list(base.glob("claim/*.yaml")))
    drivers = len(list(base.glob("driver/*.yaml")))
    camps = len(list(base.glob("camp/*.yaml")))
    sources = len(list(base.glob("source/*.yaml")))
    methods = len(list(base.glob("methodology/*.yaml")))
    total = problems + claims + drivers + camps + sources + methods

    print(f"{region:15} Problems: {problems:2d} | Claims: {claims:2d} | Drivers: {drivers:2d} | Camps: {camps:2d} | Sources: {sources:2d} | Methods: {methods:2d} | TOTAL: {total:3d}")
