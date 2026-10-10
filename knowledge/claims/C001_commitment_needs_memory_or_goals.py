"""Keeping a commitment across a gap requires memory or goals; without both it collapses.

Builds on: L02 (v1 Day 0 kept one stored task across process death); here a
*learning* organism must carry a request it saw once to an unannounced bell.
Rival panel: the transcript rivals (reactive, window4/8) see the same raw
observations with the same learner (K03) but no workspace, memory or goals.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C001",
    title="Commitments across a gap need memory or goals",
    statement="In vigil/dev, removing both memory and goals lowers the rate of kept commitments by more "
              "than 0.5 (from ~0.9 to near zero).",
    kind="effect",
    scope="L2",
    question="H008",
    about=("memory", "goals"),
    depends_on=("K03",),
    extends=("L02",),
    test=Compare(world="vigil", a="organism", b="organism -memory -goals", metric="kept",
                 direction=">", margin=0.5, seeds=16),
    by="pipeline-v2",
    created="2026-10-10",
    rationale="Positive control for the vigil world: if this failed, no other vigil claim would mean anything.",
)
