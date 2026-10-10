# H001 — Causal Autobiographical Memory, Identity and Future Action
**Living scientific dossier v0.1 · 2026-10-10 · Status: SEED / TARGETED NARRATIVE SYNTHESIS, not systematic or independently peer reviewed.**

**Scientific state:** H001 PROPOSED, E001 G0 OPEN, no scored AI agent trials. The source set draws from the existing [evidence ledger](../../evidence-ledger.md), abstract-level analyses, formal derivations and the already logged simulator tests. A cross-disciplinary systematic search, screened corpus, and full methods review have **not** been completed.

## Abstract

An artificial agent can persist facts, recreate a persona and retrieve episodes without retaining a privileged autobiographical self. Conversely, genuine historical causal competence does not necessarily require a graph or a natural-language narrative; a compact state estimator can preserve every task-relevant consequence of prior experience. This dossier asks what would discriminate experience-sensitive agency from simple transcript access and whether any autobiographical representation provides measurable advantages in action selection, correction, calibration and developmental continuity. The immediate empirical program E001 has only established correctness properties of deterministic test instruments, not agent-level benefits. The first small world is exactly identified by three diagnostic bits; a second graph-based world is fully reconstructible from observed intervention-effect records. These are meaningful *negative results for instrument discriminability*, not negative evidence against autobiographical memory in richer environments.

## 1. Construct definition: four claims that must not be conflated

**Personal fact retention** is accurate recall of biographical assertions or past dialogue. **Episodic memory** represents discrete events with context, action and outcome. **Causal autobiographical memory** is a proposed representation of how one's own actions and commitments caused consequences and corrections, available to constrain later policy after reset. **Identity continuity** is a broader philosophical and operational property: whether one is entitled to consider the changing agent a persisting individual rather than a set of unrelated outputs. These are not logically equivalent.

For this program, H001 concerns *functional future action*, not a test of phenomenal remembering. We operationalize an episode as `(world, time, agent action, predicted consequences, observed delayed feedback, provenance, confidence, corrections, affected goals)`; the specification is PROPOSED. An event log may carry the same information as a graph, so any advantage must be measured in generalization, efficiency, robustness to missing observations or errors—not assumed from the label.

Cognition and neuropsychology distinguish memory functions, but **this dossier has not yet critically examined enough primary neuroscience to make mechanistic human-memory transfer claims**. The relation between autobiographical memory, self-continuity and agency in humans is a priority evidence gap, not settled by an AI benchmark.

## 2. Formal decision-theoretic rival: a sufficient information state

Consider a partially observable world with hidden state `s_t`, history `h_t = (o_1,a_1,...,o_t)`, future action `a_t` and outcomes. A Bayes belief state is `b_t(s)=P(s_t=s | h_t)`. Under a correctly specified POMDP and appropriate Markov assumptions, `b_t` is a sufficient statistic for selecting a policy that maximizes conditional expected reward. If a proposed autobiographical memory `M(h_t)` contains no information beyond the identical allowed history, it cannot increase the *information-theoretic optimal value* beyond the true sufficient belief representation. It may still be substantially **easier to learn, approximate, audit, update or compress under finite computation**. This distinction is the core falsifier for extravagant claims of necessary graph memory.

A *predictive-state representation* instead represents history through predictions of action-contingent future observations. A raw event log, vector retrieval, a learned recurrent latent, and a structured cause/effect graph may all approximate control-relevant sufficient state. They have different inductive biases, editability and retrieval costs, but not automatic superiority. The test needs equal experience access and honest accounting of compute and memory budgets. See [rival models](competing-theories.md).

This observation also rebuts a common but invalid inference: showing C (structured memory) beats A (no memory) only proves that *some* persistent information matters; showing C beats a weak retrieval arm does not prove graph necessity if stronger B/F/G baselines were excluded.

## 3. What previous E001 work actually established

**Instrument 0: XOR Causal Switchboard.** A hidden three-bit rule produces the correct binary action for contextual probes. Given diagnostic contexts `00,10,01` with known attempted action and truthful binary reward, the three target bits can be inverted, yielding the exact rule `b0=v(00)`, `b1=v(00) XOR v(10)`, `b2=v(00) XOR v(01)`; its `11` probe is `b0 XOR b1 XOR b2`. The recorded 7-unit-test suite and 832 exhaustive instrument cases validated the oracle/queue specification (see [iteration 002](../../runs/2026-10-10-iteration-002.md)). This is a finite deterministic identity, **not** a statistical sample or LLM agent evaluation. After fresh phase diagnostics, intervention changes do not create a hidden-change inference problem: the new rule is identified afresh. This world should remain a unit-test instrument.

**Instrument 1: Causal Commitments Workshop.** A randomly generated acyclic graph governs how binary interventions propagate across nodes; commitments assign penalties to undesired terminal states. The simulator exposes each action's full effect mask during phase 0, then chooses an optimal pair of interventions after the protocol reset. In [iteration 003](../../runs/2026-10-10-iteration-003.md), local tests passed 10/10; 100 seeded worlds yielded matching privileged and observation-only optimal plans. Removing the final commitment changed the optimal plan in 419/1,000 seeded paired scenarios. This 41.9% is a **deterministic generator-specific sensitivity frequency**, not a causal effect estimate on AI memory or a transferable agent result. Moreover, the full action-effect matrix is a sufficient lookup for the task; an elaborate graph cannot have extra available information. The protocol reset changes simulator phase, not demonstrably a separate model process.

