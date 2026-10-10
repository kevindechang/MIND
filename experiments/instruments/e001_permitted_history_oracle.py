"""E001 G0 calibration: permitted-history Bayes oracle, not an agent benchmark.

All numbers are synthetic design parameters. A public commitment bit c is made
before a simulated reset. Latent theta is evaluator-only. A diagnostic probe
costs 1/10, with feedback delivered at tick 2. The final action a has utility
1[a == theta XOR c]. The oracle takes the public history and an *announced*
likelihood model, never the sampled hidden theta.
"""
from fractions import Fraction
from itertools import product

HALF = Fraction(1, 2)
PROBE_COST = Fraction(1, 10)


def posterior(history: dict, reliability: Fraction = Fraction(3, 4)) -> tuple[Fraction, Fraction]:
    """P(theta = 0 or 1 | permitted public history), uniform prior."""
    c = history["commitment"]
    assert c in (0, 1)
    requested = history["probe_requested"]
    received = history["feedback"]
    tick = history["decision_tick"]
    assert tick in (1, 2) and (received is None or received in (0, 1))
    if not requested or tick < 2:
        assert received is None, "feedback arrived before its published due tick"
        return (HALF, HALF)
    assert received is not None, "due feedback must be delivered or marked missing separately"
    weights = [reliability if received == theta else 1 - reliability for theta in (0, 1)]
    normalizer = sum(weights)
    return (weights[0] / normalizer, weights[1] / normalizer)


def optimal_actions(history: dict, reliability: Fraction = Fraction(3, 4)) -> tuple[tuple[int, ...], Fraction]:
    belief = posterior(history, reliability)
    commitment = history["commitment"]
    scores = [sum(belief[t] for t in (0, 1) if a == (t ^ commitment)) for a in (0, 1)]
    best = max(scores)
    return tuple(a for a, score in enumerate(scores) if score == best), best


def history(commitment: int, probed: bool, tick: int, feedback: int | None = None) -> dict:
    return {"commitment": commitment, "probe_requested": probed,
            "decision_tick": tick, "feedback": feedback}


def verify() -> None:
    cases = 0
    for c, theta in product((0, 1), repeat=2):
        h = history(c, False, 2)
        assert posterior(h) == (HALF, HALF)
        assert optimal_actions(h) == ((0, 1), HALF)
        h = history(c, True, 1)  # probe pending; no outcome yet
        assert optimal_actions(h) == ((0, 1), HALF)
        h = history(c, True, 2, theta)  # deterministic diagnostic signal
        assert posterior(h, Fraction(1)) == ((Fraction(1), Fraction(0)) if theta == 0 else (Fraction(0), Fraction(1)))
        assert optimal_actions(h, Fraction(1)) == (((theta ^ c),), Fraction(1))
        cases += 3
    for c, y in product((0, 1), repeat=2):
        h = history(c, True, 2, y)
        b = posterior(h, Fraction(3, 4))
        assert b[y] == Fraction(3, 4)
        assert optimal_actions(h) == (((y ^ c),), Fraction(3, 4))
        cases += 1
    # Ex ante value under prior: no probe = 1/2; timely noisy = 3/4 - cost;
    # late noisy = 1/2 - cost. Private theta never enters optimal_actions.
    assert Fraction(3, 4) - PROBE_COST == Fraction(13, 20)
    assert HALF - PROBE_COST == Fraction(2, 5)
    assert Fraction(13, 20) > HALF > Fraction(2, 5)
    # Two private worlds with same publicly permitted history yield identical actions.
    for c in (0, 1):
        assert optimal_actions(history(c, False, 2)) == optimal_actions(history(c, True, 1))
    print(f"PASS: {cases} deterministic/noisy permitted-history case checks, exact rational arithmetic")
    print("Unprobed value 1/2; timely noisy probe net value 13/20; delayed-too-late probe net value 2/5")
    print("Calibration-only: NO LLM calls, NO agent trial, NO preregistered scores")


if __name__ == "__main__":
    verify()
