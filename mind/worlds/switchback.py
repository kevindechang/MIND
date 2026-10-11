"""H012 switchback: episode-specific A-B-A action-rule retention.

Each episode independently samples which action works in phase A. Phase B
requires the opposite action. The first action after returning to A is the
primary retention probe. Only phase cues, distractors, rewards and public
outcomes reach agents; the hidden mapping remains scorer-private.

Exogenous noise and outcome flips are keyed by seed, episode and tick, never
by the agent's chosen actions. This permits paired policy comparisons.
"""
from __future__ import annotations

import random

from .base import Step, World


_SETTINGS = {
    "dev": {"a": 6, "b": 12, "noise": 1, "flip": 0.0},
    "long": {"a": 6, "b": 32, "noise": 4, "flip": 0.0},
    "noisy": {"a": 6, "b": 12, "noise": 3, "flip": 0.15},
}


class Switchback(World):
    name = "switchback"
    actions = ("left", "right")
    metrics = {
        "return_first": ("retention", "higher"),
        "return_mean": ("retention", "higher"),
        "acquisition_mean": ("adaptation", "higher"),
        "interference_mean": ("adaptation", "higher"),
    }
    atlas_metrics = ("return_first", "acquisition_mean")
    variants = ("dev", "long", "noisy")
    heldout_variants = ("long", "noisy")
    default_episodes = 160

    def _stream(self, *parts):
        return random.Random("|".join(
            ["world", self.name, self.variant, str(self.seed)]
            + [str(x) for x in parts]
        ))

    def reset(self):
        self.episode = getattr(self, "episode", -1) + 1
        self.t = 0
        self.a_rule = self._stream("episode", self.episode, "rule").choice(self.actions)
        self.b_rule = "right" if self.a_rule == "left" else "left"
        self.scores = {"a1": [], "b": [], "a2": []}
        return self._obs()

    def _stage(self):
        s = _SETTINGS[self.variant]
        if self.t < s["a"]:
            return "a1"
        if self.t < s["a"] + s["b"]:
            return "b"
        return "a2"

    def _obs(self):
        s = _SETTINGS[self.variant]
        phase = "amber" if self._stage() != "b" else "violet"
        rng = self._stream("episode", self.episode, "tick", self.t, "observation")
        obs = {"phase": phase}
        for i in range(s["noise"]):
            obs[f"noise{i}"] = str(rng.randrange(2))
        return obs

    def step(self, action):
        if action not in self.actions:
            raise ValueError(f"illegal action {action!r}")
        s = _SETTINGS[self.variant]
        stage = self._stage()
        correct = self.a_rule if stage != "b" else self.b_rule
        # A predetermined actuator/feedback flip, independent of policy.
        flip = self._stream("episode", self.episode, "tick", self.t,
                            "feedback").random() < s["flip"]
        outcome = int((action == correct) != flip)
        self.scores[stage].append(float(outcome))
        info = {"stage": stage, "a_rule": self.a_rule,
                "b_rule": self.b_rule, "feedback_flip": flip}
        self.t += 1
        done = self.t == 2 * s["a"] + s["b"]
        return Step({} if done else self._obs(),
                    1.0 if outcome else -1.0, outcome, done, info)

    def summary(self):
        return {
            "return_first": self.scores["a2"][0],
            "return_mean": sum(self.scores["a2"]) / len(self.scores["a2"]),
            "acquisition_mean": sum(self.scores["a1"]) / len(self.scores["a1"]),
            "interference_mean": sum(self.scores["b"]) / len(self.scores["b"]),
        }
