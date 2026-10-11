"""Memory's contents serve two consumers in silent outages: control and metacognition (H007).

Global availability means that one broadcast content can be used by several functions at
once. The access lesion cut:memory>policy measures the policy's use of memory's contents
(behaviour is allowed to change: that is what a controller's use of information is for).
The fixed-behaviour shadow measures the self-model's use of the same contents without
letting behaviour change. Both must be reliable: reward falls by more than 0.5 per episode
when memory's contents are withheld from the policy (C009's margin for the whole organ),
and the self-model's Brier score rises when they are removed from its view at fixed
behaviour.

Dev exploration (32 seeds): control +1.49 [+0.98, +2.00]; metacognition +0.0021
[+0.0015, +0.0027]. C009 (organism -memory, inconclusive at margin 0.5) tests the whole
organ; this claim splits its contents between their consumers. Removing contents from the
self-model's view also lowers its feature count (its step is lr / len(feats)), so the
metacognition part is the contents' net value. That removal still hurts means they are
worth more than their load (no sham is involved here).
"""
from mind.claims import Check, Claim

EPISODES = 120
MARGIN = 0.5


def dual_use(ctx):
    from mind.shadow import fixed_behaviour_many
    from mind.stats import bootstrap_ci
    a = ctx.lab.metric("organism", "outage", "silent", ctx.seeds, EPISODES, "reward")
    b = ctx.lab.metric("organism cut:memory>policy", "outage", "silent", ctx.seeds, EPISODES, "reward")
    rows = fixed_behaviour_many(ctx.lab, "organism", "outage", "silent", ctx.seeds, EPISODES,
                                {"drop:memory": {"drop": ("memory",)}})
    if not all(r["exact"] for r in rows):
        raise RuntimeError("the unfiltered shadow did not reproduce the organism (K09)")
    control = [x - y for x, y in zip(a, b)]
    info = [r["drop:memory"] - r["brier"] for r in rows]
    cm, clo, chi = bootstrap_ci(control, seed="C033|control")
    im, ilo, ihi = bootstrap_ci(info, seed="C033|metacognition")
    ok = clo > MARGIN and ilo > 0
    failed = chi <= MARGIN or ihi <= 0
    return {"verdict": "HOLDS" if ok else "FAILS" if failed else "INCONCLUSIVE", "robust": True,
            "control": {"mean": cm, "lo": clo, "hi": chi}, "metacognition": {"mean": im, "lo": ilo, "hi": ihi},
            "summary": f"policy loses {cm:+.2f} [{clo:+.2f},{chi:+.2f}] reward without memory's contents "
                       f"(claim > {MARGIN}); self-model loses {im:+.4f} [{ilo:+.4f},{ihi:+.4f}] Brier at fixed "
                       f"behaviour (claim > 0)"}


CLAIM = Claim(
    id="C033",
    title="Memory's contents serve two consumers in silent outages (control and metacognition)",
    statement="In outage/silent, memory's broadcast contents are used by both the policy and the self-model: "
              "withholding them from the policy (cut:memory>policy) lowers reward by more than 0.5 per episode, and, "
              "at fixed behaviour, removing them from the self-model's inputs raises its Brier score (reliably > 0).",
    kind="effect",
    scope="L2",
    question="H007",
    depends_on=("K09",),
    extends=("C009", "C018"),
    test=Check(dual_use, seeds=32),
    by="claude-code (session 01VdSAnY)",
    created="2026-10-11",
    rationale="The global-workspace signature stated as a measurement: one broadcast content, two consumers, two "
              "functions, each use isolated by its own intervention.",
)
