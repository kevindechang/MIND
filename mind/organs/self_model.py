"""Self-model: a learned, calibrated forecast of the organism's OWN success.

For every action it has tried, it fits an online logistic model of
P(success | action, broadcast context) from the public outcome signal. It
(1) supplies the confidence that calibration metrics score against reality,
(2) bids compact self-knowledge into the workspace (`self:<action>=doubt|unsure|sure`),
(3) flags surprising outcomes (`surprise=<action>`), a candidate capability change.

Context comes only from the broadcast, so what other organs make globally
available changes how well the organism knows itself -- a cross-function
dependency the lesion atlas can measure. Constant learning rate = recency,
which lets it track capabilities that drift. Rival: a per-action success table.
"""
from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

from ..kernel import Content, Organ


class SelfModel(Organ):
    name = "self_model"
    home = ("metacognition",)
    defaults = {"lr": 0.6, "min_n": 3, "report": 2, "surprise": 0.6}

    def __init__(self, params):
        super().__init__(params)
        self.w: Dict[Tuple[str, str], float] = {}
        self.n: Dict[str, int] = {}
        self.context: List[str] = ["bias"]
        self.decision_feats: Optional[List[str]] = None
        self.surprised: Optional[str] = None

    @staticmethod
    def _features(view) -> List[str]:
        return ["bias"] + sorted({c.feature for c in view if c.source != "self_model"})

    def _p(self, action: str, feats: List[str]) -> float:
        z = sum(self.w.get((action, f), 0.0) for f in feats)
        return 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))

    def _update(self, action: str, feats: List[str], outcome: int) -> None:
        g = float(outcome) - self._p(action, feats)
        step = self.p["lr"] / len(feats)
        for f in feats:
            self.w[(action, f)] = self.w.get((action, f), 0.0) + step * g
        self.n[action] = self.n.get(action, 0) + 1
        if abs(g) > self.p["surprise"]:
            self.surprised = action

    def propose(self, sense, ctx) -> List[Content]:
        out = []
        if self.surprised is not None:
            out.append(Content(self.name, "surprise", self.surprised, 1.0))
        scored = []
        for action in sorted(self.n):
            if self.n[action] >= self.p["min_n"]:
                p = self._p(action, self.context)
                scored.append((-abs(p - 0.5), action, p))
        scored.sort()
        for _, action, p in scored[: int(self.p["report"])]:
            label = "doubt" if p < 0.35 else "sure" if p > 0.75 else "unsure"
            out.append(Content(self.name, "self:" + action, label, 0.2 + abs(p - 0.5)))
        return out

    def learn(self, prev, now, view, ctx) -> None:
        self.surprised = None
        if (prev is not None and prev.action is not None and now.outcome is not None
                and self.decision_feats is not None):
            self._update(prev.action, self.decision_feats, now.outcome)
        self.context = self._features(view)

    def learn_terminal(self, prev, reward, outcome, ctx) -> None:
        if outcome is not None and self.decision_feats is not None:
            self._update(prev.action, self.decision_feats, outcome)

    def after_act(self, now, view, action, ctx) -> None:
        self.decision_feats = self._features(view)

    def forecast(self, view, action: str) -> float:
        if self.n.get(action, 0) == 0:
            return 0.5
        return round(self._p(action, self._features(view)), 6)

    def introspect(self):
        return {"confidence": {a: round(self._p(a, self.context), 3) for a in sorted(self.n)}}
