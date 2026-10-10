"""E001 v0.3 (v1): with no probes at all, the prior alone flips the optimal plan."""
from mind.claims import Check, Claim


def prior_flip(ctx):
    from fractions import Fraction as F
    from mind.legacy import instrument
    vs = instrument("e001_three_node_version_space")
    rb = instrument("e001_three_node_robustness")
    pair = (frozenset(), frozenset(((0, 1), (0, 2), (1, 2))))
    hist = vs.make_history((vs.PublicCommitment(0, 1, 8), vs.PublicCommitment(2, 1, 8)), (), (), (), 2)
    ign = rb.uniform_censor(pair)
    a = rb.conditional_score(hist, (9, 1), ign, pair)[0]
    b = rb.conditional_score(hist, (1, 9), ign, pair)[0]
    m = rb.robust_score(hist, [(9, 1), (1, 9)], [ign, ign], pair)[:2]
    ok = a == ((0, 2),) and b == ((0,),) and m == (((0,),), -F(41, 5))
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True,
            "summary": f"prior 9:1 → {a}, prior 1:9 → {b}, maximin → {m[0]} at {m[1]}"}


CLAIM = Claim(
    id="L07",
    title="E001: the prior alone flips the optimal plan",
    statement="For commitments (0,1,8),(2,1,8) with no probes, prior 9:1 over {empty, full} selects plan (0,2), "
              "prior 1:9 selects (0,), and the maximin rule over both selects (0,) at -41/5.",
    kind="fact",
    scope="instrument",
    test=Check(prior_flip),
    question="H001",
    extends=("experiments/instruments/e001_three_node_robustness.py",),
    by="pipeline-v2 migration (v1 author: E001 v0.3)",
    created="2026-10-10",
)
