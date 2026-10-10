"""The organism kernel: one persistent, event-sourced agent shared by every experiment.

Cognitive cycle per tick (a global-workspace architecture, used as a testable
hypothesis rather than an assumption):

    sense -> every organ proposes contents -> capacity-limited workspace selects
    -> broadcast to all organs (minus cut edges) -> organs learn from the
    transition -> policy acts -> self-model forecasts success -> organs observe
    the act -> ONE atomic tick event is appended to the ledger.

Continuity invariant: organ state is a deterministic fold over ledger events.
`Organism.restore(ledger)` re-executes the identical code path on the logged
inputs and *verifies* every logged decision, so any organ that keeps hidden or
nondeterministic state is caught at the first replay (see claims C-K01/C-K02).

Lesions are declarative modifiers on one shared organism, never bespoke toys:
    -X              ablate organ X (no proposals, no learning, no state)
    +X              add an optional organ
    cut:X>Y         contents from X still compete for the workspace but are not
                    delivered to Y (Y may be '*')
    freeze:X        X keeps its state but stops updating it
    shuffle:X       X's proposals are replaced by its own proposals from a
                    random earlier tick (sham with matched statistics)
    capacity=N|inf  workspace size; inf = flat, no bottleneck
    X.key=value     organ parameter
    @E:modifier     apply modifier at the start of episode E (acute lesion)
"""
from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .ledger import Ledger

KERNEL_VERSION = "1"


class ReplayDivergence(Exception):
    """Replaying the ledger did not reproduce a logged decision."""


@dataclass(frozen=True)
class Content:
    source: str
    key: str
    value: str
    salience: float

    @property
    def feature(self) -> str:
        return f"{self.key}={self.value}"

    @property
    def tag(self) -> str:
        return f"{self.source}:{self.key}={self.value}"


@dataclass(frozen=True)
class Sense:
    t: int
    obs: Dict[str, str]
    reward: float
    outcome: Optional[int]
    boundary: bool
    actions: Tuple[str, ...]


@dataclass
class Moment:
    t: int
    obs: Dict[str, str]
    reward: float            # reward for the PREVIOUS action, delivered with this observation
    outcome: Optional[int]   # public success/failure signal for the previous action
    boundary: bool
    actions: Tuple[str, ...]
    broadcast: Tuple[Content, ...]
    action: Optional[str] = None


@dataclass(frozen=True)
class Decision:
    action: str
    confidence: Optional[float]
    broadcast: Tuple[str, ...]


class Organ:
    """Base class. Subclasses override only the hooks they need.

    Hard rule: all state must change only inside these hooks, as a deterministic
    function of their arguments and `ctx.rng(...)`. Never iterate a set of
    strings where order matters (hash randomisation differs between processes).
    """

    name = "organ"
    home: Tuple[str, ...] = ()        # competencies this organ was designed for (atlas)
    defaults: Dict[str, Any] = {}

    def __init__(self, params: Dict[str, Any]):
        self.p = dict(self.defaults)
        self.p.update(params)

    def reset_episode(self) -> None:
        pass

    def propose(self, sense: Sense, ctx: "Organism") -> List[Content]:
        return []

    def learn(self, prev: Optional[Moment], now: Moment, view: Tuple[Content, ...],
              ctx: "Organism") -> None:
        pass

    def learn_terminal(self, prev: Moment, reward: float, outcome: Optional[int],
                       ctx: "Organism") -> None:
        pass

    def after_act(self, now: Moment, view: Tuple[Content, ...], action: str,
                  ctx: "Organism") -> None:
        pass

    def introspect(self) -> Dict[str, Any]:
        return {}


# --------------------------------------------------------------------------- config

def _parse_value(text: str) -> Any:
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            pass
    return text


