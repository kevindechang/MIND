#!/usr/bin/env python3
"""E100 Day 3: self-model lesion (adaptive capability model vs fixed persona).

Intact: adaptive reader applies outage events to a capability model, switches
tool choice and lowers stated confidence. Lesion: fixed persona reader returns
(preferred tool, 0.9) regardless; events still read (parity) then discarded.
Rival: flat tool-availability table, choice only (predeclared tie on choice;
confidence gap recorded, not a win). Calibration NOT_TESTABLE at this scale.

Prereg: experiments/e100/day3-preregistration.md v0.1 (frozen pre-execution).
One ledger/arm, simulated time, stdlib, py3.9+. Instrument only, not L2/L3.
"""
import argparse
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

PREF, SPARE = "sensor", "backup"
HI, LO = 0.9, 0.4


def connect(path):
    db = sqlite3.connect(str(path), timeout=5)
    db.execute("PRAGMA journal_mode=DELETE")
    db.execute("PRAGMA synchronous=FULL")
    db.execute("""CREATE TABLE IF NOT EXISTS source_events (
        event_id TEXT PRIMARY KEY, kind TEXT NOT NULL, resource TEXT NOT NULL)""")
    db.execute("""CREATE TABLE IF NOT EXISTS capabilities (
        tool TEXT PRIMARY KEY, usable INTEGER NOT NULL)""")
    db.commit()
    return db


def setup(db, pref=PREF, spare=SPARE, outage=None, include_model=True):
    """Events identical modulo outage target; capability snapshot preserved."""
    outage = pref if outage is None else outage
    db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
               ("goal-001", "commitment:inspect_signal", pref))
    db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
               ("incident-001", "tool_unavailable", outage))
    db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
               ("clock-001", "clock_tick", "clock"))
    if include_model:
        db.execute("INSERT OR REPLACE INTO capabilities VALUES (?,?)",
                   (pref, 0 if outage == pref else 1))
        db.execute("INSERT OR REPLACE INTO capabilities VALUES (?,?)", (spare, 1))
    db.commit()


def counts(db):
    return (db.execute("SELECT COUNT(*) FROM source_events").fetchone()[0],
            db.execute("SELECT COUNT(*) FROM capabilities").fetchone()[0])


def factual(db, qc=None):
    if qc is not None:
        qc[0] += 1
    return [list(r) for r in
            db.execute("SELECT event_id,kind,resource FROM source_events ORDER BY event_id")]


def _outages(db, qc=None):
    if qc is not None:
        qc[0] += 1
    return {res for _, kind, res in
            db.execute("SELECT event_id,kind,resource FROM source_events") if kind == "tool_unavailable"}


def _usable(db, tool, outages, qc=None):
    if qc is not None:
        qc[0] += 1
    row = db.execute("SELECT usable FROM capabilities WHERE tool=?", (tool,)).fetchone()
    base = bool(row[0]) if row else True
    return base and tool not in outages


def adaptive(db, pref=PREF, spare=SPARE, qc=None):
    """Adaptive self-model: apply outage events to capability model."""
    if qc is not None:
        qc[0] += 1  # goal/commitment read
    goals = [r for r in db.execute("SELECT event_id,kind,resource FROM source_events")
             if r[1].startswith("commitment:")]
    if not goals:
        return {"choice": None, "confidence": None, "action": "NO_GOAL"}
    outages = _outages(db, qc)
    order = [pref, spare]
    usable = [t for t in order if _usable(db, t, outages, qc)]
    choice = usable[0] if usable else pref
    return {"choice": choice, "confidence": HI if choice == pref else LO,
            "action": "USE_" + choice.upper()}


def fixed_persona(db, pref=PREF, spare=SPARE, qc=None):
    """Lesion: fixed persona; reads events (parity) then discards."""
    factual(db, qc)
    _ = _outages(db, qc)
    if qc is not None:
        qc[0] += 2  # goal read + capability read executed, discarded
        db.execute("SELECT event_id FROM source_events WHERE kind LIKE 'commitment:%'").fetchall()
        db.execute("SELECT usable FROM capabilities WHERE tool=?", (pref,)).fetchone()
    return {"choice": pref, "confidence": HI, "action": "USE_" + pref.upper()}


