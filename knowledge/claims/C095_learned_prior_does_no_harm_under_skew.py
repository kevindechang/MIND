"""H017 (no harm under the skewed prior, noninferiority): the learned-prior organism is not worse than plain by more than
0.05 under the skewed prior (each edge present with probability 4/5). H016 showed no harm there (C087, confirmed).
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C095",
    title="The learned-prior organism does no harm under the skewed prior",
    statement="In workshop/skewed, the organism with the learned structure prior earns mean utility per episode (second "
              "half of a 1500-episode lifetime) no lower than the plain organism by more than 0.05.",
    kind="effect",
    scope="L2",
    question="H017",
    about=("causal",),
    depends_on=("C090",),
    extends=("C087",),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0 causal.em=1",
                 b="organism", metric="utility", direction=">", margin=-0.05, seeds=16, variant="skewed"),
    by="claude-code (H017 session 2026-10-13)",
    created="2026-10-13",
)
