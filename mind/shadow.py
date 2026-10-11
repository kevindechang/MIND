"""Shadow replay: what one consumer would have done with other inputs, at fixed behaviour.

A lesion changes what the organism does, so every metric measured after it mixes two
causes: the lesioned organ's contents no longer reaching some consumer (information),
and the different events that the changed behaviour produces (event mix). Comparing
same-event calibration ACROSS lesion arms re-imports the confound that retired C007,
C008 and C010: each arm is scored on its own events.

The ledger logs every tick's broadcast, action, confidence and outcome. A shadow re-runs
ONE consumer's learning on that logged stream with its inputs filtered, while the
organism's behaviour, and so the event stream, stays exactly as it was lived. The
difference between the shadow and the organism is the consumer's informational
dependence on the filtered source with behaviour held fixed (a natural direct effect,
in mediation terms). Lesions answer "what does this organ do to the organism?";
shadows answer "what does this consumer get from that organ's contents?".

Implemented consumer: the self-model, the only organ whose output (its confidence) is
scored. The shadow is the real `SelfModel` class, built with the life's own parameters
and fed the view the organism fed it (the logged broadcast minus the life's own cuts to
the self-model). With no filter it reproduces every logged confidence exactly; claim K09
checks that in every world and variant.

Filters, by organ name:
  drop   the organ's contents are removed from the consumer's view
  sham   as the kernel's `shuffle:X`: the organ's contents in the view are replaced by its
         contents from a random one of the previous 64 ticks (matched statistics, broken
         relation to the present). real vs sham isolates what the content says; sham vs
         drop is the cost of carrying the organ's features at all.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import random
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Sequence

from .kernel import Config, Content
from .ledger import Event, MemoryLedger

SHAM_BUFFER = 64        # ticks of history a sham draws from, as kernel.Organism._shuffle


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


def replay_self_model(events: Sequence[Event], drop: Sequence[str] = (),
                      sham: Sequence[str] = ()) -> List[Forecast]:
    """Re-run the life's self-model on its logged broadcasts, with `drop`/`sham` filters."""
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
    model = SelfModel({k: v for organ, k, v in cfg.params if organ == "self_model"})
    seed = genesis["seed"]
    buffers: Dict[str, List[List[Content]]] = {name: [] for name in sham}
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
            view = [c for c in seen if c.source not in drop and c.source not in buffers]
            for name in sorted(buffers):
                buffer = buffers[name]
                if buffer:
                    pick = random.Random(f"{seed}|{p['t']}|shadow-sham:{name}").randrange(len(buffer))
                    view.extend(buffer[pick])
                buffer.append([c for c in seen if c.source == name])
                if len(buffer) > SHAM_BUFFER:
                    buffer.pop(0)
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
                    conditions: Optional[Dict[str, Dict[str, Sequence[str]]]] = None) -> Dict[str, Any]:
    """Live one lifetime, then score the self-model's shadows on its own events.

    Returns the life's runner metrics, whether the unfiltered shadow reproduced every
    logged confidence (`exact`), the shadow's late Brier and table Brier, and one late
    Brier per named condition, e.g. {"drop:memory": {"drop": ("memory",)}}."""
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
    return out


def _task(args) -> Dict[str, Any]:
    arm, world, variant, seed, episodes, conditions = args
    return fixed_behaviour(arm, world, seed, episodes, variant, conditions)


def fixed_behaviour_many(lab: Any, arm: str, world: str, variant: str, seeds: Sequence[int],
                         episodes: Optional[int],
                         conditions: Optional[Dict[str, Dict[str, Sequence[str]]]] = None) -> List[Dict[str, Any]]:
    """`fixed_behaviour` for many seeds, in parallel with the lab's worker count."""
    tasks = [(arm, world, variant, s, episodes, conditions) for s in seeds]
    jobs = getattr(lab, "jobs", 1) or 1
    if jobs > 1 and len(tasks) > 1:
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            return list(pool.map(_task, tasks, chunksize=1))
    return [_task(t) for t in tasks]
