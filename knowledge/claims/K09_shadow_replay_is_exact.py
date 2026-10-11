"""Instrument: the shadow self-model replayed from a life's ledger IS the organism's self-model.

mind/shadow.py re-runs the self-model's learning on the logged broadcasts so that a
consumer's informational dependence on one organ can be measured while behaviour is held
fixed (C030, C032, C033). That is only meaningful if the unfiltered shadow is the
organism's own self-model, bit for bit: the same confidence at every forecast, the same late
Brier and table Brier as the runner, and a life lived with a ledger identical to the lab's
life for the same arm and seed. Covers cuts to and from the self-model, a parameter change,
the flat workspace and an organism-configured rival, in every world and every variant.
"""
from mind.claims import Check, Claim

CONFIGS = ("organism", "organism -memory", "organism -goals", "organism cut:memory>self_model",
           "organism cut:perception>self_model cut:self_model>*", "organism capacity=inf",
           "organism self_model.lr=0.3", "rival:flat")
EPISODES = 80


def exact(ctx):
    from mind.shadow import fixed_behaviour_many
    from mind.worlds import WORLDS
    lives, failures = 0, []
    for world in sorted(WORLDS):
        for variant in WORLDS[world].variants:
            for config in CONFIGS:
                shadows = fixed_behaviour_many(ctx.lab, config, world, variant, ctx.seeds, EPISODES)
                lab = ctx.lab.runs([(config, world, variant, s, EPISODES) for s in ctx.seeds])
                for r, ref in zip(shadows, lab):
                    lives += 1
                    if not (r["exact"] and r["brier"] == r["metrics"]["brier"]
                            and r["brier_table"] == r["metrics"]["brier_table"]
                            and r["metrics"] == ref["metrics"]):
                        failures.append(f"{world}/{variant}/{config}/seed{r['seed']}")
    return {"verdict": "HOLDS" if not failures else "FAILS", "robust": True, "lives": lives,
            "failures": failures[:10],
            "summary": f"{lives} lives, every world and variant: {lives - len(failures)}/{lives} shadows reproduce "
                       f"every logged confidence, the runner's Brier and table Brier, and the lab's life"}


CLAIM = Claim(
    id="K09",
    title="Shadow replay: the self-model re-run from the ledger is the organism's own, bit for bit",
    statement="For every world and variant and for intact, lesioned, cut, re-parameterised and flat organisms, the "
              "unfiltered shadow self-model reproduces every logged confidence exactly, its late Brier and table "
              "Brier equal the runner's, and the life lived with a ledger is identical to the lab's life.",
    kind="invariant",
    scope="instrument",
    test=Check(exact, seeds=4),
    question="H007",
    extends=("K01", "K08"),
    by="claude-code (session 01VdSAnY)",
    created="2026-10-11",
    rationale="Fixed-behaviour estimands are only as good as the replay they rest on.",
)
