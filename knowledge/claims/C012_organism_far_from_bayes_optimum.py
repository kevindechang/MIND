"""The organism stays far from the E001 Bayes optimum: it does not discover the value of probing.

Regret is measured per episode against the legacy v0.4 dynamic program (K04),
which probes on ~54% of episodes; the organism probes on ~16% and plans worse.
A negative result that defines the target for H001.
"""
from mind.claims import Claim, Threshold

CLAIM = Claim(
    id="C012",
    title="The organism remains far from the Bayes-optimal causal policy",
    statement="In workshop/dev, after 1500 episodes the organism's mean regret against the v0.4 optimum is "
              "at least 0.3 utility per episode.",
    kind="threshold",
    scope="L2",
    question="H001",
    depends_on=("K04",),
    extends=("L06",),
    test=Threshold(world="workshop", arm="organism", metric="regret", op=">=", value=0.3, seeds=16),
    by="pipeline-v2",
    created="2026-10-10",
)
