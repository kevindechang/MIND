"""The organism is integrated, not modular: off-home effects and degenerate pairs exist.

Computed from the integration atlas (python -m mind atlas) over all worlds' dev
variants. A purely modular system would show reliable effects only on home
competencies and no degenerate pairs. This claim will be re-tested automatically
as organs and worlds are added, so its numbers will move; its truth may not.
"""
from mind.claims import Check, Claim


def integration(ctx):
    from mind.atlas import atlas
    data = atlas(ctx.lab, ctx.seeds)
    s = data["summary"]
    ok = s["cross_function"] >= 3 and len(s["degenerate_pairs"]) >= 1
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True,
            "causal_density": s["causal_density"], "cross_function": s["cross_function_cells"],
            "degenerate": s["degenerate_pairs"],
            "summary": f"causal density {s['causal_density']:.2f}; {s['cross_function']} cross-function effects; "
                       f"{len(s['degenerate_pairs'])} degenerate pairs"}


CLAIM = Claim(
    id="C014",
    title="The organism's causal organisation is integrated, not modular",
    statement="Across the dev variants of all worlds, at least 3 organs reliably help a competency they were "
              "not designed for, and at least one organ pair is degenerate.",
    kind="effect",
    scope="L2",
    question="H007",
    extends=("C004", "C009", "C013"),
    test=Check(integration, seeds=12),
    by="pipeline-v2",
    retired='v2 review (2026-10-10): the test counted organ x metric CELLS while the statement says ORGANS (only 2 organs qualify, so the statement was false); cells included re-labelled home effects, action-mix Brier artifacts and pinned-metric interactions; no multiplicity control. Superseded by C016 (Holm-corrected, distinct organs, curated metrics).',
    created="2026-10-10",
)
