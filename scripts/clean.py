#!/usr/bin/env python3
"""Cross-platform cleanup for caches and interim build artifacts."""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for cache_dir in ROOT.rglob("__pycache__"):
    try:
        shutil.rmtree(cache_dir, ignore_errors=True)
    except Exception:
        pass

for name in [".pytest_cache", ".ruff_cache", ".mypy_cache", ".next/cache"]:
    target = ROOT / name
    if target.exists():
        try:
            shutil.rmtree(target, ignore_errors=True)
        except Exception:
            pass

print("Cleaned cache and temporary files.")
