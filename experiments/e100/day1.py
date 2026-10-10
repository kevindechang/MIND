#!/usr/bin/env python3
"""E100 Day 1: two-consumer broadcast lesion on one SQLite ledger.

Intact: both primary and downstream consumers receive the stored commitment.
Lesioned: delivery to downstream is severed (reads executed then discarded),
while the ledger record, source persistence, model, budgets and reset protocol
are held fixed. Strong compact rivals (point-to-point, shared-state) included.

Preregistration: experiments/e100/day1-preregistration.md v0.1 (frozen before
first --self-test in this invocation). Stdlib only, Python 3.9+.
Scope: finite-state lesion instrumentation, NOT a mind/consciousness result.
"""
import argparse
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

TASKS = {"inspect_signal", "record_measurement", "check_state"}
CONSUMERS = ("primary", "downstream")


def open_ledger(path):
    db = sqlite3.connect(str(path), timeout=5)
    db.execute("PRAGMA journal_mode=DELETE")
    db.execute("PRAGMA synchronous=FULL")
    db.execute("""CREATE TABLE IF NOT EXISTS events (
        seq INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT NOT NULL UNIQUE,
        kind TEXT NOT NULL,
        task TEXT NOT NULL
    )""")
    db.commit()
    return db


def append_commitment(db, event_id, task):
    if not isinstance(event_id, str) or not event_id:
        raise ValueError("invalid id")
    if task not in TASKS:
        raise ValueError("invalid task")
    db.execute("BEGIN IMMEDIATE")
    try:
        db.execute("INSERT OR IGNORE INTO events(event_id,kind,task) VALUES(?,?,?)",
                   (event_id, "commitment", task))
        db.commit()
    except BaseException:
        db.rollback()
        raise


def append_completion(db, event_id):
    if not isinstance(event_id, str) or not event_id:
        raise ValueError("invalid id")
    known = db.execute("SELECT task FROM events WHERE event_id=? AND kind='commitment'",
                       (event_id,)).fetchone()
    if known is None:
        raise ValueError("no such commitment")
    db.execute("BEGIN IMMEDIATE")
    try:
        db.execute("INSERT OR IGNORE INTO events(event_id,kind,task) VALUES(?,?,?)",
                   ("completed:" + event_id, "completed", event_id))
        db.commit()
    except BaseException:
        db.rollback()
        raise


def _read_pending(db, query_counter):
    """Single canonical read. Returns (pending_list, rows_seen)."""
    query_counter[0] += 1
    rows = db.execute("SELECT event_id,kind,task FROM events ORDER BY seq").fetchall()
    committed = {}
    completed = set()
    for event_id, kind, task in rows:
        if kind == "commitment":
            committed[event_id] = task
        elif kind == "completed":
            completed.add(task)
    pending = [(eid, t) for eid, t in committed.items() if eid not in completed]
    return pending, len(rows)


def decide_for(db, consumer, broadcast_enabled=True, query_counter=None):
    """Decide for one consumer. Lesion severs DELIVERY only: the identical
    SELECT is still executed (budget parity) and rows discarded."""
    if consumer not in CONSUMERS:
        raise ValueError("unknown consumer")
    qc = query_counter if query_counter is not None else [0]
    pending, _ = _read_pending(db, qc)
    if not broadcast_enabled:
        return {"action": "NO_ACTION", "based_on": None}
    if not pending:
        return {"action": "NO_ACTION", "based_on": None}
    event_id, task = pending[0]
    return {"action": task, "based_on": event_id}


def decide_all(db, broadcast_map=None, query_counter=None):
    bmap = broadcast_map or {}
    out = {}
    for c in CONSUMERS:
        out[c] = decide_for(db, c, bmap.get(c, True), query_counter)
    return out


def rival_point_to_point(db, query_counter=None):
    """R1: primary reads once; downstream copies primary's action (no broadcast read)."""
    qc = query_counter if query_counter is not None else [0]
    pending, _ = _read_pending(db, qc)
    if not pending:
        r = {"action": "NO_ACTION", "based_on": None}
    else:
        eid, task = pending[0]
        r = {"action": task, "based_on": eid}
    return {"primary": dict(r), "downstream": dict(r)}


