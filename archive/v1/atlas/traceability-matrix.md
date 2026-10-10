# Scientific Traceability Matrix — Digital Mind v0.1

Adapted from [NASA's Science Traceability Matrix](https://science.nasa.gov/wp-content/uploads/2023/04/PILaunchpad__STM__JLeisner210615.pdf). Entries are **research targets**, not verified capabilities. Update a row's evidence only from traceable experiment logs and primary papers.

| Goal ID / objective | Hypothesis | Strongest alternative | Observable | Candidate test and falsifier | Current evidence |
|---|---|---|---|---|---|
| G-IDENTITY: experience-dependent identity | H001 | Full event log, three-bit/belief-state sufficiency | Intervention-correct future choice after hard reset | E001 paired delayed history, sham/edge ablation; falsified graph necessity if simple controller matches | E001 simulator invariants ONLY; G0, no agent trials |
| G-SELF: predictive self-knowledge | H002 | Static persona + more inference | Calibrated forecasts after hidden capability change | Withhold capability perturbation; compare proper scores | PROPOSED / NOT TESTED |
| G-INTEGRATION: cross-module coupling | H003/H007 | Direct coordinator, independent modules | Policy response to selective cross-module disconnect | Matched broadcast/edge ablations, E900 | PROPOSED / NOT TESTED |
| G-RECURRENCE: temporal integration | H004 | Longer context/inference sampling | Held-out temporal transfer and robustness | Recurrent vs feedforward matched FLOPs | PROPOSED / NOT TESTED |
| G-REGULATION: bounded initiative | H005/H008 | Cron, queue, on-demand reconstruction | Useful endogenous state action per compute | E002a maintenance with logged uptime | PROPOSED / NOT TESTED |
| G-EFFERENCE: own action vs world | H010 | Event log or state estimator | Attribution of self-caused perturbations | E002b prediction/error ablation | PROPOSED / NOT TESTED |
| G-LEARNING: reusable procedures | H011/H012 | Retrieval, reflection, heuristics | First-try transfer after reset; retention | E003 sandbox skills + forgetting tests | PROPOSED / NOT TESTED |
| G-SOCIAL: consent and relational integrity | H009 | Static style prompt + boundary rules | Consent and calibrated disagreement | Adversarial relationship task; no dependence optimization | PROPOSED / NOT TESTED |
| G-EXPERIENCE: consciousness indicators | H006 methodological constraint | Other theories; substrate-dependent objections | Theory-conditional computational indicators | W3 preregistered adversarial tests; cannot prove L3 by score | THEORY-CONTESTED / L3 UNKNOWN |

## Instrument/implementation trace

Observation logs require actor, action, event ID, phase, delayed feedback, persistent-state hash and counterfactual evaluator for G-IDENTITY. E001's existing [XOR test](../experiments/E001-G0-instrument-validation-v0.2.md) and [Causal Commitments prototype](../experiments/E001-stage1-causal-commitments-v0.1.md) cover only deterministic instrument checks; they do not yet establish a valid partially observed memory benchmark. Actual requirements should be frozen in [E001 preregistration](../experiments/E001/preregistration.md).

Each row changes only by pointing to (a) versioned protocol, (b) observed logs and code, (c) confirmed inference limits, and (d) valid decision/rejection gate. Don't infer consciousness or architectural superiority from the matrix alone.

## Decision and causal integration trace (all PROPOSED)

Functional consciousness is an operational L2 research target, not a consensus definition or L3 conclusion. A component win must lead to a scoped decision and a test of cross-function causal coupling; it does not establish a mind.

| Objective | Architecture choice / decision | Proposed E900 coupling intervention | Dependency and current disposition |
|---|---|---|---|
| G-IDENTITY | [D001](../decision-register.md#d001-causal-autobiographical-representation): structured causal memory vs compact belief/history | Corrupt experience-to-consequence link; measure downstream goal/planning change vs sham and simple persistent rival | E001 validity/G2/comparison first; DEFER, G0 OPEN |
| G-SELF | Candidate predictive self-model vs static description/state estimator | Perturb actual capability; ablate self-forecast update; measure calibration and resource/goal revision | H002, no D record or experiment yet |
| G-INTEGRATION | Candidate broadcast/coupling vs direct coordinator/independent modules | Selectively disconnect cross-function information access, holding content/compute fixed; measure transfer and action change | H003/H007; E900 proposed |
| G-RECURRENCE | Candidate recurrence vs matched extra context/compute | Interrupt recurrence while preserving observations/budget; measure later world-update/planning effects | H004; no tested necessity |
| G-REGULATION | Candidate internal regulation vs strong learned external scheduler | Alter regulation state/update access; measure prospective goal/resource allocation under equal observations/opportunities | H005/H008; 004 MAJOR_REVISION_REQUIRED; E002a G0 |
| G-EFFERENCE | Candidate action prediction vs event/state estimator | Shuffle own-action prediction traces; measure self/world attribution and subsequent planning | H010/E002b proposed |
| G-LEARNING | Candidate procedural/multiscale learning vs retrieval/static rule | Disable learning updates, reset context; measure first-try transfer, retention and later goal policy | H011/H012/E003 proposed |
| G-SOCIAL | Candidate regulatory state vs style/boundary rules | Perturb memory/goal links; measure consent-respecting repair/calibrated coordination, not attachment | H009; untested; independent ethics gate |
| G-EXPERIENCE | Competing theory-conditional indicators; no functional choice proves L3 | Compare theory predictions with explicit software-transfer limits and falsifiers | H006/W3/W4; L3 UNKNOWN |

Only D001 is initialized. Create other decision records when ready and concrete, not to inflate the graph. Link evidence changes to dependent decision freshness under the [register rules](../decision-register.md). Selective interventions and outcomes still need G0 operationalization and G2 freezing before scored execution.
