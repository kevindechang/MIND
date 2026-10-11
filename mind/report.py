"""Report probe and transcript narrator (question H013).

A report is valid only insofar as it predicts the organism's next action.
`grounded_report` reads the workspace broadcast the organism already emits
(`pending=`, `was:request=`, and the act cue `bell=1`) and names one legal
action. It does not read policy weights, organ state, or the raw observation.
`self:<action>=sure|unsure|doubt` is a confidence label, not an intention, so
it never selects the action.

`Narrator` reads the public observation transcript of the whole episode and
nothing else: the last `request=` it has seen, and the current `bell`. That is
v1's zero-read narrator strengthened to the same transcript the organism sees.
Both are scored only by agreement with the action then taken.

Scope of the act cue: vigil marks the tick an intention comes due with
`bell=1`. Worlds without that cue produce no scored ticks.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

from .kernel import Decision, Organism


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
    predict `wait`.
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


def organ_holds_intention(agent: Organism, actions: Sequence[str]) -> bool:
    """Goals or memory still carry a request. Read-only; call before the tick that might discharge it."""
    legal = set(actions)
    info = agent.introspect()
    if any(p in legal for p in info.get("goals", {}).get("pending", ())):
        return True
    for feature in info.get("memory", {}).get("remembered", ()):
        key, sep, value = str(feature).partition("=")
        if sep and key == "request" and value in legal:
            return True
    return False


class Narrator:
    """Full-episode public transcript. No broadcast, no organ, no policy weights."""

    def __init__(self) -> None:
        self._history: List[Dict[str, str]] = []

    def reset_episode(self) -> None:
        self._history = []

    def predict(self, obs: Dict[str, str], actions: Sequence[str]) -> str:
        legal = set(actions)
        request = None
        for past in self._history:
            if past.get("request") in legal:
                request = past["request"]
        if obs.get("request") in legal:
            request = obs["request"]
        if obs.get("bell") == "1" and request is not None:
            return request
        return _default(actions)

    def observe(self, obs: Dict[str, str]) -> None:
        self._history.append({str(k): str(v) for k, v in obs.items()})


class NarratorAgent:
    """The narrator as a rival arm: it acts from the transcript alone, in vigil.

    Same step interface as `rivals.Agent`. Not a subclass, so this module does not
    import the rival registry (the registry imports this class).
    """

    def __init__(self) -> None:
        self.narrator = Narrator()

    def step(self, obs, reward=0.0, outcome=None, boundary=False, actions=("wait",)) -> Decision:
        obs = {str(k): str(v) for k, v in obs.items()}
        if boundary:
            self.narrator.reset_episode()
        action = self.narrator.predict(obs, actions)
        self.narrator.observe(obs)
        return Decision(action, None, ())

    def end_episode(self, reward=0.0, outcome=None) -> None:
        pass


def score_life(arm: str, world: str, seed: int, episodes: int, variant: str = "dev",
               kill_at: Sequence[int] = (), trace: bool = False) -> Dict:
    """Score the grounded report against the narrator on this arm's own actions.

    The life loop matches `runner.run` (same observations, same death-and-restore
    points) so a probe cannot drift from the organism the rest of the repository
    measures. Only ticks whose observation carries `bell=1` count, and only in
    the late half of the life (the same window as `runner.aggregate`).

    `grounded` / `narrator` are accuracies against the action taken.
    `reportable` is the fraction of those ticks whose broadcast still contains
    `pending=` or `was:request=`. `held` is the fraction on which goals or memory
    still carried a request just before the tick; it is diagnostic, not a claim
    metric. `n` is the number of scored ticks.
    """
    from .ledger import MemoryLedger
    from .runner import make_agent
    from .worlds import make_world

    ledger: Optional[MemoryLedger] = MemoryLedger() if kill_at else None
    agent = make_agent(arm, world, variant, seed, ledger)
    if kill_at and not isinstance(agent, Organism):
        raise ValueError(f"{arm} is not an organism: only organisms can die and be reborn from a ledger")
    env = make_world(world, seed, variant)
    narrator = Narrator()
    kills = sorted(set(kill_at))
    tick = 0
    # per episode: grounded hits, narrator hits, reportable, held, bell ticks
    rows: List[Tuple[int, int, int, int, int]] = []
    actions_trace: List[str] = []
    for _ in range(episodes):
        obs = env.reset()
        reward, outcome, boundary = 0.0, None, True
        g_hit = n_hit = rep = held = n_bell = 0
        while True:
            legal = env.legal()
            if boundary:
                narrator.reset_episode()
            pred_n = narrator.predict(obs, legal)
            holds = bool(obs.get("bell") == "1" and isinstance(agent, Organism)
                         and organ_holds_intention(agent, legal))
            decision = agent.step(obs, reward, outcome, boundary, legal)
            pred_g = grounded_report(decision.broadcast, legal)
            narrator.observe(obs)
            if trace:
                actions_trace.append(decision.action)
            if obs.get("bell") == "1":
                n_bell += 1
                g_hit += int(pred_g == decision.action)
                n_hit += int(pred_n == decision.action)
                rep += int(intention_in_broadcast(decision.broadcast, legal))
                held += int(holds)
            step = env.step(decision.action)
            if kills and tick == kills[0]:
                kills.pop(0)
                agent = Organism.restore(ledger)  # type: ignore[arg-type]
            tick += 1
            if step.done:
                agent.end_episode(step.reward, step.outcome)
                break
            obs, reward, outcome, boundary = step.obs, step.reward, step.outcome, False
        rows.append((g_hit, n_hit, rep, held, n_bell))
    late = rows[episodes // 2:]
    n = sum(r[4] for r in late)
    if n == 0:
        raise ValueError(f"{arm} in {world}/{variant} produced no bell ticks to score")

    def rate(i: int) -> float:
        return sum(r[i] for r in late) / n

    out = {"grounded": rate(0), "narrator": rate(1), "reportable": rate(2), "held": rate(3),
           "n": float(n)}
    if trace:
        out["trace"] = actions_trace
    return out
