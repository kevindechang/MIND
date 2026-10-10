"""The self-model's broadcast forecasts improve the policy's causal decisions (metacognition → control).

Not designed in: the self-model only predicts its own success. But its contents
(e.g. `self:do:01=doubt` in the current context) are globally available, and the
policy learns to use them as advice. An L2 integration pathway found by the atlas.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C013",
    title="Self-knowledge improves causal decisions (cross-function)",
    statement="In workshop/dev, removing the self-model lowers mean utility (reliably > 0).",
    kind="effect",
    scope="L2",
    question="H007",
    about=("self_model",),
    test=Compare(world="workshop", a="organism", b="organism -self_model", metric="utility",
                 direction=">", margin=0.0, seeds=16),
    by="pipeline-v2",
    created="2026-10-10",
)
