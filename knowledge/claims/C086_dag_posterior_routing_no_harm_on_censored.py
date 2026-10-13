"""H016 (robustness, censored probes): the generic DAG posterior, routed to action, does not change utility against the
plain organism when half the probes come back censored. An equivalence claim: the difference must lie within 0.05.

H015 showed that the routed package with a fixed bonus and an approximate count prior loses about 0.08 utility here
(C083, refuted). The claim asks whether exact inference, with a censor-aware value, removes that harm.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C086",
    title="The generic DAG posterior does no harm under censored probes",
    statement="In workshop/censored, the routed organism with the exact DAG posterior and the plain organism earn "
              "mean utility per episode (second half of a 1500-episode lifetime) that differ by less than 0.05.",
    kind="equivalence",
    scope="L2",
    question="H016",
    about=("causal",),
    depends_on=("C085",),
    extends=("C083",),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0",
                 b="organism", metric="utility", direction="~", margin=0.05, seeds=16, variant="censored"),
    by="claude-code (H016 session 2026-10-13)",
    created="2026-10-13",
)
