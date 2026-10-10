#!/usr/bin/env python3
"""v1 entry point, kept for old instructions and schedulers: delegates to `python -m mind doctor`."""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    raise SystemExit(subprocess.call([sys.executable, "-m", "mind", "doctor"], cwd=root))
