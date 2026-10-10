# W2 — Endogenous Maintenance, Metareasoning, and the Illusion of Continuous Cognition
**Living dossier v0.1 | 2026-10-10 | W2/H005/H008/E002a | Targeted theory and instrument investigation.**
**Status:** SEED / prospective research; NO MODEL-AGENT TRIALS, no continuously operating mind. Review mode: SELF-REVIEW_ONLY. The research is an investigation of mechanism identifiability, not a claim about L3 consciousness.

## Abstract — a negative identification result with practical consequences

The Digital Mind project proposes that an enduring entity might maintain internal state, deliberate, anticipate deadlines, and choose useful cognitive work between direct conversations. But a system that periodically wakes, updates a queue, and later reports coherent concerns can appear to have done all of these things. The research question is not whether unsupervised processing can be useful; it can, in ordinary planning and metareasoning. The harder question is whether behavioral outcomes and maintenance timestamps *identify the claimed internal causal organization* and whether continuous endogenous processes outperform much simpler trigger and state-reconstruction policies at matched resources.

We derive a fundamental **observational equivalence warning**: if evaluation observes only public inputs, downstream external actions and serialized state at finitely many checkpoints, a sufficiently capable event-driven scheduler can implement the same observable input-output map as any candidate autonomous maintenance controller, provided it has equivalent observations, compute opportunities, and state. Thus performance at those checkpoints cannot establish that 'ongoing thought' is a distinct intrinsic mechanism. This is a theoretical constructive argument, not an impossibility theorem for all physical models of minds: additional measurements of internal dynamics, causal interventions, sub-cycle timing, resource consumption, or substrate constraints can break equivalence. A digital agent may genuinely maintain state, but that must be demonstrated by instrumented causal dynamics, not by a story or simply elapsed calendar time.

An executable one-slot synthetic maintenance-selection instrument is checked as a technical aid. It shows how a value-of-computation controller can differ from a fixed schedule or earliest-deadline policy, and how incorrect gain estimates can make it worse. These are design sanity checks, not evidence of endogenous cognition or a model benchmark.

## 1. What constitutes 'internal cognition' operationally?

Distinguish five levels often conflated:

1. **Narrated thinking:** a model says it was pondering something; in absence of traces this is a report, not proof that a computation occurred.
2. **Scheduled maintenance:** a time trigger or external controller invokes code to re-evaluate stored state; real computation occurs, but its timing may be fixed by a clock.
3. **Event-driven maintenance:** new information, uncertainty, expiration or policy thresholds trigger bounded computation; state and controller can be adaptive without being sentient.
4. **Endogenously prioritized metareasoning:** the controller itself chooses what internal computation to perform, on the basis of internal estimates and expected downstream consequences. This is a *functional* criterion; implementation could be a simple scheduler running a value-of-computation algorithm.
5. **Phenomenal ongoing experience:** a distinct L3 claim with no accepted computational proof criterion. Nothing in 1–4 entails it.

For E002a the constructive target is 4 compared against 2–3, *not* uninterrupted continuous activity. Log an actual monotonic timeline of task arrivals, state updates, compute decisions and externally consequential outcomes, including downtime. Identify the controller and opportunity to act: a deferred function call is still a function call. We should not call periodic ChatGPT task execution a continuous mind.

## 2. Formal observational equivalence and what intervention breaks it

Let a controller C map permitted history h_t and internal state m_t into a next maintenance decision d_t, state update m_{t+1}, and externally visible later action a_{t+1}. Suppose only O={external actions, serialized states at observation times, public timestamps} is measured, and an alternative scheduler S has the same observations, state, and computational opportunity at those times. Construct S to evaluate the same transition policy C when awakened, then write the same state and action. By induction over the observation times, if initial states and input histories agree and transition choices agree, O_S = O_C.

This establishes **non-identification from the limited observation channel**, not necessarily identical implementation costs or hidden fine-grained trajectories. If real continuous dynamics affect a later output through events unavailable to S, or if C performs calculations at intervening time points S cannot access, equivalence assumptions fail. Therefore a decisive protocol must control *observability and compute opportunities*, not present a fixed cron task as a deliberately weak foil.

