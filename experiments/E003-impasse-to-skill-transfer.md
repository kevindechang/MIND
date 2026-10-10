# E003 — Impasse-driven procedural learning after complete session reset

**Status:** PROPOSED / G0 OPEN / NOT PREREGISTERED / NOT IMPLEMENTED / NOT EXECUTED.
**Research origin:** R002 mechanism M3; H011. This is a **candidate future experiment**; not an existing LongMemEval-V2 executable benchmark.

## Question

Can an agent detect failed strategies, derive a verified reusable procedure and deploy that capability **on the first attempt** in structurally novel held-out worlds *after destroying its running context*, above equally resourced retrieval/reflection or simple rules?

## Candidate environment

A deterministic local sandbox featuring changing tool semantics, hidden preconditions and delayed asynchronous effects. Generate training and held-out worlds with shared latent failure structures but distinct names, layouts, tools, action sequences and surface text. Verify no secret oracle/test-generation parameters reach the agent.

## Candidate arms (not frozen)

A. Ordinary agent + episodic memory/retrieval.
B. Agent + explicit reflection and reusable natural-language instruction summaries, no executable compiled procedure.
C. Agent + impasse diagnosis + **sandbox-validated, versioned procedural rule or code module**, gated by test success.
D. C with learned procedure disabled or replaced by sham (causal test).
E. Strong hand-engineered recovery rule/model-based controller comparator.

Separate data construction, diagnostic/compilation compute and test-time decision budget, and report both total lifecycle cost and matched test budget. Generated procedures execute only in isolated allowlisted sandbox with resource limits and no credentials/network access. Require unit tests, rollback and human review before deployment outside the simulator.

## Measurable outcomes

- Held-out first-trial action success after hard process termination, context reset and state restoration exclusively from predeclared persisted stores.
- Verified trace showing whether a learned procedure causally executed.
- Structural transfer success across unrelated surface descriptions, error recovery, false-skill adoption, regression on older tasks, compute/runtime cost.
- Paired differences, uncertainty intervals, seeds, prerequisites for any claim of transfer, and no post-hoc threshold shopping.

Reject the strong 'compiler improves development' claim if ordinary summaries, retrieval, matched explicit reflection or simple rules reach comparable transfer, or if success relies on human engineering, oracle leakage or hidden transcript retention.

**Dependencies:** formal simulator, frozen models/budgets, independent preregistration, ethics/sandbox review. No numerical success claim is asserted.
