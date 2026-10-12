"""H015 (the workspace biases learning): with the routing bonus on, the causal memory fed by an efference record
beats the same memory fed only by attended probe results.

Exploration on dev (not evidence): attention admitted 67 of 590 node-0 probe results to the learned prior (11%), and
the learned distribution of reach sets was 0.108 away from the truth in total variation. The efference record learned
308 of 329 results and was 0.021 away. A learned world model should not depend on which results won a slot.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C080",
    title="Learning from an efference record beats learning from attended results, when routed",
    statement="In workshop/dev, the routed organism that learns from its efference record earns more mean utility per "
              "episode (second half of a 1500-episode lifetime) than the same routed organism that learns only from "
              "attended probe results, by more than 0.15.",
    kind="effect",
    scope="L2",
    question="H015",
    about=("causal",),
    depends_on=("C079",),
    test=Compare(world="workshop", a="organism +causal causal.voi=1 causal.source=efference policy.bonus=1.0",
                 b="organism +causal causal.voi=1 policy.bonus=1.0", metric="utility", direction=">", margin=0.15,
                 seeds=16),
    by="claude-code (H015 session 2026-10-13)",
    created="2026-10-13",
)
