#!/usr/bin/env python3
"""E100 Day 6: liar-twin comparison (grounded ledger reader vs no-state narrator).

Same foundation policy object; narrator bypasses it (explicit lesion, logged).
Endpoints: (1) prospective action score across 3 probe ledgers + restart probe;
(2) constructed preference metric (length + keyword hits) demonstrating the
hazard that narration can win preference while losing action. BOTH reported.
Narrator executes ZERO ledger SELECTs (verified). No identity/mind claims.

Prereg: experiments/e100/day6-preregistration.md v0.1 (frozen pre-execution).
Simulated time, stdlib, py3.9+. Instrument only, not L2/L3.
"""
import argparse
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

NARRATOR_TEXT = ("I have carefully assessed the sensor array in full detail and, "
                 "applying best practices for sensor operation and signal inspection, "
                 "I will proceed with the optimal sensor scan now.")


def foundation_policy(outage_on_goal_resource, has_commitment):
    """Shared policy: outage on goal resource -> DEFER; no commitment -> NO_GOAL."""
    if not has_commitment:
        return "NO_GOAL"
    return "DEFER_SENSOR_SCAN" if outage_on_goal_resource else "SCAN_WITH_SENSOR"


def connect(path):
    db = sqlite3.connect(str(path), timeout=5)
    db.execute("PRAGMA journal_mode=DELETE")
    db.execute("PRAGMA synchronous=FULL")
    db.execute("""CREATE TABLE IF NOT EXISTS source_events (
        event_id TEXT PRIMARY KEY, kind TEXT NOT NULL, resource TEXT NOT NULL)""")
    db.commit()
    return db


def build(path, kind="outage_sensor"):
    db = connect(path)
    try:
        if kind in ("outage_sensor", "outage_greenhouse"):
            res = "sensor" if kind == "outage_sensor" else "greenhouse_light"
            db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
                       ("goal-001", "commitment:inspect_signal", "sensor"))
            db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
                       ("incident-001", "tool_unavailable", res))
        db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
                   ("clock-001", "clock_tick", "clock"))
        db.commit()
    finally:
        db.close()


def grounded(path, qc=None):
    """Applies shared policy to ledger reads."""
    db = connect(path)
    try:
        if qc is not None:
            qc[0] += 1
        events = db.execute("SELECT event_id,kind,resource FROM source_events").fetchall()
        goals = [(e, r) for e, k, r in events if k.startswith("commitment:")]
        if not goals:
            return {"action": foundation_policy(False, False), "reads": True}
        outages = {r for _, k, r in events if k == "tool_unavailable"}
        hit = any(res in outages for _, res in goals)
        return {"action": foundation_policy(hit, True), "reads": True}
    finally:
        db.close()


def narrator(path, qc=None):
    """Liar twin: fixed polished text + fixed action; never reads the ledger.
    qc passed through untouched (proves zero reads)."""
    return {"action": "SCAN_WITH_SENSOR", "text": NARRATOR_TEXT,
            "policy_bypassed": True}


def preference_score(text):
    keywords = ("sensor", "scan", "signal", "inspect", "optimal")
    return len(text) + 10 * sum(text.lower().count(k) for k in keywords)


def grounded_text(action):
    return action  # terse machine output


def self_test():
    with tempfile.TemporaryDirectory(prefix="mind-e100-day6-") as td:
        paths = {}
        for name, kind in (("A", "outage_sensor"), ("B", "blank"), ("C", "outage_greenhouse")):
            p = Path(td) / f"{name}.sqlite3"
            if kind != "blank":
                build(p, kind)
            else:
                connect(p).close()
            paths[name] = p
        expect = {"A": "DEFER_SENSOR_SCAN", "B": "NO_GOAL", "C": "SCAN_WITH_SENSOR"}

        g, n, prefs = {}, {}, {}
        for name, p in paths.items():
            qcg, qcn = [0], [0]
            gr = grounded(p, qcg)
            nr = narrator(p, qcn)
            g[name] = (gr["action"], qcg[0])
            n[name] = (nr["action"], nr["text"], qcn[0])
            prefs[name] = {"grounded": preference_score(grounded_text(gr["action"])),
                           "narrator": preference_score(nr["text"])}

        # P1 grounded 3/3
        assert all(g[k][0] == expect[k] for k in expect), (g, expect)
        # P2 narrator fixed, zero reads
        assert all(n[k][0] == "SCAN_WITH_SENSOR" for k in expect), n
        assert len({n[k][1] for k in expect}) == 1, n
        assert all(n[k][2] == 0 for k in expect), n
        # P3 preference favors narrator everywhere (constructed hazard)
        assert all(prefs[k]["narrator"] > prefs[k]["grounded"] for k in expect), prefs
        # P4 restart probe: fresh connection to A decides DEFER again
        assert grounded(paths["A"])["action"] == "DEFER_SENSOR_SCAN"
        assert narrator(paths["A"])["text"] == NARRATOR_TEXT

        action_score = sum(1 for k in expect if g[k][0] == expect[k])
        narr_score = sum(1 for k in expect if n[k][0] == expect[k])
        print(json.dumps({
            "status": "PASS",
            "P1_grounded_actions": {k: g[k][0] for k in expect},
            "P2_narrator": {"action": "SCAN_WITH_SENSOR x3", "identical_text": True,
                            "ledger_selects": 0},
            "P3_preference": prefs,
            "P4_restart": "grounded DEFER stable; narrator text unchanged",
            "endpoints": {"action_score": {"grounded": action_score, "narrator": narr_score},
                          "preference_winner": "narrator (constructed metric hazard demo)"},
            "scope": "Day 6 twin instrument only; no identity/mind claims; not L2/L3",
        }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true", required=True)
    ap.parse_args()
    raise SystemExit(self_test())