A proposed causal test intervenes on internal maintenance opportunities with external observations held constant (e.g. selectively block the agent's maintenance action, corrupt its internal model, or replace a deliberation outcome with an old checkpoint) and measures downstream regret. The stronger rival runs the same adaptive planner via an external event scheduler. If both respond equivalently, the agent's 'endogenous' label has no demonstrated functional explanatory advantage on the tested measure.

## 3. Utility of computing versus appearing busy

A maintenance computation is worthwhile only if its expected improvement in a later external decision is worth its time/resource cost. For an idealized one-step choice j under information state I, define

`VOC(j | I) = E[max_a E[U(a) | I, result(j)]] - max_a E[U(a) | I] - cost(j)`.

This is a theoretical metareasoning objective, not an operational consciousness indicator. When computation is costly, waiting or skipping may be optimal. The formula depends on a valid generative model of what the computation reveals; an incorrect estimate of expected benefit can make active maintenance worse than a simpler priority rule.

[S013 Russell & Wefald (1991)](https://doi.org/10.1016/0004-3702(91)90015-C) grounds resource-bounded computation choices in their expected effect on external decisions, rather than 'thinking time' itself. [S014 Hay et al. (2012)](https://proceedings.mlr.press/r10/hay12a.html) develops a metalevel framework for selecting computations, highlighting that intuitively plausible heuristics need not be optimal; its conclusions are not a laboratory result for our agents. [S015 Sutton (1991)](https://doi.org/10.1145/122344.122377) describes Dyna's model-based incremental planning, a practical reminder that learning/planning can occur without human-like self-presentation. These sources were inspected from primary publisher proceedings/abstract pages in this run, **not through a complete line-by-line examination of all paper methods**.

The relevant counterargument to H008 is stronger than 'cron cannot think': *a well-engineered event-driven policy can select computations using exactly the same expected-value criterion*. H008 requires extra discriminating claims about state-coupling, world-grounding or efficiency that survive this comparator.

## 4. Existing E002a research proposal and its confounders

The [E002 proposal](../../experiments/E002-endogenous-regulation-and-efference.md) already contains no-idle/on-demand, fixed periodic, deterministic priority queue, internally prioritized maintenance and regulatory-state ablation arms. We must not silently add an A1-style mind module simply because a term like allostasis sounds biologically plausible.

A rigorous task world would have commitments with expiries, hidden environmental transitions, predictable/uncertain costs of missing each update, drift of cached predictions, and limited opportunities for computation. If each condition receives a different *amount* of inference or a different source of information, a performance difference cannot be assigned to the controller architecture. If the adaptive policy is allowed a privileged oracle of realized future gain, its victory is engineered and scientifically uninformative.

The stronger comparison is:
- A: no pre-interaction processing; update only on request.
- B: periodic trigger, matched maximum execution opportunities and compute tokens.
- C: deterministic priority queue with task value/deadline forecasts.
- D: externally triggered **adaptive value-of-computation** scheduler sharing the candidate's observable information and computation opportunities.
- E: self-prioritized controller with declared internal state and model forecasts.
- F: E with regulatory state shuffled/ablated (negative control).
- G: idealized evaluator upper bound whose privileged information is *never* given to E/D, labeled non-budget-matched.

Only E vs D and targeted regulatory-state interventions potentially identify a special benefit beyond rational maintenance selection. E vs A or B demonstrates that working between prompts can be useful, not that the system possesses endogenous cognition.

## 5. Executed calibration microinstrument (not an agent trial)

Added [e002a_maintenance_selection.py](../../experiments/instruments/e002a_maintenance_selection.py) and [tests](../../experiments/instruments/test_e002a_maintenance_selection.py). Its synthetic tasks have an index, a deadline, an estimated incremental gain and an evaluator-only misspecification factor. Each policy gets **one optional compute slot**; fixed-index, earliest-deadline and estimated-gain selection see the same published task descriptions. The evaluator computes a stylized expected incremental utility. The script executes no simulated passage of real time, no LLM inference, no stochastic social environment and no independent review.

**Locally observed 2026-10-10 (Python 3.13.5):** first a test import failed with ModuleNotFoundError (expected TDD RED); after implementation, `python -m unittest -v` passed **10/10** checks and `python e002a_maintenance_selection.py` printed illustrative expected values -0.03, 0.3 and 2.4 for fixed, earliest-deadline and estimated-value selection in its one demonstration. A second adversarial case confirms that incorrect estimates can reverse the ranking. These are code/fixture validity checks: the value policy is designed to pick the largest estimated gain, so outperforming simple baselines on a hand-authored favorable example cannot count as independent empirical confirmation of H008.

Critical weakness: `estimated_gain * actual_ratio` is an ad hoc synthetic evaluator proxy and does not represent a model actually improving through computation. Some policies commit one slot despite negative payoff and a skip policy may trivially win. There is no learning, no exploration, no independent sessions, no calibration of estimated utility and no model under test. Treat the code as **calibration-only** and falsify the toy's identifiability as a proxy for an endogenous mind.

## 6. Protocol design next and expected falsifier

A revised E002a G0 must instrument decision windows, strict computational budgets, output equivalence and state dependence. Introduce paired worlds where identical arrival schedules differ in predicted marginal value of maintenance, and matched worlds where internal state is selectively perturbed. A value-based controller should increase outcome quality **per unit compute** only under adequate forecast calibration. If a transparent externally scheduled value estimator achieves the same regret/cost and response to interventions, claim no incremental functional necessity for a special endogenous maintenance architecture in those conditions. If a candidate beats it, check whether internal observations, inference cycles, stored state and adversarial model class remained matched.

Measurement candidates: realized intervention-adjusted regret across independent worlds, resource-adjusted regret, calibration error of predicted maintenance gain, missed commitments, false stale state updates, amount of compute during actual idle intervals, errors under manual checkpoint cancellation, and recovery after genuine process pause/restart. All numerical thresholds, model parameters, sample sizes, seeds, confidence intervals, stop rules and P-values are **NOT preregistered**.

## 7. Broader philosophical and architectural implications

The computer-science notion of **endogenous scheduling** concerns what selects an internal computation, not automatically what experiences it. Higher-order, global workspace, active inference and recurrent models may generate distinct internal dynamics, but their presence cannot be inferred from the fact that a daemon ran periodically. Temporal self-continuity requires tested causal links between internal state, old commitments, future behavior and corrections, not continuous network activity as a marketing claim.

For an on-device Anjo-like system, this favors a disciplined engineering null hypothesis: begin with event-driven bounded state maintenance and only add an always-active cognitive loop if evidence shows benefits that strong triggered, stateful policies cannot reproduce. This is an **architectural decision rule**, not an adoption or rejection of the existing A1 candidate. Safety, user privacy, consent and resource caps remain independent.

## Findings and exact next action

- **THEORETICAL:** checkpoint-level observations alone cannot distinguish two implementations producing identical state/action trajectories under identical information, policy and execution opportunities. This is conditional equivalence, not a consciousness theorem.
- **PAPER-REPORTED:** metareasoning and Dyna provide non-anthropomorphic computational rivals (S013–S015); not replicated on Digital Mind.
- **OBSERVED:** 10 local microinstrument tests pass; no agent performance result; no authentic 40-minute scheduled task verified.
- **DECISION:** Keep H005/H008 **CANDIDATE**, E002a **G0 OPEN** and A0/A1 unselected.
- **NEXT:** produce a test-ready, partially observable E002a environment with two genuinely budget-matched active controllers (external adaptive scheduler vs internal self-prioritizer) and a preregistered intervention on internal state. Do not score AI systems until G2.

## Revision history

2026-10-10 v0.1: W2 non-W1 anti-starvation iteration 004, direct primary abstract/proceedings metadata checks and deterministic one-slot instrument TDD; not a systematic literature review; SELF-REVIEW_ONLY.

### Verification refinement (2026-10-10)

The initially observed test import error was **not** a valid assertion-level TDD RED under Superpowers' strict protocol; it only established that the module did not exist. To check real fault sensitivity after implementation, we temporarily replaced the low-value abstention branch with a deliberately incorrect unconditional selection: `python -m unittest test_e002a_maintenance_selection.SelectionTests.test_no_compute_when_every_gain_below_cost -v` produced **FAIL** with `AssertionError: 'valuable' is not None`. Restoring the original branch gave `python -m unittest test_e002a_maintenance_selection -v` → **10/10 PASS**. This is a **post-implementation mutation RED→GREEN validation**, not retrospective proof of full test-first compliance. No research outcome changes.

## Publication-status correction (2026-10-10; no new agent results)

The original v0.1 is an initial *targeted narrative seed and instrument-calibration report*, not a sufficiently deep interdisciplinary study. [Internal scientific referee report](../../reviews/2026-10-10-iteration-004-scientific-rigor-audit.md) assigns `MAJOR_REVISION_REQUIRED` despite GitHub/code verification. The [detailed methodological reassessment](methodological-reassessment.md) distinguishes the same-policy equivalence construction from a nontrivial proof, critically reviews an additional full-text cognitive-control model (Lieder et al., 2018) and specifies a stronger learned adaptive-scheduler comparison. **Nothing here promotes H005/H008, proves continuous internal cognition, or constitutes a new scored experiment.** The prior test traces and status remain preserved.
