"""H017 (no loss on the uniform prior): the learned structure prior does not lower utility on the dev prior, relative to
the uniform prior, by more than 0.05. A noninferiority claim: it asks whether the probe economy costs anything.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C092",
    title="The learned structure prior does not lower utility on the dev prior",
    statement="In workshop/dev, the organism with the learned structure prior earns mean utility per episode (second half "
              "of a 1500-episode lifetime) no lower than the same organism with the uniform prior by more than 0.05.",
    kind="effect",
    scope="L2",
    question="H017",
    about=(),
    depends_on=("C090",),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0 causal.em=1",
                 b="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0",
                 metric="utility", direction=">", margin=-0.05, seeds=16),
    by="claude-code (H017 session 2026-10-13)",
    created="2026-10-13",
)