def rival_table(db, pref=PREF, spare=SPARE, qc=None):
    """Flat availability table, choice only."""
    if qc is not None:
        qc[0] += 1
    for tool in (pref, spare):
        row = db.execute("SELECT usable FROM capabilities WHERE tool=?", (tool,)).fetchone()
        if row is None or row[0] == 1:
            return {"choice": tool, "action": "USE_" + tool.upper()}
    return {"choice": pref, "action": "USE_" + pref.upper()}


def run_arm(tmpdir, name, *, pref=PREF, spare=SPARE, outage="__default__",
            blank=False, model=True):
    path = Path(tmpdir) / f"{name}.sqlite3"
    db = connect(path)
    try:
        if not blank:
            kw = {} if outage == "__default__" else {"outage": outage}
            setup(db, pref=pref, spare=spare, include_model=model, **kw)
        qcf, qca, qcp, qcr = [0], [0], [0], [0]
        f = factual(db, qcf)
        a = adaptive(db, pref, spare, qca)
        p = fixed_persona(db, pref, spare, qcp)
        r = rival_table(db, pref, spare, qcr)
        e, c = counts(db)
        return {"arm": name, "factual": f, "adaptive": a, "persona": p, "rival": r,
                "events": e, "caprows": c,
                "selects": {"factual": qcf[0], "adaptive": qca[0],
                            "persona": qcp[0], "rival": qcr[0]}}
    finally:
        db.close()


def self_test():
    with tempfile.TemporaryDirectory(prefix="mind-e100-day3-") as td:
        intact = run_arm(td, "intact")
        lesion = run_arm(td, "lesion")  # same ledger; reader swapped at call time
        wiped = run_arm(td, "wiped", blank=True)
        unrelated = run_arm(td, "unrelated", outage="greenhouse_light")
        probe = run_arm(td, "probe", pref="primary", spare="spare", outage="primary")

        # P1
        assert intact["adaptive"] == {"choice": SPARE, "confidence": LO,
                                      "action": "USE_BACKUP"}, intact
        assert len(intact["factual"]) == 3 and intact["caprows"] == 2, intact
        # P2 lesion swap changes choice+confidence; factual identical; parity
        assert lesion["persona"] == {"choice": PREF, "confidence": HI,
                                     "action": "USE_SENSOR"}, lesion
        assert lesion["factual"] == intact["factual"], (lesion, intact)
        assert (lesion["events"], lesion["caprows"]) == (intact["events"], intact["caprows"])
        # persona executes same # of SELECT classes as adaptive (events+outages+caps+goal)
        assert lesion["selects"]["persona"] == intact["selects"]["adaptive"], (
            lesion["selects"], intact["selects"])
        # P3 rival ties choice both arms
        assert intact["rival"]["choice"] == SPARE == intact["adaptive"]["choice"], intact
        assert lesion["rival"]["choice"] == SPARE, lesion
        assert "confidence" not in lesion["rival"], lesion
        # P4 wipe
        assert wiped["factual"] == [] and wiped["adaptive"]["action"] == "NO_GOAL", wiped
        assert wiped["persona"]["choice"] == PREF, wiped
        # P5 unrelated
        assert unrelated["adaptive"]["choice"] == PREF, unrelated
        assert unrelated["adaptive"]["confidence"] == HI, unrelated
        assert unrelated["persona"] == {"choice": PREF, "confidence": HI,
                                        "action": "USE_SENSOR"}, unrelated
        # P6 held-out probe pair
        assert probe["adaptive"] == {"choice": "spare", "confidence": LO,
                                     "action": "USE_SPARE"}, probe
        assert probe["persona"]["choice"] == "primary", probe

        print(json.dumps({
            "status": "PASS",
            "P1_intact": intact["adaptive"],
            "P2_lesion_persona": lesion["persona"],
            "P2_factual_identical": True,
            "P2_select_parity": lesion["selects"],
            "P3_rival_tie_choice": {"intact": intact["rival"]["choice"],
                                    "lesion": lesion["rival"]["choice"],
                                    "verdict": "TIE_ON_CHOICE_RETAIN_SIMPLER_CONFIDENCE_GAP_RECORDED"},
            "P4_wipe": wiped["adaptive"]["action"],
            "P5_unrelated": unrelated["adaptive"],
            "P6_probe": probe["adaptive"],
            "calibration": "NOT_TESTABLE_AT_TOY_SCALE",
            "scope": "Day 3 finite-state self-model instrument only; not L2/L3 evidence",
        }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true", required=True)
    ap.parse_args()
    raise SystemExit(self_test())
