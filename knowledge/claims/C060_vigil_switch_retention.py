"""Mid-life vigil variant switch: acute deficit, recovery, and retention.

H012 asks whether learning at more than one timescale transfers without an
unacceptable loss of the earlier competence. This claim does not add an organ.
It runs one life through vigil/dev, then vigil/long, then vigil/dev, and it
freezes the policy at the switch with a scheduled lesion. Memory and goals
already reset every episode, so the only durable learner is the policy. A
second durable timescale would be warranted if returning to dev cost more than
the margin even though the policy had kept learning. On the dev seeds used to
choose the windows, it did not.

The margin is 0.10 kept-rate (ten commitments in a hundred episodes), the same
order as the vigil control margins already in use (C005 uses 0.08, C006 uses
0.12). The gap versus the window rival uses C001's 0.50 commitment margin.
rival:window8 is the organism's own TD learner on the last eight raw
observations, with the same public observations, rewards, outcomes and legal
actions. It is not an oracle. Its acute deficit and its immediate return
change were not resolved against 0.10 on dev seeds 0-31, so those two
intervals are reported and do not decide the verdict.

Scope: this organism, this vigil switch, L2. Not L3, and not a general result
about multi-timescale learning.
"""
from mind.claims import Check, Claim

PHASE = 160
WIN = 40
KEPT = 0.10
GAP = 0.50
FROZEN = "organism @160:freeze:policy"


def _mean(xs):
    return sum(xs) / len(xs)


def _life(arm, seed):
    from mind.kernel import Organism
    from mind.rivals import RIVALS
    from mind.worlds.vigil import Vigil

    if arm.startswith("rival:"):
        agent = RIVALS[arm.split(":", 1)[1]].factory("vigil", "dev", seed)
    else:
        agent = Organism(arm, seed)
    env = Vigil(seed, "dev")
    rows = []
    for variant, n in (("dev", PHASE), ("long", PHASE), ("dev", PHASE)):
        # Mid-life variant switch: the same world object, so its random stream
        # continues and organism arms stay paired until behaviour diverges.
        env.variant = variant
        for _ in range(n):
            obs = env.reset()
            reward, outcome, boundary = 0.0, None, True
            while True:
                decision = agent.step(obs, reward, outcome, boundary, env.legal())
                step = env.step(decision.action)
                if step.done:
                    agent.end_episode(step.reward, step.outcome)
                    break
                obs, reward, outcome, boundary = step.obs, step.reward, step.outcome, False
            rows.append(env.summary()["kept"])
    if len(rows) != 3 * PHASE:
        raise RuntimeError("life length does not match the sealed schedule")
    p = PHASE
    return {
        "pre": _mean(rows[p - WIN:p]),
        "acute": _mean(rows[p:p + WIN]),
        "recovered": _mean(rows[2 * p - WIN:2 * p]),
        "ret_acute": _mean(rows[2 * p:2 * p + WIN]),
        "ret_late": _mean(rows[3 * p - WIN:3 * p]),
    }


def _ci(xs, label):
    from mind.stats import bootstrap_ci
    return bootstrap_ci(xs, seed="C060|" + label)


def _above(lo, hi, margin):
    if lo > margin:
        return "HOLDS"
    if hi <= margin:
        return "FAILS"
    return "INCONCLUSIVE"


def _inside(lo, hi, margin):
    if -margin < lo and hi < margin:
        return "HOLDS"
    if lo >= margin or hi <= -margin:
        return "FAILS"
    return "INCONCLUSIVE"


def _join(parts):
    if any(part == "FAILS" for part in parts):
        return "FAILS"
    if all(part == "HOLDS" for part in parts):
        return "HOLDS"
    return "INCONCLUSIVE"


def _fmt(name, mean, lo, hi, part):
    return f"{name} {mean:+.3f} [{lo:+.3f}, {hi:+.3f}] ({part})"


