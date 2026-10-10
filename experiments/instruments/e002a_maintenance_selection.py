"""E002a one-slot maintenance-policy INSTRUMENT, not an agent experiment.

All policies have exactly one optional compute slot and the same task list.
No wall-clock background process, LLM, self or consciousness is simulated.
Values are synthetic forecasts. actual_ratio determines evaluator payoff,
which is never used by a policy. No estimator-accuracy claim.
"""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Task:
    name: str
    deadline: int
    estimated_gain: float
    actual_ratio: float
    compute_units: int = 1


def _check(tasks, cost=0.0):
    if not isinstance(cost, (float, int)) or not isfinite(cost) or cost < 0:
        raise ValueError('invalid compute cost')
    names = [t.name for t in tasks]
    if len(names) != len(set(names)):
        raise ValueError('duplicate task id')
    for t in tasks:
        if not t.name or not isinstance(t.deadline, int) or t.deadline < 0:
            raise ValueError('invalid task')
        if not isfinite(t.estimated_gain) or not isfinite(t.actual_ratio):
            raise ValueError('invalid gain')
        if t.estimated_gain < 0 or t.actual_ratio < 0 or t.compute_units != 1:
            raise ValueError('invalid task parameter')


def choose_fixed(tasks):
    """Deterministic pre-registered fixed index (one optional compute slot)."""
    _check(tasks)
    return tasks[0].name if tasks else None


def choose_deadline(tasks):
    """Earliest-deadline-first simple priority queue baseline."""
    _check(tasks)
    return min(tasks, key=lambda t: (t.deadline, t.name)).name if tasks else None


def choose_expected_value(tasks, cost=0.0):
    """One-step forecast-based compute selection; no evaluator truth access."""
    _check(tasks, cost)
    if not tasks:
        return None
    selected = max(tasks, key=lambda t: (t.estimated_gain, t.name))
    return selected.name if selected.estimated_gain > cost else None


def expected_outcome(tasks, selection, cost=0.0):
    """Evaluator-only expected incremental decision value, not observed reward."""
    _check(tasks, cost)
    if selection is None:
        return 0.0
    chosen = next((t for t in tasks if t.name == selection), None)
    if chosen is None:
        raise ValueError('unrecognized action')
    return chosen.estimated_gain * chosen.actual_ratio - cost


def compare(tasks, cost=0.0):
    """Equal one-slot budgets; no runtime or model-cognition comparison."""
    _check(tasks, cost)
    policies = {'fixed': choose_fixed(tasks),
                'deadline': choose_deadline(tasks),
                'estimated_value': choose_expected_value(tasks, cost)}
    return {name: {'action': action,
                   'expected_incremental_utility': expected_outcome(tasks, action, cost)}
            for name, action in policies.items()}


if __name__ == '__main__':
    demo = [Task('first', 5, 0.7, 0.1), Task('soon', 1, 2.0, 0.2), Task('valuable', 3, 5.0, 0.5)]
    print(compare(demo, cost=0.1))
    print('Synthetic instrument check only; no model trial, real compute schedule or empirical outcome')
