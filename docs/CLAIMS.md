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
  exact facts (e.g. the ported v1 results L04–L07), invariants (K01–K05) and composite estimands (the C004
  degeneracy interaction, the C014 atlas).

Arms are organism configurations (`organism -memory cut:goals>policy`, see [SUBSTRATE.md](SUBSTRATE.md)) or
`rival:<name>`.

## The prediction lock and the seal

`prediction = {id, kind, scope, test spec}` and `prediction_hash = sha256(canonical(prediction))[:16]`. Title,
statement, rationale and lineage are prose and may be improved at any time without consequence.

The **seal** is the earliest commit whose version of the file carries the current prediction hash.
**Held-out seeds** are `sample(range(10_000, 10_000_000), n)` drawn from a hash of `seal | id | prediction_hash`. You
cannot know them before committing the prediction, so you cannot tune on them. If you change the prediction, you
create a new registration with a new seal and new seeds. That is allowed and its history stays visible, but never do it
to rescue a failed confirmation. Register a successor claim instead.

## Running

```text
python -m mind check                  # every claim at full strength on dev seeds (exit 1 only on BROKEN/ERROR)
python -m mind check C005 --quick     # 4 dev seeds, a draft, never recorded
python -m mind check C005 --record    # full strength; writes knowledge/records/<time>-<env>-full.json
python -m mind check C005 --heldout --record   # sealed seeds; requires the claim to be committed
python -m mind status --write         # regenerate STATUS.md
```

Records are append-only, one file per run, and carry the contributor (`--by`), an environment fingerprint, the git
HEAD, and the fingerprint of all result-affecting code. Commit them with your contribution.

## States

| State | Meaning | Build |
|---|---|---|
| HOLDS | the latest strongest evaluation holds | ✓ |
| REFUTED | fails and has never held on these seeds: a negative result, kept as knowledge | ✓ |
| INCONCLUSIVE | the interval straddles the margin: needs a sharper successor, not a verdict | ✓ |
| STALE | holds, but a premise is REFUTED/BROKEN/RETIRED/STALE/ERROR | ✓ |
| UNTESTED | never evaluated | ✓ |
| RETIRED | `retired="reason"`; kept forever | ✓ |
| BROKEN | held before and fails now **on the same seeds**: something changed the result | ✗ exit 1 |
| ERROR | the check crashed | ✗ exit 1 |

"Strongest" means held-out beats dev and dev beats quick. A failed sealed confirmation therefore cannot be
overwritten by re-running dev seeds. Holding on dev but failing on held-out is REFUTED with the note *did not
generalise*, not BROKEN.

## Levels

PROPOSED → OBSERVED → ROBUST → RIVAL-TESTED → PREREGISTERED → REPLICATED. Cumulative, computed by
`mind/knowledge.py`.

* **RIVAL-TESTED** applies only to `effect` claims with a non-empty `about` (they assert a mechanism is better).
  Every rival in the zoo that challenges one of those mechanisms in that world is run on the same seeds, and the claim's
  arm `a` must beat each reliably. Reference rivals (privileged oracles) are reported as a ceiling but not required.
  Beating a rival directly as arm `b` counts.
* **PREREGISTERED** needs a robust pass on the sealed held-out seeds of the current prediction (and a clean rival
  panel when one applies). Deterministic checks without seeds skip this rung.
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
use `~`. **No claim file has ever been deleted from git history.** Pinned Anjo sources are byte-unchanged. Links in the
living docs resolve.

## Good claims

* State the strongest simple rival in the docstring and make sure the zoo contains it.
* Put the margin where it matters scientifically, not where your dev data happens to land. The first held-out run
  demoted 4 of 15 organism claims whose margins were too close to their dev estimates.
* Prefer a pair of conditional claims (C005 with C006, C007 with C008) to one universal claim: necessity is a property of
  a mechanism in a world.
* A refuted or inconclusive claim that teaches something is a contribution. A claim that cannot fail is not.
