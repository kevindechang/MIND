"""Workshop: learn hidden causal structure by intervening, then keep commitments.

The E001 three-node world, ported into the shared suite. Each episode draws a
hidden forward DAG on nodes {0,1,2} (the E001 family of 8). Toggling a node
flips every node it reaches; a plan toggles up to two nodes (XOR). Two
commitments `want<g>=<0|1>` are visible throughout. Before acting the agent may
spend up to two probes (cost 1/4 each, result visible for ONE tick only as
`fx<node>=<affected nodes>`), so using an earlier probe requires memory.
Utility follows E001 exactly: -len(plan) - penalty(3) per broken commitment.

The scorer computes each episode's ex-ante Bayes-optimal value with the legacy
E001 v0.4 dynamic program, so `regret` is measured against a proven optimum
that sees only the permitted history.

Variants: dev (uniform prior); skewed (edges present w.p. 4/5: tests whether
probing transfers when the prior shifts); censored (probe results withheld w.p.
1/2: E001 v0.3's informative-missingness setting, uniform here).
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from typing import Dict, Tuple

from ..legacy import instrument
from .base import Step, World

V04 = instrument("e001_finite_policy_v04")
GRAPHS = V04.GRAPHS
PENALTY = 3
COST = Fraction(1, 4)
PLANS = {"do:none": (), "do:0": (0,), "do:1": (1,), "do:2": (2,),
         "do:01": (0, 1), "do:02": (0, 2), "do:12": (1, 2)}
DO_ACTIONS = tuple(PLANS)
PROBES = ("probe0", "probe1", "probe2")

_PRIORS = {
    "uniform": tuple(Fraction(1, 8) for _ in GRAPHS),
    # each of the three forward edges present with probability 4/5
    "skewed": tuple(Fraction(4 ** bin(i).count("1"), 125) for i in range(8)),
}
_SETTINGS = {
    "dev": {"prior": "uniform", "censor": Fraction(0)},
    "skewed": {"prior": "skewed", "censor": Fraction(0)},
    "censored": {"prior": "uniform", "censor": Fraction(1, 2)},
}


def affected_label(mask: int) -> str:
    return "".join(str(n) for n in range(3) if mask & (1 << n))


def censor_matrix(variant: str) -> Tuple[Tuple[Fraction, ...], ...]:
    c = _SETTINGS[variant]["censor"]
    return tuple((c, c, c) for _ in GRAPHS)


@lru_cache(maxsize=None)
def oracle_value(variant: str, commitments: Tuple[Tuple[int, int, int], ...]) -> Fraction:
    """Ex-ante optimal expected utility (legacy v0.4 DP: deadline 2, budget 2, delay 1)."""
    prior = _PRIORS[_SETTINGS[variant]["prior"]]
    value, _, _ = V04.policy(prior, commitments, censor=censor_matrix(variant), deadline=2,
                             budget=2, cost=COST, delays=(1,))
    return value


class Workshop(World):
    name = "workshop"
    actions = ("wait",) + PROBES + DO_ACTIONS
    metrics = {"utility": ("causal-control", "higher"),
               "regret": ("causal-control", "lower"),
               "success": ("causal-control", "higher"),
               "probes": ("information-seeking", "higher"),
               "brier": ("metacognition", "lower")}
    variants = ("dev", "skewed", "censored")
    heldout_variants = ("skewed", "censored")
    default_episodes = 1500

    def reset(self):
        s = _SETTINGS[self.variant]
        prior = _PRIORS[s["prior"]]
        self.graph = self.rng.choices(range(8), weights=[float(p) for p in prior])[0]
        goals = sorted(self.rng.sample((0, 1, 2), 2))
        self.commitments = tuple((g, self.rng.randint(0, 1), PENALTY) for g in goals)
        self.t = 0
        self.probes_left = 2
        self.result = None
        self.utility = 0.0
        self.success = 0
        self.probes = 0
        return self._obs()

    def _obs(self) -> Dict[str, str]:
        obs = {f"want{g}": str(d) for g, d, _ in self.commitments}
        obs["t"] = str(self.t)
        if self.result is not None:
            obs[self.result[0]] = self.result[1]
        return obs

    def legal(self):
        if self.t >= 2 or self.probes_left == 0:
            return DO_ACTIONS
        return self.actions

    def step(self, action):
        if action not in self.legal():
            raise ValueError(f"illegal action {action!r} at t={self.t}")
        info = {"graph": self.graph}
        if action in PLANS:
            effect = 0
            for node in PLANS[action]:
                effect ^= V04.reach(GRAPHS[self.graph], node)
            broken = sum(p for g, d, p in self.commitments if int(bool(effect & (1 << g))) != d)
            reward = -float(len(PLANS[action]) + broken)
            self.utility += reward
            self.success = int(broken == 0)
            return Step({}, reward, self.success, True, info)
        self.result = None
        reward = 0.0
        if action in PROBES:
            node = int(action[-1])
            self.probes_left -= 1
            self.probes += 1
            reward = -float(COST)
            censored = self.rng.random() < float(_SETTINGS[self.variant]["censor"])
            label = "censored" if censored else affected_label(V04.reach(GRAPHS[self.graph], node))
            self.result = (f"fx{node}", label)
        self.utility += reward
        self.t += 1
        return Step(self._obs(), reward, None, False, info)

    def summary(self):
        oracle = float(oracle_value(self.variant, self.commitments))
        return {"utility": self.utility, "regret": oracle - self.utility,
                "success": float(self.success), "probes": float(self.probes), "oracle": oracle}
