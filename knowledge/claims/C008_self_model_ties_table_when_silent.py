"""When outages are silent, a per-action success table is as calibrated as the self-model.

With C007: the self-model's calibration advantage is entirely attributable to
the information in announcements. A compact rival suffices exactly when the
context carries no extra information — the v1 PR #15 lesson, now on a learner.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C008",
    title="Without announcements, a success table is as calibrated as the self-model",
    statement="In outage/silent, the organism's Brier score equals the reactive rival's success-table Brier "
              "score within ±0.02.",
    kind="equivalence",
    scope="L2",
    question="H002",
    depends_on=("K03",),
    extends=("C007",),
    test=Compare(world="outage", a="organism", b="rival:reactive", metric="brier",
                 direction="~", margin=0.02, seeds=16, variant="silent"),
    by="pipeline-v2",
    retired="v2 review (2026-10-10): the apparent tie was an action-mix artifact (the organism scans more). On the same events the self-model is BETTER than the table even without announcements; the claim's interpretation is reversed. Superseded by C018.",
    created="2026-10-10",
)
