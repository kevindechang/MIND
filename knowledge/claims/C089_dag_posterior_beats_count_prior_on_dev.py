"""H016 (structure learning, dev prior): the exact posterior over generic graphs beats the approximate count prior, with
the same censor-aware, value-scaled, salience-carried route.

The count prior is the H015 machinery (marginal and pair counts across episodes). The DAG posterior is exact inference
over a fixed hypothesis space. Both are supplied the same facts, the same route, the same censor correction, and the
same salience carry. So the difference is the representation of what the organism knows about the world.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C089",
    title="Exact inference over generic graphs beats the approximate count prior on the dev prior",
    statement="In workshop/dev, the routed organism with the exact DAG posterior earns more mean utility per episode "
              "(second half of a 1500-episode lifetime) than the same routed organism with the approximate count prior, "
              "by more than 0.05.",
    kind="effect",
    scope="L2",
    question="H016",
    about=("causal",),
    depends_on=("C085",),
    extends=("C079", "C080"),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0",
                 b="organism +causal causal.voi=1 causal.source=efference causal.aware=1 causal.value_carry=1 "
                   "policy.bonus=1.0 policy.value_bonus=4.0",
                 metric="utility", direction=">", margin=0.05, seeds=16),
    by="claude-code (H016 session 2026-10-13)",
    created="2026-10-13",
)
