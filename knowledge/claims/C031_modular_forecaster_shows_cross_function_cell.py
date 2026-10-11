"""The atlas's cross-function signature appears in a modular forecaster (instrument validity, H007).

If a self-model that receives NOTHING from other organs still "gains calibration" from
goals in the atlas's sense, then a reliable lesion effect on calib_gain cannot by itself
show that the self-model uses other organs' contents. Here the self-model is cut off
from perception, memory and goals (it sees only its own actions and their public
outcomes), and its own contents reach no organ. Lesioning goals can then change only what
the organism does, and so the events on which the self-model and the success table are
compared.

Dev exploration (32 seeds): +0.008 [+0.005, +0.011]; memory gives +0.006 [+0.003, +0.009],
and goals in vigil/long +0.010. The atlas sees this with 12 seeds only when the effect is
larger, but its criterion (a reliable off-home lesion effect) does not exclude it. The
fixed-behaviour estimand that does is C032; the decomposition of C016's own cells is C030.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C031",
    title="A modular self-model shows the atlas's cross-function calibration cell",
    statement="In vigil/dev, with the self-model informationally isolated (no contents from perception, memory or "
              "goals reach it, and its own reach no organ), lesioning goals still lowers same-event calibration gain "
              "reliably (> 0): a modular forecaster meets the atlas's cross-function criterion through behaviour "
              "alone.",
    kind="effect",
    scope="instrument",
    question="H007",
    depends_on=("K08",),
    extends=("C016",),
    test=Compare(world="vigil",
                 a="organism cut:perception>self_model cut:memory>self_model cut:goals>self_model cut:self_model>*",
                 b="organism -goals cut:perception>self_model cut:memory>self_model cut:self_model>*",
                 metric="calib_gain", direction=">", margin=0.0, seeds=32),
    by="claude-code (session 01VdSAnY)",
    created="2026-10-11",
    rationale="Any measure meant to show that one organ's contents reach another must read zero for a forecaster "
              "built to receive none. This is that negative control in this organism; the atlas's calibration "
              "column fails it.",
)
