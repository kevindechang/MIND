# MIND H019 staged integration — design specification

**Date:** 2026-10-17  
**Repository:** https://github.com/kevindechang/MIND  
**Baseline:** main @ e3098aeb8e718257b30791137096f0c770217a26  
**Status:** DESIGN FOR OWNER REVIEW — no implementation or sealed scientific confirmation authorised by this document.  
**Source package:** user-supplied MIND Principal-Scientist Package (2026-10-17), updated with independent review and subsequently uploaded scripts.

## 1. Objective and non-goals

**Objective.** Integrate the research provenance, repair the K07 tick-zero harness race, and introduce H019 model-first residual arbitration as a reversible, opt-in experiment inside MIND's existing organism, world suite and claims engine. Preserve existing decision/replay semantics when flags are absent. Obtain reproducible, preregistered evidence that can validate or refute the proposed controller, without altering scientific history.

**Non-goals.** No production Anjo integration; no assertion of subjective consciousness; no rewrite of the kernel or ledger; no replacement of existing H018 defaults; no paid APIs, real user data, GitHub Actions or autonomous scheduling; no self-declared independent replication; no held-out treatment-arm utilities prior to a registered and pushed claim.

**Success** is not a HOLDS verdict. Success means the submission and its baselines are reviewable, all relevant invariants and re-record requirements are satisfied, and every prospective claim receives an honestly recorded outcome, including failure or inconclusiveness.

## 2. Verified starting point and evidence boundaries

MIND main at the baseline commit has 53 HOLDS, 7 INCONCLUSIVE, 7 REFUTED and 7 RETIRED claims according to the generated STATUS.md snapshot; that is **existing project evidence**, not an independently reproduced result of this integration. Open PRs #56, #57, #59, #60, #61 and #71 may overlap on result code or research design. Issue #55 tracks standing integration debt; #39 programme-level error control; #40 independent replication; #54 execution limitations; #70 model-backbone continuity.

