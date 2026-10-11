"""Instrument: the announcement-aware scorer is the success table plus public alerts.

`brier_alert` scores AlertTable on the agent's own events. That table is the
plain success table (same rate, same prior) also updated by public `alert=down`
(scan outcome 0) and `alert=up` (scan outcome 1) before the forecast. Where a
world emits neither announcement the two Brier scores are exactly equal, and
rival:reactive — whose confidence is the plain table — has calib_gain_alert
exactly 0. In outage/dev the announcements are present, so the scores must move.
C041, C042 and C043 rest on this.
"""
from mind.claims import Check, Claim

MATCH = (("outage", "silent"), ("outage", "shift"), ("outage", "shift_late"),
         ("vigil", "dev"), ("workshop", "dev"))
REACTIVE = (("vigil", "dev"), ("workshop", "dev"), ("outage", "silent"))
EPISODES = 40


def wired(ctx):
    bad = []
    for world, variant in MATCH:
        for seed in ctx.seeds:
            metrics = ctx.lab.runs([("organism", world, variant, seed, EPISODES)])[0]["metrics"]
            for suffix in ("", "@all", "@early"):
                if abs(metrics["brier_alert" + suffix] - metrics["brier_table" + suffix]) > 1e-12:
                    bad.append(f"{world}/{variant}/seed{seed}/brier_alert{suffix}")
    for world, variant in REACTIVE:
        for seed in ctx.seeds:
            metrics = ctx.lab.runs([("rival:reactive", world, variant, seed, EPISODES)])[0]["metrics"]
            for suffix in ("", "@all", "@early"):
                if abs(metrics["calib_gain_alert" + suffix]) > 1e-12:
                    bad.append(f"reactive {world}/{variant}/seed{seed}{suffix}")
    moved = []
    for seed in ctx.seeds:
        metrics = ctx.lab.runs([("organism", "outage", "dev", seed, EPISODES)])[0]["metrics"]
        moved.append(abs(metrics["brier_alert@all"] - metrics["brier_table@all"]))
    if max(moved) <= 1e-12:
        bad.append("outage/dev: announcements did not move the alert table")
    ok = not bad
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True, "violations": bad[:8],
            "summary": "alert scorer matches the plain table with no announcements, is zero for "
                       "rival:reactive there, and moves in outage/dev" if ok
                       else f"alert scorer mis-wired: {bad[0]}"}


CLAIM = Claim(
    id="K13",
    title="The announcement-aware scorer matches the success table unless alerts are public",
    statement="brier_alert equals brier_table in every window for the organism in outage/silent, outage/shift, "
              "outage/shift_late, vigil/dev and workshop/dev; calib_gain_alert is exactly 0 for rival:reactive in "
              "vigil/dev, workshop/dev and outage/silent; and in outage/dev the two Brier scores differ.",
    kind="invariant",
    scope="instrument",
    question="H002",
    depends_on=("K08",),
    extends=("K08",),
    test=Check(wired, seeds=4),
    by="researcher-bot",
    created="2026-10-11",
    rationale="C017's table does not read announcements. The stronger same-event scorer has to be the same rule "
              "plus those public alerts, and it has to be a no-op wherever the alerts are absent.",
)
