# MIND

**Anjo's research program toward functional consciousness**, operationalised as causally integrated, persistent,
self-monitoring cognition. **Status: not achieved.** The program also studies testable cognitive, affective,
moral and social functions without equating them with subjective experience. The scope and ethical limits are in
[RESEARCH_SCOPE.md](docs/RESEARCH_SCOPE.md). The only results status page is [STATUS.md](STATUS.md), generated
from executable evidence.

## How it works

Every contribution is built on top of the previous ones, mechanically:

* **One organism.** A small learning agent ([mind/kernel.py](mind/kernel.py)) whose organs (perception, memory, goals,
  self-model, policy) compete for a capacity-limited global workspace. Its only durable state is a hash-chained
  ledger, so it survives real `SIGKILL`s byte-for-byte. Every experiment lesions *this* organism, so each new organ
  or lesion operator is inherited by every later experiment.
* **One world suite.** [mind/worlds/](mind/worlds/) holds seeded, partially observable tasks with held-out variants,
  including the E001 causal workshop, whose exact optimum is the v1 dynamic program, imported unchanged.
* **One rival zoo.** [mind/rivals/](mind/rivals/) holds standing competitors on the same learner. A claim that a
  mechanism is better is automatically pitted against every relevant rival, past and future.
* **One claim ledger.** [knowledge/claims/](knowledge/claims/) holds results as executable files. Predictions are
  sealed by git: held-out seeds derive from the commit that registered them. Evidence levels, staleness and the
  research frontier are computed, never asserted.

The design rationale, and why v1's twenty-file governance never compounded, is in
[docs/PIPELINE.md](docs/PIPELINE.md).

## Quickstart (standard library only; tested on Python 3.11, 3.12 and 3.13 with identical results)

```bash
python -m mind status                       # computed state of all knowledge + frontier
python -m mind check --quick                # re-run every claim (4 dev seeds; `check` alone = full strength)
python -m mind run "organism -memory" vigil --seeds 8     # explore: lesion memory, watch commitments fail
python -m mind atlas                        # lesion map: which organ causally serves which competency
python -m unittest discover -s tests        # substrate and claims-engine tests
```

Contributors and agents start at [GO.md](GO.md). The rules are in [AGENTS.md](AGENTS.md) and
[CONTRIBUTING.md](CONTRIBUTING.md).

## Map

| Path | What |
|---|---|
| `mind/` | the substrate: kernel, ledger, organs, worlds, rivals, runner, claims engine, CLI |
| `knowledge/claims/` | executable claims (`L*` ported v1 results, `K*` substrate invariants, `C*` organism findings) |
| `knowledge/records/` | append-only evaluation records (who, where, which code, which seeds) |
| `knowledge/questions/` | open research questions H001–H013 (plus pipeline question P001) and their next steps |
| `knowledge/literature.md` | literature ledger (motivation, not evidence) |
| `docs/` | [PIPELINE](docs/PIPELINE.md) · [SUBSTRATE](docs/SUBSTRATE.md) · [CLAIMS](docs/CLAIMS.md) · [MIGRATION-v2](docs/MIGRATION-v2.md) |
| `experiments/` | v1 instruments and protocols; still executed by the `L*` claims |
| `dossiers/`, `reviews/`, `runs/` | v1 long-form science and records (historical) |
| `sources/` | pinned Anjo source snapshots (byte-checked by `mind doctor`) |
| `archive/v1/` | the v1 governance layer, superseded |

## Relationship to Anjo

MIND is Anjo's dedicated research arm and is scientifically independent of it. Its results may argue against Anjo's
designs, and nothing transfers to the Anjo product without separate engineering, safety and release approval. No
claim here concerns phenomenal experience (L3). See [AGENTS.md](AGENTS.md).
