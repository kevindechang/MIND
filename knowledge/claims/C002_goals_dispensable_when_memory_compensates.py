"""With a short gap, ablating goals changes nothing: memory takes over.

A v1-style single lesion ("Day 4: remove goals") would report NO effect here and
conclude goals are useless. C003 shows the opposite in vigil/long, and C004 shows
why: memory and goals are degenerate (mutually redundant). Necessity is a property
of an organ IN a world, which is why every lesion must be run across the suite.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C002",
    title="Goals are dispensable on short gaps (memory compensates)",
    statement="In vigil/dev, the organism without its goals organ keeps commitments at the same rate as the "
              "intact organism, within ±0.12.",
    kind="equivalence",
    scope="L2",
    question="H007",
    extends=("C001",),
    test=Compare(world="vigil", a="organism", b="organism -goals", metric="kept",
                 direction="~", margin=0.12, seeds=16),
    by="pipeline-v2",
    created="2026-10-10",
)
