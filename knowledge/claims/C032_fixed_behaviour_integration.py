"""Fixed-behaviour integration: memory's and goals' contents each inform the self-model (H007).

The valid successor of C016's integration reading. A consumer integrates an organ's contents
if it does better with the real contents than with a matched sham of them while the
organism's behaviour, and so every scored event, stays fixed. The sham is the kernel's
`shuffle:X` applied to the self-model's view only (X's contents from a random one of the
previous 64 ticks: the same statistics, no relation to the present), so the test also
controls for the cost of carrying X's features at all. Family: organ in {memory, goals} x
world in {vigil, outage, workshop} (dev variants), Holm-corrected (alpha 0.05), with the
atlas's bootstrap p-values.

Dev exploration (16 seeds): memory informs the self-model in vigil (+0.003) and outage
(+0.004) but not in the workshop; goals inform it in vigil (+0.012) and are silent elsewhere
(no requests). Strongest alternative: everything the self-model knows comes from perception
and other organs' contents are noise to it; then no memory or goals cell survives.
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
                                    WORLDS[world].default_episodes, conditions)
        if not all(r["exact"] for r in rows):
            raise RuntimeError("the unfiltered shadow did not reproduce the organism (K09)")
        for organ in ORGANS:
            key = f"{organ}>{world}"
            gain = [r[f"sham:{organ}"] - r["brier"] for r in rows]
            m, lo, hi = bootstrap_ci(gain, seed="C032|" + key)
            cells[key] = {"organ": organ, "world": world, "info": m, "lo": lo, "hi": hi,
                          "p": bootstrap_p(gain, seed="C032|" + key)}
    reliable = holm({k: c["p"] for k, c in cells.items()})
    for key, cell in cells.items():
        cell["reliable"] = reliable[key] and cell["info"] > 0
    found = {o: sorted(c["world"] for c in cells.values() if c["organ"] == o and c["reliable"]) for o in ORGANS}
    absent = [o for o in ORGANS if all(c["hi"] <= 0 for c in cells.values() if c["organ"] == o)]
    verdict = "HOLDS" if all(found.values()) else "FAILS" if absent else "INCONCLUSIVE"
    shown = ", ".join(f"{k} {c['info']:+.4f}{'*' if c['reliable'] else ''}" for k, c in cells.items())
    return {"verdict": verdict, "robust": True, "cells": cells, "informs": found,
            "summary": f"Holm-corrected, sham-controlled, fixed behaviour: memory informs the self-model in "
                       f"{found['memory'] or 'no world'}, goals in {found['goals'] or 'no world'} ({shown})"}


CLAIM = Claim(
    id="C032",
    title="At fixed behaviour, memory's and goals' contents each inform the self-model (Holm, sham-controlled)",
    statement="Holding the organism's behaviour fixed, the self-model forecasts reliably better with the real broadcast "
              "contents of memory, and of goals, than with matched shams of them (the kernel's shuffle, from the "
              "previous 64 ticks), each in at least one dev world, with family-wise error controlled (Holm, alpha "
              "0.05) over organ x world.",
    kind="effect",
    scope="L2",
    question="H007",
    depends_on=("K09",),
    extends=("C016", "C030"),
    test=Check(informs, seeds=16),
    by="claude-code (session 01VdSAnY)",
    created="2026-10-11",
    rationale="Integration operationalised as information transfer to a consumer, measured where behaviour cannot "
              "masquerade as it.",
)
