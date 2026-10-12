# MIND repository and PR scientific integration audit — 2026-10-12

**Review type:** same-model static/API review, NOT independently executed or replicated. Main head inspected: `3fdf7034684b68da6ae907899a334237c8a72368` after merging documentation PR #62 and claim-only experiment PR #58. Evidence from source files, claim/record JSON and GitHub PR diffs. No claim of a full source-level security audit.

## Integration capability and verification debt

- Git-history checkout was attempted with `git ls-remote https://github.com/kevindechang/MIND.git HEAD`, and failed: `fatal: unable to access 'https://github.com/kevindechang/MIND.git/': Could not resolve host: github.com`. No Python `mind doctor`, unit suite or combined-tree `mind check` was run in this reviewer environment. API inspection is NOT equivalent to executing the Git-dependent claim integrity tests.
- GitHub reported no combined status contexts and no check runs on open PR heads #56–#61. The repository tree has no `.github/workflows/` CI files. A green PR narrative is branch-author evidence only.
- PR #58 was integrated with **merge commit** preserving its original claim seal and records; its branch had author-reported passing validation, and the new main prior to merger changed documentation only. Nonetheless **combined-tree validation remains owed** and must not be claimed as observed by this reviewer.
- Latest STATUS is a generated snapshot, not a live execution. At this checkpoint: 36 HOLDS, 3 INCONCLUSIVE, 7 RETIRED; C019 has CURRENT_CODE_UNVERIFIED standing. On a proper checkout regenerate status after `mind doctor`, unittest, full and sealed checks, and verify git history/records before further result-code merges.

## Whole-repo architecture assessment

**Strengths.** The same learning organism and its hash-chained event ledger are reused; organs can be removed or access-cut; process-restart/replay invariants exist (K01/K02/K06/K07); predictions are commit-sealed; held-out and negative records remain append-only; outcome metrics are adjudicated with intervals rather than unqualified PASS; simple rival controllers live in the suite. The corrected shadow readout and matched feature-load shams (PR #29) are a concrete improvement over earlier lesion interpretation. The experiment-to-claim-to-record-to-status pipeline is superior to v1's independent scripts and hand-written project status.

**Scientific threats to validity (ranked):**
1. **Architectural necessity not identified.** Many strong effects establish that a feature is useful in this particular organism, not that it is uniquely required. C020 still fails to beat `window4`, and C011/C012 show poor causal planning compared with a reactive/Bayesian comparator. For all consciousness-relevant indicators, prefer matched-state interventions and strong sufficient-state rivals. Positive tests in worlds designed around a mechanism should not become general claims.
2. **Calibration and integration confounds.** C030/C031 disprove a naive interpretation of C016's cross-function cells; changed action distributions and feature-count/learning-rate load can create apparent integration. Use K09/K10, load-matched sham, shared event streams, negative controls and separate causal estimands.
3. **Held-out and replication independence.** Seeds depend on registering commit hashes and are in principle inspectable before commitment (see P001); don't grind commits. Free-text contributor names and distinct VMs can meet an automated ladder without independent people or autonomous labs. Label such runs `SAME_MODEL` or `SELF_REVIEW_ONLY` and report both operational reproducibility and genuine independent confirmation.
4. **Out-of-family generalization is untested.** Existing worlds (`vigil`, `outage`, `workshop`) are informative instruments but not a comprehensive repertoire. Random held-out seeds within a fixed simulator do not test unseen causal laws, social partners, latent variables, normative conflicts or first-encounter generalization.
5. **Cross-PR result-code interference.** #57 changes world and rival registries, #59 changes rival/runner/world/claims metrics, #61 changes the self-model and shadow. Independently green source fingerprints do not imply that the combined research program is green; every result-code merge forces re-recording and source/seed provenance checks.

**Governance strengths and limits.** `AGENTS.md` has explicit rules for irreversibility, no fabricated runs, independent evidence, scope labels and a welfare stop. These are necessary but not substitutes for executable CI, unique claim IDs across branches, reviewer independence or future randomness. New `docs/RESEARCH_SCOPE.md` is prospective only; it authorizes no valence, suffering, drive deprivation, self-preservation, real-world social engagement or production transfer.

## Decisions on open PRs

| PR | Review finding | Integration ruling / concrete next action |
| --- | --- | --- |
| [#56](https://github.com/kevindechang/MIND/pull/56) H013 matched-state fork | K11/C025 narrowly useful, C026 inconclusive. A triple cut is not proof of an independently necessary self-model path. | Keep draft; preserve records, run all gates on combined tree and prevent claim ID collisions. Strong transcript-based report rival still unresolved. |
| [#57](https://github.com/kevindechang/MIND/pull/57) H010 efference | C038 beats one estimator in `poltergeist/dev`; cannot beat a privileged reference filter. No autonomous choice of motor action. | Keep draft; strengthen matched belief-estimator comparator or narrow claim; evaluate held-out gusty/slippy and combined rival registry. |
| [#59](https://github.com/kevindechang/MIND/pull/59) H002 silent shift | Valuable REFUTED C042/C043 and INCONCLUSIVE C041, with alert scorer K13. | Must split `mind/claims.py` evaluator/metric change away from claim registration under the explicit separation rule. Reconcile overlapping `mind/rivals/__init__.py` with #57; preserve seals and failing records. |
| [#60](https://github.com/kevindechang/MIND/pull/60) H012 switch-retention | C060 held-out INCONCLUSIVE; no new multi-timescale mechanism. | Retain the negative record. Keep draft while re-generating STATUS and checking integrated validation. |
| [#61](https://github.com/kevindechang/MIND/pull/61) H014 gate/optimizer | C050 fixed-behaviour AdaGrad result holds; learned selection C051 fails simple strong controls. No demonstrated live-policy benefit. | Keep pending combined-tree result-code rechecks, replay tests, immutable record audit, and no misleading REPLICATED claims. |

Individual static review comments were posted on each PR. The API rejected a formal REQUEST_CHANGES on #59 because the reviewer account owns the PR; a substantive blocking comment was posted instead.

## Recovery and decision protocol

1. Establish a history-complete checkout in a working environment, without bypassing network or platform permissions. Pin main commit and confirm `python -m mind doctor` returns clean.
2. Run `python -m unittest discover -s tests` and `python -m mind check`; if necessary capture fresh `--record` and `--heldout --record` runs without altering sealed predictions. Commit **every** held-out record, including failures; re-generate `STATUS.md` using code, never by hand.
3. Integrate at most one result-code-changing PR per validation cycle; detect and resolve rival/registry conflicts; never squash/rebase a sealed claim. Verify K01, K06, K07 as applicable, plus new shadow/reporter/welfare gates.
4. Add true independent replication (different contributor with proven independent environment), a future-randomness-heldout design, and at least one unseen-task-family challenge before interpreting broad cognitive integration.
5. Keep new moral/social/appraisal work in **design only** until baseline parity, consent and anti-manipulation metrics, and welfare tripwire review are satisfied.

**Reviewer verdict:** research pipeline is operationally serious, scientific findings are meaningful but simulator-bounded, integration across PRs remains UNVERIFIED, functional consciousness NOT ACHIEVED. The safest immediate objective is a freshly validated, provenance-clean main before adding more organs.
