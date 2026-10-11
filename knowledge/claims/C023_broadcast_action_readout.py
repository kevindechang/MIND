"""H013-A: can selected workspace contents predict actions beyond public history?

Both readouts forecast the same next action with the same supervised decoder.
The transcript narrator receives all current-episode public events and lifetime
public counts. The grounded decoder additionally receives workspace tags.
An advantage is not an organism-generated self-report or evidence of L3.
"""
from mind.claims import Check, Claim


def grounded_action_gain(ctx):
    from mind.rivals.report_probe import run_report_probe
    from mind.stats import bootstrap_ci
    margin = 0.02  # absolute multiclass Brier; chosen before any experiment
    estimates = {}
    for variant in ("long", "crowded"):
        runs = [run_report_probe("vigil", variant, s) for s in ctx.seeds]
        values = [float(r["gain"]) for r in runs]
        mean, lo, hi = bootstrap_ci(values, seed="C023:" + variant)
        estimates[variant] = {"mean": mean, "lo": lo, "hi": hi,
                              "n": len(values), "steps": sum(r["steps"] for r in runs)}
    # Intersection-union: both variants must clear the predeclared margin.
    passed = all(x["lo"] > margin for x in estimates.values())
    failed = any(x["hi"] <= margin for x in estimates.values())
    verdict = "HOLDS" if passed else "FAILS" if failed else "INCONCLUSIVE"
    summary = "; ".join("%s: gain %+.4f [%+.4f,%+.4f] (n=%d)" %
                        (v, x["mean"], x["lo"], x["hi"], x["n"])
                        for v, x in estimates.items())
    return {"verdict": verdict, "robust": True, "variants": estimates,
            "margin": margin, "summary": summary}


CLAIM = Claim(
    id="C023",
    title="Broadcast-grounded readout predicts action beyond public transcript",
    statement="With equal frozen readout training, the grounded action readout improves "
              "multiclass Brier loss by >0.02 over the transcript narrator in both "
              "vigil/long and vigil/crowded, each on 24 paired 180-episode lifetimes.",
    kind="effect",
    scope="L2",
    question="H013",
    extends=("C004", "C016"),
    test=Check(grounded_action_gain, seeds=24),
    by="H013 design research agent",
    created="2026-10-11",
    rationale="A nontrivial reportable-content signal must predict real actions, "
              "not merely produce plausible narration. Same action events and "
              "frozen readouts prevent action-mix and in-sample score artifacts.",
)
