"""Causal organ: intervention effects identified from probe results (H001, H015, H016).

A workshop probe toggles one node and reports the nodes the toggle reaches, as
`fx<node>=<labels>`, visible for ONE tick. The organ keeps the reach set of each probed
node for the episode and proposes those facts as `reach<node>=<labels>`. With `derive=1`
it also composes the facts into the predicted outcome of each plan the world allows, and
proposes the best predicted plan as `best=<plan>`. Both proposals are late (see
`Organ.late`): the decision at the tick the probe result is shown can already use them.

Where the facts come from (`source`). `broadcast` (the H001 default) learns only from
what won a workspace slot on the tick it was shown. `efference` learns from the raw
observation of its own probes, outside the workspace, as an efference-style record. The
workspace filter biases what is learned (H015): a learned world model should not depend
on which results happened to win a slot.

Value of information (`voi=1`). For each probe still available, the organ estimates the
expected improvement in its best plan from learning that probe's result, net of the probe
cost, and proposes the most valuable probe as `probe=<action>` when the net value is
positive. The estimate uses one of two hypothesis spaces (`hypotheses`):
- `counts` (H015): a prior over reach sets, learned across episodes from the organ's own
  counts (singly and in pairs). Each episode draws a new hidden graph, but the family of
  graphs is fixed, so the counts are a prior.
- `dag` (H016): the exact posterior over all 25 labelled directed acyclic graphs on the
  three nodes. This hypothesis space is generic. It contains the workshop's graphs, but the
  organ is not given them, and the prior is uniform.
`aware=1` discounts a probe's value by the censor rate the organ has learned from its own
probe results. `value_carry=1` carries the net value of the probe in the proposal's
salience (`VALUE_SALIENCE` times the net value), so the workspace ranks valuable probes higher
and the policy can scale its routing to the value (see policy.py `value_bonus`).

Causal model: fixed in advance, not learned. Plans compose by XOR of their nodes' reach
sets. A plan costs one per node, and each broken commitment costs `penalty`. Those are
the workshop's scoring rule and probe cost, so this is a supplied payoff model, not causal
discovery. The organ never sees the E001 graph family.

Controls with the same channel and load: `derive=0` proposes a constant `pad` where
`best` would be, so the facts and the load are unchanged. `sham=1` proposes `best` with
a random legal plan instead, at the same ticks.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
from typing import Dict, List, Optional, Sequence, Tuple

from ..kernel import Content, Organ

PROBE_KEYS = ("fx0", "fx1", "fx2")
MASKS_WITH = {n: tuple(m for m in range(1, 8) if m & (1 << n)) for n in range(3)}
VALUE_SALIENCE = 4.0   # salience per unit of expected net value, when value_carry=1


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


def labelled_dag_reach() -> Tuple[Dict[int, int], ...]:
    """Reach masks of every labelled directed acyclic graph on the three nodes (25 of them)."""
    edges = [(i, j) for i in range(3) for j in range(3) if i != j]
    out = []
    for k in range(len(edges) + 1):
        for chosen in combinations(edges, k):
            succ = {n: {j for i, j in chosen if i == n} for n in range(3)}
            if any(_reaches_itself(succ, n) for n in range(3)):
                continue
            reach = {}
            for n in range(3):
                seen, stack = {n}, [n]
                while stack:
                    for j in succ[stack.pop()]:
                        if j not in seen:
                            seen.add(j)
                            stack.append(j)
                reach[n] = sum(1 << v for v in seen)
            out.append(reach)
    return tuple(out)


def _reaches_itself(succ: Dict[int, set], start: int) -> bool:
    seen, stack = set(), list(succ[start])
    while stack:
        u = stack.pop()
        if u == start:
            return True
        if u not in seen:
            seen.add(u)
            stack.extend(succ[u])
    return False


DAG_REACH = labelled_dag_reach()


class Causal(Organ):
    name = "causal"
    home = ("causal-control",)
    late = True
    # salience 2.0: the workspace ranks contents by salience x (1 + relevance), and a feature the
    # policy has not yet credited never beats relevance-boosted ones at 1.0 (dev exploration:
    # 8 recommendations reached the workspace at 1.0, 37/37 at 2.0 and at 4.0)
    # goals 2: the workshop has two commitments; the organ waits until it has seen both
    # cost 0.25: the workshop's probe cost (used only when voi=1)
    defaults = {"salience": 2.0, "penalty": 3, "derive": 1, "sham": 0, "goals": 2,
                "source": "broadcast", "voi": 0, "cost": 0.25, "smooth": 1.0,
                "hypotheses": "counts", "aware": 0, "value_carry": 0, "em": 0, "alpha": 0.1,
                "posterior_plan": 0}
    choices = {"source": ("broadcast", "efference"), "hypotheses": ("counts", "dag")}

    def __init__(self, params):
        super().__init__(params)
        self.reach: Dict[int, int] = {}   # node -> bitmask of the nodes its toggle reaches
        self.wants: Dict[int, int] = {}   # goal -> desired value, as learned this episode
        # across episodes (never reset): counts of learned reach masks, singly and in pairs
        self.single: Dict[int, Counter] = {n: Counter() for n in range(3)}
        self.pair: Counter = Counter()    # (a, mask_a, b, mask_b) with a < b
        # across episodes: probe results seen, and how many came back censored
        self.seen = 0
        self.censored = 0
        # across episodes (em=1, H017): the learned prior over the DAG hypotheses, by online EM
        self.S = [0.0] * len(DAG_REACH)                  # accumulated responsibilities
        self.pi = [1.0 / len(DAG_REACH)] * len(DAG_REACH)  # the prior used for the next episode

    def reset_episode(self) -> None:
        if self.p["em"]:
            self._learn_structure_prior()  # this episode's facts, before they are cleared
        self.reach = {}                   # every episode draws a new hidden graph
        self.wants = {}

    def late_propose(self, now, view, ctx) -> List[Content]:
        before = set(self.reach)
        if self.p["source"] == "efference":
            # the organ's own record of its probes and goals: raw observations, not the workspace
            view = tuple(Content("perception", k, v, 0.0) for k, v in sorted(now.obs.items())
                         if k in PROBE_KEYS or k.startswith("want"))
        for c in view:                    # learned from what the chosen source delivers this tick
            if c.source != "perception":
                continue
            if c.key in PROBE_KEYS:
                self.seen += 1
                self.censored += c.value == "censored"
            if c.key in PROBE_KEYS and c.value != "censored":
                self.reach[int(c.key[2:])] = mask_of(c.value)
            elif c.key.startswith("want"):
                self.wants[int(c.key[4:])] = int(c.value)
        self._count_new_facts(before)
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
        if self.p["voi"] and len(self.wants) >= self.p["goals"]:
            choice = self._probe_recommendation(now.actions)
            if choice is not None:
                probe, net = choice
                carried = VALUE_SALIENCE * net if self.p["value_carry"] else salience
                out.append(Content(self.name, "probe", probe, carried))
        return out

    def _count_new_facts(self, before: set) -> None:
        for n in sorted(set(self.reach) - before):
            self.single[n][self.reach[n]] += 1
            for k in sorted(before):
                a, b = min(k, n), max(k, n)
                self.pair[(a, self.reach[a], b, self.reach[b])] += 1

    def _best(self, actions: Sequence[str], ctx) -> Optional[str]:
        if self.p["posterior_plan"]:
            return self._posterior_best(actions)
        if not self.reach or len(self.wants) < self.p["goals"]:
            return None
        commitments = sorted(self.wants.items())
        scored = []
        for action in actions:
            utility = predicted_utility(self.reach, action, commitments, self.p["penalty"])
            if utility is not None:
                scored.append((-utility, action))
        return min(scored)[1] if scored else None

    def _posterior_best(self, actions: Sequence[str]) -> Optional[str]:
        """The plan with the highest expected utility under the DAG posterior (H018): unknown nodes are integrated out,
        so a plan whose reach is still uncertain is weighed by what the organism believes it does, not dropped."""
        if not self.reach or len(self.wants) < self.p["goals"]:
            return None
        idxs = [i for i, r in enumerate(DAG_REACH) if all(r[n] == m for n, m in self.reach.items())]
        if not idxs:
            return None
        commitments = sorted(self.wants.items())
        total = sum(self._dag_weight(i) for i in idxs)
        scored = []
        for action in actions:
            if plan_nodes(action) is None:
                continue
            eu = sum(self._dag_weight(i) * predicted_utility(DAG_REACH[i], action, commitments, self.p["penalty"])
                     for i in idxs) / total
            scored.append((-eu, action))
        return min(scored)[1] if scored else None

    def _sham_plan(self, actions: Sequence[str], ctx) -> str:
        plans = sorted(a for a in actions if plan_nodes(a) is not None)
        return plans[ctx.rng("causal-sham").randrange(len(plans))]

    def _censor_rate(self) -> float:
        """Probability that a probe comes back censored, learned from the organ's own probe results."""
        if not self.p["aware"]:
            return 0.0
        return (self.censored + 1.0) / (self.seen + 2.0)

    # ---- value of information (voi=1) -----------------------------------------------------

    def _prior(self, n: int, evidence: Dict[int, int]) -> Dict[int, float]:
        """P(reach mask of node n | evidence) from the counts across episodes. One known node conditions
        the pair counts when they exist; otherwise the marginal counts are used. Laplace-smoothed."""
        masks = MASKS_WITH[n]
        s = self.p["smooth"]
        if evidence:
            k = min(evidence)
            a, b = min(k, n), max(k, n)

            def key(m: int):
                return (a, evidence[k], b, m) if k < n else (a, m, b, evidence[k])
            weights = {m: self.pair[key(m)] for m in masks}
            if sum(weights.values()) > 0:
                total = sum(weights.values()) + s * len(masks)
                return {m: (weights[m] + s) / total for m in masks}
        counts = self.single[n]
        total = sum(counts[m] for m in masks) + s * len(masks)
        return {m: (counts[m] + s) / total for m in masks}

    def _expected_best(self, actions: Sequence[str], fixed: Dict[int, int],
                       commitments: Sequence[Tuple[int, int]]) -> float:
        """Best plan's expected utility, with the unknown nodes drawn from their priors (chained)."""
        unknown = [n for n in range(3) if n not in fixed]
        joint: List[Tuple[Dict[int, int], float]] = []

        def expand(i: int, reach: Dict[int, int], prob: float) -> None:
            if i == len(unknown):
                joint.append((reach, prob))
                return
            n = unknown[i]
            for m, pm in self._prior(n, reach).items():
                expand(i + 1, {**reach, n: m}, prob * pm)

        expand(0, dict(fixed), 1.0)
        best = None
        for action in actions:
            if plan_nodes(action) is None:
                continue
            eu = sum(prob * predicted_utility(reach, action, commitments, self.p["penalty"])
                     for reach, prob in joint)
            if best is None or eu > best:
                best = eu
        return 0.0 if best is None else best

    def _probe_recommendation(self, actions: Sequence[str]) -> Optional[Tuple[str, float]]:
        """The probe with the largest positive expected net value, and that value, or None."""
        if self.p["hypotheses"] == "dag":
            return self._dag_probe_recommendation(actions)
        candidates = [a for a in sorted(actions) if a.startswith("probe") and int(a[-1]) not in self.reach]
        if not candidates:
            return None
        commitments = sorted(self.wants.items())
        base = self._expected_best(actions, self.reach, commitments)
        c = self._censor_rate()
        best_net, best_action = None, None
        for action in candidates:
            n = int(action[-1])
            informed = sum(pm * self._expected_best(actions, {**self.reach, n: m}, commitments)
                           for m, pm in sorted(self._prior(n, self.reach).items()))
            value = (1 - c) * informed + c * base
            net = value - base - self.p["cost"]
            if net > 0 and (best_net is None or net > best_net):
                best_net, best_action = net, action
        return None if best_action is None else (best_action, best_net)

    # ---- the generic DAG posterior (voi=1, hypotheses=dag) -------------------------------

    def _dag_weight(self, i: int) -> float:
        """Prior weight of DAG hypothesis i: uniform, or learned across episodes when em=1 (H017)."""
        return self.pi[i] if self.p["em"] else 1.0

    def _dag_best(self, actions: Sequence[str], idxs: Sequence[int], commitments) -> float:
        """Best plan's expected utility under the weighted posterior over the given DAG hypotheses."""
        total = sum(self._dag_weight(i) for i in idxs)
        best = None
        for action in actions:
            if plan_nodes(action) is None:
                continue
            eu = sum(self._dag_weight(i) * predicted_utility(DAG_REACH[i], action, commitments, self.p["penalty"])
                     for i in idxs) / total
            if best is None or eu > best:
                best = eu
        return 0.0 if best is None else best

    def _dag_probe_recommendation(self, actions: Sequence[str]) -> Optional[Tuple[str, float]]:
        idxs = [i for i, r in enumerate(DAG_REACH) if all(r[n] == m for n, m in self.reach.items())]
        if not idxs:
            return None
        candidates = [a for a in sorted(actions) if a.startswith("probe") and int(a[-1]) not in self.reach]
        if not candidates:
            return None
        commitments = sorted(self.wants.items())
        base = self._dag_best(actions, idxs, commitments)
        c = self._censor_rate()
        total = sum(self._dag_weight(i) for i in idxs)
        best_net, best_action = None, None
        for action in candidates:
            n = int(action[-1])
            groups: Dict[int, List[int]] = {}
            for i in idxs:
                groups.setdefault(DAG_REACH[i][n], []).append(i)
            informed = sum(sum(self._dag_weight(i) for i in g) / total * self._dag_best(actions, g, commitments)
                           for _, g in sorted(groups.items()))
            value = (1 - c) * informed + c * base
            net = value - base - self.p["cost"]
            if net > 0 and (best_net is None or net > best_net):
                best_net, best_action = net, action
        return None if best_action is None else (best_action, best_net)

    def _learn_structure_prior(self) -> None:
        """Online EM over the DAG hypotheses (H017). The responsibilities of the hypotheses that explain this episode's
        probe results, accumulated across episodes, give the prior used for the next episode. No family is supplied:
        the prior starts uniform over all DAGs and moves toward whatever the organism's own experience supports."""
        idxs = [i for i, r in enumerate(DAG_REACH) if all(r[n] == m for n, m in self.reach.items())]
        if not idxs:
            return
        norm = sum(self.pi[i] for i in idxs)
        for i in idxs:
            self.S[i] += self.pi[i] / norm
        total = sum(self.S)
        alpha = self.p["alpha"]
        self.pi = [(self.S[i] + alpha) / (total + alpha * len(DAG_REACH)) for i in range(len(DAG_REACH))]

    def introspect(self):
        return {"reach": {node: label_of(mask) for node, mask in sorted(self.reach.items())},
                "wants": dict(sorted(self.wants.items()))}