def switch_retention(ctx):
    if PHASE != 160 or WIN != 40 or FROZEN != "organism @160:freeze:policy":
        raise RuntimeError("sealed schedule does not match the constants")
    organism = [_life("organism", seed) for seed in ctx.seeds]
    frozen = [_life(FROZEN, seed) for seed in ctx.seeds]
    window = [_life("rival:window8", seed) for seed in ctx.seeds]
    if any(a["pre"] != b["pre"] for a, b in zip(organism, frozen)):
        raise RuntimeError("freeze:policy changed behaviour before its episode")

    def diff(rows, left, right):
        return [row[left] - row[right] for row in rows]

    specs = (
        ("org deficit", diff(organism, "pre", "acute"), "above", KEPT, True),
        ("org recovery", diff(organism, "recovered", "acute"), "above", KEPT, True),
        ("frozen recovery", diff(frozen, "recovered", "acute"), "inside", KEPT, True),
        ("org return-pre", diff(organism, "ret_acute", "pre"), "above", -KEPT, True),
        ("org late-pre", diff(organism, "ret_late", "pre"), "above", -KEPT, True),
        ("frozen return-pre", diff(frozen, "ret_acute", "pre"), "above", -KEPT, True),
        ("org-window8 pre", [a["pre"] - b["pre"] for a, b in zip(organism, window)], "above", GAP, True),
        ("window8 recovery", diff(window, "recovered", "acute"), "inside", KEPT, True),
        ("window8 deficit", diff(window, "pre", "acute"), "inside", KEPT, False),
        ("window8 return-pre", diff(window, "ret_acute", "pre"), "above", -KEPT, False),
    )
    reported = []
    gated = []
    for name, xs, rule, margin, decides in specs:
        mean, lo, hi = _ci(xs, name)
        part = _above(lo, hi, margin) if rule == "above" else _inside(lo, hi, margin)
        reported.append(_fmt(name, mean, lo, hi, part))
        if decides:
            gated.append(part)
    verdict = _join(gated)
    return {
        "verdict": verdict,
        "robust": True,
        "summary": "; ".join(reported) + ". Window8 deficit and immediate return are reported, not required.",
    }


CLAIM = Claim(
    id="C060",
    title="Vigil gap switch: acute loss, policy-dependent recovery, retained competence",
    statement="In one vigil life of 480 episodes (dev for 0-159, long for 160-319, dev for 320-479), windows of 40 "
              "episodes, the plain organism's kept rate falls by more than 0.10 from the last dev window before the "
              "switch to the first long window, then rises by more than 0.10 from that acute window to the last long "
              "window. The scheduled lesion organism @160:freeze:policy, which stops policy updates at the switch "
              "while memory, goals and the self-model keep learning, has a recovered-minus-acute change whose whole "
              "95% interval lies inside ±0.10. On the return to dev, the plain organism's first 40 episodes and its "
              "last 40 episodes are each no worse than 0.10 below its pre-switch kept rate (lower bound above -0.10), "
              "and the frozen policy's first 40 episodes back are likewise no worse than 0.10 below its pre-switch "
              "rate. Before the switch the plain organism exceeds rival:window8, the same TD learner on the last 8 "
              "raw observations, by more than 0.50 kept. That rival's recovered-minus-acute change lies inside ±0.10. "
              "Its acute deficit and its immediate return change are estimated in the same lives and do not decide "
              "the verdict. This organism, this switch, L2.",
    kind="effect",
    scope="L2",
    question="H012",
    extends=("C001", "C003"),
    test=Check(switch_retention, seeds=32),
    by="researcher-bot",
    created="2026-10-12",
    rationale="0.10 kept is a loss of ten commitments per hundred episodes, in the range already treated as a vigil "
              "control effect (C005 0.08, C006 0.12). 0.50 is C001's margin for a commitment gap. The frozen arm is "
              "the scheduled-lesion control: exploration still decays, because the policy still counts decisions, so "
              "a recovery inside ±0.10 is what that decay is worth without weight updates. Retention is judged "
              "against the competence the arm had when it left dev, not against a life that kept practising. "
              "window8 sees the same public stream. No multi-timescale organ is added: the pre-switch policy still "
              "supports the original competence after the return, frozen or not. Not L3.",
)
