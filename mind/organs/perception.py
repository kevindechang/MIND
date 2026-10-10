"""Perception: turns the current observation into workspace contents.

Salience is learned information content (habituation). Perception keeps
lifetime counts of every feature and bids with its surprisal
-log2 P(feature), squashed to (0,1): rare events (a bell, a new request)
stand out; features that are always present or flip constantly fade.
`perception.salience=novelty` restores the naive rule (changed since the last
tick = 1.0, else 0.35), kept as a standing rival mechanism.
"""
from __future__ import annotations

import math
from typing import Dict, List

from ..kernel import Content, Organ


class Perception(Organ):
    name = "perception"
    home = ("sensing",)
    defaults = {"salience": "surprisal", "novel": 1.0, "stale": 0.35}
    choices = {"salience": ("surprisal", "novelty")}

    def __init__(self, params):
        super().__init__(params)
        self.last: Dict[str, str] = {}
        self.counts: Dict[str, int] = {}
        self.ticks = 0

    def reset_episode(self) -> None:
        self.last = {}

    def _salience(self, key: str, value: str) -> float:
        if self.p["salience"] == "novelty":
            return self.p["novel"] if self.last.get(key) != value else self.p["stale"]
        p = (self.counts.get(f"{key}={value}", 0) + 1) / (self.ticks + 2)
        bits = -math.log2(p)
        return bits / (1.0 + bits)

    def propose(self, sense, ctx) -> List[Content]:
        return [Content(self.name, key.replace("&", "+"), sense.obs[key].replace("&", "+"),
                        self._salience(key, sense.obs[key]))
                for key in sorted(sense.obs)]

    def learn(self, prev, now, view, ctx) -> None:
        self.last = dict(now.obs)
        self.ticks += 1
        for key in sorted(now.obs):
            f = f"{key}={now.obs[key]}"
            self.counts[f] = self.counts.get(f, 0) + 1
