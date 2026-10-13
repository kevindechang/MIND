"""H017 (censored probes): the learned structure prior earns more utility than the uniform prior when half the probes
come back censored. The margin is zero: the claim is the direction, since no scientific threshold for this comparison
was set in advance. H016 found the uniform prior loses to plain under censoring (C086); this asks whether learning the
prior recovers that.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C093",
    title="The learned structure prior earns more than the uniform prior under censored probes",
    statement="In workshop/censored, the organism with the learned structure prior earns more mean utility per episode "
              "(second half of a 1500-episode lifetime) than the same organism with the uniform prior.",
    kind="effect",
    scope="L2",
    question="H017",
    about=(),
    depends_on=("C090",),
    extends=("C086",),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0 causal.em=1",
                 b="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0",
                 metric="utility", direction=">", margin=0.0, seeds=16, variant="censored"),
    by="claude-code (H017 session 2026-10-13)",
    created="2026-10-13",
)
