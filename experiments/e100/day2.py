#!/usr/bin/env python3
"""E100 Day 2 causal-link lesion: SQLite worker, actual SIGKILL, held-out action.

This is a finite deterministic INSTRUMENT, not a mind or an agent-efficacy trial.
One ledger per arm. The supervisor's held-out reward function is never given to
worker. All arms have identical source histories and decision opportunities.
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

ACTIONS = ("A", "B")
MODES = ("causal", "compact", "predictive")


def connect(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(str(path), timeout=5)
    db.execute("PRAGMA journal_mode=DELETE")
    db.execute("PRAGMA synchronous=FULL")
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("""CREATE TABLE IF NOT EXISTS source_events (
        event_id TEXT PRIMARY KEY, regime TEXT NOT NULL, intervention TEXT NOT NULL,
        outcome INTEGER NOT NULL CHECK(outcome IN (0,1)), context TEXT NOT NULL
    )""")
    db.execute("""CREATE TABLE IF NOT EXISTS causal_links (
        source TEXT NOT NULL, target TEXT NOT NULL, value INTEGER NOT NULL,
        PRIMARY KEY(source,target))""")
    db.commit()
    return db


def raw(db: sqlite3.Connection) -> list[list]:
    return [list(r) for r in db.execute(
        "SELECT event_id,regime,intervention,outcome,context FROM source_events ORDER BY event_id")]


def links(db: sqlite3.Connection) -> list[list]:
    return [list(r) for r in db.execute(
        "SELECT source,target,value FROM causal_links ORDER BY source,target")]


def seed(db: sqlite3.Connection, rows: list[list]) -> None:
    if db.execute("SELECT count(*) FROM source_events").fetchone()[0]:
        raise ValueError("already seeded")
    if len(rows) > 6 or len(rows) < 2:
        raise ValueError("invalid source budget")
    for eid, regime, intervention, outcome, context in rows:
        if regime not in ("do", "observe") or intervention not in ACTIONS or outcome not in (0, 1) or context != "train":
            raise ValueError("invalid event")
        db.execute("INSERT INTO source_events VALUES(?,?,?,?,?)", (eid, regime, intervention, outcome, context))
    db.commit()


def extract(db: sqlite3.Connection) -> None:
    """Only intervention records support edges; observational correlation is ignored."""
    observations = raw(db)
    if db.execute("SELECT count(*) FROM causal_links").fetchone()[0]:
        raise ValueError("already extracted")
    for action in ACTIONS:
        values = [outcome for _, regime, act, outcome, _ in observations if regime == "do" and act == action]
        if len(values) == 1:
            db.execute("INSERT INTO causal_links VALUES(?,?,?)", (action, "GOAL", values[0]))
    db.execute("INSERT INTO causal_links VALUES(?,?,?)", ("clock", "beacon", 1))
    db.commit()


def cut(db: sqlite3.Connection, intervention: str) -> None:
    if intervention == "lesion":
        db.execute("DELETE FROM causal_links WHERE target='GOAL'")
    elif intervention == "sham":
        db.execute("DELETE FROM causal_links WHERE source='clock' AND target='beacon'")
    elif intervention != "intact":
        raise ValueError("invalid lesion")
    db.commit()


def decide(db: sqlite3.Connection, mode: str) -> str:
    if mode == "causal":
        signal = {s: v for s, target, v in links(db) if target == "GOAL"}
    elif mode in ("compact", "predictive"):
        # Strong simple rival: sufficient one-bit action success estimates from
        # SAME publicly available raw interventions, ignoring observational rows.
        # No private graph or evaluator's future reward is accessible here.
        signal = {}
        for action in ACTIONS:
            values = [o for _, regime, act, o, _ in raw(db) if regime == "do" and act == action]
            if len(values) == 1:
                signal[action] = values[0]
    else:
        raise ValueError("invalid policy")
    winners = [a for a in ACTIONS if signal.get(a) == 1]
    return "DO_" + winners[0] if len(winners) == 1 else "NO_ACTION"


def worker(path: Path) -> None:
    db = connect(path)
    try:
        for line in sys.stdin:
            try:
                cmd = json.loads(line)
                op = cmd.get("op")
                if op == "seed" and set(cmd) == {"op", "rows"}:
                    seed(db, cmd["rows"])
                    result = {"status": "SEEDED"}
                elif cmd == {"op": "extract"}:
                    extract(db)
                    result = {"status": "EXTRACTED"}
                elif op == "cut" and set(cmd) == {"op", "intervention"}:
                    cut(db, cmd["intervention"])
                    result = {"status": "CUT"}
                elif cmd == {"op": "raw"}:
                    result = {"raw": raw(db)}
                elif cmd == {"op": "links"}:
                    result = {"links": links(db)}
                elif op == "decide" and set(cmd) == {"op", "mode"} and cmd["mode"] in MODES:
                    result = {"action": decide(db, cmd["mode"])}
                else:
                    raise ValueError("invalid command or forbidden decision payload")
                print(json.dumps(result, sort_keys=True), flush=True)
            except (KeyError, TypeError, ValueError, sqlite3.Error) as exc:
                print(json.dumps({"error": str(exc)}, sort_keys=True), flush=True)
    finally:
        db.close()


def spawn(path: Path) -> subprocess.Popen[str]:
    return subprocess.Popen([sys.executable, "-u", __file__, "--worker", "--ledger", str(path)],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, bufsize=1)


def ask(proc: subprocess.Popen[str], obj: dict) -> dict:
    assert proc.stdin is not None and proc.stdout is not None
    proc.stdin.write(json.dumps(obj) + "\n")
    proc.stdin.flush()
    line = proc.stdout.readline()
    if not line:
        raise RuntimeError("worker died or produced no response")
    result = json.loads(line)
    if "error" in result:
        raise AssertionError(result)
    return result


def stop(proc: subprocess.Popen[str]) -> None:
    if proc.poll() is None:
        proc.stdin.close()
        proc.wait(timeout=5)
    else:
        proc.stdin.close()
    proc.stdout.close()
    proc.stderr.close()


def kill(proc: subprocess.Popen[str]) -> int:
    try:
        os.kill(proc.pid, signal.SIGKILL)
        code = proc.wait(timeout=5)
        if code != -signal.SIGKILL:
            raise AssertionError("not SIGKILL: " + str(code))
        return code
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=5)
        proc.stdin.close()
        proc.stdout.close()
        proc.stderr.close()


def history(training_winner: str, observed_decoy: bool = True) -> list[list]:
    if training_winner not in ("A", "B", "NONE"):
        raise ValueError("invalid training world")
    rows = [["do-a", "do", "A", int(training_winner == "A"), "train"],
            ["do-b", "do", "B", int(training_winner == "B"), "train"]]
    if observed_decoy:
        # Observational records point in the OPPOSITE direction in world A/B;
        # they must not override the actual interventional effect estimate.
        rows += [["obs-a", "observe", "A", int(training_winner == "B"), "train"],
                 ["obs-b", "observe", "B", int(training_winner == "A"), "train"]]
    return rows


def reward(action: str, future_winner: str) -> int:
    """Supervisor-only evaluator; never passed to the worker at decision time."""
    if future_winner == "NONE":
        return int(action == "NO_ACTION")
    return int(action == "DO_" + future_winner)


def run_arm(root: Path, label: str, rows: list[list], intervention: str, future_winner: str) -> dict:
    ledger = root / (label + ".sqlite3")
    first = spawn(ledger)
    try:
        assert ask(first, {"op": "seed", "rows": rows})["status"] == "SEEDED"
        assert ask(first, {"op": "extract"})["status"] == "EXTRACTED"
        assert ask(first, {"op": "cut", "intervention": intervention})["status"] == "CUT"
        pid_before = first.pid
    finally:
        exitcode = kill(first)
    second = spawn(ledger)
    try:
        assert second.pid != pid_before
        raw_after = ask(second, {"op": "raw"})["raw"]
        links_after = ask(second, {"op": "links"})["links"]
        acts = {m: ask(second, {"op": "decide", "mode": m})["action"] for m in MODES}
        pid_after = second.pid
    finally:
        stop(second)
    return {"arm": label, "intervention": intervention, "raw": raw_after,
            "links": links_after, "actions": acts, "rewards": {m: reward(a, future_winner) for m, a in acts.items()},
            "worker_exit": exitcode, "first_pid": pid_before, "resumed_pid": pid_after,
            "ledger_sha256": hashlib.sha256(ledger.read_bytes()).hexdigest()}


def self_test() -> int:
    if os.name != "posix" or not hasattr(signal, "SIGKILL"):
        print(json.dumps({"status": "NOT_EXECUTED", "reason": "POSIX SIGKILL required"}))
        return 2
    with tempfile.TemporaryDirectory(prefix="mind-e100-day2-") as td:
        root = Path(td)
        outcomes = {}
        # World A, world B, null, and unannounced future mechanism reversal.
        worlds = [("A", "A", "A"), ("B", "B", "B"), ("NONE", "NONE", "NONE"),
                  ("SHIFT", "A", "B")]
        for world, training, future in worlds:
            rows = history(training)
            arms = {arm: run_arm(root, world + "-" + arm, rows, arm, future)
                    for arm in ("intact", "lesion", "sham")}
            assert arms["intact"]["raw"] == arms["lesion"]["raw"] == arms["sham"]["raw"]
            assert arms["intact"]["links"] != arms["lesion"]["links"]
            assert all(x["worker_exit"] == -9 and x["first_pid"] != x["resumed_pid"] for x in arms.values())
            for arm in arms.values():
                assert arm["actions"]["compact"] == arm["actions"]["predictive"]
            assert arms["intact"]["actions"]["causal"] == arms["sham"]["actions"]["causal"]
            assert arms["intact"]["actions"]["causal"] == arms["lesion"]["actions"]["compact"]
            if world in ("A", "B"):
                assert arms["intact"]["actions"]["causal"] == "DO_" + world
                assert arms["lesion"]["actions"]["causal"] == "NO_ACTION"
                assert arms["intact"]["rewards"]["causal"] == 1
                assert arms["lesion"]["rewards"]["causal"] == 0
                assert arms["lesion"]["rewards"]["compact"] == 1
            elif world == "NONE":
                assert all(x["actions"]["causal"] == "NO_ACTION" for x in arms.values())
            elif world == "SHIFT":
                assert arms["intact"]["actions"]["causal"] == "DO_A"
                assert arms["intact"]["rewards"]["causal"] == 0
                assert arms["lesion"]["rewards"]["compact"] == 0
            outcomes[world] = {arm: {"causal_action": d["actions"]["causal"],
                                     "compact_action": d["actions"]["compact"],
                                     "predictive_action": d["actions"]["predictive"],
                                     "causal_reward": d["rewards"]["causal"],
                                     "compact_reward": d["rewards"]["compact"],
                                     "source_sha256": hashlib.sha256(json.dumps(d["raw"], sort_keys=True).encode()).hexdigest(),
                                     "worker_exit": d["worker_exit"],
                                     "first_pid": d["first_pid"], "resumed_pid": d["resumed_pid"]}
                               for arm, d in arms.items()}
        print(json.dumps({"status": "PASS", "experiment": "E100 Day2 finite causal-memory lesion",
                          "worlds": outcomes, "world_count": len(worlds), "arm_count": len(worlds) * 3,
                          "claim_boundary": "synthetic routing/storage lesion; compact and predictive rivals tie intact; shift falsifies transfer; not evidence of a mind"},
                         sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--worker", action="store_true")
    g.add_argument("--self-test", action="store_true")
    parser.add_argument("--ledger", type=Path)
    args = parser.parse_args()
    if args.worker:
        if args.ledger is None:
            parser.error("--worker requires --ledger")
        worker(args.ledger)
    else:
        raise SystemExit(self_test())
