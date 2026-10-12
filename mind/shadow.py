"""Shadow replay: what one consumer would have done with other inputs, at fixed behaviour.

A lesion changes what the organism does, so every metric measured after it mixes the
lesioned organ's contents no longer reaching some consumer with everything else the
lesion changes: workspace selection, other organs, behaviour and so the scored events.
Comparing same-event calibration ACROSS lesion arms re-imports the confound that
retired C007, C008 and C010: each arm is scored on its own events.

The ledger logs every tick's broadcast, action, confidence and outcome. A shadow re-runs
ONE consumer's learning on that logged stream with its inputs filtered, while the
organism's behaviour, its workspace and so the event stream stay exactly as they were
lived. The difference between the shadow and the organism is the consumer's dependence
on the filtered source's contents with everything else held fixed: the direct path from
that source to that consumer. Lesions answer "what does this organ do to the organism?";
shadows answer "what does this consumer get from that organ's contents?". The two do not
add up to a mediation analysis: lesion minus shadow is a residual over every other
pathway the lesion changes, not an identified indirect effect.

Implemented consumer: the self-model, the only organ whose output (its confidence) is
scored. The shadow is the real `SelfModel` class, built with the life's own parameters
and fed the view the organism fed it (the logged broadcast minus the life's own cuts to
the self-model). With no filter it reproduces every logged confidence exactly (K09).

Filters, by organ name:
  drop   the organ's contents are removed from the consumer's view. This changes both
         what the consumer is told and how many features it learns over (the self-model
         normalises its step by the feature count), so it measures their net value.
  sham   a content permutation that keeps everything but the content. At every tick the
         organ keeps its presence and its exact number of distinct features in the view;
         only which features they are changes. They are drawn without replacement from
         the organ's earlier broadcast contents in this life, weighted by how often each
         occurred. Real vs sham isolates what the content says at a fixed feature load;
         sham vs drop is the cost of carrying that many of the organ's features. It is
         NOT the kernel's `shuffle:X`, which replays earlier proposals before selection
         and so changes presence and count. Until the life has shown enough distinct
         contents from the organ, the shortfall is filled with the real contents (a
         fallback, counted by `sham_audit`); K10 checks there is none in the scored half.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import random
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Sequence

from .kernel import Config, Content
from .ledger import Event, MemoryLedger


def content_from_tag(tag: str) -> Content:
    """Rebuild a broadcast content from its logged tag `source:key=value`."""
    source, _, rest = tag.partition(":")
    key, _, value = rest.partition("=")
    content = Content(source, key, value, 0.0)
    if content.tag != tag:
        raise ValueError(f"logged broadcast tag {tag!r} does not round-trip")
    return content


@dataclass(frozen=True)
class Forecast:
    episode: int
    action: str
    confidence: float
    logged: Optional[float]      # what the organism itself said at this tick
    outcome: Optional[int]       # public outcome of the action (None: not scored)


class _ShamPool:
    """One organ's earlier broadcast contents in this life, counted by feature."""

    def __init__(self) -> None:
        self.count: Dict[str, int] = {}          # insertion order = first appearance (deterministic)
        self.example: Dict[str, Content] = {}

    def draw(self, k: int, rng: random.Random) -> List[Content]:
        """Up to k distinct contents, without replacement, weighted by past occurrence."""
        features = list(self.count)
        weights = [self.count[f] for f in features]
        out: List[Content] = []
        while features and len(out) < k:
            r = rng.random() * sum(weights)
            i = 0
            while i < len(weights) - 1 and r >= weights[i]:
                r -= weights[i]
                i += 1
            out.append(self.example[features.pop(i)])
            weights.pop(i)
        return out

    def add(self, contents: Sequence[Content]) -> None:
        for c in contents:
            self.count[c.feature] = self.count.get(c.feature, 0) + 1
            self.example.setdefault(c.feature, c)


