"""Paired bootstrap estimation and three-valued verdicts.

The rule "a nonsignificant difference is not equivalence" is enforced here:
equivalence HOLDS only when the whole confidence interval lies inside the
declared margin; an interval that straddles it is INCONCLUSIVE.
"""
from __future__ import annotations

import random
from typing import Dict, Sequence, Tuple

HOLDS, FAILS, INCONCLUSIVE = "HOLDS", "FAILS", "INCONCLUSIVE"


def mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs)


def bootstrap_ci(xs: Sequence[float], resamples: int = 4000, level: float = 0.95,
                 seed: str = "mind") -> Tuple[float, float, float]:
    """Percentile bootstrap CI of the mean. Deterministic given `seed`."""
    xs = list(xs)
    if not xs:
        raise ValueError("no observations")
    m = mean(xs)
    if len(xs) == 1 or min(xs) == max(xs):
        return m, m, m
    rng = random.Random(seed)
    n = len(xs)
    means = sorted(sum(xs[rng.randrange(n)] for _ in range(n)) / n for _ in range(resamples))
    lo = means[int((1 - level) / 2 * resamples)]
    hi = means[min(resamples - 1, int((1 + level) / 2 * resamples))]
    return m, lo, hi


def compare(a: Sequence[float], b: Sequence[float], direction: str, margin: float,
            seed: str = "mind") -> Dict:
    """Paired claim about mean(a - b).

    '>'  : a exceeds b by more than `margin`
    '<'  : a falls below b by more than `margin`
    '~'  : |a - b| < margin (equivalence; requires the full CI inside the band)
    """
    if len(a) != len(b):
        raise ValueError("paired samples must have equal length")
    diffs = [x - y for x, y in zip(a, b)]
    m, lo, hi = bootstrap_ci(diffs, seed=seed)
    if direction == ">":
        verdict = HOLDS if lo > margin else FAILS if hi <= margin else INCONCLUSIVE
    elif direction == "<":
        verdict = HOLDS if hi < -margin else FAILS if lo >= -margin else INCONCLUSIVE
    elif direction == "~":
        if -margin < lo and hi < margin:
            verdict = HOLDS
        elif lo >= margin or hi <= -margin:
            verdict = FAILS
        else:
            verdict = INCONCLUSIVE
    else:
        raise ValueError(f"unknown direction {direction!r}")
    return {"verdict": verdict, "diff": m, "lo": lo, "hi": hi, "n": len(diffs),
            "a": mean(a), "b": mean(b)}


def threshold(xs: Sequence[float], op: str, value: float, seed: str = "mind") -> Dict:
    m, lo, hi = bootstrap_ci(xs, seed=seed)
    if op == ">=":
        verdict = HOLDS if lo >= value else FAILS if hi < value else INCONCLUSIVE
    elif op == "<=":
        verdict = HOLDS if hi <= value else FAILS if lo > value else INCONCLUSIVE
    else:
        raise ValueError(f"unknown operator {op!r}")
    return {"verdict": verdict, "mean": m, "lo": lo, "hi": hi, "n": len(xs)}
