# E001 — Stage 1 Prospective Protocol (DRAFT, NOT FROZEN)

**Registration status:** NOT PREREGISTERED; G0 OPEN. This document is an internal *draft*, not a journal peer-reviewed Registered Report or a commitment that any study has begun. Before each scored test, create a separately versioned, timestamped, frozen protocol and preserve this revision history.

## Question and scope

Does an experience-linked causal autobiographical representation produce lower future-action regret across true session resets than conventional retrieval, complete event histories and *the best feasible compact belief/predictive-state policy* when evidence, resources and tools are controlled?

## Main hypothesis and strongest counter-hypothesis

H001 candidate: Graph-like causal autobiography (C) offers improved adaptation, correction or decision efficiency under held-out changes. Rival: compact, sufficient-state or direct event-history algorithms preserve all useful evidence and can do as well as or better than C; complex causal edges introduce error and cost. This rival is explicitly allowed to win.

## Proposed comparisons (not implemented or assigned yet)

- A reactive/no durable state (information-deprived floor).
- B complete timestamped raw event history; same relevant observational evidence.
- R matched retrieval or memory-selection architecture.
- C structured action, consequence, goal, provenance and causal links, correction protocol.
- D internally consistent sham causal links/outcomes (negative control).
- E selective causal edge ablation, ideally graded corruption.
- S approximate/control-sufficient belief-state; P predictive state; F analytic privileged solver for instrument validation only (NOT FLOP-matched).

## World and information conditions (unresolved)

A seedable, partially observable sequential world must include bounded probes, delayed action-to-outcome feedback, multiple commitments, hidden transitions and optional nonstationary interventions. Each independent world has private simulator truth and a public observation history. Explicitly identify when multiple worlds are observationally indistinguishable; a hidden-world-optimal action must **not** be used as the unique agent score under such ambiguity without preregistered prior, expected utility or robust feasible-action criteria. Real model process reset must be separately instrumented; changing a simulator phase alone is insufficient.

Training, dev, and held-out *mechanism families* must be separated; prevent leakage from generated aliases and prior trials. The prior complete-diagnostics graph workshop is an instrument validity baseline, not a decisive benchmark.

## Outcomes and statistical design (all UNFROZEN)

Primary candidate: mean paired per-world regret, normalized to observable-history Bayes-optimal expected policy. Secondary: choice switching after intervention, calibration/abstention, causal credit assignment, stale/false-memory uptake, episode repair, total lifecycle token/FLOPs/latency and tool calls, sample efficiency, cross-family transfer, forgetting.

**Still required before G2:** model/checkpoint and decoding parameters; prompt templates; allowed memory serialization; retrieval budget; exact intervention generator; independent world cluster count and paired seeds; power/precision simulation; effect size of practical importance; CI estimator and multiplicity correction; stop/exclusion criteria; ethical permission for any human-like simulation; budget and cost ceilings. The older proposed +10 percentage point threshold from E001 v0.1 is **NOT preregistered**.

## Interpretation and decision rubric

A C>A difference may show *historical information is useful* but never graph necessity. An asserted C superiority requires C vs B/R/S/P under matched observation and reported cost, plus damage under targeted causal ablation, independent held-out mechanisms and uncertainty bounds. If S/P or B match or outperform C at equal resources, reject necessity of a richer representation on the tested family. Invalid oracle, leaked test data or confounded budgets invalidate score claims. Unexpected effects must be exploratory amendments; never edit a frozen hypothesis retroactively.

## Gates

G0: open environment, metrics, population, oracle-identifiability details. G1: at least two distinct mutually discriminating predictions. G2: freeze protocol before scored trials. G3: implement with smoke tests. G4: execute logged controlled trials. G5: revise architectural conclusions. All latter gates are presently pending. [Current E001 result status](results.md) remains NO AGENT TRIALS.
