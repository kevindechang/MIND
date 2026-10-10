"""E001 v0.4 (v1): an adaptive second probe is worth exactly 7/120 in the reference setting.

This dynamic program is the engine of the workshop world's exact optimum (K04
depends on it), so if it broke, every regret number in v2 would go STALE.
"""
from mind.claims import Check, Claim


def gain(ctx):
    from fractions import Fraction as F
    from mind.legacy import instrument
    v04 = instrument("e001_finite_policy_v04")
    C = ((2, 1, 2), (0, 1, 8), (1, 1, 2))
    P = (1, 1, 1, 2, 1, 2, 2, 2)
    Z = ((F(0),) * 3,) * 8
    v = {b: v04.policy(P, C, Z, deadline=2, budget=b, cost=F(1, 10), delays=(1,)) for b in (0, 1, 2)}
    ok = (v[0][0] == -F(7, 3) and v[1][0] == -F(121, 60) and v[2][0] == -F(47, 24)
          and v[2][0] - v[1][0] == F(7, 120) and v[2][1] == (("PROBE", 0, 1),))
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True,
            "summary": f"values: none {v[0][0]}, one probe {v[1][0]}, two {v[2][0]}; "
                       f"adaptive gain {v[2][0] - v[1][0]}"}


CLAIM = Claim(
    id="L06",
    title="E001: the adaptive second probe is worth exactly 7/120",
    statement="With commitments ((2,1,2),(0,1,8),(1,1,2)), prior (1,1,1,2,1,2,2,2), deadline 2, delay 1 and "
              "probe cost 1/10, the optimal values are -7/3 (no probe), -121/60 (one), -47/24 (two).",
    kind="fact",
    scope="instrument",
    test=Check(gain),
    question="H001",
    extends=("experiments/instruments/e001_finite_policy_v04.py",
             "experiments/E001/E001-G0-policy-value-identifiability-v0.4.md"),
    sources=("S017",),
    by="pipeline-v2 migration (v1 author: E001 v0.4)",
    created="2026-10-10",
)
