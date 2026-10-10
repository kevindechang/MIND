"""Episodic memory: keeps attended perceptions and offers them back once they vanish.

Only contents that won the workspace are encoded (attention gates memory, as in
global-workspace accounts), so memory depends causally on the bottleneck.
Each remembered feature is offered as `was:<key>=<value>` while the current
observation no longer shows it, with salience decaying by age. Capacity is
finite; the least salient trace is forgotten first.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from ..kernel import Content, Organ


class Memory(Organ):
    name = "memory"
    home = ("continuity",)
    defaults = {"capacity": 6, "decay": 0.92, "age_tags": 0}

    def __init__(self, params):
        super().__init__(params)
        # feature "key=value" -> (key, value, tick last attended, salience when attended)
        self.items: Dict[str, Tuple[str, str, int, float]] = {}

    def reset_episode(self) -> None:
        self.items = {}

    def _strength(self, item: Tuple[str, str, int, float], t: int) -> float:
        return item[3] * self.p["decay"] ** (t - item[2])

    def propose(self, sense, ctx) -> List[Content]:
        out = []
        for feature in sorted(self.items):
            key, value, when, _ = self.items[feature]
            if sense.obs.get(key) == value:
                continue  # still perceived; nothing to remember yet
            shown = value
            if self.p["age_tags"]:
                age = sense.t - when
                shown = f"{value}@{'recent' if age <= 2 else 'earlier' if age <= 6 else 'long-ago'}"
            out.append(Content(self.name, "was:" + key, shown,
                               self._strength(self.items[feature], sense.t)))
        return out

    def learn(self, prev, now, view, ctx) -> None:
        for c in view:
            if c.source == "perception":
                self.items[c.feature] = (c.key, c.value, now.t, c.salience)
        capacity = int(self.p["capacity"])
        while len(self.items) > capacity:
            weakest = min(self.items, key=lambda f: (self._strength(self.items[f], now.t),
                                                      self.items[f][2], f))
            del self.items[weakest]

    def introspect(self):
        return {"remembered": sorted(self.items)}
