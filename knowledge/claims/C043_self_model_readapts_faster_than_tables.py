"""Does the self-model's same-event advantage over both tables peak acutely after a silent drop?

Same world as C042: outage/shift, no announcements, so the plain success table
and the announcement-aware table are one rule seen twice. They are equally
informed. Calibration is pooled Brier on the intact organism's own events
(sum of squared errors over the window, not the mean of episode Briers).

Acute window episodes 60–74, recovered window episodes 100–119. The claim is
that the self-model's advantage over that shared table (table Brier minus
self-model Brier) is larger acutely than after recovery, by more than 0.004.
0.004 is C018's margin for a same-event calibration advantage when no
announcement is available. It is the bar for a difference of advantages, chosen
as that existing calibration margin, not from a shift sample.
"""
from mind.claims import Check, Claim

EPISODES = 120
SHIFT_AT, BEFORE, AFTER = 60, 0.9, 0.15
ACUTE = (60, 75)
RECOVERED = (100, 120)
MARGIN = 0.004


def _gap(scores, which, start, end):
    count = sum(scores["n"][start:end])
    if count <= 0:
        raise RuntimeError("window has no scored outcomes")
    return (sum(scores[which][start:end]) - sum(scores["sq"][start:end])) / count


def readapt_calib(ctx):
    from mind.stats import bootstrap_ci
    from mind.worlds.outage import _SHIFT
    spec = _SHIFT["shift"]
    if (spec["at"], spec["before"], spec["after"]) != (SHIFT_AT, BEFORE, AFTER):
        raise RuntimeError("outage/shift schedule does not match the sealed schedule")
    rows = ctx.lab.runs([("organism", "outage", "shift", seed, EPISODES) for seed in ctx.seeds])
    diffs, acute_gaps, recovered_gaps = [], [], []
    for run in rows:
        scores = run["scores"]
        if scores["sq_alert"] != scores["sq_table"]:
            raise RuntimeError("alert table diverged from the success table on a silent shift")
        if len(scores["reward"]) != EPISODES:
            raise RuntimeError("life length does not match the sealed episode count")
        acute = _gap(scores, "sq_table", *ACUTE)
        recovered = _gap(scores, "sq_table", *RECOVERED)
        acute_gaps.append(acute)
        recovered_gaps.append(recovered)
        diffs.append(acute - recovered)
    mean, lo, hi = bootstrap_ci(diffs, seed="C043|speed")
    if lo > MARGIN:
        verdict = "HOLDS"
    elif hi <= MARGIN:
        verdict = "FAILS"
    else:
        verdict = "INCONCLUSIVE"
    acute_m, recovered_m = sum(acute_gaps) / len(acute_gaps), sum(recovered_gaps) / len(recovered_gaps)
    return {"verdict": verdict, "robust": True, "diff": mean, "lo": lo, "hi": hi,
            "acute": acute_m, "recovered": recovered_m,
            "summary": f"acute minus recovered same-event advantage {mean:+.4f} [{lo:+.4f},{hi:+.4f}] "
                       f"(claim > {MARGIN}); both tables identical "
                       f"(acute advantage {acute_m:+.4f}, recovered {recovered_m:+.4f})"}


CLAIM = Claim(
    id="C043",
    title="Self-model re-adapts calibration faster than both tables after a silent capability drop",
    statement="In outage/shift, on the organism's own events, the plain success table and the announcement-aware "
              "table match exactly (no alerts are emitted). The self-model's Brier advantage over that shared table "
              "in episodes 60–74 exceeds its advantage in episodes 100–119 by more than 0.004.",
    kind="effect",
    scope="L2",
    question="H002",
    depends_on=("K13",),
    extends=("C017", "C018", "C042"),
    test=Check(readapt_calib, seeds=16),
    by="researcher-bot",
    created="2026-10-11",
    rationale="Both tables receive the same public outcomes. 0.004 is the silent-outage same-event margin (C018), "
              "used here as the smallest calibration-speed gap already treated as worth claiming. This organism "
              "and outage/shift only. Not L3.",
)
