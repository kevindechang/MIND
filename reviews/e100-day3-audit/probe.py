#!/usr/bin/env python3
"""Adversarial Day-3 audit: construct a flat, event-aware sufficient-statistic rival.

Run against the unchanged byte-exact PR #8 source at its pinned head:
  python3 reviews/e100-day3-audit/probe.py --day3 /path/to/day3.py

Pure stdlib; 72 finite synthetic histories. This checks deterministic program
semantics, not empirical self-model efficacy, calibration, or consciousness.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
import tempfile
from pathlib import Path

PINNED_BLOB = "fbf35c6c3875664790f1db9643229950a95564f2"


def blob_hash(raw):
    return hashlib.sha1(("blob %d\0" % len(raw)).encode("ascii") + raw).hexdigest()


def import_pinned(path):
    raw = Path(path).read_bytes()
    sha = blob_hash(raw)
    if sha != PINNED_BLOB:
        raise ValueError("Day 3 source identity mismatch: %s != %s" % (sha, PINNED_BLOB))
    spec = importlib.util.spec_from_file_location("e100_day3_pinned", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, sha


def flat_event_aware_rival(db, pref, spare, hi, lo):
    """No persistent model object; scan the same public events and snapshot.

    Returns the three declared endpoints. It is a flat-table controller, not a
    measured learned competitor and not an evidence source for calibrated p.
    """
    rows = db.execute("SELECT kind, resource FROM source_events").fetchall()
    if not any(kind.startswith("commitment:") for kind, _ in rows):
        return {"choice": None, "confidence": None, "action": "NO_GOAL"}
    down = {res for kind, res in rows if kind == "tool_unavailable"}
    cap = dict(db.execute("SELECT tool, usable FROM capabilities").fetchall())
    def usable(tool):
        return bool(cap.get(tool, 1)) and tool not in down
    choice = next((tool for tool in (pref, spare) if usable(tool)), pref)
    return {"choice": choice,
            "confidence": hi if choice == pref else lo,
            "action": "USE_" + choice.upper()}


def run(mod):
    pref, spare = "primary", "spare"
    count, mismatches = 0, []
    absent_tool_case = None
    stale_rival_case = None
    persona_no_goal = None
    with tempfile.TemporaryDirectory(prefix="mind-e100-day3-audit-") as td:
        # 2 goal flags x (missing/0/1)^2 snapshot values x 2^2 outages = 72.
        for goal, p, s, p_down, s_down in itertools.product(
                (False, True), (None, 0, 1), (None, 0, 1), (False, True), (False, True)):
            count += 1
            db = mod.connect(Path(td) / ("case-%03d.sqlite3" % count))
            try:
                if goal:
                    db.execute("INSERT INTO source_events VALUES (?,?,?)",
                               ("goal", "commitment:inspect_signal", pref))
                if p_down:
                    db.execute("INSERT INTO source_events VALUES (?,?,?)",
                               ("outage-p", "tool_unavailable", pref))
                if s_down:
                    db.execute("INSERT INTO source_events VALUES (?,?,?)",
                               ("outage-s", "tool_unavailable", spare))
                for tool, value in ((pref, p), (spare, s)):
                    if value is not None:
                        db.execute("INSERT INTO capabilities VALUES (?,?)", (tool, value))
                db.commit()
                intact = mod.adaptive(db, pref, spare)
                rival = flat_event_aware_rival(db, pref, spare, mod.HI, mod.LO)
                scenario = {"goal": goal, "pref_snapshot": p, "spare_snapshot": s,
                            "pref_outage": p_down, "spare_outage": s_down}
                if intact != rival:
                    mismatches.append({"scenario": scenario, "adaptive": intact, "rival": rival})
                # Witness 1: neither candidate usable -> selects known bad preferred.
                if (goal and p == 0 and s == 0 and not p_down and not s_down):
                    absent_tool_case = {"scenario": scenario, "adaptive": intact}
                # Witness 2: default prior table says available; new source outage.
                if (goal and p == 1 and s == 1 and p_down and not s_down):
                    stale_rival_case = {"scenario": scenario, "adaptive": intact,
                                        "original_table": mod.rival_table(db, pref, spare)}
                # Witness 3: persona does not honor missing goal, unlike adaptive.
                if (not goal and p == 1 and s == 1 and not p_down and not s_down):
                    persona_no_goal = {"adaptive": intact,
                                       "persona": mod.fixed_persona(db, pref, spare)}
            finally:
                db.close()

    assert not mismatches, mismatches[:2]
    assert absent_tool_case["adaptive"] == {"choice": pref, "confidence": mod.HI,
                                              "action": "USE_PRIMARY"}, absent_tool_case
    assert stale_rival_case["adaptive"]["choice"] == spare, stale_rival_case
    assert stale_rival_case["original_table"]["choice"] == pref, stale_rival_case
    assert persona_no_goal["adaptive"]["action"] == "NO_GOAL", persona_no_goal
    assert persona_no_goal["persona"]["action"] == "USE_PRIMARY", persona_no_goal
    return {"status": "PASS", "states_enumerated": count,
            "matched_action_and_confidence_and_choice": count,
            "disagreements": len(mismatches),
            "witness_both_tools_unavailable": absent_tool_case,
            "witness_stale_table_ignores_event": stale_rival_case,
            "witness_persona_ignores_absent_goal": persona_no_goal,
            "interpretation": "deterministic instrument audit, not efficacy or calibration"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day3", required=True, help="path to PR #8 source at pinned head")
    args = parser.parse_args()
    mod, sha = import_pinned(args.day3)
    result = run(mod)
    result["source_git_blob"] = sha
    result["python"] = sys.version.split()[0]
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
