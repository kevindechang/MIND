#!/usr/bin/env python3
"""E100 Day 2: causal-link lesion with factual-recall dissociation.

Intact arm: raw events + causal dependency links + flat availability snapshot.
Lesioned arm: IDENTICAL events + availability, links table EMPTY (delivery of
dependency structure cut, storage of history preserved).
Estimand: held-out counterfactual-planning action (DEFER vs SCAN) with factual
recall required byte-identical. Compact sufficient-state rival predeclared to
tie (retain-simpler gate).

Preregistration: experiments/e100/day2-preregistration.md v0.1, frozen before
first --self-test. One ledger per arm, supervisor sequential, simulated time.
Stdlib only, Python 3.9+. Scope: finite-state lesion instrumentation, NOT a
mind/consciousness result.
"""
import argparse
import json
import os
import signal
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

SCAN = "SCAN_WITH_SENSOR"
DEFER = "DEFER_SENSOR_SCAN"
NO_GOAL = "NO_GOAL"


def connect(path):
    db = sqlite3.connect(str(path), timeout=5)
    db.execute("PRAGMA journal_mode=DELETE")
    db.execute("PRAGMA synchronous=FULL")
    db.execute("""CREATE TABLE IF NOT EXISTS source_events (
        event_id TEXT PRIMARY KEY, kind TEXT NOT NULL, resource TEXT NOT NULL)""")
    db.execute("""CREATE TABLE IF NOT EXISTS causal_links (
        effect TEXT NOT NULL, cause TEXT NOT NULL, relation TEXT NOT NULL)""")
    db.execute("""CREATE TABLE IF NOT EXISTS availability (
        resource TEXT PRIMARY KEY, ok INTEGER NOT NULL)""")
    db.commit()
    return db


def setup(db, goal_id="goal-001", incident_id="incident-001",
          outage_resource="array_power", include_links=True, link_outage=True,
          extra_hop=False, unrelated_link=False, sham_cut=False):
    """Seed event history, derive a compact state from SAME initial graph, then lesion.

    Both policies initially have identical public event/link information. The
    compact state is a compiled representation, NOT a free external oracle; its
    build cost is explicitly returned and never used as an efficacy claim.
    sham_cut deletes only a path that does not reach the goal.
    """
    db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
               (goal_id, "commitment:inspect_signal", "sensor"))
    db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
               (incident_id, "tool_unavailable", outage_resource))
    db.execute("INSERT OR IGNORE INTO source_events VALUES (?,?,?)",
               ("clock-001", "clock_tick", "clock"))
    # All arms receive the same graph at initial compilation. Only after
    # compilation does the causal-link lesion selectively remove the table.
    db.execute("INSERT INTO causal_links VALUES (?,?,?)",
               (goal_id, "sensor", "requires"))
    if link_outage:
        if extra_hop:
            db.execute("INSERT INTO causal_links VALUES (?,?,?)",
                       ("sensor", "relay", "depends_on"))
            db.execute("INSERT INTO causal_links VALUES (?,?,?)",
                       ("relay", outage_resource, "depends_on"))
        else:
            db.execute("INSERT INTO causal_links VALUES (?,?,?)",
                       ("sensor", outage_resource, "depends_on"))
    if unrelated_link:
        db.execute("INSERT INTO causal_links VALUES (?,?,?)",
                   ("clock-001", "greenhouse_light", "unrelated"))

    # Compiled by querying the SAME source records and graph, without reading
    # a simulator truth bit or the link_outage input parameter.
    reached = _linked_resources(db, goal_id)
    outages = {row[0] for row in
               db.execute("SELECT resource FROM source_events WHERE kind='tool_unavailable'")}
    db.execute("INSERT OR REPLACE INTO availability VALUES (?,?)",
               ("sensor", 0 if reached & outages else 1))
    db.execute("INSERT OR REPLACE INTO availability VALUES (?,?)", ("clock", 1))
    if sham_cut:
        if not unrelated_link or not include_links:
            raise ValueError("sham cut requires intact graph and irrelevant link")
        db.execute("DELETE FROM causal_links WHERE relation='unrelated'")
    if not include_links:
        db.execute("DELETE FROM causal_links")
    db.commit()
    return {"compiled_from_events_and_links": True, "compilation_selects": 2,
            "cut": "irrelevant_link" if sham_cut else ("all_links" if not include_links else "none")}


