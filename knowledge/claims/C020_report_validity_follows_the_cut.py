"""Report validity falls where the path from the report to action is cut; reportability stays.

Memory and goals are degenerate (C004), so both are cut. Dev exploration of the
instrument — not a measurement this claim may be edited to fit — showed a third
path: with only those two cuts, `self:` doubt tags still reach the policy and
accuracy does not reliably fall. The self-model is cut as well
(`cut:self_model>policy`) so no broadcast path from those self-reports remains.
Perception is left intact. The intention tokens themselves are not removed from
the workspace; that is what "reportability stays" checks.

Margins, set before held-out evaluation: a drop of 0.25 in next-action accuracy
is a substantial dissociation (a quarter of decision ticks), not a sliver.
Reportability stays if the cut still broadcasts an intention on at least half
of bell ticks and the drop versus the intact organism is under 0.15.
"""
from mind.claims import Check, Claim

# Substantial fall in next-action agreement once the broadcast path to policy is gone.
VALIDITY_DROP = 0.25
# "Stays": not a loss of 0.15 or more, and still present on at least half of bell ticks.
REPORT_LOSS = 0.15
REPORT_FLOOR = 0.50
CUT = "organism cut:goals>policy cut:memory>policy cut:self_model>policy"


def _loss_verdict(intact, cut):
    from mind.stats import bootstrap_ci
    diffs = [a - b for a, b in zip(intact, cut)]
    mean, lo, hi = bootstrap_ci(diffs, seed="C020-report")
    if hi < REPORT_LOSS:
        verdict = "HOLDS"
    elif lo >= REPORT_LOSS:
        verdict = "FAILS"
    else:
        verdict = "INCONCLUSIVE"
    return {"verdict": verdict, "diff": mean, "lo": lo, "hi": hi}


def _combine(parts):
    verdicts = [p["verdict"] for p in parts]
    if "FAILS" in verdicts:
        return "FAILS"
    if "INCONCLUSIVE" in verdicts:
        return "INCONCLUSIVE"
    return "HOLDS"


def report_dissociates(ctx):
    from mind.report import score_life
    from mind.stats import compare, threshold
    intact_g, cut_g, intact_r, cut_r = [], [], [], []
    intact_held, cut_held = [], []
    for seed in ctx.seeds:
        intact = score_life("organism", "vigil", seed, 300, "dev")
        cut = score_life(CUT, "vigil", seed, 300, "dev")
        intact_g.append(intact["grounded"])
        cut_g.append(cut["grounded"])
        intact_r.append(intact["reportable"])
        cut_r.append(cut["reportable"])
        intact_held.append(intact["held"])
        cut_held.append(cut["held"])
    validity = compare(intact_g, cut_g, ">", VALIDITY_DROP, seed="C020-validity")
    loss = _loss_verdict(intact_r, cut_r)
    floor = threshold(cut_r, ">=", REPORT_FLOOR, seed="C020-floor")
    verdict = _combine((validity, loss, floor))
    return {
        "verdict": verdict, "robust": True,
        "validity_drop": validity["diff"], "validity_lo": validity["lo"], "validity_hi": validity["hi"],
        "intact_accuracy": validity["a"], "cut_accuracy": validity["b"],
        "report_loss": loss["diff"], "report_loss_lo": loss["lo"], "report_loss_hi": loss["hi"],
        "intact_reportable": sum(intact_r) / len(intact_r),
        "cut_reportable": floor["mean"], "cut_reportable_lo": floor["lo"], "cut_reportable_hi": floor["hi"],
        "intact_held": sum(intact_held) / len(intact_held),
        "cut_held": sum(cut_held) / len(cut_held),
        "summary": (
            f"accuracy {validity['a']:.3f} → {validity['b']:.3f} "
            f"({validity['diff']:+.3f} [{validity['lo']:+.3f}, {validity['hi']:+.3f}]; claim drop > {VALIDITY_DROP}); "
            f"reportable {sum(intact_r) / len(intact_r):.3f} → {floor['mean']:.3f} "
            f"(loss {loss['diff']:+.3f} [{loss['lo']:+.3f}, {loss['hi']:+.3f}], "
            f"claim loss < {REPORT_LOSS} and cut ≥ {REPORT_FLOOR})"
        ),
    }


CLAIM = Claim(
    id="C020",
    title="Report validity falls when the broadcast path to policy is cut; reportability stays",
    statement="In vigil/dev, on bell ticks in the late half of the life, cutting goals, memory and the "
              "self-model off from the policy lowers broadcast-report accuracy by more than 0.25, while "
              "intention tokens stay reportable: under the cut they are still in the broadcast on at least "
              "half of those ticks, and reportability drops by less than 0.15 relative to the intact organism.",
    kind="effect",
    scope="L2",
    question="H013",
    depends_on=("C004",),
    extends=("C004", "C019", "knowledge/questions/H013.md"),
    test=Check(report_dissociates, seeds=16),
    by="Cursor Agent",
    created="2026-10-11",
    rationale="Access lesions leave a content in the workspace but stop delivering it. Memory and goals are "
              "both cut because they are degenerate (C004). The self-model is cut too because its bids are a "
              "remaining broadcast path into the policy; perception is not cut. Validity is next-action "
              "agreement of the same report as C019. Reportability is whether pending or was:request is still "
              "in the broadcast. held (organ state) is recorded and is not part of the verdict.",
)
