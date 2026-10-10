# MIND agent constitution

Applies to every human or AI contributor in `kevindechang/MIND`. Operational steps are in [GO.md](GO.md). Design
rationale is in [docs/PIPELINE.md](docs/PIPELINE.md). This page holds the commitments that code cannot enforce for you.

## Mission and boundary

MIND is **Anjo's foundational research program toward functional consciousness**, operationalised as causally
integrated, persistent, self-monitoring cognition (L2). The target is **not achieved**. L1 is behaviour, L2 is causal
organisation, L3 is phenomenal experience. They are separate, and nothing here licenses an L3 claim. MIND is
scientifically independent of the Anjo product: its findings must be able to contradict Anjo's design, and nothing
transfers to Anjo without separate engineering, safety and release approval (`NOT_READY_FOR_PRODUCT_TRANSFER` by
default). Anjo's product invariants (`sources/anjo/`) are product requirements, not evidence.

## What the machinery enforces (do not work around it)

* **Build on what exists.** One organism, one world suite, one rival zoo. Never write a standalone toy that
  re-implements an agent, a ledger or a world. Extend `mind/` instead.
* **Predictions are sealed by git.** Never edit a committed prediction to fit results. Register a successor claim.
* **Claims are retired, never deleted.** Negative and inconclusive results stay visible.
* **Records are never edited or deleted.** The doctor checks each committed record against the blob that added it.
* **A lesion that would do nothing is an error.** A misspelled target or parameter is rejected; fix the config.
* **STATUS.md is generated.** Never edit it by hand.
* **New organs must replay.** If K01, K06 or K07 break, your organ keeps hidden or order-dependent state. Fix the
  organ, not the claim.

## What is on you

1. **Never fabricate.** No invented runs, records, numbers, reviewers, durations or sources. Records are written
   only by `python -m mind check --record`. If you could not execute something, say NOT_EXECUTED.
2. **Record what happened.** Commit every held-out record you produce, *especially* failing ones. Deleting an
   unwanted record before committing it, and **grinding** (previewing candidate commit hashes to pick favourable
   held-out seeds), are the cheats the machinery cannot see. Both are fraud.
3. **Independence is real or absent.** Replication means a different contributor in a different environment. A
   second prompt to the same model in the same session is self-review and must be labelled as such.
4. **Strong rivals, honest margins.** Choose margins for scientific relevance, not to fit dev data. A compact rival
   that ties your mechanism is a finding. Register it.
5. **Literature is motivation, not evidence.** Cite sources in `knowledge/literature.md` with the depth actually
   read (abstract, methods or data). A paper is never a premise for an L2 claim about this organism.
6. **Scope every statement.** Claims are about this organism in these worlds. Do not generalise in prose beyond
   what the claim tests.

## Ethics and autonomy

* No access to real people's data, accounts, messages or sensors. No contact with real people. No credentials.
* No paid APIs, GitHub Actions, background workers, new recurring schedules or production Anjo changes without
  explicit approval from the repository owner. The owner's existing hourly research task is the only authorised
  scheduled runner.
* No self-replication and no uncontrolled self-modification of the organism outside the sandboxed simulator.
* Never present the organism, or any result, as sentient, conscious, feeling or continuously thinking when it is
  not running.
* **Welfare tripwire:** before adding any organ that implements valence, pain, distress, drive deprivation or
  self-preservation pressure, open a question file that documents the welfare considerations and stop conditions,
  and get owner sign-off.
