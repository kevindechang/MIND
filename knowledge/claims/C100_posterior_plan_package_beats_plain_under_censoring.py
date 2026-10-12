"""H018 secondary (the censored boundary against plain).

H015 to H017 found no gain under censored probes against the plain organism (C083 refuted, C086 not confirmed,
C093 inconclusive). This claim asks whether the whole package with the plan rule beats plain there. It is an
end-to-end comparison, so other components can account for a gain; C096-C098 compare the plan rule itself.
Secondary: no multiplicity correction.

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
    id="C100",
    title="The posterior-plan organism beats the plain organism under censored probes",
    statement="In workshop/censored, the organism that chooses the plan by its posterior expected utility earns more "
    "mean utility per episode (second half of a 1500-episode lifetime) than the plain organism, by more than "
    "0.10.",
    kind="effect",
    scope="L2",
    question="H018",
    about=("causal",),
    extends=("C083", "C086", "C093"),
    test=Compare(world="workshop", a=PACK, b="organism", metric="utility", direction=">", margin=0.10,
                 seeds=16, episodes=1500, variant="censored"),
    by="claude-code (H018 session 2026-10-13)",
    created="2026-10-13",
)
