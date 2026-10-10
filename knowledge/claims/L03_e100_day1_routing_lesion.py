"""E100 Day 1 (v1): cutting event->planner delivery flips the planner; a compact reader ties.

Kept byte-unchanged and re-executed. Its lesson (a routing lesion on a hand-written
rule is a by-construction effect, and a compact state ties) motivated making
lesions operators on ONE learning organism (kernel `cut:X>Y`) instead of toys.
"""
from mind.claims import Check, Claim


def day1(ctx):
    import json
    import subprocess
    import sys
    from mind.claims import ROOT
    p = subprocess.run([sys.executable, "experiments/e100/day1.py", "--self-test"], cwd=ROOT,
                       capture_output=True, text=True, timeout=60)
    if p.returncode == 2:
        return {"verdict": "INCONCLUSIVE", "robust": False, "summary": "NOT_EXECUTED: needs POSIX SIGKILL"}
    r = json.loads(p.stdout)
    ok = (p.returncode == 0 and r["intact"]["routed_action"] == "DEFER_SENSOR_SCAN"
          and r["lesion"]["routed_action"] == "SCAN_WITH_SENSOR"
          and r["compact_rival_matches_intact"] is True)
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True,
            "summary": f"intact {r['intact']['routed_action']}, cut {r['lesion']['routed_action']}, "
                       f"compact rival ties: {r['compact_rival_matches_intact']}"}


CLAIM = Claim(
    id="L03",
    title="Day 1: a routing cut flips a hand-written planner, and a compact reader ties (v1)",
    statement="With identical stored events, cutting delivery to the planner changes DEFER_SENSOR_SCAN to "
              "SCAN_WITH_SENSOR, while a compact direct ledger reader matches the intact planner.",
    kind="fact",
    scope="instrument",
    test=Check(day1),
    question="H003",
    extends=("experiments/e100/day1.py",),
    by="pipeline-v2 migration (v1 author: E100 Day 1)",
    created="2026-10-10",
)
