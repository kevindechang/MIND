# The MIND v2 research pipeline: how every contribution builds on the last

**Status:** adopted with the v2 migration (branch `pipeline/v2-compounding`). Governs how research is done
in this repository. The v1 governance it replaces is preserved in [archive/v1](../archive/v1/README.md).

## 1. Why v1 did not compound

v1 was rigorous in intent and honest in reporting, but its *structure* prevented accumulation:

| Symptom (observed at migration, 2026-10-10) | Cause |
|---|---|
| E100 Days 0–7 were eight separate scripts; none imported another or any shared module. Each re-defined its own SQLite schema, worker loop and decision rule. PR #16 showed that merging the days yields **contradictory policies on one ledger** (restoration and dependency scope disagree). | No shared substrate. Nothing persisted between experiments, so nothing could build on anything. |
| Every "mechanism" was a 5–20-line hand-written if/else; every lesion emptied the table that rule read; several "rivals" were AST-identical to the mechanism (Days 4, 5). PASS meant "the code does what it was written to do". | Nothing learned and nothing was measured against a hidden environment, so every effect was by construction. |
| ~19,300 words of Markdown against ~2,200 lines of Python across the ten open PRs; status restated by hand in ~15 files; commit history dominated by "remove stale next-action text". | Knowledge lived in prose. Every contribution had to re-edit the prose, and the prose drifted. |
| "0 accepted contributions" after five iterations; ten PRs waiting on one integrator to serialise `research-state.md`. | Acceptance was a manual verdict with a bar no available infrastructure could clear, and state was a single hand-written file. |
| E001 v0.1 → v0.4 produced four ever-better oracles but no agent that used them. | Instruments were endpoints rather than parts of a system. |

None of this was for lack of care: the rules (strong rivals, preregistration, L1/L2/L3 separation, no
by-construction claims, transitive invalidation) were right. They were just written down instead of built in.

## 2. Design principles

1. **One organism.** Every experiment lesions *the same* persistent, learning agent. A contribution changes
   one organ and inherits everything else.
2. **Knowledge is executable.** A claim is a file whose test is re-run forever. If later work breaks it, it
   turns BROKEN by itself; if its premise falls, its dependents turn STALE by themselves.
3. **Rules are mechanisms, not prose, wherever a mechanism exists.** Held-out seeds are fixed by the
   registering commit, and only the first held-out run counts. Deleted claims, deleted records and predictions
   amended after confirmation are rejected by the doctor. Strong rivals are applied automatically. L3 claims are
   rejected by the schema. What cannot be mechanised is stated once, in [AGENTS.md](../AGENTS.md).
4. **Status is computed.** [STATUS.md](../STATUS.md) is generated from claims, records and git. No one edits status; no
   integrator serialises it; a merge conflict in it is resolved by regenerating it.
5. **Negative results are first-class and cheap.** REFUTED and INCONCLUSIVE never fail the build. Only a
   regression (BROKEN) or a crash (ERROR) does.
6. **The frontier is derived.** What to do next is computed from the state of the knowledge itself, not from a
   hand-curated queue.

## 3. The machine

```text
   contributions                      shared substrate                         knowledge
 ┌──────────────┐   ┌────────────────────────────────────────────┐   ┌──────────────────────────┐
 │ organ        │──▶│ organism kernel: one event-sourced agent   │   │ claims (executable,      │
 │ world        │──▶│  ledger · workspace · organs · lesions     │──▶│  sealed predictions)     │
 │ rival        │──▶│ world suite · rival zoo · runner · stats   │   │ records (append-only)    │
 │ claim        │───┼────────────────────────────────────────────┼──▶│ questions · literature   │
 │ replication  │───┘                                            │   └────────────┬─────────────┘
 └──────▲───────┘                                                │                │ python -m mind status
        │            STATUS.md: states · levels · atlas · ───────┴────────────────┘
        └─────────── FRONTIER (broken → stale → inconclusive → rivals → questions → replication)
```

* **Substrate** ([docs/SUBSTRATE.md](SUBSTRATE.md)). `mind/kernel.py` runs a global-workspace cognitive cycle: organs
  propose contents, a capacity-limited workspace selects and broadcasts them, organs learn, the policy acts.
  The only durable state is a hash-chained ledger; organ state is a deterministic fold over it, and
  `Organism.restore` *verifies the chain and re-derives every logged decision*. So a new organ that keeps hidden
  state breaks K01 in every world and under every lesion. One whose behaviour depends on hash order breaks K06,
  which replays in fresh processes under different hash seeds. Exactly-once acting after a crash is K07.
