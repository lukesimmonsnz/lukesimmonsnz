#!/usr/bin/env python3
"""Test lint for both regions."""
import sys
from pathlib import Path

# Setup paths
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root))

for region in ['hawkes-bay', 'taranaki']:
    print(f"\n=== Testing {region} ===")
    # Import and run lint
    lint_file = repo_root / f'content/{region}/tools/lint.py'
    spec = __import__('importlib.util').util.spec_from_file_location("lint", lint_file)
    lint_module = __import__('importlib.util').util.module_from_spec(spec)
    sys.modules['lint'] = lint_module
    try:
        spec.loader.exec_module(lint_module)
        exit_code = lint_module.main()
        print(f"Lint exit code: {exit_code}")
    except Exception as e:
        print(f"Error running lint: {e}")
        import traceback
        traceback.print_exc()