The uploaded package contains a research monograph, architecture comparison, 18-experiment portfolio, 12-week roadmap, source register (114 entries), two proposed patches, H019 question, draft C102–C107 claims, scripts, raw dev JSON datasets and check logs. The first independent review was conducted before the final batch of scripts arrived; file availability and reproducibility must be re-assessed from the complete package. In particular, run_x.py/run_y.py/run_z.py and tune_gru.json **are now supplied**; gru_best.json remains absent but can be reconstructed from tune_gru.py and tune_gru.json (grid item #18: hidden=64, lr=0.003, eps_decay=600, target_every=25), subject to script verification.

All uploaded simulation results are **development exploration**. Recalculating numerical differences is not an independent run or confirmation. The supplied final check log reports 67 checks: 56 HOLDS, 7 expected FAILS and 4 INCONCLUSIVE, with no ERROR, BROKEN or REGRESSION reported; code fingerprint standing still requires the repository-prescribed re-record. There is no captured held-out/beacon result, registered H019 claim, or pushed H019 implementation.

## 3. Alternatives considered and chosen design

1. **Monolithic research + feature PR.** Simple upload, but creates a large, unreviewable diff; mixes metadata, bugfix, result-code modifications and predictions. Rejected.
2. **Three sequential, independently reviewable contributions (chosen):** research provenance archive; K07 harness repair; H019 opt-in implementation, with claims registered only after the final result code is merged and re-recorded. This separates scientific hypothesis from integration and makes regressions attributable.
3. **Rewrite the MIND organism around a neural learned core.** Premature: no robust evidence that a learned recurrent architecture beats matched simpler controls, and changing the kernel would invalidate substantial provenance. Deferred to a separately scoped H020+ experiment.

This spec and each later component must get its own review gate. Sequence is determined by RESULT_CODE and sealed-record requirements, not by what is easiest to upload.

## 4. Research archive design

Target paths:
- docs/research/h019/README.md — provenance matrix, baseline SHA, source manifest, links to original report modules, omissions, and exact epistemic status.
- docs/research/h019/01_research_monograph.md ... 11_source_register.md — research material, clearly marked **external proposal / not MIND-confirmed**. Retain substantive negative results and disagreements; fix stale execution-status text with a dated errata file, not undisclosed silent edits.
- docs/research/h019/execution_status_2026-10-17.md — immutable account of executed vs NOT_EXECUTED commands, trees, seed classes and known held-out exposure.
- experiments/exploration/h019/ — runnable scripts, selected hyperparameters, reproducibility instructions, and optionally compressed data/artifacts when repo policy and size permit. Existing hardcoded /tmp/MIND and /tmp/explore paths must become relative to a documented checkout; do not claim scripts reproduce results until they execute.
- Draft question/claims and proposed patches live as documented **draft artifacts**, outside active knowledge/claims and executable result paths until implementation is ready. No accidental registration or benchmark run from documentation imports.

Archive checks: source file count and SHA-256 manifest, consistent document citations, no claims of sealed or independent evidence, no private/secret material, and lint/Markdown link checks where available. The 114-entry citation audit reported by the source is not independently certified: label each bibliography verification status faithfully.

## 5. K07 race fix design — own PR

**Root cause.** In mind/worker.py, _wait_committed repeatedly calls _last_event; a fresh-worker tick-zero commit may be polled before the SQLite ledger exists or its events table is initialized. The uploaded patch catches sqlite3.OperationalError globally, which is too broad and can mask corruption, locking and unrelated SQL errors.

**Minimal change.** Retry *only* transient database-not-created / events-table-not-ready errors until the existing bounded deadline, on a monotonic clock. Unexpected OperationalError, corrupt schema, permission failure or invalid ledger should fail loudly. Never treat a malformed existing ledger as an empty one. Preserve the existing exactly-once semantics, replay counter and SIGKILL protocol.

**Tests.** (1) Baseline regression: tick-zero kill_committed raises before fix and passes after fix, with trace and ledger head identical to a no-death run. (2) A deliberately malformed/corrupt database aborts clearly, rather than spinning until timeout. (3) Delayed file/table creation is retried only until committed event observed. (4) K07 and K06 through real processes where POSIX SIGKILL is available. Use red-green verification, not only a single successful run.

**Scientific integration.** mind/worker.py is included in RESULT_CODE, so this PR requires full dev and held-out re-record according to GO.md §5; coordinate other result-code PRs, preserve original records, use merge commit (never squash/rebase a seal). Do not merge while CURRENT_CODE_UNVERIFIED or tests/error reports remain unexplained.

## 6. H019 controller design — subsequent opt-in PR

**Extension points.**
- mind/organs/causal.py: keep the 25-DAG posterior, source/efference semantics and myopic VOI. Add opt-in prior_plan, residual, model_free, optimism, optimism_cap and residual_floor. The residual is keyed by public commitments, known probe results and chosen plan; prediction is captured in after_act and updated from realized terminal payoff. Exactly-zero initial residual retains model control at birth. Model inconsistency falls back to legally scored raw observations rather than assuming an inconsistent posterior.
- mind/organs/policy.py: opt-in obey routes legal causal probe/best recommendations directly. **Critical correction required:** forced action must still execute QLearner bookkeeping (including known legal actions and decisions), preserving learned relevance used in workspace priority. Split bookkeeping from stochastic action selection rather than calling choose (which might sample a different action). Test learned relevance and workspace selection under identical observations.
- mind/worlds/workbench.py + mind/worlds/__init__.py: registered shared world with dev XOR, development OR, held-out AND and stochastic slip. Same allowed observations and actions; no privileged graph access. Report utility as primary. Define gap_full as expectation-relative under slip; realized episodes can have negative gap.
- tests/test_h019_proposal.py: expand into isolated tests for posterior with no facts, inconsistent DAG fallback, legal ties, learned residual update, recency floor, optimism cap, OR/AND truth table, slip probability/action independence, same-stream pairing, old-default byte-identical ledgers, lesion cut:causal>policy, workspace relevance, and K02/K06/K07/K09/K10 where applicable.

**Alternative baselines.** H018 integrated, organ-direct/no-residual, equal-key tabular corrective policy, compact memory, Bayes oracle when well-defined, and a genuinely separate recurrent model-free learner. The equal-key tabular rival still uses model-based information-seeking (VOI), so label it **model-free plan scoring with shared model-based probing**. The supplied recurrent baseline is an **Elman DQN**, not a GRU. Its dev results are informative but not a final comparison to modern recurrent/meta-RL baselines.

**Dependencies.** Main organism remains stdlib-only (CONTRIBUTING.md). Proposal: optional pinned NumPy only in isolated research-rival extras/environment, with explicit owner approval of the change in dependency policy, numerical reproducibility/tolerance tests and compute accounting. Do not silently introduce NumPy into organs or required core checks.

**Compatibility.** Unset flags reproduce existing ledgers byte-for-byte. New configurations must survive fresh-process replay under varied hash seeds, real SIGKILL after committed step/end, long-term replay, and relevant negative controls. Anomaly triage uses logs and correct root cause; no relaxation of test gates.

## 7. Prospective claims and data hygiene

H019 question and draft C102–C107 are **not registered**. Before any new treatment-arm computation on reserved families:
1. Resolve ambiguous inference target: C102 is a controller-level intersection-union comparison of six one-sided margins. If calling it mechanistic, specify about-organ coverage and the automatic rival ladder; otherwise explicitly limit the claim to controller-level effects.
2. Freeze prediction source, contrasts, sample count, metrics and margins. Avoid data-dependent alteration of margins using dev performance.
3. Set exposure matrix: dev XOR/censored/skewed, dev OR and nonstationary switch used; AND/slip had nonutility smoke and replay/shadow invariant exposure with plain arms but no reported utility. Record any additional unintentional exposure.
4. Re-record existing claims on exact final result code, ensure all current-code standing gates pass. Resolve #55 and overlapping result-code PRs first.
5. Register H019 and C102–C107 on the *final* code, commit and push seal, then run prospective --record and --beacon --record exactly once per declared protocol. Commit every record regardless of outcome.
6. Never treat a second run by the same agent/environment as independent replication. Report uncertainty across claim families and rival-search degrees of freedom; coordinate issue #39 error controls.

If any registered claim fails, retain its evidence and propose a new successor question instead of editing its prediction. Do not promote opt-in behavior to default based on exploratory development data.

## 8. Integration and error handling

**PR ordering:** P0 docs-only research archive (no result code); P1 K07 isolated harness fix and re-record; P2 H019 opt-in feature and expanded tests plus re-record; P3 H019 registered prospective claims once result code is stable. Open PRs #56, #57, #59, #60, #61, #71 require overlap review before each result-code PR; do not bulk merge them as part of H019. Preserve a single organism/world/rival suite. Standalone simulator scripts remain exploratory and must not create a second implementation.

**Failure gates:** missing original files or source provenance; undecidable experiment overlap; green tests without a red regression stage; K02/K06/K07 or byte-identical default replay failure; unexpected result-code drift; stale STATUS; missing doctor git verification; Git unavailable; unhandled errors; unexplained performance deltas; or unregistered held-out exposure. Mark blocked tasks NOT_EXECUTED rather than fabricating outcomes.

**GitHub workflow:** isolate each PR on a branch based on the current main at implementation time. Maintain branch pointers and ensure merge commits preserve sealing ancestry. No force-push or squash of sealed commits. This document is a design specification only; executing scripts in a scratch checkout is permissible for nonsealed dev verification after implementation approvals, never for seal-sensitive heldout experiments ahead of registration.

## 9. Research questions after H019

**H020 (proposed, not yet registered):** Can a learner detect an inadequately specified causal model and grow a new hypothesis class or representation, outperforming a matched residual lookup-table controller on unseen form-changing environments without increasing false discoveries on null worlds? Enforce matched observation, action budget, compute, development leakage and first-action regret; compare to an enumerated-form Bayesian rival and learnt abstraction controls.

**Other deferred directions:** cross-task first-action transfer and learned relational abstraction, model-independent typed state across LLM A→B swaps (coordinate issues #70/#71/#50), second-order competence monitoring with entropy-gating rival, offline consolidation versus equal-compute rehearsal, and proper recurrent/meta-RL baselines. No phenomenal consciousness claims or Anjo production transfer without separate authorization.

## 10. Acceptance and review contract

**Design review:** owner reads and approves this written spec before a code implementation plan is started.  
**Plan review:** create file docs/superpowers/plans/2026-10-17-mind-h019-staged-integration.md using Superpowers writing-plans; owner approves and selects inline/subagent execution before modifying product code.  
**Research archive:** complete, attributed, self-contained provenance and no false scientific registration.  
**K07:** regression red/green, malformed-db failure, real SIGKILL K06/K07 where executable, unit suite, doctor, check, required records.  
**H019:** specified tests, opt-in behavior, default byte-equivalence, cross-process replay, K02, strict source/held-out controls, no unexplained standing regression.  
**Scientific confirmation:** predictions sealed and outcomes recorded as HOLDS/FAILS/INCONCLUSIVE, not preselected.  
**Product transfer:** NOT_READY_FOR_PRODUCT_TRANSFER until an independent, separate safety/engineering approval.

**Decision requested:** approve this written design, then author the implementation plan and choose its execution workflow. Approval of this specification does not itself authorise running held-out comparisons or merging code to main.
