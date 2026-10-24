# H070 — Portable behavioral continuity across model backbones

**Status:** Stage 1 implementation on an isolated branch; MIND integration and empirical hypothesis NOT_EXECUTED. Related: [issue #70](https://github.com/kevindechang/MIND/issues/70), #50, #54, #40.

## Question

With target inference model B fixed, does cognitive state accumulated under model A improve first-action performance after A→B replacement against an equally informed, temporally versioned structured-memory+B rival? MIND's distinctive cognitive architecture must beat the strongest simple memory and belief-state controls, not merely no-memory or short-window controls.

## Architecture and constraints

The one shared `Organism` and hash-chained `genesis/tick/end/lesion` ledger remain the scientific substrate. Stage 1's `mind/portable_state.py` is a **read-only projection**, not an organ or a parallel model. A researcher may optionally put a strictly structured JSON `portable_event` string in an existing tick's `obs`, then call `project(ledger, subject)` to derive an inspectable subject-scoped snapshot.

The event vocabulary is `belief`, `correct`, `retract`, `commit`, `close`, `revoke_source`, and `forget`. Each event has a unique ID, subject and epoch. Belief revisions cite the exact previous current belief; source revocation invalidates active evidence and its correction descendants; all-person forgetting fences the previous epoch and blocks reuse of previously seen source IDs. Events are validated and bounded before projection, duplicate IDs are deduplicated, conflicting IDs are errors, and ledger verification is mandatory by default. No model is called, and the projector never changes policy or kernel state.

**Important:** `forget` and `revoke_source` here hide records in the *derived projection*. They **do not physically erase** the underlying append-only ledger or backed-up event data. This experimental prototype MUST NOT ingest real users' data or be presented as production deletion compliance. A production design needs separate authority-controlled deletion or cryptographic erasure, including caches, replicas, derived weights and exports. The current implementation is also O(number of historical events) per projection; snapshots/caching require separate validity tests.

Stage 1 accepts explicit events, not arbitrary language. It does not attribute LLM inferences as user assertions, determine permissions, learn neural representations, select actions, or preserve model parameters. A strong structured-memory baseline could implement the same semantics; this is intentional.

## Prospective comparison (not yet registered)

- **Treatment:** shared MIND organism with portable state and a model A→B adapter, with cognitive state causally influencing decisions.
- **Strongest rival:** same model B and task/environment inputs, complete source/revision/epoch-aware structured state without MIND cognitive arbitration.
- **Additional controls:** transcript retrieval+B, no-memory+B, A→A and B→B, mismatched-state negative control, frozen learned state, access cut at the state→policy path, equal-state simple belief controller.
- **Primary outcome:** persona-clustered paired difference in **correct first action after backbone swap** on never-seen synthetic task families; test before any feedback-assisted recovery.
- **Secondary outcomes:** correction/revocation handling, calibrated confidence, regret/recovery, token/call/latency/compute, replay bytes, and out-of-distribution task transfer.
- **Falsifier:** If equal-information structured memory or compact belief-state rivals tie or beat MIND, there is no demonstrated distinctive advantage. If action does not change under an appropriate matched-state access cut, the proposed causal influence is not established.

Register precise contrasts, scientific margin, confidence interval, multiplicity plan, task-family partitions and sample-size rationale **before any held-out evaluation**. Use commit-sealed future-beacon seeds. Never edit a prediction to fit results; retain negative results. L2 is an unachieved research objective, not proof of subjective experience.

## Ordered execution gates

1. **Stage 1, this branch:** code + unit tests for read-only provenance, correction, scoped erasure projection, deduplication and isolation. Local isolated-module tests: 13/13 pass on Python 3.13.5. No repository-wide tests or seal checks executed in this environment.
2. **Stage 1 acceptance:** checkout exact complete MIND history; run `python -m mind doctor`, `python -m unittest discover -s tests`, full `python -m mind check`, including an *actual* `MemoryLedger`/`Organism.restore` integration case; review privacy and load bounds. Only then consider merging this branch with a merge commit.
3. **Stage 2, dependency #50:** journal nondeterministic model outputs within each tick, support deterministic replay without re-calling the model, and preserve K01/K06/K07 under process death. Do not make paid model calls in this prerequisite.
4. **Stage 3:** extend **existing** world/rival/organ registries with synthetic multi-session model-swap tasks and a strong equal-information memory rival. Split instruments from claim registration. Conduct only dev exploration.
5. **Stage 4:** register prediction with frozen estimand, power and controls. Commit seal, generate future beacon held-out seeds and record first result. Run full historical/active claim checks and preserve all records.
6. **Stage 5:** genuine A→B and B→A neural-model evaluation only after owner approval of any paid API, data/compute budget and nondeterministic-output replay. Replicate on a different machine and with an independent contributor before promoting confidence.

## Current infrastructure restriction

A full Git-history checkout was not available in this conversation's container. `git ls-remote https://github.com/kevindechang/MIND.git HEAD` returned exit 128 with a DNS-resolution error. Connected GitHub reads/writes support a **draft branch**, but do not establish local `mind doctor` or combined-tree test success. Follow issue #54; do not try to recreate immutable Git history from an API snapshot.
