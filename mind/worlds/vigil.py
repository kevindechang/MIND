"""Vigil: keep a commitment across a gap, act on it unprompted, resist false starts.

Generalises E100 Day 0 (a committed action must survive process death) and the
Day 4 initiative lesion into a learning task. At t=0 the agent sees
`request=<x>`; a bell rings once at a random later tick, when the request is no
longer visible. Doing <x> at the bell pays +1; another action pays -0.5; any
non-wait action before the bell is a false start (-0.1). Flickering `noise*`
features compete for attention.

Variants: dev (gap 3-8, 2 distractors); long (gap 9-16: tests decay and
capacity); crowded (gap 3-8, 5 distractors: tests the bottleneck).
"""
from __future__ import annotations

from .base import Step, World

_SETTINGS = {
    "dev": {"gap": (3, 8), "noise": 2},
    "long": {"gap": (9, 16), "noise": 2},
    "crowded": {"gap": (3, 8), "noise": 5},
}


class Vigil(World):
    name = "vigil"
    actions = ("wait", "a", "b", "c")
    metrics = {"kept": ("continuity", "higher"),
               "false_starts": ("inhibition", "lower"),
               "reward": ("control", "higher"),
               "brier": ("metacognition", "lower")}
    atlas_metrics = ("kept", "false_starts", "calib_gain")
    variants = ("dev", "long", "crowded")
    heldout_variants = ("long", "crowded")
    default_episodes = 300

    def reset(self):
        s = _SETTINGS[self.variant]
        self.t = 0
        self.symbol = self.rng.choice(("a", "b", "c"))
        self.bell = self.rng.randint(*s["gap"])
        self.kept = 0
        self.false_starts = 0
        return self._obs()

    def _obs(self):
        obs = {f"noise{i}": str(self.rng.randint(0, 1)) for i in range(_SETTINGS[self.variant]["noise"])}
        if self.t == 0:
            obs["request"] = self.symbol
        if self.t == self.bell:
            obs["bell"] = "1"
        return obs

    def step(self, action):
        info = {"bell": self.t == self.bell, "symbol": self.symbol}
        if self.t == self.bell:
            if action == self.symbol:
                reward, outcome, self.kept = 1.0, 1, 1
            elif action == "wait":
                reward, outcome = 0.0, None
            else:
                reward, outcome = -0.5, 0
            return Step({}, reward, outcome, True, info)
        if action != "wait":
            self.false_starts += 1
            reward, outcome = -0.1, 0
        else:
            reward, outcome = 0.0, None
        self.t += 1
        return Step(self._obs(), reward, outcome, False, info)

    def summary(self):
        return {"kept": float(self.kept), "false_starts": float(self.false_starts)}
