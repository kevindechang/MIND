"""Efference copy: predict the sensation your own act should produce, and broadcast the error.

Polarity (which way an act moves the sensation) is hidden and redrawn every
episode, and an external impulse of the same size can imitate the act. The
organ keeps a running estimate of polarity from public sensations only, predicts
the sensation the last motor command should have caused, and bids the prediction
error plus that estimate. It does not see the world's private causes, and it
does not read the reward: the forward model is unsupervised. The policy learns
what to do with the error.

Optional. Enable with `+efference`. Belief resets at each episode because the
world redraws polarity then.
"""
from __future__ import annotations

from typing import List

from ..kernel import Content, Organ

_MOTOR = {"push": 1, "pull": -1}


class Efference(Organ):
    name = "efference"
    home = ("attribution",)
    defaults = {"lr": 0.4, "thresh": 0.12, "salience": 3.0}

    def __init__(self, params):
        super().__init__(params)
        self.belief = 0.0
        self.motor = 0

    def reset_episode(self) -> None:
        self.belief = 0.0
        self.motor = 0

    def _gain(self):
        thresh = float(self.p["thresh"])
        if self.belief > thresh:
            return "pos", 1
        if self.belief < -thresh:
            return "neg", -1
        return "unk", 0

    def propose(self, sense, ctx) -> List[Content]:
        if sense.obs.get("phase") != "judge" or "sense" not in sense.obs or self.motor == 0:
            return []
        label, gain = self._gain()
        observed = int(sense.obs["sense"])
        predicted = 0 if gain == 0 else gain * self.motor
        if predicted > 1:
            predicted = 1
        elif predicted < -1:
            predicted = -1
        residual = observed - predicted
        sal = float(self.p["salience"])
        return [Content(self.name, "res", str(residual), sal),
                Content(self.name, "gain", label, sal * 0.8)]

    def learn(self, prev, now, view, ctx) -> None:
        if now.obs.get("phase") != "judge" or "sense" not in now.obs or self.motor == 0:
            return
        observed = int(now.obs["sense"])
        lr = float(self.p["lr"])
        # E[sensation * command] has the sign of the hidden polarity when the
        # external impulse is mean-zero. Public sensation only.
        target = float(observed * self.motor)
        self.belief = (1.0 - lr) * self.belief + lr * target

    def after_act(self, now, view, action, ctx) -> None:
        if action in _MOTOR:
            self.motor = _MOTOR[action]

    def introspect(self):
        label, _ = self._gain()
        return {"belief": round(self.belief, 4), "gain": label, "motor": self.motor}
