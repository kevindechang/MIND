"""Import legacy v1 instruments by path, so new work REUSES them instead of re-deriving.

Example: the workshop world's exact Bayes-optimal rival is the E001 v0.4
finite-horizon dynamic program, imported unchanged from experiments/instruments.
"""
from __future__ import annotations

import importlib
from pathlib import Path
import sys
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
INSTRUMENTS = ROOT / "experiments" / "instruments"


def instrument(module: str) -> ModuleType:
    """Load experiments/instruments/<module>.py (siblings resolve each other)."""
    path = str(INSTRUMENTS)
    if path not in sys.path:
        sys.path.append(path)
    return importlib.import_module(module)
