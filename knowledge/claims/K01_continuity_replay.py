"""Continuity invariant: death at random ticks + ledger-only rebirth = the same life, byte for byte.

This is the guard that makes the whole pipeline compound safely. Any future organ
that keeps state outside the event-sourced fold (hidden caches, wall-clock,
set-iteration order, unlogged randomness) breaks this claim immediately, in
every world and under every lesion type.
"""
from mind.claims import Check, Claim

CONFIGS = ("organism", "organism -memory", "organism -goals", "organism -self_model",
           "organism capacity=inf", "organism cut:memory>policy",
           "organism shuffle:memory freeze:self_model", "organism @2:-memory")


def continuity(ctx):
    import random
    from mind.ledger import MemoryLedger
    from mind.runner import run
    from mind.worlds import WORLDS
    lives, deaths, failures = 0, 0, []
    for seed in ctx.seeds:
        for world in sorted(WORLDS):
            for config in CONFIGS:
                ref = run(config, world, seed, 10, ledger=MemoryLedger(), trace=True)
                ticks = len(ref["trace"])
                kills = sorted(random.Random(f"{seed}|{world}|{config}").sample(range(ticks), min(4, ticks)))
                died = run(config, world, seed, 10, kill_at=kills, trace=True)
                lives += 1
                deaths += len(kills)
                if died["trace"] != ref["trace"] or died["head"] != ref["head"]:
                    failures.append(f"{world}/{config}/seed{seed}")
    return {"verdict": "HOLDS" if not failures else "FAILS", "robust": True, "lives": lives,
            "deaths": deaths, "failures": failures[:10],
            "summary": f"{lives} lives, {deaths} deaths: {lives - len(failures)}/{lives} ledgers byte-identical"}


CLAIM = Claim(
    id="K01",
    title="Continuity: any death, any lesion, any world — the same life, byte for byte",
    statement="For every world and lesion family, destroying the organism at random ticks and rebuilding it "
              "from its ledger alone yields an action trace and ledger head hash identical to an "
              "uninterrupted life.",
    kind="invariant",
    scope="instrument",
    test=Check(continuity, seeds=6),
    question="H008",
    extends=("L02",),
    by="pipeline-v2",
    created="2026-10-10",
    rationale="Generalises E100 Day 0 from one stored task to the whole learning organism.",
)
