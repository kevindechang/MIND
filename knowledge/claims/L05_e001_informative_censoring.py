"""E001 v0.3 (v1): a censored probe with NO delivered effect still moves the posterior.

Consequence carried forward: in workshop/censored, "result withheld" is evidence;
an agent that treats censoring as "nothing happened" is miscalibrated by construction.
"""
from mind.claims import Check, Claim


def censoring(ctx):
    from fractions import Fraction as F
    from mind.legacy import instrument
    vs = instrument("e001_three_node_version_space")
    rb = instrument("e001_three_node_robustness")
    pair = (frozenset(), frozenset(((0, 1), (0, 2), (1, 2))))
    hist = vs.make_history((), (vs.PublicProbe(7, 2, 0, 1),), (), (7,), 2)
    informative = rb.conditional_posterior(hist, (F(1, 2), F(1, 2)), ((F(1, 4),) * 3, (F(3, 4),) * 3), pair)
    ignorable = rb.conditional_posterior(hist, (F(1, 2), F(1, 2)), rb.uniform_censor(pair), pair)
    ok = informative == {0: F(1, 4), 1: F(3, 4)} and ignorable == {0: F(1, 2), 1: F(1, 2)}
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True,
            "summary": f"censor rates 1/4 vs 3/4: 1/2:1/2 → {informative[0]}:{informative[1]}; "
                       f"equal rates leave {ignorable[0]}:{ignorable[1]}"}


CLAIM = Claim(
    id="L05",
    title="E001: informative censoring moves belief with no delivered effect",
    statement="With graph-dependent censor rates 1/4 vs 3/4, one censored probe moves the posterior over "
              "{empty, full} from 1/2:1/2 to 1/4:3/4; equal rates leave it at 1/2:1/2.",
    kind="fact",
    scope="instrument",
    test=Check(censoring),
    question="H001",
    extends=("experiments/instruments/e001_three_node_robustness.py",
             "experiments/E001/E001-G0-prior-censoring-robustness-v0.3.md"),
    sources=("S018",),
    by="pipeline-v2 migration (v1 author: E001 v0.3)",
    created="2026-10-10",
)
