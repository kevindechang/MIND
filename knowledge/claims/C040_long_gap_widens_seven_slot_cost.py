"""Long retention raises the cost of a wide but still-binding workspace.

Under two distractors, late ticks of vigil usually offer about seven bids
(exploration on four dev seeds: mode 7, mean about 7.2). Capacity 7 therefore
drops a bid on the ticks that carry eight or more proposals, while capacity 8
usually does not bind. A dev-seed sweep of K=1..8 found the kept-rate loss
versus unlimited access on vigil/long growing through K=5, K=6 and K=7, then
gone at K=8. K=7 is the registered contrast because it is that wide, still-binding
end of the curve, not because other capacities were invisible. K=5 and K=6 moved
the same way in exploration and are not separate claims. The default four-slot
bottleneck's long-gap loss did not clear 0.08 in that exploration, so it is not
this claim.

The margin is 0.08 kept-rate, the same bar as C005, applied to how much MORE
costly capacity 7 is after long gaps than after short ones. Both arms are the
same organism; unlimited access is rival:flat. Seeds are paired by index across
variants, which draw different episodes.

Strongest rival: rival:flat, the identical learner with no bottleneck.
"""
from mind.claims import Check, Claim


def retention_shift(ctx):
    from mind.stats import bootstrap_ci
    margin = 0.08

    def effect(variant):
        limited = ctx.lab.metric("organism capacity=7", "vigil", variant, ctx.seeds, 300, "kept")
        flat = ctx.lab.metric("rival:flat", "vigil", variant, ctx.seeds, 300, "kept")
        return [a - b for a, b in zip(limited, flat)]

    long, dev = effect("long"), effect("dev")
    shift = [a - b for a, b in zip(long, dev)]
    mean, lo, hi = bootstrap_ci(shift, seed="C040")
    if hi < -margin:
        verdict = "HOLDS"
    elif lo >= -margin:
        verdict = "FAILS"
    else:
        verdict = "INCONCLUSIVE"
    return {
        "verdict": verdict,
        "robust": True,
        "shift": mean,
        "lo": lo,
        "hi": hi,
        "long": sum(long) / len(long),
        "dev": sum(dev) / len(dev),
        "summary": (
            f"long-dev {mean:+.3f} [{lo:+.3f}, {hi:+.3f}] "
            f"(long {sum(long)/len(long):+.3f}, dev {sum(dev)/len(dev):+.3f}; claim: < -0.08)"
        ),
    }


CLAIM = Claim(
    id="C040",
    title="Long retention increases the seven-slot workspace's cost",
    statement="Over 64 paired seeds and 300 episodes, the kept-rate effect of a 7-slot workspace "
              "minus unlimited access is more negative in vigil/long (2 distractors, gaps 9-16) than "
              "in vigil/dev (2 distractors, gaps 3-8) by more than 0.08.",
    kind="effect",
    scope="L2",
    question="H003",
    extends=("C005", "C019", "C006"),
    test=Check(retention_shift, seeds=64),
    by="researcher-bot",
    created="2026-10-11",
    rationale="Capacity 7 is the wide end of the still-binding curve when two distractors leave about "
              "seven bids. The claim tests whether lengthening the gap makes that bottleneck more "
              "costly than unlimited access, by the same 0.08 kept-rate bar C005 used. It does not "
              "say the default four-slot workspace hurts on long gaps, and it is not a claim about "
              "other worlds.",
)
