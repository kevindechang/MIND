"""The broadcast's own report of the next action, against a transcript narrator.

The grounded report reads only the workspace broadcast: an explicit `pending=`
if the act cue `bell=1` is broadcast, otherwise a remembered `was:request=`,
otherwise `wait`. Confidence labels (`self:`) do not name an action. The
narrator (`rival:narrator`, `mind/report.py`) reads the full public transcript
and no internal state: the last `request` in the episode, and the current bell.
Both are scored on the same ticks — the bell ticks in the late half of the life —
by whether they name the action the organism then takes.

Margin 0.10 is a pre-set scientific bar: ten extra decision ticks in a hundred
is the smallest gap that would mean the internal report adds something real
over a reader that already has the whole public transcript. It was not placed
on a dev estimate.
"""
from mind.claims import Check, Claim

# Ten percentage points of bell ticks. Chosen as the smallest scientifically
# relevant advantage over a full-transcript reader, before held-out evaluation.
MARGIN = 0.10


def report_beats_narrator(ctx):
    from mind.report import score_life
    from mind.stats import compare
    grounded, narrator = [], []
    for seed in ctx.seeds:
        row = score_life("organism", "vigil", seed, 300, "dev")
        grounded.append(row["grounded"])
        narrator.append(row["narrator"])
    est = compare(grounded, narrator, ">", MARGIN, seed="C019")
    return {
        "verdict": est["verdict"], "robust": True,
        "diff": est["diff"], "lo": est["lo"], "hi": est["hi"],
        "grounded": est["a"], "narrator": est["b"],
        "summary": (
            f"bell-tick accuracy grounded {est['a']:.3f} vs narrator {est['b']:.3f}: "
            f"{est['diff']:+.3f} [{est['lo']:+.3f}, {est['hi']:+.3f}] (claim: > {MARGIN})"
        ),
    }


CLAIM = Claim(
    id="C019",
    title="A broadcast report predicts the next action better than a transcript narrator",
    statement="In vigil/dev, on bell ticks in the late half of the life, a report read from the organism's "
              "broadcast (pending, else remembered request, when the bell is broadcast) predicts the next "
              "action better than a narrator with the full public transcript and no internal state, by more "
              "than 0.10.",
    kind="effect",
    scope="L2",
    question="H013",
    extends=("C001", "knowledge/questions/H013.md"),
    test=Check(report_beats_narrator, seeds=16),
    by="Cursor Agent",
    created="2026-10-11",
    rationale="H013: a self-report is valid only if it predicts the next action better than a report with no "
              "access to internal state. The narrator is the strengthened zero-read rival (full transcript). "
              "The margin is the smallest gap that would count as the report adding something.",
)
