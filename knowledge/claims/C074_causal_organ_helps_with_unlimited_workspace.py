"""H001 (diagnostic, no attention limit): the causal organ helps when the workspace is unlimited.

`capacity=inf` removes the workspace bottleneck, so every attended probe result reaches the organ. Any
remaining gap therefore comes from the representation and its one-tick learning lag, not from attention. It
separates the two explanations for a null result in C070. Supplied payoff model: see C070.
Strongest simpler rival: the flat organism itself (rival:flat is the same comparison without the causal organ).
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C074",
    title="With an unlimited workspace the causal organ raises utility over the flat organism",
    statement="In workshop/dev, the organism with the causal organ and an unlimited workspace earns more mean "
              "utility per episode (second half of a 1500-episode lifetime) than the flat organism, by more than 0.10.",
    kind="effect",
    scope="L2",
    question="H001",
    about=("causal",),
    test=Compare(world="workshop", a="organism +causal capacity=inf", b="organism capacity=inf", metric="utility",
                 direction=">", margin=0.10, seeds=16),
    by="claude-code (H001 session 2026-10-12)",
    created="2026-10-12",
)
