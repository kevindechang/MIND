# E001 — Causal autobiographical memory under counterfactual intervention

**Status:** PROPOSED / NOT PREREGISTERED / NOT IMPLEMENTED / NOT EXECUTED. **Hypothesis:** H001. **Gate:** G0 OPEN; G1 comparator design drafted; G2 pending.

**Iteration 001 (2026-10-10):** [Formal G0 causal-switchboard and identification instrument v0.1](E001-G0-transition-and-identification-v0.1.md) defines a two-phase seeded transition, closed-form action oracle, context reset, changed/unchanged interventions and strong raw-log, sham, ablation and three-bit sufficient-statistic comparators. This is a deliberately falsifiable toy instrument, **not** a validated benchmark or a result.

**Iteration 002 (2026-10-10, manual):** [Exhaustive simulator/oracle validation v0.2](E001-G0-instrument-validation-v0.2.md) with [instrument code](instruments/e001_switchboard.py) and tests. **7/7 local tests and 832 exhaustive cases passed; no AI model was evaluated.** The XOR toy is now classified as *calibration-only* because the three observations are a sufficient statistic. Rich graph memory cannot gain information over a three-bit baseline on this task. G0 remains OPEN.

## Question

Does an agent preserve and use a causal narrative of its own past actions in choosing plans across sessions, above what can be explained by retrieval, context length, or generic chain-of-thought?

## Environment design (to specify before running)

A reproducible partially observable sequential world containing personal commitments, hidden skill constraints, evolving relationships with non-human simulated entities, delayed outcomes and conflicting goals. Episodic observations include what the agent tried, expected, observed, inferred and later corrected. Make future policy choices depend on the *causal interpretation* of an earlier episode, not verbatim fact recall.

## Preplanned arms

A: same foundation model, working context and tool affordances; no long-term memory.
B: same model/budget; ordinary vector retrieval or condensed transcript memory.
C: same model/budget; structured event + action + consequence + provenance + counterfactual memory, with update/correction protocol.
D: same as C but episode-to-outcome links randomized (sham-memory negative control).
E: same as C but causal episode edges selectively ablated; measure dose response.

## Controls and tests

- Match token, compute and retrieval costs, or stratify by measured cost in a predeclared analysis.
- Split environments by underlying transition mechanism, not only episode text; prevent long-session transcript leakage and prompt contamination.
- Hidden interventions change the consequences of familiar actions across sessions.
- Blinded rubric: whether plans select the causal intervention, not whether the model mentions a memory.
- Predefine randomization, seed count, environment instances, evaluation horizon, multiple-testing correction, and exclusion criteria before collecting results.

## Primary outcome candidate

Counterfactual action success: fraction of held-out episodes where the chosen action changes in the *correct causal direction* following a hidden intervention with delayed feedback. Secondary: calibrated predictions, error recovery, regret, false-memory uptake, continuity of declared goals, resource costs.

**Quantitative thresholds: TO BE PREREGISTERED.** No numeric outcome, confidence interval or effect is yet available. Passing E001 would support a functional mechanism under that benchmark only — never prove subjective experience.

## Relationship to the digital entity north star

This is a **mechanism-level** experiment for L2 causal identity, not the longitudinal whole-entity benchmark E900. E001 should show whether an agent's personal causal history changes its future decisions, *not* whether its voice/persona seems human or whether it has consciousness. Its future environment primitives may be reused for E900 after preregistration, but other cognitive/social mechanisms must not be silently bundled into E001 arms.

## Prioritized next work

1. Write an unambiguous state-transition model and an annotation-independent action oracle.
2. Specify all agent prompts/tools/memory budgets, model version and random-seed handling.
3. Preregister an effect size, confidence-interval method, sample design and stopping threshold.
4. Implement environment and baseline harness in a disposable branch.
5. Run smoke tests, then confirm a frozen protocol before any scored trials.
