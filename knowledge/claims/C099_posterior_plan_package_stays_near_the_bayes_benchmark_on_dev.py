"""H018 secondary (distance to the Bayes-optimal benchmark, dev prior).

Regret is measured against the workshop's Bayes-optimal benchmark: oracle_value, the ex-ante optimum under the true
prior and censor model, computed by the legacy E001 v0.4 dynamic program with the permitted history. The benchmark
does not see the true graph. The bayes rival executes the same policy. A threshold claim has no rival panel
(claims.py rival_panel), so compact cannot block this claim. Secondary: no multiplicity correction; the H018 verdict
rests on C096-C098.
"""
from mind.claims import Claim, Threshold

ARM = ("organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
       "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0 causal.em=1")
PACK = ARM + " causal.posterior_plan=1"

CLAIM = Claim(
    id="C099",
    title="The posterior-plan organism stays within 0.15 of the Bayes-optimal benchmark on the dev prior",
    statement="In workshop/dev, the organism that chooses the plan by its posterior expected utility has mean "
              "regret at most 0.15 utility per episode (second half of a 1500-episode lifetime) against the "
              "Bayes-optimal benchmark, the ex-ante optimum under the true prior and censor model.",
    kind="threshold",
    scope="L2",
    question="H018",
    about=("causal",),
    extends=("C082",),
    test=Threshold(world="workshop", arm=PACK, metric="regret", op="<=", value=0.15, seeds=16,
                   episodes=1500),
    by="claude-code (H018 session 2026-10-13)",
    created="2026-10-13",
)
