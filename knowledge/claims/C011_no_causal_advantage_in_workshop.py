"""In the E001 workshop, the whole organism (workspace, memory, goals, self-model) is no better than a reactive learner.

The plain organism and the reactive rival learn equally well (and equally badly)
to act on hidden causal structure. Whatever H001's 'causal memory' is, the
generic memory organ is not it. This is the honest starting line for a causal organ.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C011",
    title="The organism gives no advantage over a reactive learner at causal probing",
    statement="In workshop/dev, the organism's mean utility equals the reactive rival's within ±0.1.",
    kind="equivalence",
    scope="L2",
    question="H001",
    depends_on=("K03",),
    extends=("L06",),
    test=Compare(world="workshop", a="organism", b="rival:reactive", metric="utility",
                 direction="~", margin=0.1, seeds=16),
    by="pipeline-v2",
    created="2026-10-10",
)
