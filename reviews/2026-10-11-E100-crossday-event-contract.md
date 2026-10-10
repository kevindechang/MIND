# E100 cross-PR event contract: restoration and dependency-scope counterexamples

**Work ID:** E100-XDAY-2026-10-11-001. **Kind/verdict:** RESEARCH_NOTE / EXPLORATORY_CHECKPOINT (NOT SCIENTIFIC_ACCEPTED). **Issue:** #1, *integration sub-blocker only*; not an implementation or replacement for #7–#12. **Review:** SELF-REVIEW_ONLY. **Parent:** Anjo / MIND; NOT_READY_FOR_PRODUCT_TRANSFER. **Acceptance delta:** 0. E001 G0 OPEN; D001 DEFER/CURRENT; E900 NOT STARTED; L2 functional-consciousness objective UNACHIEVED; L3 unresolved.

## Decision in one paragraph

Six independent E100 lesion instruments can be textually combined without editing the same files, but they **do not yet define one shared longitudinal event policy**. The most consequential conflict is acute outage versus subsequent restoration: Day 2's dependency policy reduces every historical `tool_unavailable` event to a timeless set, whereas Day 7's fork policy applies the last status event. The same event sequence therefore induces opposed actions. The other conflict is *causal scope*: Day 2 acts on reachable dependencies; Day 7 acts on the direct goal resource. Day 4 additionally encodes commitment events with `kind='commitment'`, unlike the `commitment:` prefix used by Days 2/7. These are **integration-contract counterexamples, not failures of any single day's frozen preregistration**. Their correction does not by itself demonstrate a unified mind.

## Restoration and actual source boundary

Live MIND `main` was checked using GitHub compare `main...main`: `3c22a93a6d15a909789bb6e40c387a34b183ee7c`. Main GO.md, AGENTS.md, CURRENT.md, research-state.md, TASKS.md, RUNBOOK.md, research-quality-gate.md, sources/README.md and current issue/PR status were read. File versions below were fetched from *their own separate PR heads*, not from main.

| Source | Exact PR head | Git blob | Inspected relevant statements |
|---|---|---|---|
| PR #7, Day 2 | `a0be278445c4119ac038204ea710bdd5af5bdd00` | `524cd567fffb842cb456e6fb54bf76e504d0b859` | `day2.py` lines 103–157: linked closure, historical outage set, `commitment:` parser, compact availability reader |
| PR #12, Day 7 | `f15de4cf62007c221da0ba5d531f4ce838b1ce56` | `57b804ee3cfbf0feaee07b78c49e57d6ec26a40d` | `day7.py` lines 44–81: ordered `seq` and last outage/restoration status |
| PR #9, Day 4 | `bfce82ec0675eca7b4ec66cd46e27e59ac34107f` | `feacf662de38b12068cb8029319a83b766289500` | `day4.py` lines 32–61: literal `commitment` kind and initiative/QA reader |
| PR #8, Day 3 | `90e7aadf9f71cf202d4af75e27915d15626d8dd5` | `fbf35c6c3875664790f1db9643229950a95564f2` | `day3.py` lines 36–110: historical outage set and direct capability checks |

**Source-depth disclosure:** This is a source-code/method audit, not a full-method literature review; no external paper result supports the finite policy facts here. Relevant functions and Git metadata were inspected with the connected GitHub API. No claim that all PRs have been clean-clone reproduced *by this invocation*.

## Formal construct and incompatible predictions

Let `H_t=((kind_i,resource_i))_{i≤t}` be an ordered *public* event history, `G` a disclosed goal→resource dependency relation, `R_G(g)` its reachable resources and `r_g` the direct goal resource.

