"""When outages are announced, the contextual self-model out-calibrates a per-action success table.

Rival: the transcript rivals forecast with a per-action success table, the
'compact capability table' that tied v1's hand-written self-model in all 72
cases of the PR #15 audit. Here the self-model must earn its keep on a
learning task, scored by Brier against real outcomes.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C007",
    title="The self-model out-calibrates a success table when events are informative",
    statement="In outage/dev, the organism's confidence has a Brier score at least 0.01 lower than the "
              "per-action success-table forecasts of the reactive rival.",
    kind="effect",
    scope="L2",
    question="H002",
    about=("self_model",),
    depends_on=("K03",),
    test=Compare(world="outage", a="organism", b="rival:reactive", metric="brier",
                 direction="<", margin=0.01, seeds=16),
    by="pipeline-v2",
    retired='v2 review (2026-10-10): the test compares Brier scores of two agents on their OWN action streams, which confounds calibration with behaviour (13-22% of the gap was action mix). Its conclusion survives on a common stream; superseded by C017, which compares both forecasters on the same events.',
    created="2026-10-10",
)