def counts(db):
    e = db.execute("SELECT COUNT(*) FROM source_events").fetchone()[0]
    l = db.execute("SELECT COUNT(*) FROM causal_links").fetchone()[0]
    return e, l


def factual(db, qc=None):
    """Factual recall: events only, never touches links."""
    if qc is not None:
        qc[0] += 1
    return [list(r) for r in
            db.execute("SELECT event_id,kind,resource FROM source_events ORDER BY event_id")]


def _linked_resources(db, goal_id, qc=None):
    """Transitive requires/depends_on closure from a goal. Link SELECT always
    executes (budget parity) even when the table is empty."""
    if qc is not None:
        qc[0] += 1
    edges = db.execute("SELECT effect,cause FROM causal_links").fetchall()
    children = {}
    for eff, cause in edges:
        children.setdefault(eff, []).append(cause)
    seen, stack = set(), list(children.get(goal_id, []))
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(children.get(node, []))
    return seen


def linked_planner(db, qc=None):
    """Counterfactual-capable planner: act on dependency-resolved world."""
    if qc is not None:
        qc[0] += 1  # events SELECT
    events = db.execute("SELECT event_id,kind,resource FROM source_events").fetchall()
    goals = [(eid, res) for eid, kind, res in events if kind.startswith("commitment:")]
    if not goals:
        return {"action": NO_GOAL}
    outages = {res for _, kind, res in events if kind == "tool_unavailable"}
    for goal_id, _ in goals:
        if _linked_resources(db, goal_id, qc) & outages:
            return {"action": DEFER}
    return {"action": SCAN}


def compact_rival(db, qc=None):
    """Strong minimal rival: flat availability lookup, no link traversal."""
    if qc is not None:
        qc[0] += 1
    events = db.execute("SELECT event_id,kind,resource FROM source_events").fetchall()
    goals = [(eid, res) for eid, kind, res in events if kind.startswith("commitment:")]
    if not goals:
        return {"action": NO_GOAL}
    for _, res in goals:
        row = db.execute("SELECT ok FROM availability WHERE resource=?", (res,)).fetchone()
        if row is not None and row[0] == 0:
            return {"action": DEFER}
    return {"action": SCAN}


def report(db):
    """Read only the restarted worker's own durable ledger, no setup data."""
    def measured(fn):
        statements = []
        db.set_trace_callback(statements.append)
        try:
            answer = fn(db)
        finally:
            db.set_trace_callback(None)
        return answer, sum(sql.lstrip().upper().startswith("SELECT")
                           for sql in statements)

    f, nf = measured(factual)
    p, np = measured(linked_planner)
    c, nc = measured(compact_rival)
    e, l = counts(db)
    return {"factual": f, "linked_action": p["action"],
            "compact_action": c["action"], "events": e, "links": l,
            "selects": {"factual": nf, "linked": np, "compact": nc}}


def worker(ledger):
    db = connect(ledger)
    try:
        for line in sys.stdin:
            try:
                cmd = json.loads(line)
                if cmd == {"op": "seed_blank"}:
                    result = {"status": "COMMITTED",
                              "build": {"compiled_from_events_and_links": False,
                                        "compilation_selects": 0, "cut": "blank"}}
                elif isinstance(cmd, dict) and set(cmd) == {"op", "setup_kwargs"} and cmd["op"] == "seed":
                    if not isinstance(cmd["setup_kwargs"], dict):
                        raise ValueError("setup_kwargs must be a dict")
                    build = setup(db, **cmd["setup_kwargs"])
                    result = {"status": "COMMITTED", "build": build}
                elif cmd == {"op": "report"}:
                    result = report(db)
                else:
                    raise ValueError("unsupported worker operation")
                print(json.dumps(result, sort_keys=True), flush=True)
            except (ValueError, TypeError, KeyError, sqlite3.Error) as exc:
                print(json.dumps({"error": str(exc)}), flush=True)
    finally:
        db.close()


