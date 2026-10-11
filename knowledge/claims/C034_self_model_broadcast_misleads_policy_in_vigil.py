"""Withholding the self-model's broadcast from the policy improves control in vigil (integration cost, H007).

The self-model bids compact self-knowledge into the workspace (`self:<action>=doubt|unsure|sure`,
`surprise=<action>`), and the policy learns from everything that is broadcast. C013
proposed that this advice helps causal control (inconclusive; C035 is its successor). In
vigil, the access lesion that keeps those contents in the workspace but withholds them
from the policy (cut:self_model>policy) RAISES reward: receiving them costs control.

Dev exploration (32 seeds): reward +0.114 [+0.065, +0.164], false starts -0.32, kept +0.07;
vigil/crowded +0.072 [+0.031, +0.112]; vigil/long +0.046 [-0.019, +0.111]. Removing the
self-model outright (-self_model) gives only +0.043 [-0.011, +0.096], because its contents
also occupy workspace slots, and that helps. The margin, 0.03 per episode (about 4% of
the organism's reward), is the smallest cost that matters here. It is not fitted to the
dev estimate.

Mechanism (exploration after sealing, not part of this claim): the cost is mostly not
the content. A sham self-model (shuffle:self_model: the same bids from a random earlier
tick) costs the policy about two thirds as much: cut - sham +0.078 [+0.045, +0.111],
sham - organism +0.036 [-0.015, +0.092] (32 dev seeds). The cost looks like a carry
cost of extra features in a normalised linear learner, like the self-model's own carry
cost for memory's features (C030). See H014.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C034",
    title="Withholding the self-model's broadcast from the policy improves vigil control (integration cost)",
    statement="In vigil/dev, withholding the self-model's broadcast contents from the policy (cut:self_model>policy; "
              "they still occupy workspace slots) raises reward per episode by more than 0.03.",
    kind="effect",
    scope="L2",
    question="H007",
    extends=("C013", "C016"),
    test=Compare(world="vigil", a="organism cut:self_model>policy", b="organism", metric="reward",
                 direction=">", margin=0.03, seeds=32),
    by="claude-code (session 01VdSAnY)",
    created="2026-10-11",
    rationale="Integration can cost as well as help. Global availability of self-knowledge is not free for a "
              "consumer that cannot select its inputs.",
)
