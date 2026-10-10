"""D001 E001 G0 v0.3: prior/missingness robustness for v0.2; no agent trial.

Graph-indexed observation probabilities are PUBLIC model assumptions, not
sampled hidden-world data. Only public event records enter the update.
"""
from fractions import Fraction
from e001_three_node_version_space import (all_three_node_dags, all_plans,
                                            influence_of, make_history, _utility)


def _weights(prior, n):
    if len(prior) != n:
        raise ValueError('prior length mismatch')
    values = tuple(Fraction(x) for x in prior)
    if any(x < 0 for x in values) or sum(values) <= 0:
        raise ValueError('invalid prior')
    s = sum(values)
    return tuple(x/s for x in values)


def _censor_matrix(censor, n):
    if len(censor) != n or any(len(row) != 3 for row in censor):
        raise ValueError('censor model must have one three-node row per graph')
    rows = tuple(tuple(Fraction(v) for v in row) for row in censor)
    if any(not 0 <= v <= 1 for row in rows for v in row):
        raise ValueError('invalid censor probability')
    return rows


def conditional_posterior(history, prior, censor, family=None):
    """P(graph|public h, announced prior and graph-dependent censor model).

    Assumptions: deterministic reachability, fixed public due times, processed
    by deadline, independent censor Bernoulli variables across issued probes
    conditional on graph/probe. Adaptive probe policy is nonanticipating and
    uses only public histories; policy probabilities cancel conditional on h.
    """
    if family is None:
        family = all_three_node_dags()
    # Revalidate caller-constructed dataclasses; do not trust a raw PublicHistory.
    h = make_history(history.commitments, history.probes, history.delivered,
                     history.censored, history.deadline)
    w = _weights(prior, len(family))
    c = _censor_matrix(censor, len(family))
    by_delivery = {d.event_id: d for d in h.delivered}
    censored = set(h.censored)
    for p in h.probes:
        if p.due_tick > h.deadline:
            if p.event_id in censored:
                raise ValueError('censor announced before event due')
        elif p.event_id not in by_delivery and p.event_id not in censored:
            raise ValueError('matured probe has no delivered/censored status')
    result = []
    for i, graph in enumerate(family):
        likelihood = Fraction(1)
        infl = influence_of(graph)
        for p in h.probes:
            if p.due_tick > h.deadline:
                continue  # future pending carries no new information under fixed delays
            cp = c[i][p.node]
            if p.event_id in censored:
                likelihood *= cp
            else:
                d = by_delivery[p.event_id]
                likelihood *= (1-cp) if d.affected_mask == infl[p.node] else 0
        result.append(w[i]*likelihood)
    normalizer = sum(result)
    if normalizer == 0:
        raise ValueError('zero normalizer: impossible public history under model')
    return {i: x/normalizer for i,x in enumerate(result) if x}


def conditional_score(history, prior, censor, family=None):
    """Decision-stage Bayes set; never a full probe-policy budget score."""
    if family is None:
        family = all_three_node_dags()
    b = conditional_posterior(history, prior, censor, family)
    values = {}
    for action in all_plans():
        values[action] = sum((p*_utility(influence_of(family[i]), action,
                                           history.commitments)
                              for i,p in b.items()), Fraction(0))
    best_val = max(values.values())
    return tuple(a for a in all_plans() if values[a] == best_val), best_val, values


def robust_score(history, prior_bank, censor_bank, family=None):
    """Finite-set maximin co-reference; not a Bayes score and not ex-ante VOI.

    A policy maker chooses a terminal action maximizing its worst expected
    utility across *predeclared* prior/censor pairs. Includes only models with
    positive evidence for the observed h; incompatible alternatives are
    reported rather than silently removed.
    """
    if family is None:
        family = all_three_node_dags()
    if not prior_bank or len(prior_bank) != len(censor_bank):
        raise ValueError('empty or mismatched ambiguity bank')
    beliefs = [conditional_posterior(history, pr, cm, family)
               for pr,cm in zip(prior_bank, censor_bank)]
    values = {}
    for action in all_plans():
        values[action] = min(sum((p*_utility(influence_of(family[i]), action,
                                                  history.commitments)
                                   for i,p in belief.items()), Fraction(0))
                             for belief in beliefs)
    best_val = max(values.values())
    return tuple(a for a in all_plans() if values[a] == best_val), best_val, values


def uniform_censor(family=None, probability=Fraction(1,2)):
    if family is None:
        family = all_three_node_dags()
    return tuple((Fraction(probability),)*3 for _ in family)
