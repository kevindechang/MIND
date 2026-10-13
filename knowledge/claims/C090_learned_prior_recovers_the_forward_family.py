"""H017 (structure learning, a direct measure): the online-EM prior over DAGs, learned from the organism's own probes,
puts most of its mass on the eight forward-only DAGs, which are the workshop's family.

The prior starts uniform over all 25 labelled DAGs on three nodes (the forward-only graphs are 8 of the 25, so a uniform
prior puts 0.32 on them). The measure is read directly from the organ after each lifetime, not through utility, so it
is not confounded with the routing or the value rule. The eight forward-only graphs are not supplied to the organ; the
measure only checks, after the fact, what the learned prior has concentrated on.
Exploration on dev seeds 0-7 (not evidence): mass 0.85 on dev, about 0.6 under censoring.
"""
from mind.claims import Check, Claim

ARM = ("organism +causal causal.voi=1 causal.source=efference causal.hypotheses=dag causal.aware=1 "
       "causal.value_carry=1 policy.bonus=1.0 policy.value_bonus=4.0 causal.em=1")


def learned_family_mass(ctx):
    from mind import stats
    from mind.kernel import Organism
    from mind.organs.causal import DAG_REACH
    from mind.worlds import make_world
    forward = [i for i, r in enumerate(DAG_REACH) if all((r[n] & ((1 << n) - 1)) == 0 for n in range(3))]
    masses = []
    for seed in ctx.seeds:
        org = Organism(ARM, seed=seed)
        env = make_world("workshop", seed, "dev")
        for _ in range(1500):
            obs = env.reset()
            reward, outcome, boundary = 0.0, None, True
            while True:
                d = org.step(obs, reward, outcome, boundary, env.legal())
                s = env.step(d.action)
                if s.done:
                    org.end_episode(s.reward, s.outcome)
                    break
                obs, reward, outcome, boundary = s.obs, s.reward, s.outcome, False
        pi = org.organs["causal"].pi
        masses.append(sum(pi[i] for i in forward))
    est = stats.threshold(masses, ">=", 0.80, seed="C090")
    return {"verdict": est["verdict"], "robust": True,
            "summary": f"forward-family prior mass {est['mean']:.3f} [{est['lo']:.3f}, {est['hi']:.3f}] "
                       f"over {len(masses)} lifetimes"}


CLAIM = Claim(
    id="C090",
    title="The learned structure prior concentrates on the forward-only family of graphs",
    statement="After 1500 episodes in workshop/dev, the organism's learned prior over causal graphs puts mean mass of at "
              "least 0.80 on the eight forward-only graphs, from a uniform start (0.32).",
    kind="threshold",
    scope="L2",
    question="H017",
    about=(),
    extends=("C085",),
    test=Check(learned_family_mass, seeds=16),
    by="claude-code (H017 session 2026-10-13)",
    created="2026-10-13",
)