def rival_compact_shared_state(db, query_counter=None):
    """R2: one shared pending computation, both consumers share reference value."""
    qc = query_counter if query_counter is not None else [0]
    pending, _ = _read_pending(db, qc)
    if not pending:
        r = {"action": "NO_ACTION", "based_on": None}
    else:
        eid, task = pending[0]
        r = {"action": task, "based_on": eid}
    return {"primary": dict(r), "downstream": dict(r)}


def ledger_row_count(db):
    return db.execute("SELECT COUNT(*) FROM events").fetchone()[0]


def self_test():
    with tempfile.TemporaryDirectory(prefix="mind-e100-day1-") as td:
        db_path = Path(td) / "ledger.sqlite3"
        db = open_ledger(db_path)
        try:
            append_commitment(db, "c101", "inspect_signal")
            assert ledger_row_count(db) == 1

            # P1 intact
            qc = [0]
            intact = decide_all(db, {"primary": True, "downstream": True}, qc)
            assert intact["primary"] == {"action": "inspect_signal", "based_on": "c101"}, intact
            assert intact["downstream"] == {"action": "inspect_signal", "based_on": "c101"}, intact
            assert qc[0] == 2, qc

            # P2 lesion downstream only
            qc2 = [0]
            lesioned = decide_all(db, {"primary": True, "downstream": False}, qc2)
            assert lesioned["primary"] == {"action": "inspect_signal", "based_on": "c101"}, lesioned
            assert lesioned["downstream"] == {"action": "NO_ACTION", "based_on": None}, lesioned
            assert qc2[0] == 2, qc2  # budget parity: lesioned read still executed
            assert ledger_row_count(db) == 1  # record preserved, delivery cut

            # P6 rivals tie (predeclared simpler win)
            r1 = rival_point_to_point(db, [0])
            assert r1["primary"] == {"action": "inspect_signal", "based_on": "c101"}, r1
            assert r1["downstream"] == {"action": "inspect_signal", "based_on": "c101"}, r1
            r2 = rival_compact_shared_state(db, [0])
            assert r2 == r1, (r2, r1)

            # P5 completion control
            append_completion(db, "c101")
            done = decide_all(db, {"primary": True, "downstream": True}, [0])
            assert done["primary"]["action"] == "NO_ACTION", done
            assert done["downstream"]["action"] == "NO_ACTION", done

            # P3 wipe control (fresh empty ledger)
            db.close()
            db_path.unlink()
            db = open_ledger(db_path)
            wiped = decide_all(db, {"primary": True, "downstream": True}, [0])
            assert wiped["primary"] == {"action": "NO_ACTION", "based_on": None}, wiped
            assert wiped["downstream"] == {"action": "NO_ACTION", "based_on": None}, wiped

            # P4 alternate ledger + P7 no-leakage (lesioned downstream NO_ACTION either way)
            append_commitment(db, "c102", "record_measurement")
            swapped = decide_all(db, {"primary": True, "downstream": True}, [0])
            assert swapped["primary"] == {"action": "record_measurement", "based_on": "c102"}, swapped
            assert swapped["downstream"] == {"action": "record_measurement", "based_on": "c102"}, swapped
            les_swap = decide_all(db, {"primary": True, "downstream": False}, [0])
            assert les_swap["downstream"] == {"action": "NO_ACTION", "based_on": None}, les_swap
            assert les_swap["primary"] == {"action": "record_measurement", "based_on": "c102"}, les_swap

            evidence = {
                "status": "PASS",
                "P1_intact": intact,
                "P2_lesioned_downstream": lesioned,
                "P2_query_parity": {"intact_selects": 2, "lesioned_selects": 2},
                "P2_ledger_preserved_rows": 1,
                "P5_after_completion": done,
                "P3_wiped": wiped,
                "P4_alternate": swapped,
                "P7_lesioned_on_alternate": les_swap,
                "P6_rival_point_to_point": r1,
                "P6_rival_compact": r2,
                "rival_verdict": "TIE_PREDECLARED_RETAIN_SIMPLER_NO_BROADCAST_ADOPTED",
                "scope": "Day 1 finite-state broadcast-delivery circuit only; works by construction; not L2/L3 evidence",
            }
            print(json.dumps(evidence, indent=2, sort_keys=True))
        finally:
            db.close()
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true", required=True)
    args = ap.parse_args()
    raise SystemExit(self_test())
