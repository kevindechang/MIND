"""Shift: silent exogenous reversals of two action capabilities (H002 step 2).

A potential-outcomes world: every tool's success coin is fixed for every tick,
independently of which action is selected. This keeps paired action policies in
identical environments. Only public action feedback reveals a reversal.

`post_shift_regret` and `stable_regret` are *sums* of expected per-action
regret in tagged episodes; divide by their corresponding exposure counts to
compare the two periods. Neither the phase nor the scorer's counterfactual
potential outcomes are visible to the agent.
"""
from __future__ import annotations

import random

from .base import Step, World

_SETTINGS = {
    "dev": {"hazard": 0.10, "dwell": 12, "window": 4, "high": 0.85, "low": 0.25, "switch": True},
    "fast": {"hazard": 0.18, "dwell": 8, "window": 3, "high": 0.85, "low": 0.25, "switch": True},
    "subtle": {"hazard": 0.10, "dwell": 12, "window": 4, "high": 0.75, "low": 0.35, "switch": True},
    "stationary": {"hazard": 0.10, "dwell": 12, "window": 4, "high": 0.85, "low": 0.25, "switch": False},
}
TICKS = 6
MANUAL_REWARD = 0.35


class Shift(World):
    name = "shift"
    actions = ("wait", "probe_a", "probe_b", "manual")
    metrics = {
        "reward": ("control", "higher"),
        "regret": ("causal-control", "lower"),
        "post_shift_regret": ("adaptation", "lower"),
        "post_shift_exposure": ("instrument", "higher"),
        "stable_regret": ("adaptation", "lower"),
        "stable_exposure": ("instrument", "higher"),
        "brier": ("metacognition", "lower"),
    }
    atlas_metrics = ("reward", "calib_gain")
    variants = tuple(_SETTINGS)
    heldout_variants = ("fast", "subtle")
    default_episodes = 120

    def _stream(self, *parts):
        return random.Random("|".join(["world", self.name, "dev" if self.variant == "stationary" else self.variant, str(self.seed)]
                                      + [str(x) for x in parts]))

    def reset(self):
        self.episode = getattr(self, "episode", -1) + 1
        s = _SETTINGS[self.variant]
        if self.episode == 0:
            self.phase, self.last_shift = 0, 0
        elif (self.episode - self.last_shift >= s["dwell"] and
              random.Random(f"world|shift|switch|{self.seed}|{self.episode}").random() < s["hazard"]):
            self.phase += 1
            self.last_shift = self.episode
        flipped = bool(s["switch"] and self.phase % 2)
        self.p_a, self.p_b = ((s["low"], s["high"]) if flipped
                              else (s["high"], s["low"]))
        self.t = 0
        self.result = None
        self.regret = 0.0
        self._coins = {(t, a): self._stream("episode", self.episode, "tick", t, "action", a).random()
                       for t in range(TICKS) for a in ("probe_a", "probe_b")}
        # The stationary sham has the SAME exogenous event schedule, but no
        # actual reliability reversal. It tests spurious change-point benefits.
        since = self.episode - self.last_shift
        self.post_shift = bool(self.phase > 0 and since < s["window"])
        self.stable = bool(self.phase > 0 and s["window"] <= since < 2 * s["window"])
        return self._obs()

    def _obs(self):
        rng = self._stream("episode", self.episode, "tick", self.t, "observation")
        obs = {"noise0": str(rng.randint(0, 1)), "noise1": str(rng.randint(0, 1))}
        if self.result is not None:
            obs["result"] = self.result
        return obs

    @staticmethod
    def _expected(p):
        return 1.5 * p - 0.5

    def step(self, action):
        if action not in self.actions or self.t >= TICKS:
            raise ValueError(f"invalid action {action!r} at t={self.t}")
        info = {"phase": self.phase, "p_a": self.p_a, "p_b": self.p_b,
                "post_shift": self.post_shift, "stable": self.stable,
                "actual_reversal": bool(_SETTINGS[self.variant]["switch"] and self.phase > 0)}
        best = max(self._expected(self.p_a), self._expected(self.p_b), MANUAL_REWARD)
        if action in ("probe_a", "probe_b"):
            p = self.p_a if action == "probe_a" else self.p_b
            outcome = int(self._coins[(self.t, action)] < p)
            reward = 1.0 if outcome else -0.5
            self.result = action + (":ok" if outcome else ":fail")
            chosen = self._expected(p)
        elif action == "manual":
            outcome, reward, chosen = 1, MANUAL_REWARD, MANUAL_REWARD
            self.result = "manual:ok"
        else:
            outcome, reward, chosen = None, 0.0, 0.0
            self.result = None
        self.regret += best - chosen
        self.t += 1
        done = self.t == TICKS
        return Step(self._obs() if not done else {}, reward, outcome, done, info)

    def summary(self):
        return {"regret": self.regret / TICKS,
                "post_shift_regret": self.regret / TICKS if self.post_shift else 0.0,
                "post_shift_exposure": float(self.post_shift),
                "stable_regret": self.regret / TICKS if self.stable else 0.0,
                "stable_exposure": float(self.stable)}
