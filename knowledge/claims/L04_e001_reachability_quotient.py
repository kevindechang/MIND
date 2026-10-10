"""E001 v0.4 (v1): the 8 forward three-node DAGs collapse into 7 reachability classes.

Consequence carried forward: in the workshop world no agent, however rich its
memory, can tell graph 5 {(0,1),(1,2)} from graph 7 (graph 5 + (0,2)) by
intervention alone, and it never needs to (they have identical payoffs).
"""
from mind.claims import Check, Claim


def quotient(ctx):
    from mind.legacy import instrument
    v04 = instrument("e001_finite_policy_v04")
    classes = {}
    for i, graph in enumerate(v04.GRAPHS):
        classes.setdefault(v04.effects(graph), []).append(i)
    merged = [ix for ix in classes.values() if len(ix) > 1]
    ok = len(v04.GRAPHS) == 8 and len(classes) == 7 and merged == [[5, 7]]
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True,
            "summary": f"{len(v04.GRAPHS)} DAGs → {len(classes)} reachability classes; merged {merged}"}


CLAIM = Claim(
    id="L04",
    title="E001: eight three-node DAGs, seven reachability classes",
    statement="Exactly two of the eight forward DAGs on {0,1,2} (indices 5 and 7) share a reachability "
              "signature, so the family has 7 interventionally distinguishable classes.",
    kind="fact",
    scope="instrument",
    test=Check(quotient),
    question="H001",
    extends=("experiments/instruments/e001_finite_policy_v04.py",
             "experiments/E001/E001-G0-policy-value-identifiability-v0.4.md"),
    by="pipeline-v2 migration (v1 author: E001 v0.4)",
    created="2026-10-10",
)
