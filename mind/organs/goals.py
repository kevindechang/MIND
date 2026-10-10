"""Goals: persistent intentions that keep bidding until they are fulfilled.

Protocol convention shared by all worlds: an observation `request=<action>`
asks for that action at some later time. A request the organism *attended to*
becomes a pending intention, offered every tick as `pending=<action>`, and is
discharged when the organism performs that action. This organ supplies
initiative (acting without a fresh prompt); a compact queue is its rival.
"""
from __future__ import annotations

from typing import List

from ..kernel import Content, Organ


class Goals(Organ):
    name = "goals"
    home = ("continuity", "initiative")
    defaults = {"key": "request", "max": 3, "salience": 0.9}

    def __init__(self, params):
        super().__init__(params)
        self.pending: List[str] = []

    def reset_episode(self) -> None:
        self.pending = []

    def propose(self, sense, ctx) -> List[Content]:
        return [Content(self.name, "pending", x, float(self.p["salience"])) for x in self.pending]

    def learn(self, prev, now, view, ctx) -> None:
        for c in view:
            if c.source == "perception" and c.key == self.p["key"] and c.value not in self.pending:
                self.pending.append(c.value)
        del self.pending[:-int(self.p["max"])]

    def after_act(self, now, view, action, ctx) -> None:
        if action in self.pending:
            self.pending.remove(action)

    def introspect(self):
        return {"pending": list(self.pending)}
