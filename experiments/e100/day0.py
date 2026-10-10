#!/usr/bin/env python3
"""E100 Day 0: one finite-state worker; SQLite is its ONLY durable cognitive state.

The --self-test supervisor is experiment instrumentation, not part of the worker.
Requires POSIX SIGKILL and Python 3.9+ stdlib. No model/API/Anjo dependencies.
"""
import argparse
import json
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
import sys
import tempfile

TASKS = {"inspect_signal", "record_measurement", "check_state"}


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


def append(db, event_id, kind, task):
    db.execute("BEGIN IMMEDIATE")
    try:
        db.execute("INSERT OR IGNORE INTO events(event_id,kind,task) VALUES(?,?,?)",
                   (event_id, kind, task))
        db.commit()             # acknowledged ONLY after the SQLite commit returns
    except BaseException:
        db.rollback()
        raise


def decide(db):
    # Deliberately reconstructs state from the ledger on EVERY decision; no transcript,
    # inherited globals, dialogue replay, Python pickle, or previous process memory.
    rows = db.execute("SELECT event_id,kind,task FROM events ORDER BY seq").fetchall()
    committed = {}
    completed = set()
    for event_id, kind, task in rows:
        if kind == "commitment":
            committed[event_id] = task
        elif kind == "completed":
            completed.add(task)    # completed row references the commitment event ID
    pending = [(event_id, task) for event_id, task in committed.items()
               if event_id not in completed]
    if not pending:
        return {"action": "NO_ACTION", "based_on": None}
    event_id, task = pending[0]
    return {"action": task, "based_on": event_id}


def worker(path):
    db = open_ledger(path)
    try:
        for line in sys.stdin:
            try:
                cmd = json.loads(line)
                op = cmd.get("op")
                if op == "commit":
                    event_id, task = cmd["event_id"], cmd["task"]
                    if (not isinstance(event_id, str) or not event_id or
                            task not in TASKS):
                        raise ValueError("invalid commitment")
                    append(db, event_id, "commitment", task)
                    result = {"status": "COMMITTED", "event_id": event_id}
                elif op == "decide":
                    if set(cmd) != {"op"}:
                        raise ValueError("decision may not pass history or task")
                    result = decide(db)
                elif op == "complete":
                    eid = cmd["event_id"]
                    if not isinstance(eid, str) or not eid:
                        raise ValueError("invalid id")
                    known = db.execute("SELECT task FROM events WHERE event_id=? AND kind='commitment'",
                                       (eid,)).fetchone()
                    if known is None:
                        raise ValueError("no such commitment")
                    append(db, "completed:" + eid, "completed", eid)
                    result = {"status": "COMPLETED", "event_id": eid}
                else:
                    raise ValueError("unsupported operation")
                print(json.dumps(result, sort_keys=True), flush=True)
            except (ValueError, KeyError, TypeError, sqlite3.Error) as exc:
                print(json.dumps({"error": str(exc)}), flush=True)
    finally:
        db.close()


def send(child, payload):
    if child.poll() is not None:
        raise AssertionError("worker exited unexpectedly")
    child.stdin.write(json.dumps(payload) + "\n")
    child.stdin.flush()
    line = child.stdout.readline()
    if not line:
        raise AssertionError("worker did not respond")
    return json.loads(line)


def spawn(path):
    return subprocess.Popen([sys.executable, "-u", __file__, "--worker", "--ledger", str(path)],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, bufsize=1)


def stop(child):
    child.stdin.close()
    child.wait(timeout=5)
    child.stdout.close()
    child.stderr.close()


def self_test():
    if os.name != "posix" or not hasattr(signal, "SIGKILL"):
        print(json.dumps({"status": "NOT_EXECUTED", "reason": "POSIX SIGKILL required"}))
        return 2
    with tempfile.TemporaryDirectory(prefix="mind-e100-day0-") as td:
        location = Path(td)
        db_path = location / "ledger.sqlite3"
        before = spawn(db_path)
        try:
            ack = send(before, {"op": "commit", "event_id": "c001", "task": "inspect_signal"})
            assert ack == {"status": "COMMITTED", "event_id": "c001"}, ack
            first_pid = before.pid
            os.kill(first_pid, signal.SIGKILL)  # actual death, NOT graceful shutdown
            code = before.wait(timeout=5)
            assert code == -signal.SIGKILL, code
        finally:
            if before.poll() is None:
                before.kill()
                before.wait(timeout=5)
            before.stdin.close()
            before.stdout.close()
            before.stderr.close()

        after = spawn(db_path)  # no state carried in argv except DB location
        try:
            resumed = send(after, {"op": "decide"})
            assert resumed == {"action": "inspect_signal", "based_on": "c001"}, resumed
            assert after.pid != first_pid, "not a distinct process"
            completed = send(after, {"op": "complete", "event_id": "c001"})
            assert completed["status"] == "COMPLETED"
            assert send(after, {"op": "decide"})["action"] == "NO_ACTION"
            resumed_pid = after.pid
        finally:
            stop(after)

        # Wipe ledger: a new empty database MUST abolish the action (negative control).
        db_path.unlink()
        blank = spawn(db_path)
        try:
            erased = send(blank, {"op": "decide"})
            assert erased == {"action": "NO_ACTION", "based_on": None}, erased
        finally:
            stop(blank)

        # Alternative durable history changes the decision with exactly the same read request.
        other = spawn(db_path)
        try:
            assert send(other, {"op": "commit", "event_id": "c002",
                                "task": "record_measurement"})["status"] == "COMMITTED"
        finally:
            stop(other)
        different = spawn(db_path)
        try:
            swapped = send(different, {"op": "decide"})
            assert swapped == {"action": "record_measurement", "based_on": "c002"}, swapped
        finally:
            stop(different)
        evidence = {"status": "PASS", "observed_worker_exit_code": code,
                    "signal": "SIGKILL", "first_worker_pid": first_pid,
                    "resumed_worker_pid": resumed_pid,
                    "on_restart": resumed, "after_completion": "NO_ACTION",
                    "wiped_ledger": erased, "alternate_ledger": swapped,
                    "decision_input_after_restart": {"op": "decide"},
                    "sqlite_state_store_count": 1,
                    "scope": "Day 0 finite-state persistence circuit only; not a learned mind or consciousness result"}
        print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--worker", action="store_true")
    group.add_argument("--self-test", action="store_true")
    parser.add_argument("--ledger", type=Path)
    args = parser.parse_args()
    if args.worker:
        if args.ledger is None:
            parser.error("--worker requires --ledger")
        worker(args.ledger)
    else:
        raise SystemExit(self_test())
