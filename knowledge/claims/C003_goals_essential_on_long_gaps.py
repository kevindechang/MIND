"""On long gaps, goals become essential: decaying memories lose the workspace competition.

Together with C002 this is a context-dependent necessity: the same organ is
redundant in one world and indispensable in another.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C003",
    title="Goals are essential on long gaps",
    statement="In vigil/long (bell 9-16 ticks after the request), removing goals lowers kept commitments by "
              "more than 0.3.",
    kind="effect",
    scope="L2",
    question="H007",
    about=("goals",),
    depends_on=("K03",),
    extends=("C002",),
    test=Compare(world="vigil", a="organism", b="organism -goals", metric="kept",
                 direction=">", margin=0.3, seeds=16, variant="long"),
    by="pipeline-v2",
    created="2026-10-10",
)
