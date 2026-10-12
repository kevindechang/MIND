"""H015 (distance to the ceiling): the routed efference organism gets within 0.42 regret of the v0.4 Bayes optimum.

The plain organism's regret is about 0.56 on the same seeds (C012 measures the same quantity). 0.42 is three
quarters of that, so the claim asks for a quarter of the gap closed. The Bayes reference (`rival:bayes`) uses the
family of graphs and the adaptive value of information, which this organism does not have; this claim asks how far a
learned version gets.
"""
from mind.claims import Claim, Threshold

CLAIM = Claim(
    id="C082",
    title="The routed efference organism closes a quarter of the gap to the Bayes optimum",
    statement="In workshop/dev, after 1500 episodes the routed efference organism's mean regret against the v0.4 "
              "optimum is at most 0.42 utility per episode (three quarters of the plain organism's regret).",
    kind="threshold",
    scope="L2",
    question="H015",
    about=("causal",),
    depends_on=("C079",),
    extends=("C012",),
    test=Threshold(world="workshop",
                   arm="organism +causal causal.voi=1 causal.source=efference policy.bonus=1.0",
                   metric="regret", op="<=", value=0.42, seeds=16),
    by="claude-code (H015 session 2026-10-13)",
    created="2026-10-13",
)
