"""H001 (access): the policy depends on the causal organ's contents, not only on its presence.

`cut:causal>policy` keeps the organ in the workspace competition but withholds all of its contents (facts,
recommendation and pad) from the policy. This is an access lesion. It does not isolate the recommendation:
C071 does that. Supplied payoff model: see C070.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C072",
    title="Withholding the causal organ's contents from the policy costs utility",
    statement="In workshop/dev, the organism with the causal organ earns more mean utility per episode over the second half of a 1500-episode lifetime than the same "
              "organism with cut:causal>policy, by more than 0.10.",
    kind="effect",
    scope="L2",
    question="H001",
    about=("causal",),
    test=Compare(world="workshop", a="organism +causal", b="organism +causal cut:causal>policy", metric="utility",
                 direction=">", margin=0.10, seeds=16),
    by="claude-code (H001 session 2026-10-12)",
    created="2026-10-12",
)
