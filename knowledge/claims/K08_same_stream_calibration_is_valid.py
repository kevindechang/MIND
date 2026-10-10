"""Measurement validity: the same-stream calibration metric reads exactly zero for the table itself.

`calib_gain` scores a per-action success table on the agent's own events and
subtracts the agent's Brier score. For rival:reactive, whose forecaster IS that
table rule, the gain must be exactly 0 in every world and window; anything else
means the metric is mis-wired. C017 and C018 rest on this.
"""
from mind.claims import Check, Claim


def validity(ctx):
    from mind.worlds import WORLDS
    bad = []
    for world in sorted(WORLDS):
        eps = min(WORLDS[world].default_episodes, 60)
        for seed in ctx.seeds:
            m = ctx.lab.runs([("rival:reactive", world, "dev", seed, eps)])[0]["metrics"]
            for key in ("calib_gain", "calib_gain@all", "calib_gain@early"):
                if abs(m[key]) > 1e-12:
                    bad.append(f"{world}/{seed}/{key}={m[key]}")
    return {"verdict": "HOLDS" if not bad else "FAILS", "robust": True, "violations": bad[:10],
            "summary": "rival:reactive calib_gain is exactly 0 in every world, seed and window" if not bad
                       else f"metric mis-wired: {bad[0]}"}


CLAIM = Claim(
    id="K08",
    title="The same-stream calibration metric is valid (zero for the table itself)",
    statement="For the reactive rival, whose forecaster is the success-table rule, calib_gain is exactly zero in "
              "every world, seed and window.",
    kind="invariant",
    scope="instrument",
    test=Check(validity, seeds=4),
    by="pipeline-v2 (v2 review fix)",
    created="2026-10-10",
)
