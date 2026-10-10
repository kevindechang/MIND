# Research work and acceptance index

**Repository migration note (2026-10-11):** Historical commit SHAs in records below are commits of `kevindechang/Founder-Library`, *not* the new MIND commit graph. [MIGRATION.md](MIGRATION.md) records the byte-identical source snapshot. This governance relocation creates no new substantive scientific attention or accepted science.

**Adoption baseline:** `4ec49fa45878ec33a4a07658fc418f535a5ee86f` on main before this governance change. Historical source versions below refer to that immutable repository snapshot; later amendments must cite their own version. This index does not certify the original claims.

Kinds: GOVERNANCE_CHANGE / EXPLORATORY_CHECKPOINT / RESEARCH_NOTE / INSTRUMENT_VALIDATION / AGENT_COMPARISON / SYNTHESIS. Scientific verdicts remain EXPLORATORY_CHECKPOINT / RESEARCH_NOTE / SCIENTIFIC_ACCEPTED / MAJOR_REVISION_REQUIRED; UNKNOWN means historical acceptance not established, NOT_APPLICABLE means governance. Kind and verdict are separate.

| Record | Kind | Decision / scientific status | Inspection and review provenance |
|---|---|---|---|
| [000](runs/2026-10-10-iteration-000.md) | GOVERNANCE_CHANGE | Program initialization; NOT_APPLICABLE | Historical initialization, not accepted contribution |
| [001](runs/2026-10-10-iteration-001.md) | RESEARCH_NOTE | D001 / acceptance UNKNOWN; G0 design | Primary-source/design report; no agent trial or independent acceptance established |
| [002](runs/2026-10-10-iteration-002.md) | INSTRUMENT_VALIDATION | D001 / acceptance UNKNOWN | Reported deterministic checks; no agent efficacy |
| [003](runs/2026-10-10-iteration-003.md) | INSTRUMENT_VALIDATION | D001 / acceptance UNKNOWN | Reported commitments/oracle checks; no agent trial |
| [004](runs/2026-10-10-iteration-004.md) | INSTRUMENT_VALIDATION | H005/H008 / MAJOR_REVISION_REQUIRED | [Referee audit](reviews/2026-10-10-iteration-004-scientific-rigor-audit.md); SELF-REVIEW_ONLY; preliminary calibration |
| [GOV-2026-10-10-compounding](docs/research-program/2026-10-10-compounding-research-system-design.md) | GOVERNANCE_CHANGE | D001 registration and workflow refinement; NOT_APPLICABLE | Implementation plan and [governance walkthrough](reviews/2026-10-10-compounding-governance-walkthrough.md); [independent governance review](reviews/2026-10-10-compounding-governance-review.md), not scientific peer review |

| [RN-D001-2026-10-11-001](runs/2026-10-11-research-note-D001-001.md) | RESEARCH_NOTE | D001 / RESEARCH_NOTE; E001 G0 still OPEN; NOT accepted | [v0.1 permitted-history oracle method](experiments/E001/E001-G0-permitted-history-oracle-v0.1.md); 16 local synthetic checks, S017 POMDP methods, SELF-REVIEW_ONLY; initial artifact commits `404b0b0`/`578adb5`; 1 prospective substantive W1 attention record |

| [IV-D001-2026-10-11-002](runs/2026-10-11-instrument-validation-D001-002.md) | INSTRUMENT_VALIDATION | D001 / EXPLORATORY_CHECKPOINT; E001 G0 still OPEN; NOT accepted | [v0.2 3-node version-space oracle method](experiments/E001/E001-G0-selective-probe-version-space-v0.2.md); instrument self-check + 14 new unit tests PASS on Python 3.9.6 stdlib, 10 legacy CausalWorkshop tests PASS, SELF-REVIEW_ONLY; prospective substantive W1 attention record (count → 2) |

| [IV-D001-2026-10-11-003](runs/2026-10-11-instrument-validation-D001-003.md) | INSTRUMENT_VALIDATION | D001 / EXPLORATORY_CHECKPOINT, SHORT_RUN; E001 G0 OPEN; NOT accepted | [v0.3 prior/censoring robustness](experiments/E001/E001-G0-prior-censoring-robustness-v0.3.md); 20 local deterministic checks using reconstructed compatibility fixture; SELF-REVIEW_ONLY; third prospective W1 substantive attention record (count → 3) |

