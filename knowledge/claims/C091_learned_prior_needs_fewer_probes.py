"""H017 (probe economy): with the learned structure prior the organism buys fewer probes per episode than with the uniform
prior, on the same route. The measure is the number of probes, not utility, so it isolates what the prior does to
information seeking. Expected reason: the uniform prior keeps node 2 uncertain (it can have outgoing edges in the 25 DAGs),
and the organism probes it, although in the world node 2 is always a sink.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C091",
    title="The learned structure prior reduces probes per episode",
    statement="In workshop/dev, the organism with the learned structure prior buys fewer probes per episode (mean over "
              "the second half of a 1500-episode lifetime) than the same organism with the uniform prior, by more than 0.10.",
    kind="effect",
    scope="L2",
    question="H017",
    about=(),
    depends_on=("C090",),
    test=Compare(world="workshop",
                 a="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0 causal.em=1",
                 b="organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
                   "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0",
                 metric="probes", direction="<", margin=0.10, seeds=16),
    by="claude-code (H017 session 2026-10-13)",
    created="2026-10-13",
)
