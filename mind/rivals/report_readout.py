"""Matched public-transcript and workspace action readouts for H013.

External readouts only; neither reads the policy weights or current action.
They are evaluated prequentially on the same organism actions.
"""
from __future__ import annotations

import math
from collections import Counter


class PublicTranscript:
    """Complete public history of the current episode plus lifetime counts."""

    def __init__(self):
        self.history = []
        self.counts = Counter()

    def reset_episode(self):
        self.history.clear()

    def features(self, obs, reward, outcome, actions):
        feats = ["bias", "reward=" + str(reward), "outcome=" + str(outcome),
                 "legal=" + ",".join(actions)]
        feats.extend("now:" + k + "=" + str(v) for k, v in sorted(obs.items()))
        for lag, (old_obs, act, r, o) in enumerate(reversed(self.history), 1):
            pre = "lag" + str(lag) + ":"
            feats += [pre + "action=" + act, pre + "reward=" + str(r),
                      pre + "outcome=" + str(o)]
            feats.extend(pre + k + "=" + str(v) for k, v in sorted(old_obs.items()))
        for a in actions:
            for kind in ("act", "ok", "fail"):
                feats.append("total:" + kind + ":" + a + "=" +
                             str(self.counts[(kind, a)].bit_length()))
        return tuple(sorted(set(feats)))

    def observe(self, obs, action, reward, outcome):
        self.history.append((dict(obs), action, reward, outcome))
        self.counts[("act", action)] += 1
        if outcome is not None:
            self.counts[("ok" if outcome else "fail", action)] += 1


class Decoder:
    """Identical online softmax classifiers, with frozen test weights."""

    def __init__(self, rate=0.25):
        self.rate = rate
        self.weights = {}

    def forecast(self, features, actions):
        feats = tuple(sorted(set(features)))
        if not feats or not actions:
            raise ValueError("empty features or actions")
        scale = math.sqrt(len(feats))
        logits = {a: sum(self.weights.get((a, f), 0.0) for f in feats) / scale
                  for a in actions}
        top = max(logits.values())
        scores = {a: math.exp(logits[a] - top) for a in actions}
        z = sum(scores.values())
        return {a: scores[a] / z for a in actions}

    @staticmethod
    def brier(probs, actual):
        if actual not in probs:
            raise ValueError("action not legal")
        return sum((p - float(a == actual)) ** 2 for a, p in probs.items()) / 2.0

    def learn(self, features, actions, actual, probs):
        feats = tuple(sorted(set(features)))
        scale = math.sqrt(len(feats))
        for a in actions:
            delta = self.rate * (float(a == actual) - probs[a]) / scale
            for f in feats:
                key = (a, f)
                self.weights[key] = self.weights.get(key, 0.0) + delta
