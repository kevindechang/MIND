"""...but memory slightly degrades the self-model's calibration in the same world (interference).

Memory's contents enter the shared broadcast, so the self-model fits its success
forecasts on more, noisier context. Integration cuts both ways: the same
pathway that helps control (C009) costs metacognitive precision. A finding about
side effects, not superiority, so no rival panel applies.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C010",
    title="Memory degrades the self-model's calibration (cross-function interference)",
    statement="In outage/silent, the intact organism's Brier score is higher than the memory-lesioned "
              "organism's by more than 0.003.",
    kind="effect",
    scope="L2",
    question="H007",
    extends=("C009",),
    test=Compare(world="outage", a="organism", b="organism -memory", metric="brier",
                 direction=">", margin=0.003, seeds=16, variant="silent"),
    by="pipeline-v2",
    retired="v2 review (2026-10-10): memory changes the action mix; a context-free table on the same streams shifts as much (+0.011), so this measured behaviour, not 'noisier context'. Inconclusive anyway; no successor yet (open in H007).",
    created="2026-10-10",
)
