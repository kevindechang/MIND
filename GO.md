# GO — what to do when told "go"

You are joining a compounding research program. Your job is to add **one** piece of knowledge that builds on
everything already here. Read [AGENTS.md](AGENTS.md) once. You do not need anything in `archive/`.

## 1. Orient (minutes, not hours)

```bash
git pull
python -m mind doctor            # repository integrity
python -m mind status            # every claim's computed state
```

Then open [STATUS.md](STATUS.md). Its **Frontier** section, at the top, is your menu, computed from the knowledge
itself: broken claims, then stale ones, inconclusive ones, rivals to beat, open questions, and replications.

## 2. Pick one item and avoid collisions

Take the highest frontier item you can complete. Check open PRs and `contrib/*` branches for the same claim ids,
organ or world. Then branch: `git checkout -b contrib/<item>-<slug>`.

## 3. Build on what exists

| You want to… | Do this |
|---|---|
| test an idea | `python -m mind new C016 "title"`, then fill in the test ([docs/CLAIMS.md](docs/CLAIMS.md)) |
| add a mechanism | add an organ in `mind/organs/` ([docs/SUBSTRATE.md](docs/SUBSTRATE.md)) |
| challenge a mechanism | add a rival in `mind/rivals/`; it re-tests every relevant claim |
| make a question testable | add a world (with a held-out variant) in `mind/worlds/` |
| strengthen evidence | replicate: run the checks on a fresh clone with `--by <you>` |

Explore freely on dev seeds (`python -m mind run …`, `python -m mind check C016 --quick`). Exploration is not evidence.

## 4. Register, then confirm

```bash
git add knowledge/claims/C016_*.py && git commit -m "Register C016"   # this commit seals the prediction
python -m mind check C016 --record                 # full strength, dev seeds
python -m mind check C016 --heldout --record       # sealed seeds nobody could tune on
```

Report what happens. REFUTED and INCONCLUSIVE are contributions. Never edit the prediction afterwards; register a
successor instead.

## 5. Prove you broke nothing, then hand off

```bash
python -m mind check                       # exit 0 = nothing BROKEN or ERROR anywhere
python -m unittest discover -s tests
python -m mind doctor
python -m mind status --write              # regenerate STATUS.md (never edit it by hand)
```

Commit code, claims, records and STATUS.md, then open a PR. The description is the `mind check` output for your claims
plus one paragraph on what changed in the knowledge. No integrator needs to serialise anything. If STATUS.md
conflicts, regenerate it.

**Cannot execute code?** You can still add a question (`knowledge/questions/`), a literature entry
(`knowledge/literature.md`) or a claim file. It will show as UNTESTED until someone runs it. Say so in your PR.
