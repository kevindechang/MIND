"""Real SIGKILL, including mid-request: exactly-once acting and a byte-identical life.

A worker process is killed with SIGKILL both after a reply and while a request is
in flight; a fresh PID restores from the SQLite ledger alone and the supervisor
blindly resends. Anjo invariant I7 (a retried event never duplicates a committed
change) holds by construction of `Organism.step_at`; this claim checks it physically.
"""
from mind.claims import Check, Claim


def sigkill(ctx):
    import os
    import random
    from mind.ledger import MemoryLedger
    from mind.runner import run
    from mind.worker import supervised_run
    from mind.worlds import WORLDS
    if os.name != "posix":
        return {"verdict": "INCONCLUSIVE", "robust": False, "summary": "NOT_EXECUTED: needs POSIX SIGKILL"}
    kills, failures, pids = 0, [], set()
    for seed in ctx.seeds:
        for world in sorted(WORLDS):
            ref = run("organism", world, seed, 12, ledger=MemoryLedger(), trace=True)
            ticks = random.Random(f"{seed}|{world}").sample(range(len(ref["trace"])), 4)
            res = supervised_run("organism", world, seed, 12, kill_after=ticks[:2], kill_during=ticks[2:])
            kills += len(res["deaths"])
            pids |= {d["pid"] for d in res["deaths"]} | {res["final_pid"]}
            if (any(d["exit"] != -9 for d in res["deaths"]) or res["trace"] != ref["trace"]
                    or res["head"] != ref["head"]):
                failures.append(f"{world}/seed{seed}")
    return {"verdict": "HOLDS" if not failures else "FAILS", "robust": True, "sigkills": kills,
            "distinct_pids": len(pids), "failures": failures,
            "summary": f"{kills} SIGKILLs (exit -9, half mid-request), {len(pids)} PIDs: "
                       f"{'all lives byte-identical' if not failures else 'DIVERGED: ' + ', '.join(failures)}"}


CLAIM = Claim(
    id="K02",
    title="Real SIGKILL mid-request: exactly-once action, byte-identical life",
    statement="Killing the organism's process with SIGKILL after replies and during in-flight requests, then "
              "restarting from the SQLite ledger alone, reproduces the uninterrupted action trace and ledger "
              "head exactly, with no action committed twice.",
    kind="invariant",
    scope="instrument",
    test=Check(sigkill, seeds=3),
    question="H008",
    depends_on=("K01",),
    extends=("L02", "experiments/e100/day0.py"),
    by="pipeline-v2",
    created="2026-10-10",
)