@dataclass(frozen=True)
class Config:
    organs: Tuple[str, ...]
    capacity: Optional[int] = 4
    beta: float = 1.0
    explore: float = 0.15
    cuts: Tuple[Tuple[str, str], ...] = ()
    frozen: Tuple[str, ...] = ()
    shuffled: Tuple[str, ...] = ()
    params: Tuple[Tuple[str, str, Any], ...] = ()
    schedule: Tuple[Tuple[int, str], ...] = ()
    text: str = "organism"

    @staticmethod
    def parse(text: str) -> "Config":
        from .organs import DEFAULT_ORGANS, ORGANS
        tokens = text.split()
        if not tokens or tokens[0] != "organism":
            raise ValueError(f"organism config must start with 'organism': {text!r}")
        organs = list(DEFAULT_ORGANS)
        cfg: Dict[str, Any] = {"capacity": 4, "beta": 1.0, "explore": 0.15}
        cuts: List[Tuple[str, str]] = []
        frozen: List[str] = []
        shuffled: List[str] = []
        params: List[Tuple[str, str, Any]] = []
        schedule: List[Tuple[int, str]] = []
        mods = sorted(set(tokens[1:]))
        for mod in mods:
            if mod.startswith("@"):
                when, _, inner = mod[1:].partition(":")
                if not when.isdigit() or not inner:
                    raise ValueError(f"bad scheduled lesion {mod!r}; use @EPISODE:modifier")
                Config._apply_to(inner, organs, cfg, cuts, frozen, shuffled, params, dry=True)
                schedule.append((int(when), inner))
                continue
            Config._apply_to(mod, organs, cfg, cuts, frozen, shuffled, params)
        for name in organs:
            if name not in ORGANS:
                raise ValueError(f"unknown organ {name!r}")
        if "policy" not in organs:
            raise ValueError("the policy organ cannot be ablated (nothing would act)")
        canonical = " ".join(["organism"] + mods)
        return Config(tuple(organs), cfg["capacity"], cfg["beta"], cfg["explore"],
                      tuple(sorted(cuts)), tuple(sorted(frozen)), tuple(sorted(shuffled)),
                      tuple(sorted(params, key=lambda p: (p[0], p[1]))),
                      tuple(sorted(schedule)), canonical)

    @staticmethod
    def _apply_to(mod: str, organs: List[str], cfg: Dict[str, Any], cuts: List[Tuple[str, str]],
                  frozen: List[str], shuffled: List[str], params: List[Tuple[str, str, Any]],
                  dry: bool = False) -> None:
        from .organs import ORGANS
        if dry:  # validate syntax only
            organs, cfg, cuts, frozen, shuffled, params = list(organs), dict(cfg), [], [], [], []
        if mod.startswith("-"):
            if mod[1:] not in organs:
                raise ValueError(f"cannot ablate absent organ {mod[1:]!r}")
            organs.remove(mod[1:])
        elif mod.startswith("+"):
            if mod[1:] not in ORGANS:
                raise ValueError(f"unknown organ {mod[1:]!r}")
            if mod[1:] not in organs:
                organs.append(mod[1:])
        elif mod.startswith("cut:"):
            src, _, dst = mod[4:].partition(">")
            if not src or not dst:
                raise ValueError(f"bad cut {mod!r}; use cut:SRC>DST")
            cuts.append((src, dst))
        elif mod.startswith("freeze:"):
            frozen.append(mod[7:])
        elif mod.startswith("shuffle:"):
            shuffled.append(mod[8:])
        elif mod.startswith("capacity="):
            value = mod[9:]
            cfg["capacity"] = None if value == "inf" else int(value)
            if cfg["capacity"] is not None and cfg["capacity"] < 0:
                raise ValueError("capacity must be >= 0")
        elif mod.startswith("beta="):
            cfg["beta"] = float(mod[5:])
        elif mod.startswith("explore="):
            cfg["explore"] = float(mod[8:])
        elif "." in mod and "=" in mod:
            target, _, value = mod.partition("=")
            organ, _, key = target.partition(".")
            params.append((organ, key, _parse_value(value)))
        else:
            raise ValueError(f"unknown modifier {mod!r}")


# --------------------------------------------------------------------------- organism

