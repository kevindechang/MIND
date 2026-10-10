"""...and also when outages are silent: the earlier 'tie' was an action-mix artifact.

Successor of C008 (retired). Reverses its interpretation: C008 read a cross-agent
Brier tie as "a success table suffices without announcements". Scored on the same
events, the contextual self-model is still better (its context includes the
organism's recalled results and its own surprise signals).
"""
from mind.claims import Claim, Threshold

CLAIM = Claim(
    id="C018",
    title="Self-model beats a success table on the same events, even when outages are silent",
    statement="In outage/silent, scored on the organism's own events, the self-model's Brier score is lower than a "
              "per-action success table's by at least 0.004.",
    kind="threshold",
    scope="L2",
    question="H002",
    depends_on=("K08",),
    extends=("C008", "C017"),
    test=Threshold(world="outage", arm="organism", metric="calib_gain", op=">=", value=0.004, seeds=16,
                   variant="silent"),
    by="pipeline-v2 (v2 review fix)",
    created="2026-10-10",
)
