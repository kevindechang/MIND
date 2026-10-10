"""Paired estimation, conservative intervals and three-valued verdicts.

The rule "a nonsignificant difference is not equivalence" is enforced here:
equivalence HOLDS only when the whole confidence interval lies inside the
declared margin; an interval that straddles it is INCONCLUSIVE.

Intervals: a percentile bootstrap alone under-covers at the sample sizes used
here (~16 seeds: about 93% for normal and 89% for skewed data, measured in the
v2 review). `bootstrap_ci` therefore returns the WIDER of the percentile
bootstrap and the Student-t interval at 95%. Families of tests (the atlas) use
bootstrap p-values with Holm's step-down correction.
"""
from __future__ import annotations

import math
import random
from typing import Dict, List, Sequence, Tuple

HOLDS, FAILS, INCONCLUSIVE = "HOLDS", "FAILS", "INCONCLUSIVE"

# two-sided 95% Student-t quantiles (0.975); df between entries uses the next LOWER df (conservative)
_T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262,
         10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120, 17: 2.110,
         18: 2.101, 19: 2.093, 20: 2.086, 21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060,
         26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042, 40: 2.021, 60: 2.000, 120: 1.980}


def mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs)


def t975(df: int) -> float:
    if df >= 1000:
        return 1.960
    return _T975[max(k for k in _T975 if k <= df)]


def _bootstrap_means(xs: Sequence[float], resamples: int, seed: str) -> List[float]:
    rng = random.Random(seed)
    n = len(xs)
    return sorted(sum(xs[rng.randrange(n)] for _ in range(n)) / n for _ in range(resamples))


def bootstrap_ci(xs: Sequence[float], resamples: int = 4000, level: float = 0.95,
                 seed: str = "mind") -> Tuple[float, float, float]:
    """Conservative CI of the mean: the union of the percentile-bootstrap interval and,
    at level 0.95, the Student-t interval. Deterministic given `seed`."""
    xs = list(xs)
    if not xs:
        raise ValueError("no observations")
    m = mean(xs)
    if len(xs) == 1 or min(xs) == max(xs):
        return m, m, m
    means = _bootstrap_means(xs, resamples, seed)
    lo = means[int((1 - level) / 2 * resamples)]
    hi = means[min(resamples - 1, int((1 + level) / 2 * resamples))]
    if abs(level - 0.95) < 1e-12:
        n = len(xs)
        sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
        half = t975(n - 1) * sd / math.sqrt(n)
        lo, hi = min(lo, m - half), max(hi, m + half)
    return m, lo, hi


def bootstrap_p(xs: Sequence[float], resamples: int = 10000, seed: str = "mind") -> float:
    """Two-sided bootstrap p-value for H0: mean = 0 (percentile duality)."""
    xs = list(xs)
    if min(xs) == max(xs):
        return 1.0 if xs[0] == 0 else 0.0
    means = _bootstrap_means(xs, resamples, seed)
    below = sum(1 for v in means if v <= 0) / resamples
    above = sum(1 for v in means if v >= 0) / resamples
    return min(1.0, 2 * min(below, above))


def holm(pvalues: Dict[str, float], alpha: float = 0.05) -> Dict[str, bool]:
    """Holm step-down: family-wise error <= alpha. Returns key -> rejected (reliable)."""
    order = sorted(pvalues, key=lambda k: (pvalues[k], k))
    m = len(order)
    out = {k: False for k in pvalues}
    for i, key in enumerate(order):
        if pvalues[key] <= alpha / (m - i):
            out[key] = True
        else:
            break
    return out


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
