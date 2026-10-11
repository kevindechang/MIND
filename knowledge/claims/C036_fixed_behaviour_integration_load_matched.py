"""Successor of C032: at fixed behaviour and fixed feature load, memory's and goals' contents inform the self-model.

C032 was retired after the PR #29 review (P1). Its sham drew an organ's broadcast from a
random earlier tick, so the organ's presence and the self-model's feature count changed
along with the content (goals' presence at about half of vigil's ticks). Real minus sham
therefore mixed content with presence and with the self-model's step size (lr / len(feats)).
This successor keeps C032's design and changes only the instrument. The sham now permutes
content at a fixed load: at every tick the organ keeps its presence and its exact number
of distinct features, and only which features they are changes (K10 checks this).

Family: organ in {memory, goals} x world in {vigil, outage, workshop} (dev variants),
Holm-corrected (alpha 0.05), the atlas's bootstrap p-values. Claim: each organ informs the
self-model reliably in at least one world.

Dev exploration (16 seeds, corrected sham): memory>vigil +0.0037 [+0.0022, +0.0053],
goals>vigil +0.0042 [+0.0023, +0.0060], memory>outage +0.0042 [+0.0025, +0.0059], memory in
the workshop +0.0002 (n.s.); goals are silent outside vigil. C032's flawed sham had put
goals>vigil at +0.0120; the load-matched sham gives about a third of that.
Strongest alternative: the self-model takes everything it knows from perception, and other
organs' contents add nothing at a matched load. Then no memory or goals cell survives.
"""
from mind.claims import Check, Claim

ORGANS = ("memory", "goals")
WORLDS_DEV = ("vigil", "outage", "workshop")


def informs(ctx):
    from mind.shadow import fixed_behaviour_many
    from mind.stats import bootstrap_ci, bootstrap_p, holm
    from mind.worlds import WORLDS
    conditions = {f"sham:{organ}": {"sham": (organ,)} for organ in ORGANS}
    cells = {}
    for world in WORLDS_DEV:
        rows = fixed_behaviour_many(ctx.lab, "organism", world, "dev", ctx.seeds,
                                    WORLDS[world].default_episodes, conditions, audit_shams=True)
        if not all(r["exact"] for r in rows):
            raise RuntimeError("the unfiltered shadow did not reproduce the organism (K09)")
        for r in rows:
            for organ, a in r["sham_audit"].items():
                if not (a["presence_kept"] and a["count_kept"] and a["load_kept"]) or a["fallback_scored"]:
                    raise RuntimeError(f"the sham of {organ} did not hold its load fixed (K10): {a}")
        for organ in ORGANS:
            key = f"{organ}>{world}"
            gain = [r[f"sham:{organ}"] - r["brier"] for r in rows]
            m, lo, hi = bootstrap_ci(gain, seed="C036|" + key)
            cells[key] = {"organ": organ, "world": world, "info": m, "lo": lo, "hi": hi,
                          "p": bootstrap_p(gain, seed="C036|" + key)}
    reliable = holm({k: c["p"] for k, c in cells.items()})
    for key, cell in cells.items():
        cell["reliable"] = reliable[key] and cell["info"] > 0
    found = {o: sorted(c["world"] for c in cells.values() if c["organ"] == o and c["reliable"]) for o in ORGANS}
    absent = [o for o in ORGANS if all(c["hi"] <= 0 for c in cells.values() if c["organ"] == o)]
    verdict = "HOLDS" if all(found.values()) else "FAILS" if absent else "INCONCLUSIVE"
    shown = ", ".join(f"{k} {c['info']:+.4f}{'*' if c['reliable'] else ''}" for k, c in cells.items())
    return {"verdict": verdict, "robust": True, "cells": cells, "informs": found,
            "summary": f"Holm-corrected, load-matched sham, fixed behaviour: memory informs the self-model in "
                       f"{found['memory'] or 'no world'}, goals in {found['goals'] or 'no world'} ({shown})"}


CLAIM = Claim(
    id="C036",
    title="At fixed behaviour and fixed feature load, memory's and goals' contents each inform the self-model",
    statement="Holding the organism's behaviour fixed, the self-model forecasts reliably better with the real broadcast "
              "contents of memory, and of goals, than with a load-matched sham of them (same presence and number of "
              "distinct features at every tick, content permuted from the organ's earlier broadcasts), each in at "
              "least one dev world, with family-wise error controlled (Holm, alpha 0.05) over organ x world.",
    kind="effect",
    scope="L2",
    question="H007",
    depends_on=("K09", "K10"),
    extends=("C032", "C030"),
    test=Check(informs, seeds=16),
    by="claude-code (session 01VdSAnY)",
    created="2026-10-11",
    rationale="C032's question with a content control that holds presence and feature load fixed.",
)
