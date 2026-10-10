"""The organism is integrated, not modular — tested strictly.

Successor of C014 (retired after review: it counted cells, not organs, and
included artifacts). The atlas here uses only non-redundant metrics per world,
scores calibration on the agent's own events (calib_gain), skips interactions
where a lesion pins a metric, and controls family-wise error with Holm across
ALL organ × metric tests. An existence claim: when nothing survives correction
the verdict is INCONCLUSIVE (absence of evidence), never HOLDS.
"""
from mind.claims import Check, Claim


def integration(ctx):
    from mind.atlas import atlas
    s = atlas(ctx.lab, ctx.seeds)["summary"]
    organs, pairs = s["cross_function_organs"], s["degenerate_pairs"]
    ok = len(organs) >= 1 and len(pairs) >= 1
    return {"verdict": "HOLDS" if ok else "INCONCLUSIVE", "robust": True,
            "cross_function_organs": organs, "cross_function_cells": s["cross_function_cells"],
            "degenerate": pairs, "causal_density": s["causal_density"],
            "summary": f"Holm-corrected: {len(organs)} organ(s) with off-home help {organs}; "
                       f"{len(pairs)} degenerate pair(s); causal density {s['causal_density']:.2f}"}


CLAIM = Claim(
    id="C016",
    title="Integrated, not modular (Holm-corrected, distinct organs)",
    statement="With family-wise error controlled (Holm, alpha 0.05) over every organ x curated-metric lesion effect "
              "in all worlds' dev variants, at least one organ reliably helps a competency outside its designed "
              "home, and at least one organ pair is degenerate.",
    kind="effect",
    scope="L2",
    question="H007",
    extends=("C014", "C004"),
    test=Check(integration, seeds=12),
    by="pipeline-v2 (v2 review fix)",
    created="2026-10-10",
)
