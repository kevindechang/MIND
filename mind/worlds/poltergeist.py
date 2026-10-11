"""Poltergeist: an action's sensory effect is confounded by external change.

H010 instrument, not a test of consciousness. Two actuators push a dial in
opposite directions. Their polarity is hidden and fixed over a lifetime. At
EVERY tick an action-independent ambient impulse and an independent actuator
slip are sampled, regardless of the action chosen. The next observation shows
only the resulting dial position; no observation identifies its causes.

The actor sees its own chosen action (through its own memory), the new dial,
and outcome=whether the *net* position improved. The latter is deliberately
not an oracle for actuator success. The separate Step.info exposes shock and
actuation only to the scorer, never the actor.

The mechanism is identifiable *statistically*, not from a single transition:
a predicted actuator effect may be compared against the net delta, but the
ambient impulse can cancel it or impersonate it. A future efference organ must
beat a same-information state estimator, not merely learn this world by fiat.
"""
from __future__ import annotations
from .base import Step, World

_SETTINGS = {
    "dev": {"shock": 0.35, "slip": 0.12},
    "storm": {"shock": 0.65, "slip": 0.25},
    "calm": {"shock": 0.15, "slip": 0.12},
}
_LENGTH = 24


class Poltergeist(World):
    name = "poltergeist"
    actions = ("wait", "tap_a", "tap_b")
    metrics = {"reward": ("control", "higher"),
               "mean_abs_error": ("control", "lower"),
               "wrong_corrections": ("control", "lower"),
               "brier": ("metacognition", "lower")}
    atlas_metrics = ("reward", "calib_gain")
    variants = ("dev", "storm", "calm")
    heldout_variants = ("storm", "calm")
    default_episodes = 160

    def __init__(self, seed: int, variant: str = "dev"):
        super().__init__(seed, variant)
        self.polarity = self.rng.choice((-1, 1))
        self.t = 0
        self.position = 0
        self.total_abs_error = 0
        self.wrong_corrections = 0
        self.shocks = 0
        self._impulses = []
        self._slips = []

    def reset(self):
        self.t = 0
        self.position = self.rng.choice((-2, -1, 1, 2))
        self.total_abs_error = 0
        self.wrong_corrections = 0
        self.shocks = 0
        settings = _SETTINGS[self.variant]
        # Pre-draw the whole episode before ANY agent action. A paired arm
        # receives exactly the same exogenous events and actuator failures.
        self._impulses = []
        self._slips = []
        for _ in range(_LENGTH):
            roll = self.rng.random()
            direction = -1 if self.rng.random() < 0.5 else 1
            self._impulses.append(direction if roll < settings["shock"] else 0)
            self._slips.append(self.rng.random() < settings["slip"])
        return self._obs()

    def _obs(self):
        return {"dial": str(self.position)}

    def step(self, action):
        if action not in self.actions:
            raise ValueError(f"illegal poltergeist action: {action!r}")
        before = self.position
        desired = {"wait": 0, "tap_a": self.polarity, "tap_b": -self.polarity}[action]
        actuation = 0 if self._slips[self.t] else desired
        shock = self._impulses[self.t]
        self.position = before + actuation + shock
        self.shocks += int(shock != 0)
        self.total_abs_error += abs(self.position)
        if before and actuation and abs(before + actuation) > abs(before):
            self.wrong_corrections += 1
        # This reports only NET improvement. It can be misleading when an
        # external shock cancels or impersonates an action's expected effect.
        outcome = int(abs(self.position) < abs(before)) if action != "wait" else None
        reward = 1.0 - min(abs(self.position), 8) / 8.0
        self.t += 1
        return Step(self._obs() if self.t < _LENGTH else {}, reward, outcome,
                    self.t >= _LENGTH,
                    {"shock": shock, "actuation": actuation, "slipped": self._slips[self.t - 1],
                     "polarity": self.polarity, "before": before, "after": self.position})

    def summary(self):
        return {"mean_abs_error": self.total_abs_error / _LENGTH,
                "wrong_corrections": float(self.wrong_corrections)}
