"""The integration atlas: a lesion map of the whole organism across every world.

Functional consciousness is operationalised in this program as causally
integrated, persistent, self-monitoring cognition (L2). The atlas makes the
"integrated" part measurable instead of rhetorical. For every lesionable organ
o and every non-redundant competency metric m in every world (`atlas_metrics`),
it estimates the paired, sign-normalised effect of removing o on m.

  reliable         Holm-corrected across ALL organ x metric tests (family-wise
                   alpha 0.05), so the map does not fill with chance findings.
  causal density   fraction of tested pairs with a reliable effect.
  cross-function   reliable HELP of an organ to a competency outside its
                   designed `home`; reported both as cells and as distinct organs.
                   A purely modular system shows none.
  degeneracy       organ pairs whose joint lesion hurts more than the sum of the
                   singles (Holm-corrected separately). Skipped when a lesion pins
                   the metric to a constant (an interaction there is an artifact).

None of these is a consciousness score. They are falsifiable descriptions of
causal organisation that grow automatically as organs, worlds and metrics are added.
"""
from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, List, Optional, Sequence

from . import stats
from .claims import GENERIC_METRICS, metric_orientation
from .organs import DEFAULT_ORGANS, ORGANS
from .worlds import WORLDS

LESIONABLE = tuple(o for o in DEFAULT_ORGANS if o not in ("policy", "perception"))


def competency(world: str, metric: str) -> str:
    base = metric.split("@")[0]
    spec = WORLDS[world].metrics.get(base) or GENERIC_METRICS.get(base)
    return spec[0]


def atlas_metrics(world: str) -> List[str]:
    cls = WORLDS[world]
    return list(cls.atlas_metrics or cls.metrics)


def atlas(lab, seeds: Sequence[int], worlds: Optional[Sequence[str]] = None,
          variants: Optional[Dict[str, str]] = None, organs: Sequence[str] = LESIONABLE,
          pairs: bool = True, base: str = "organism", alpha: float = 0.05) -> Dict[str, Any]:
    worlds = list(worlds or WORLDS)
    variants = variants or {}
    cells: List[Dict[str, Any]] = []
    degeneracy: List[Dict[str, Any]] = []
    skipped: List[str] = []
    for world in worlds:
        variant = variants.get(world, "dev")
        eps = WORLDS[world].default_episodes
        metrics = atlas_metrics(world)
        arms = [base] + [f"{base} -{o}" for o in organs]
        if pairs:
            arms += [f"{base} -{a} -{b}" for a, b in combinations(organs, 2)]
        runs = {arm: lab.runs([(arm, world, variant, s, eps) for s in seeds]) for arm in arms}
        values = {arm: {m: [r["metrics"][m] for r in rs] for m in metrics} for arm, rs in runs.items()}
        for organ in organs:
            home = ORGANS[organ].home
            for m in metrics:
                better = metric_orientation(world, m)
                intact, lesion = values[base][m], values[f"{base} -{organ}"][m]
                # positive effect = the organ HELPS this competency (sign-normalised)
                diffs = [(x - y) if better == "higher" else (y - x) for x, y in zip(intact, lesion)]
                key = f"{world}|{organ}|{m}"
                mean, lo, hi = stats.bootstrap_ci(diffs, seed=key)
                comp = competency(world, m)
                cells.append({"world": world, "variant": variant, "organ": organ, "metric": m,
                              "competency": comp, "home": comp in home, "effect": mean, "lo": lo, "hi": hi,
                              "p": stats.bootstrap_p(diffs, seed=key)})
        if pairs:
            for a, b in combinations(organs, 2):
                for m in metrics:
                    arms_ab = (base, f"{base} -{a}", f"{base} -{b}", f"{base} -{a} -{b}")
                    if any(min(values[x][m]) == max(values[x][m]) for x in arms_ab[1:]):
                        skipped.append(f"{a}+{b}→{world}.{m}")   # a lesion pins this metric
                        continue
                    sign = 1.0 if metric_orientation(world, m) == "higher" else -1.0
                    i, la, lb, z = (values[x][m] for x in arms_ab)
                    # interaction = joint loss beyond the sum of single losses (sign-normalised)
                    inter = [sign * ((x - zz) - (x - ya) - (x - yb)) for x, ya, yb, zz in zip(i, la, lb, z)]
                    key = f"{world}|{a}+{b}|{m}"
                    mean, lo, hi = stats.bootstrap_ci(inter, seed=key)
                    degeneracy.append({"world": world, "organs": [a, b], "metric": m, "synergy": mean,
                                       "lo": lo, "hi": hi, "p": stats.bootstrap_p(inter, seed=key)})
    reliable = stats.holm({f"{c['world']}|{c['organ']}|{c['metric']}": c["p"] for c in cells}, alpha)
    for c in cells:
        r = reliable[f"{c['world']}|{c['organ']}|{c['metric']}"]
        c.update({"reliable": r, "helps": r and c["effect"] > 0, "hurts": r and c["effect"] < 0})
    degenerate = stats.holm({f"{d['world']}|{'+'.join(d['organs'])}|{d['metric']}": d["p"]
                             for d in degeneracy}, alpha)
    for d in degeneracy:
        d["degenerate"] = degenerate[f"{d['world']}|{'+'.join(d['organs'])}|{d['metric']}"] and d["synergy"] > 0
    cross = [c for c in cells if c["helps"] and not c["home"]]
    return {"seeds": list(seeds), "worlds": worlds, "organs": list(organs), "cells": cells,
            "degeneracy": degeneracy, "skipped_pairs": skipped,
            "correction": f"Holm, family-wise alpha {alpha}",
            "summary": {"pairs": len(cells), "reliable": sum(c["reliable"] for c in cells),
                        "causal_density": sum(c["reliable"] for c in cells) / len(cells) if cells else 0.0,
                        "helps": sum(c["helps"] for c in cells),
                        "hurts": sum(c["hurts"] for c in cells),
                        "cross_function": len(cross),
                        "cross_function_organs": sorted({c["organ"] for c in cross}),
                        "cross_function_cells": [f"{c['organ']}→{c['world']}.{c['metric']}" for c in cross],
                        "degenerate_pairs": [f"{'+'.join(d['organs'])}→{d['world']}.{d['metric']}"
                                             for d in degeneracy if d["degenerate"]]}}
