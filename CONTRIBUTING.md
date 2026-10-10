# Contributing to MIND

Every contribution type below plugs into the shared substrate, so it is evaluated against everything that came
before, and everything that comes after is evaluated against it. Workflow: [GO.md](GO.md). Rules:
[AGENTS.md](AGENTS.md).

| Contribution | You add | It automatically… | Accepted when |
|---|---|---|---|
| **Claim** | `knowledge/claims/<ID>_<slug>.py` | joins the knowledge graph; is re-run by every future `mind check`; feeds the frontier | committed (sealed), evaluated with `--record` and `--heldout --record`, records committed, whatever the verdict |
| **Organ** | `mind/organs/<name>.py` + registry entry | is lesionable by every operator; enters the atlas; every claim re-evaluates against it | K01/K02 still hold (it replays), `mind check` has no BROKEN, plus at least one claim about what it does |
| **World** | `mind/worlds/<name>.py` with ≥ 1 held-out variant | every organism config and rival can run in it; the atlas gains its competencies | private info never reaches agents (add a test), plus at least one positive-control claim |
| **Rival** | entry in `mind/rivals/__init__.py` | is run against every claim asserting superiority of a mechanism it challenges; may demote them | uses the shared learner where a learner is involved (keep K03 meaningful) |
| **Lesion operator / probe** | kernel modifier or Check helper | becomes available to every claim | covered by `tests/` and K01 (it replays) |
| **Replication** | records from your environment (`--by <you>`) | lifts claims to REPLICATED | records from a fresh clone, committed unmodified |
| **Question** | `knowledge/questions/<ID>.md` with `next:` | appears on the frontier | states the strongest rival and what would answer it |
| **Literature** | an entry in `knowledge/literature.md` | can be cited by claims and questions | states the depth actually read |

## Code rules

* Python standard library only. Must run on Python ≥ 3.9 and in seconds to minutes on a laptop.
* Organs and worlds are deterministic given their seeds. No clock, no I/O, no order-dependent iteration of string
  sets (see [docs/SUBSTRATE.md](docs/SUBSTRATE.md)).
* Never re-implement what exists. Import it, even from `experiments/instruments` (see `mind/legacy.py`).
* Tests in `tests/` for every engine or kernel change: `python -m unittest discover -s tests`.

## Merging without an integrator

Claims, records, organs, worlds and questions are one file each, so parallel PRs rarely touch the same file. The
only shared files are the small registries (`mind/*/__init__.py`) and `STATUS.md`. If `STATUS.md` conflicts,
regenerate it with `python -m mind status --write`. A PR is mergeable when `python -m mind check`,
`python -m unittest discover -s tests` and `python -m mind doctor` all pass on the merged tree.

Approval of a PR is not a scientific verdict. Scientific standing comes only from the computed ladder.
