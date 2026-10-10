"""Memory, built for continuity, improves tool control when outages are silent (cross-function).

Remembering `was:result=scan:fail` keeps the organism on the manual route while
the sensor is likely still down. Rivals: transcript windows hold the same raw
results for 4-8 ticks; if one ties, memory's advantage here is just recency.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C009",
    title="Memory improves control of an unreliable tool (off-home effect)",
    statement="In outage/silent, removing memory lowers reward per episode by more than 0.5.",
    kind="effect",
    scope="L2",
    question="H007",
    about=("memory",),
    depends_on=("K03",),
    test=Compare(world="outage", a="organism", b="organism -memory", metric="reward",
                 direction=">", margin=0.5, seeds=16, variant="silent"),
    by="pipeline-v2",
    created="2026-10-10",
)
