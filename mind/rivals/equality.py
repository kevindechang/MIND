"""Equal-information, equal-Q-learner structural rival for glyph transfer.

Uses the same public glyphs, actions and outcomes as the organism. No private
rule, phase or scorer labels are used; raw tokens are reduced to equality.
"""
from __future__ import annotations

from . import Transcript


class EqualityTranscript(Transcript):
    def __init__(self, seed: int):
        super().__init__(k=1, seed=seed, pairs=True)

    def step(self, obs, reward=0.0, outcome=None, boundary=False,
             actions=("press_a", "press_b")):
        if "sample" not in obs or "candidate" not in obs:
            raise ValueError("equality rival requires sample and candidate")
        reduced = {"equal": "1" if obs["sample"] == obs["candidate"] else "0"}
        return super().step(reduced, reward, outcome, boundary, actions)
