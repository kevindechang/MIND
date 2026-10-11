"""Precision successor to inconclusive C009: memory-dependent control during silent outages.

C009's first sealed held-out comparison was inconclusive for a 0.5 reward/episode
margin (paired delta +0.658, 95% interval [-0.297, +1.612], 16 seeds).
This prospectively retains the *same* world, arms, outcome, margin and lifetime
length, increasing paired independent seeds to 512. A positive result is not
assumed: REFUTED or INCONCLUSIVE are meaningful evidence as well.

The stronger recency rivals (especially window4) challenged C009. Even if the
ablation comparison holds, it does not establish that memory outperforms an
appropriately matched transcript window; the rival panel must be evaluated.

Design justification only, NOT a C020 observation: approximating the historical
paired SD as 1.8 yields a normal-theory 95% half-width of about 0.16 at n=512,
near the gap between C009's observed +0.658 and the fixed +0.5 margin. Neither
variance stability nor a pass is guaranteed; the runner's actual CI rules.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C020",
    title="Silent-outage memory effect at higher paired precision",
    statement="In outage/silent, intact memory increases mean reward per episode by more "
              "than 0.5 over otherwise identical memory ablation across 512 paired lifetimes.",
    kind="effect",
    scope="L2",
    question="H007",
    about=("memory",),
    depends_on=("K03",),
    extends=("C009",),
    test=Compare(world="outage", a="organism", b="organism -memory",
                 metric="reward", direction=">", margin=0.5,
                 seeds=512, episodes=120, variant="silent"),
    by="ChatGPT (registration); executed by claude-code (session 01WMmox); see immutable records",
    created="2026-10-11",
    rationale="Resolve C009's wide paired interval without weakening its original effect margin; "
              "report the same-event recency rival panel separately.",
)
