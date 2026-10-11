"""Online multinomial readout shared by H013 report and transcript rivals."""
from __future__ import annotations
import math
from typing import Dict, Iterable, Sequence, Tuple

class OnlineActionReadout:
    """Shared learner for both narrators: online multinomial logistic regression."""

    def __init__(self, rate: float = 0.3):
        self.rate = float(rate)
        self.weights: Dict[Tuple[str, str], float] = {}

    @staticmethod
    def _features(features: Iterable[str]) -> Tuple[str, ...]:
        return tuple(sorted(set(features) | {"bias"}))

    def predict(self, features: Iterable[str], actions: Sequence[str]) -> Dict[str, float]:
        feats = self._features(features)
        actions = tuple(actions)
        if not actions or len(actions) != len(set(actions)):
            raise ValueError("legal actions must be nonempty and unique")
        scores = {a: sum(self.weights.get((a, f), 0.0) for f in feats) for a in actions}
        peak = max(scores.values())
        exp = {a: math.exp(max(-60.0, scores[a] - peak)) for a in actions}
        total = sum(exp.values())
        return {a: exp[a] / total for a in actions}

    def learn(self, features: Iterable[str], actual: str, probabilities: Dict[str, float]) -> None:
        """Call ONLY after prediction and after the organism has chosen its action."""
        if actual not in probabilities:
            raise ValueError("actual action was not legal")
        feats = self._features(features)
        scale = self.rate / len(feats)
        for action in sorted(probabilities):
            error = (1.0 if action == actual else 0.0) - probabilities[action]
            for f in feats:
                key = (action, f)
                self.weights[key] = self.weights.get(key, 0.0) + scale * error