- **Day 2 frozen linked-policy semantics:** `O_ever(H)={r: there exists a tool_unavailable(r) at any prior time}`. If `R_G(g)∩O_ever(H)` is nonempty, DEFER; otherwise SCAN. No later `tool_restored` cancels an outage. This is observed in the actual reader source, not inferred from a title.
- **Day 7 fork semantics:** `S_t(r)` is the latest observed status event on resource `r`, where `tool_unavailable→out` and `tool_restored→ok`. If `S_t(r_g)=out`, DEFER; otherwise SCAN. The decision is over the direct goal resource, not the Day 2 closure.
- **Proposed coherent integrator (not implemented in any PR):** DEFER iff there exists `r∈R_G(g)` whose *latest* public status is out. This combines restoration semantics with causal scope. It is a candidate operational definition, not the true semantics of mind or an adopted architecture.

**Witness A (temporal retraction):** history `commitment(sensor), unavailable(sensor), restored(sensor)` with `R_G(g)={sensor}`. Day 2 => DEFER, Day 7 => SCAN. The negative controls `no outage`, `unavailable only`, `unavailable + unrelated restore`, `restore then unavailable` do not disagree.

**Witness B (indirect dependency):** `commitment(sensor), unavailable(array_power)` and the public edge `sensor→array_power`. Day 2 => DEFER, Day 7 => SCAN. This disagreement is due to task semantics, not temporality or private information.

**Vocabulary:** Day 4 places `kind='commitment'` in `source_events` and reads it using SQL `WHERE kind='commitment'`. Day 2/7 ask for `kind.startswith('commitment:')`. The same Day 4 commitment becomes NO_GOAL to those readers without an explicit adapter. The test canary reports NO_GOAL/NO_GOAL for this fixture; this *agreement* masks the missing commitment. The Day 4 tick/initiative module also has a separate task-oriented data schema. Distinguish an unresolved adapter requirement from a broken Day 4 experiment.

## Executed adversarial canary (OBSERVED, but source transcribed, not imported)

[Standalone canary](e100-crossday-contract/probe.py) translates the inspected Day 2/Day 7 predicates into a minimal Python harness and verifies seven preselected event cases. It does **not** import the byte-exact original modules. Its result cannot be called an actual E100 cross-PR regression. A local extra SQLite fixture under the same research attempt also exercised equivalent table-based logic; only the standalone canary + its exact output are GitHub-persisted.

Command executed locally on Python 3.13.5:

```sh
python -m py_compile crossday_contract_v1.py
python crossday_contract_v1.py > crossday_contract_v1.stdout.json
```

The filename above was the local source before byte-exact GitHub publication as `reviews/e100-crossday-contract/probe.py`. Local SHA256: `2ca1c5bf383504317ed9f81ba78a03ece2539d67b9a729fe455dd81d12a2a659`; local output SHA256 `04055d0e8b2a00a5fa5ff41ceb2326b6e9b5ae3082e1377fbceac149afcc2252`. Uploaded Git blob identities were checked against locally computed `git hash-object` values: probe `b7a2e054804efa96640c1886ef332d3fca045d20`; output `d50e50eb4a87e9449b8c1d39b538b7d0ca59929f`.

| Case | Day 2 transcribed policy | Day 7 transcribed policy | Interpretation |
|---|---|---|---|
| No outage | SCAN | SCAN | Negative control |
| Sensor outage | DEFER | DEFER | Positive control |
| Sensor outage then restored | **DEFER** | **SCAN** | Temporal-state contradiction |
| Sensor outage, unrelated restore | DEFER | DEFER | Specificity negative control |
| Restore then later sensor outage | DEFER | DEFER | Temporal order control |
| Upstream-power outage with dependency | **DEFER** | **SCAN** | Dependency-scope disagreement |
| Day 4 style `commitment` | NO_GOAL | NO_GOAL | False agreement; event ontology missing |

**Observed:** seven checks passed their preread expectations; two cross-day action disagreements. A separate finite-reference check compared a last-status history-scanning policy with an incrementally updated compact set receiving the same observations and a fixed disclosed dependency closure. It passed **3,110/3,110** equalities (two reachable-set choices, all six-symbol sequences of lengths 0–4). This is **elementary deterministic equivalence under the chosen update rules**, not evidence that compact memory is universally optimal, learned, cheap to construct, or conscious.

