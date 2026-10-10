"""Without distractor load the bottleneck neither helps nor hurts.

Paired with C005: the bottleneck's value is conditional on interference, which
is the falsifiable shape of H003. (An earlier 4-seed pilot suggested the
bottleneck HURTS on long gaps; 12 dev seeds did not support that, so it was not
registered. It remains an open thread in H003.)
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C006",
    title="Without distractors the bottleneck is neutral",
    statement="In vigil/dev (2 distractors), the 4-item workspace and the unlimited workspace keep "
              "commitments at the same rate within ±0.12.",
    kind="equivalence",
    scope="L2",
    question="H003",
    extends=("C005",),
    test=Compare(world="vigil", a="organism", b="rival:flat", metric="kept",
                 direction="~", margin=0.12, seeds=16),
    by="pipeline-v2",
    created="2026-10-10",
)
