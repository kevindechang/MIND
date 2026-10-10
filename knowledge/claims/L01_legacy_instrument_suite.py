"""All v1 instrument tests still pass (75 at migration), so v1 knowledge stays executable.

Builds on: every v1 instrument under experiments/instruments. Ported as a single
regression guard so that the v1 results cited by L02–L07 cannot silently rot.
"""
from mind.claims import Check, Claim


def legacy_suite(ctx):
    import re
    import subprocess
    import sys
    from mind.claims import ROOT
    p = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "experiments/instruments",
                        "-p", "test_*.py"], cwd=ROOT, capture_output=True, text=True, timeout=900)
    m = re.search(r"Ran (\d+) tests?", p.stderr)
    ran = int(m.group(1)) if m else 0
    ok = p.returncode == 0 and ran >= 75
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True, "tests": ran,
            "summary": f"{ran} v1 instrument tests {'all pass' if p.returncode == 0 else 'FAIL'}"}


CLAIM = Claim(
    id="L01",
    title="The v1 instrument suite still passes",
    statement="All v1 instrument unit tests (>= 75) pass on the current checkout.",
    kind="invariant",
    scope="instrument",
    test=Check(legacy_suite),
    extends=("experiments/instruments", "scripts/verify_instruments.py"),
    by="pipeline-v2 migration",
    created="2026-10-10",
    rationale="v1 recorded these as separately observed runs; v2 makes them one standing check.",
)
