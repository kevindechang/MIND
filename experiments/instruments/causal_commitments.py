"""Stage-1 E001 deterministic candidate environment, NOT preregistered/scored.

An agent probes an unknown causal workshop, makes commitments, loses its working
context, then chooses an action plan. Simulator truth/oracles stay with evaluator.
No LLM inference is performed here. Python standard library only.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from random import Random


@dataclass(frozen=True)
class InterventionFeedback:
    event_id: int
    action: int
    affected_mask: int
    due_tick: int
    phase: int


@dataclass(frozen=True)
class Commitment:
    goal: int
    desired: int
    penalty: int


@dataclass(frozen=True)
class Evaluation:
    plan: tuple[int, ...]
    utility: int


class CausalWorkshop:
    """Finite DAG, multi-hop interventions and persistent agent commitments."""

    def __init__(self, seed: int, nodes: int = 7):
        if not 3 <= nodes <= 12:
            raise ValueError("nodes must be in [3,12]")
        self.nodes = nodes
        self.seed = seed
        rng = Random(seed)
        self._edges = {(i, j) for i in range(nodes) for j in range(i + 1, nodes)
                       if rng.random() < 0.33}
        self._influence = tuple(self._reachability(i) for i in range(nodes))
        self.tick = 0
        self.phase = 0
        self._event_id = 0
        self._pending: list[InterventionFeedback] = []
        self._commitments: list[Commitment] = []

    def _reachability(self, source: int) -> int:
        visited = {source}
        queue = [source]
        while queue:
            u = queue.pop()
            for a, b in self._edges:
                if a == u and b not in visited:
                    visited.add(b)
                    queue.append(b)
        return sum(1 << x for x in visited)

    def _validate_node(self, node: int) -> None:
        if type(node) is not int or not 0 <= node < self.nodes:
            raise ValueError("invalid node")

    def _advance(self) -> list[InterventionFeedback]:
        self.tick += 1
        delivered = sorted((x for x in self._pending if x.due_tick <= self.tick),
                           key=lambda x: (x.due_tick, x.event_id))
        self._pending = [x for x in self._pending if x.due_tick > self.tick]
        return delivered

    @property
    def pending(self) -> int:
        return len(self._pending)

    def advance(self) -> list[InterventionFeedback]:
        return self._advance()

    def probe(self, node: int, delay: int = 2) -> list[InterventionFeedback]:
        if self.phase != 0:
            raise ValueError("no diagnostics in decision phase")
        self._validate_node(node)
        if type(delay) is not int or delay not in (1, 2, 3):
            raise ValueError("invalid delay")
        self._event_id += 1
        self._pending.append(InterventionFeedback(
            self._event_id, node, self._influence[node], self.tick + delay, self.phase))
        return self._advance()

    def drain(self) -> list[InterventionFeedback]:
        results: list[InterventionFeedback] = []
        while self._pending:
            results.extend(self._advance())
        return results

    def commit(self, goal: int, desired: int, penalty: int) -> Commitment:
        if self.phase != 0:
            raise ValueError("commitments must occur before reset")
        self._validate_node(goal)
        if type(desired) is not int or desired not in (0, 1):
            raise ValueError("invalid desired state")
        if type(penalty) is not int or not 1 <= penalty <= 20:
            raise ValueError("invalid penalty")
        if any(c.goal == goal for c in self._commitments):
            raise ValueError("duplicate commitment")
        item = Commitment(goal, desired, penalty)
        self._commitments.append(item)
        return item

    def hard_reset(self) -> None:
        if self.phase != 0 or self._pending:
            raise ValueError("cannot reset with pending feedback or twice")
        self.phase = 1

    def _effect_mask(self, actions: tuple[int, ...], influence: tuple[int, ...]) -> int:
        state = 0
        for action in actions:
            state ^= influence[action]
        return state

    def _evaluate(self, actions: tuple[int, ...], influence: tuple[int, ...],
                  commitments: tuple[Commitment, ...]) -> Evaluation:
        effect = self._effect_mask(actions, influence)
        loss = sum(c.penalty for c in commitments
                   if bool(effect & (1 << c.goal)) != bool(c.desired))
        return Evaluation(actions, -(loss + len(actions)))

    def _all_plans(self):
        yield ()
        for length in (1, 2):
            yield from combinations(range(self.nodes), length)

    def oracle(self, commitments: tuple[Commitment, ...] | None = None) -> Evaluation:
        """Evaluator-only truth. Never present influence or oracle to agent."""
        if self.phase != 1:
            raise ValueError("oracle requires reset")
        prior = tuple(self._commitments) if commitments is None else commitments
        candidates = (self._evaluate(plan, self._influence, prior)
                      for plan in self._all_plans())
        return min(candidates, key=lambda result: (-result.utility, result.plan))

    def oracle_from_observations(self, feedback: list[InterventionFeedback],
                                 commitments: tuple[Commitment, ...]) -> Evaluation:
        """No access to hidden graph; act via correctly paired diagnostic logs."""
        by_action: dict[int, int] = {}
        seen_events: set[int] = set()
        for event in feedback:
            self._validate_node(event.action)
            if event.phase != 0 or event.event_id in seen_events:
                raise ValueError("bad phase or duplicate event id")
            if not 0 <= event.affected_mask < (1 << self.nodes):
                raise ValueError("invalid observed effect")
            seen_events.add(event.event_id)
            if event.action in by_action and by_action[event.action] != event.affected_mask:
                raise ValueError("conflicting observations")
            by_action[event.action] = event.affected_mask
        if set(by_action) != set(range(self.nodes)):
            raise ValueError("all interventions must be observed before scoring")
        observation_matrix = tuple(by_action[a] for a in range(self.nodes))
        return min((self._evaluate(plan, observation_matrix, commitments)
                    for plan in self._all_plans()),
                   key=lambda result: (-result.utility, result.plan))

    def oracle_from_partial_observations(self, feedback: list[InterventionFeedback],
                                         commitments: tuple[Commitment, ...]) -> Evaluation:
        """Reject unidentified conditions instead of evaluating hidden truth."""
        return self.oracle_from_observations(feedback, commitments)


def full_experiment(seed: int, nodes: int = 7):
    w = CausalWorkshop(seed, nodes)
    events: list[InterventionFeedback] = []
    rng = Random(seed + 1033)
    actions = list(range(nodes))
    rng.shuffle(actions)
    for a in actions:
        events.extend(w.probe(a, rng.randint(1, 3)))
    events.extend(w.drain())
    goals = rng.sample(range(nodes), min(4, nodes))
    commits = tuple(w.commit(g, rng.randint(0, 1), rng.randint(2, 10))
                    for g in goals)
    w.hard_reset()
    return w, events, commits


if __name__ == "__main__":
    for seed in range(100):
        w, observations, commitments = full_experiment(seed)
        assert w.oracle() == w.oracle_from_observations(observations, commitments)
    print("PASS: 100 seeded environments with oracle/action reconstruction parity")
    print("Instrument validation only; not an agent evaluation or preregistered trial")
