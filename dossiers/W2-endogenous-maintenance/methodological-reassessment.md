# W2 E002a — Methodological Reassessment and Strengthened Research Specification

**Dossier supplement v0.2 · 2026-10-10 · status: CRITICAL REVIEW / FUTURE STUDY DESIGN.** Read with the [main W2 dossier](synthesis.md), the [004 referee audit](../../reviews/2026-10-10-iteration-004-scientific-rigor-audit.md), [E002a proposal](../../experiments/E002-endogenous-regulation-and-efference.md) and [the original calibration instrument](../../experiments/E002a-G0-maintenance-selection-v0.1.md). There are **no new scored model experiments** in this supplement.

## I. Reformulate the target

A long-lived artificial agent can carry a belief state, goals, event history and learned parameters from one conversation to the next. It may also spend compute without a prompt. Calling this 'endogenous cognition' bundles three separable questions:

1. **Scheduling autonomy:** who/what triggers a computational operation? Is the policy in the agent's source code, external orchestration, a periodic timer, or a resource controller?
2. **Metacognitive competence:** does the chosen computation actually *improve subsequent action* after costs, counterfactual deadlines, model errors and shifts are accounted for?
3. **Self-maintaining dynamical organization:** do persistent internal regulatory variables mediate behavior in a way not explained by simpler observable histories and generic adaptive policies?

A fourth, L3 phenomenal question is not identifiable merely from these outcomes.

The scientifically fruitful hypothesis is primarily (2) and perhaps (3): a persistently learned controller might achieve better net downstream reward per unit computation under changing constraints than strong resource-matched alternatives. The label or software packaging of policy (1) does not automatically predict better outcomes. The *source* of computational triggering is observable in instrumented code, but it is not by itself a cognitive breakthrough.

## II. Scope of formal non-identification

Let an environment produce permitted observation o_t and an information state m_t. A controller chooses internal compute operation c_t (including skip) and eventual external action a_t. Suppose two implementations C and S have equal initial state, permitted observations, computational opportunities and the **same conditional transition kernel** K(m_{t+1},a_t|m_t,o_t), including random seed coupling where relevant. Then their joint observable trajectories over the specified checkpoints have the same distribution. This is an elementary process-equivalence construction: any behavior-only test whose data comprise that observable trajectory has zero power to distinguish the implementation labels. This **does not** prove all candidate internal controllers equal all external schedulers or eliminate alternative physical dynamics.

To test meaningful mechanisms one must either (a) compare distinguishable learned policies with the same *available information and resources*, reporting an advantage without anthropomorphizing its location; or (b) select an intervention that reveals a relevant difference in actual internal dynamics while retaining proper matched comparator controls. An inaccessible internal signal given only to C may create an advantage through extra data, not endogenous structure. An architecture that wins because it was assigned more time, a more expressive value estimator or earlier event notifications fails causal identification.

A literal 'special endogenous cognition wins against a clone of itself' hypothesis is unfalsifiable as a performance claim. The proposed study must not be engineered with an unbeatable baseline, nor claim a performance difference when no difference is even theoretically predicted.

## III. Stronger primary evidence: value of control is a learned policy

**Full-text source examined:** Lieder, Shenhav, Musslick & Griffiths (2018), *Rational metareasoning and the plasticity of cognitive control*, *PLOS Computational Biology*, 14(4): e1006043, [publisher main article](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006043). Main text consulted: Models, alternative comparators, Results and Discussion, including Tables 1–2 and the visual-search/Stroop/Flanker cases. **Supplementary DOCX/model code and original five human datasets were not independently re-analyzed.**

The authors formalize cognitive-control choice as metalevel decision making: the state encodes beliefs about environment and internal computations; meta-actions choose control signals or strategies; costs include effort/time; the ideal meta-policy weighs effects on external decisions. They propose **Learned Value of Control (LVOC)**: predict value from features of the current situation and control option, update from reward/error, and select appropriate control intensity or strategy. Their paper models learning phenomena across several previously published human behavioral experiments, and compares predicted patterns to simple Rescorla–Wagner associative and win-stay/lose-shift strategies.

The human-task evidence matters because it illustrates a richer class of claim than 004: **adaptive control can be learned and transferred across conditions**, not merely chosen from an authored cost table. The article reports qualitative successes and fitted comparisons, but also imperfect fit and assumptions about feature representation, time cost and control processes. Its paper-level comparisons are not against today's strongest LLM policies or externally deployed metacontrollers; nor does the study establish continuous private thinking or artificial consciousness. Treat it as **published computational cognitive science**, not proof of H008.

