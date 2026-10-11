"""Redundancy of the matched-state cuts at the first exposed bell.

C004 says memory and goals back each other up over a lifetime, so cutting one
path into the policy may leave the other. A note on the dropped lifelong cut
also said that cutting only those two leaves the self-model's bids as a path,
and that the action moved reliably only when the self-model was cut as well.
This claim tests that pattern on the matched fork, not on two differently
trained lives.

Prediction, fixed before any held-out run: the triple cut changes the realized
action on more lifetimes than a goals-only cut, than a memory-only cut, and than
a goals-and-memory cut that still delivers the self-model. Each excess is more
than 0.10 of paired lifetimes. 0.10 is the smallest extra share that would still
count as a distinct path; it is not a lifetime-scale interaction and it was not
fit to a dev estimate. If the triple cut does not clear a partial cut, that
partial cut already carries the instantaneous effect and the triple is not
identifying a further path.

The same forks record every single and paired cut. Those rates are the map.
The verdict is only the three contrasts above. Scope: L2, this organism,
vigil/dev, this tick.
"""
from mind.claims import Check, Claim

PROBE = "64b5bf633f168201"
# A further path has to move more than one life in ten, or it is not distinct.
REDUNDANCY_MARGIN = 0.10
CONTRASTS = ("goals", "memory", "goals+memory")


def _combine(parts):
    verdicts = [p["verdict"] for p in parts]
    if "FAILS" in verdicts:
        return "FAILS"
    if "INCONCLUSIVE" in verdicts:
        return "INCONCLUSIVE"
    return "HOLDS"


def redundancy(ctx):
    from mind.report import CONDITIONS, fork_rates, matched_forks, probe_fingerprint
    from mind.stats import compare
    got = probe_fingerprint()
    if got != PROBE:
        return {"verdict": "FAILS", "robust": True,
                "summary": f"mind/report.py fingerprint {got} != sealed {PROBE}"}
    rows = matched_forks(ctx.seeds, episodes=300, variant="dev", jobs=ctx.lab.jobs)
    if not rows or any(not (r["sham_identical"] and r["broadcasts_identical"] and r["exposed"]) for r in rows):
        bad = sum(1 for r in rows if not (r["sham_identical"] and r["broadcasts_identical"] and r["exposed"]))
        return {"verdict": "FAILS", "robust": True,
                "summary": f"instrument failed on {bad}/{len(rows)} lifetimes (K11)"}
    rates = fork_rates(rows)
    triple = rates["triple"]["changed"]
    parts = {}
    for name in CONTRASTS:
        parts[name] = compare(triple, rates[name]["changed"], ">", REDUNDANCY_MARGIN,
                              seed="C026-" + name)
    verdict = _combine(parts.values())
    change = {name: sum(rates[name]["changed"]) / len(rows) for name, _cuts in CONDITIONS}
    shown = ", ".join(
        f"{name} {parts[name]['diff']:+.3f} [{parts[name]['lo']:+.3f}, {parts[name]['hi']:+.3f}]"
        for name in CONTRASTS)
    return {
        "verdict": verdict, "robust": True,
        "contrasts": {name: {"diff": parts[name]["diff"], "lo": parts[name]["lo"], "hi": parts[name]["hi"],
                             "verdict": parts[name]["verdict"]} for name in CONTRASTS},
        "change": change,
        "n": len(rows),
        "summary": (f"triple minus partial, claim > {REDUNDANCY_MARGIN}: {shown}; "
                    f"map " + ", ".join(f"{name} {change[name]:.3f}" for name, _cuts in CONDITIONS)),
    }


CLAIM = Claim(
    id="C026",
    title="At a matched bell, the triple cut changes action more than memory, goals, or both",
    statement="In vigil/dev, on the same matched-state forks as the first exposed bell of the late half, the "
              "triple cut of goals, memory and the self-model off the policy changes the realized action on more "
              "lifetimes than cutting goals alone, than cutting memory alone, and than cutting goals and memory "
              "while still delivering the self-model, each by more than 0.10.",
    kind="effect",
    scope="L2",
    question="H013",
    depends_on=("K11",),
    extends=("C004", "C025", "knowledge/questions/H013.md"),
    test=Check(redundancy, seeds=64),
    by="researcher-bot",
    created="2026-10-11",
    rationale="C004's degeneracy and the leftover self-model path are tested at one matched tick, where neither "
              "copy learns on the intervention and both share the pre-intervention state. The map of single and "
              "paired cuts is recorded with the three contrasts the verdict uses.",
)
