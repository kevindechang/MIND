"""The integration atlas: a lesion map of the whole organism across every world.

Functional consciousness is operationalised in this program as causally
integrated, persistent, self-monitoring cognition (L2). The atlas makes the
"integrated" part measurable instead of rhetorical. For every lesionable organ
o and every competency metric m in every world, it estimates the paired effect
of removing o on m. From that matrix:

  causal density   fraction of (organ, metric) pairs with a reliable effect.
                   Independent modules give a sparse, block-diagonal map.
  cross-function   reliable effects of an organ on a competency it was NOT
                   designed for (its `home`). These are evidence that
                   information is shared across functions, the defining L2 claim.
  degeneracy       for organ pairs: the double lesion hurts more than the sum
                   of the singles (redundant, mutually backing-up organs).

None of these is a consciousness score. They are falsifiable, comparable
descriptions of causal organisation that grow automatically as contributors add
organs, worlds and metrics. (A lesion-based cousin of 'causal density' measures
of neural dynamics; see knowledge/questions/H003.md and H007.md.)
"""
from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, List, Optional, Sequence, Tuple

from . import stats
from .claims import GENERIC_METRICS, metric_orientation
from .organs import DEFAULT_ORGANS, ORGANS
from .worlds import WORLDS

LESIONABLE = tuple(o for o in DEFAULT_ORGANS if o not in ("policy", "perception"))


def competency(world: str, metric: str) -> str:
    base = metric.split("@")[0]
    spec = WORLDS[world].metrics.get(base) or GENERIC_METRICS.get(base)
    return spec[0]


def atlas(lab, seeds: Sequence[int], worlds: Optional[Sequence[str]] = None,
          variants: Optional[Dict[str, str]] = None, organs: Sequence[str] = LESIONABLE,
          pairs: bool = True, base: str = "organism") -> Dict[str, Any]:
    worlds = list(worlds or WORLDS)
    variants = variants or {}
    cells: List[Dict[str, Any]] = []
    degeneracy: List[Dict[str, Any]] = []
    for world in worlds:
        variant = variants.get(world, "dev")
        eps = WORLDS[world].default_episodes
        metrics = [m for m in WORLDS[world].metrics]
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
                mean, lo, hi = stats.bootstrap_ci(diffs, seed=f"{world}|{organ}|{m}")
                comp = competency(world, m)
                cells.append({"world": world, "variant": variant, "organ": organ, "metric": m,
                              "competency": comp, "home": comp in home, "effect": mean,
                              "lo": lo, "hi": hi,
                              "reliable": lo > 0 or hi < 0, "helps": lo > 0, "hurts": hi < 0})
        if pairs:
            for a, b in combinations(organs, 2):
                for m in metrics:
                    better = metric_orientation(world, m)
                    sign = 1.0 if better == "higher" else -1.0
                    i, la, lb = values[base][m], values[f"{base} -{a}"][m], values[f"{base} -{b}"][m]
                    lab_ = values[f"{base} -{a} -{b}"][m]
                    # interaction = joint loss beyond the sum of single losses (sign-normalised)
                    inter = [sign * ((x - z) - (x - ya) - (x - yb)) for x, ya, yb, z in zip(i, la, lb, lab_)]
                    mean, lo, hi = stats.bootstrap_ci(inter, seed=f"{world}|{a}+{b}|{m}")
                    degeneracy.append({"world": world, "organs": [a, b], "metric": m, "synergy": mean,
                                       "lo": lo, "hi": hi, "degenerate": lo > 0})
    reliable = [c for c in cells if c["reliable"]]
    cross = [c for c in cells if c["helps"] and not c["home"]]
    return {"seeds": list(seeds), "worlds": worlds, "organs": list(organs), "cells": cells,
            "degeneracy": degeneracy,
            "summary": {"pairs": len(cells), "reliable": len(reliable),
                        "causal_density": len(reliable) / len(cells) if cells else 0.0,
                        "helps": sum(c["helps"] for c in cells),
                        "hurts": sum(c["hurts"] for c in cells),
                        "cross_function": len(cross),
                        "cross_function_cells": [f"{c['organ']}→{c['world']}.{c['metric']}" for c in cross],
                        "degenerate_pairs": [f"{'+'.join(d['organs'])}→{d['world']}.{d['metric']}"
                                             for d in degeneracy if d["degenerate"]]}}
