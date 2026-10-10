# E002 — Endogenous maintenance and causal self/world action attribution

**Status:** PROPOSED / G0 OPEN / NOT PREREGISTERED / NOT IMPLEMENTED / NOT EXECUTED.
**Research origin:** R002 mechanisms M1+M2; H005, H008 and H010. This is a **candidate future experiment**; E001 remains active first.

## The two questions (do not confound)

**E002a — Maintenance:** When an agent is not prompted, does internally prioritized cognitive maintenance improve *later objective decisions* more than equal-budget fixed scheduling, heuristic prioritization, or on-demand reconstruction?

**E002b — Efference:** Does an explicit predictive record of the agent's own actions and their expected state changes improve discrimination between self-induced and externally induced environmental changes?

Measure them separately before any factorial integration.

## Minimal simulator sketch (G0 needs formalization)

A seeded partially observable world with bounded computation allowance, changing tasks, action efficacy, delayed consequences, injected disturbances and a prospective goal/action oracle. Record at each step observations, available budget, agent internal state and generated proposals, chosen action, predicted state delta, actually observed delta, provenance and wall-clock activity.

### E002a candidate arms

A. No idle processing; reconstruct state only on next interaction.
B. Fixed periodic maintenance (script/cron), with equal compute and state access.
C. Tuned deterministic priority queue based on uncertainty/expiry, equal compute.
D. Candidate internally prioritized maintenance controller.
E. D with regulatory/state variables shuffled or ablated.

**Outcome candidates:** downstream oracle decision quality, changed-model calibration, missed-commitment rate, unnecessary compute/action cost, stale-claim uptake. A prose explanation of what the system 'thought about' during downtime does not count. Log **actual** activity, no retroactive reconstruction disguised as uptime.

### E002b candidate arms

A. Action/event trace + standard inference, no dedicated self-action prediction.
B. Explicit expected-action effect/efference record.
C. B with shuffled or delayed action prediction/receipt (negative control).
D. Simpler state-estimation/filtering comparator with matched observations.

**Outcome candidates:** self/exogenous cause attribution accuracy on held-out transition mechanisms; forecast log loss/Brier score; adaptation after hidden tool impairment and disturbance. Check whether extra information, not representation, explains a result.

## Before a scored trial

Freeze environment equations and oracle, agent information access, paired randomization, sample/seed justification, exact budgets, outcome direction/effect floor, multiplicity correction, confidence interval procedure, exclusions, stop rules and ethics. Run unit/smoke tests separately. E002 does not establish a subjective self or phenomenal consciousness.
