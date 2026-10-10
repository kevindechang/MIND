#!/usr/bin/env python3
"""E100 Day 5: maintenance selector lesion (internal vs external-adaptive vs cron).

Intact: internal mechanism selects max-net-gain work, executes, receipts.
Strong rival: adaptive EXTERNAL scheduler, same rule/same evidence/same
opportunities — predeclared TIE (no identified endogenous advantage; the null
IS the finding). Second rival: compute-matched cron (same SELECTs, fixed
order) — must underperform, proving task signal exists.
Estimand: realized net utility minus compute cost (1/select).

Prereg: experiments/e100/day5-preregistration.md v0.1 (frozen pre-execution).
One ledger/arm, simulated time, stdlib, py3.9+. Instrument only, not L2/L3.
"""
import argparse
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

CRON_ORDER = ["vacuum", "recalibrate", "audit"]


def connect(path):
    db = sqlite3.connect(str(path), timeout=5)
    db.execute("PRAGMA journal_mode=DELETE")
    db.execute("PRAGMA synchronous=FULL")
    db.execute("""CREATE TABLE IF NOT EXISTS work_orders (
        task TEXT PRIMARY KEY, gain REAL NOT NULL, cost REAL NOT NULL)""")
    db.execute("""CREATE TABLE IF NOT EXISTS receipts (
        task TEXT PRIMARY KEY, net REAL NOT NULL)""")
    db.commit()
    return db


def setup(db, orders=(("recalibrate", 10, 3), ("vacuum", 5, 1), ("audit", 2, 4))):
    for task, gain, cost in orders:
        db.execute("INSERT OR IGNORE INTO work_orders VALUES (?,?,?)", (task, gain, cost))
    db.commit()


def _orders(db, qc):
    qc[0] += 1
    return db.execute("SELECT task,gain,cost FROM work_orders").fetchall()


def _execute(db, pick, qc):
    if pick is None:
        return {"action": "IDLE", "receipt": None}
    qc[0] += 1  # receipt write counts as compute
    rows = db.execute("SELECT gain,cost FROM work_orders WHERE task=?", (pick,)).fetchone()
    net = rows[0] - rows[1]
    db.execute("INSERT OR REPLACE INTO receipts VALUES (?,?)", (pick, net))
    db.commit()
    return {"action": "EXEC_" + pick.upper(), "receipt": net}


def internal(db, qc):
    """Endogenous mechanism: max net gain, strictly positive, else IDLE."""
    best, best_net = None, 0.0
    for task, gain, cost in _orders(db, qc):
        if gain - cost > best_net:
            best, best_net = task, gain - cost
    return _execute(db, best, qc)


def external_adaptive(db, qc):
    """Strong rival: same max-net rule as outside directive, same evidence."""
    best, best_net = None, 0.0
    for task, gain, cost in _orders(db, qc):
        if gain - cost > best_net:
            best, best_net = task, gain - cost
    return _execute(db, best, qc)


def cron_matched(db, qc):
    """Compute-matched cron: fixed order over the single orders read (no extra
    lookups), then the same receipt write. Total SELECTs equal adaptive arms."""
    rows = _orders(db, qc)  # the one and only read
    avail = {t for t, _, _ in rows}
    pick = next((t for t in CRON_ORDER if t in avail), None)
    return _execute(db, pick, qc)


def estimand(result, selects):
    return (result["receipt"] or 0.0) - float(selects)


def run_arm(tmpdir, name, *, blank=False, orders=None):
    path = Path(tmpdir) / f"{name}.sqlite3"
    db = connect(path)
    try:
        if not blank:
            setup(db, **({} if orders is None else {"orders": orders}))
        qi, qe, qc = [0], [0], [0]
        i = internal(db, qi)
        # external + cron need fresh receipt state: use savepoint-free reset
        db.execute("DELETE FROM receipts")
        db.commit()
        e = external_adaptive(db, qe)
        db.execute("DELETE FROM receipts")
        db.commit()
        c = cron_matched(db, qc)
        return {"arm": name,
                "internal": {**i, "estimand": estimand(i, qi[0])},
                "external": {**e, "estimand": estimand(e, qe[0])},
                "cron": {**c, "estimand": estimand(c, qc[0])},
                "selects": {"internal": qi[0], "external": qe[0], "cron": qc[0]}}
    finally:
        db.close()


def self_test():
    with tempfile.TemporaryDirectory(prefix="mind-e100-day5-") as td:
        m = run_arm(td, "main")
        wiped = run_arm(td, "wiped", blank=True)
        neg = run_arm(td, "negative", orders=(("a", 1, 5), ("b", 1, 5)))
        probe = run_arm(td, "probe", orders=(("polish", 6, 2), ("sweep", 9, 3), ("log", 1, 9)))

        # P1 intact picks recalibrate net 7
        assert m["internal"]["action"] == "EXEC_RECALIBRATE", m
        assert m["internal"]["receipt"] == 7, m
        # P2 predeclared null: external identical pick/receipt/selects/estimand
        assert m["external"]["action"] == m["internal"]["action"], m
        assert m["external"]["receipt"] == m["internal"]["receipt"], m
        assert m["selects"]["external"] == m["selects"]["internal"], m
        assert m["external"]["estimand"] == m["internal"]["estimand"], m
        # P3 cron matched-compute but worse estimand (signal exists)
        assert m["selects"]["cron"] == m["selects"]["internal"], m
        assert m["cron"]["action"] == "EXEC_VACUUM", m
        assert m["cron"]["estimand"] < m["internal"]["estimand"], m
        # P4 wipe
        assert wiped["internal"]["action"] == "IDLE", wiped
        assert wiped["external"]["action"] == "IDLE", wiped
        # P5 all-negative
        assert neg["internal"]["action"] == "IDLE", neg
        assert neg["external"]["action"] == "IDLE", neg
        # P6 held-out probe sweep net 6, internal==external
        assert probe["internal"]["action"] == "EXEC_SWEEP", probe
        assert probe["external"]["action"] == "EXEC_SWEEP", probe
        assert probe["internal"]["receipt"] == 6, probe

        print(json.dumps({
            "status": "PASS",
            "P1_internal": {"action": m["internal"]["action"], "receipt": m["internal"]["receipt"]},
            "P2_external_tie": {"action": m["external"]["action"],
                                "estimand_equal": True,
                                "verdict": "NULL_NO_IDENTIFIED_ENDOGENOUS_ADVANTAGE"},
            "P3_cron": {"action": m["cron"]["action"],
                        "estimand": m["cron"]["estimand"],
                        "internal_estimand": m["internal"]["estimand"]},
            "P4_wipe": wiped["internal"]["action"],
            "P5_negative": neg["internal"]["action"],
            "P6_probe": probe["internal"]["action"],
            "scope": "Day 5 finite-state selector instrument only; not L2/L3 evidence",
        }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true", required=True)
    ap.parse_args()
    raise SystemExit(self_test())
