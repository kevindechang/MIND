"""Optional, bounded recurrent reservoir over *attended public* evidence.

This is an online state representation, not a trained recurrent weight matrix.
The existing TD policy learns to use (or ignore) the discretised trace. The
fixed deterministic feature projections are deliberately agnostic to world
semantics; no private scorer information or future action/outcome is read.

Its proposals on tick t encode evidence absorbed through tick t-1.
Consequently the current sensory observation cannot be copied straight into
the trace and an access lesion can isolate its effect on the policy.
"""
from __future__ import annotations

import hashlib
from typing import List

from ..kernel import Content, Organ


def projection(feature: str, channel: int) -> float:
    """Stable signed projection; Python hash() would break cross-process replay."""
    digest = hashlib.sha256(f"{channel}|{feature}".encode("utf-8")).digest()
    return 1.0 if digest[0] & 1 else -1.0


class Recurrent(Organ):
    name = "recurrent"
    home = ("continuity", "control")
    defaults = {"width": 4, "decay": 0.85, "threshold": 0.10, "salience": 0.55}

    def __init__(self, params):
        super().__init__(params)
        width = int(self.p["width"])
        decay = float(self.p["decay"])
        threshold = float(self.p["threshold"])
        if not 1 <= width <= 16:
            raise ValueError("recurrent.width must be in 1..16")
        if not 0.0 <= decay < 1.0:
            raise ValueError("recurrent.decay must be in [0, 1)")
        if not 0.0 < threshold < 1.0:
            raise ValueError("recurrent.threshold must be in (0, 1)")
        if float(self.p["salience"]) < 0.0:
            raise ValueError("recurrent.salience must be nonnegative")
        self.state = [0.0] * width

    def reset_episode(self) -> None:
        self.state = [0.0] * len(self.state)

    def propose(self, sense, ctx) -> List[Content]:
        out = []
        for i, value in enumerate(self.state):
            if abs(value) >= self.p["threshold"]:
                out.append(Content(
                    self.name, f"trace{i}", "pos" if value > 0 else "neg",
                    float(self.p["salience"]) * abs(value)))
        return out

    def learn(self, prev, now, view, ctx) -> None:
        # Only *selected* perception contents: an unbroadcast percept cannot
        # bypass the bottleneck by entering the trace through the back door.
        # Exclude our own contents, avoiding feedback from a proposal to itself.
        public = sorted({c.feature for c in view if c.source == "perception"})
        # The previous action's public outcome is delivered at this tick.
        # It is not the outcome of the action the policy is about to choose.
        if prev is not None and prev.action is not None and now.outcome is not None:
            public.append(f"prior_action={prev.action}|outcome={now.outcome}")
        rate = 1.0 - float(self.p["decay"])
        for i, old in enumerate(self.state):
            evidence = sum(projection(f, i) for f in public) / len(public) if public else 0.0
            self.state[i] = float(self.p["decay"]) * old + rate * evidence

    def introspect(self):
        return {"trace": list(self.state)}
