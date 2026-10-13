"""Policy: the organism's action learner. It sees ONLY the broadcast.

Linear temporal-difference Q-learning over the broadcast's features plus all
pairwise conjunctions (normalised step, epsilon-greedy with a half-life). The
pairwise expansion makes the workspace bottleneck consequential: K broadcast
items give K(K-1)/2 conjunctions to learn, so a narrow workspace trades
information for faster credit assignment (the 'consciousness prior' idea,
testable here via capacity lesions, claim family H003).

The same learner class is reused by rivals so that comparisons isolate
representation, not learning algorithm.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

from ..kernel import Organ


def expand(singles: Sequence[str], pairs: bool = True) -> List[str]:
    singles = sorted(set(singles))
    feats = ["bias"] + singles
    if pairs:
        feats += [a + "&" + b for i, a in enumerate(singles) for b in singles[i + 1:]]
    return feats


class QLearner:
    """Representation-agnostic linear TD learner (shared with rival agents)."""

    def __init__(self, alpha=0.3, gamma=0.9, eps=0.3, eps_min=0.01, half_life=400):
        self.alpha, self.gamma = alpha, gamma
        self.eps, self.eps_min, self.half_life = eps, eps_min, half_life
        self.w: Dict[Tuple[str, str], float] = {}
        # credit[(single, action)] = own weight + weights of every conjunction containing it,
        # so a feature that matters only jointly (pending & bell) still counts as relevant.
        self.credit: Dict[Tuple[str, str], float] = {}
        self.known: List[str] = []
        self.episodes = 0
        self.decisions = 0

    def q(self, feats: Sequence[str], action: str) -> float:
        w = self.w
        return sum(w.get((f, action), 0.0) for f in feats)

    def greedy(self, feats: Sequence[str], actions: Sequence[str]) -> str:
        best, best_q = actions[0], self.q(feats, actions[0])
        for a in actions[1:]:
            v = self.q(feats, a)
            if v > best_q + 1e-12:
                best, best_q = a, v
        return best

    def greedy_with(self, feats: Sequence[str], actions: Sequence[str], bonus: Dict[str, float]) -> str:
        """Greedy choice with a direct bonus added to the value of named actions (broadcast proposals)."""
        best, best_q = actions[0], self.q(feats, actions[0]) + bonus.get(actions[0], 0.0)
        for a in actions[1:]:
            v = self.q(feats, a) + bonus.get(a, 0.0)
            if v > best_q + 1e-12:
                best, best_q = a, v
        return best

    def choose(self, feats: Sequence[str], actions: Sequence[str], rng,
               bonus: Optional[Dict[str, float]] = None) -> str:
        for a in actions:
            if a not in self.known:
                self.known.append(a)
        # exploration halves every `half_life` decisions (not episodes: worlds differ in length)
        eps = max(self.eps_min, self.eps * 0.5 ** (self.decisions / self.half_life))
        self.decisions += 1
        if rng.random() < eps:
            return actions[rng.randrange(len(actions))]
        if bonus:
            return self.greedy_with(feats, actions, bonus)
        return self.greedy(feats, actions)

    def update(self, feats: Sequence[str], action: str, target: float) -> None:
        delta = target - self.q(feats, action)
        step = self.alpha / len(feats)
        w, credit = self.w, self.credit
        for f in feats:
            key = (f, action)
            w[key] = w.get(key, 0.0) + step * delta
            for part in f.split("&"):
                ck = (part, action)
                credit[ck] = credit.get(ck, 0.0) + step * delta

    def bootstrap(self, reward: float, feats: Sequence[str], actions: Sequence[str]) -> float:
        return reward + self.gamma * max(self.q(feats, a) for a in actions)

    def relevance(self, feature: str) -> float:
        if not self.known:
            return 0.0
        vals = [self.credit.get((feature, a), 0.0) for a in self.known]
        return max(vals) - min(vals)


class Policy(Organ):
    name = "policy"
    home = ("control",)
    # bonus: a direct route from broadcast proposals to action (H015). Every causal proposal that names an action
    # (`probe=...`, `best=...`) adds `bonus` to that action's value. 0 keeps the learned values alone.
    defaults = {"alpha": 0.3, "gamma": 0.9, "eps": 0.3, "eps_min": 0.01, "half_life": 400, "pairs": 1,
                "bonus": 0.0}
    NAMING_KEYS = ("probe", "best")

    def __init__(self, params):
        super().__init__(params)
        self.learner = QLearner(self.p["alpha"], self.p["gamma"], self.p["eps"],
                                self.p["eps_min"], self.p["half_life"])
        self._feats: Optional[List[str]] = None
        self._prev_feats: Optional[List[str]] = None

    def features(self, view) -> List[str]:
        return expand([c.feature for c in view], bool(self.p["pairs"]))

    def decide(self, view, actions, rng) -> str:
        self._feats = self.features(view)
        if not self.p["bonus"]:
            return self.learner.choose(self._feats, actions, rng)
        named = {c.value: float(self.p["bonus"]) for c in view
                 if c.source == "causal" and c.key in self.NAMING_KEYS}
        return self.learner.choose(self._feats, actions, rng, bonus=named)

    def learn(self, prev, now, view, ctx) -> None:
        if prev is None or prev.action is None or self._prev_feats is None:
            return
        target = self.learner.bootstrap(now.reward, self.features(view), now.actions)
        self.learner.update(self._prev_feats, prev.action, target)

    def learn_terminal(self, prev, reward, outcome, ctx) -> None:
        if self._prev_feats is not None:
            self.learner.update(self._prev_feats, prev.action, reward)
        self.learner.episodes += 1

    def after_act(self, now, view, action, ctx) -> None:
        self._prev_feats = self._feats

    def relevance(self, feature: str) -> float:
        return self.learner.relevance(feature)

    def greedy(self, singles: Sequence[str], actions: Sequence[str]) -> str:
        return self.learner.greedy(expand(singles, bool(self.p["pairs"])), list(actions))

    def introspect(self):
        return {"episodes": self.learner.episodes, "weights": len(self.learner.w)}
