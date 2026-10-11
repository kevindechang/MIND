"""A running prediction of the act is worth more than the current sensation alone.

Positive control for poltergeist. Both arms know the world's parameters and see
the same public stream. Both are told the same act (it is the only legal one).
The filter keeps a belief about polarity and predicts the sensation that act
should produce. The moment judge uses the current act and the current sensation
with a fresh 50/50 polarity prior every trial. Neither reads private causes.
The margin is five percentage points of attribution: below that, the aliasing
would not be doing enough work to be worth a mechanism.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C037",
    title="A running prediction of one's own act beats a moment judge in poltergeist",
    statement="In poltergeist/dev, a polarity filter that predicts the sensory consequence of the current act "
              "attributes external impulses more accurately than a moment judge with the same parameters and "
              "the same current act and sensation but no running prediction, by more than 0.05.",
    kind="effect",
    scope="instrument",
    question="H010",
    about=(),
    depends_on=("K12",),
    extends=("K12", "mind/worlds/poltergeist.py"),
    test=Compare(world="poltergeist", a="rival:filter", b="rival:moment", metric="attributed",
                 direction=">", margin=0.05, seeds=16),
    by="Cursor Agent",
    created="2026-10-11",
    rationale="Shows the confound is solvable from matched public information, and that solving it uses the "
              "trace rather than the current sensation. Both arms are privileged oracles; this is not a "
              "claim that the organism does it. Empty `about` because neither arm is an organ.",
)
