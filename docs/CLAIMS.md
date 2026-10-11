# Claims: the unit of knowledge

A claim is one Python file in `knowledge/claims/` that defines `CLAIM = Claim(...)`. `python -m mind new C016 "title"`
scaffolds one. The file is the claim's whole public life. Its **test** is executed by `python -m mind check`. Its
**prediction** is hashed and sealed by git. Its **state and level** are computed from records. It is never deleted.

## Anatomy

```python
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C005",                       # letter + 2-4 digits; file name must start with "C005_"
    title="The workspace bottleneck helps under distractor load",
    statement="In vigil/crowded the 4-item workspace keeps more commitments than capacity=inf, by > 0.08.",
    kind="effect",                   # effect | equivalence | threshold | invariant | fact
    scope="L2",                      # instrument | L1 | L2   (L3 is rejected by the doctor)
    question="H003",                 # knowledge/questions/H003.md
    about=("workspace",),            # mechanisms whose SUPERIORITY is asserted: selects the rival panel
    depends_on=(),                   # premises: if one fails, this claim turns STALE
    extends=("L03",),                # lineage: claims or repo paths this builds on (graph only)
    test=Compare(world="vigil", a="organism", b="rival:flat", metric="kept",
                 direction=">", margin=0.08, seeds=16, variant="crowded"),
    by="your name", created="2026-10-10", rationale="why it matters",
)
```

**Tests.**

* `Compare(world, a, b, metric, direction, margin, seeds, episodes=None, variant="dev")`: paired over independent
  lifetimes on mean(a − b). `'>'` means a exceeds b by more than the margin. `'<'` means a falls below b by more than the margin. `'~'` means equivalence:
  the whole 95% bootstrap CI must lie inside ±margin. *Nonsignificance is never equivalence*: a CI that straddles the
  band is INCONCLUSIVE.
* `Threshold(world, arm, metric, op, value, seeds, ...)`: the mean clears a bound (`>=` / `<=`) with its whole CI.
* `Check(fn, seeds=0)`: custom logic. `fn(ctx)` returns `{"verdict": "HOLDS"|"FAILS"|"INCONCLUSIVE",
  "robust": bool, "summary": str, ...}`. `ctx.lab` runs lifetimes (cached, parallel), `ctx.seeds` holds dev or sealed
  held-out seeds, and `ctx.mode` is the run mode. The function's **source** is part of the prediction hash. Use it for
  exact facts (e.g. the ported v1 results L04–L07), invariants (K01–K08) and composite estimands (the C004
  degeneracy interaction, the C016 atlas). Since scheme 2 the **whole claim file's code** (helpers, constants,
  imports, but not its docstring or the `CLAIM = ...` block) is part of the prediction. Editing a helper is
  editing the prediction.

Arms are organism configurations (`organism -memory cut:goals>policy`, see [SUBSTRATE.md](SUBSTRATE.md)) or
`rival:<name>`.

## The prediction lock and the seal

`prediction = {id, kind, scope, test spec}`, plus, for `Check` claims, the hash of the file's code without its
docstring and `CLAIM` block (scheme 2). `prediction_hash = sha256(canonical(prediction))[:16]`. Title, statement,
rationale, lineage and `retired` are prose and may be improved at any time without consequence. Records store the
scheme they were made under, so records from before a scheme change still match an unchanged prediction.

The **seal** is the earliest commit containing a file for this claim id (searched by id, so renames do not move
it) that carries the current prediction hash. **Held-out seeds** are `sample(range(10_000, 10_000_000), n)` drawn
from a hash of `seal | id | prediction_hash`. They are fixed by the registering commit. Rules:

* **Only the first recorded held-out evaluation decides PREREGISTERED.** A failure stays attached to the claim; later
  re-runs update its state but never its preregistration.
* **Never change a prediction after a held-out run.** The doctor rejects it. Register a successor claim with a new
  id; its new commit gives it new seeds.
* **Merge with merge commits.** Squash or rebase merges rewrite sealing commits, and the doctor rejects held-out
  records whose seal has left history.
* **Do not grind.** You *can* compute a commit's hash before creating it, and so preview its seeds. Choosing a
  commit for its seeds is fraud that the tool cannot detect (see [AGENTS.md](../AGENTS.md)).

## Running

```text
python -m mind check                  # every claim at full strength on dev seeds (exit 1 only on BROKEN/ERROR)
python -m mind check C005 --quick     # 4 dev seeds, a draft, never recorded
python -m mind check C005 --record    # full strength; writes knowledge/records/<time>-<env>-full.json
python -m mind check C005 --heldout           # sealed seeds; requires the claim to be committed; always recorded
python -m mind status --write         # regenerate STATUS.md
```

Records are append-only, one file per run, and carry the contributor (`--by`), an environment fingerprint, the git
HEAD, and the fingerprint of all result-affecting code. Commit them with your contribution. The doctor compares every
committed record byte for byte with the blob that added it. Deleting one, or editing it in a later commit, a merge or
the working tree, is a problem it reports.

