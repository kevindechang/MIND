"""H004 preregistration: an added recurrent state must improve long-gap commitment retention.

Strong counterfactual control: the identical organism without recurrence.
The long-history transcript zoo challenges whether recurrence is needed at all.
Failure or inconclusive results must remain registered, not rationalised away.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C021",
    title="Recurrent trace improves long-gap commitment retention",
    statement="In vigil/long, adding the bounded recurrent trace increases kept "
              "commitments by more than 0.05 against the same organism without it.",
    kind="effect",
    scope="L2",
    question="H004",
    about=("recurrent",),
    extends=("C003",),
    test=Compare(world="vigil", a="organism +recurrent", b="organism",
                 metric="kept", direction=">", margin=0.05, seeds=16,
                 episodes=300, variant="long"),
    by="h004-recurrence-sprint",
    created="2026-10-11",
    rationale="An additive causal effect would support useful maintained-state "
              "access, not consciousness. Goals already retain requests, so a "
              "negative or inconclusive result is plausible.",
)
