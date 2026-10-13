"""H016 (calibration, censored probes): the generic DAG posterior with a censor-aware, value-scaled route beats H015's
fixed-bonus package on censored probes by more than 0.05.

This is the calibration claim: the same routed organism, with its value estimate calibrated to the observation model.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C088",
    title="A calibrated, exact-posterior route beats the fixed route on censored probes",
    statement="In workshop/censored, the routed organism with the exact DAG posterior, a censor-aware value and a "
              "value-scaled route earns more mean utility per episode (second half of a 1500-episode lifetime) than the "
              "H015 routed organism with a fixed bonus, by more than 0.05.",
    kind="effect",
    scope="L2",
    question="H016",
    about=("causal",),
    depends_on=("C079",),
    extends=("C083",),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0",
                 b="organism +causal causal.voi=1 causal.source=efference policy.bonus=1.0",
                 metric="utility", direction=">", margin=0.05, seeds=16, variant="censored"),
    by="claude-code (H016 session 2026-10-13)",
    created="2026-10-13",
)
