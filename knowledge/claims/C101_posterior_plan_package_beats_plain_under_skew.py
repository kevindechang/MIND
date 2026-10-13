"""H018 secondary (the skewed boundary against plain).

H015 did not establish a gain under the skewed prior against plain (C084 inconclusive), and C095 showed the learned prior does no
harm there. This claim asks whether the whole package with the plan rule beats plain under skew. It is an
end-to-end comparison; C096-C098 compare the plan rule itself. Secondary: no multiplicity correction.

This compares the complete posterior-plan package against the plain organism, not an isolated plan-rule
intervention. The observed difference includes possible effects of learning, probing and routing; it cannot
establish mediation by the posterior plan rule. C096-C098 isolate the plan-rule configuration change.
about=("causal",) puts the facts-only rival (compact) in the panel. PREREGISTERED then also needs this organism
to beat compact with a bootstrap lower bound above zero. That gate is separate from the primary comparison: if the
comparison holds but compact is not beaten, the claim is reported as blocked by the rival, not refuted.
"""
from mind.claims import Claim, Compare

ARM = ("organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
       "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0 causal.em=1")
PACK = ARM + " causal.posterior_plan=1"

CLAIM = Claim(
    id="C101",
    title="The posterior-plan organism beats the plain organism under the skewed prior",
    statement="In workshop/skewed, the organism that chooses the plan by its posterior expected utility earns "
              "more mean utility per episode (second half of a 1500-episode lifetime) than the plain organism, "
              "by more than 0.10.",
    kind="effect",
    scope="L2",
    question="H018",
    about=("causal",),
    extends=("C084", "C095"),
    test=Compare(world="workshop", a=PACK, b="organism", metric="utility", direction=">", margin=0.10,
                 seeds=16, episodes=1500, variant="skewed"),
    by="claude-code (H018 session 2026-10-13)",
    created="2026-10-13",
)
