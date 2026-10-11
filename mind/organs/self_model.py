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
    defaults = {"lr": 0.6, "min_n": 3, "report": 2, "surprise": 0.6,
                "step": "normalised", "gate": "all"}
    fixed_gates = ("all", "no_memory", "no_goals", "no_memory_goals", "bias")
    choices = {"step": ("normalised", "sqrt", "adagrad"),
               "gate": fixed_gates + ("learned", "uniform")}

    def __init__(self, params):
        super().__init__(params)
        self.w: Dict[Tuple[str, str], float] = {}
        self.n: Dict[str, int] = {}
        self.context: List[str] = ["bias"]
        self.decision_feats: Optional[List[str]] = None
        self.surprised: Optional[str] = None
        self.grad_sq: Dict[Tuple[str, str], float] = {}
        # Five fixed-input experts; the control learns exactly the same experts.
        # All updates are folded from public outcomes in the ordinary organ hooks.
        self.experts = ([SelfModel({**self.p, "gate": gate}) for gate in self.fixed_gates]
                        if self.p["gate"] in ("learned", "uniform") else [])
        self.losses: Dict[str, List[float]] = {}
        self.expert_predictions: Optional[List[float]] = None
        self.decision_confidence: Optional[float] = None

    def _filtered(self, view):
        gate = self.p["gate"]
        blocked = {"no_memory": ("memory",), "no_goals": ("goals",),
                   "no_memory_goals": ("memory", "goals")}.get(gate, ())
        return () if gate == "bias" else tuple(c for c in view if c.source not in blocked)

    def gate_weights(self, action: str) -> List[float]:
        """Hedge weights (eta=1) from past prequential Brier losses, per action.

        These are prediction-mixture weights, not workspace bids or neuron gates.
        Subtracting the minimum loss avoids underflow of every weight at once.
        Uniform still computes the same losses/weights, then discards the weights.
        """
        losses = self.losses.get(action, [0.0] * len(self.experts))
        if not losses:
            return []
        best = min(losses)
        raw = [math.exp(-(loss - best)) for loss in losses]
        total = sum(raw)
        weights = [w / total for w in raw]
        return [1 / len(weights)] * len(weights) if self.p["gate"] == "uniform" else weights

    def _context_p(self, action):
        if self.experts:
            return sum(w * e._p(action, e.context)
                       for w, e in zip(self.gate_weights(action), self.experts))
        return self._p(action, self.context)

    def _score_experts(self, prev, outcome):
        if (prev is None or prev.action is None or outcome is None
                or self.expert_predictions is None):
            return
        losses = self.losses.setdefault(prev.action, [0.0] * len(self.experts))
        for i, prediction in enumerate(self.expert_predictions):
            losses[i] += (prediction - outcome) ** 2
        self.n[prev.action] = self.n.get(prev.action, 0) + 1
        if abs(outcome - self.decision_confidence) > self.p["surprise"]:
            self.surprised = prev.action

    @staticmethod
    def _features(view) -> List[str]:
        return ["bias"] + sorted({c.feature for c in view if c.source != "self_model"})

    def _p(self, action: str, feats: List[str]) -> float:
        z = sum(self.w.get((action, f), 0.0) for f in feats)
        return 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))

    def _update(self, action: str, feats: List[str], outcome: int) -> None:
        g = float(outcome) - self._p(action, feats)
        step = self.p["lr"] / len(feats)
        if self.p["step"] == "sqrt":
            step = self.p["lr"] / math.sqrt(len(feats))
        for f in feats:
            if self.p["step"] == "adagrad":
                key = (action, f)
                self.grad_sq[key] = self.grad_sq.get(key, 0.0) + g * g
                step = self.p["lr"] / (math.sqrt(self.grad_sq[key]) + 1e-8)
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
                p = self._context_p(action)
                scored.append((-abs(p - 0.5), action, p))
        scored.sort()
        for _, action, p in scored[: int(self.p["report"])]:
            label = "doubt" if p < 0.35 else "sure" if p > 0.75 else "unsure"
            out.append(Content(self.name, "self:" + action, label, 0.2 + abs(p - 0.5)))
        return out

    def learn(self, prev, now, view, ctx) -> None:
        self.surprised = None
        if self.experts:
            self._score_experts(prev, now.outcome)
            for expert in self.experts:
                expert.learn(prev, now, view, ctx)
            return
        if (prev is not None and prev.action is not None and now.outcome is not None
                and self.decision_feats is not None):
            self._update(prev.action, self.decision_feats, now.outcome)
        self.context = self._features(self._filtered(view))

    def learn_terminal(self, prev, reward, outcome, ctx) -> None:
        if self.experts:
            self._score_experts(prev, outcome)
            for expert in self.experts:
                expert.learn_terminal(prev, reward, outcome, ctx)
            return
        if outcome is not None and self.decision_feats is not None:
            self._update(prev.action, self.decision_feats, outcome)

    def after_act(self, now, view, action, ctx) -> None:
        if self.experts:
            self.expert_predictions = [e.forecast(view, action) for e in self.experts]
            self.decision_confidence = self.forecast(view, action)
            for expert in self.experts:
                expert.after_act(now, view, action, ctx)
            return
        self.decision_feats = self._features(self._filtered(view))

    def forecast(self, view, action: str) -> float:
        if self.n.get(action, 0) == 0:
            return 0.5
        if self.experts:
            return round(sum(w * e.forecast(view, action)
                             for w, e in zip(self.gate_weights(action), self.experts)), 6)
        return round(self._p(action, self._features(self._filtered(view))), 6)

    def introspect(self):
        return {"confidence": {a: round(self._context_p(a), 3) for a in sorted(self.n)}}
