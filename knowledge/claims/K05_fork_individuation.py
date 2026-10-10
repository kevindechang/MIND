"""Ledger forks (E100 Day 7, generalised): one origin, two lives, two individuals.

Fork a living organism's ledger; continue one copy with experience X, a second
with experience Y, a third again with X. The X-twins stay byte-identical (the
organism is fully determined by its history); the X/Y pair comes to act
differently in identical situations. This does NOT show either fork is 'the
same mind' or 'a different mind' — only that individuation tracks experience.
"""
from mind.claims import Check, Claim


def _live(org, world, seed, episodes):
    from mind.worlds import make_world
    env = make_world(world, seed)
    for _ in range(episodes):
        obs = env.reset()
        r, o, b = 0.0, None, True
        while True:
            d = org.step(obs, r, o, b, env.legal())
            s = env.step(d.action)
            if s.done:
                org.end_episode(s.reward, s.outcome)
                break
            obs, r, o, b = s.obs, s.reward, s.outcome, False


def individuation(ctx):
    from mind.kernel import Organism
    from mind.ledger import MemoryLedger
    from mind.stats import bootstrap_ci
    actions = ("wait", "a", "b", "c")
    divergence, twins_identical = [], True
    for seed in ctx.seeds:
        led = MemoryLedger()
        org = Organism("organism", seed, led)
        _live(org, "vigil", seed, 60)
        probes = sorted({tuple(sorted(t.split(":", 1)[1] for t in e.payload["ws"]))
                         for e in led if e.kind == "tick"})
        fx, fy, fx2 = led.fork(), led.fork(), led.fork()
        x, y, x2 = Organism.restore(fx), Organism.restore(fy), Organism.restore(fx2)
        _live(x, "vigil", 50_000 + seed, 60)
        _live(y, "vigil", 90_000 + seed, 60)
        _live(x2, "vigil", 50_000 + seed, 60)
        twins_identical &= fx.head == fx2.head
        divergence.append(sum(x.greedy(p, actions) != y.greedy(p, actions) for p in probes) / len(probes))
    m, lo, hi = bootstrap_ci(divergence, seed="fork")
    ok = twins_identical and lo > 0
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True, "twins_identical": twins_identical,
            "divergence": m, "lo": lo, "hi": hi,
            "summary": f"same-experience forks identical: {twins_identical}; different-experience forks "
                       f"disagree on {m:.1%} [{lo:.1%}, {hi:.1%}] of shared situations"}


CLAIM = Claim(
    id="K05",
    title="Forks individuate by experience: identical lives stay identical, different lives diverge",
    statement="Forks of one ledger continued with the same experience remain byte-identical; forks continued "
              "with different experience choose different actions in a reliably non-zero fraction of "
              "situations from their shared past.",
    kind="invariant",
    scope="L2",
    test=Check(individuation, seeds=12),
    question="H007",
    depends_on=("K01",),
    extends=("L02",),
    by="pipeline-v2",
    retired='v2 review (2026-10-10): divergence after different experience is by construction (different data, different weights) and twin identity is already covered by K01. Retired without successor.',
    created="2026-10-10",
    rationale="E100 Day 7 asked for this; v1's version injected the divergence by hand (PR #12).",
)
