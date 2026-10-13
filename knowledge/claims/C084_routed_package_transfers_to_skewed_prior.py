"""H015 (boundary, transfer): the routed efference organism beats the plain organism under the skewed prior (each
edge present with probability 4/5).

Exploration on dev (not evidence): the plain organism already does well under the skewed prior (regret 0.34), so the
room for gain is small. Registered as a boundary, not as a hoped-for success.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C084",
    title="The routed efference organism beats the plain organism under the skewed prior",
    statement="In workshop/skewed, the routed efference organism earns more mean utility per episode (second half of a "
              "1500-episode lifetime) than the plain organism, by more than 0.10.",
    kind="effect",
    scope="L2",
    question="H015",
    about=("causal",),
    depends_on=("C079",),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference policy.bonus=1.0",
                 b="organism", metric="utility", direction=">", margin=0.10, seeds=16, variant="skewed"),
    by="claude-code (H015 session 2026-10-13)",
    created="2026-10-13",
)
