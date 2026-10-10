"""Fairness guard: stripped to perception + policy, the organism IS the reactive rival.

Every organism-vs-transcript comparison in this repository assumes the rivals use
the same learner, exploration and credit assignment as the organism, so that a
difference can only come from representation (workspace, memory, goals, self-model).
This claim checks that assumption action for action in every world's dev variant,
for the k=1 transcript. Scope (v2 review): it certifies the shared learner, RNG
streams and episode handling, not the window rivals' longer histories and not
forecasters (the success-table forecaster is checked separately: rival:reactive's
calib_gain is exactly 0 by construction, see tests).
"""
from mind.claims import Check, Claim


def identity(ctx):
    from mind.runner import run
    from mind.worlds import WORLDS
    same, total = 0, 0
    for seed in ctx.seeds:
        for world in sorted(WORLDS):
            a = run("organism -memory -goals -self_model", world, seed, 40, trace=True)
            b = run("rival:reactive", world, seed, 40, trace=True)
            total += 1
            same += a["trace"] == b["trace"]
    return {"verdict": "HOLDS" if same == total else "FAILS", "robust": True,
            "summary": f"{same}/{total} lives action-identical"}


CLAIM = Claim(
    id="K03",
    title="Matched learner: the stripped organism is action-identical to rival:reactive",
    statement="With memory, goals and self-model ablated, the organism takes exactly the same actions as the "
              "reactive transcript rival in every world (the workspace never saturates there).",
    kind="invariant",
    scope="instrument",
    test=Check(identity, seeds=8),
    by="pipeline-v2",
    created="2026-10-10",
)