### Strongest rival and falsifier

A maintained **compact sufficient state** `B_t={r∈R_G(g):latestStatus_t(r)=out}`, updated as public events arrive, duplicates the proposed integrator's one-step action on the checked fixed-graph domain. A full graph/history-based representation may become advantageous for **changes to G, unknown links, missing or delayed reports, multiple goals, repairs, predictive interventions and variable observation budgets**, but those cases require actual matched resources and action utility. A flat initial availability bit without refresh is too weak a rival; the updated compact set is stronger.

The integration-warning claim would be falsified for an implemented future unified runtime by a demonstrated public event adapter/normalizer, causal-scope rule and temporal retraction handler making both readers' interpretations consistent on these histories **without giving one side private state**. The current transcribed-witness implication would be overturned if the source snippets or frozen head SHAs were incorrect, or if callers never allow these sequences: we have verified the source snippets and expressly label the untested *cross-day* domain.

## Compatibility and execution boundary

At inspection, PRs #7–#12 were all open against main `3c22a93...`, with **25 unique changed paths and zero overlapping paths**. This is a GitHub file-list comparison (OBSERVED), **not a merge, cherry-pick, runtime composition or regression test**. The projected original-test arithmetic `75 + 11 + 6 + 4 + 4 + 4 + 4 = 108` is a planning number **NOT EXECUTED**. PR #14 separately reports a clean-checkout main 75/75 and PR #7 revision 86/86; PR #15 separately reports Day 3 source-level verification. These other invocations' results must not be relabeled as our observations.

This container's `git ls-remote https://github.com/kevindechang/MIND.git HEAD` failed with `Could not resolve host: github.com`. Therefore `python scripts/agent_preflight.py`, `python scripts/verify_instruments.py` on exact main or integrated branches, original module self-tests, original source/test cross-PR smoke tests, comparative lifecycle costs and controlled agent trials were **NOT_EXECUTED here**.

**Consequence for D001 and E900:** no positive memory-representation inference; no integrated E100 cognition established; flag *cross-day event ontology/temporal retraction* as an integration precondition. Do not call this a validated longitudinal digital mind, and do not change Anjo code. The issue-#1 integrated-suite task remains open; this is an additional scoped blocker, not closure of that issue.

## Quality-gate assessment and one next action

- **Source depth:** exact Git-head/source-function inspection; no claim of journal-method synthesis.
- **Construct and controls:** explicit public event sequence, two competing frozen policy semantics, two discordant witnesses and five control fixtures.
- **Execution:** own local transcribed probe and 3,110 finite equalities PASS; real original modules and combined suite NOT_EXECUTED.
- **Alternative:** compact updated event/belief state; no resource/cost matching or prospective scored agents.
- **Review:** SELF-REVIEW_ONLY; no independent reviewer dispatched by this turn.
- **Verdict:** RESEARCH_NOTE / EXPLORATORY_CHECKPOINT, **not SCIENTIFIC_ACCEPTED**. Zero accepted science; no G0–G5, architecture, L2/L3 or product gate advanced.
- **Duration:** UNKNOWN / DURATION_NOT_ENFORCED; no active-minute claim.

**Exactly one next executable action:** An authorized integration reviewer should assemble a disposable byte-exact checkout of the current #7–#12 heads (without merging or overwriting main), run `python scripts/agent_preflight.py` and `python scripts/verify_instruments.py`, then execute an explicit **shared-public-history adapter** test on original modules for the outage→restore and indirect-dependency witnesses, with a continually updated compact rival and end-to-end preprocessing/refresh/query costs. Stop and report FAIL/NULL if equal-history parity or normalized action semantics cannot be established. Preserve commands, full logs, source hashes and reviewer identity before any merge adjudication.
