"""On the SAME events, the self-model is better calibrated than a success table (announced outages).

Successor of C007 (retired: it compared two agents on their own action streams).
calib_gain scores the table rule on the organism's own actions and outcomes and
subtracts the self-model's Brier score, so behaviour cannot masquerade as
calibration. Margin chosen from dev exploration (+0.018) and the review's
re-analysis; held-out seeds are new.
"""
from mind.claims import Claim, Threshold

CLAIM = Claim(
    id="C017",
    title="Self-model beats a success table on the same events (announced outages)",
    statement="In outage/dev, scored on the organism's own events, the self-model's Brier score is lower than a "
              "per-action success table's by at least 0.008.",
    kind="threshold",
    scope="L2",
    question="H002",
    depends_on=("K08",),
    extends=("C007",),
    test=Threshold(world="outage", arm="organism", metric="calib_gain", op=">=", value=0.008, seeds=16),
    by="pipeline-v2 (v2 review fix)",
    created="2026-10-10",
)
