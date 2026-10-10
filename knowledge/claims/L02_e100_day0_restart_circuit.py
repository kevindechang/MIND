"""E100 Day 0 (v1): a SIGKILLed worker's committed action survives in a fresh process.

The v1 circuit is kept byte-unchanged and re-executed. Its generalisation to the
whole learning organism, every world and every lesion is claim K02.
"""
from mind.claims import Check, Claim


def day0(ctx):
    import json
    import subprocess
    import sys
    from mind.claims import ROOT
    p = subprocess.run([sys.executable, "experiments/e100/day0.py", "--self-test"], cwd=ROOT,
                       capture_output=True, text=True, timeout=60)
    if p.returncode == 2:
        return {"verdict": "INCONCLUSIVE", "robust": False, "summary": "NOT_EXECUTED: needs POSIX SIGKILL"}
    r = json.loads(p.stdout)
    ok = (p.returncode == 0 and r["observed_worker_exit_code"] == -9
          and r["on_restart"]["action"] == "inspect_signal"
          and r["wiped_ledger"]["action"] == "NO_ACTION"
          and r["alternate_ledger"]["action"] == "record_measurement")
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True,
            "summary": f"exit {r['observed_worker_exit_code']}, restart→{r['on_restart']['action']}, "
                       f"wipe→{r['wiped_ledger']['action']}, alternate→{r['alternate_ledger']['action']}"}


CLAIM = Claim(
    id="L02",
    title="Day 0: a committed task survives real process death (v1 circuit)",
    statement="After SIGKILL (exit -9) a new process given only the ledger path recovers the committed "
              "action; a wiped ledger yields NO_ACTION; a different ledger yields a different action.",
    kind="fact",
    scope="instrument",
    test=Check(day0),
    question="H008",
    extends=("experiments/e100/day0.py",),
    by="pipeline-v2 migration (v1 author: E100 Day 0)",
    created="2026-10-10",
    rationale="A finite-state circuit, not cognition. Kept as the ancestor of K02.",
)