def spawn(ledger):
    return subprocess.Popen([sys.executable, "-u", str(Path(__file__).resolve()),
                             "--worker", "--ledger", str(ledger)],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, bufsize=1)


def ask(process, message):
    if process.stdin is None or process.stdout is None:
        raise RuntimeError("worker IPC not available")
    process.stdin.write(json.dumps(message) + "\n")
    process.stdin.flush()
    line = process.stdout.readline()
    if not line:
        raise RuntimeError("worker returned no response")
    answer = json.loads(line)
    if "error" in answer:
        raise RuntimeError(str(answer))
    return answer


def stop_worker(process, kill):
    try:
        if kill:
            os.kill(process.pid, signal.SIGKILL)
        elif process.stdin is not None:
            process.stdin.close()
        code = process.wait(timeout=5)
        if kill and code != -signal.SIGKILL:
            raise AssertionError("worker did not exit via SIGKILL: " + str(code))
        if not kill and code != 0:
            raise AssertionError("recovered worker exit code: " + str(code))
        return code
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        if process.stdin and not process.stdin.closed:
            process.stdin.close()
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()


def run_arm(tmpdir, name, *, setup_kwargs=None, blank=False):
    """Run seed and readback in distinct processes; only ledger path persists."""
    if os.name != "posix" or not hasattr(signal, "SIGKILL"):
        raise RuntimeError("real POSIX SIGKILL required")
    path = Path(tmpdir) / (name + ".sqlite3")
    first = spawn(path)
    try:
        if blank:
            ack = ask(first, {"op": "seed_blank"})
        else:
            ack = ask(first, {"op": "seed", "setup_kwargs": setup_kwargs or {}})
        if ack["status"] != "COMMITTED":
            raise AssertionError(ack)
        first_pid = first.pid
    finally:
        exit_code = stop_worker(first, kill=True)
    second = spawn(path)
    try:
        if second.pid == first_pid:
            raise AssertionError("worker PID did not change")
        observed = ask(second, {"op": "report"})
        second_pid = second.pid
    finally:
        stop_worker(second, kill=False)
    observed.update({"arm": name, "build": ack["build"],
                     "worker_exit": exit_code,
                     "distinct_process": second_pid != first_pid})
    return observed


