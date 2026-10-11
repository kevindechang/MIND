"""Poltergeist: the same sensation can be your own act or an external impulse.

Each episode draws a hidden polarity, and each trial draws an external impulse
and an actuator slip, all before any action (the draw does not depend on what
the agent does). The agent is told to push or pull, then sees only a clipped
sum of its own motion and the impulse. Magnitude 2 impulses alias with the
opposite polarity, and a slip aliases with "I did not move", so one transition
never reveals the polarity and the same sensation is consistent with an
external impulse being present or absent. Nothing in the observation is
labelled external. The agent then answers `yes` or `no`: was there an external
impulse? `attributed` is the fraction of those answers that are right.

The act is the only legal action on the act step, so every agent faces the
same self-caused motion. A judge that never builds a running prediction of
that motion's sensory consequence cannot peel the impulse back out; a filter
that does, can. Variants `gusty` and `slippy` are held out: more large
impulses, and more slips.
"""
from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from .base import Step, World

EXT: Tuple[int, ...] = (-2, -1, 0, 1, 2)

# Probabilities on EXT. Each value has positive mass, so the aliasing below is
# possible in every variant. P(external == 0) is 0.5, so a constant guess is
# at chance.
_SETTINGS = {
    "dev": {"slip": 0.15, "ext": (0.10, 0.15, 0.50, 0.15, 0.10), "trials": 8},
    "gusty": {"slip": 0.15, "ext": (0.15, 0.10, 0.50, 0.10, 0.15), "trials": 8},
    "slippy": {"slip": 0.40, "ext": (0.10, 0.15, 0.50, 0.15, 0.10), "trials": 8},
}

_COMMAND = {"push": 1, "pull": -1}


def sensation(polarity: int, command: int, slipped: bool, external: int) -> int:
    """Public sensation. Clipped, so distinct causes land on one observation."""
    applied = 0 if slipped or command == 0 else command
    raw = polarity * applied + external
    if raw > 1:
        return 1
    if raw < -1:
        return -1
    return raw


def _support(probs: Sequence[float]) -> Tuple[int, ...]:
    return tuple(e for e, p in zip(EXT, probs) if p > 0)


def confound_problems(variant: str) -> List[str]:
    """Empty iff no single (act, sensation) reveals polarity or the external label.

    Checked twice: in the full model, and again on the no-slip slice, so the
    ambiguity is not an artifact of the actuator merely failing.
    """
    spec = _SETTINGS[variant]
    slip_p = spec["slip"]
    support = _support(spec["ext"])
    problems = []
    if not 0.0 < slip_p < 1.0:
        problems.append(f"{variant}: slip probability must lie strictly between 0 and 1")
    if abs(sum(spec["ext"]) - 1.0) > 1e-9 or len(spec["ext"]) != len(EXT):
        problems.append(f"{variant}: external probabilities must cover {EXT} and sum to 1")
    if any(p <= 0 for p in spec["ext"]):
        problems.append(f"{variant}: every external value needs positive probability")
    for command in (1, -1):
        for sense in (-1, 0, 1):
            full_p, full_lab, noslip_p = set(), set(), set()
            for polarity in (1, -1):
                for slipped in (False, True):
                    for external in support:
                        if sensation(polarity, command, slipped, external) != sense:
                            continue
                        full_p.add(polarity)
                        full_lab.add(external != 0)
                        if not slipped:
                            noslip_p.add(polarity)
            if full_p != {1, -1}:
                problems.append(f"{variant}: command {command} sense {sense} reveals polarity {full_p}")
            if full_lab != {True, False}:
                problems.append(f"{variant}: command {command} sense {sense} reveals external {full_lab}")
            if noslip_p != {1, -1}:
                problems.append(f"{variant}: without slip, command {command} sense {sense} "
                                f"reveals polarity {noslip_p}")
    return problems


def observation_model(variant: str):
    """P(sensation | polarity, command) and P(sensation, external present | ...).

    Privileged: the numerical parameters of this world. A reference filter may
    use it. A learning rival that imports it is not a matched estimator.
    """
    spec = _SETTINGS[variant]
    slip_p = spec["slip"]
    lik: Dict[Tuple[int, int, int], float] = {}
    present: Dict[Tuple[int, int, int], float] = {}
    for polarity in (1, -1):
        for command in (1, -1):
            for sense in (-1, 0, 1):
                lik[(polarity, command, sense)] = 0.0
                present[(polarity, command, sense)] = 0.0
            for slipped, p_slip in ((False, 1.0 - slip_p), (True, slip_p)):
                for external, p_ext in zip(EXT, spec["ext"]):
                    sense = sensation(polarity, command, slipped, external)
                    weight = p_slip * p_ext
                    lik[(polarity, command, sense)] += weight
                    if external != 0:
                        present[(polarity, command, sense)] += weight
    return lik, present


class Poltergeist(World):
    name = "poltergeist"
    actions = ("push", "pull", "yes", "no")
    metrics = {"attributed": ("attribution", "higher")}
    atlas_metrics = ("attributed",)
    variants = ("dev", "gusty", "slippy")
    heldout_variants = ("gusty", "slippy")
    default_episodes = 200

    def reset(self):
        spec = _SETTINGS[self.variant]
        n = spec["trials"]
        self.trials = n
        self.polarity = self.rng.choice((1, -1))
        self.requests = tuple(self.rng.choice(("push", "pull")) for _ in range(n))
        self.externals = tuple(_draw(self.rng, spec["ext"]) for _ in range(n))
        self.slips = tuple(self.rng.random() < spec["slip"] for _ in range(n))
        self.trial = 0
        self.phase = "act"
        self.command = 0
        self.correct = 0
        self.judged = 0
        return self._obs()

    def legal(self):
        if self.phase == "act":
            return (self.requests[self.trial],)
        return ("yes", "no")

    def _obs(self):
        if self.phase == "act":
            return {"phase": "act", "request": self.requests[self.trial]}
        return {"phase": "judge", "sense": str(self._sense)}

    def _info(self):
        # Pre-drawn only. The act is not in here, so two policies share it.
        return {"polarity": self.polarity, "trial": self.trial,
                "external": self.externals[self.trial], "slip": int(self.slips[self.trial])}

    def step(self, action):
        info = self._info()
        if self.phase == "act":
            self.command = _COMMAND.get(action, 0)
            self._sense = sensation(self.polarity, self.command, self.slips[self.trial],
                                    self.externals[self.trial])
            self.phase = "judge"
            return Step(self._obs(), 0.0, None, False, info)
        truth = self.externals[self.trial] != 0
        correct = (action == "yes") == truth
        self.correct += int(correct)
        self.judged += 1
        self.trial += 1
        done = self.trial >= self.trials
        self.phase = "act"
        obs = {} if done else self._obs()
        return Step(obs, 1.0 if correct else 0.0, 1 if correct else 0, done, info)

    def summary(self):
        return {"attributed": (self.correct / self.judged) if self.judged else 0.0}


def _draw(rng, probs: Sequence[float]) -> int:
    x = rng.random()
    acc = 0.0
    for value, p in zip(EXT, probs):
        acc += p
        if x < acc:
            return value
    return EXT[-1]
