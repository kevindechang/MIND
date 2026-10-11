"""Successor of C013: the self-model neither helps nor hurts causal control in the workshop.

C013 claimed that the self-model's broadcast forecasts improve the policy's causal decisions
(margin 0). Its first sealed confirmation was inconclusive. Dev exploration with 32 seeds
puts the whole-organ effect at +0.001 [-0.028, +0.031], and the advice pathway alone
(cut:self_model>policy) at +0.003 [-0.022, +0.028]. An equivalence claim is the sharper
successor. The margin, +/-0.05 utility per episode, is a tenth of the organism's regret to
the Bayes-optimal policy (C012: about 0.5). An effect smaller than that is irrelevant to
the gap H001 asks about.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C035",
    title="The self-model neither helps nor hurts causal control in the workshop (C013 successor)",
    statement="In workshop/dev, the organism with and without its self-model reaches the same mean utility per episode "
              "within +/-0.05 (the whole 95% CI inside the band).",
    kind="equivalence",
    scope="L2",
    question="H007",
    extends=("C013", "C012"),
    test=Compare(world="workshop", a="organism", b="organism -self_model", metric="utility",
                 direction="~", margin=0.05, seeds=32),
    by="claude-code (session 01VdSAnY)",
    created="2026-10-11",
    rationale="Resolves the frontier's inconclusive C013 with a precise null instead of another underpowered effect "
              "test.",
)
