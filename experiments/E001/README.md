# E001 — Causal Autobiographical Memory: Experiment Record

**Scientific status:** G0 OPEN. E001 **NOT PREREGISTERED**, no scored AI agent trials, no E001 result supporting H001. New file layout is a *documentation index*, not a replacement for any existing experiment, code or version history.

## Two-stage reporting

- [Stage 1 draft preregistration](preregistration.md): hypotheses, controls, metrics, identifiability, planned samples, stop/decision rules. **Not frozen; no journal Registered Report claim.**
- [Methodology](methodology.md): concrete current environment instruments, actual logged deterministic checks and validity limitations.
- [Permitted-history oracle v0.1](E001-G0-permitted-history-oracle-v0.1.md): history-only Bayesian action reference, ambiguous/identifiable cases, exact arithmetic calibration, and outstanding G0 gaps; no scored agent trial.
- [Selective-probe version-space oracle v0.2 (3-node)](E001-G0-selective-probe-version-space-v0.2.md): finite 8-graph family, uniform prior, version-space posterior, history-only action sets with ambiguous/separating/pending/censored/deadline checks (14 unit tests PASS); G0 still OPEN, no scored agent trial.
- [Prior and informative-censoring robustness v0.3](E001-G0-prior-censoring-robustness-v0.3.md): counterexamples and local 20-test calibration of prior/censor-conditioned reference, **not yet tested against a byte-exact v0.2 checkout**; G0 remains OPEN.
- [Finite-horizon adaptive probe policy v0.4](E001-G0-policy-value-identifiability-v0.4.md): exact ex-ante acquisition reference, seven reachability classes among eight graphs, synthetic B2>B1 gain; standalone 12 tests and 128 differential checks; G0 OPEN.
- [Stage 2 results](results.md): currently contains only an accurate **NO AGENT TRIALS** status and references to previous simulator checks; append real agent data only with genuine run evidence.

## Existing provenance—do not move or overwrite

- [Original E001 proposal](../E001-causal-autobiographical-memory.md)
- [XOR Switchboard design](../E001-G0-transition-and-identification-v0.1.md) and [instrument validation](../E001-G0-instrument-validation-v0.2.md)
- [Causal Commitments v0.1](../E001-stage1-causal-commitments-v0.1.md)
- [Instrument Python source and unit tests](../instruments/)
- [Iterations 001–003](../../runs/) and [H001 dossier](../../dossiers/H001-autobiographical-memory/synthesis.md)
- [Canonical research state](../../research-state.md)

Every future experiment has a frozen design stage and separate results stage; moving a proposal into a results file does not demonstrate execution.
