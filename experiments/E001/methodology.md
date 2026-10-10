# E001 — Methodology and Test Integrity Record

**Status:** G0 instrument prototypes exist; no preregistered scored agent evaluation.

## Current deterministic instruments

**XOR Causal Switchboard** ([source](../instruments/e001_switchboard.py), [tests](../instruments/test_e001_switchboard.py)): seeded three-bit contextual hidden rule; diagnostic action/reward reconstruction; one-/two-step tagged feedback delay; phase transition without pending queue; oracle reconstruction. Previous local observations: 7 tests passed, 768 single-phase + 64 two-phase enumerated cases reconstructed hidden rules. See [iteration 002](../../runs/2026-10-10-iteration-002.md), not independent replication.

**Causal Commitments** ([source](../instruments/causal_commitments.py), [tests](../instruments/test_causal_commitments.py)): seedable DAG action-effect masks, out-of-order delayed feedback with event IDs, four commitments with penalties, simulated process-phase change and selecting up to two interventions. In [iteration 003](../../runs/2026-10-10-iteration-003.md), the local report records 10/10 tests, oracle parity across 100 seeded worlds, and optimal action changed after last commitment deletion in 419/1000 synthetic paired cases. No LLM was an experimental subject.

## Why these are calibration-only

Both fully expose a sufficient statistic in their diagnostic observations: three action target bits for XOR; seven action-effect masks plus commitments for DAG world. A simple exact solver should be capable of optimal action from these without a causal narrative. This is useful for instrumentation and evidence pairing but **not diagnostic of whether an autobiographical graph is beneficial or necessary**.

The DAG generator is a causal world by construction, but real causal identification under confounding is not tested. Delays are simulator steps, not autonomous real-time persistence. No approved model selection, model inference logs, stochastic probe observation protocol, held-out mechanism-family benchmark or external replicator was used.

## Required next methodology

- Design selective probes, noisy/delayed observations, possible confounding, and observation-consistent belief worlds.
- Provide evaluator-defined outcome metrics that do not assume hidden truth is known by the policy.
- Specify independent model resets, persistent-state serialization and zero leakage of privileged oracles.
- Implement comprehensive raw-history, retrieval, compact belief-state, predictive-state, graph, sham and ablation agents under matched budgets.
- Preregister seeds, evaluation population, thresholds, analysis, stopping/exclusion rules and compute before any scored runs.
- Log exact commands, package versions, input checksums, seeds, outputs, artifact SHA and costs; stratify uncontrolled resource differences.

These are **prospective engineering requirements**, not completed steps. See [draft Stage 1 protocol](preregistration.md).