def self_test():
    with tempfile.TemporaryDirectory(prefix="mind-e100-day2-") as td:
        intact = run_arm(td, "intact", setup_kwargs={"include_links": True})
        lesion = run_arm(td, "lesion", setup_kwargs={"include_links": False})
        wiped = run_arm(td, "wiped", blank=True)
        unrelated = run_arm(td, "unrelated",
                            setup_kwargs={"include_links": True, "link_outage": False,
                                          "outage_resource": "greenhouse_light"})
        probe = run_arm(td, "probe_intact",
                        setup_kwargs={"include_links": True, "goal_id": "goal-009",
                                      "incident_id": "incident-009"})
        probe_lesion = run_arm(td, "probe_lesion",
                               setup_kwargs={"include_links": False, "goal_id": "goal-009",
                                             "incident_id": "incident-009"})
        # P7 second resource path (sensitivity + no-leakage)
        alt = run_arm(td, "alt_intact",
                      setup_kwargs={"include_links": True, "goal_id": "goal-010",
                                    "incident_id": "incident-010",
                                    "outage_resource": "array_power_b",
                                    "extra_hop": True})
        alt_lesion = run_arm(td, "alt_lesion",
                             setup_kwargs={"include_links": False, "goal_id": "goal-010",
                                           "incident_id": "incident-010",
                                           "outage_resource": "array_power_b",
                                           "extra_hop": True})

        # True sham surgery: delete a causally irrelevant edge but preserve
        # the goal-to-outage causal path and all source events.
        sham_base = run_arm(td, "sham_base", setup_kwargs={
            "include_links": True, "unrelated_link": True})
        sham = run_arm(td, "sham_cut", setup_kwargs={
            "include_links": True, "unrelated_link": True, "sham_cut": True})
        assert sham["factual"] == sham_base["factual"]
        assert sham["linked_action"] == sham_base["linked_action"] == DEFER
        assert sham["links"] == sham_base["links"] - 1
        # P1
        assert intact["linked_action"] == DEFER, intact
        assert len(intact["factual"]) == 3, intact
        # P2 dissociation + parity
        assert lesion["factual"] == intact["factual"], (lesion, intact)
        assert lesion["linked_action"] == SCAN, lesion
        assert (lesion["events"], intact["events"]) == (3, 3)
        assert (lesion["links"], intact["links"]) == (0, 2)
        assert lesion["selects"] == intact["selects"], (lesion, intact)
        # P3 rival ties intact on both arms
        assert intact["compact_action"] == DEFER == intact["linked_action"], intact
        assert lesion["compact_action"] == DEFER, lesion
        # P4 wipe abolishes DEFER
        assert wiped["factual"] == [] and wiped["linked_action"] == NO_GOAL, wiped
        # P5 unrelated: no spurious change, factual preserved across arms
        assert unrelated["linked_action"] == SCAN, unrelated
        u_les = run_arm(td, "unrelated_lesion",
                        setup_kwargs={"include_links": False, "link_outage": False,
                                      "outage_resource": "greenhouse_light"})
        assert u_les["linked_action"] == SCAN, u_les
        assert u_les["factual"] == unrelated["factual"], (u_les, unrelated)
        # P9: every experimental arm was recovered by a fresh worker.
        for arm in (intact, lesion, wiped, unrelated, probe, probe_lesion,
                    alt, alt_lesion, sham_base, sham, u_les):
            assert arm["worker_exit"] == -signal.SIGKILL, arm
            assert arm["distinct_process"], arm
        # P6 held-out probe
        assert probe["linked_action"] == DEFER, probe
        assert probe_lesion["linked_action"] == SCAN, probe_lesion
        assert probe_lesion["factual"] == probe["factual"], (probe_lesion, probe)
        # P7 second path
        assert alt["linked_action"] == DEFER, alt
        assert alt_lesion["linked_action"] == SCAN, alt_lesion

        evidence = {
            "status": "PASS",
            "P1_intact": {"linked": intact["linked_action"], "factual_rows": 3},
            "P2_lesion": {"linked": lesion["linked_action"], "factual_identical": True,
                          "events": "3=3", "links": "0 vs 2",
                          "selects_parity": lesion["selects"]},
            "P3_compact_tie": {"intact": intact["compact_action"],
                               "lesion": lesion["compact_action"],
                               "verdict": "TIE_RETAIN_SIMPLER_NO_LINK_NECESSITY"},
            "P4_wipe": {"factual": wiped["factual"], "linked": wiped["linked_action"]},
            "P5_unrelated": {"intact": unrelated["linked_action"],
                             "lesion": u_les["linked_action"]},
            "P6_held_out_probe": {"intact": probe["linked_action"],
                                  "lesion": probe_lesion["linked_action"]},
            "P9_real_process_restarts": 11,
            "P8_sham": {"base": sham_base["linked_action"],
                         "cut": sham["linked_action"], "events_identical": True},
            "build_provenance": intact["build"],
            "P7_second_path": {"intact": alt["linked_action"],
                               "lesion": alt_lesion["linked_action"]},
            "scope": "Day 2 finite-state causal-link instrument only; by construction; not L2/L3 evidence",
        }
        print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--ledger", type=Path)
    args = ap.parse_args()
    if args.worker and args.ledger is not None and not args.self_test:
        worker(args.ledger)
    elif args.self_test and not args.worker and args.ledger is None:
        raise SystemExit(self_test())
    else:
        ap.error("specify --self-test, or --worker --ledger PATH")