* **Lesions are operators**, not toys: `-memory`, `cut:memory>policy`, `freeze:self_model`,
  `shuffle:memory` (sham), `capacity=inf`, `@150:-goals` (acute lesion mid-life). The v1 audits' taxonomy
  (reconstruction vs access vs information knockout; acute vs recovered) maps onto these operators plus world
  variants that remove the information itself.
* **Worlds** share one observation/action protocol and keep the agent-visible observation strictly separate
  from the scorer's private `info`. Each has dev and held-out variants. The E001 three-node world is
  `workshop`, and its exact optimum is the **legacy v0.4 dynamic program, imported unchanged** (claim K04 checks
  the port by simulation).
* **Rivals** accumulate in a zoo. The transcript rivals use the *same* learner as the organism (claim K03 checks
  this action for action), so a difference can only come from representation. When a claim asserts that a
  mechanism is superior, every applicable rival is run automatically; registering a stronger rival can demote old
  claims, and that counts as a contribution.
* **Claims** ([docs/CLAIMS.md](CLAIMS.md)) live in `knowledge/claims/`, one file each, with premises
  (`depends_on`) and lineage (`extends`). The prediction is hashed; prose is free.

## 4. The evidence ladder (computed, never asserted)

| Rung | Meaning | How it is earned |
|---|---|---|
| PROPOSED | registered, untested | the file exists |
| OBSERVED | holds once | any passing evaluation |
| ROBUST | holds at declared strength | ≥ declared seeds; the CI clears the margin (exhaustive for exact checks) |
| RIVAL-TESTED | beats every standing rival | automatic rival panel, only for claims asserting mechanism superiority |
| PREREGISTERED | holds on sealed data | passes on held-out seeds derived from the **git commit that registered the prediction** |
| REPLICATED | independently reproduced | records from ≥ 2 contributors **and** ≥ 2 environments |

**Commit-sealed held-out seeds.** A claim's held-out seeds are a hash of the commit that first contains its
current prediction (searched by claim id, so renames do not move it). The rules that make this work:

* **Only the first recorded held-out evaluation decides PREREGISTERED.** Once sealed seeds have been seen,
  re-running them after a code change proves nothing about prediction. A failed first confirmation stays
  attached to the claim forever.
* **Held-out runs are always recorded**, and records are append-only (the doctor rejects deletions).
* **A prediction never changes after a held-out run.** The doctor rejects it. Register a successor claim; its new
  id and new commit give it new seeds.
* **Held-out evidence dominates dev evidence**, so re-running dev seeds can never overwrite a confirmation.
* **Merge with merge commits.** Squash or rebase merges rewrite the sealing commits. The doctor detects held-out
  records whose seal has vanished from history.

What this does *not* stop is deliberate seed **grinding** (v2 review, finding 2a). A contributor who controls the
registering commit can compute candidate commit hashes offline and commit only one whose seeds favour them. The
pipeline cannot see that. It is forbidden in [AGENTS.md](../AGENTS.md), and preventing it needs randomness from
outside the contributor's control (a public beacon, or seeds drawn at merge by someone else). That is an open item
on the frontier.

States: HOLDS · REFUTED (failed, never held: knowledge) · BROKEN (held, now fails on identical seeds: a
regression) · INCONCLUSIVE (the interval straddles the margin; *not* a negative result) · STALE (a premise
failed) · UNTESTED · ERROR · RETIRED (withdrawn with a reason, never deleted).

This replaces v1's single SCIENTIFIC_ACCEPTED bit. A contribution earns visible standing at each rung instead of
waiting for a verdict nobody could give.

## 5. Functional consciousness, operationally

