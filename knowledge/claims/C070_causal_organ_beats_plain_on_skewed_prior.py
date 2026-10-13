"""H001 (behaviour, held-out prior): the causal organ raises utility over the plain organism under a skewed prior.

Supplied payoff model: the causal organ composes probe results by the workshop's XOR scoring rule and
penalty (see mind/organs/causal.py). This claim tests whether that supplied model, fed by attended probe
results, helps a learner. It does not test discovery of causal structure: the eight graphs stay hidden.
Known limits, recorded before any held-out run: a probe result is attended in a minority of episodes (the
workspace ranks a feature the policy has not learned to use below relevance-boosted ones), and the organ
learns each result one tick after it is attended, so a second probe's result cannot feed the same decision.
The skewed prior (each edge present with probability 4/5) is the held-out transfer test; the organ was
designed and debugged on the uniform dev prior.
Strongest simpler rival: the same recalled facts without the derived plan, rival:compact (see C071).
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C070",
    title="The causal organ raises utility over the plain organism under a skewed prior",
    statement="In workshop/skewed, the organism with the causal organ earns more mean utility per episode over the second half of a 1500-episode lifetime than the "
              "plain organism, by more than 0.15.",
    kind="effect",
    scope="L2",
    question="H001",
    about=("causal",),
    extends=("C011", "C012"),
    test=Compare(world="workshop", a="organism +causal", b="organism", metric="utility", direction=">",
                 margin=0.15, seeds=16, variant="skewed"),
    by="claude-code (H001 session 2026-10-12)",
    created="2026-10-12",
)
