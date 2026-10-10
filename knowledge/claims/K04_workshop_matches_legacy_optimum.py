"""World fidelity: the workshop world + Bayes agent realise the legacy E001 v0.4 optimum.

The v1 dynamic program computes each episode's ex-ante optimal value exactly; the
v2 world simulates episodes. If the world implemented E001 semantics wrongly (or
the oracle wrapper mis-planned — this claim caught exactly such a bug during
construction), simulated regret of the Bayes agent would be biased away from 0.
"""
from mind.claims import Check, Claim


def fidelity(ctx):
    from mind.stats import bootstrap_ci
    parts, ok = [], True
    for variant in ("dev", "skewed", "censored"):
        regrets = ctx.lab.metric("rival:bayes", "workshop", variant, ctx.seeds, 400, "regret@all")
        m, lo, hi = bootstrap_ci(regrets, seed=variant)
        ok = ok and -0.05 < lo and hi < 0.05
        parts.append(f"{variant} {m:+.4f} [{lo:+.4f},{hi:+.4f}]")
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True,
            "summary": "Bayes-agent mean regret vs v0.4 optimum: " + "; ".join(parts)}


CLAIM = Claim(
    id="K04",
    title="The workshop world realises the legacy E001 v0.4 optimum",
    statement="In every workshop variant the Bayes reference agent's mean realised utility equals the v0.4 "
              "dynamic program's ex-ante optimal value within ±0.05 (95% CI).",
    kind="invariant",
    scope="instrument",
    test=Check(fidelity, seeds=12),
    question="H001",
    depends_on=("L06", "L04"),
    extends=("experiments/instruments/e001_finite_policy_v04.py",),
    by="pipeline-v2",
    created="2026-10-10",
)
