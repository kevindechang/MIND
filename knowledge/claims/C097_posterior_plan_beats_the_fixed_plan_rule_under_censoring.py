"""H018 primary (censored probes: a censored probe leaves the plans through its node unknown).

The two configurations differ only in the plan rule. The comparison measures the total effect of that change,
including any learning and probing feedback; it does not measure mediation by the rule. With no known reach fact
the posterior rule falls back to the policy, as the known-plan rule does.
about=("causal",) puts the facts-only rival (compact) in the panel. PREREGISTERED then also needs this organism
to beat compact with a bootstrap lower bound above zero. That gate is separate from the primary comparison: if the
comparison holds but compact is not beaten, the claim is reported as blocked by the rival, not refuted.
"""
from mind.claims import Claim, Compare

ARM = ("organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
       "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0 causal.em=1")
PACK = ARM + " causal.posterior_plan=1"

CLAIM = Claim(
    id="C097",
    title="The posterior plan rule beats the known-plan rule under censored probes",
    statement="In workshop/censored, the organism that chooses the plan by its expected utility under the DAG "
              "posterior earns more mean utility per episode (second half of a 1500-episode lifetime) than the "
              "same organism that chooses among fully known plans, by more than 0.10.",
    kind="effect",
    scope="L2",
    question="H018",
    about=("causal",),
    extends=("C083", "C093"),
    test=Compare(world="workshop", a=PACK, b=ARM, metric="utility", direction=">", margin=0.10,
                 seeds=16, episodes=1500, variant="censored"),
    by="claude-code (H018 session 2026-10-13)",
    created="2026-10-13",
)
