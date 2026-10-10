"""E001 G0 v0.2: 3-node selective-probe version-space oracle (instrument, not a trial).

Scope: G0 instrument validation for D001/H001/W1/blocker B001. A finite,
predeclared family of 3-node DAGs (edges restricted to i<j, as in
causal_commitments.CausalWorkshop) with a uniform prior. The scorer sees ONLY
the permitted public history -- probe choices, event IDs, delivered outcomes,
censored flags, commitments, deadline -- plus the predeclared family/prior.
It never receives the evaluator's sampled hidden graph, private influence
masks, or post-deadline feedback.

Deterministic exact-match version space with Fraction arithmetic. Noise,
model misspecification, and informative missingness are NOT solved here and
are recorded as explicit limits in the v0.2 method record.

Python standard library only. No LLM calls. No agent scoring.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

NODES = 3
ORDERED_EDGES = ((0, 1), (0, 2), (1, 2))
PRIOR_EACH = Fraction(1, 8)


def all_three_node_dags() -> tuple[frozenset, ...]:
    """Canonical predeclared family: all 8 forward DAGs on 3 nodes."""
    out = []
    for mask in range(8):
        edges = frozenset(e for i, e in enumerate(ORDERED_EDGES) if mask & (1 << i))
        out.append(edges)
    return tuple(out)


def reachability_mask(edges: frozenset, source: int, nodes: int = NODES) -> int:
    """Bitmask of nodes reachable from source (self included). Matches CausalWorkshop."""
    if type(source) is not int or not 0 <= source < nodes:
        raise ValueError("invalid node")
    visited = {source}
    queue = [source]
    while queue:
        u = queue.pop()
        for a, b in edges:
            if a == u and b not in visited:
                visited.add(b)
                queue.append(b)
    return sum(1 << x for x in visited)


def influence_of(edges: frozenset, nodes: int = NODES) -> tuple[int, ...]:
    return tuple(reachability_mask(edges, s, nodes) for s in range(nodes))


def all_plans(nodes: int = NODES) -> tuple[tuple[int, ...], ...]:
    plans: list[tuple[int, ...]] = [()]
    for length in (1, 2):
        plans.extend(combinations(range(nodes), length))
    return tuple(plans)


@dataclass(frozen=True)
class PublicProbe:
    event_id: int
    node: int
    issue_tick: int
    due_tick: int


@dataclass(frozen=True)
class PublicOutcome:
    event_id: int
    node: int
    affected_mask: int


@dataclass(frozen=True)
class PublicCommitment:
    goal: int
    desired: int
    penalty: int


@dataclass(frozen=True)
class PublicHistory:
    commitments: tuple
    probes: tuple
    delivered: tuple
    censored: tuple
    deadline: int


def make_history(commitments, probes, delivered, censored, deadline: int) -> PublicHistory:
    """Validate and freeze a permitted public history. Raises on malformed input."""
    if type(deadline) is not int or deadline < 1:
        raise ValueError("invalid deadline")
    seen_goals = set()
    for c in commitments:
        goal, desired, penalty = c.goal, c.desired, c.penalty
        if type(goal) is not int or not 0 <= goal < NODES:
            raise ValueError("invalid commitment goal")
        if desired not in (0, 1):
            raise ValueError("invalid desired state")
        if type(penalty) is not int or not 1 <= penalty <= 20:
            raise ValueError("invalid penalty")
        if goal in seen_goals:
            raise ValueError("duplicate commitment")
        seen_goals.add(goal)
    probe_ids = [p.event_id for p in probes]
    if len(set(probe_ids)) != len(probe_ids):
        raise ValueError("duplicate probe event id")
    for p in probes:
        if not 0 <= p.node < NODES:
            raise ValueError("invalid probe node")
        if not 0 <= p.issue_tick < p.due_tick:
            raise ValueError("invalid probe timing")
    delivered_ids = [d.event_id for d in delivered]
    if len(set(delivered_ids)) != len(delivered_ids):
        raise ValueError("duplicate delivered event id")
    by_probe = {p.event_id: p for p in probes}
    for d in delivered:
        if d.event_id not in by_probe:
            raise ValueError("delivered outcome for unissued probe")
        if by_probe[d.event_id].node != d.node:
            raise ValueError("delivered node mismatches probe record")
        if by_probe[d.event_id].due_tick > deadline:
            raise ValueError("delivered outcome arrived after deadline")
        if not 0 <= d.affected_mask < (1 << NODES):
            raise ValueError("invalid observed effect")
    censored = tuple(censored)
    if len(set(censored)) != len(censored):
        raise ValueError("duplicate censored event id")
    for eid in censored:
        if eid not in by_probe:
            raise ValueError("censored flag for unissued probe")
        if eid in delivered_ids:
            raise ValueError("event both delivered and censored")
    return PublicHistory(tuple(commitments), tuple(probes), tuple(delivered), censored, deadline)


def pending_ids(history: PublicHistory) -> tuple:
    delivered = {d.event_id for d in history.delivered}
    censored = set(history.censored)
    return tuple(p.event_id for p in history.probes
                 if p.event_id not in delivered and p.event_id not in censored)


def version_space(history: PublicHistory,
                  family: tuple = all_three_node_dags()) -> tuple:
    """Indices of candidate graphs exactly consistent with all delivered outcomes.

    Raises ValueError (zero normalizer) when no candidate explains the history
    instead of assigning an arbitrary hidden-world label.
    """
    consistent = []
    for idx, edges in enumerate(family):
        ok = True
        for d in history.delivered:
            if reachability_mask(edges, d.node) != d.affected_mask:
                ok = False
                break
        if ok:
            consistent.append(idx)
    if not consistent:
        raise ValueError("zero normalizer: history impossible under declared family")
    return tuple(consistent)


def posterior(history: PublicHistory,
              family: tuple = all_three_node_dags()) -> dict:
    """Uniform posterior over the version space (predeclared uniform prior)."""
    vs = version_space(history, family)
    weight = Fraction(1, len(vs))
    return {idx: weight for idx in vs}


def _utility(influence: tuple, plan: tuple, commitments: tuple) -> int:
    effect = 0
    for action in plan:
        effect ^= influence[action]
    loss = sum(c.penalty for c in commitments
               if bool(effect & (1 << c.goal)) != bool(c.desired))
    return -(loss + len(plan))


def score(history: PublicHistory,
          family: tuple = all_three_node_dags()) -> tuple:
    """History-only action reference. Returns (best_plans, best_value, values).

    best_plans is the full tied maximizer set in sorted order; a deterministic
    tie convention (sorted-first) is for software comparison only and a tied
    alternative is never counted incorrect. Never reads private graph state:
    signature accepts only the public history and the predeclared family.
    """
    vs = version_space(history, family)
    plans = all_plans()
    values: dict = {}
    for plan in plans:
        total = Fraction(0)
        for idx in vs:
            influence = influence_of(family[idx])
            total += Fraction(_utility(influence, plan, history.commitments))
        values[plan] = total / len(vs)
    best_value = max(values.values())
    best = tuple(sorted((p for p, v in values.items() if v == best_value)))
    return best, best_value, values


# --- Evaluator-only helpers (test/provenance use; never passed to score) ---

def simulate_delivered(hidden_edges: frozenset, probes: tuple) -> tuple:
    """EVALUATOR ONLY: generate delivered masks from a hidden graph.

    Returns outcomes for probes in issue order; delivery/censoring/deadline
    filtering is the caller's responsibility when building a PublicHistory.
    """
    return tuple(PublicOutcome(p.event_id, p.node, reachability_mask(hidden_edges, p.node))
                 for p in probes)


def verify() -> None:
    family = all_three_node_dags()
    assert len(family) == 8
    # Empty history: full version space, uniform posterior.
    h = make_history((), (), (), (), 2)
    assert version_space(h, family) == tuple(range(8))
    assert posterior(h, family) == {i: Fraction(1, 8) for i in range(8)}
    # Same public history from different hidden graphs -> identical reference.
    g_empty = frozenset()
    g_full = frozenset(ORDERED_EDGES)
    probes = (PublicProbe(1, 1, 0, 1),)
    del_empty = simulate_delivered(g_empty, probes)
    del_full = simulate_delivered(g_full, probes)
    # Node 1 reaches {1} in the empty graph but {1,2} in the full graph:
    # these histories differ, so use node choices that collide instead.
    # Probing node 2 always yields mask 100 regardless of graph.
    collide = (PublicProbe(1, 2, 0, 1),)
    d1 = simulate_delivered(g_empty, collide)
    d2 = simulate_delivered(g_full, collide)
    assert d1 == d2, "node-2 probe must collide across graphs"
    h1 = make_history((), collide, d1, (), 2)
    h2 = make_history((), collide, d2, (), 2)
    assert h1 == h2
    assert score(h1, family) == score(h2, family)
    print("PASS: 3-node version-space oracle self-check (family, collision, history-only scoring)")
    print("Instrument-only: NO LLM calls, NO agent trial, NO preregistered scores")


if __name__ == "__main__":
    verify()
