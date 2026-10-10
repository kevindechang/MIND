# Issue #3 referee checkpoint — E100 Day 5 / E002a mechanism identifiability

**Date:** 2026-10-11 (Asia/Taipei). **Artifact:** ADVERSARIAL_RESEARCH_REVIEW / EXPLORATORY_CHECKPOINT; **scientific acceptance:** 0, unchanged. **Review mode:** CROSS-INVOCATION_AI_REVIEW_NOT_INDEPENDENT_EXTERNAL / SELF-REVIEW_ONLY for scientific independence. **Duration:** UNKNOWN / DURATION_NOT_ENFORCED. **E900:** NOT STARTED. **Anjo:** NOT_READY_FOR_PRODUCT_TRANSFER.

**Target immutable evidence:** MIND main `3c22a93a6d15a909789bb6e40c387a34b183ee7c`; PR [#10](https://github.com/kevindechang/MIND/pull/10), head `238c08c267b8506b625b0e45b1660ee6915000f7`; `experiments/e100/day5.py` blob `222e6a2d9d5e1ad823019b9b62931d16c0497200`; `experiments/e100/day5-preregistration.md` blob `53bce790b0ddb362e6356b1440e62880110ed960`; test blob `55aff0286b90091b73da4f63d03d84cbf4cc9a78`. Compare the live PR head again before applying any change. This is **not** approval of PR #10 or evidence Day 5 is integrated.

## Precise research question and decision

Can the Day 5 instrument identify an *incremental causal effect of endogenous self-maintenance* rather than (i) mere access to a task-value table, (ii) an adaptive decision rule, or (iii) the placement of otherwise identical code inside/outside a worker?

**Decision D-W2-IDENTIFICATION:** Do not promote H005/H008, endogenous cognition or an architecture if an external learned controller with matched observations, resources and state retention is observationally equivalent. A deterministic tie between identical policies validates implementation parity but **cannot estimate** a special endogenous advantage. A positive value relative to a weak timer is also insufficient.

## Finding 1 — the primary comparison is an identity, not an empirical null (IMPORTANT; HIGH confidence)

In PR #10 `internal(db,qc)` and `external_adaptive(db,qc)` have precisely the same selection algorithm and the same `_execute` call. Each computes

```
argmax_(task in visible orders) (gain(task) - cost(task))
if max net <= 0: IDLE
otherwise: execute selected task
```

with the same SQLite input and reset between sequential invocations. Hence for every possible work-order table in the current API (modulo nondeterministic equal-net iteration ordering or environmental side effects that are not part of this controlled setup), action and nominal receipt necessarily match. When both active they also follow the same manual query-counter increments. Formally, for identical policies `f` and shared observation `O`, `Y_internal(O) = f(O) = Y_external(O)`. This is an **elementary equivalence invariant**, not a sampled scientific effect or an equivalence test with a predeclared practical margin.

**Counterfactual:** Retitle the result `REFERENCE_POLICY_IDENTITY_CHECK` or `INSTRUMENT_NULL_BY_CONSTRUCTION`. The label 'adaptive' is descriptively accurate only as a deterministic rule reacting to a given table; it is **not a learned external scheduler**. The preregistration explicitly says 'learned = fixed max-net rule (no training)', contrary to the W2 protocol's distinct *learned* value-of-computation comparator. One cannot use a positive result to infer special internal agency, nor the tie as evidence that independently trained internal/external controllers are equivalent in evolving environments.

## Finding 2 — cron gap depends on a planted order and is not a discriminative control (IMPORTANT; HIGH confidence)

The fixed `CRON_ORDER` begins with `vacuum`. The default table makes `recalibrate` uniquely optimal (net 7) while `vacuum` is net 4. The cron comparison therefore loses by choice of synthetic world, while max-net is provably at least as good as a fixed choice under the very cost labels it optimizes. The statement that cron underperformance 'validates the comparison isn't vacuous' overstates what has been measured.

**Counterexample world, independently checked as arithmetic on the published policy semantics (NOT a byte-exact PR test):**

| World | `recalibrate` net | `vacuum` net | Internal/external action and net | Cron action and net | Implication |
|---|---:|---:|---|---|---|
| Frozen default | 7 | 4 | recalibrate, 7 | vacuum, 4 | Constructed cron disadvantage |
| Changed payoff map | 4 | 9 | vacuum, 9 | vacuum, 9 | Cron **ties** adaptive; predeclared 'cron must lose' is not a universal instrument validity requirement |
| Both tasks negative | -4 | -4 | IDLE, 0 | vacuum, -4 | Cron still spends resources; advantage is a rational stop rule, not endogenous structure |

Reproducer semantics: for each row, select the maximum strictly positive `gain-cost`, otherwise IDLE; cron takes the first present key from `['vacuum','recalibrate','audit']`. These three outputs were computed in this invocation using a small independent Python probe. **PR #10 code and unit suites were NOT_EXECUTED here**; the repository is readable through GitHub but container DNS prevented an authenticated byte-exact clone. The existing PR's reported 79/79 is historical author evidence, not freshly reproduced verification. The altered world is an adversarial probe to preregister in the next version, not a retrospective preregistration.

**Correct stop rule:** A cron tie or win in an eligible world is valid negative evidence about the heuristic margin; it must not automatically invalidate the simulator or be excluded. Report per-world differences and uncertainty with a frozen practical margin.

## Finding 3 — parity and isolation are not measured as claimed (IMPORTANT; HIGH confidence)

- `run_arm` executes all three policies **sequentially on one ledger**, deleting and committing receipts between calls. It does not implement three separately randomized/restarted experimental arms. Although current policy functions ignore prior receipts and the sequence may be harmless for this toy, it cannot establish arm isolation, runtime-equivalent storage/access or restart behavior. Use separate ledgers per treatment, then require hash-equivalent initial permitted state.
- `qc[0]` is incremented **manually** in `_orders` and `_execute`; the `_execute` increment calls a `SELECT` but is described as a 'receipt write'. Actual SQLite statement counts, reads/writes, time, disk I/O, training/precomputation, model/token costs and scheduler invocation costs are not measured. `DELETE FROM receipts` and `db.commit()` between arms are not charged. Matching this counter is **not** compute parity.
- `work_orders` contains the payoff labels supplied before choice; there is no uncertain value estimate, hidden state, feedback delay, out-of-distribution world, endogenous initiative trigger, or learned parameter update. The action receipt is the same table's difference, not a realized downstream return. This is a deterministic rule-selection **instrument**, not a maintenance efficacy trial.

## Positive methodological contribution: a falsifiable next comparison

Target a **prospectively frozen, multi-period** partially observed maintenance world. Define the estimand as the paired world-level mean difference in realized downstream utility net of *total* compute/preprocessing/serialization cost (with a confidence interval and preregistered practical effect margin). Compare:

1. Internal *learned* maintenance controller with persistent state.
2. Separate external *learned* value-of-computation scheduler, with identical observation/feature interface, offline training budget, inference opportunity schedule, tools, wall-clock windows, memory capacity and restart access.
3. Strong compact queue / expiry-value learner and resource-matched fixed timer.
4. Internal latent-variable lesion plus sham, and an **external+same-extra-inputs** control for any purported private-signal advantage.

Use separate worker processes and isolated ledgers. Keep evaluator world state hidden; predeclare paired randomized seeds, held-out dynamics, ablations, missingness/delayed feedback, uncertainty computation at world rather than timestep level, leakage checks, fail/stop/exclusion criteria, and honest null interpretations. If the learned policies are behaviorally identical under matched state and observation, the correct conclusion is **non-identification**; investigate a different mechanistic intervention, not cosmetic labels. If internal outperforms, rule out model-capacity/data/timing asymmetries before calling it endogenous competence. Register an E900 cross-function prediction only after useful mechanism evidence: a maintenance-policy lesion should alter later memory-correction/planning under fixed interface and budget.

## Provenance and review limitations

**Directly inspected in this invocation:** PR #10 head metadata, complete `day5.py`, preregistration and dedicated tests, issue #3, existing `dossiers/W2-endogenous-maintenance/methodological-reassessment.md`, MIND `GO.md`, `AGENTS.md`, `TASKS.md`, `RUNBOOK.md`, `review-protocol.md`, `research-quality-gate.md`, and source hierarchy. Existing W2 dossier cites a full-text 2018 Lieder et al. methods/results examination **by a previous invocation**; those primary methods and additional cited papers were **not freshly fetched/read** for this review. No source-count or independent-peer-review claim is made. No private Anjo input was used.

**Actual local execution:** small independent Python arithmetic probe for default/changed-payoff/all-negative examples. **Not executed:** PR source, PR unit tests, integrated `scripts/verify_instruments.py`, scored LLM-agent trials, separately trained comparator, process-restart treatment trial, E900. **CI:** no commit statuses found at inspected PR head; no Actions triggered. **Independent review:** no independent human/external scientific referee.

**Decision:** REVISE / EXPLORATORY_CHECKPOINT, G0 OPEN, scientific accepted contributions **0**, H005/H008 unpromoted, D-W2-IDENTIFICATION OPEN/NEEDS_DISCRIMINATING_TEST. Reuses W2 v0.2 methodological constraints but does not claim a new empirical mechanism or invalidate other lesions without reviewing them. This review should not become a substitute for Day 2's pending reproducibility work. No Anjo architecture selection or production transfer.

**Exactly one next executable action:** Revise PR #10's claim and implement an isolated, independently learned external-scheduler comparator on a prospectively frozen multi-period held-out maintenance test, then reproduce all arms from an exact checkout before claiming matched-compute or learned-policy results. Stop and report **NON_IDENTIFIABLE** if the two policies remain identical by definition; retain the simpler mechanism.
