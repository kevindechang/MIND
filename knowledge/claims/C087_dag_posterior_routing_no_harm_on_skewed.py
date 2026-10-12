"""H016 (robustness, skewed prior): the generic DAG posterior, routed to action, does not change utility against the
plain organism under the skewed prior (each edge present with probability 4/5). An equivalence claim within 0.05.

H015 registered the skewed prior as a boundary (C084, not confirmed). The claim asks whether exact inference removes the
small loss that the approximate count prior showed here.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C087",
    title="The generic DAG posterior does no harm under the skewed prior",
    statement="In workshop/skewed, the routed organism with the exact DAG posterior and the plain organism earn mean "
              "utility per episode (second half of a 1500-episode lifetime) that differ by less than 0.05.",
    kind="equivalence",
    scope="L2",
    question="H016",
    about=("causal",),
    depends_on=("C085",),
    extends=("C084",),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0",
                 b="organism", metric="utility", direction="~", margin=0.05, seeds=16, variant="skewed"),
    by="claude-code (H016 session 2026-10-13)",
    created="2026-10-13",
)
