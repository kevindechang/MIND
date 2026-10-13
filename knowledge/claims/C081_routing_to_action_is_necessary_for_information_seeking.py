"""H015 (routing is necessary): the efference-fed value-of-information organism earns more when its probe
recommendation is routed to action (policy.bonus=1.0) than when it is not (policy.bonus=0).

Without the route, the policy learns the value of a probe only from the rare probes it already takes, so the
recommendation changes almost no decisions (exploration on dev: 0.17 probes per episode, regret 0.59).
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C081",
    title="Routing a probe recommendation to action is necessary for information seeking",
    statement="In workshop/dev, the routed efference-fed organism earns more mean utility per episode (second half of a "
              "1500-episode lifetime) than the same organism without the routing bonus, by more than 0.15.",
    kind="effect",
    scope="L2",
    question="H015",
    about=("causal",),
    depends_on=("C079",),
    test=Compare(world="workshop", a="organism +causal causal.voi=1 causal.source=efference policy.bonus=1.0",
                 b="organism +causal causal.voi=1 causal.source=efference", metric="utility", direction=">",
                 margin=0.15, seeds=16),
    by="claude-code (H015 session 2026-10-13)",
    created="2026-10-13",
)