**Abstract/proceedings-level rivals still pending detailed methods review:** Russell & Wefald (1991) justify computational choices via expected influence on external actions; Hay et al. (2012) analyze metalevel sampling and note counterintuitive optimal policies; Sutton (1991) integrates learning and planning in Dyna. These papers support well-engineered alternative policies but do not independently show that an AI subjective self exists.

## IV. What would count as a discriminating future experiment?

**Environment proposal:** a multi-period, partially observed, resource-constrained maintenance world: at each of T decision windows new commitments arrive; some targets drift, others stay stable; computation options can inspect/check a target, refresh a prediction, verify memory provenance, or do nothing. Such computations consume discrete budget and may return delayed/noisy observations. Event arrival is logged at a common interface, not privileged for a favored arm. Each agent resumes after actual process restarts with serialized states; evaluator-only hidden transitions remain sealed.

**Primary estimand:** paired improvement in *realized task utility minus total computation cost* for a candidate learned maintenance policy relative to the strongest learned external adaptive scheduler on held-out world families. Predeclare whether the target is best achievable expected performance, regret vs privileged Bayes oracle, or practical cost Pareto frontier. These are different estimands and cannot be switched after results. Cluster uncertainty at independent world/run level, not individual decisions inside the same generated episode.

**Arms before G2 freeze:**
- A. On-demand (no between-interaction computations).
- B. Periodic timer (equal number of maximum opportunities, resource-limited).
- C. Strong deterministic earliest-deadline/expiry and priority-queue policy.
- D. **Externally triggered learned value-of-computation controller** with exactly matched observable features, pretrained/learned parameters, calls, compute opportunities and state persistence to E.
- E. Candidate internal self-prioritizing learned controller (state access/feature sets identical to D unless one explicitly studies added information).
- F. E with its regulatory latent shuffled/frozen while preserving the matched budgets (negative-control ablation).
- G. Privileged Bayes planner *upper bound only*, not a fair budget-matched treatment arm.

**Crucial falsification:** If E and D compute the same transition policies over all available histories, then expected output equivalence is predicted. Do not call this a failed experiment; it is a specification failure for the 'special endogenous' claim. Reframe the comparison to a specific learnable representation or causal dependency before spending models. If E performs better due to extra hidden-state inputs, run a D+inputs control to distinguish architecture from privileged observability.

**Adversarial held-out families:** different event interarrival processes, delayed feedback, misspecified value forecasts, deadline bursts, abrupt goal changes, resource starvation, policy reset and stale provenance. Include negative controls where maintenance makes later decisions worse and a 'skip' action can dominate expensive work. Randomize paired independent worlds, predeclare exclusion when rewards are not identifiable from allowed observations, and report sensitivity to compute units/context budget.

**Measurements:** discounted total utility and net reward per compute; paired-world task-regret difference with confidence interval; computation-selection calibration; false-stale-memory and missed-commitment rates; transfer across new target types; robustness to abrupt changes; actual durations/uptime vs no-op periods; learned policy changes before vs after feedback. Real-time delayed sessions should not be confused with rapid simulated ticks.

## V. G0/G1 prerequisites still missing

1. World transition equations and simulator event semantics, with confidential evaluator/private state separation.
2. A *learned* baseline and identically exposed policy interface; weak cron-vs-heuristic wins are insufficient.
3. A proved identifiability argument for the chosen intervention and estimand; if structurally identical policies, no performance difference hypothesis is admissible.
4. Exact cost measure for cognition and matching rules for model calls, token budgets, preprocessing and checkpoint storage.
5. Frozen outcome target, practical effect floor, independent-world seed design, confidence interval/power/precision plan, family-wise testing, stopping/exclusion rule and full code versions **before** scored trials.
6. Independent reviewer/counterexample analysis. Present status: **SELF-REVIEW_ONLY**.

## VI. Decision for digital-mind architecture

**REVISE E002a research design; DO NOT PROMOTE H005/H008.** The prior toy remains a calibration test. A multi-period learned metacontrol study could contribute W2 L2 evidence only if a mechanism-specific intervention shows reliable effects under matched inputs/resources. Neither outcome can establish L3 subjective experience. No continuous agent system has been built or observed. The simplest well-instrumented event-driven learned controller should remain a favored baseline until evidence justifies more expensive continuous processing.

**Source/method ledger:** new full main-text review of Lieder et al. (2018) on 2026-10-10, published model-level outcomes only. S013–S015 remain mostly abstracts/proceedings metadata; neither their methods nor the current project agent environment have been reproduced. Original 004 remains immutable; this file records its non-independent critical reassessment.
