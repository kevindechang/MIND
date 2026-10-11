"""H004 cross-world preregistration: general-purpose recurrence in silent outages.

The current action's outcome is never available to the recurrence update;
only the prior action's publicly delivered outcome is incorporated.
The comparison isolates an incremental effect beyond the standing organism.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C022",
    title="Recurrent trace improves reward under silent tool outages",
    statement="In outage/silent, adding the bounded recurrent trace increases "
              "reward per episode by more than 0.10 against the identical "
              "organism without it.",
    kind="effect",
    scope="L2",
    question="H004",
    about=("recurrent",),
    extends=("C021",),
    test=Compare(world="outage", a="organism +recurrent", b="organism",
                 metric="reward", direction=">", margin=0.10, seeds=16,
                 episodes=120, variant="silent"),
    by="h004-recurrence-sprint",
    created="2026-10-11",
    rationale="Transfer to a second world guards against an isolated "
              "commitment-memory trick. It cannot by itself establish a "
              "general-purpose recurrent integration advantage.",
)
