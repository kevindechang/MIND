# H004 design SELF-REVIEW — 2026-10-11

**Review type:** SELF-REVIEW / STATIC DESIGN PASS ONLY. This is a second written adversarial pass by the same model, **not** an independent reviewer, replication, executed review, or scientific validation.

**Material inspected:** live `AGENTS.md`, `GO.md`, `docs/SUBSTRATE.md`, `docs/CLAIMS.md`, `docs/PIPELINE.md §5`, `STATUS.md`; H004 branch diff and C021/C022. No independent reviewer agent available in the exposed tool interface.

**Execution capability:** `git clone --no-single-branch https://github.com/kevindechang/MIND.git /mnt/data/MIND` returned exit **128**, with `Could not resolve host: github.com`. The GitHub connector can inspect and write files, but it cannot run Git-backed `mind` integrity checks. No attempt was made to impersonate evidence, construct held-out seals outside Git, or run GitHub Actions (prohibited without owner approval).

## Adversarial checks and disposition

| ID | Finding / attack | Disposition |
|---|---|---|
| SR01 | Earlier long-window transcript baselines used public `outcome` to update TD and table estimates, but **did not** feed the previous action/outcome pair into their policy features; the recurrent organ did. An advantage might reflect unequal inputs, not recurrence. | **FIXED IN DESIGN:** `FeedbackTranscript` injects `previous_action_outcome` into the current observation before TD action selection; `window16fb` and `window32fb_lin` added to the rival zoo. The transcript rival has **at least** the public information of recurrence, often more. Tests cover outcome absence and episode boundaries. NOT_EXECUTED. |
| SR02 | Default K01/K06/K07 checks use the default organism without the optional organ. They cannot establish replay/determinism/exactly-once for `+recurrent`. | **FIXED IN DESIGN:** explicit optional-organ restore, fresh subprocess under three `PYTHONHASHSEED` values, and `step_at` idempotent retry tests added. Tests NOT_EXECUTED. Existing full invariant checks also NOT_EXECUTED. |
| SR03 | The recurrence's four fixed random signed projections are not learned weights; only the downstream Q policy learns. Labelling them a trained recurrent representation would be misleading. | **DOCUMENTED:** bounded fixed recurrent reservoir; claims concern its incremental causal utility only. No trained RNN, no L3 assertion. |
| SR04 | With `capacity=4`, adding recurrent proposals also alters what other workspace contents are selected. Positive/negative effects can be due to **competition/attention** rather than temporal integration. | **UNRESOLVED EMPIRICAL CONTROL:** compare `organism +recurrent` to `organism +recurrent shuffle:recurrent` and `organism +recurrent cut:recurrent>policy` on dev, plus `capacity=inf` sensitivity. No inference is licensed until the lesion actually alters the relevant causal path and the results are inspected. |
| SR05 | `window16fb` may lose the request just before a maximal 16-tick bell; `window32fb_lin` covers the entire long-gap transcript but has no conjunctions. Neither is parameter- or compute-matched. | **PARTIALLY MITIGATED:** two feedback-enabled baselines with different capacity/feature trade-offs. **STILL OPEN:** consider `window32fb` with full conjunctions and benchmark actual compute if feasible. Under no circumstances claim a resource-matched superiority from these rivals. |
| SR06 | In the recurrence implementation, public prior-action feedback is incorporated into the trace after selection at time `t`, but becomes broadcast only at `t+1`. The transcript baseline sees that feedback in current-step policy features at `t`. | **DOCUMENTED:** information is matched but latency is **not**; the feedback rival is strictly less delayed on that channel. This makes it a strong adversarial comparator, not a controlled architectural ablation. |
| SR07 | The goals organ independently retains the request and may already solve `vigil/long`; recurrent traces could be redundant or harmful. Fixed projections may also alias distinct requests. | **FALSIFIABLE / NOT_EXECUTED:** C021 predeclares a +0.05 effect; negative or inconclusive C021 is a first-class result. Inspect request-conditioned trajectories and goal-lesion sensitivity on dev only. |
| SR08 | Existing C021/C022 predictions were committed prior to the present design pass. Rewriting them to rescue a future null would be invalid. | **UNCHANGED:** no committed claim prediction has been altered. No held-out seeds have been inspected, sampled or selected. |
| SR09 | The optional organ is absent from the default atlas lesion set; running `python -m mind atlas` alone cannot show an H004-specific causal atlas. | **OPEN EXECUTION STEP:** additionally invoke `mind.atlas.atlas(..., base="organism +recurrent", organs=("recurrent",), worlds=("vigil","outage"), variants={"vigil":"long","outage":"silent"}, pairs=False)`. Use the default atlas for regressions, not as evidence of optional-organ effects. |
| SR10 | Registering additional rivals that challenge memory and goals can demote older superiority claims and alter code fingerprints. | **REQUIRED GATE:** rerun/record both seed sets for **every** claim after result code changes, commit all records including failures, run full check/tests/doctor, and only then regenerate `STATUS.md`. Old records must never be edited/deleted. |
| SR11 | The GitHub API can write source, but it cannot prove tests pass or emit valid `--record` evidence, and it cannot establish live held-out seeds without full Git history. | **BLOCKING ENVIRONMENT LIMITATION:** all `mind` commands, exploratory runs, quality gates, records, atlas, and independent reviews remain **NOT_EXECUTED**. This design-only PR must remain draft and unmerged. |

## Independent review request (not performed)

Request an independent contributor, using a different environment and model/human reviewer, to audit exact source and claims, all information flows, the truth-by-construction problem, control fairness, whether lesions have a measurable impact, and sealed record provenance **before any merge**. No named reviewer has been assigned; **INDEPENDENT_REVIEW_NOT_DONE**.

## Completion determination

**Blocking items remain**: runtime unavailable; claims never run; rival performance unknown; atlas and quality gates unexecuted; independent review absent. SELF-REVIEW does not clear them. This is a design checkpoint, not evidence for L2 functional consciousness.

## Next concrete run

1. Obtain a true, history-preserving `git clone`; run `python -m mind doctor`.
2. Run new tests and exploratory dev sweeps, including two worlds, feedback rivals and shuffle/cut/capacity controls.
3. Run C021 and C022 on full dev seeds with `--record`, commit records; then run first sealed held-out checks and commit **all** records regardless of verdict. Do not amend predictions.
4. Run `python -m mind atlas` **and** optional-base atlas, refresh both dev/held-out evidence for every claim (result code changed), and commit all records.
5. Rerun `mind check`, unit tests, doctor; `mind status --write` and commit STATUS; secure genuinely independent review, resolve findings and keep PR draft until all checks pass.
