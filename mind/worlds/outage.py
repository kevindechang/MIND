"""Outage: a tool that silently breaks and recovers; know your own capabilities.

Generalises E100 Day 1 (an outage event must reach the decision-maker) and Day 3
(self-model after abrupt tool loss) into one learning task. Every tick is a
job: `scan` pays +1 if the hidden sensor is up and -0.5 if it is down; `manual`
always pays +0.35; `wait` pays 0. The sensor fails and recovers as a hidden
Markov process that persists across episodes. Outages are only sometimes
announced (`alert=down`/`alert=up`, with occasional false alarms); the agent
also sees the result of its previous action (`result=scan:ok|scan:fail|manual:ok`).

Variants: dev; silent (no announcements: capability must be inferred from one's
own failures); volatile (faster failure and repair).
"""
from __future__ import annotations

from .base import Step, World

_SETTINGS = {
    "dev": {"fail": 0.06, "fix": 0.12, "alert": 0.6, "alert_up": 0.5, "false": 0.02, "noise": 2},
    "silent": {"fail": 0.06, "fix": 0.12, "alert": 0.0, "alert_up": 0.0, "false": 0.0, "noise": 2},
    "volatile": {"fail": 0.12, "fix": 0.25, "alert": 0.6, "alert_up": 0.5, "false": 0.02, "noise": 2},
}
SCAN_OK, SCAN_FAIL, MANUAL = 1.0, -0.5, 0.35
LENGTH = 25


class Outage(World):
    name = "outage"
    actions = ("wait", "scan", "manual")
    metrics = {"reward": ("control", "higher"),
               "brier": ("metacognition", "lower"),
               "wasted_scans": ("control", "lower")}
    variants = ("dev", "silent", "volatile")
    heldout_variants = ("silent", "volatile")
    default_episodes = 120

    def __init__(self, seed, variant="dev"):
        super().__init__(seed, variant)
        self.s = _SETTINGS[variant]
        self.up = True          # hidden; persists across episodes
        self.alert = None       # announcement visible on the next tick
        self.result = None

    def reset(self):
        self.t = 0
        self.wasted = 0
        return self._obs()

    def _obs(self):
        obs = {f"noise{i}": str(self.rng.randint(0, 1)) for i in range(self.s["noise"])}
        if self.alert:
            obs["alert"] = self.alert
        if self.result:
            obs["result"] = self.result
        return obs

    def _evolve(self):
        s, before = self.s, self.up
        if self.up and self.rng.random() < s["fail"]:
            self.up = False
        elif not self.up and self.rng.random() < s["fix"]:
            self.up = True
        roll = self.rng.random()
        if before and not self.up:
            self.alert = "down" if roll < s["alert"] else None
        elif not before and self.up:
            self.alert = "up" if roll < s["alert_up"] else None
        else:
            self.alert = "down" if roll < s["false"] else None

    def step(self, action):
        info = {"up": self.up}
        if action == "scan":
            ok = self.up
            reward, outcome = (SCAN_OK, 1) if ok else (SCAN_FAIL, 0)
            self.result = "scan:ok" if ok else "scan:fail"
            self.wasted += 0 if ok else 1
        elif action == "manual":
            reward, outcome, self.result = MANUAL, 1, "manual:ok"
        else:
            reward, outcome, self.result = 0.0, None, None
        self._evolve()
        self.t += 1
        done = self.t >= LENGTH
        return Step(self._obs() if not done else {}, reward, outcome, done, info)

    def summary(self):
        return {"wasted_scans": float(self.wasted)}
