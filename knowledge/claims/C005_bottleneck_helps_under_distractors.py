"""A capacity-limited workspace beats unlimited ('flat') access when distractors abound.

H003 / consciousness-prior prediction: broadcasting few contents makes credit
assignment over conjunctions tractable. rival:flat is the identical organism with
capacity=inf, so the comparison isolates the bottleneck itself.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C005",
    title="The workspace bottleneck helps under distractor load",
    statement="In vigil/crowded (5 flickering distractors), the organism with a 4-item workspace keeps more "
              "commitments than the same organism with an unlimited workspace, by more than 0.08.",
    kind="effect",
    scope="L2",
    question="H003",
    about=("workspace",),
    extends=("L03",),
    test=Compare(world="vigil", a="organism", b="rival:flat", metric="kept",
                 direction=">", margin=0.08, seeds=16, variant="crowded"),
    sources=(),
    by="pipeline-v2",
    created="2026-10-10",
)