## States

| State | Meaning | Build |
|---|---|---|
| HOLDS | the latest run on every seed set (dev, sealed held-out) holds | ✓ |
| REFUTED | fails and has never held on these seeds: a negative result, kept as knowledge | ✓ |
| INCONCLUSIVE | the interval straddles the margin: needs a sharper successor, not a verdict | ✓ |
| STALE | holds, but a premise is REFUTED/BROKEN/RETIRED/STALE/ERROR | ✓ |
| UNTESTED | never evaluated | ✓ |
| RETIRED | `retired="reason"`; kept forever | ✓ |
| BROKEN | held before and fails now **on the same seeds**: something changed the result | ✗ exit 1 |
| ERROR | the check crashed | ✗ exit 1 |

Each seed set speaks through its latest run, and the most conservative of those runs decides the state. So a failed
sealed confirmation cannot be overwritten by re-running dev seeds, and an old held-out success cannot mask a dev
regression that `mind check` finds in the current code. A claim that holds on one seed set and is inconclusive on
another is INCONCLUSIVE, noted as *mixed evidence*. Quick drafts count only when nothing else exists. Holding on dev
but failing on held-out is REFUTED with the note *did not generalise*, not BROKEN.

## Levels

PROPOSED → OBSERVED → ROBUST → RIVAL-TESTED → PREREGISTERED → REPLICATED. Cumulative, computed by
`mind/knowledge.py`.

* **RIVAL-TESTED** applies only to `effect` claims with a non-empty `about` (they assert a mechanism is better).
  Every rival in the zoo that challenges one of those mechanisms in that world is run on the same seeds, and the claim's
  arm `a` must beat each reliably. Reference rivals (privileged oracles) are reported as a ceiling but not required.
  Beating a rival directly as arm `b` counts.
  * The rung is judged on the *latest* run on every seed set, against *today's* zoo.
  * A newer run that does not beat a rival revokes it, and so does a rival added since the latest run. The ladder is
    cumulative, so everything above the rung is revoked too.
  * Re-running the claim earns it back. The frontier asks for that re-run.
* **PREREGISTERED** needs the *first* recorded evaluation on the sealed held-out seeds of the current prediction to
  be a robust pass (with a clean rival panel when one applies). Deterministic checks without seeds skip this rung.
* **Current standing.** RIVAL-TESTED and above need *recorded* evidence from the current result code on every seed
  set.
  * The code fingerprint covers every file in `RESULT_CODE` (`mind/runner.py`), comments and docstrings included;
    Markdown never counts.
  * After any change to that code, those levels are suspended until `mind check --record` and `--heldout --record`
    re-record the claim. STATUS marks the claim `CURRENT_CODE_UNVERIFIED`, and a priority-1 refresh item appears on
    the frontier.
  * Standing returns only if the new runs hold and beat the panel. An unrecorded run can revoke standing but never
    restore it.
  * The original sealed confirmation stays historical fact. Re-running exposed held-out seeds never counts as a new
    preregistration.
* **REPLICATED** needs robust passing records from at least two distinct contributors **and** two distinct
  environments.

## Premises vs lineage

`depends_on` is logical: "this result is only meaningful if that one holds" (e.g. every regret number depends on
K04, the world matching the legacy optimum). Failure propagates transitively as STALE. `extends` is intellectual
lineage, drawn in the knowledge graph only. Use premises sparingly and honestly. A dependency cycle is a doctor
error (Anjo invariant I5: no self-evidence).

## Doctor rules (`python -m mind doctor`)

Claim ids are unique and match file names. Kinds and scopes are valid (no L3). Premises exist and are acyclic.
Lineage points to a claim or a real path. Every test names a real world, variant, metric and arm. Equivalence claims
use `~`. **No claim file and no record file has ever been deleted from git history. No prediction has changed
after a held-out evaluation. Every held-out seal is still in history.** Pinned Anjo sources are byte-unchanged.
Links in the living docs resolve.

## Good claims

* State the strongest simple rival in the docstring and make sure the zoo contains it.
* Put the margin where it matters scientifically, not where your dev data happens to land. The first held-out run
  demoted 4 of 15 organism claims whose margins were too close to their dev estimates.
* Prefer a pair of conditional claims (C002 with C003, C005 with C006) to one universal claim: necessity is a property of
  a mechanism in a world.
* Compare forecasters on the **same events** (`calib_gain`), never two agents' Brier scores on their own action
  streams: behaviour then masquerades as calibration (C007/C008 were retired for exactly this).
  `calib_gain_alert` is the same comparison against the announcement-updated table.
* Count what the statement says. C014 said "organs" and counted cells (retired).
* A refuted or inconclusive claim that teaches something is a contribution. A claim that cannot fail is not.
