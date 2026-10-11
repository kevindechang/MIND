"""H013-B: access cuts should dissociate reportability from causal action.

A scheduled joint cut hides goals/memory from policy, not from the workspace
readout. Readouts are frozen before the cut; matched lives must have identical
training histories. This probes causal access, not subjective experience.
"""
from mind.claims import Check, Claim


def access_dissociation(ctx):
    from mind.rivals.report_probe import run_report_probe
    from mind.stats import bootstrap_ci
    margin = 0.02
    estimates = {}
    for variant in ("long", "crowded"):
        deltas = []
        for seed in ctx.seeds:
            intact = run_report_probe("vigil", variant, seed, cut=False)
            cut = run_report_probe("vigil", variant, seed, cut=True)
            if intact["training_digest"] != cut["training_digest"]:
                raise AssertionError("matched arms diverged BEFORE scheduled access cut")
            deltas.append(float(intact["gain"]) - float(cut["gain"]))
        mean, lo, hi = bootstrap_ci(deltas, seed="C024:" + variant)
        estimates[variant] = {"mean": mean, "lo": lo, "hi": hi, "n": len(deltas)}
    passed = all(x["lo"] > margin for x in estimates.values())
    failed = any(x["hi"] <= margin for x in estimates.values())
    verdict = "HOLDS" if passed else "FAILS" if failed else "INCONCLUSIVE"
    summary = "; ".join("%s: gain-drop %+.4f [%+.4f,%+.4f] (n=%d)" %
                        (v, x["mean"], x["lo"], x["hi"], x["n"])
                        for v, x in estimates.items())
    return {"verdict": verdict, "robust": True, "variants": estimates,
            "margin": margin, "summary": summary}


CLAIM = Claim(
    id="C024",
    title="Joint access cuts reduce grounded report-action coupling",
    statement="Cutting goals and memory from policy at episode 120, while leaving "
              "their workspace contents reportable, reduces the frozen grounded "
              "readout's Brier advantage over a transcript narrator by >0.02 "
              "in both vigil/long and vigil/crowded across 24 paired lifetimes.",
    kind="effect",
    scope="L2",
    question="H013",
    extends=("C004", "C023"),
    test=Check(access_dissociation, seeds=24),
    by="H013 design research agent",
    created="2026-10-11",
    rationale="Tests whether a reportable content stream remains action-predictive "
              "when its causal access path is severed, using the same pre-cut "
              "training histories and same-event narrator baseline.",
)
