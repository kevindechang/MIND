"""H001 (sham control): the content of the recommendation matters, not only its presence and timing.

`causal.sham=1` keeps every emission at the same ticks with the same facts, load and salience, and replaces
only the recommended plan with a random legal plan. Supplied payoff model: see C070.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C073",
    title="The recommended plan's content matters beyond a matched random plan",
    statement="In workshop/dev, the organism with the causal organ earns more mean utility per episode over the second half of a 1500-episode lifetime than the same "
              "organism with causal.sham=1, by more than 0.10.",
    kind="effect",
    scope="L2",
    question="H001",
    about=("causal",),
    test=Compare(world="workshop", a="organism +causal", b="organism +causal causal.sham=1", metric="utility",
                 direction=">", margin=0.10, seeds=16),
    by="claude-code (H001 session 2026-10-12)",
    created="2026-10-12",
)