| [IV-D001-2026-10-11-004](runs/2026-10-11-instrument-validation-D001-004.md) | INSTRUMENT_VALIDATION | D001 / EXPLORATORY_CHECKPOINT, SHORT_RUN; E001 G0 OPEN; NOT accepted | [v0.4 adaptive policy and closure nonidentification](experiments/E001/E001-G0-policy-value-identifiability-v0.4.md); byte-exact source/test blobs; 12 Python tests PASS, 128 seeded differential equalities; SELF-REVIEW_ONLY; fourth W1 execution-critical allocation exception; next W2–W4 opportunity required. |

## Identity and counters

Legacy `latest_verified_iteration: 004` stays a historical persistence ID, not a completed-science count. Future work artifacts use unique `runs/YYYY-MM-DD-<kind>-<decision-or-topic>-NNN.md` paths, checked for collision against live main. Do not reuse/overwrite an ID. Failed persistence creates a pending delta, not a canonical record or increment.

Prospective accepted-contribution count starts at **0 on adoption of this refinement**. No backfill of 001–003; their acceptance remains UNKNOWN until a documented audit. Count once per distinct contribution ID, after SCIENTIFIC_ACCEPTED, verified artifact/state publication and intact pivotal evidence. Repeated amendments or multiple files for the same contribution are not additional accepted contributions. Governance, checkpoints, instrument scaffolding and skipped runs do not qualify by themselves.

If accepted pivotal evidence later fails, preserve the original verdict/history but mark the contribution NEEDS_REASSESSMENT and remove it from the current valid accepted count until reaccepted. Keep milestone history so reaccepting the same contribution cannot retrigger an already completed eighth-contribution synthesis. Publication may honestly accept a null, negative, proof or critical synthesis; positive results are not privileged.

## Allocation and synthesis

A completed substantive work record (checkpoint, note, validation, comparison or scientific synthesis) counts for **attention allocation**, independent of scientific acceptance. Pure governance, superficial repetition and skipped invocations do not. In every four new completed substantive records, reserve at least one opportunity for a non-leading stream; document exceptions for safety or execution-critical dependencies. Historical 001–004 remain history and do not initialize prospective attention accounting.

Deep synthesis is due after each eight new distinct valid accepted contributions since the last milestone, or earlier for a major validated finding or pivotal dependency invalidation. An invalidation may warrant synthesis even with zero new acceptances. Do not trigger from the legacy 008 filename. Track milestone contribution IDs, not only a volatile total.

## Persistence and interruption

Read live main first. Commit artifacts/index/decisions before state; state then cites the immutable artifact commit. Read back final publication SHA externally or in a subsequent audit: no file can cite its own final commit hash. If interrupted, compare record IDs and artifacts to state, reconcile and finalize the pending handoff once; do not rerun or double-count. Normal Git fast-forward rejection or API SHA conflict requires rereading/reconciliation, never force-pushing.


## 2026-10-11 agent onboarding and source hierarchy (non-scientific governance)

`GO.md`, `TASKS.md`, `CURRENT.md`, `CONTRIBUTING.md` and `sources/README.md` establish a shared agent interface and source-provenance policy. Anjo's proposed Oct 2 product spec and the Oct 9 VERA research monograph were ingested as immutable source snapshots. This does not create a work record eligible for substantive scientific allocation or a SCIENTIFIC_ACCEPTED contribution. Prior experimental metrics, W1 allocation count 4 and accepted count 0 remain unchanged. See live `research-state.md` for the canonical next action.


## 2026-10-11 E100 Day 0 executable checkpoint (W2 substrate; NOT accepted science)

[E100 local observation](runs/2026-10-11-E100-day0-local-checkpoint.md): local Python 3.13.5 real SIGKILL (-9), fresh-process ledger-only action `inspect_signal`, wiped-ledger `NO_ACTION`, alternate-ledger `record_measurement`, 1 dedicated subprocess unittest PASS. Worker source/test Git blob hashes documented. This is a **local, deterministic finite-state instrument check**, no model trial, no independent reviewer, no integration proof, and not evidence of achieved functional consciousness. Prior 73/73 externally reported integrated tests were not rerun. **Accepted contributions stay 0, E001 G0 OPEN, D001 DEFER/CURRENT, E900 NOT STARTED.** The next eligible W2 substantive lesion study requires stronger mechanism distinction and preregistered action change. The checkpoint and priority-setting are not counted as SCIENTIFIC_ACCEPTED or gate advancement.
