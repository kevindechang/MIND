"""Does the announcement-aware table close C017's margin on announced outages?

C017 says the self-model's Brier score beats a per-action success table by at
least 0.008 on the organism's own events in outage/dev. That table ignores
public `alert=down` / `alert=up`. v1 PR #15's event-aware rival reads them.
Here the rival is that same success table, updated by each announcement as one
extra scan observation (down → 0, up → 1) at the table's own rate, scored on
the same events (`calib_gain_alert`). The margin is C017's 0.008: the question
is whether this rival closes that margin, not a new bar fit to a sample.
HOLDS means it does not. REFUTED means the advantage is reliably below 0.008.
INCONCLUSIVE means the interval still covers the margin.
"""
from mind.claims import Claim, Threshold

CLAIM = Claim(
    id="C041",
    title="Announcement-aware table does not close the self-model's same-event margin",
    statement="In outage/dev, on the organism's own events, the self-model's Brier score is lower than an "
              "announcement-updated success table's by at least 0.008.",
    kind="threshold",
    scope="L2",
    question="H002",
    depends_on=("K13",),
    extends=("C017",),
    test=Threshold(world="outage", arm="organism", metric="calib_gain_alert", op=">=", value=0.008, seeds=16),
    by="researcher-bot",
    created="2026-10-11",
    rationale="C017's margin, applied to the stronger same-event scorer H002 names. This organism, outage/dev "
              "only. Not a claim that the self-model is the unique compact explanation, and not L3.",
)
