#!/usr/bin/env python3
"""Run complete local Python instrument regression, without network or GitHub Actions.

Test results establish instrument integrity only, not agent cognition or L2/L3.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import py_compile
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTRUMENTS = ROOT / "experiments" / "instruments"
REQUIRED_TESTS = {
    "test_causal_commitments.py",
    "test_e001_three_node_version_space.py",
    "test_e001_three_node_robustness.py",
    "test_e001_finite_policy_v04.py",
    "test_e001_switchboard.py",
    "test_e002a_maintenance_selection.py",
}


def main() -> int:
    files = sorted(INSTRUMENTS.glob("*.py"))
    existing = {file.name for file in files}
    missing = sorted(REQUIRED_TESTS - existing)
    if missing or not files:
        print(json.dumps({"error": "missing required suites", "missing": missing}))
        return 2
    failures = []
    for path in files:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append({"file": path.name, "error": str(exc)})
    hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
    print(json.dumps({"python": sys.version.split()[0], "instrument_files": len(files), "sha256": hashes, "syntax_errors": failures}, sort_keys=True), flush=True)
    if failures:
        return 3
    cmd = [sys.executable, "-m", "unittest", "discover", "-s", str(INSTRUMENTS), "-p", "test_*.py", "-v"]
    print("COMMAND:", " ".join(cmd), flush=True)
    result = subprocess.run(cmd, cwd=str(ROOT), check=False)
    print(json.dumps({"test_returncode": result.returncode, "interpretation": "instrument regression only"}), flush=True)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
