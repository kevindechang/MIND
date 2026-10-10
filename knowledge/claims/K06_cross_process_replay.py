"""Replay determinism across processes and hash seeds, for every lesion configuration.

K01 replays in the SAME process, so it cannot see hash randomisation (iteration
order of string sets) or other process-global state; K02 crosses processes but
only for the default organism. Here every life is replayed in fresh Python
processes under three different PYTHONHASHSEEDs; Organism.restore re-derives and
verifies every decision, so any order-dependent organ fails (v2 review, finding 6).
"""
from mind.claims import Check, Claim

CONFIGS = ("organism", "organism -memory", "organism -goals", "organism -self_model",
           "organism capacity=inf", "organism cut:memory>policy",
           "organism shuffle:memory freeze:self_model", "organism @2:-memory", "organism @3:freeze:memory")

REPLAY = """
import json, sys
from mind.kernel import Organism
from mind.ledger import MemoryLedger
out = {}
for name, events in json.load(sys.stdin).items():
    led = MemoryLedger()
    for kind, payload in events:
        led.append(kind, payload)
    Organism.restore(led)
    out[name] = led.head
print(json.dumps(out))
"""


def cross_process(ctx):
    import json
    import os
    import subprocess
    import sys
    from mind.claims import ROOT
    from mind.ledger import MemoryLedger
    from mind.runner import run
    from mind.worlds import WORLDS
    lives, heads = {}, {}
    for seed in ctx.seeds:
        for world in sorted(WORLDS):
            for i, config in enumerate(CONFIGS):
                led = MemoryLedger()
                heads[f"{world}|{seed}|{i}"] = run(config, world, seed, 8, ledger=led)["head"]
                lives[f"{world}|{seed}|{i}"] = [(e.kind, e.payload) for e in led]
    failures = []
    for hashseed in ("1", "2", "3"):
        p = subprocess.run([sys.executable, "-c", REPLAY], input=json.dumps(lives), cwd=ROOT,
                           env=dict(os.environ, PYTHONHASHSEED=hashseed), capture_output=True, text=True,
                           timeout=900)
        if p.returncode != 0:
            failures.append(f"PYTHONHASHSEED={hashseed}: {p.stderr.strip().splitlines()[-1]}")
            continue
        got = json.loads(p.stdout)
        failures += [f"PYTHONHASHSEED={hashseed}: {k}" for k in heads if got.get(k) != heads[k]]
    return {"verdict": "HOLDS" if not failures else "FAILS", "robust": True, "lives": len(lives),
            "failures": failures[:10],
            "summary": f"{len(lives)} lives × 3 hash seeds in fresh processes: "
                       f"{'all replays verified, heads identical' if not failures else 'DIVERGED: ' + failures[0]}"}


CLAIM = Claim(
    id="K06",
    title="Replay is deterministic across processes and hash seeds, under every lesion",
    statement="Lives of every lesion configuration in every world, replayed from their ledgers in fresh processes "
              "under PYTHONHASHSEED 1, 2 and 3, re-derive every logged decision and reach identical head hashes.",
    kind="invariant",
    scope="instrument",
    test=Check(cross_process, seeds=4),
    question="H008",
    depends_on=(),
    extends=("K01",),
    by="pipeline-v2 (v2 review fix)",
    created="2026-10-10",
)
