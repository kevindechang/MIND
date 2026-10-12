"""H017 (no harm under censored probes, noninferiority): the learned-prior organism is not worse than plain by more than
0.05 when half the probes come back censored. H016's uniform-prior package lost about 0.05 here (C086, not confirmed);
this asks whether learning the prior removes that loss.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C094",
    title="The learned-prior organism does no harm under censored probes",
    statement="In workshop/censored, the organism with the learned structure prior earns mean utility per episode (second "
              "half of a 1500-episode lifetime) no lower than the plain organism by more than 0.05.",
    kind="effect",
    scope="L2",
    question="H017",
    about=("causal",),
    depends_on=("C090",),
    extends=("C086",),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0 causal.em=1",
                 b="organism", metric="utility", direction=">", margin=-0.05, seeds=16, variant="censored"),
    by="claude-code (H017 session 2026-10-13)",
    created="2026-10-13",
)
