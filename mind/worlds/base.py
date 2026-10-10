"""World protocol shared by every environment in the suite.

A world is seeded, partially observable and episodic. Each step returns what
the agent may see (obs, reward, a public success `outcome` for the action just
taken) separately from `info`, which is PRIVATE to the scorer and never reaches
any agent. Every agent -- organism configuration or rival -- meets the same
interface, so one world automatically evaluates all of them.

To contribute a world: subclass World, declare its metrics with the competency
each one measures, provide at least one held-out variant, register it in
worlds/__init__.py, and run `python -m mind check`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Any, Dict, Optional, Tuple


@dataclass
class Step:
    obs: Dict[str, str]
    reward: float
    outcome: Optional[int]          # public: did the action just taken succeed?
    done: bool
    info: Dict[str, Any] = field(default_factory=dict)   # PRIVATE to the scorer


class World:
    name = "world"
    actions: Tuple[str, ...] = ("wait",)
    # metric -> (competency it measures, "higher" or "lower" is better)
    metrics: Dict[str, Tuple[str, str]] = {}
    # Non-redundant metrics for the integration atlas: one per competency, no metric that is
    # a re-labelling of another (vigil.reward ~ kept, workshop.regret ~ utility), and
    # same-stream calibration instead of raw Brier (v2 review, findings 1 and 7).
    atlas_metrics: Tuple[str, ...] = ()
    variants: Tuple[str, ...] = ("dev",)
    heldout_variants: Tuple[str, ...] = ()
    default_episodes = 200

    def __init__(self, seed: int, variant: str = "dev"):
        if variant not in self.variants:
            raise ValueError(f"{self.name}: unknown variant {variant!r}; choose {self.variants}")
        self.seed = seed
        self.variant = variant
        self.rng = random.Random(f"world|{self.name}|{variant}|{seed}")

    def reset(self) -> Dict[str, str]:
        raise NotImplementedError

    def legal(self) -> Tuple[str, ...]:
        return self.actions

    def step(self, action: str) -> Step:
        raise NotImplementedError

    def summary(self) -> Dict[str, float]:
        """Per-episode metrics, called once after the episode ends."""
        return {}
