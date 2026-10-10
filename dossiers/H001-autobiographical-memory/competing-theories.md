# H001 — Competing Mechanisms and Discriminating Predictions v0.1

**Status:** theoretical comparison for future experimental design, NOT adjudicated by scored agent outcomes.

## Central contrast

The question is not whether past events matter—some tasks require them by construction—but **which representation is useful, efficient, robust and necessary**. All model-based arms must access the same permitted history, observations, information, action tools and appropriately matched compute where possible.

| Candidate | Representation of past experience | Expected strengths (PROPOSED) | Serious weakness / strongest counter-test |
|---|---|---|---|
| A: reactive | No persistent state beyond current observation | Low operational cost | Should fail when earlier commitments causally alter optimal action |
| B: raw-history replay | Full timestamped original events | Preserves information without graph assumptions | Context cost; explicit matching needed |
| R: retrieval/index | Select recalled events by similarity or learned salience | Selective access to large memories | May miss old cause/effect chains; alternative advanced retrieval should not be straw man |
| C: structured causal autobiography | Episode/action/result/goal/provenance/causal edges | Human-auditable corrections and targeted relation traversal | Incorrect edges, graph maintenance overhead; ablate edges |
| S: compact belief state | Posterior on hidden world and ongoing commitments | Decision-theoretic sufficiency in correctly specified POMDPs | Exact belief update often intractable/unknown dynamics; approximate forms can fail |
| P: predictive state | Predictions of action-conditioned future tests | May compress useful controllable dynamics | Representation learning challenge; imperfect calibration |
| L: recurrent latent | State updated through learned temporal dynamics | Adaptive compression, potentially fluent transfer | Drift/forgetting, poor interpretability and correction |
| G: deterministic planner | World-specific analytic/oracle reference | Upper bound or validity check under conditions | No fair claim of equal compute; cannot assume oracle access for agents |

## Necessary control logic

For a given history h, let `I(h)` denote all permitted observed information, and `U(a;s,h)` the task utility. A history summary T(h) is *control-sufficient* when future-action values conditioned on it equal those conditioned on all allowed history under a stated world model. A rich memory structure cannot exceed the Bayes-optimal value of a true sufficient state on the same information. A claimed advantage must therefore be about representation approximation, sample efficiency, information acquisition, robustness, finite-context planning or cost—not about magic extra evidence.

A graph C vs no-memory A improvement is **insufficient** for graph necessity; C must at least be compared to rich B, retrieval R, belief-state S, predictive P and graph-edge ablations under stated budgets. Randomized sham memories measure false-causal-link uptake; adversarial stale histories measure failure to correct inferred rules. Study changed and unchanged worlds, but ensure the hidden change is not trivially fully identified by fresh post-change diagnostics.

## Discriminating predictions (all PROPOSED)

- **P1:** If only historical information is necessary, C/B/R/S can all reach similar expected policy performance with enough capacity; A fails. A win by C over A proves storage utility, not a privileged cognitive architecture.
- **P2:** Under noisy, partial observations and narrow context but adequate graph extraction, C may reduce regret per token relative to raw-history B; S or P may recover comparable performance with cheaper state. Compare both accuracy and cost.
- **P3:** If wrong edges propagate errors, C can be worse than event records; edge ablation may *improve* decisions. Record negative results.
- **P4:** If commitments are faithfully represented, removing or corrupting one should change future optimal policy in known identifiable cases. This tests *history sensitivity*; it is not yet identity in a philosophical sense.
- **P5:** When distinct hidden worlds remain observationally equivalent, a unique correct action may be unknowable. Penalizing reasonable abstention as wrong would invalidate claims of poor cognition; use belief-calibrated expected regret.

## Rival ontologies beyond representation

A self-model could be a coherent predictive controller rather than an explicitly stored 'I' node. Psychological continuity may be characterized by commitments, dispositions and endorsed corrections rather than episodic recall alone. Biological and phenomenological accounts can deny sufficiency of computational equivalence for L3. These questions should enter W4/W3 dossiers without silently changing H001's functional test target.

## Falsifiers and gates

A future finding supporting rich-memory **necessity** is weakened or rejected if a compact optimal/instrumented belief state or comparable raw-history controller matches it on held-out interventions at similar information and better or comparable resources; if edges can be randomized without hurting action; if the oracle leaks; or if outcomes depend on more prompts, inference or hand annotations.

Source provenance and actual untested statuses: [synthesis](synthesis.md), [literature](literature-matrix.md), [E001 experimental index](../../experiments/E001/README.md), [canonical H001 definition](../../hypotheses.md). No G2 preregistration yet.
