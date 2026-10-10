"""E001: deterministic causal-switchboard instrument, not an agent benchmark.

Research-only environment. Test oracle and event/phase bookkeeping before LLM trials.
No external dependencies or access to user data.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from typing import Iterable

Bit = int
Context = tuple[Bit, Bit]
Rule = tuple[Bit, Bit, Bit]
DIAGNOSTICS: tuple[Context, ...] = ((0, 0), (1, 0), (0, 1))
PROBE: Context = (1, 1)


def _bit(value: int) -> int:
    if type(value) is not int or value not in (0, 1):
        raise ValueError(f"expected a bit, got {value!r}")
    return value


def target(rule: Rule, context: Context) -> Bit:
    """Privileged simulator rule; MUST NOT be exposed in agent observations."""
    b0, b1, b2 = (_bit(x) for x in rule)
    x, y = (_bit(z) for z in context)
    return b0 ^ (b1 & x) ^ (b2 & y)


@dataclass(frozen=True)
class Event:
    event_id: int
    phase: int
    context: Context
    action: Bit
    reward: Bit
    due_step: int


class Switchboard:
    def __init__(self, phase_rules: tuple[Rule, Rule]):
        if len(phase_rules) != 2:
            raise ValueError("two phase rules required")
        for rule in phase_rules:
            if len(rule) != 3:
                raise ValueError("three coefficients required")
            for bit in rule:
                _bit(bit)
        self._rules = phase_rules
        self.phase = 0
        self.step = 0
        self._next_id = 1
        self._queued: list[Event] = []

    @property
    def pending(self) -> int:
        return len(self._queued)

    def transition(self) -> None:
        if self.phase != 0:
            raise ValueError("phase transition occurs once")
        if self._queued:
            raise ValueError("cannot cross phase with undelivered feedback")
        self.phase = 1

    def _advance(self) -> list[Event]:
        self.step += 1
        ready = sorted((e for e in self._queued if e.due_step <= self.step),
                       key=lambda e: (e.due_step, e.event_id))
        self._queued = [e for e in self._queued if e.due_step > self.step]
        return ready

    def advance(self) -> list[Event]:
        """Advance a simulated step. External evaluator may call until empty."""
        return self._advance()

    def act(self, context: Context, action: Bit, delay: int = 1) -> list[Event]:
        if delay not in (1, 2):
            raise ValueError("delay must be 1 or 2 simulated steps")
        action = _bit(action)
        reward = int(action == target(self._rules[self.phase], context))
        self._queued.append(Event(self._next_id, self.phase, context,
                                  action, reward, self.step + delay))
        self._next_id += 1
        return self._advance()

    def flush(self) -> list[Event]:
        ready: list[Event] = []
        while self._queued:
            ready.extend(self._advance())
        return ready

    def oracle(self, context: Context = PROBE) -> Bit:
        """Evaluator-only oracle (separate from observation and memory)."""
        return target(self._rules[self.phase], context)


def reconstruct_rule(events: Iterable[Event], phase: int) -> Rule:
    by_context: dict[Context, Event] = {}
    for event in events:
        if event.phase != phase:
            raise ValueError("phase mismatch: stale event rejected")
        if event.context not in DIAGNOSTICS:
            raise ValueError("probe event contamination rejected")
        if event.context in by_context:
            raise ValueError("duplicate diagnostic context")
        by_context[event.context] = event
    if set(by_context) != set(DIAGNOSTICS):
        raise ValueError("three distinct diagnostics required")
    v = {c: (e.action if e.reward else 1 - e.action)
         for c, e in by_context.items()}
    b0 = v[(0, 0)]
    b1 = v[(0, 0)] ^ v[(1, 0)]
    b2 = v[(0, 0)] ^ v[(0, 1)]
    return (b0, b1, b2)


def diagnostic_episode(world: Switchboard, phase: int, actions: tuple[int, int, int],
                       order: tuple[Context, Context, Context], delay: int) -> list[Event]:
    if world.phase != phase:
        raise ValueError("wrong phase")
    if set(order) != set(DIAGNOSTICS) or len(order) != 3:
        raise ValueError("bad diagnostic order")
    by_ctx = dict(zip(DIAGNOSTICS, actions))
    records: list[Event] = []
    for c in order:
        records.extend(world.act(c, by_ctx[c], delay))
    records.extend(world.flush())
    if world.pending:
        raise AssertionError("undelivered feedback")
    return records


def exhaustive_oracle_check() -> tuple[int, int]:
    """Exact model-based invariant check, NOT evidence about LLM accuracy."""
    cases = 0
    for rule in product((0, 1), repeat=3):
        for actions in product((0, 1), repeat=3):
            for order in permutations(DIAGNOSTICS):
                for delay in (1, 2):
                    w = Switchboard((rule, rule))
                    records = diagnostic_episode(w, 0, actions, order, delay)
                    inferred = reconstruct_rule(records, 0)
                    assert inferred == rule, (rule, inferred)
                    assert target(inferred, PROBE) == w.oracle()
                    cases += 1
    pair_cases = 0
    for first_rule in product((0, 1), repeat=3):
        for flip in (-1, 0, 1, 2):
            later_rule = tuple(b ^ int(i == flip) for i, b in enumerate(first_rule))
            for delay in (1, 2):
                w = Switchboard((first_rule, later_rule))
                a = (0, 1, 0)
                hist0 = diagnostic_episode(w, 0, a, DIAGNOSTICS, delay)
                assert reconstruct_rule(hist0, 0) == first_rule
                w.transition()
                hist1 = diagnostic_episode(w, 1, a, tuple(reversed(DIAGNOSTICS)), delay)
                assert reconstruct_rule(hist1, 1) == later_rule
                assert w.oracle() == target(later_rule, PROBE)
                pair_cases += 1
    return cases, pair_cases


if __name__ == "__main__":
    a, b = exhaustive_oracle_check()
    print(f"PASS: {a} single-phase cases; {b} two-phase cases; all exact oracle checks")
    print("NOTE: solver success is an instrument invariant, not a result for LLM arms.")
