"""New self-model state is ledger-folded: shadow, in-process restart, and process replay.

Covers all 21 step/gate combinations on vigil/dev, outage/silent and workshop/dev,
two seeds per world/config, 20 episodes. This checks instrumentation, not cognition.
K01/K02/K06/K07 remain standing substrate checks; this extends coverage to new options.
"""
from mind.claims import Check, Claim

STEPS = ("normalised", "sqrt", "adagrad")
GATES = ("all", "no_memory", "no_goals", "no_memory_goals", "bias", "learned", "uniform")
WORLDS = (("vigil", "dev"), ("outage", "silent"), ("workshop", "dev"))
REPLAY = """
import json, sys
from mind.kernel import Organism
from mind.ledger import MemoryLedger
heads = {}
for key, events in json.load(sys.stdin).items():
    ledger = MemoryLedger()
    for kind, payload in events:
        ledger.append(kind, payload)
    Organism.restore(ledger)
    heads[key] = ledger.head
print(json.dumps(heads))
"""


def replay(ctx):
    import json
    import os
    import subprocess
    import sys
    from mind.claims import ROOT
    from mind.ledger import MemoryLedger
    from mind.runner import run
    from mind.shadow import late_brier, replay_self_model
    failures, lives, heads = [], {}, {}
    for seed in ctx.seeds:
        for world, variant in WORLDS:
            for step in STEPS:
                for gate in GATES:
                    arm = f"organism self_model.step={step} self_model.gate={gate}"
                    key = f"{world}/{variant}/{seed}/{step}/{gate}"
                    ledger = MemoryLedger()
                    ref = run(arm, world, seed, 20, variant, ledger=ledger)
                    died = run(arm, world, seed, 20, variant, kill_at=(5, 29))
                    events = list(ledger)
                    forecasts = replay_self_model(events)
                    if not (ref["head"] == died["head"] and all(f.confidence == f.logged for f in forecasts)
                            and late_brier(forecasts, 20) == ref["metrics"]["brier"]):
                        failures.append(key)
                    lives[key] = [(e.kind, e.payload) for e in events]
                    heads[key] = ledger.head
    for hash_seed in ("1", "99"):
        result = subprocess.run([sys.executable, "-c", REPLAY], input=json.dumps(lives), cwd=ROOT,
                                env=dict(os.environ, PYTHONHASHSEED=hash_seed),
                                capture_output=True, text=True, timeout=120)
        if result.returncode:
            failures.append(f"hash seed {hash_seed}: {result.stderr[-1000:]}")
        elif json.loads(result.stdout) != heads:
            failures.append(f"hash seed {hash_seed}: heads differ")
    return {"verdict": "FAILS" if failures else "HOLDS", "robust": True,
            "failures": failures, "lives": len(lives),
            "summary": f"{len(lives)} lives, 21 options: shadow + restart + 2 fresh-process hash seeds; "
                       f"{len(failures)} failures"}


CLAIM = Claim(
    id="K14", title="Adaptive self-models replay exactly across restarts and processes",
    statement="All 21 step/gate combinations on vigil/dev, outage/silent and workshop/dev reproduce "
              "every logged confidence and Brier in shadows, retain identical heads after two in-process "
              "restarts, and replay without divergence in fresh processes under hash seeds 1 and 99.",
    kind="invariant", scope="instrument", question="H014", extends=("K01", "K06", "K09"),
    test=Check(replay, seeds=2), by="Codex (H014 session)", created="2026-10-11",
)