**Current scientific decision:** neither simulator supplies a valid estimate of H001's architectural advantage. The models/agents under comparison have not been run. A0 is still proposed; A1 is unselected. This is an epistemic advance through falsification of *benchmark informativeness*, not an empirical demonstration of mind-like personal history.

## 4. Existing empirical AI evidence and transfer limitations

The [literature matrix](literature-matrix.md) distinguishes external evidence from these local tests. LongMemEval (S003) stresses conversational temporal updating/abstention, LoCoMo (S005) stresses multi-session conversational memory, and MemoryAgentBench (S004) extends incremental memory and selective forgetting; their measured domains are not direct E001 intervention/action inference. MemoryArena (S006), EMBER-Bench (S007) and AMA-Bench (S010) are more relevant to downstream action and cross-event constraints, but the current dossier largely inherits abstract/metadata reviews. CausalGame (S011) motivates interventions under confounding and noisy measurements; an intervention-based memory admission preprint (S012) is a candidate retrieval comparator, not established superiority in our target environments.

**Literature caveat:** these are scoped source leads, not a completed systematic literature review. No exhaustive database search, deduplication, PRISMA diagram, eligibility accounting, full methods extraction, study-quality grading or replication has occurred in this dossier. Therefore no performance figure reported externally is pooled, generalized, or treated as independent confirmation of H001.

## 5. Designing a genuinely discriminative future test

We need a *partially identified*, dynamic environment where earlier personal commitments, interventions and corrections matter **after reset** and only limited noisy probes are available. A sufficient-state controller must remain the strongest expected-value rival. Proposed operations:

1. Sample world-family transition mechanisms and personal commitments from independently held-out mechanisms, not merely lexical aliases.
2. Allow bounded diagnostic actions under budget, sometimes with delayed/incomplete feedback and controllable observational confounding.
3. Use an evaluator whose privileged world model remains strictly inaccessible to the policy. Calculate the optimal action under each world hypothesis consistent with the actual permitted observations, or a Bayes-optimal expectation using *preregistered priors*. Do **not** present a single hidden-world oracle as if the environment were identifiable.
4. Establish distinct test splits for identifiable, partially identifiable and unidentifiable scenarios. In the latter, reward calibrated uncertainty or further sampling, not impossible certainty.
5. Compare same-foundation-model policies with no memory, raw-history, retrieval, compact belief/predictive state, causal graph, sham and selectively ablated edges. Include a deterministic oracle/planner reference **not FLOP-matched**, labeled appropriately.
6. Freeze prompts, models/decoding, context, total lifecycle inference/search budgets, sample sizes, seed assignment, metrics, thresholds, statistical and multiplicity plan, exclusions, stopping rules **before scored trials**.

Primary metrics should be policy regret and intervention-correct action after history under matched budgets; secondary measures include calibration, correction uptake, causal-trace integrity, forgetting, false-memory susceptibility, cost and robustness. A graph representation might outperform approximately learned belief states under constrained compute; it should lose gracefully if the compact solver attains better accuracy/cost. **Any graph win must survive ablation** and uncertainty estimates clustered by independent world.

## 6. Implications for digital identity and integrated mind

A positive E001 outcome would support an *L2 component mechanism* at the evaluated task distribution. It would not establish rich subjective memory, an enduring identity across real calendar time, an emotionally coherent personality, consciousness or the necessity of A1. Integration must ultimately test causal interdependence among self-model, goals, memory, planning and learning in a single system in [E900](../../experiments/E900-longitudinal-entity-benchmark.md), which is still PROPOSED.

The methodological stance is intentionally pluralistic: memory may be a graph, a recurrent process, a probabilistic information state, verifiable procedural rules, a human-inspectable event log, or a hybrid. The engineering task is to determine which representation produces durable and correct downstream decisions under the real operating constraints and safety requirements.

## 7. Critical limitations and forward agenda

The toy generators are synthetic and authored by the research program; their dynamics may privilege particular data structures and compressible assumptions. Phase resets are not genuine independent sessions. Environment rewards do not operationalize social meaning, human identity, self-modeling or welfare. Current evidence is insufficient to make claims about how human autobiographical memory is implemented or which theory of consciousness applies to an artificial system. No independent reviewer or external replication has verified these results.

**Next decision-relevant milestone:** define an observation-consistent oracle and information-budget protocol for selective, noisy interventions in the Stage-1 environment, including test-case exclusion for genuine unidentifiability, before preregistration G2. W2–W4 investigation must also proceed under [the roadmap](../../atlas/research-roadmap.md), rather than allowing memory to monopolize research.

## Revision history

2026-10-10 v0.1: retrospective **targeted narrative seed** based on pre-existing project state and source leads S003–S012; no new trials and no independent scholarly review. The original evidence remains in [runs](../../runs/) and [source ledger](../../evidence-ledger.md).
