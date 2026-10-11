"""Matched-state report access forks (question H013).

A lifelong access cut confounds the instantaneous path from a broadcast into the
policy with everything that cut changes about later learning and history. This
probe does not. One organism is trained on its normal, uncut history. Immediately
before the designated bell tick, `Organism.restore` rebuilds copies from that
one ledger. Every copy gets `freeze:policy`, so the intervention tick does not
update the policy. Cuts are applied to some copies only. Every copy then
processes the same observation, reward, outcome, boundary and legal actions, at
the same `t`, seed and RNG purpose (`rng` is `seed|t|purpose`).

The designated tick is the first *exposed* bell of the late half of the life:
episode index at least `episodes // 2` (the same late window as
`runner.aggregate`), observation `bell=1`, and the frozen sham broadcast
contains an intention token (`pending=<legal action>` or `was:request=<legal
action>`). One tick per lifetime. Later bells are not scored, because continuing
the forks would let their histories diverge.

The predeclared report reads that broadcast and nothing else: `pending=` if one
is present, otherwise `was:request=`, and only when `bell=1` is in the
broadcast. It does not read policy weights, organ state, or the raw observation.
`self:` tags are confidence labels, not the report.

`mind/report.py` is result-affecting for the claims that call it. It is not
listed in `RESULT_CODE`: adding it would change the suite fingerprint, and
re-recording every claim on this machine would add a second environment id on
top of historical records that already carry two free-text session labels. The
ladder would then mark those claims REPLICATED. That is not independent
replication. Claims that call this module seal `probe_fingerprint()` instead, so
a later edit of this file fails those claims.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .kernel import Organism
from .ledger import MemoryLedger

FREEZE = "freeze:policy"

# Fixed order. Sham is two restores with no cut; the rest are the redundancy map.
# Memory and goals are degenerate on a lifetime timescale (C004). The self-model
# is included because its bids are another path into the policy.
CONDITIONS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("sham", ()),
    ("goals", ("cut:goals>policy",)),
    ("memory", ("cut:memory>policy",)),
    ("self_model", ("cut:self_model>policy",)),
    ("goals+memory", ("cut:goals>policy", "cut:memory>policy")),
    ("goals+self_model", ("cut:goals>policy", "cut:self_model>policy")),
    ("memory+self_model", ("cut:memory>policy", "cut:self_model>policy")),
    ("triple", ("cut:goals>policy", "cut:memory>policy", "cut:self_model>policy")),
)


def probe_fingerprint() -> str:
    """Hash of this file. Claim code seals it; editing the probe fails the claim."""
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:16]


def parse_tag(tag: str) -> Tuple[str, str, str]:
    """`source:key=value`. Keys may themselves contain colons (`was:request`)."""
    source, _, rest = tag.partition(":")
    key, sep, value = rest.rpartition("=")
    if not sep:
        return source, rest, ""
    return source, key, value


def _default(actions: Sequence[str]) -> str:
    return "wait" if "wait" in actions else actions[0]


def grounded_report(broadcast: Sequence[str], actions: Sequence[str]) -> str:
    """Next-action report from the broadcast alone.

    When the broadcast contains the act cue (`perception`, `bell=1`) and an
    intention, predict that intention: an explicit `pending=` first, otherwise
    a remembered `was:request=`, in broadcast order (workspace rank). Otherwise
    predict the default legal action (`wait` when it is legal).
    """
    actions = tuple(actions)
    legal = set(actions)
    pending: List[str] = []
    remembered: List[str] = []
    bell = False
    for tag in broadcast:
        source, key, value = parse_tag(tag)
        if source == "perception" and key == "bell" and value == "1":
            bell = True
        elif key == "pending" and value in legal:
            pending.append(value)
        elif key == "was:request" and value in legal:
            remembered.append(value)
    if bell:
        for choice in pending + remembered:
            return choice
    return _default(actions)


def intention_in_broadcast(broadcast: Sequence[str], actions: Sequence[str]) -> bool:
    """An intention token occupies the broadcast, whether or not the policy receives it."""
    legal = set(actions)
    for tag in broadcast:
        _, key, value = parse_tag(tag)
        if key in ("pending", "was:request") and value in legal:
            return True
    return False


def _blocked_sources(cuts: Sequence[str]) -> set:
    blocked = set()
    for cut in cuts:
        src, _, dst = cut[4:].partition(">")
        if dst in ("policy", "*"):
            blocked.add(src)
    return blocked


def _arm_step(checkpoint: MemoryLedger, obs: Dict[str, str], reward: float,
              outcome: Optional[int], boundary: bool, legal: Sequence[str],
              cuts: Sequence[str]) -> Dict:
    """Restore one copy, freeze the policy, apply cuts, step once."""
    org = Organism.restore(checkpoint.fork())
    t_before = org.t
    seed = org.seed
    org.lesion(FREEZE)
    for cut in cuts:
        org.lesion(cut)
    if org.t != t_before:
        raise RuntimeError("a lesion advanced the tick")
    if org.seed != seed:
        raise RuntimeError("restore did not keep the seed")
    decision = org.step(obs, reward, outcome, boundary, legal)
    policy = org.organs["policy"]
    greedy = policy.learner.greedy(policy._feats, list(legal))
    tags = tuple(decision.broadcast)
    report = grounded_report(tags, legal)
    blocked = _blocked_sources(cuts)
    removed = sum(1 for tag in tags if parse_tag(tag)[0] in blocked)
    return {
        "action": decision.action,
        "greedy": greedy,
        "broadcast": tags,
        "report": report,
        "agree": int(report == decision.action),
        "t": t_before,
        "seed": seed,
        "explored": int(decision.action != greedy),
        "removed": removed,
        "frozen": "policy" in org.cfg.frozen,
        "cuts": tuple(sorted(org.cfg.cuts)),
    }


def matched_fork(seed: int, episodes: int = 300, variant: str = "dev", world: str = "vigil",
                 require_exposed: bool = True) -> Dict:
    """One paired lifetime: train intact, fork at the first designated bell.

    Returns the two sham copies and every cut condition. `sham_identical` is 1
    when the two no-cut forks took the same action and broadcast the same tags
    at the same `t`. `broadcasts_identical` is 1 when every cut copy broadcast
    the same tags as the sham (the report contents did not move).
    """
    from .runner import make_agent
    from .worlds import make_world

    if episodes < 2:
        raise ValueError("need at least 2 episodes so the late half exists")
    ledger = MemoryLedger()
    agent = make_agent("organism", world, variant, seed, ledger)
    if not isinstance(agent, Organism):
        raise ValueError("matched forks require an organism")
    env = make_world(world, seed, variant)
    late = episodes // 2
    found = None
    sham_a = None
    for episode in range(episodes):
        obs = env.reset()
        reward, outcome, boundary = 0.0, None, True
        while True:
            legal = tuple(env.legal())
            bell = str(obs.get("bell")) == "1"
            if episode >= late and bell:
                if boundary:
                    raise ValueError(
                        f"seed {seed}: designated bell is an episode boundary; "
                        "the fork would mix a reset with the cut")
                checkpoint = ledger.fork()
                head = checkpoint.head
                obs_s = {str(k): str(v) for k, v in obs.items()}
                peek = _arm_step(checkpoint, obs_s, float(reward), outcome, False, legal, ())
                if checkpoint.head != head:
                    raise RuntimeError("stepping a fork mutated the checkpoint ledger")
                exposed = intention_in_broadcast(peek["broadcast"], legal)
                if exposed or not require_exposed:
                    found = {
                        "checkpoint": checkpoint,
                        "obs": obs_s,
                        "reward": float(reward),
                        "outcome": outcome,
                        "boundary": False,
                        "legal": legal,
                        "episode": episode,
                        "exposed": exposed,
                        "head": head,
                    }
                    sham_a = peek
                    break
            decision = agent.step(obs, reward, outcome, boundary, legal)
            step = env.step(decision.action)
            if step.done:
                agent.end_episode(step.reward, step.outcome)
                break
            obs, reward, outcome, boundary = step.obs, step.reward, step.outcome, False
        if found is not None:
            break
    if found is None or sham_a is None:
        why = "exposed " if require_exposed else ""
        raise ValueError(
            f"seed {seed}: no {why}bell in the late half of {world}/{variant} "
            f"({episodes} episodes)")

    sham_b = _arm_step(found["checkpoint"], found["obs"], found["reward"], found["outcome"],
                       found["boundary"], found["legal"], ())
    arms: Dict[str, Dict] = {"sham": sham_a}
    for name, cuts in CONDITIONS:
        if name == "sham":
            continue
        arms[name] = _arm_step(found["checkpoint"], found["obs"], found["reward"], found["outcome"],
                               found["boundary"], found["legal"], cuts)
    if found["checkpoint"].head != found["head"]:
        raise RuntimeError("forks mutated the pre-intervention ledger")
    sham_same = (sham_a["action"] == sham_b["action"] and sham_a["broadcast"] == sham_b["broadcast"]
                 and sham_a["report"] == sham_b["report"] and sham_a["t"] == sham_b["t"]
                 and sham_a["seed"] == sham_b["seed"])
    broadcasts_same = all(arm["broadcast"] == sham_a["broadcast"] for arm in arms.values())
    reports_same = all(arm["report"] == sham_a["report"] for arm in arms.values())
    ticks_same = all(arm["t"] == sham_a["t"] for arm in arms.values())
    return {
        "seed": seed,
        "world": world,
        "variant": variant,
        "episodes": episodes,
        "episode": found["episode"],
        "t": sham_a["t"],
        "exposed": int(found["exposed"]),
        "sham_identical": int(sham_same),
        "broadcasts_identical": int(broadcasts_same and reports_same and ticks_same),
        "report": sham_a["report"],
        "sham_action": sham_a["action"],
        "sham_agree": sham_a["agree"],
        "sham_explored": sham_a["explored"],
        "sham_b_action": sham_b["action"],
        "arms": arms,
    }


def _fork_job(args: Tuple) -> Dict:
    seed, episodes, variant, world, require_exposed = args
    return matched_fork(seed, episodes, variant, world, require_exposed)


def fork_rates(rows: Sequence[Dict]) -> Dict[str, Dict[str, List[float]]]:
    """Per condition, one number per lifetime: action change and report-agreement drop vs the sham."""
    out: Dict[str, Dict[str, List[float]]] = {}
    for name, _cuts in CONDITIONS:
        changed: List[float] = []
        drop: List[float] = []
        removed: List[float] = []
        agree: List[float] = []
        for row in rows:
            arm = row["arms"][name]
            changed.append(float(arm["action"] != row["sham_action"]))
            drop.append(float(row["sham_agree"] - arm["agree"]))
            removed.append(float(arm["removed"]))
            agree.append(float(arm["agree"]))
        out[name] = {"changed": changed, "drop": drop, "removed": removed, "agree": agree}
    return out


def matched_forks(seeds: Sequence[int], episodes: int = 300, variant: str = "dev",
                  world: str = "vigil", require_exposed: bool = True, jobs: int = 1) -> List[Dict]:
    """One matched fork per seed. `jobs` > 1 uses processes; the result order follows `seeds`."""
    seeds = list(seeds)
    payloads = [(s, episodes, variant, world, require_exposed) for s in seeds]
    if jobs <= 1 or len(payloads) <= 1:
        return [_fork_job(p) for p in payloads]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        return list(pool.map(_fork_job, payloads, chunksize=1))
