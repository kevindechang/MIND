"""The rival zoo: standing competitors every claim must face.

A rival is either a standalone agent with the organism's step interface or a
named organism configuration. Rivals accumulate: once registered, the claims
engine automatically pits every applicable superiority claim against it, so a
new strong rival can demote old claims. That is a contribution, not an attack.

Fields:
  challenges  organs whose necessity this rival questions
  reference   True for privileged-model oracles: reported as a ceiling,
              never required to be beaten
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import random
from typing import Callable, Dict, Optional, Tuple

from ..kernel import Decision
from ..organs.policy import Policy, QLearner, expand


class SuccessTable:
    """The compact capability forecaster: per-action exponential average of public
    outcomes. Used by the transcript rivals AND by the runner's shadow scorer
    (calib_gain), so both are literally the same rule (claim K08)."""

    def __init__(self, rate: float = 0.25, prior: float = 0.5):
        self.rate, self.prior = rate, prior
        self.p: Dict[str, float] = {}

    def forecast(self, action: str) -> float:
        return self.p.get(action, self.prior)

    def update(self, action: str, outcome: int) -> None:
        old = self.forecast(action)
        self.p[action] = old + self.rate * (outcome - old)


class Agent:
    def step(self, obs, reward=0.0, outcome=None, boundary=False, actions=("wait",)) -> Decision:
        raise NotImplementedError

    def end_episode(self, reward=0.0, outcome=None) -> None:
        pass


class Transcript(Agent):
    """Raw-history rival: the same TD learner as the organism's policy, but its
    state is the last k observations verbatim (lag-tagged), with no workspace,
    memory, goals or self-model. Confidence is a per-action success table."""

    def __init__(self, k: int, seed: int, pairs: bool = True):
        d = Policy.defaults
        self.k, self.seed, self.pairs, self.t = k, seed, pairs, 0
        self.learner = QLearner(d["alpha"], d["gamma"], d["eps"], d["eps_min"], d["half_life"])
        self.history: deque = deque(maxlen=k)
        self.table = SuccessTable()
        self.prev_feats = None
        self.prev_action: Optional[str] = None

    def _record(self, outcome):
        if self.prev_action is not None and outcome is not None:
            self.table.update(self.prev_action, outcome)

    def step(self, obs, reward=0.0, outcome=None, boundary=False, actions=("wait",)):
        obs = {str(k): str(v) for k, v in obs.items()}
        if boundary:
            self.history.clear()
            self.prev_feats, self.prev_action = None, None
        self._record(outcome)
        self.history.append(obs)
        singles = [f"lag{lag}:{k}={v}" for lag, o in enumerate(reversed(self.history))
                   for k, v in sorted(o.items())]
        feats = expand(singles, self.pairs)
        if self.prev_feats is not None:
            self.learner.update(self.prev_feats, self.prev_action,
                                self.learner.bootstrap(reward, feats, actions))
        action = self.learner.choose(feats, tuple(actions), random.Random(f"{self.seed}|{self.t}|policy"))
        self.prev_feats, self.prev_action = feats, action
        self.t += 1
        return Decision(action, self.table.forecast(action), ())

    def end_episode(self, reward=0.0, outcome=None):
        if self.prev_feats is not None:
            self.learner.update(self.prev_feats, self.prev_action, reward)
        self._record(outcome)
        self.learner.episodes += 1
        self.prev_feats, self.prev_action = None, None


class VigilOracle(Agent):
    """Hand-written perfect pending-queue rule: knows the task semantics."""

    def __init__(self, variant: str):
        self.request = None

    def step(self, obs, reward=0.0, outcome=None, boundary=False, actions=("wait",)):
        if boundary:
            self.request = None
        if "request" in obs:
            self.request = obs["request"]
        if obs.get("bell") == "1" and self.request in actions:
            return Decision(self.request, 1.0, ())
        return Decision("wait", None, ())


class OutageBayes(Agent):
    """Exact HMM filter with the TRUE world parameters, myopic expected-value action.
    Strong privileged reference, not proven optimal (ignores the value of probing)."""

    def __init__(self, variant: str):
        from ..worlds.outage import _SETTINGS, MANUAL, SCAN_FAIL, SCAN_OK
        self.s, self.ok, self.fail, self.manual = _SETTINGS[variant], SCAN_OK, SCAN_FAIL, MANUAL
        self.b = 1.0                 # P(sensor up) at the next action
        self.last: Optional[str] = None
        self.need_transition = False

    def _absorb(self, outcome):
        if self.last == "scan" and outcome is not None:
            self.b = 1.0 if outcome == 1 else 0.0
        self.last = None
        self.need_transition = True

    def _transition(self, alert):
        s, b = self.s, self.b
        joint = {"uu": b * (1 - s["fail"]), "ud": b * s["fail"],
                 "du": (1 - b) * s["fix"], "dd": (1 - b) * (1 - s["fix"])}
        lik = {"uu": {"down": s["false"], None: 1 - s["false"]},
               "dd": {"down": s["false"], None: 1 - s["false"]},
               "ud": {"down": s["alert"], None: 1 - s["alert"]},
               "du": {"up": s["alert_up"], None: 1 - s["alert_up"]}}
        post = {k: joint[k] * lik[k].get(alert, 0.0) for k in joint}
        total = sum(post.values())
        self.b = (post["uu"] + post["du"]) / total if total > 0 else self.b

    def step(self, obs, reward=0.0, outcome=None, boundary=False, actions=("wait",)):
        if self.last is not None:
            self._absorb(outcome)
        if self.need_transition:
            self._transition(obs.get("alert"))
            self.need_transition = False
        scan_value = self.b * self.ok + (1 - self.b) * self.fail
        action = "scan" if scan_value > self.manual else "manual"
        self.last = action
        return Decision(action, round(self.b, 6) if action == "scan" else 1.0, ())

    def end_episode(self, reward=0.0, outcome=None):
        self._absorb(outcome)


@lru_cache(maxsize=None)
def _workshop_root(weights, commitments, censor, deadline, budget):
    from ..worlds.workshop import COST, V04
    _, actions, _ = V04.policy(weights, commitments, censor=censor, deadline=deadline,
                               budget=budget, cost=COST, delays=(1,))
    return actions


class WorkshopBayes(Agent):
    """Exact history-only Bayes agent built from the legacy E001 v0.4 dynamic
    program: posterior over the 8 DAGs from delivered/censored probe results,
    probes chosen by finite-horizon value of information, plan by expected utility."""

    def __init__(self, variant: str):
        from ..worlds.workshop import _PRIORS, _SETTINGS, censor_matrix
        self.prior = _PRIORS[_SETTINGS[variant]["prior"]]
        self.censor = censor_matrix(variant)
        self.c = _SETTINGS[variant]["censor"]

    def step(self, obs, reward=0.0, outcome=None, boundary=False, actions=("wait",)):
        from ..worlds.workshop import GRAPHS, PLANS, V04
        if boundary:
            self.weights = list(self.prior)
            self.probes = 0
        commitments = tuple(sorted((int(k[4:]), int(v), 3) for k, v in obs.items() if k.startswith("want")))
        for key, value in sorted(obs.items()):
            if key.startswith("fx"):
                node = int(key[2:])
                for i, graph in enumerate(GRAPHS):
                    if value == "censored":
                        self.weights[i] *= self.c
                    else:
                        delivered = sum(1 << int(ch) for ch in value)
                        self.weights[i] *= (1 - self.c) if V04.reach(graph, node) == delivered else 0
        t = int(obs["t"])
        total = sum(self.weights)
        weights = tuple(Fraction(w) / total for w in self.weights)
        if t < 2 and self.probes < 2 and "probe0" in actions:
            root = _workshop_root(weights, commitments, self.censor, 2 - t, 2 - self.probes)
            probes = sorted(a for a in root if a[0] == "PROBE")
            # WAIT can tie with PROBE (probing at t=1 still lands before the deadline), but
            # probing now weakly dominates probing later; and if no probe is optimal, no
            # optimal continuation probes at all, so committing now loses nothing.
            if probes:
                self.probes += 1
                return Decision(f"probe{probes[0][1]}", None, ())
        _, best = V04.terminal(weights, commitments)
        plan = best[0]
        action = next(name for name, p in PLANS.items() if p == plan)
        p_ok = sum(w for i, w in enumerate(weights)
                   if V04.payoff(GRAPHS[i], plan, commitments) == -len(plan))
        return Decision(action, round(float(p_ok), 6), ())


ORACLES: Dict[str, Callable[[str], Agent]] = {
    "vigil": VigilOracle, "outage": OutageBayes, "workshop": WorkshopBayes}


class _PolarityBayes(Agent):
    """Shared privileged model for the poltergeist attribution question.

    Knows the world's parameters. Sees only public observations, its own acts,
    rewards and outcomes — never `info`. `trace=False` resets the polarity
    belief every trial (a moment-by-moment judge). `trace=True` keeps it, which
    is a running prediction of the act's sensory consequence.
    """

    def __init__(self, variant: str, trace: bool):
        from ..worlds.poltergeist import observation_model
        self.lik, self.present = observation_model(variant)
        self.trace = trace
        self.belief = 0.5
        self.motor = 0

    def _reset_belief(self) -> None:
        self.belief = 0.5

    def _judge(self, sense: int):
        num = den = 0.0
        for polarity, mass in ((1, self.belief), (-1, 1.0 - self.belief)):
            den += mass * self.lik[(polarity, self.motor, sense)]
            num += mass * self.present[(polarity, self.motor, sense)]
        p_yes = num / den if den > 0.0 else 0.5
        if self.trace:
            pos = self.belief * self.lik[(1, self.motor, sense)]
            neg = (1.0 - self.belief) * self.lik[(-1, self.motor, sense)]
            total = pos + neg
            self.belief = pos / total if total > 0.0 else 0.5
        return p_yes

    def step(self, obs, reward=0.0, outcome=None, boundary=False, actions=("wait",)):
        if boundary:
            self._reset_belief()
            self.motor = 0
        if obs.get("phase") == "act":
            action = actions[0]
            self.motor = 1 if action == "push" else -1 if action == "pull" else 0
            if not self.trace:
                self._reset_belief()
            return Decision(action, None, ())
        p_yes = self._judge(int(obs["sense"]))
        return Decision("yes" if p_yes >= 0.5 else "no", round(p_yes, 6), ())


class Estimator(Agent):
    """Generic state estimator with the same public stream as the efference organ.

    Features are the current observation, the act just taken, and a short raw
    history of both, expanded with the same conjunctions as the organism's
    policy. The learner is the organism's `QLearner` with the policy's default
    step size, discount and exploration. There is no forward model, no polarity
    belief, and no import of the world's parameters or private `info`.
    """

    def __init__(self, seed: int, lags: int = 3):
        d = Policy.defaults
        self.seed, self.lags, self.t = seed, lags, 0
        self.learner = QLearner(d["alpha"], d["gamma"], d["eps"], d["eps_min"], d["half_life"])
        self.table = SuccessTable()
        self.history: deque = deque(maxlen=lags)
        self.motor: Optional[str] = None
        self.prev_feats = None
        self.prev_action: Optional[str] = None

    def _features(self, obs):
        singles = [f"{k}={v}" for k, v in sorted(obs.items())]
        if self.motor is not None:
            singles.append("act=" + self.motor)
        for lag, (past, act) in enumerate(reversed(self.history)):
            bits = [f"{k}={v}" for k, v in sorted(past.items())]
            singles.append(f"lag{lag}:" + ",".join(bits) + f",act={act}")
        return expand(singles, bool(Policy.defaults["pairs"]))

    def _record(self, outcome):
        if self.prev_action is not None and outcome is not None:
            self.table.update(self.prev_action, outcome)

    def step(self, obs, reward=0.0, outcome=None, boundary=False, actions=("wait",)):
        obs = {str(k): str(v) for k, v in obs.items()}
        actions = tuple(actions)
        if boundary:
            self.history.clear()
            self.motor = None
            self.prev_feats, self.prev_action = None, None
        self._record(outcome)
        feats = self._features(obs)
        if self.prev_feats is not None:
            self.learner.update(self.prev_feats, self.prev_action,
                                self.learner.bootstrap(reward, feats, actions))
        action = self.learner.choose(feats, actions, random.Random(f"{self.seed}|{self.t}|policy"))
        self.prev_feats, self.prev_action = feats, action
        self.history.append((obs, action))
        if action in ("push", "pull"):
            self.motor = action
        self.t += 1
        return Decision(action, self.table.forecast(action), ())

    def end_episode(self, reward=0.0, outcome=None):
        if self.prev_feats is not None:
            self.learner.update(self.prev_feats, self.prev_action, reward)
        self._record(outcome)
        self.learner.episodes += 1
        self.prev_feats, self.prev_action = None, None


@dataclass(frozen=True)
class Rival:
    name: str
    doc: str
    challenges: Tuple[str, ...]
    reference: bool = False
    config: Optional[str] = None                     # organism configuration rivals
    factory: Optional[Callable[[str, str, int], Agent]] = None   # (world, variant, seed)
    worlds: Tuple[str, ...] = ()                     # empty = every world


RIVALS: Dict[str, Rival] = {r.name: r for r in (
    Rival("reactive", "same TD learner on the current observation only",
          ("memory", "goals"), factory=lambda w, v, s: Transcript(1, s)),
    Rival("window4", "same TD learner on the last 4 raw observations",
          ("memory", "goals"), factory=lambda w, v, s: Transcript(4, s)),
    Rival("window8", "same TD learner on the last 8 raw observations",
          ("memory", "goals"), factory=lambda w, v, s: Transcript(8, s)),
    Rival("window8lin", "last 8 raw observations, linear (no conjunctions)",
          ("memory", "goals"), factory=lambda w, v, s: Transcript(8, s, pairs=False)),
    Rival("flat", "the organism with an unlimited workspace (no bottleneck)",
          ("workspace",), config="organism capacity=inf"),
    Rival("bayes", "privileged-model Bayes reference (E001 v0.4 DP in workshop)",
          ("memory", "goals", "self_model", "workspace"), reference=True,
          worlds=("vigil", "outage", "workshop"),
          factory=lambda w, v, s: ORACLES[w](v)),
    Rival("filter", "poltergeist polarity filter: privileged parameters, running prediction of the act's sensation",
          ("efference",), reference=True, worlds=("poltergeist",),
          factory=lambda w, v, s: _PolarityBayes(v, trace=True)),
    Rival("moment", "poltergeist moment judge: same privileged model and current act, no running prediction",
          (), worlds=("poltergeist",),
          factory=lambda w, v, s: _PolarityBayes(v, trace=False)),
    Rival("estimator", "generic Q-learner on the same public observations and own acts as the efference organ",
          ("efference",), worlds=("poltergeist",),
          factory=lambda w, v, s: Estimator(s)),
)}