The program's target, *functional consciousness*, is operationalised here as **causally integrated, persistent,
self-monitoring cognition** (v1's L2), and made measurable at three levels:

1. **Persistence of an individual.** The organism's whole learned self survives real process death
   (K01, K02, K06), never acting twice after a crash (K07).
2. **Selective global availability.** A capacity-limited workspace broadcasts few contents to all functions.
   Whether that helps is an empirical question with a conditional answer so far (C005 holds under distractor
   load; C006, neutrality without load, is inconclusive).
3. **Integration, not modularity.** The integration atlas (`python -m mind atlas`) estimates the lesion effect
   of every organ on every non-redundant competency metric in every world. Calibration is scored on the agent's
   own events, and family-wise error is Holm-controlled. A modular system shows only on-diagonal effects. The
   organism shows cross-function effects (memory and goals improve the self-model's calibration) and degeneracy
   (memory and goals back each other up, C004). Claim C016 asserts this and is re-tested every time the suite
   grows. Its predecessor C014 was retired after review because it counted cells instead of organs and had no
   multiplicity control.

These are descriptions of causal organisation, **not** consciousness scores. Phenomenal experience (L3) is not
an admissible scope for any claim (the doctor rejects it). A system can satisfy every L2 description and
remain silent on L3.

## 6. The contribution loop

```text
frontier item ──▶ branch ──▶ explore on dev seeds (free) ──▶ write claim(s) ──▶ COMMIT (= seal)
     ▲                                                                              │
     │                         python -m mind check --record   (dev, full strength) ◀┘
     │                         python -m mind check --heldout --record (sealed seeds)
     │                         python -m mind check  (exit 0: nothing BROKEN anywhere)
     └──── STATUS.md regenerated ◀── PR with the check output; merge without an integrator bottleneck
```

Parallel contributors rarely conflict: claims and records are one file each, and organs, worlds and rivals are
one module each. The registry `__init__.py` files and STATUS.md are the only shared files, and the latter is
regenerated rather than merged.

## 7. What is mechanical and what is not

| Rule | Enforcement |
|---|---|
| Held-out data cannot be re-used to rescue a prediction | first-held-out rule; held-out runs always recorded; held-out dominates dev |
| Predictions cannot be edited after confirmation | doctor: amendment after a held-out run is a problem; check helpers are hashed |
| Claims and records cannot be silently deleted | doctor scans git history for deleted claim and record files |
| Seals survive merges | doctor: every held-out seal must be in history (merge commits only) |
| Strong rivals cannot be dodged | automatic rival panel; a new rival re-tests old claims |
| Failed premises propagate | transitive STALE |
| New organs cannot hide state or depend on hash order | K01 (in-process), K06 (fresh processes, 3 hash seeds), K07 (exactly-once) |
| Nonsignificance is not equivalence | equivalence HOLDS only if the whole conservative CI is inside the margin |
| Forecasters are compared on the same events | `calib_gain` (validated by K08) |
| No L3 claims | schema `scope ∈ {instrument, L1, L2}` |
| Result evidence tracks the code that produced it | records carry a fingerprint of all result-affecting code |
| **Not mechanical:** seed grinding, deleting a held-out failure *before* committing it, real independence for replication, sensible margins, ethics | social: [AGENTS.md](../AGENTS.md), review |

## 8. Known limits (to be attacked, not hidden)

* The organism is small: linear TD over pairwise conjunctions, logistic self-model, finite episodic memory.
  It is a *substrate for causal questions*, not a candidate mind. Every claim is scoped to it.
* Worlds are toys. The held-out variants test generalisation across seeds and parameters, not across domains (H011).
* Dev exploration then held-out confirmation is a train/test discipline, not a full Registered Report.
  Margins chosen after seeing dev data inflate apparent success. The first held-out run demoted 4 of 15 organism
  claims to INCONCLUSIVE, which is the ladder doing its job.
* Intervals: the wider of the percentile bootstrap and Student-t intervals measured about 95% coverage on normal
  data and 91% on skewed data at n = 16. There is no multiplicity correction *across* claims; the atlas corrects
  within its own family.
* The first adversarial review ([reviews/2026-10-10-v2-pipeline-adversarial-review.md](../reviews/2026-10-10-v2-pipeline-adversarial-review.md))
  found one critical and seven important defects, all now fixed, retired or documented. It was a separate
  invocation of the same model, not independent replication.
* Replication needs a second contributor in a second environment. Until then the top rung is empty.
* No LLM organ yet. The design admits one once the kernel gains a small extension (per-organ notes inside the tick
  event). The organ would log each model output there and read it back on replay, so continuity (K01) would still hold
  for a nondeterministic organ. Any paid model use needs cost and data approval first.
