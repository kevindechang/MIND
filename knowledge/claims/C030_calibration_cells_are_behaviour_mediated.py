"""C016's calibration cells are not carried by the lesioned organ's own contents (H007, mediation).

C016's two cross-function cells are memory→vigil.calib_gain and goals→vigil.calib_gain:
lesioning either organ lowers the self-model's same-event advantage over a success table.
Read as integration, that says the self-model uses memory's and goals' broadcast contents.
But calib_gain compares two forecasters on ONE arm's events, and the atlas differences it
ACROSS arms, i.e. across different event streams (a lesioned organism behaves differently).
That is the confound that retired C007, C008 and C010, re-entering one level up.

Decomposition. TE = calib_gain(organism) - calib_gain(organism -X), the atlas cell.
DE = the fixed-behaviour direct effect: on the intact organism's own events, the Brier
cost of removing X's contents from the self-model's inputs (mind/shadow.py, exact by K09;
the success table does not change when behaviour is fixed, so DE is in calib_gain units).
Claim: for both organs TE > 0 and DE < TE/4, i.e. mean(TE - 4*DE) > 0 with its whole CI.
In mediation terms TE = DE + the indirect effect, which here includes the event mix AND the
workspace reallocating the organ's freed slots to other contents. Reported, not decided on:
TE split into the success table's change (it sees no contents at all, so this part is pure
event mix) and the self-model's change; and DE split into content (real vs sham) and carry.

Dev exploration (32 seeds). Memory: TE +0.088 [+0.072, +0.103], DE -0.007 [-0.008, -0.005].
At fixed behaviour memory's contents make the self-model WORSE; they do carry information
(real beats a matched sham by +0.003) but carrying their features costs +0.009. Goals:
TE +0.057 [+0.039, +0.075], DE +0.006 [+0.004, +0.008], about a tenth. Strongest
alternative: the informational pathway carries the effect (DE >= TE/4). A modular
forecaster shows the same kind of cell (C031); the valid integration test is C032.
"""
from mind.claims import Check, Claim

ORGANS = ("memory", "goals")
EPISODES = 300
SHARE = 4           # the informational part must stay below 1/SHARE of the atlas effect


def mediation(ctx):
    from mind.shadow import fixed_behaviour_many
    from mind.stats import bootstrap_ci
    conditions = {}
    for organ in ORGANS:
        conditions[f"drop:{organ}"] = {"drop": (organ,)}
        conditions[f"sham:{organ}"] = {"sham": (organ,)}
    shadows = fixed_behaviour_many(ctx.lab, "organism", "vigil", "dev", ctx.seeds, EPISODES, conditions)
    if not all(r["exact"] for r in shadows):
        raise RuntimeError("the unfiltered shadow did not reproduce the organism (K09)")
    intact = ctx.lab.metric("organism", "vigil", "dev", ctx.seeds, EPISODES, "calib_gain")
    intact_table = ctx.lab.metric("organism", "vigil", "dev", ctx.seeds, EPISODES, "brier_table")
    result, ok, failed, parts = {}, True, False, []
    for organ in ORGANS:
        lesioned = ctx.lab.metric(f"organism -{organ}", "vigil", "dev", ctx.seeds, EPISODES, "calib_gain")
        table = [a - b for a, b in zip(intact_table, ctx.lab.metric(f"organism -{organ}", "vigil", "dev", ctx.seeds,
                                                                   EPISODES, "brier_table"))]
        series = {"te": [a - b for a, b in zip(intact, lesioned)],
                  "te_table": table,
                  "te_self": [(a - b) - t for a, b, t in zip(intact, lesioned, table)],
                  "de": [r[f"drop:{organ}"] - r["brier"] for r in shadows],
                  "content": [r[f"sham:{organ}"] - r["brier"] for r in shadows],
                  "carry": [r[f"sham:{organ}"] - r[f"drop:{organ}"] for r in shadows]}
        series["contrast"] = [t - SHARE * d for t, d in zip(series["te"], series["de"])]
        est = {}
        for name, xs in series.items():
            m, lo, hi = bootstrap_ci(xs, seed=f"C030|{organ}|{name}")
            est[name] = {"mean": m, "lo": lo, "hi": hi}
        est["share"] = est["de"]["mean"] / est["te"]["mean"] if est["te"]["mean"] else None
        result[organ] = est
        ok = ok and est["te"]["lo"] > 0 and est["contrast"]["lo"] > 0
        failed = failed or est["te"]["hi"] <= 0 or est["contrast"]["hi"] <= 0
        te, de = est["te"], est["de"]
        share = f"{100 * est['share']:+.0f}%" if est["share"] is not None else "n/a"
        parts.append(f"{organ}: TE {te['mean']:+.3f} [{te['lo']:+.3f},{te['hi']:+.3f}], "
                     f"DE {de['mean']:+.4f} [{de['lo']:+.4f},{de['hi']:+.4f}] (share {share})")
    verdict = "HOLDS" if ok else "FAILS" if failed else "INCONCLUSIVE"
    return {"verdict": verdict, "robust": True, **result,
            "summary": "; ".join(parts) + f" · claim: TE > 0 and DE < TE/{SHARE}"}


CLAIM = Claim(
    id="C030",
    title="The atlas's calibration cells are not carried by the lesioned organ's contents (mediation)",
    statement="In vigil/dev, lesioning memory or goals lowers same-event calibration gain (TE > 0, C016's two "
              "cross-function cells), but for each organ less than a quarter of that effect is informational: at the "
              "intact organism's own behaviour, removing the organ's broadcast contents from the self-model's inputs "
              "costs less than TE/4 in Brier score (mean(TE - 4*DE) > 0 with its whole 95% CI).",
    kind="effect",
    scope="L2",
    question="H007",
    depends_on=("K08", "K09"),
    extends=("C016", "C010"),
    test=Check(mediation, seeds=32),
    by="claude-code (session 01VdSAnY)",
    created="2026-10-11",
    rationale="Separates the two routes by which an organ can move a calibration metric: what its contents tell "
              "the forecaster, and which events its effect on behaviour makes the forecaster face.",
)
