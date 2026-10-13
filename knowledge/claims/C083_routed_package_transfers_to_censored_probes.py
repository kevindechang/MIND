"""H015 (boundary, transfer): the routed efference organism beats the plain organism when half of the probes come back
censored (the held-out variant E001 v0.3 calls informative missingness).

Exploration on dev (not evidence): the routed organism was worse here (regret 0.44 against 0.36). Its value estimate
assumes every probe returns information; a censored probe returns none. This claim is registered so that the limit
is recorded either way.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C083",
    title="The routed efference organism beats the plain organism on censored probes",
    statement="In workshop/censored, the routed efference organism earns more mean utility per episode (second half of a "
              "1500-episode lifetime) than the plain organism, by more than 0.05.",
    kind="effect",
    scope="L2",
    question="H015",
    about=("causal",),
    depends_on=("C079",),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference policy.bonus=1.0",
                 b="organism", metric="utility", direction=">", margin=0.05, seeds=16, variant="censored"),
    by="claude-code (H015 session 2026-10-13)",
    created="2026-10-13",
)
