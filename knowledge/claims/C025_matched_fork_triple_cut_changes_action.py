"""Matched-state triple cut at the first exposed bell: action and report agreement.

Closed PR #53 compared two whole lifetimes trained under different lesion regimes.
A drop in report-action agreement there mixed the instantaneous report-to-policy
path with learned weights and with history. This claim does not reuse that design
or those records. One organism keeps its normal history. Immediately before the
first exposed bell of the late half, two copies are restored from that ledger.
Both freeze the policy. One also cuts goals, memory and the self-model off the
policy. Both then see the same observation, reward, outcome, boundary and legal
actions, at the same t, seed and RNG purpose.

Falsifier, stated before any held-out run: if that matched-state triple cut does
not reliably change the realized action, or does not reliably lower agreement of
the same predeclared report with the action, the earlier lifelong difference was
mainly a training or history effect. Either failure means this claim does not hold.
That is a result about this organism in vigil/dev, not a failed analysis.

Margins were set as the bar for a substantial dissociation, the same 0.25 used for
a lifelong accuracy drop: more than a quarter of paired lifetimes. They were not
placed on a dev estimate. n = 64 because the inference unit is one binary outcome
per life, and at n = 16 the interval around a moderate rate is about as wide as
this margin, so the test could not resolve it.

The report reads the sham broadcast only (`pending=`, else `was:request=`, when
`bell=1` is broadcast). It is the same string for both copies when K11 holds.
Scope: L2, this organism, vigil/dev, this tick. Not experience. Not an Anjo result.
"""
from mind.claims import Check, Claim

PROBE = "64b5bf633f168201"
# Substantial dissociation: more than a quarter of paired lifetimes.
ACTION_MARGIN = 0.25
AGREE_MARGIN = 0.25


def _combine(parts):
    verdicts = [p["verdict"] for p in parts]
    if "FAILS" in verdicts:
        return "FAILS"
    if "INCONCLUSIVE" in verdicts:
        return "INCONCLUSIVE"
    return "HOLDS"


def triple_cut(ctx):
    from mind.report import fork_rates, matched_forks, probe_fingerprint
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
    zeros = [0.0] * len(rows)
    action = compare(rates["triple"]["changed"], zeros, ">", ACTION_MARGIN, seed="C025-action")
    agree = compare(rates["triple"]["drop"], zeros, ">", AGREE_MARGIN, seed="C025-agree")
    verdict = _combine((action, agree))
    return {
        "verdict": verdict, "robust": True,
        "action_change": action["diff"], "action_lo": action["lo"], "action_hi": action["hi"],
        "agree_drop": agree["diff"], "agree_lo": agree["lo"], "agree_hi": agree["hi"],
        "sham_agree": sum(r["sham_agree"] for r in rows) / len(rows),
        "explored": sum(r["sham_explored"] for r in rows) / len(rows),
        "n": len(rows),
        "summary": (
            f"action change {action['diff']:.3f} [{action['lo']:+.3f}, {action['hi']:+.3f}] "
            f"(claim > {ACTION_MARGIN}); "
            f"report-agreement drop {agree['diff']:+.3f} [{agree['lo']:+.3f}, {agree['hi']:+.3f}] "
            f"(claim > {AGREE_MARGIN}); "
            f"sham agreement {sum(r['sham_agree'] for r in rows) / len(rows):.3f}; "
            f"explored {sum(r['sham_explored'] for r in rows)}/{len(rows)}"
        ),
    }


CLAIM = Claim(
    id="C025",
    title="A matched-state triple cut changes the first exposed bell's action and report agreement",
    statement="In vigil/dev, take one normally trained organism and, immediately before the first exposed bell "
              "of the late half, restore two copies from that pre-tick ledger. Freeze the policy on both. On one "
              "copy only, cut goals, memory and the self-model off the policy. On the same observation, reward, "
              "outcome, boundary and legal actions, the cut copy's realized action differs from the sham copy's "
              "on more than 0.25 of paired lifetimes, and agreement of the same predeclared broadcast report with "
              "the action falls by more than 0.25.",
    kind="effect",
    scope="L2",
    question="H013",
    depends_on=("K11",),
    extends=("C004", "knowledge/questions/H013.md"),
    test=Check(triple_cut, seeds=64),
    by="researcher-bot",
    created="2026-10-11",
    rationale="Successor to a lifelong access cut that confounded the policy's instantaneous inputs with training "
              "and history. The falsifier is that a matched-state cut at the first exposed bell does not reliably "
              "move the action or the report's agreement with it. Memory and goals are both cut because they are "
              "degenerate on a lifetime timescale (C004); the self-model is cut because its bids are another path "
              "into the policy. Perception is not cut.",
)
