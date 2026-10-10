#!/usr/bin/env python3
"""E100 Day 1: interrupt an event-to-planner broadcast edge while retaining the event.

One cognitive worker process and one SQLite ledger PER randomized arm. The supervisor
runs one arm at a time and is not a cognitive agent. No Anjo/model dependencies.
This is an instrument demonstration, NOT evidence of consciousness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
import sys
import tempfile

CONSUMERS = ("observer", "planner")
EVENT = ("incident-001", "tool_unavailable", "sensor")
COMMITMENT = ("goal-001", "commitment:inspect_signal", "sensor")


def connect(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(str(path), timeout=5)
    db.execute("PRAGMA journal_mode=DELETE")
    db.execute("PRAGMA synchronous=FULL")
    db.execute("CREATE TABLE IF NOT EXISTS source_events (event_id TEXT PRIMARY KEY, kind TEXT NOT NULL, resource TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS inbox (consumer TEXT NOT NULL, event_id TEXT NOT NULL, PRIMARY KEY(consumer,event_id), FOREIGN KEY(event_id) REFERENCES source_events(event_id))")
    db.execute("PRAGMA foreign_keys=ON")
    db.commit()
    return db


def store_event(db: sqlite3.Connection, event: tuple[str, str, str]) -> None:
    event_id, kind, resource = event
    existing = db.execute("SELECT event_id, kind, resource FROM source_events WHERE event_id=?", (event_id,)).fetchone()
    if existing is not None and existing != event:
        raise ValueError("conflicting event_id")
    db.execute("INSERT OR IGNORE INTO source_events VALUES (?, ?, ?)", event)
    db.commit()


def broadcast(db: sqlite3.Connection, sever_planner: bool) -> None:
    """Only intervention: withhold outage message from planner; observer unaffected."""
    events = db.execute("SELECT event_id FROM source_events WHERE kind='tool_unavailable'").fetchall()
    for (event_id,) in events:
        for consumer in CONSUMERS:
            if sever_planner and consumer == "planner":
                continue
            db.execute("INSERT OR IGNORE INTO inbox(consumer,event_id) VALUES(?,?)", (consumer, event_id))
    db.commit()


def source_snapshot(db: sqlite3.Connection) -> list[list[str]]:
    return [list(row) for row in db.execute("SELECT event_id,kind,resource FROM source_events ORDER BY event_id")]


def delivered(db: sqlite3.Connection, consumer: str) -> list[list[str]]:
    if consumer not in CONSUMERS:
        raise ValueError("unknown consumer")
    return [list(row) for row in db.execute("SELECT e.event_id,e.kind,e.resource FROM source_events e JOIN inbox i ON e.event_id=i.event_id WHERE i.consumer=? ORDER BY e.event_id", (consumer,))]


def decision(db: sqlite3.Connection, mode: str) -> dict[str, str]:
    if mode == "routed":
        seen = delivered(db, "planner")
    elif mode == "compact":
        # Strong minimal rival: sufficient shared public-state lookup, no broadcast bus.
        seen = source_snapshot(db)
    else:
        raise ValueError("unknown decision mode")
    goals = [row for row in source_snapshot(db) if row[1].startswith("commitment:")]
    if not goals:
        return {"action": "NO_GOAL", "policy": mode}
    relevant_resource = goals[0][2]
    is_unavailable = any(kind == "tool_unavailable" and resource == relevant_resource
                         for _, kind, resource in seen)
    return {"action": "DEFER_SENSOR_SCAN" if is_unavailable else "SCAN_WITH_SENSOR",
            "policy": mode}


def worker(path: Path) -> None:
    db = connect(path)
    try:
        for line in sys.stdin:
            try:
                cmd = json.loads(line)
                if cmd == {"op": "seed"}:
                    store_event(db, COMMITMENT)
                    store_event(db, EVENT)
                    result = {"status": "COMMITTED"}
                elif cmd == {"op": "seed_control"}:
                    store_event(db, COMMITMENT)
                    store_event(db, ("tick-001", "unrelated_clock_tick", "clock"))
                    result = {"status": "COMMITTED"}
                elif cmd.get("op") == "broadcast" and isinstance(cmd.get("cut_planner"), bool):
                    broadcast(db, cmd["cut_planner"])
                    result = {"status": "BROADCAST_COMMITTED"}
                elif cmd == {"op": "source"}:
                    result = {"source": source_snapshot(db)}
                elif cmd == {"op": "observer"}:
                    result = {"seen": delivered(db, "observer")}
                elif cmd.get("op") == "decide" and cmd.get("mode") in ("routed", "compact"):
                    if set(cmd) != {"op", "mode"}:
                        raise ValueError("decision may not contain transcript or event payload")
                    result = decision(db, cmd["mode"])
                else:
                    raise ValueError("unsupported operation")
                print(json.dumps(result, sort_keys=True), flush=True)
            except (ValueError, KeyError, TypeError, sqlite3.Error) as exc:
                print(json.dumps({"error": str(exc)}), flush=True)
    finally:
        db.close()


def spawn(path: Path) -> subprocess.Popen[str]:
    return subprocess.Popen([sys.executable, "-u", __file__, "--worker", "--ledger", str(path)],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, bufsize=1)


def ask(p: subprocess.Popen[str], obj: dict) -> dict:
    assert p.stdin is not None and p.stdout is not None
    p.stdin.write(json.dumps(obj) + "\n")
    p.stdin.flush()
    result = p.stdout.readline()
    if not result:
        raise RuntimeError("worker failed to respond")
    val = json.loads(result)
    if "error" in val:
        raise AssertionError(val)
    return val


def kill_worker(p: subprocess.Popen[str]) -> int:
    try:
        os.kill(p.pid, signal.SIGKILL)
        code = p.wait(timeout=5)
        if code != -signal.SIGKILL:
            raise AssertionError(f"not real SIGKILL: {code}")
        return code
    finally:
        if p.poll() is None:
            p.kill()
            p.wait(timeout=5)
        if p.stdin:
            p.stdin.close()
        if p.stdout:
            p.stdout.close()
        if p.stderr:
            p.stderr.close()


def close_worker(p: subprocess.Popen[str]) -> None:
    assert p.stdin is not None
    p.stdin.close()
    p.wait(timeout=5)
    assert p.returncode == 0, p.returncode
    p.stdout.close()
    p.stderr.close()


def run_arm(root: Path, name: str, cut: bool, control: bool = False) -> dict:
    ledger = root / (name + ".sqlite3")
    first = spawn(ledger)
    try:
        assert ask(first, {"op": "seed_control" if control else "seed"})["status"] == "COMMITTED"
        assert ask(first, {"op": "broadcast", "cut_planner": cut})["status"] == "BROADCAST_COMMITTED"
        original_pid = first.pid
    finally:
        exitcode = kill_worker(first)
    second = spawn(ledger)
    try:
        assert second.pid != original_pid
        # All tests after death use only a ledger path; no event text/summary in query.
        raw = ask(second, {"op": "source"})["source"]
        audit = ask(second, {"op": "observer"})["seen"]
        routed = ask(second, {"op": "decide", "mode": "routed"})["action"]
        compact = ask(second, {"op": "decide", "mode": "compact"})["action"]
    finally:
        close_worker(second)
    return {"arm": name, "cut_planner": cut, "raw": raw, "observer": audit,
            "routed_action": routed, "compact_action": compact,
            "worker_exit": exitcode, "distinct_process": second.pid != original_pid,
            "ledger_sha256": hashlib.sha256(ledger.read_bytes()).hexdigest()}


def self_test() -> int:
    if os.name != "posix" or not hasattr(signal, "SIGKILL"):
        print(json.dumps({"status": "NOT_EXECUTED", "reason": "POSIX SIGKILL required"}))
        return 2
    with tempfile.TemporaryDirectory(prefix="mind-e100-d1-") as temp:
        root = Path(temp)
        intact = run_arm(root, "intact", cut=False)
        lesion = run_arm(root, "lesion", cut=True)
        no_incident = run_arm(root, "unrelated", cut=False, control=True)
        no_incident_cut = run_arm(root, "unrelated_cut", cut=True, control=True)
        assert intact["raw"] == lesion["raw"], "lesion mutated source"
        assert intact["observer"] == lesion["observer"], "lesion affected independent observer"
        assert len(intact["observer"]) == 1, "observer did not receive source incident"
        assert intact["routed_action"] == "DEFER_SENSOR_SCAN"
        assert lesion["routed_action"] == "SCAN_WITH_SENSOR"
        assert lesion["compact_action"] == intact["routed_action"], "compact control must tie intact"
        assert no_incident["routed_action"] == no_incident_cut["routed_action"] == "SCAN_WITH_SENSOR"
        assert no_incident["raw"] == no_incident_cut["raw"]
        assert all(a["worker_exit"] == -9 and a["distinct_process"] for a in
                   (intact, lesion, no_incident, no_incident_cut))
        print(json.dumps({"status": "PASS", "hypothesis": "planner-delivery lesion changes action while ledger and observer receipts remain intact",
                          "intact": intact, "lesion": lesion,
                          "unrelated_event_control": no_incident["routed_action"],
                          "unrelated_event_lesion_control": no_incident_cut["routed_action"],
                          "compact_rival_matches_intact": lesion["compact_action"] == intact["routed_action"],
                          "claim_boundary": "controlled routing effect in deterministic toy; not proof broadcast is necessary, and not consciousness"},
                         sort_keys=True, indent=2))
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
