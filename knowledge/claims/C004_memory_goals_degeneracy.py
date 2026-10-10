"""Memory and goals are degenerate: their joint lesion hurts far more than the sum of singles.

Degeneracy (structurally different parts that can each do a job) is a hallmark
of integrated biological systems and invisible to one-lesion-per-toy designs.
Measured as the interaction loss(both) - loss(memory) - loss(goals) on kept.
"""
from mind.claims import Check, Claim


def degeneracy(ctx):
    from mind.stats import bootstrap_ci
    eps = 300
    arm = lambda cfg: ctx.lab.metric(cfg, "vigil", "dev", ctx.seeds, eps, "kept")
    i, m, g, mg = arm("organism"), arm("organism -memory"), arm("organism -goals"), arm("organism -memory -goals")
    synergy = [(x - z) - (x - a) - (x - b) for x, a, b, z in zip(i, m, g, mg)]
    mean, lo, hi = bootstrap_ci(synergy, seed="C004")
    return {"verdict": "HOLDS" if lo > 0.4 else "FAILS" if hi <= 0.4 else "INCONCLUSIVE", "robust": True,
            "synergy": mean, "lo": lo, "hi": hi,
            "summary": f"interaction {mean:+.3f} [{lo:+.3f}, {hi:+.3f}] (claim: > 0.4)"}


CLAIM = Claim(
    id="C004",
    title="Memory and goals back each other up (degeneracy)",
    statement="In vigil/dev, the loss from removing memory and goals together exceeds the sum of the losses "
              "from removing each alone by more than 0.4 (kept rate).",
    kind="effect",
    scope="L2",
    question="H007",
    extends=("C001", "C002"),
    test=Check(degeneracy, seeds=16),
    by="pipeline-v2",
    created="2026-10-10",
)
