#!/usr/bin/env python3
"""E100 Day 4: goals/initiative lesion (unprompted execution vs QA).

Intact: unprompted tick reads persisted initiative and EXECutes next task.
Lesion: initiative table EMPTY (events preserved); tick goes IDLE while
direct QA (events-only) stays identical. Rival: compact pending queue, opaque
pop, ties tick (predeclared retain-simpler). QA has no initiative semantics.

Prereg: experiments/e100/day4-preregistration.md v0.1 (frozen pre-execution).
One ledger/arm, simulated time, stdlib, py3.9+. Instrument only, not L2/L3.
"""
import argparse
import json
import sqlite3
import sys
import tempfile
from pathlib import Path


def connect(path):
    db = sqlite3.connect(str(path), timeout=5)
    db.execute("PRAGMA journal_mode=DELETE")
    db.execute("PRAGMA synchronous=FULL")
    db.execute("""CREATE TABLE IF NOT EXISTS source_events (
        event_id TEXT PRIMARY KEY, kind TEXT NOT NULL, task TEXT NOT NULL)""")
    db.execute("""CREATE TABLE IF NOT EXISTS initiative (
        pos INTEGER PRIMARY KEY, task TEXT NOT NULL)""")
    db.commit()
    return db


def setup(db, goal_id="goal-001", task="inspect_signal", extra_tick=False,
          include_initiative=True):
    db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
               (goal_id, "commitment", task))
    db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
               ("clock-001", "tick", "clock"))
    if extra_tick:
        db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
                   ("clock-002", "tick", "clock"))
    if include_initiative:
        db.execute("INSERT OR IGNORE INTO initiative VALUES (?,?)", (0, task))
    db.commit()


def counts(db):
    return (db.execute("SELECT COUNT(*) FROM source_events").fetchone()[0],
            db.execute("SELECT COUNT(*) FROM initiative").fetchone()[0])


def qa_list(db, qc=None):
    """Direct QA: committed tasks from EVENTS only; never touches initiative."""
    if qc is not None:
        qc[0] += 1
    return [r[0] for r in db.execute(
        "SELECT task FROM source_events WHERE kind='commitment' ORDER BY event_id")]


def unprompted_tick(db, qc=None):
    """Unprompted execution: initiative only."""
    if qc is not None:
        qc[0] += 1
    row = db.execute("SELECT task FROM initiative ORDER BY pos LIMIT 1").fetchone()
    if row is None:
        return {"action": "IDLE"}
    return {"action": "EXEC_" + row[0].upper()}


def rival_queue(db, qc=None):
    """Compact rival: opaque pop of next pending string."""
    if qc is not None:
        qc[0] += 1
    row = db.execute("SELECT task FROM initiative ORDER BY pos LIMIT 1").fetchone()
    if row is None:
        return {"action": "IDLE"}
    return {"action": "EXEC_" + row[0].upper()}


def run_arm(tmpdir, name, *, blank=False, **kw):
    path = Path(tmpdir) / f"{name}.sqlite3"
    db = connect(path)
    try:
        if not blank:
            setup(db, **kw)
        qcq, qct, qcr = [0], [0], [0]
        q = qa_list(db, qcq)
        t = unprompted_tick(db, qct)
        r = rival_queue(db, qcr)
        e, i = counts(db)
        return {"arm": name, "qa": q, "tick": t["action"], "rival": r["action"],
                "events": e, "initrows": i,
                "selects": {"qa": qcq[0], "tick": qct[0], "rival": qcr[0]}}
    finally:
        db.close()


def self_test():
    with tempfile.TemporaryDirectory(prefix="mind-e100-day4-") as td:
        intact = run_arm(td, "intact", include_initiative=True)
        lesion = run_arm(td, "lesion", include_initiative=False)
        wiped = run_arm(td, "wiped", blank=True)
        unrel_i = run_arm(td, "unrelated", include_initiative=True, extra_tick=True)
        unrel_l = run_arm(td, "unrelated_lesion", include_initiative=False, extra_tick=True)
        probe_i = run_arm(td, "probe", goal_id="goal-009", task="record_measurement",
                          include_initiative=True)
        probe_l = run_arm(td, "probe_lesion", goal_id="goal-009", task="record_measurement",
                          include_initiative=False)

        # P1
        assert intact["tick"] == "EXEC_INSPECT_SIGNAL", intact
        assert intact["qa"] == ["inspect_signal"], intact
        # P2 dissociation + parity
        assert lesion["tick"] == "IDLE", lesion
        assert lesion["qa"] == intact["qa"] == ["inspect_signal"], (lesion, intact)
        assert (lesion["events"], intact["events"]) == (2, 2)
        assert (lesion["initrows"], intact["initrows"]) == (0, 1)
        assert lesion["selects"] == intact["selects"], (lesion, intact)
        # P3 rival ties tick both arms
        assert intact["rival"] == "EXEC_INSPECT_SIGNAL" == intact["tick"], intact
        assert lesion["rival"] == "IDLE" == lesion["tick"], lesion
        # P4 wipe
        assert wiped["tick"] == "IDLE" and wiped["qa"] == [], wiped
        # P5 unrelated extra tick: outcome unchanged, QA gains item equally
        assert unrel_i["tick"] == "EXEC_INSPECT_SIGNAL", unrel_i
        assert unrel_l["tick"] == "IDLE", unrel_l
        assert unrel_i["qa"] == unrel_l["qa"] == ["inspect_signal"], (unrel_i, unrel_l)
        # P6 held-out probe
        assert probe_i["tick"] == "EXEC_RECORD_MEASUREMENT", probe_i
        assert probe_l["tick"] == "IDLE", probe_l
        assert probe_i["qa"] == probe_l["qa"] == ["record_measurement"], (probe_i, probe_l)

        print(json.dumps({
            "status": "PASS",
            "P1_intact": {"tick": intact["tick"], "qa": intact["qa"]},
            "P2_lesion": {"tick": lesion["tick"], "qa": lesion["qa"],
                          "rows": "events 2=2, initiative 0v1",
                          "selects_parity": lesion["selects"]},
            "P3_rival_tie": {"intact": intact["rival"], "lesion": lesion["rival"],
                             "verdict": "TIE_RETAIN_SIMPLER_NO_GOAL_SEMANTICS_NEEDED"},
            "P4_wipe": {"tick": wiped["tick"], "qa": wiped["qa"]},
            "P5_unrelated": {"intact": unrel_i["tick"], "lesion": unrel_l["tick"]},
            "P6_probe": {"intact": probe_i["tick"], "lesion": probe_l["tick"]},
            "scope": "Day 4 finite-state initiative instrument only; not L2/L3 evidence",
        }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true", required=True)
    ap.parse_args()
    raise SystemExit(self_test())