def replay_self_model(events: Sequence[Event], drop: Sequence[str] = (), sham: Sequence[str] = (),
                      audit: Optional[List[Dict[str, Any]]] = None,
                      model_params: Optional[Dict[str, Any]] = None) -> List[Forecast]:
    """Re-run the life's self-model on its logged broadcasts, with `drop`/`sham` filters.
    With `audit` (a list), every shammed tick appends what the sham changed (`sham_audit`).
    `model_params` overrides validated self-model parameters in this shadow only;
    the logged actions/outcomes and other organs' broadcasts remain fixed. Such a
    shadow is an alternative predictor, not a counterfactual live trajectory."""
    from .organs import ORGANS
    from .organs.self_model import SelfModel
    if not events or events[0].kind != "genesis":
        raise ValueError("a shadow needs a ledger that starts with genesis (only organisms keep one)")
    genesis = events[0].payload
    cfg = Config.parse(genesis["config"])
    if "self_model" not in cfg.organs:
        raise ValueError(f"{cfg.text!r} has no self-model to shadow")
    if "self_model" in cfg.frozen:
        raise ValueError("a frozen self-model does not learn; there is nothing to shadow")
    if cfg.schedule:
        raise ValueError("the shadow does not replay scheduled lesions (@E:...)")
    for name in tuple(drop) + tuple(sham):
        if name not in ORGANS or name == "self_model":
            raise ValueError(f"cannot filter {name!r} from the self-model's view")
    if set(drop) & set(sham):
        raise ValueError("an organ cannot be both dropped and shammed")
    blocked = {src for src, dst in cfg.cuts if dst in ("self_model", "*")}
    from .kernel import _check_param
    params = {k: v for organ, k, v in cfg.params if organ == "self_model"}
    for key, value in (model_params or {}).items():
        params[key] = _check_param("self_model", key, value)
    model = SelfModel(params)
    seed = genesis["seed"]
    pools = {name: _ShamPool() for name in sorted(set(sham))}
    out: List[Forecast] = []
    pending: Optional[tuple] = None
    prev: Optional[SimpleNamespace] = None
    episode = -1
    for event in events[1:]:
        p = event.payload
        if event.kind == "tick":
            if p["b"]:
                episode += 1
            if pending is not None:              # the previous action's outcome arrives now
                out.append(Forecast(*pending, p["o"]))
                pending = None
            seen = [c for c in map(content_from_tag, p["ws"]) if c.source not in blocked]
            view = [c for c in seen if c.source not in drop and c.source not in pools]
            for name, pool in pools.items():
                real = [c for c in seen if c.source == name]
                wanted = len({c.feature for c in real})
                drawn = pool.draw(wanted, random.Random(f"{seed}|{p['t']}|shadow-sham:{name}")) if wanted else []
                fallback = wanted - len(drawn)
                if fallback:                     # too few distinct earlier contents: keep real ones
                    taken = {c.feature for c in drawn}
                    drawn += [c for c in real if c.feature not in taken][:fallback]
                view.extend(drawn)
                pool.add(real)
                if audit is not None:
                    audit.append({"t": p["t"], "episode": episode, "source": name,
                                  "real": sorted(c.feature for c in real),
                                  "sham": sorted(c.feature for c in drawn), "fallback": fallback,
                                  "features_real": len(SelfModel._features(seen)),
                                  "features_sham": len(SelfModel._features(
                                      [c for c in seen if c.source != name] + drawn))})
            frame = tuple(view)
            model.learn(prev, SimpleNamespace(outcome=p["o"]), frame, None)
            confidence = model.forecast(frame, p["act"])
            model.after_act(SimpleNamespace(action=p["act"]), frame, p["act"], None)
            prev = SimpleNamespace(action=p["act"])
            pending = (episode, p["act"], confidence, p["conf"])
        elif event.kind == "end":
            if pending is not None:
                out.append(Forecast(*pending, p["o"]))
                pending = None
            if prev is not None:
                model.learn_terminal(prev, p["r"], p["o"], None)
            prev = None
        else:
            raise ValueError(f"the shadow cannot replay a {event.kind!r} event")
    return out


