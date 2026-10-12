"""H014 selection must beat optimizer-only, an equal-expert mixture, and dev-selected fixed filters.

Primary: equally world-weighted late Brier improvement > .002 against ALL three
controls, with paired 95% intervals (intersection-union claim). No per-world
superiority claim. Strongest fixed rival selected before sealing on dev seeds
0..7 among normalised/adagrad x five fixed masks plus sqrt/all. Winners below.
Dev scores overlap selection data. Sealed seeds are independent confirmation.

The full 2x7 table and sqrt/all are retained, not only favourable comparisons.
Single-expert controls use less compute; uniform trains the identical five experts.
No claim about policy utility, sparsity, efficiency, transfer or consciousness.
"""
from mind.claims import Check, Claim

WORLDS = (("vigil", "dev", 300, "sqrt/all"), ("outage", "silent", 120, "adagrad/all"))
GATES = ("all", "no_memory", "no_goals", "no_memory_goals", "bias", "learned", "uniform")


def selection(ctx):
    from mind.shadow import fixed_behaviour_many
    from mind.stats import compare
    conditions = {f"{step}/{gate}": {"model_params": {"step": step, "gate": gate}}
                  for step in ("normalised", "adagrad") for gate in GATES}
    conditions["sqrt/all"] = {"model_params": {"step": "sqrt"}}
    by_world, differences = {}, {k: [0.0] * len(ctx.seeds) for k in ("all", "uniform", "fixed")}
    for world, variant, episodes, fixed in WORLDS:
        rows = fixed_behaviour_many(ctx.lab, "organism", world, variant, ctx.seeds, episodes, conditions)
        if not all(r["exact"] for r in rows):
            raise RuntimeError("K09 failed: baseline shadow differs from logged confidence")
        by_world[f"{world}/{variant}"] = {
            "fixed_rival": fixed,
            "means": {k: sum(r[k] for r in rows) / len(rows) for k in conditions},
            "per_seed": [{"seed": r["seed"], **{k: r[k] for k in conditions}} for r in rows],
        }
        for rival, key in (("all", "adagrad/all"), ("uniform", "adagrad/uniform"), ("fixed", fixed)):
            for i, r in enumerate(rows):
                differences[rival][i] += (r[key] - r["adagrad/learned"]) / len(WORLDS)
    contrasts = {k: compare(xs, [0.0] * len(xs), ">", 0.002, seed="C051|" + k)
                 for k, xs in differences.items()}
    verdicts = [r["verdict"] for r in contrasts.values()]
    verdict = "HOLDS" if all(v == "HOLDS" for v in verdicts) else "FAILS" if "FAILS" in verdicts else "INCONCLUSIVE"
    summary = "; ".join(f"vs {k}: {r['diff']:+.4f} [{r['lo']:+.4f},{r['hi']:+.4f}]"
                        for k, r in contrasts.items())
    return {"verdict": verdict, "robust": True, "contrasts": contrasts, "by_world": by_world,
            "summary": "learned AdaGrad selection, mean fixed-behaviour Brier gain " + summary + "; ALL > 0.002"}


CLAIM = Claim(
    id="C051", title="Learned receiver selection adds prediction value beyond the optimizer and fixed filters",
    statement="Equally averaging vigil/dev and outage/silent fixed-behaviour Brier, AdaGrad/learned "
              "beats AdaGrad/all, AdaGrad/uniform and the per-world dev-selected strongest fixed predictor "
              "(sqrt/all in vigil, AdaGrad/all in outage), each by more than 0.002.",
    kind="threshold", scope="L2", question="H014", depends_on=("K09", "K14"),
    extends=("C050", "C030", "C036"), test=Check(selection, seeds=32),
    by="Codex (H014 session)", created="2026-10-11",
    rationale="A conjunction of explicit same-stream rival comparisons; a negative outcome argues against "
              "adding this selection mechanism. No live-trajectory rival panel is substituted for these controls.",
)
