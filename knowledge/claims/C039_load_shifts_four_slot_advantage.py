"""Distractor load shifts the value of the default four-slot workspace.

C005 found that four slots beat unlimited access under five distractors.
C019 found the same contrast equivalent within +/-0.12 under two distractors.
Neither claim says the advantage itself grows by a scientifically relevant
amount when the load rises. This claim tests that growth.

The margin is 0.08 kept-rate, the same bar C005 used for a single contrast,
not a tolerance fitted to the dev estimate. Dev-seed exploration (not this
claim's test) put a 16-seed interval for the shift with its lower end on
that bar, so the precision budget is 64 paired seeds. Both arms are the
same organism; unlimited access is rival:flat. Seeds are paired by index
across variants. The variants draw different episodes.

Strongest rival: rival:flat, the identical learner with no bottleneck.
"""
from mind.claims import Check, Claim


def load_shift(ctx):
    from mind.stats import bootstrap_ci
    margin = 0.08

    def effect(variant):
        limited = ctx.lab.metric("organism capacity=4", "vigil", variant, ctx.seeds, 300, "kept")
        flat = ctx.lab.metric("rival:flat", "vigil", variant, ctx.seeds, 300, "kept")
        return [a - b for a, b in zip(limited, flat)]

    crowded, dev = effect("crowded"), effect("dev")
    shift = [c - d for c, d in zip(crowded, dev)]
    mean, lo, hi = bootstrap_ci(shift, seed="C039")
    if lo > margin:
        verdict = "HOLDS"
    elif hi <= margin:
        verdict = "FAILS"
    else:
        verdict = "INCONCLUSIVE"
    return {
        "verdict": verdict,
        "robust": True,
        "shift": mean,
        "lo": lo,
        "hi": hi,
        "crowded": sum(crowded) / len(crowded),
        "dev": sum(dev) / len(dev),
        "summary": (
            f"crowded-dev {mean:+.3f} [{lo:+.3f}, {hi:+.3f}] "
            f"(crowded {sum(crowded)/len(crowded):+.3f}, dev {sum(dev)/len(dev):+.3f}; claim: > 0.08)"
        ),
    }


CLAIM = Claim(
    id="C039",
    title="Distractor load increases the four-slot workspace's advantage",
    statement="Over 64 paired seeds and 300 episodes, the kept-rate advantage of a 4-slot workspace "
              "over unlimited access is larger in vigil/crowded (5 distractors, gaps 3-8) than in "
              "vigil/dev (2 distractors, gaps 3-8) by more than 0.08.",
    kind="effect",
    scope="L2",
    question="H003",
    extends=("C005", "C019", "C006"),
    test=Check(load_shift, seeds=64),
    by="researcher-bot",
    created="2026-10-11",
    rationale="The 0.08 kept-rate bar is C005's, applied to the change in the bottleneck's effect "
              "when distractor count rises from 2 to 5. Sixty-four seeds are the precision budget "
              "because a 16-seed exploration interval sat on that bar. This does not assert that "
              "four slots are best at every load, and it is not a claim about other worlds.",
)
