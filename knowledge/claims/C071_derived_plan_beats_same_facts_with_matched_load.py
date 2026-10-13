"""H001 (representation): the derived plan recommendation beats the same recalled facts with matched load.

`causal.derive=0` keeps the causal organ's facts, timing, channel and workspace load. It proposes a constant
`pad` where `best` would be, so the only difference is the derived plan. Both arms are fed the same attended
probe results and the same commitments. Supplied payoff model: see C070.
Strongest simpler rival: this one, rival:compact.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C071",
    title="The derived plan recommendation beats the same recalled facts with matched load",
    statement="In workshop/dev, the organism with the causal organ earns more mean utility per episode over the second half of a 1500-episode lifetime than the same "
              "organism with causal.derive=0, by more than 0.10.",
    kind="effect",
    scope="L2",
    question="H001",
    about=("causal",),
    test=Compare(world="workshop", a="organism +causal", b="organism +causal causal.derive=0", metric="utility",
                 direction=">", margin=0.10, seeds=16),
    by="claude-code (H001 session 2026-10-12)",
    created="2026-10-12",
)
