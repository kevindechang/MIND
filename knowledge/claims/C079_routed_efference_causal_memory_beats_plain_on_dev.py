"""H015 (behaviour): a causal memory fed by an efference record, with value-of-information probing routed to action,
raises utility over the plain organism on the dev prior.

Mechanism, as built (mind/organs/causal.py, mind/organs/policy.py): the causal organ learns reach sets from its own
probe observations outside the workspace (`source=efference`), keeps counts of them across episodes as a prior,
proposes the most valuable probe when its expected gain exceeds the probe cost (`voi=1`), and that proposal adds a
bonus to the value of the named action (`policy.bonus=1.0`). Supplied payoff model: the XOR composition, penalty and
probe cost are the workshop's scoring rule (see C070).
Design choices made on dev seeds 0-7 before registration: bonus 1.0 (checked at 0.5 and 2.0: same ordering), salience
2.0, cost 0.25 (the workshop's probe cost), smoothing 1.0. Held-out seeds come from the drand beacon.
Strongest simpler rival: the same organism without the routing bonus (C081) and the compact facts-only rival.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C079",
    title="A routed, efference-fed causal memory raises utility over the plain organism",
    statement="In workshop/dev, the organism with the efference-fed causal organ, value-of-information probing and the "
              "routing bonus earns more mean utility per episode (second half of a 1500-episode lifetime) than the plain "
              "organism, by more than 0.15.",
    kind="effect",
    scope="L2",
    question="H015",
    about=("causal",),
    extends=("C011", "C012", "C070"),
    test=Compare(world="workshop", a="organism +causal causal.voi=1 causal.source=efference policy.bonus=1.0",
                 b="organism", metric="utility", direction=">", margin=0.15, seeds=16),
    by="claude-code (H015 session 2026-10-13)",
    created="2026-10-13",
)
