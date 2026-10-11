"""Prospective H011 L1 claim. UNTESTED until dev and sealed held-out runs.

The margin and sample size were frozen in research/h011/protocol.md before
any evaluation. This does not test procedural compilation or SIGKILL recovery.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C024",
    title="Public relational feature improves first-try transfer to unseen glyphs",
    statement="On glyph/dev, adding a public equality feature improves late first-action transfer accuracy over the otherwise identical organism by more than 0.10.",
    kind="effect",
    scope="L1",
    question="H011",
    about=("analogy",),
    depends_on=(),
    test=Compare(world="glyph", a="organism +analogy capacity=inf",
                 b="organism capacity=inf", metric="transfer",
                 direction=">", margin=0.10, seeds=32, episodes=200,
                 variant="dev"),
    by="MIND design sprint (SELF-REVIEW_ONLY)",
    created="2026-10-11",
    rationale="Ten percentage points of binary first-action accuracy is a meaningful predeclared gain; a same-QLearner equality rival can tie or defeat this representational hypothesis.",
)