def sham_audit(events: Sequence[Event], name: str, episodes: int) -> Dict[str, Any]:
    """What a sham of `name` did over one life. A valid sham keeps, at every tick, the organ's
    presence, its number of distinct features and the self-model's total feature count, and
    changes only which features they are. Counts fallbacks overall and in the scored half."""
    audit: List[Dict[str, Any]] = []
    replay_self_model(events, sham=(name,), audit=audit)
    start = episodes // 2
    present = [a for a in audit if a["real"]]
    return {"ticks": len(audit), "present": len(present),
            "presence_kept": all(bool(a["real"]) == bool(a["sham"]) for a in audit),
            "count_kept": all(len(a["real"]) == len(a["sham"]) for a in audit),
            "load_kept": all(a["features_real"] == a["features_sham"] for a in audit),
            "changed": sum(a["real"] != a["sham"] for a in present),
            "fallback": sum(1 for a in audit if a["fallback"]),
            "fallback_scored": sum(1 for a in audit if a["fallback"] and a["episode"] >= start)}


def late_brier(forecasts: Sequence[Forecast], episodes: int, table: bool = False) -> float:
    """Brier score over the late half of a life, summed exactly as the runner sums `brier`
    (per episode, then over episodes). table=True scores the runner's shadow success table
    on the same events instead (`brier_table`)."""
    from .rivals import SuccessTable
    start = episodes // 2
    rule = SuccessTable()
    sq = [0.0] * episodes
    n = [0] * episodes
    for f in forecasts:
        if f.outcome is None:
            continue
        p = rule.forecast(f.action) if table else f.confidence
        sq[f.episode] += (p - f.outcome) ** 2
        n[f.episode] += 1
        rule.update(f.action, f.outcome)
    count = sum(float(k) for k in n[start:])
    return sum(sq[start:]) / count if count else 0.25


def fixed_behaviour(arm: str, world: str, seed: int, episodes: Optional[int] = None, variant: str = "dev",
                    conditions: Optional[Dict[str, Dict[str, Any]]] = None,
                    audit_shams: bool = False) -> Dict[str, Any]:
    """Live one lifetime, then score the self-model's shadows on its own events.

    Returns the life's runner metrics, whether the unfiltered shadow reproduced every
    logged confidence (`exact`), the shadow's late Brier and table Brier, and one late
    Brier per named condition, e.g. {"drop:memory": {"drop": ("memory",)}}. With
    `audit_shams`, also `sham_audit` for every organ any condition shams."""
    from .runner import run
    ledger = MemoryLedger()
    result = run(arm, world, seed, episodes, variant, ledger=ledger)
    events = list(ledger)
    n = result["episodes"]
    full = replay_self_model(events)
    out: Dict[str, Any] = {"seed": seed, "metrics": result["metrics"],
                           "exact": all(f.confidence == f.logged for f in full),
                           "brier": late_brier(full, n), "brier_table": late_brier(full, n, table=True)}
    for name, spec in sorted((conditions or {}).items()):
        out[name] = late_brier(replay_self_model(events, **spec), n)
    if audit_shams:
        shammed = sorted({o for spec in (conditions or {}).values() for o in spec.get("sham", ())})
        out["sham_audit"] = {o: sham_audit(events, o, n) for o in shammed}
    return out


def _task(args) -> Dict[str, Any]:
    arm, world, variant, seed, episodes, conditions, audit_shams = args
    return fixed_behaviour(arm, world, seed, episodes, variant, conditions, audit_shams)


def fixed_behaviour_many(lab: Any, arm: str, world: str, variant: str, seeds: Sequence[int],
                         episodes: Optional[int],
                         conditions: Optional[Dict[str, Dict[str, Any]]] = None,
                         audit_shams: bool = False) -> List[Dict[str, Any]]:
    """`fixed_behaviour` for many seeds, in parallel with the lab's worker count."""
    tasks = [(arm, world, variant, s, episodes, conditions, audit_shams) for s in seeds]
    jobs = getattr(lab, "jobs", 1) or 1
    if jobs > 1 and len(tasks) > 1:
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            return list(pool.map(_task, tasks, chunksize=1))
    return [_task(t) for t in tasks]
