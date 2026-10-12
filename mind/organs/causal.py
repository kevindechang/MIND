"""Causal organ: intervention effects identified from attended probe results (H001).

A workshop probe toggles one node and reports the nodes the toggle reaches, as
`fx<node>=<labels>`, visible for ONE tick. The organ learns from what won a workspace
slot on the tick it was shown, and only from that: probe results (`fx`) and goal
commitments (`want`). It keeps the reach set of each probed node for the episode and
proposes those facts as `reach<node>=<labels>`. With `derive=1` it also composes the
facts into the predicted outcome of each plan the world allows, and proposes the best
predicted plan as `best=<plan>`. The proposal is late (see `Organ.late`): the decision
at the tick the probe result is shown can already use it.

Causal model: fixed in advance, not learned. Plans compose by XOR of their nodes' reach
sets. A plan costs one per node, and each broken commitment costs `penalty`. Those are
the workshop's scoring rule, so this is a supplied payoff model, not causal discovery.
The organ never sees the E001 graph family and knows the reach of only probed nodes.

Controls with the same channel and load: `derive=0` proposes a constant `pad` where
`best` would be, so the facts and the load are unchanged. `sham=1` proposes `best` with
a random legal plan instead, at the same ticks.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

from ..kernel import Content, Organ

PROBE_KEYS = ("fx0", "fx1", "fx2")


def mask_of(label: str) -> int:
    """Node labels such as '02' as a bitmask over nodes."""
    return sum(1 << int(ch) for ch in label)


def label_of(mask: int) -> str:
    return "".join(str(n) for n in range(3) if mask & (1 << n))


def plan_nodes(action: str) -> Optional[Tuple[int, ...]]:
    """The nodes a plan action toggles, or None if the action is not a plan."""
    if not action.startswith("do:"):
        return None
    return tuple(int(ch) for ch in action[3:] if ch.isdigit())


def predicted_utility(reach: Dict[int, int], action: str, commitments: Sequence[Tuple[int, int]],
                      penalty: int) -> Optional[int]:
    """A plan's utility under the learned reach sets, or None while it toggles an unprobed node."""
    nodes = plan_nodes(action)
    if nodes is None or any(n not in reach for n in nodes):
        return None
    effect = 0
    for node in nodes:
        effect ^= reach[node]
    broken = sum(1 for goal, want in commitments if ((effect >> goal) & 1) != want)
    return -(len(nodes) + penalty * broken)


class Causal(Organ):
    name = "causal"
    home = ("causal-control",)
    late = True
    # salience 2.0: the workspace ranks contents by salience x (1 + relevance), and a feature the
    # policy has not yet credited never beats relevance-boosted ones at 1.0 (dev exploration:
    # 8 recommendations reached the workspace at 1.0, 37/37 at 2.0 and at 4.0)
    # goals 2: the workshop has two commitments; the organ waits until it has seen both
    defaults = {"salience": 2.0, "penalty": 3, "derive": 1, "sham": 0, "goals": 2}

    def __init__(self, params):
        super().__init__(params)
        self.reach: Dict[int, int] = {}   # node -> bitmask of the nodes its toggle reaches
        self.wants: Dict[int, int] = {}   # goal -> desired value, as attended this episode

    def reset_episode(self) -> None:
        self.reach = {}                   # every episode draws a new hidden graph
        self.wants = {}

    def late_propose(self, now, view, ctx) -> List[Content]:
        for c in view:                    # only contents that won a slot on this tick
            if c.source != "perception":
                continue
            if c.key in PROBE_KEYS and c.value != "censored":
                self.reach[int(c.key[2:])] = mask_of(c.value)
            elif c.key.startswith("want"):
                self.wants[int(c.key[4:])] = int(c.value)
        salience = self.p["salience"]
        out = [Content(self.name, f"reach{node}", label_of(mask), salience)
               for node, mask in sorted(self.reach.items())]
        best = self._best(now.actions, ctx)
        if best is not None:
            if not self.p["derive"]:
                out.append(Content(self.name, "pad", "0", salience))
            elif self.p["sham"]:
                out.append(Content(self.name, "best", self._sham_plan(now.actions, ctx), salience))
            else:
                out.append(Content(self.name, "best", best, salience))
        return out

    def _best(self, actions: Sequence[str], ctx) -> Optional[str]:
        if not self.reach or len(self.wants) < self.p["goals"]:
            return None
        commitments = sorted(self.wants.items())
        scored = []
        for action in actions:
            utility = predicted_utility(self.reach, action, commitments, self.p["penalty"])
            if utility is not None:
                scored.append((-utility, action))
        return min(scored)[1] if scored else None

    def _sham_plan(self, actions: Sequence[str], ctx) -> str:
        plans = sorted(a for a in actions if plan_nodes(a) is not None)
        return plans[ctx.rng("causal-sham").randrange(len(plans))]

    def introspect(self):
        return {"reach": {node: label_of(mask) for node, mask in sorted(self.reach.items())},
                "wants": dict(sorted(self.wants.items()))}
