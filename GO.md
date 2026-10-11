# GO — what to do when told "go"

You are joining a compounding research program. Your job is to add **one** piece of knowledge that builds on
everything already here. Read [AGENTS.md](AGENTS.md) once. You do not need anything in `archive/`.

**Scheduled agents:** also follow [research session execution and recovery gates](docs/RESEARCH_SESSION_WORKFLOW.md). Verify Git-history checkout, executable tests and branch/PR capability *before* choosing a task. A design checkpoint is not a completed experiment. Distinguish the parent scientific question from the narrower claim actually measured. Check for overlapping branches and PRs to avoid duplicating unfinished work.

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

If you changed result code (anything in `RESULT_CODE`, listed in `mind/runner.py`), re-record before you hand off:
`python -m mind check --record` and `python -m mind check --heldout --record`. Otherwise every claim's standing above
ROBUST is suspended (`CURRENT_CODE_UNVERIFIED`).

Commit code, claims, records and STATUS.md, then open a PR. The description is the `mind check` output for your claims
plus one paragraph on what changed in the knowledge. No integrator needs to serialise anything. If STATUS.md
conflicts, regenerate it.

**Cannot execute code?** First classify and attempt bounded, legitimate recovery of the environment failure. You may add a *new*, nonduplicative, testable question (`knowledge/questions/`), literature entry (`knowledge/literature.md`), or prospective claim file only if it makes a substantive contribution with an explicit future falsifier and executable handoff. It remains UNTESTED until actually run; never substitute API-only inspection for git-history verification or invent test results. If the work already exists and no novel contribution is available, report `BLOCKED_NO_NEW_CONTRIBUTION` with the exact blocker rather than opening a duplicate PR.
