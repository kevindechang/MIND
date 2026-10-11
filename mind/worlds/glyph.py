"""H011 world: learn a hidden binary relation, transfer to unseen glyphs.

Every episode is one action. The rule is fixed per lifetime, but the public
sample/candidate tokens change. Episodes 0-99 use one alphabet; 100+ use a
disjoint alphabet. No action affects future random draws. Scorer-private info
never enters the agent's observation. This is a representation prerequisite,
not a procedure compiler or real process-death experiment.
"""
from __future__ import annotations

import random
from .base import Step, World


class Glyph(World):
    name = "glyph"
    actions = ("press_a", "press_b")
    metrics = {"first_try": ("procedural-transfer", "higher"),
               "transfer": ("procedural-transfer", "higher"),
               "brier": ("metacognition", "lower")}
    atlas_metrics = ("first_try", "calib_gain")
    variants = ("dev", "shift")
    heldout_variants = ("shift",)
    default_episodes = 200
    transfer_start = 100

    def __init__(self, seed: int, variant: str = "dev"):
        super().__init__(seed, variant)
        self.rule = random.Random(f"world|glyph|latent|{seed}").randrange(2)
        self.episode = -1
        self.done = False

    def reset(self):
        self.episode += 1
        self.done = False
        self.phase = "transfer" if self.episode >= self.transfer_start else "train"
        rng = random.Random(f"world|glyph|{self.variant}|{self.seed}|episode|{self.episode}")
        self.same = bool(rng.randrange(2))
        size = 80 if self.variant == "shift" else 40
        left = rng.randrange(size)
        right = left if self.same else rng.randrange(size - 1)
        if not self.same and right >= left:
            right += 1
        transfer = self.phase == "transfer"
        if self.variant == "shift":
            token = lambda i: (f"Y-{i:03d}-long" if transfer else f"X-{i:03d}-long")
        else:
            token = lambda i: (f"new{i:03d}" if transfer else f"old{i:03d}")
        obs = {"sample": token(left), "candidate": token(right)}
        if self.variant == "shift":
            obs["noise"] = str(rng.randrange(8))
        self.correct = 0
        return obs

    def step(self, action: str) -> Step:
        if self.done:
            raise ValueError("glyph episode already completed")
        if action not in self.actions:
            raise ValueError(f"illegal glyph action {action!r}")
        expected = "press_a" if int(self.same) == self.rule else "press_b"
        self.correct = int(action == expected)
        self.done = True
        private = {"rule": self.rule, "same": self.same,
                   "phase": self.phase, "expected": expected}
        return Step({}, 1.0 if self.correct else -1.0, self.correct, True, private)

    def summary(self):
        return {"first_try": float(self.correct),
                "transfer": float(self.correct) if self.phase == "transfer" else 0.0}
