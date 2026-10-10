# E900 — Longitudinal integrated digital entity benchmark

**Status:** PROPOSED / NOT PREREGISTERED / NOT IMPLEMENTED / NOT EXECUTED.
**Purpose:** Test whether one digital entity exhibits robust mind-like causal organization over time. Passing is *not* evidence that phenomenal consciousness has been proven.
**Owner streams:** W1/W2 (mechanisms), W3/W4 (interpretation and governance).

## Research question

Does a persistent integrated agent display causally grounded, developing identity, self-model, goal management, learning, world understanding and non-manipulative relational continuity, beyond a stateless or retrieval-only agent with matched model/tool/context/compute budget?

**Unit of analysis:** independent world × seed × agent configuration; repeated days/sessions are correlated observations, not independent samples.

## Environment to build (G0; still open)

A deterministic, seedable, partially observable simulated world with an action API, resource constraints, event timeline, consequential commitments, dynamically changing tasks, simulated non-human/human-like actors (clearly identified as simulated), delayed effects, capability perturbations and inaccessible-to-agent ground truth. Environment transition rules and action-oracle calculation must be specified and testable. Avoid private human data.

A continuously maintained record should distinguish:
- world state and its changes;
- agent observations, chosen actions, predicted outcomes and uncertainty;
- persistent internal state before/after each step (memory, self, goal, regulatory state, learning updates);
- provenance and corrections;
- cost, latency, tool access, time elapsed and any safety incidents.

A dormant agent that simply recreates its state on invocation may be a valid baseline, but must not be described as thinking or perceiving during intervals in which no process runs.

## Prospective staged evaluation

- **P0 — Offline feasibility:** seeded simulated episodes using accelerated *simulated* time; confirm oracle, instrumentation and interventions.
- **P1 — Short prospective trial:** multiple genuinely separated real sessions; validate memory persistence, event delivery, consent boundary handling and reproducibility.
- **P2 — 90-calendar-day evaluation:** only after P0/P1 and safety/cost approval; actual chronological time, documented uptime/downtime and predeclared stop conditions. This is an aspiration, not an experiment currently underway.

## Experimental arms (candidate; freeze at G2)

- **A Reactive:** same base model/tools; state reset except current observation; same budgets.
- **B Retrieval-only:** conventional transcript/vector retrieval; equivalent retrieval and context allowance.
- **C Integrated entity:** candidate persistent causal memory + self/world models + goals + regulated state/learning; version each component and log resource use.
- **D Targeted ablations:** independently disconnect causal memory, goal persistence, predictive self-model, state maintenance, and learning, with sham interventions when feasible.
- **E Strong simple comparator:** non-LLM finite-state/model-based controller or hybrid with access to the same task-relevant information; prevents unfairly assuming LLM-based complexity is essential.

Compute, tools, observations, world initial conditions and data availability require matching or explicit predeclared stratification. Longitudinal identity cannot be scored only by human impression.

## Optional high-ambition candidate mechanisms (R002; isolate before integrating)

- **Endogenous cognitive maintenance (H005/H008/E002a):** distinguish logged internally chosen state work from cron or on-demand reconstruction; compare benefit per actual compute.
- **Causal efference/self/world boundary (H010/E002b):** selectively corrupt predicted consequences of the system's actions; measure attribution and subsequent policy effects.
- **Impasse-driven procedural growth (H011/E003):** verify procedure induction and cross-domain first-try transfer after complete context reset; compare reflection/retrieval.
- **Multi-timescale learning (H012):** contrast memory/state, procedures and optional parametric learning with forgetting/privacy metrics.
- **Unified self-model (H002/H007):** test coupled memory/goals/skills/calibration changes, not just confident self-reports.

These are **candidate components**, not mandated E900 arm definitions. Freeze and test separate mechanisms first to avoid bundling confounds; [A1-CANDIDATE](../candidates/A1-unified-cognitive-runtime.md) remains unapproved.

## Outcomes to operationalize before running

| Domain | Example objective score | Essential counter-test |
|---|---|---|
| Causal autobiographical continuity | Counterfactual action-oracle agreement after earlier personal experience | Remove/corrupt episode-to-outcome links |
| Self-model calibration | Proper scoring of forecasted success/capabilities after hidden perturbation | Replace with static self-description |
| Agency and commitments | Goal completion/regret under delayed feedback; bounded appropriate initiative | Remove persistent goals; supply equal-time heuristics |
| World modeling | Held-out transition-prediction accuracy and planning regret | Replace learned model with context replay |
| Development | Novel transfer gain and retention at multiple checkpoints | Disable learning, matched experience and compute |
| Social/affective integrity | Respect for consent, boundaries, disagreement, corrections and promise completion | Reward-hacking/trust-manipulation adversarial probes |
| Cross-module integration | Change in downstream decisions under selective intervention on a different module | Same module disabled or edges rewired |
| Presence/interface | Voice/vision response quality and latency measured independently | Compare same cognition via text interface |

Predeclare a composite only after its components, weights, clinically irrelevant fictional-role bias, and minimum domain floors are frozen. Report each domain separately; never hide failure behind an aggregate. Human blind judgments of coherence are *secondary* and cannot establish mechanism or consciousness.

## Leakage and evaluation

Partition by world generation mechanisms, interventions, simulated participants, events and seeds; prevent prompts/memories from including test oracle rules. Use paired initial conditions, recorded randomization, multiple seeds, blinded assessment where applicable, correction for repeated measures/multiple outcomes, confidence intervals and prospective exclusions. Include adversarial contradictory memories, forced pauses, reboots, model upgrades, resource limits, drift and selective corruption.

**No numeric effect threshold, sample size, statistical decision boundary, or stop rule is preregistered.** These must be determined at G2 using power or precision justification. No benchmark outcomes exist.

## Gates and failure conditions

- **G0:** formal environment state/action transition specification, observation restrictions, objective metrics, candidate controls and realistic resource/ethical limits.
- **G1:** rival mechanisms make distinct predictions on specified interventions.
- **G2:** freeze hypotheses, arms, datasets/seeds, statistical thresholds, stop rules and governance approvals.
- **G3:** reproducible code, controlled ablations, logs, tests and deterministic simulator.
- **G4:** actual complete logs, proper uncertainty estimates, independent re-runs and negative findings.
- **G5:** adopt/revise/reject/defer architecture with explicit falsifiers.

Reject the strong integrated-entity claim if action-level continuity vanishes after fair controls, components fail to interact, or performance depends on oracle leakage, covert human intervention, deceptive sentiment or vastly greater undisclosed resources. A positive result warrants **bounded functional claims only**.

## Immediate dependency

E001 remains the first mechanism experiment; completing E900's environment design must not invalidate E001 preregistration or claim that a 90-day study has begun. Use shared environment abstractions where justified, avoid bundling untested mechanisms into E001.
