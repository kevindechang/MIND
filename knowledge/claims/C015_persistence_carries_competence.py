"""What persists across death is not a task but a learned individual.

Generalises the v1 Day 0 wipe control: an organism trained for 200 episodes is
killed; one copy is rebuilt from its ledger (continuity, K01), the other is
reborn with the same configuration and seed but no history. Both then live the
same 40 new episodes. The difference is everything the ledger carried.
"""
from mind.claims import Check, Claim


def _live(org, seed, episodes):
    from mind.worlds import make_world
    env = make_world("vigil", seed)
    kept = []
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
        kept.append(env.summary()["kept"])
    return sum(kept) / len(kept)


def persistence(ctx):
    from mind.kernel import Organism
    from mind.ledger import MemoryLedger
    from mind.stats import bootstrap_ci
    diffs = []
    for seed in ctx.seeds:
        led = MemoryLedger()
        _live(Organism("organism", seed, led), seed, 200)
        restored, reborn = Organism.restore(led), Organism("organism", seed)
        diffs.append(_live(restored, 70_000 + seed, 40) - _live(reborn, 70_000 + seed, 40))
    m, lo, hi = bootstrap_ci(diffs, seed="C015")
    return {"verdict": "HOLDS" if lo > 0.3 else "FAILS" if hi <= 0.3 else "INCONCLUSIVE", "robust": True,
            "diff": m, "lo": lo, "hi": hi,
            "summary": f"restored − reborn kept {m:+.3f} [{lo:+.3f}, {hi:+.3f}] (claim: > 0.3)"}


CLAIM = Claim(
    id="C015",
    title="The ledger carries a learned individual across death",
    statement="After 200 episodes, an organism restored from its ledger keeps more commitments over the next 40 "
              "episodes than a reborn copy with the same configuration and seed, by more than 0.3.",
    kind="effect",
    scope="L2",
    question="H008",
    depends_on=("K01",),
    extends=("L02",),
    test=Check(persistence, seeds=12),
    by="pipeline-v2",
    created="2026-10-10",
)
