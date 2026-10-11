"""Instrument: two matched forks with no cut are the same action, and cuts do not move the broadcast.

The H013 access test restores two copies from one pre-bell ledger, freezes the policy
on both, and cuts only one. If the two no-cut copies disagree, or if a cut changes the
workspace the report is read from, the contrast is not a matched-state access lesion.
This claim checks that, on the same designated tick the effect claims use (the first
exposed bell of the late half in vigil/dev). It is an instrument check, not a finding
about cognition.
"""
from mind.claims import Check, Claim

# Sealed hash of mind/report.py. A later edit of the probe fails this claim.
PROBE = "64b5bf633f168201"


def sham_matches(ctx):
    from mind.report import matched_forks, probe_fingerprint
    got = probe_fingerprint()
    if got != PROBE:
        return {"verdict": "FAILS", "robust": True,
                "summary": f"mind/report.py fingerprint {got} != sealed {PROBE}"}
    rows = matched_forks(ctx.seeds, episodes=300, variant="dev", jobs=ctx.lab.jobs)
    same = sum(r["sham_identical"] for r in rows)
    broadcasts = sum(r["broadcasts_identical"] for r in rows)
    exposed = sum(r["exposed"] for r in rows)
    n = len(rows)
    holds = got == PROBE and same == n and broadcasts == n and exposed == n
    return {
        "verdict": "HOLDS" if holds else "FAILS", "robust": True,
        "sham_identical": same, "broadcasts_identical": broadcasts, "exposed": exposed, "n": n,
        "summary": (f"{same}/{n} sham forks action-identical at the same t; "
                    f"{broadcasts}/{n} cut forks kept the sham broadcast; "
                    f"{exposed}/{n} ticks exposed an intention"),
    }


CLAIM = Claim(
    id="K11",
    title="Matched forks with no cut are action-identical, and access cuts leave the broadcast",
    statement="In vigil/dev, at the first exposed bell of the late half, two organisms restored from the same "
              "pre-tick ledger, both with freeze:policy and neither cut, take the same action and broadcast the "
              "same tags. Copies that also receive any single, paired, or triple cut of goals, memory and the "
              "self-model into the policy broadcast those same tags.",
    kind="invariant",
    scope="instrument",
    question="H013",
    test=Check(sham_matches, seeds=16),
    by="researcher-bot",
    created="2026-10-11",
    rationale="Instrument check for the matched-state access fork. A sham that is not action-identical, or a cut "
              "that changes the report's broadcast, would confound the access contrast.",
)
