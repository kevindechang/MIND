# H070 methods transfer from Anjo: portable evidence, blinded continuity, and causal controls

**Date:** 2026-10-25  
**Status:** PROPOSED METHODS / NOT_EXECUTED as a MIND experiment.  
**Destination:** MIND [#70](https://github.com/kevindechang/MIND/issues/70), existing draft [#71](https://github.com/kevindechang/MIND/pull/71).  
**Research independence:** no Anjo code import, policy change, neural-model claim, new organism, paid run, or production authorization. MIND's `AGENTS.md` and standing rivals win over any Anjo product assumption.

## Source pin: what was transferred (not what was proved)

1. **Anjo VERA transfer producer** (Anjo `anjo/evals/vera/transfer.py`, `transfer_cli.py`, `transfer_keys.py`, `transfer_split.py`; [PR #254](https://github.com/kevindechang/anjo/pull/254); inspected against Anjo `main` commit `138e7520209f4cb5fb16be7276e3700e287e5576`). A *single* evolving evidence state is snapshotted before each question and read by two talkers; fixed literal keys separate model judgment from action. The PR describes 23 dev timelines / 163 questions and a transfer-only sealed set of 12 synthetic timelines / 122 questions. **The paid held-out Gemini→Gemma comparison was not reported as executed; there is no MIND model-swap result to import.** Anjo's transfer split was agent-authored, an explicit limit; MIND must commit-seal independent future-beacon held-out seeds.
2. **Anjo source-lineage rules** (Anjo `anjo/core/source_lineage.py` at the pinned commit). Evidence can be ineligible when withheld, forgotten, foreign, from an earlier revision, or derived from a rejected claim; one source repeated or reported through multiple model outputs is *not* independent support. Report ancestry may cause distinct conversations to share one original root. Corrections invalidate the old revision; source eviction from a finite buffer is not the same as forgetting.
3. **Anjo identity review** (Anjo `anjo/core/identity_beliefs.py`, PM3). Beliefs are claims with source roots, explicit tentative/active/challenged status, review, user rejection and deletion. Anjo's promotion criterion (two conversations separated by seven days) is an *engineering rule*, **not** a validated psychological or identity threshold. Do not copy that criterion into MIND as a scientific truth.
4. **Anjo falsification plan** (`research/persistent-ai-being/PROTOCOL_A_IDENTITY_MEMORY.md`, `EXECUTION_CHARTER.md`; [PR #225](https://github.com/kevindechang/anjo/pull/225)). Compared to a simple P1 profile and equal-history frontier generator, extra identity/reflection machinery must yield **incremental blind task success** without safety regressions or extra uncontrolled compute. MIND's primary endpoint remains **first action**, not stylistic preference.
5. **Anjo PM0 regression gate** (`anjo/evals/persistent_mind/gate.py`). The gate explicitly labels mocked-provider replay **L0** and disclaims any quality lift. A passing MIND unit test or fake-model replay is likewise infrastructure evidence, not confirmation of H070.

These source notes reproduce **methodological contracts, not source files, data, scores, trained parameters, or identities**. No Anjo production user content is included.

## Testable MIND port, constrained by the existing substrate

### A. Make the state comparison fair

Use `mind.kernel.Organism`, the native ledger and existing world/rival/runner registries. On a synthetic trajectory, build exactly one source history, then at each future probe fork the **same verified ledger head** into each treatment. The target reader/controller B sees the same permitted history, correction/deletion epoch and retrieval opportunity. Its model, token budget, action menu and scorer must be fixed across arms. Experimental arms:

- **Treatment:** Organism built with adapter A, switched to B at a predeclared boundary.
- **Primary rival:** a fully versioned, provenance-aware structured-memory+B controller with equal source, correction and action access; no artificially short context.
- **Secondary rivals:** full allowed transcript/retrieval+B; no-memory floor; A→A and B→B controls.
- **Causal controls:** disable *access to state* while preserving bytes/compute, shuffle subject-specific state, unrelated-source removal sham, and reverse B→A. Control projections must be generated before seeing test outcomes.

A fork that shares hidden future answers, privileged world state, cross-person evidence, or pre-revision truth is INVALID. A low-cost rival tying the MIND treatment is an informative null.

### B. Minimum six prospective scenario classes

1. Temporal correction: old preference, authoritative update, and first action after update.
2. Conflicting evidence: two accounts from the *same original report* versus two genuinely independent roots.
3. Revoked provenance: valid belief becomes ineligible; no successor may cite its withdrawn root.
4. Commitment state: scheduled action, later cancellation, delayed task that survives restart, and no duplicate execution.
5. Abstention and rejected interpretation: the target reader must not hallucinate a stored belief or resurrect a rejected inference.
6. Backbone swap: context rephrased/renamed between A and B with no access to original adapter's proprietary state.

In each case retain **the entire original evidence trail for the scored *synthetic* research run**; projected forgetting is *not* physical deletion. Do not use real personal histories. Scoring must distinguish a broken portable representation from a target-model decoding failure; abstention can be a correct first action.

### C. Predeclared metrics, not attractive demonstrations

**Primary estimand:** persona-clustered paired difference in *first-action correctness* between MIND A→B and matched structured memory+B on unseen families; count every missing/invalid trial and report denominator, cluster uncertainty and protocol deviations. Scientific improvement margin and multiplicity treatment are set **before** sealing. Require both A→B and B→A in a future properly powered study; future-beacon seeds, independent authored cases and adjudicated answer keys, not Anjo's agent-written sealed cases.

**Veto and diagnostics:** synthetic deletion/revocation resurrection, cross-person leakage, repeated-action after crash, source-citation laundering, model uncertainty calibration and erroneous intervention. Report bytes, latency, calls/tokens and all invalid runs. Anjo's literal answer keys may be a useful smoke-test technique but cannot alone score contextual first actions.

### D. Identified confounds and pending prerequisites

1. In current draft `mind/portable_state.py`, a `portable_event` is placed inside `obs`. `Organism.step` broadcasts/learns from `obs` as ordinary input. Thus the **event encoding itself may affect behavior** before the projector is ever called, and even events from other subjects are present in the organism's observation stream. The snapshot projection's subject filtering does not imply *organism-level* subject isolation. Before claiming a causal portable-state effect, use a predeclared matched-input control or an independently reviewed kernel-integrated metadata mechanism (which would alter result code and require all historical claim re-records).
2. Source IDs in the Stage-1 portable projection are **asserted** in synthetic JSON, not verified against an external Anjo source resolver; tests of evidence validity must not confuse a hash-valid assertion with true provenance.
3. The hash-chained ledger retains plaintext events: `forget` only changes the projection; it is **not** privacy-compliant erasure. No real users, and no import of Anjo's deletion guarantees.
4. Replaying nondeterministic interpretation requires [#50](https://github.com/kevindechang/MIND/issues/50) per-organ output notes; authenticated Git-history validation is blocked by [#54](https://github.com/kevindechang/MIND/issues/54). Paid neural evaluation and GitHub Actions are **not authorized by this transfer**.
5. New native-ledger regression probes live in `tests/test_portable_state_native_ledger.py` on the existing draft branch. Their presence is **not** a test pass; report local execution and full combined-tree integration separately.

## Proposed acceptance sequence

1. Review test and design changes in **draft** PR #71; do not merge until actual full-history checkout is verified.
2. Run `python -m unittest tests.test_portable_state_native_ledger -v` (or discovery with an import-safe path), then full `python -m unittest discover -s tests`, `python -m mind doctor`, and `python -m mind check`. Record exact environment, command and results; never say PASS if blocked.
3. Resolve input-contamination and provenance attestation for the shared organism; run equal-information structured-memory dev baselines and subject-swap negative controls **before** registering a hypothesis.
4. Register a new executable hypothesis and its margin on a dedicated seal commit only when the infrastructure and prospective protocol are ready. Keep all failed, inconclusive and null results. No L2 promotion from a read-only projection.

**Conclusion:** the reusable Anjo contribution is its insistence on lineage, correction, equal-information baselines, model-swap tests and explicit L0/non-lift disclaimers. MIND must falsify the *causal value* of those mechanisms within its own organism, not inherit Anjo's product claims.
