"""H016 (behaviour, dev prior): exact inference over generic causal graphs, routed to action, raises utility over the
plain organism on the uniform dev prior.

Mechanism (mind/organs/causal.py `hypotheses=dag`, `aware=1`, `value_carry=1`; mind/organs/policy.py `value_bonus`): the
organ keeps the exact posterior over all 25 labelled directed acyclic graphs on its three nodes (a generic hypothesis
space, uniform prior, not the workshop's eight forward graphs), computes the one-step value of each probe, discounts it
by the censor rate it has learned from its own probe results, and carries the net value as the probe proposal's
salience. The policy adds 4 x net value to the probe's action (value_bonus 4.0 times salience over VALUE_SALIENCE 4.0).
Supplied payoff model: the reach semantics (toggling a node flips the nodes it reaches), the XOR composition, the
penalty and the probe cost are the workshop's rule. The organ does not know the eight graphs.
Design choices made on dev seeds 0-7 before registration: value_bonus 4.0 (chosen over the unscaled route, value_bonus 0,
not tuned further), censor-aware value, salience carry. Held-out seeds come from the drand beacon.
Exploration on dev seeds 0-7 (not evidence): regret 0.27 against 0.56 for the plain organism, and utility -1.39 against -1.68.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C085",
    title="Exact inference over generic graphs, routed to action, raises utility over the plain organism",
    statement="In workshop/dev, the routed organism with the exact DAG posterior earns more mean utility per episode "
              "(second half of a 1500-episode lifetime) than the plain organism, by more than 0.15.",
    kind="effect",
    scope="L2",
    question="H016",
    about=("causal",),
    extends=("C079", "C012"),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0",
                 b="organism", metric="utility", direction=">", margin=0.15, seeds=16),
    by="claude-code (H016 session 2026-10-13)",
    created="2026-10-13",
)
