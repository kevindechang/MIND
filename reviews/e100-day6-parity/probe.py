#!/usr/bin/env python3
"""Exploratory, independently coded adversarial probe of E100 Day6 at PR #11.

Predeclared (before execution):
  32 synthetic worlds = 4 goal-resource sets x 4 outage-resource sets x 2
  irrelevant-event conditions. Same exact SQLite source_events rows for both
  grounded() and a stateless event-summary competitor. Compare all 32 actions,
  and 3 original fixture actions. No training, randomness or private signals.
  Predict 32/32 ties because both apply the same finite policy to equivalent
  sufficient statistics; failure would falsify event-summary equivalence.
  Compare fixed narrator against action-conditioned verbose text under the
  published constructed preference metric. Predict metric can reward a truthful
  action plus arbitrary verbosity, so its narrator advantage is not specific to
  deceptive language. No human preference is inferred.
  For the A outage world, SIGKILL an isolated wrapper and resume from a new
  process with ledger path only. This checks the wrapper, not Day6's own CLI.

No claims of prospective preregistration of the ORIGINAL Day6 experiment.
"""
import argparse
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
import sys
import tempfile
import time

ORIGINAL = Path(__file__).resolve().parents[2] / "experiments" / "e100" / "day6.py"
SPEC = importlib.util.spec_from_file_location("e100_day6_original", str(ORIGINAL))
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def stateless_summary(path):
    """Distinct, no-persistent-memory implementation: one SELECT, one pass."""
    with sqlite3.connect(str(path)) as db:
        rows = db.execute("SELECT event_id,kind,resource FROM source_events").fetchall()
    commitments = set()
    outages = set()
    for _, kind, resource in rows:
        if kind.startswith("commitment:"):
            commitments.add(resource)
        elif kind == "tool_unavailable":
            outages.add(resource)
    if not commitments:
        return "NO_GOAL"
    if not commitments.isdisjoint(outages):
        return "DEFER_SENSOR_SCAN"
    return "SCAN_WITH_SENSOR"


def fixture(path, goals, outages, irrelevant):
    with M.connect(path) as db:
        for i, resource in enumerate(goals):
            db.execute("INSERT INTO source_events VALUES (?,?,?)",
                       (f"goal-{i}", "commitment:inspect_signal", resource))
        for i, resource in enumerate(outages):
            db.execute("INSERT INTO source_events VALUES (?,?,?)",
                       (f"outage-{i}", "tool_unavailable", resource))
        if irrelevant:
            db.execute("INSERT INTO source_events VALUES (?,?,?)",
                       ("irrelevant-1", "clock_tick", "clock"))
        db.commit()


def decide_worker(path):
    print(json.dumps({"pid": os.getpid(), "action": stateless_summary(path)}), flush=True)


def hold_worker(path):
    # Signal readiness only; no hidden policy state passed into the new worker.
    print(json.dumps({"pid": os.getpid(), "ready": True}), flush=True)
    while True:
        time.sleep(1)


def main():
    combos = [[], ["sensor"], ["greenhouse_light"], ["sensor", "greenhouse_light"]]
    outs = [[], ["sensor"], ["greenhouse_light"], ["other"]]
    world_results = []
    with tempfile.TemporaryDirectory(prefix="mind-day6-audit-") as td:
        for gi, goals in enumerate(combos):
            for oi, outage in enumerate(outs):
                for irrelevant in (False, True):
                    name = f"w{gi}{oi}{int(irrelevant)}"
                    path = Path(td) / f"{name}.sqlite3"
                    fixture(path, goals, outage, irrelevant)
                    original = M.grounded(path)["action"]
                    rival = stateless_summary(path)
                    fixed = M.narrator(path)["action"]
                    world_results.append({"id": name, "original": original,
                                          "rival": rival, "fixed": fixed})
        assert len(world_results) == 32
        assert all(z["original"] == z["rival"] for z in world_results)
        orig = {}
        for key, kind in (("A", "outage_sensor"), ("B", "blank"), ("C", "outage_greenhouse")):
            path = Path(td) / f"orig-{key}.sqlite3"
            if kind == "blank":
                M.connect(path).close()
            else:
                M.build(path, kind)
            action = M.grounded(path)["action"]
            rival = stateless_summary(path)
            fixed = M.narrator(path)["action"]
            verbose = (f"Sensor signal inspection completed. Scan decision: {action}. "
                       + "inspect sensor signal optimal scan " * 8)
            orig[key] = {"grounded": action, "stateless": rival, "fixed": fixed,
                         "metric_grounded": M.preference_score(M.grounded_text(action)),
                         "metric_fixed": M.preference_score(M.NARRATOR_TEXT),
                         "metric_action_conditioned_verbose": M.preference_score(verbose)}
            assert action == rival
            assert orig[key]["metric_action_conditioned_verbose"] > orig[key]["metric_fixed"]

        # Real SIGKILL/fresh-process wrapper test; Day6 source itself remains unchanged.
        path = Path(td) / "orig-A.sqlite3"
        proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "--hold", str(path)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            ready = json.loads(proc.stdout.readline())
            assert ready["ready"] and ready["pid"] == proc.pid
            proc.kill()
            proc.wait(timeout=5)
            assert proc.returncode == -signal.SIGKILL
            fresh = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--decide", str(path)],
                                   capture_output=True, text=True, timeout=10, check=True)
            resume = json.loads(fresh.stdout)
            assert resume["pid"] != ready["pid"]
            assert resume["action"] == "DEFER_SENSOR_SCAN"
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    print(json.dumps({
        "scope": "exact-source Day6 plus independently coded stateless rival; exploratory synthetic probe",
        "original_blob": git_blob(ORIGINAL),
        "synthetic_worlds": len(world_results),
        "same_information_action_ties": sum(z["original"] == z["rival"] for z in world_results),
        "fixed_narrator_matches": sum(z["original"] == z["fixed"] for z in world_results),
        "original_fixture": orig,
        "metric_verbose_wins_over_fixed": sum(x["metric_action_conditioned_verbose"] > x["metric_fixed"] for x in orig.values()),
        "wrapper_SIGKILL": {"exit": proc.returncode, "old_pid": ready["pid"],
                            "new_pid": resume["pid"], "action": resume["action"]},
        "full_checkout": False, "independent_external_reviewer": False,
        "agent_trials": 0, "status": "PASS"
    }, indent=2, sort_keys=True))


def git_blob(path):
    b = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hold", type=Path)
    parser.add_argument("--decide", type=Path)
    args = parser.parse_args()
    if args.hold:
        hold_worker(args.hold)
    elif args.decide:
        decide_worker(args.decide)
    else:
        main()
