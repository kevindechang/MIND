"""Does the surprise broadcast speed control re-adaptation after a silent capability drop?

outage/shift holds P(scan success) at 0.9 for episodes 0–59 and at 0.15 from
episode 60, with no announcements. Manual pays +0.35 and always succeeds; a
failed scan pays -0.5, so one avoided failed scan is worth 0.85 reward. The
lesion sets self_model.surprise=2, above any logistic error, so the surprise
bid never fires. Weight updates are unchanged. Both table scorers see only
public outcomes; this variant emits no alert=, so they are the same rule.

Acute window: episodes 60–74, the first 15 after the drop. Recovered window:
episodes 100–119. The pre-specified pattern is an acute reward advantage of
the intact organism over the lesion of more than 0.5 per episode (more than
half a mis-scan; the same 0.5 reward bar C033 uses for an outage control
effect) and a recovered difference whose whole 95% interval lies inside ±0.5.
The claim holds only if both parts hold. A reliable advantage that is still
there late, or an acute advantage that is absent, refutes this pattern.
"""
from mind.claims import Check, Claim

EPISODES = 120
SHIFT_AT, BEFORE, AFTER = 60, 0.9, 0.15
ACUTE = (60, 75)
RECOVERED = (100, 120)
MARGIN = 0.5
LESION = "organism self_model.surprise=2"


def _mean(xs, start, end):
    part = xs[start:end]
    return sum(part) / len(part)


def _above(lo, hi, margin):
    if lo > margin:
        return "HOLDS"
    if hi <= margin:
        return "FAILS"
    return "INCONCLUSIVE"


def _inside(lo, hi, margin):
    if -margin < lo and hi < margin:
        return "HOLDS"
    if lo >= margin or hi <= -margin:
        return "FAILS"
    return "INCONCLUSIVE"


def _join(parts):
    if any(part == "FAILS" for part in parts):
        return "FAILS"
    if all(part == "HOLDS" for part in parts):
        return "HOLDS"
    return "INCONCLUSIVE"


def readapt(ctx):
    from mind.stats import bootstrap_ci
    from mind.worlds.outage import _SHIFT
    spec = _SHIFT["shift"]
    if (spec["at"], spec["before"], spec["after"]) != (SHIFT_AT, BEFORE, AFTER):
        raise RuntimeError("outage/shift schedule does not match the sealed schedule")
    intact = ctx.lab.runs([("organism", "outage", "shift", seed, EPISODES) for seed in ctx.seeds])
    lesion = ctx.lab.runs([(LESION, "outage", "shift", seed, EPISODES) for seed in ctx.seeds])
    acute, recovered = [], []
    for left, right in zip(intact, lesion):
        for run in (left, right):
            if run["scores"]["sq_alert"] != run["scores"]["sq_table"]:
                raise RuntimeError("alert table diverged from the success table on a silent shift")
            if len(run["scores"]["reward"]) != EPISODES:
                raise RuntimeError("life length does not match the sealed episode count")
        acute.append(_mean(left["scores"]["reward"], *ACUTE) - _mean(right["scores"]["reward"], *ACUTE))
        recovered.append(_mean(left["scores"]["reward"], *RECOVERED) - _mean(right["scores"]["reward"], *RECOVERED))
    am, alo, ahi = bootstrap_ci(acute, seed="C042|acute")
    rm, rlo, rhi = bootstrap_ci(recovered, seed="C042|recovered")
    acute_v, recovered_v = _above(alo, ahi, MARGIN), _inside(rlo, rhi, MARGIN)
    verdict = _join((acute_v, recovered_v))
    return {"verdict": verdict, "robust": True,
            "acute": {"mean": am, "lo": alo, "hi": ahi, "part": acute_v},
            "recovered": {"mean": rm, "lo": rlo, "hi": rhi, "part": recovered_v},
            "summary": f"intact−lesion reward acute {am:+.3f} [{alo:+.3f},{ahi:+.3f}] ({acute_v}, claim > {MARGIN}); "
                       f"recovered {rm:+.3f} [{rlo:+.3f},{rhi:+.3f}] ({recovered_v}, claim inside ±{MARGIN})"}


CLAIM = Claim(
    id="C042",
    title="Surprise broadcast speeds control re-adaptation after a silent capability drop",
    statement="In outage/shift, after scan reliability drops from 0.9 to 0.15 at episode 60 with no announcement, "
              "the intact organism out-earns an organism whose surprise bid never fires (self_model.surprise=2) by "
              "more than 0.5 reward per episode over episodes 60–74, and over episodes 100–119 that difference's "
              "whole 95% interval lies inside ±0.5. Both the plain and the announcement-aware tables are scored on "
              "the same events and receive no alerts.",
    kind="effect",
    scope="L2",
    question="H002",
    depends_on=("K13",),
    extends=("C017", "C018"),
    test=Check(readapt, seeds=16),
    by="researcher-bot",
    created="2026-10-11",
    rationale="Half a mis-scan per episode (a failed scan costs 0.85 against manual) is the smallest control "
              "difference that matters here, and 0.5 is the outage reward bar already used for a content effect. "
              "The recovered band is that same bar: the deficit has recovered only if the late gap is inside it. "
              "This organism, this silent shift only. Not L3.",
)
