"""Instrument: the shadow's sham changes content only (presence, count and feature load kept).

PR #29 review (P1): a sham that replaced an organ's contents with its broadcast from a
random earlier tick injected the organ where it was absent and removed it where it was
present (goals' presence changed at about half of vigil's ticks), and so changed the
self-model's feature count, which sets its step size (lr / len(feats)). Real minus sham
then mixed content with presence and feature load (C032 retired; successor C036).

The corrected sham (mind/shadow.py) permutes content at a fixed load. This claim checks
it in every world and variant, for memory and goals, at every tick: the organ is present
in the sham view exactly when it is in the real view, with the same number of distinct
features, and the self-model's total feature count is unchanged; the content does
change on some tick wherever the organ appears; and the sham never has to fall back on
real contents in the scored (late) half of a life. K09 checks unfiltered replay only.
"""
from mind.claims import Check, Claim

ORGANS = ("memory", "goals")


def content_only(ctx):
    from mind.ledger import MemoryLedger
    from mind.runner import run
    from mind.shadow import sham_audit
    from mind.worlds import WORLDS
    lives, audits, failures, fallbacks = 0, 0, [], 0
    for world in sorted(WORLDS):
        for variant in WORLDS[world].variants:
            for seed in ctx.seeds:
                ledger = MemoryLedger()
                result = run("organism", world, seed, None, variant, ledger=ledger)
                events = list(ledger)
                lives += 1
                for organ in ORGANS:
                    a = sham_audit(events, organ, result["episodes"])
                    audits += 1
                    fallbacks += a["fallback"]
                    ok = (a["presence_kept"] and a["count_kept"] and a["load_kept"]
                          and a["fallback_scored"] == 0 and (a["present"] == 0 or a["changed"] > 0))
                    if not ok:
                        failures.append(f"{world}/{variant}/seed{seed}/{organ}")
    return {"verdict": "HOLDS" if not failures else "FAILS", "robust": True, "lives": lives,
            "audits": audits, "early_fallback_ticks": fallbacks, "failures": failures[:10],
            "summary": f"{audits - len(failures)}/{audits} sham audits ({lives} lives, every world and variant) keep "
                       f"presence, distinct-feature count and feature load at every tick, change content, and "
                       f"never fall back in the scored half ({fallbacks} early fallback ticks in all)"}


CLAIM = Claim(
    id="K10",
    title="The shadow's sham changes content only: presence, count and feature load are kept at every tick",
    statement="In every world and variant, for memory and goals, the shadow's sham keeps the organ's presence, its "
              "number of distinct features and the self-model's total feature count identical to the real view at "
              "every tick, changes the content wherever the organ appears, and never falls back on real contents "
              "in the scored half of a life.",
    kind="invariant",
    scope="instrument",
    test=Check(content_only, seeds=4),
    question="H007",
    depends_on=("K09",),
    extends=("K09",),
    by="claude-code (session 01VdSAnY)",
    created="2026-10-11",
    rationale="A content control is only a content control if it holds everything else fixed.",
)
