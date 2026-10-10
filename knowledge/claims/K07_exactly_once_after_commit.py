"""Exactly-once acting (Anjo invariant I7), physically tested.

The supervisor SIGKILLs the worker only after the tick (or the episode's end)
is durably COMMITTED in SQLite and before the reply is read, then resends. The
fresh process must answer from the ledger (the replay path of Organism.step_at
and the end-idempotency check) and the life must stay byte-identical. K02's
in-flight kills never reached this path (v2 review, finding 5).
"""
from mind.claims import Check, Claim


def exactly_once(ctx):
    import os
    import random
    from mind.ledger import MemoryLedger
    from mind.runner import run
    from mind.worker import supervised_run
    from mind.worlds import WORLDS
    if os.name != "posix":
        return {"verdict": "INCONCLUSIVE", "robust": False, "summary": "NOT_EXECUTED: needs POSIX SIGKILL"}
    failures, kills, replays = [], 0, {"step": 0, "end": 0}
    for seed in ctx.seeds:
        for world in sorted(WORLDS):
            ref = run("organism", world, seed, 12, ledger=MemoryLedger(), trace=True)
            rng = random.Random(f"{seed}|{world}|K07")
            ticks, ends = rng.sample(range(len(ref["trace"])), 2), rng.sample(range(12), 2)
            res = supervised_run("organism", world, seed, 12, kill_committed=ticks, kill_end_committed=ends)
            kills += len(res["deaths"])
            for k in replays:
                replays[k] += res["replays"][k]
            if (any(d["exit"] != -9 for d in res["deaths"]) or res["replays"] != {"step": 2, "end": 2}
                    or res["trace"] != ref["trace"] or res["head"] != ref["head"]):
                failures.append(f"{world}/seed{seed}: replays {res['replays']}")
    return {"verdict": "HOLDS" if not failures else "FAILS", "robust": True, "sigkills": kills,
            "replays": replays, "failures": failures,
            "summary": f"{kills} SIGKILLs after durable commit; {replays['step']} step and {replays['end']} end "
                       f"resends answered from the ledger; "
                       f"{'all lives byte-identical' if not failures else 'FAILED: ' + failures[0]}"}


CLAIM = Claim(
    id="K07",
    title="Exactly-once: a committed act is never repeated after a crash",
    statement="Killing the worker after a tick or an episode end is durably committed but before its reply is "
              "read, then resending, is answered from the ledger every time (no second act, no second end) and "
              "leaves the life byte-identical to an uninterrupted one.",
    kind="invariant",
    scope="instrument",
    test=Check(exactly_once, seeds=3),
    question="H008",
    extends=("K02",),
    by="pipeline-v2 (v2 review fix)",
    created="2026-10-10",
)