class Organism:
    """One persistent individual. Create fresh with a config and seed, or rebuild
    from a ledger with `Organism.restore`."""

    def __init__(self, config: "str | Config" = "organism", seed: int = 0,
                 ledger: Optional[Ledger] = None, _genesis: bool = True):
        self.cfg = Config.parse(config) if isinstance(config, str) else config
        self.seed = int(seed)
        self.ledger = ledger
        self.t = 0
        self.episode = -1
        self.prev: Optional[Moment] = None
        self._shuffle_buffers: Dict[str, List[List[Content]]] = {}
        self._decisions: Dict[int, Decision] = {}
        self._build_organs()
        if _genesis and self.ledger is not None:
            if len(self.ledger) != 0:
                raise ValueError("ledger is not empty; use Organism.restore")
            self.ledger.append("genesis", {"config": self.cfg.text, "seed": self.seed,
                                           "kernel": KERNEL_VERSION})

    # ---- construction -----------------------------------------------------
    def _build_organs(self) -> None:
        from .organs import ORGANS
        self.organs: Dict[str, Organ] = {}
        for name in self.cfg.organs:
            params = {k: v for organ, k, v in self.cfg.params if organ == name}
            self.organs[name] = ORGANS[name](params)
        self.order = [name for name in self.cfg.organs]

    def rng(self, purpose: str) -> random.Random:
        return random.Random(f"{self.seed}|{self.t}|{purpose}")

    def relevance(self, feature: str) -> float:
        policy = self.organs.get("policy")
        return policy.relevance(feature) if policy is not None else 0.0  # type: ignore[attr-defined]

    # ---- lesions ------------------------------------------------------------
    def lesion(self, modifier: str) -> None:
        """Apply a lesion to the living organism now; logged so replay repeats it."""
        self._apply_modifier(modifier)
        if self.ledger is not None:
            self.ledger.append("lesion", {"t": self.t, "modifier": modifier})

    def _apply_modifier(self, modifier: str) -> None:
        organs = list(self.cfg.organs)
        cfg = {"capacity": self.cfg.capacity, "beta": self.cfg.beta, "explore": self.cfg.explore}
        cuts, frozen = list(self.cfg.cuts), list(self.cfg.frozen)
        shuffled, params = list(self.cfg.shuffled), list(self.cfg.params)
        Config._apply_to(modifier, organs, cfg, cuts, frozen, shuffled, params)
        if "policy" not in organs:
            raise ValueError("the policy organ cannot be ablated")
        from .organs import ORGANS
        for name in organs:
            if name not in self.organs:
                p = {k: v for organ, k, v in params if organ == name}
                self.organs[name] = ORGANS[name](p)
        for name in list(self.organs):
            if name not in organs:
                del self.organs[name]
        self.order = organs
        self.cfg = Config(tuple(organs), cfg["capacity"], cfg["beta"], cfg["explore"],
                          tuple(sorted(cuts)), tuple(sorted(frozen)), tuple(sorted(shuffled)),
                          tuple(params), self.cfg.schedule, self.cfg.text)

    # ---- the cognitive cycle ------------------------------------------------
    def _view(self, consumer: str, broadcast: Tuple[Content, ...]) -> Tuple[Content, ...]:
        if not self.cfg.cuts:
            return broadcast
        blocked = {src for src, dst in self.cfg.cuts if dst in (consumer, "*")}
        return tuple(c for c in broadcast if c.source not in blocked)

    def _select(self, proposals: List[Content]) -> Tuple[Content, ...]:
        beta = self.cfg.beta

        def priority(c: Content) -> Tuple[float, str, str, str]:
            return (-(c.salience * (1.0 + beta * self.relevance(c.feature))), c.source, c.key, c.value)

        ranked = sorted(proposals, key=priority)
        cap = self.cfg.capacity
        if cap is None or len(ranked) <= cap:
            return tuple(ranked)
        chosen = ranked[:cap]
        if cap >= 2 and self.cfg.explore > 0:
            rng = self.rng("workspace")
            if rng.random() < self.cfg.explore:
                losers = ranked[cap:]
                chosen = ranked[:cap - 1] + [losers[rng.randrange(len(losers))]]
        return tuple(chosen)

    def _shuffle(self, name: str, proposals: List[Content]) -> List[Content]:
        buffer = self._shuffle_buffers.setdefault(name, [])
        out: List[Content] = []
        if buffer:
            out = list(buffer[self.rng("shuffle:" + name).randrange(len(buffer))])
        buffer.append(proposals)
        if len(buffer) > 64:
            buffer.pop(0)
        return out

    def step(self, obs: Dict[str, Any], reward: float = 0.0, outcome: Optional[int] = None,
             boundary: bool = False, actions: Sequence[str] = ("wait",)) -> Decision:
        return self._step(obs, reward, outcome, boundary, actions, log=True)

    def step_at(self, t: int, obs: Dict[str, Any], reward: float = 0.0,
                outcome: Optional[int] = None, boundary: bool = False,
                actions: Sequence[str] = ("wait",)) -> Decision:
        """Idempotent step for at-least-once delivery (Anjo invariant I7): a tick
        that is already committed returns its logged decision, never a second act."""
        if t < self.t:
            return self._decisions[t]
        if t > self.t:
            raise ValueError(f"tick {t} skips ahead of organism tick {self.t}")
        return self.step(obs, reward, outcome, boundary, actions)

    def _step(self, obs: Dict[str, Any], reward: float, outcome: Optional[int], boundary: bool,
              actions: Sequence[str], log: bool) -> Decision:
        obs = {str(k): str(v) for k, v in obs.items()}
        actions = tuple(actions)
        if not actions:
            raise ValueError("at least one legal action is required")
        if boundary:
            self.episode += 1
            for when, modifier in self.cfg.schedule:
                if when == self.episode:
                    self._apply_modifier(modifier)
            for organ in self.organs.values():
                organ.reset_episode()
        sense = Sense(self.t, obs, float(reward), outcome, boundary, actions)
        proposals: List[Content] = []
        for name in self.order:
            props = self.organs[name].propose(sense, self)
            if name in self.cfg.shuffled:
                props = self._shuffle(name, props)
            proposals.extend(props)
        broadcast = self._select(proposals)
        now = Moment(self.t, obs, float(reward), outcome, boundary, actions, broadcast)
        frozen = set(self.cfg.frozen)
        for name in self.order:
            if name not in frozen:
                self.organs[name].learn(self.prev, now, self._view(name, broadcast), self)
        policy = self.organs["policy"]
        action = policy.decide(self._view("policy", broadcast), actions, self.rng("policy"))  # type: ignore[attr-defined]
        self_model = self.organs.get("self_model")
        confidence = (self_model.forecast(self._view("self_model", broadcast), action)  # type: ignore[attr-defined]
                      if self_model is not None else None)
        now.action = action
        for name in self.order:
            if name not in frozen:
                self.organs[name].after_act(now, self._view(name, broadcast), action, self)
        self.prev = now
        decision = Decision(action, confidence, tuple(c.tag for c in broadcast))
        self._decisions[self.t] = decision
        if log and self.ledger is not None:
            self.ledger.append("tick", {"t": self.t, "obs": obs, "r": float(reward), "o": outcome,
                                        "b": int(boundary), "a": list(actions),
                                        "ws": list(decision.broadcast), "act": action,
                                        "conf": confidence})
        self.t += 1
        return decision

    def end_episode(self, reward: float = 0.0, outcome: Optional[int] = None) -> None:
        self._end(reward, outcome, log=True)

    def _end(self, reward: float, outcome: Optional[int], log: bool) -> None:
        if self.prev is not None and self.prev.action is not None:
            frozen = set(self.cfg.frozen)
            for name in self.order:
                if name not in frozen:
                    self.organs[name].learn_terminal(self.prev, float(reward), outcome, self)
        self.prev = None
        if log and self.ledger is not None:
            self.ledger.append("end", {"t": self.t, "r": float(reward), "o": outcome})

    # ---- persistence ----------------------------------------------------------
    @classmethod
    def restore(cls, ledger: Ledger) -> "Organism":
        """Rebuild from the ledger alone, verifying every logged decision."""
        events = list(ledger)
        if not events or events[0].kind != "genesis":
            raise ReplayDivergence("ledger has no genesis event")
        g = events[0].payload
        if g.get("kernel") != KERNEL_VERSION:
            raise ReplayDivergence(f"ledger kernel {g.get('kernel')} != {KERNEL_VERSION}")
        org = cls(g["config"], g["seed"], ledger=None, _genesis=False)
        for event in events[1:]:
            p = event.payload
            if event.kind == "tick":
                if p["t"] != org.t:
                    raise ReplayDivergence(f"tick gap: ledger {p['t']} vs organism {org.t}")
                d = org._step(p["obs"], p["r"], p["o"], bool(p["b"]), p["a"], log=False)
                if (d.action != p["act"] or list(d.broadcast) != p["ws"]
                        or d.confidence != p["conf"]):
                    raise ReplayDivergence(
                        f"tick {p['t']}: replay chose {d.action!r}/{list(d.broadcast)} "
                        f"but ledger says {p['act']!r}/{p['ws']}")
            elif event.kind == "end":
                org._end(p["r"], p["o"], log=False)
            elif event.kind == "lesion":
                org._apply_modifier(p["modifier"])
            else:
                raise ReplayDivergence(f"unknown event kind {event.kind!r}")
        org.ledger = ledger
        return org

    # ---- probes -----------------------------------------------------------------
    def introspect(self) -> Dict[str, Any]:
        """What the organism's own state says about itself (for report-validity probes)."""
        return {name: organ.introspect() for name, organ in self.organs.items()}

    def greedy(self, features: Sequence[str], actions: Sequence[str]) -> str:
        """The policy's exploitation choice for a given broadcast feature set."""
        return self.organs["policy"].greedy(features, actions)  # type: ignore[attr-defined]
