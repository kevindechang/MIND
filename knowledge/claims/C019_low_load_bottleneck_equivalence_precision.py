"""Higher-precision successor to C006: low-load workspace equivalence.

C006 was inconclusive on the FIRST sealed held-out test: paired mean kept-rate
difference (capacity 4 minus unlimited) -0.03125 with a 95% interval
[-0.18387, +0.12137], which is not wholly inside the predeclared +/-0.12
equivalence band. The dev interval was [-0.07875, +0.04571]. These are
HISTORICAL observations from C006, not evidence for this successor.

C019 preserves C006's estimand, world, arms, metric and substantive +/-0.12
margin; it changes only the precision budget to 128 independent, paired
lifetimes, explicitly fixing the existing world default of 300 episodes.
The larger n was selected using C006's *previously revealed* held-out
variance for sample-size planning. Under an ideal normal, independent-seed
approximation (estimated SD 0.286), expected 95% interval half-width is
about 0.050 and approximate equivalence power is 0.94 if the true
difference is -0.031. Those prospective numbers are NOT a test result.
The engine's actual conservative bootstrap/t interval decides.

Strongest rival: rival:flat is the same organism with unlimited workspace,
not a separate hand-coded controller. BOTH arms are paired on each world
seed. The criterion is equivalence, not failure to find a difference.
The claim may HOLDS, INCONCLUSIVE or FAILS, and any result must be recorded.
No simulator code or other claim is modified. The first held-out record of
this new sealed claim is decisive for its preregistration status.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C019",
    title="Low-load workspace bottleneck is equivalent to unlimited access (high precision)",
    statement="In vigil/dev with two noise features, over 300 episodes per life, "
              "the four-slot and unlimited workspaces differ in kept rate by "
              "less than 0.12 in either direction over 128 paired lifetimes.",
    kind="equivalence",
    scope="L2",
    question="H003",
    extends=("C006", "C005"),
    test=Compare(
        world="vigil",
        a="organism",
        b="rival:flat",
        metric="kept",
        direction="~",
        margin=0.12,
        seeds=128,
        episodes=300,
        variant="dev",
    ),
    by="ChatGPT GPT-6 (self-authored; not independent replication)",
    created="2026-10-11",
)
