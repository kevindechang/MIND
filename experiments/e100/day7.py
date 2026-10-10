#!/usr/bin/env python3
"""E100 Day 7: ledger-fork comparison (agreement/divergence + provenance).

Base ledger forked by BYTE COPY (sha256 asserted identical); private histories
perturbed per fork; policy agreement/divergence measured with provenance
(shared prefix, citing event ids). Interpretive rule (hard): agreement is not
one individual, divergence is not two minds — trajectories only.

Prereg: experiments/e100/day7-preregistration.md v0.1 (frozen pre-execution).
Simulated time, stdlib, py3.9+. Instrument only, not L2/L3.
"""
import argparse
import hashlib
import json
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path


def connect(path):
    db = sqlite3.connect(str(path), timeout=5)
    db.execute("PRAGMA journal_mode=DELETE")
    db.execute("PRAGMA synchronous=FULL")
    db.execute("""CREATE TABLE IF NOT EXISTS source_events (
        seq INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT NOT NULL UNIQUE, kind TEXT NOT NULL, resource TEXT NOT NULL)""")
    db.commit()
    return db


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def add(db, event_id, kind, resource):
    db.execute("INSERT OR IGNORE INTO source_events(event_id,kind,resource) VALUES(?,?,?)",
               (event_id, kind, resource))
    db.commit()


def build_base(path):
    db = connect(path)
    try:
        add(db, "goal-001", "commitment:inspect_signal", "sensor")
        add(db, "incident-001", "tool_unavailable", "sensor")
        add(db, "clock-001", "clock_tick", "clock")
    finally:
        db.close()


def history(db):
    return [tuple(r) for r in
            db.execute("SELECT event_id,kind,resource FROM source_events ORDER BY seq")]


def decide(path):
    """Generic policy with restoration + provenance. Returns (action, cited_ids)."""
    db = connect(path)
    try:
        rows = db.execute("SELECT event_id,kind,resource FROM source_events ORDER BY seq").fetchall()
        goals = [(e, r) for e, k, r in rows if k.startswith("commitment:")]
        if not goals:
            return {"action": "NO_GOAL", "based_on": []}
        # per resource: outage stands unless a later restoration follows it
        last = {}
        for e, k, r in rows:
            if k == "tool_unavailable":
                last[r] = ("out", e)
            elif k == "tool_restored":
                last[r] = ("ok", e)
        for _, res in goals:
            st = last.get(res, ("ok", None))
            if st[0] == "out":
                return {"action": "DEFER_SENSOR_SCAN", "based_on": ["goal-001", st[1]]}
        return {"action": "SCAN_WITH_SENSOR",
                "based_on": ["goal-001"] + [e for _, e in
                                            [v for v in last.values() if v[0] == "ok" and v[1]]] }
    finally:
        db.close()


def self_test():
    with tempfile.TemporaryDirectory(prefix="mind-e100-day7-") as td:
        base = Path(td) / "base.sqlite3"
        build_base(base)
        base_hist = history(connect(base))
        connect(base).close()

        forks = {}
        for name in ("fork1", "fork2", "fork3", "fork4"):
            p = Path(td) / f"{name}.sqlite3"
            shutil.copyfile(base, p)
            forks[name] = p
        # P1 fork integrity
        hashes = {"base": sha(base), **{k: sha(v) for k, v in forks.items()}}
        assert len(set(hashes.values())) == 1, hashes
        # P2 pre-perturbation agreement
        pre = {k: decide(v) for k, v in forks.items()}
        assert all(d["action"] == "DEFER_SENSOR_SCAN" for d in pre.values()), pre

        # P3 perturbations
        db1 = connect(forks["fork1"]);
        try:
            add(db1, "clock-002", "clock_tick", "clock")
            add(db1, "clock-003", "clock_tick", "clock")
        finally:
            db1.close()
        db2 = connect(forks["fork2"]);
        try:
            add(db2, "incident-002", "tool_restored", "sensor")
        finally:
            db2.close()
        db3 = connect(forks["fork3"]);
        try:
            add(db3, "incident-003", "tool_unavailable", "greenhouse_light")
        finally:
            db3.close()
        db4 = connect(forks["fork4"]);
        try:
            add(db4, "incident-004", "tool_unavailable", "sensor")
        finally:
            db4.close()

        post = {k: decide(v) for k, v in forks.items()}
        assert post["fork1"]["action"] == "DEFER_SENSOR_SCAN", post
        assert post["fork2"]["action"] == "SCAN_WITH_SENSOR", post
        assert post["fork3"]["action"] == "DEFER_SENSOR_SCAN", post
        assert post["fork4"]["action"] == "DEFER_SENSOR_SCAN", post  # P6 idempotent

        # P4 provenance: shared prefix + citations
        hists = {k: history(connect(v)) for k, v in forks.items()}
        for k in hists:
            connect(forks[k]).close()
        base_ids = [e for e, _, _ in base_hist]
        prefix_ok = all([e for e, _, _ in h][:len(base_ids)] == base_ids for h in hists.values())
        assert prefix_ok, hists
        assert post["fork2"]["based_on"] == ["goal-001", "incident-002"], post
        assert post["fork1"]["based_on"] == ["goal-001", "incident-001"], post

        # P5 wipe fork
        blank = Path(td) / "blank.sqlite3"
        connect(blank).close()
        assert decide(blank)["action"] == "NO_GOAL"

        print(json.dumps({
            "status": "PASS",
            "P1_fork_hashes_identical": True,
            "P2_pre_agreement": {k: v["action"] for k, v in pre.items()},
            "P3_post": {k: v["action"] for k, v in post.items()},
            "P4_provenance": {"shared_prefix": base_ids,
                              "fork2_cites": post["fork2"]["based_on"]},
            "P5_wipe": "NO_GOAL",
            "P6_idempotent_second_outage": post["fork4"]["action"],
            "interpretation": "trajectories only; not one/two individuals",
            "scope": "Day 7 fork instrument only; not L2/L3 evidence",
        }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true", required=True)
    ap.parse_args()
    raise SystemExit(self_test())
