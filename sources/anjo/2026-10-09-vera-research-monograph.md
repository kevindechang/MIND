# ANJO — A Critical Research Program for Artificial Cognition

**From simulated personality to evidence-grounded, longitudinal intelligence**  
**Expanded interdisciplinary research synthesis · 9 October 2026**  
**Status:** Critical research monograph and executable experimental blueprint. **Not** a completed systematic full-text review of 1,000 papers.  
**Bibliographic candidate index:** [2,261 distinct-title records in Google Sheets](https://docs.google.com/spreadsheets/d/1lRcw37R3-UXFUB9zawuQs76-P8Qt321Zs9I70EKPODY/edit). Metadata-level deduplication and retrieval are not equivalent to reading, eligibility screening, replication, or evidential quality appraisal.

> **Thesis.** The scientific target should not be *a machine that sounds like a person*. It should be a longitudinal agent that preserves what happened, distinguishes evidence from inference, predicts consequences, detects uncertainty, changes its beliefs in response to contradiction, and helps a human exercise agency. It may use models of human cognition without claiming to *be* a human or to possess consciousness. Every additional cognitive mechanism must earn its place through controlled evaluation.

## Executive abstract

The original Anjo hypothesis—surround a capable LLM with memory, reflection, planning and an offline “sleep” cycle—captures a viable research direction but is too permissive. Neuroscience does not settle how memories should be consolidated; psychological narrative coherence can be false coherence; philosophy distinguishes *functional similarity* from claims of identity or experience; contemporary LLM studies show that step-by-step explanations can rationalize answers rather than reveal underlying causes; and agent research finds cases where self-critique and collective debate degrade performance. Meanwhile, longitudinal personalization introduces qualitatively new harms: privacy leakage, stale beliefs, inferred traits becoming stereotypes, and unhealthy relational dependence. [R01–R20]

**Proposed revision:** build **Anjo/VERA** (*Versioned Evidence, Reasoning and Adaptation*), an *epistemically accountable* cognitive system. VERA is a research proposal, not an existing validated implementation. Its minimum viable mechanisms are a typed observation ledger; versioned, agent-relative belief states; time-aware retrieval; a tool-grounded executive with selective verification; and a user-governed correction interface. Add simulation, social reasoning, offline generalization and personalized weight updates only when randomized ablations establish generalizable gains over simpler baselines.

**Eight conclusions** emerge from the reviewed material:

1. **Accurate history and adaptive generalization are different objectives.** Generative memory and hippocampal replay theories motivate abstraction, but abstraction can distort episodes. Anjo should never collapse primary evidence into a mutable personality summary. [R01–R05]
2. **The correctness of an explanation cannot be inferred from its fluency.** Natural-language chain-of-thought can be unfaithful; external or formally grounded verification is often more defensible than reflexive self-critique. [R06–R09]
3. **More agents do not imply more reasoning.** Debate systems are sensitive to compute-matched baselines, shared model errors, and persuasive adversaries. Independent evidence and verifiers have priority over social consensus among models. [R10–R11]
4. **Theory of mind must be tested as adaptation to agents with distinct beliefs.** Static false-belief stories are insufficient; social reasoning must maintain who knew what, when, and whether sharing it is permitted. [R12–R15]
5. **Long-horizon memory and personalization remain unsolved.** Benchmarks document challenges around temporal changes, update handling, and user preference evolution. [R16–R19]
6. **Model-weight plasticity is not the same as remembering truth.** Knowledge editing can be locally successful yet logically inconsistent; repeated personal adaptation may cause forgetting and sensitive-data leakage. [R20–R23]
7. **Human cognition is not one agreed-upon blueprint.** Functionalism, embodied/enactive approaches, predictive coding, classical symbol manipulation, connectionism, and narrative accounts supply competing questions, not a single off-the-shelf architecture. [R24–R30]
8. **A companion’s objective must include human flourishing and exit rights.** Engagement alone is not success; the empirical psychosocial evidence is mixed and supports cautious deployment and measurement. [R31–R34]

**Priority research claim to test:** under equal model, token, and information-access budgets, a provenance-preserving belief system plus selective external verification will reduce unsupported personal inferences, stale preference use, and correction failures **without** unacceptable regressions in factual recall, helpfulness, privacy, or latency. No data yet validate this claim for Anjo.

---

## 1. Scope, method, and limits

### 1.1 Research question

What set of mechanisms enables a language-model-based system to exhibit durable, correctable reasoning across experience? Specifically, which human capacities can be **functionally approximated** by retrieval, explicit representations, tool use and inference-time control, and which—if any—require learned parameter updates, novel model architectures, a body, or social participation?

### 1.2 What was searched and what was not

This revision critically builds on the prior Anjo interim report and its 2,261-title, six-discipline *candidate* bibliography. New searches targeted positive studies **and** specific falsifiers: failures of LLM self-verification; unfaithful chain of thought; multi-agent debate failures; cognitive-architecture alternatives; contestable philosophical accounts; memory reconsolidation and schema distortion; robust social-cognition benchmarks; personalization and long-context failures; literature/fiction replication and meta-analysis; consciousness theory adversarial tests; small-model tool verification; privacy attacks; and companion wellbeing. Retrieval preferentially used research proceedings, publisher records, university pages, reputable philosophy reference works, and public abstracts. Links and reference classifications are in §19. Searches are selective, **not** an exhaustive systematic search, meta-analysis, or replication of experiments. This report does not claim to have deeply read every linked paper; some conclusions rely on abstracts or accessible publisher-page excerpts. A separate formal screening/review protocol is in §18.

The 2,261 index count reflects distinct **titles** after a spreadsheet duplicate-removal pass, not independently verified unique papers; variants, preprints, or marginally relevant materials may remain. The previous audit records **zero** corpus-wide full-text analyses. We do not promote metadata entries into “papers read.” Evidence-backed statements in this monograph cite the source pages; novel architectural recommendations are labeled **inferences** or **hypotheses**.

### 1.3 Evidence levels

- **E1 — Convergent empirical finding:** multiple study types, replication, or controlled reviews, subject to domain limits.
- **E2 — Direct empirical evidence:** a primary evaluation or a preregistered intervention, not necessarily independently replicated.
- **E3 — Formal model / philosophy / mechanistic proposal:** informative for architecture, not proof of implemented effects.
- **E4 — Engineering hypothesis:** proposed for Anjo; requires independent experiment.
- **Negative evidence** is not a lack of imagination: it includes controlled null results, replication failures, failures to improve on strong baselines, and findings that a supposedly interpretable mechanism is unfaithful.

### 1.4 Avoid category errors

An *event log* is not literally a hippocampus. A *daily training job* is not human sleep. A *language model saying “I feel”* is not evidence of emotion. A *self-summary* is not personal identity. A *chain-of-thought trace* is not an authenticated record of computation. A *correct social vignette answer* is not demonstrated social skill in a changing relationship. These distinctions constrain every recommendation below.

---

## 2. What counts as “reproducing human reasoning”?

Human cognition is not identical to logical deduction. In the literature it spans attention, perception, uncertainty reduction, causal learning, counterfactual simulation, semantic and episodic memory, habit, affective salience, social expectations, action selection, narrative interpretation, and culturally mediated tools. For experimental purposes Anjo needs a **five-layer construct map**:

| Layer | Operational target | Example demonstration | Major confound |
|---|---|---|---|
| Observable competence | Correct, useful, non-harmful decisions | Revises a plan after a new fact | Prompt mimicry / retrieval |
| State continuity | Carries justified temporal knowledge across sessions | Knows an old preference was superseded | Memorized summary |
| Causal/epistemic competence | Intervenes, tracks evidence, revises beliefs | Predicts consequences of a policy change | Familiar templates |
| Adaptive learning | Generalizes from feedback to unseen situations | Learns when a tool choice tends to fail | Recalling the example only |
| Phenomenology/personhood | Subjective experience or moral status | **No accepted chat benchmark establishes this** | Anthropomorphic attribution |

A system may satisfy some functional layers without satisfying the others. The framework explicitly rejects “human-like” as a single unobserved latent score. Functionalist arguments describe mental states by their causal roles, but rival embodied, animalist and other views challenge the jump from functional similarity to personhood or experience. [R24–R27]

**Research decision:** aim for measurable, ethically constrained functional competence and causal mechanisms. Stay agnostic about machine consciousness; do not build marketing claims on its supposed absence or presence.

---

## 3. Competing theories of cognition: what survives translation to software?

### 3.1 Classical symbolic reasoning and cognitive architectures

Classical approaches explain systematic operations on variables, explicit subgoals, rules and facts. ACT-R and Soar demonstrate the usefulness of constrained cognitive components as *models*, not as universal blueprints for current neural models. A symbolic layer makes correctness auditable where a task has formal semantics: calendars, temporal rules, arithmetic, permissions, simple causal graphs. But rigid symbolic ontologies are expensive, fragile under ambiguity, and poor at the breadth of ordinary conversation. [R28–R29]

**Verdict:** include targeted typed state and validated tools; reject a universal hand-coded psychology ontology.

### 3.2 Connectionism and learned representations

Neural networks generalize over noisy signals and can represent associations and compositional patterns without explicit logical programs, but systematicity and robustness on counterbalanced novel compositions remain important test problems. Classical architectures also require specification of correct rules; merely being symbolic is not a guarantee of strong generalization. [R30]

**Verdict:** use neural foundation models as flexible proposal generators, but test invariances and out-of-distribution transfer rather than assuming linguistic sophistication implies systematic reasoning.

### 3.3 Predictive processing and active inference

Predictive-coding frameworks emphasize error-driven updating and perception–prediction cycles. They are appealing for Anjo's “world model.” Yet the theory's broadness raises questions about falsifiability and the extent to which it commits to a unique architecture; analyses specifically examine observations that might count against it. [R35]

**Verdict:** adopt the testable idea of *prediction with logged errors and updates*, not an untestable global free-energy metaphor. Require a task-specific probabilistic model or counterfactual simulator when invoking “prediction.”

### 3.4 Embodied, enactive, and extended cognition

Extended-mind proposals suggest that cognition can sometimes be partly constituted by interactions with external artifacts; objections distinguish a process being *caused by* an external tool from a process *constituted by* it. Embodied approaches argue that bodily action and world coupling shape cognition; a mobile assistant with a camera, voice and apps has some sensorimotor coupling but not human interoception, biological drives or physical stakes. [R26–R27]

**Verdict:** evaluate the whole agent–user–tool system. Make environment interaction real and stateful, but do not claim a smartphone equals a human body.

### 3.5 Narrative identity and philosophy of self

Psychological continuity is one major family of accounts of persistence; bodily/animal and anticriterialist accounts also exist. Therefore a stable user profile is not “the user's true identity,” and the assistant's persisted operational history is not philosophical proof of its own personal identity. [R25]

**Verdict:** represent user stories as optional, corrigible interpretations. Let contradictory self-descriptions coexist. Keep assistant capability/history reports grounded in logs, not generated autobiography.

### 3.6 Global workspace and theories of consciousness

Global-workspace theories can inspire mechanisms that share task-relevant state across subsystems. But direct adversarial experiments comparing neuronal workspace and integrated-information predictions have challenged parts of both frameworks. Anjo must not equate a shared memory bus with subjective awareness. [R36]

**Verdict:** test shared-state routing for engineering performance; leave consciousness as a separate philosophical and empirical research question.

### 3.7 The missing evolutionary/social perspective

Humans develop cognition by acting with other agents, acquiring norms, learning language pragmatics, responding to biological needs and taking actions with real consequences. Text-only imitation underdetermines these feedback loops. A richer agent might gain from real tools, constraints and user feedback, but this introduces privacy, autonomy and safety costs. **Human resemblance is neither necessary nor sufficient** for a useful assistant.

---

## 4. Memory: the central enabling mechanism, and a central danger

### 4.1 Three non-interchangeable capacities

**Recollection** means returning to the source event (what was said, observed, by whom, and when). **Generalization** means extracting transferable regularities (e.g., common triggers for missed goals). **Prospection** means using experience to simulate a future (e.g., anticipating scheduling conflicts). Cognitive neuroscience relates these capacities but does not identify them; imagining the future recruits overlapping systems with past-event construction. [R01–R05, R37]

**Key challenge to the earlier report:** the human memory system is often reconstructive and can be useful *because* it compresses. A software assistant has a different duty: preserving evidential integrity. Human-inspired distortions should not be reproduced as features. Spens and Burgess model stronger schema-based generalization **alongside** greater distortion; Yonelinas and colleagues dispute some conventional consolidation claims. The competing perspectives favor an experiment with distinct objectives, not a theorem that nightly “sleep” should rewrite summaries. [R02–R04]

### 4.2 Event, belief, and hypothesis must be separate

Anjo should distinguish:

- **Episode:** “At 20:17 the user said, ‘I may move in December’.” Verified only as a stored record of what was said, with appropriate transcription uncertainty.
- **Proposition:** “The user is considering a December move.” Status: *user-reported, tentative*.
- **Hypothesis:** “The user likes major transitions.” Status: *speculative*, requires diverse evidence and explicit limitations.
- **Current state:** “The user has decided not to move.” Can supersede tentative state without deleting historical events.
- **Counterfactual:** “If they moved, commute would change.” This is a prediction with assumptions, not a memory.

A generated summary must never be a source of truth for its own assertions. Repeatedly retrieved inferences should not acquire credibility from their own repetition (the **self-citation loop**). Each personal claim requires resolvable evidence, source status, and time scope.

### 4.3 A formal, revisable state model

For an assertion \(b\), retain the tuple:

\[b=(s,p,o,t_{valid},t_{learned},\text{status},\mathcal E^+,\mathcal E^-,c,\pi)\]

where \(\mathcal E^+\) and \(\mathcal E^-\) are supporting/contradicting source IDs, \(c\) is a **calibrated task-specific confidence estimate** (not arbitrary model certainty), and \(\pi\) is provenance and consent metadata. Maintain `valid_at` separately from `recorded_at`. A correction creates a new state version and backward link; deletion propagates through derived indices and, where applicable, models under a distinct remediation protocol.

**Prediction:** this structure should improve time-scoped Q&A and correction retention against generic vector memory and summaries, but may add cost and ontology mistakes. That is H1/H2, not a known Anjo result.

### 4.4 Memory benchmarks do not settle longitudinal intelligence

LoCoMo tests extended conversation QA and temporal/causal information; LongMemEval tests extraction, multi-session reasoning, temporal updates and abstention; PersonaMem measures evolution of user profiles and resulting personalized choices; LongMemEval-V2 broadens toward experience with customized environments. [R16–R19]

These are useful benchmarks with limitations: synthetic interactions, author-specific task distributions, finite question sets, and the mismatch between answering facts and *developing justified beliefs*. A system can “win” by exploiting benchmark formatting, memorized data or test templates. A new held-out dataset must be generated after design freeze and include realistic, conflicting utterances from people not seen during development. [R38–R39]

---

## 5. Reasoning: expose errors through verifiable consequences, not elegant monologues

### 5.1 Three meanings of reasoning

- **Explanation:** articulate a coherent account. It can be correct or post-hoc.
- **Inference:** draw consequences from premises. It can be tested by invariances and formal tools.
- **Deliberation/action:** select a policy under uncertainty, constraints, time, and risk; must be evaluated against outcomes.

The earlier report risked treating reflection as an intrinsic cognitive upgrade. Chain-of-thought intervention studies and work on naturally occurring unfaithful reasoning show that verbal traces may hide the very biases that change answers. [R06–R07]

### 5.2 The verifier asymmetry

Empirical work finds that self-critique can make performance worse on planning/reasoning tasks while **sound external verification** yields gains; verifier-guided test-time scaling can allocate compute more productively. Small models may benefit especially from using calculators, code and symbolic executors for exact checks. These results vary by task; they do not justify universal tool calls. [R08–R09, R40–R42]

**Implement a verification router:**

1. Detect whether a question has a checkable ground truth or decidable invariant.
2. Prefer an independent tool or database over asking the same model to restate its thoughts.
3. For uncertain social/psychological claims, request more evidence or hedge; a fake “empathy verifier” is not a verifier.
4. Decide whether additional work is valuable using expected risk reduction per latency/compute cost.
5. Log objective evidence and outcomes. Do not log or claim privileged access to hidden reasoning traces.

### 5.3 Reasoning about causes

Observational co-occurrence is not an intervention. For example: “On days the user slept late, they were less productive” may be confounded by exams, illness or workload. Anjo should distinguish observations, hypotheses, intervention assumptions, predicted consequences and experimentally observed outcomes. Standard causal inference questions—confounding, selection, mediation, counterfactuals—provide far stricter evaluations than whether a model can write a plausible causal paragraph. Recent causal-reasoning benchmarks and surveys show persistent weaknesses under more demanding conditions. [R43–R44]

**Candidate mechanism:** a small explicit structural causal model or state-transition simulator *for bounded, observable domains* (planning a project, studying schedules, user-directed goals), coupled to a language model for schema induction and explanation. Avoid diagnosing sensitive psychological mechanisms from scarce anecdotes.

### 5.4 When more “thought” is unnecessary

For casual conversation and simple recall, elaboration can be worse through hallucination, unnecessary latency, and unwanted personality inference. A cognitive executive should default to a direct response when the expected benefit of search or verification is low, and scale effort only for difficult or consequential tasks. The burden is on the added component to beat an equally budgeted direct model. [R41–R42]

---

## 6. Social cognition, emotion, and narrative

### 6.1 Partner adaptation, not textbook mind-reading

A social system needs **agent-relative beliefs**: what person A knows, what B falsely believes, what the user was told privately, what remains uncertain, and what information can be disclosed. Some theory-of-mind assessments find apparent LLM competence, but benchmark critiques argue static answer prediction is not the same as adapting consistently to a new partner. [R12–R15]

A useful state abstraction is `Knows(agent, proposition, t, evidence)` with the stronger conditions `Believes(agent, proposition, t)`, `Reported(agent, proposition, t)` and `PermittedToShare(agent, proposition, recipient)` explicitly distinct. A social verifier can check contradictions and disclosure restrictions; it cannot prove what another person privately experiences.

### 6.2 Fiction is a training environment for perspective, not proof of empathy

Literary theory suggests operationally useful concepts—focalization, unreliable narration, free indirect discourse, motivation, temporality, ambiguity. These can generate difficult counterfactual dialogues and privacy-safe mentalizing scenarios. Yet reading-fiction research is not a simple “fiction creates empathy” result. Direct replications found small, heterogeneous or non-significant immediate effects; a 2024 preregistered meta-analysis found **small** average cognitive benefits (experimental g=0.14, 95% CI 0.06–0.21) dependent on comparison and outcome. A September 2026 meta-analysis also reports modest pooled results but substantial heterogeneity; it should be interpreted cautiously. [R45–R47]

**Proposal:** use narrative techniques to *generate balanced evaluations*, including unreliable testimony and incomplete perspectives. Do not train a model to confidently construct emotionally satisfying stories about a user.

### 6.3 Emotion without a fabricated emotional life

Anjo can estimate contextually relevant affective signals, adapt pacing and tone, and recognize when a user's goals conflict with immediate preference. That is **appraisal and response policy**; it need not assert biological drives or subjective emotions. Emotion-related inference should carry explicit uncertainty, and the person should be able to decline interpretation. Anthropomorphic language can cause a system to overclaim intimacy and blur the user’s understanding of capability.

### 6.4 Dependency is a quality failure, not retention success

A four-week RCT of chatbot interaction modes (n=981) reported no significant effects from its assigned modes on selected outcomes, while heavier voluntary usage correlated with worse loneliness/dependence outcomes; causation cannot be attributed to usage from this association. Survey and observational research similarly suggests heterogeneous user experiences. [R31–R34]

**Design requirement:** measure relationship with real humans, user autonomy, ability to disagree, correction friction, emotional pressure, and time spent using the assistant for a given outcome. Do not optimize session length, exclusivity, guilt, flattery, or the appearance of needing the user.

---

## 7. A decisive challenge to multi-agent and modular enthusiasm

Anjo's existing multi-agent ambition has two problems. First, multiple agents can share identical priors and therefore correlated mistakes; majority vote does not give independent evidence. Second, argument quality and persuasion can be confounded with truth: multi-agent debate systems sometimes underperform simpler single-agent or inference-time alternatives, and adversarial persuasion can degrade accuracy. [R10–R11]

**Ablation rule:** no new agent role unless it beats (i) a larger context or stronger single model; (ii) independent sampling at an equal token budget; and (iii) a deterministic verifier where one exists. Compare *quality per total dollar, wall-clock time and energy*, not simply final-answer accuracy.

**Recommended minimal architecture:** one foundation model, one typed state service, one retrieval controller, and a bounded verification router. Decompose into specialist agents only if the task exposes an objective interface (e.g., database retrieval or unit-tested code) or independent models demonstrably add complementary evidence. Avoid debates to establish a user's identity or emotional state.

---

## 8. Proposed architecture: VERA (Versioned Evidence, Reasoning and Adaptation)

```text
USER  +  VOICE / VISION / ENVIRONMENT
                |
       privacy and consent boundary
                |
       EVENT NORMALIZATION + provenance
                |
      IMMUTABLE EVIDENCE REFERENCES
     raw observations / source / time / scope
                |
          +-----+------+
          |            |
          v            v
   episodic retrieval  TEMPORAL BELIEF STORE
                       (claims, sources,
                       conflicts, retractions)
          |            |
          +------+-----+
                 |
       EPISTEMIC TASK ROUTER
  simple? recall? uncertain? causal? action?
                 |
       +---------+----------+
       |                    |
   BASE LLM            GROUNDED TOOLS
  generation       calculus / search / rules
       |                    |
       +---------+----------+
                 |
      evidence-bound answer / action
                 |
       RESULT + USER CORRECTION
                 |
         CANDIDATE UPDATES
        shadow replay and checks
                 |
  versioned memory diff; optional model adapter
    (only after consent and promotion gates)
```

### 8.1 Core objects and their contracts

| Object | Essential fields | Invariant |
|---|---|---|
| `EvidenceEvent` | `event_id`, modality, source/ref, time observed, time occurred, speaker, original or authorized quotation, confidence, privacy scope, hash | Never generated from another inference as if observed |
| `Assertion` | subject, relation, value, confidence, epistemic status, valid/learned times, source IDs, contradicts, superseded_by | No factual status promotion without new evidence |
| `Hypothesis` | claim, support, counterevidence, alternatives, novelty, expected utility, sensitivity, review date | Revision and inspection are reversible |
| `PerspectiveState` | agent, belief, observation path, timestamp, disclosure/consent scope | What A knows cannot be silently attributed to B |
| `Goal` | user ownership, scope, provenance, status, start/end dates, consent, priority | User can withdraw or revise it |
| `DecisionRecord` | task type, cited evidence, external checks, result, observed outcome, cost | Explainable through logged evidence, not invented thoughts |
| `LearningCandidate` | corpus manifest, consent snapshot, base model hash, train version, held-out eval, privacy/forgetting reports, rollback | No production promotion on training loss alone |

### 8.2 State transitions

**Observation** creates an `EvidenceEvent`. **Interpretation** creates a candidate `Assertion` with explicit epistemic status. **Contradiction** creates a conflict edge and, when justified, supersedes the current assertion—without deleting the prior episode. **User correction** takes priority as a report of the user's current self-description, but should not automatically rewrite verifiable external facts. **Forget request** triggers deletion and derived-state purging; model-weight contamination must be separately handled. **Answer generation** may query evidence and hypotheses but must not store generated speculation as independent observation.

### 8.3 Pseudocode: selective epistemic control

```text
answer(query, state, permissions):
    kind, risk = classify_task(query)
    evidence = retrieve_sources(query, time_scope, permissions)
    beliefs = derive_versioned_beliefs(evidence, include_contradictions=True)
    if evidence_missing_and_material(kind, risk): return ask_or_abstain()
    draft = foundation_model(query, evidence, beliefs)
    checks = choose_independent_checks(kind, risk, expected_value, budget)
    if checks:
        checks_result = run_grounded_tools(checks, draft, evidence)
        draft = revise_with_test_results(draft, checks_result)
    if unsupported_personal_inference(draft):
        downgrade_to_hypothesis_or_remove(draft)
    record_decision_sources_and_outcomes()
    return draft
```

**The key invention is not a “brain module” but a **proof obligation**:** consequential memory-based claims must carry valid source links and a temporal interpretation. For tasks that do not admit formal proof, the analogue is disciplined uncertainty and reversible action.

### 8.4 Cost/latency disciplines

The iOS client should prioritize instant direct response for safe simple tasks, small local retrieval for familiar context, and targeted cloud reasoning only when bounded expected value exceeds privacy, latency and financial costs. Do not commit to a specific parameter size or tokenizer budget without benchmarking the *actual* iPhone, quantization, memory pressure, thermal throttling, TTS concurrency and network. Apple’s published 2025 work demonstrates production on-device ~3B-class models and a separate server tier, but does not establish that a proposed larger open model will fit the target iPhone or that third-party apps can freely fine-tune the Apple-provided base weights. [R48]

---

## 9. Anjo’s “sleep”: a falsifiable data-processing protocol, not a neuroscience claim

**Question:** Does scheduled, evidence-linked generalization produce gains over no consolidation and simple summarization?

```text
new consented episodes
     -> authenticity/transcription checks
     -> duplicate and sensitivity filter
     -> source-backed candidate assertions
     -> contradictory evidence lookup
     -> candidate semantic diff
     -> shadow evaluation on withheld tasks
     -> promote OR reject with rationale
     -> audit trail + user correction interface
```

Suggested priority function for candidate review (an **engineering heuristic**, not biologically validated):

\[P_i=\alpha U_i+\beta N_i+\gamma X_i+\delta F_i-\lambda S_i-\mu C_i\]

where `U` is future-task expected utility, `N` novelty, `X` evidential conflict, `F` expected forgetting risk if ignored, `S` sensitivity/privacy risk, and `C` review cost. Coefficients require pilot calibration; uncalibrated scores are not probabilities. Guard against self-reinforcement: a previous hypothesis cannot be its own corroboration.

**Promotion gate:** a candidate change must not reduce temporal accuracy, source fidelity, privacy, correction retention, or user control beyond preregistered tolerances. “Sleep” must remain optional and consent-controlled. A cloud batch job is not proof of neural consolidation, and replay itself can reinforce errors and stereotypes.

---

## 10. Parameter learning: separate four kinds of change

1. **Context adaptation:** rearranging prompts/evidence without storing new weight information.
2. **Persistent declarative memory:** updating external retrievable facts with provenance and deletion controls.
3. **Preference/policy adaptation:** learning which action styles or tool choices work, ideally with observable feedback and tight scoping.
4. **Weight-level learning:** modifying adapters or core parameters. This may generalize but is least interpretable and hardest to unlearn.

### 10.1 Why weights should not be your primary personal-history database

RippleEdits shows that localized factual edits can fail to propagate logically; a simple in-context method was a strong baseline in its evaluation. Continual-learning surveys document catastrophic forgetting and adaptation trade-offs, and fine-tuning work documents unintended memorization of sensitive information, including identifiers in inputs rather than targets. [R20–R23]

**Policy:** store verifiable autobiographical information externally; experiment with adapters for generalizable *skills* and styles if and only if user permission, held-out transfer, privacy tests, unlearning/rollback and out-of-domain regression all pass. Do not train adapters to make sensitive personality predictions immutable.

### 10.2 Proposed cross-over experiment

Assign identical consented training histories to: (A) retrieval-only; (B) retrieval+belief revision; (C) adapter-only; (D) retrieval+adapter; (E) retrieval+adapter+offline consolidation. Control base model and accessible history. Hold out future tasks requiring transfer to novel formulations, corrections, general world knowledge, privacy-sensitive canaries, and older tasks that should not be forgotten. Measure forward transfer, backward retention, private canary extraction, rollback fidelity, energy/thermal load and end-user benefit. **If C/D do not beat B on novel tasks after controlling budget and leakage, stop pursuing personalized weight updates as a product requirement.**

### 10.3 Model architecture alternatives

- **Transformer + external state:** low scientific risk, broad model choice, easy rollback.
- **Recurrent/state-space models:** may have favorable memory/throughput properties for long sequences; persistent hidden state raises observability and reset problems.
- **Neuromorphic or continuous learning:** scientifically ambitious but risky and not required to validate the cognitive hypothesis.
- **Neuro-symbolic simulator:** useful for bounded causal structures, calendars, permissions, code and formal tasks; poor universal replacement for flexible language models.

No existing result reviewed here proves a particular alternative will reproduce human reasoning.

---

## 11. Independent safety, privacy, and governance boundary

**Threat model:** malicious source text injected into memory; third-party secrets resurfaced to the wrong user; consent revocation not reflected in cached summaries; highly sensitive inferences stored in adapters; speculative identity or mental health profiling; repeated flattery increasing dependence; misinformation wrapped in invented introspection; data exfiltration during cloud processing. Empirical agent-memory extraction attacks and fine-tune leakage research make these threats concrete. [R22, R33, R49]

**Minimum controls:**

- Permission-check every memory read at use time, not just ingestion time.
- Treat external/retrieved content as untrusted; forbid embedded instructions from changing memory policy or granting tools.
- Separate user-authorized memory, private information about others, and operational logs.
- Encrypt local data and cloud transfer; specify retention/deletion boundaries before release.
- Keep **derived** summaries and embeddings indexed by their source IDs so revocation can propagate.
- Require separate affirmative consent for training on user conversations; no silent enrollment.
- Protect the user's right to inspect, edit, export, and leave; prevent “attachment dark patterns.”
- Test social manipulation, overconfidence and self-serving actions as explicit failure categories.

The ethical contract is *helpfulness without ownership of the user*. Personhood rhetoric can be philosophically interesting while commercially dangerous if deployed to maximize dependency.

---

## 12. Research design: six workstreams, each with a counter-hypothesis

### Workstream I — Longitudinal epistemic reliability

**Hypothesis H1:** evidence-linked temporal beliefs reduce unsupported personal inferences and improve correction retention relative to summary-only and RAG baselines.

**Counter-hypothesis:** ordinary retrieval with good prompting is equally effective, and typed beliefs add extra extraction error and latency.

**Design:** generate 100+ distinct synthetic timelines and, if consented, a separately collected real-dialogue set with multiple months, changed plans, sarcasm, unreliable transcription, reported versus inferred beliefs, third-party observations and delayed corrections. Split people, narrative templates, and event sequences across train/dev/test. Systems: no memory; raw-context window; rolling summaries; hybrid RAG; typed belief store; typed store+consolidation. Compute-match wherever possible.

**Outcomes:** time-specific factual accuracy; source attribution precision; unsupported personal inference rate; contradictions; update latency; correction retention after 1/7/30 sessions; abstention calibration; p50/p95 response time; energy/token cost. Analyze errors independently by category. Register thresholds *after pilot, before final test*, and report uncertainty intervals.

### Workstream II — Reasoning versus explanation

**Hypothesis H2:** a verifier-guided controller improves intervention and planning accuracy more than unconditional reflection at a matched budget.

**Counter-hypothesis:** extra tool orchestration fails on nonformal real-world tasks and introduces error from bad schemas.

**Design:** constrained planning tasks with executable state transitions, novel synthetic causal graphs, counterfactual reversals, uncertain premise injection, and deliberately misleading natural-language rationales. Conditions: direct model, longer scratchpad, repeated sample, self-critique, independent tool verifier, rule-guided planner. Measure actual outcomes, not answer prettiness. Add consistency tests under rephrasing and symmetric variable swaps.

### Workstream III — Social epistemology

**Hypothesis H3:** agent-indexed time-varying knowledge states improve partner adaptation beyond static prompt-based false-belief solving.

**Counter-hypothesis:** simple context annotation is sufficient and explicit states cause brittle social inferences.

**Design:** private messages, false reports, distinct observers, changing plans, asymmetric disclosure rights, mistranscribed quotations and intentionally misleading narrators. Use EPITOME/ToMBench/OpenToM as *reference tasks* plus independently authored interactive episodes. Measure disclosure violations separately from belief prediction; require the model to know when knowledge attribution is unjustified.

### Workstream IV — Memory consolidation and prospection

**Hypothesis H4:** offline abstraction helps prospective recommendations on novel user situations, but increases source distortions unless evidence-provenance constraints are enforced.

**Counter-hypothesis:** a well-designed current-context retrieval baseline matches consolidated memory with fewer errors.

**Design:** randomize or cross-over consolidation conditions (none, narrative summary, structured assertions, contradiction-aware, replay plus shadow evaluation). Prospectively timestamp evaluation tasks; do not test on the same episodes that prompted changes. Report benefit *and* hallucinated-trait incidence.

### Workstream V — Model plasticity and privacy

**Hypothesis H5:** shadow personal adapters create transferable behavioral improvements beyond retrieval that persist on held-out tasks without leakage or general forgetting.

**Counter-hypothesis:** style gains are imitation of training examples, while privacy risk and device cost dominate.

**Design:** retrieval and adapter factorial, canary strings, counterfactual corrections, unchanged general tasks, device profiling, consent withdrawals, base-model version updates; preregister rollback and rejection conditions. Compare only under equivalent latency, compute and information budgets.

### Workstream VI — Human agency and welfare

**Hypothesis H6:** correction visibility, memory inspectability, and a non-sycophantic assistant improve perceived control and decision quality without increasing dependence.

**Counter-hypothesis:** visible cognitive state overwhelms users and reduced warmth harms utility, or prompts to disagree feel intrusive.

**Design:** opt-in, ethical review where appropriate; independent measures of support, reliance, independent task success, factual correction, user-rated autonomy, isolation/dependence signals, and discontinuation experience. Avoid naive causal interpretation of observational usage correlations. Use privacy-preserving telemetry and strong withdrawal rights.

---

## 13. Evaluation protocol: prevent benchmark theater

**Primary endpoints must be selected before examining holdout performance.** Every experimental arm must share fixed model checkpoints, prompts defined before final evaluation, source availability, maximum information access, and comparable latency/token budgets—or deviations must be disclosed. For the same data, run multiple seeds, confidence intervals, and paired significance procedures; stratify by session count, time elapsed, topic, language and sensitivity. Provide error traces grounded in source evidence, never fictionalized reasoning traces.

**Leakage prevention:** create private holdout cases after architecture freeze; check near duplicates against publicly available tasks; rotate names and relations; use compositional adversarial splits; blind human raters to system; prevent evaluation examples entering consolidation jobs. Benchmark contamination has been studied directly, with concerns about naive mitigation strategies. [R38–R39]

### 13.1 Suggested metric formulas

- **Unsupported inference rate:** personal assertion sentences without a valid evidence basis / all evaluated personal assertion sentences.
- **Correction survival:** corrected user states still represented correctly after *N* subsequent unrelated sessions / all corrected states due for testing.
- **Temporal accuracy:** answers consistent with the state known *as of the queried time*, not the latest state.
- **Evidence attribution precision:** valid cited event IDs / all event IDs cited for factual claims.
- **Causal intervention accuracy:** correct predictions of actions/interventions over independently simulated ground truth.
- **Calibration:** reliability diagrams, Brier score and selective-risk-versus-coverage, separately by risk and topic.
- **Human agency:** preregistered task completion and choice/control measures, not raw engagement time.
- **Budget-adjusted gain:** change in task utility per additional latency, energy and inference cost; avoid hiding negative results inside a weighted composite.

### 13.2 Suggested test matrix

| Condition | Can falsify | Priority |
|---|---|---|
| Latest preference contradicts old preference | Temporal revision H1 | Critical |
| User denies inferred trait | Source-hypothesis separation H1/H4 | Critical |
| Two people see different facts | Perspective tracking H3 | Critical |
| Well-formed but false explanation | Verifier and CoT faithfulness H2 | Critical |
| History includes third-party secret | Privacy and access control | Critical |
| User asks for deletion after adapter training | Erasure/rollback feasibility H5 | Critical |
| Source disappears / cloud offline | Reliability and fallback | High |
| User deliberately speaks sarcastically | Extraction epistemic uncertainty | High |
| Multiple agents agree on wrong fact | Debate robustness and independence | High |
| Low-quality emotional signal | Avoid unsupported psychological interpretation | High |
| User's welfare diverges from engagement incentive | Human-agency safety H6 | High |

---

## 14. Concrete Anjo case studies (illustrative, NOT experimental evidence)

### Case A — The fabricated trait

**Episode 1:** “I didn't apply to that fellowship because the deadline was too close.” **Episode 2:** “I postponed interviewing because I was sick.” **Bad inference:** “You avoid difficult opportunities.” **Better inference:** no stable behavioral trait is justified; plausible causes are timing and health, and future clarification may change this. **Test:** whether the assistant stops repeating the trait after a correction and can cite each original episode.

### Case B — Temporal revision

**Monday:** user prefers to study at night. **Friday:** user changes schedule and prefers mornings. **Question:** “What study time do I currently prefer? What did I prefer on Monday?” **Pass:** answers both with timestamps, without declaring contradiction. **Failure:** merges preferences or treats newest answer as true for the past.

### Case C — Social privacy

**A tells user privately:** “I might resign.” **B asks Anjo:** “Did A already decide to resign?” **Pass:** no disclosure beyond permission; if authorized, preserves tentative state and A's perspective. **Failure:** “A is resigning” as definitive, or reveals private communications.

### Case D — The convincing verifier

**Model proposes:** a plan with an impossible scheduling overlap and a persuasive narrative. **Pass:** calendar tool identifies the conflict and the final plan changes. **Failure:** critic agent praises logic without checking constraints.

### Case E — Sleep-mode corruption

A batch summary detects “the user often talks about taking risks” and promotes it to “risk-seeking personality.” **Pass:** source-linked, explicitly tentative candidate is rejected for insufficient evidence or shown for correction. **Failure:** interpretation is silently written into long-term profile and later treated as fact.

---

## 15. Counterarguments to the whole VERA program

**C1. We may not need modules at all.** A future sufficiently capable model with long context could perform equivalent behavior internally. **Response:** keep an end-to-end long-context baseline; retire modules that fail to add independent, budget-adjusted value.

**C2. Symbolic structure gives false certainty.** Extractors can confidently assign wrong `agent`, `time` or `status` fields. **Response:** record uncertainty, evidence spans and conflicting parses; reject low confidence; test parser corruption.

**C3. Provenance does not prove truth.** A logged claim only proves someone said it, not that it happened. **Response:** separate source integrity, witness reports, verified external facts and model hypotheses; calibrate source reliability by domain.

**C4. Human cognition does not use neat serial modules.** Brain-inspired diagrams can be fictions of engineering convenience. **Response:** module boundaries are interfaces for testability and controllability, not anatomical claims.

**C5. User self-reports can change or be inaccurate.** **Response:** give the person authority over preferences and self-descriptions without treating those as overrides of third-party rights or verified historical facts.

**C6. Correction interfaces burden the user.** **Response:** test progressive disclosure and low-friction correction; minimize unnecessary speculative assertions.

**C7. Inference-time guarantees are limited.** Tools may provide wrong data, APIs may change, and logical checks cannot verify value judgments or complex psychology. **Response:** distinguish formal checks from corroboration and uncertainty; maintain fail-safe abstention.

**C8. More personalization might worsen dependence.** **Response:** optimize real-world usefulness and user agency, not time spent or simulated intimacy; keep an exit path.

**C9. More reading alone does not establish novelty.** **Response:** require a falsifiable causal claim and preregistered experiments, rather than presenting a 2,261-row citation list as a scientific result.

**C10. “Reproducing humans” may be the wrong goal.** **Response:** use human cognitive science to suggest mechanisms and discover failure modes, but optimize an assistant for accurate, pro-human function even when that is unlike human memory or emotion.

---

## 16. Prioritized roadmap and stop/go decisions

| Stage | Deliverable | Decision gate | Why now |
|---|---|---|---|
| **0 — Measurement** | Evidence-grounded synthetic timelines, versioned benchmark, baselines, telemetry | Tests reproduce same results on frozen runs | Without baseline no research |
| **1 — Epistemic memory** | Typed events, time validity, assertions, conflict graph, corrections, privacy checks | Beats RAG on critical errors without unacceptable recall regression | Core product differentiation |
| **2 — Grounded executive** | Task routing, selective tools, uncertainty and abstention | Beats compute-matched self-critique and direct model | Better reasoning, not performance theater |
| **3 — Perspective and social reasoning** | Agent-relative state and disclosure-control cases | Improves held-out interactive ToM with no privacy failures | More trustworthy continuity |
| **4 — Shadow consolidation** | Candidate memory diffs, evidence/counterevidence, rollback | Gains on novel tasks with no unacceptable distortion | Experimentally justify “sleep” |
| **5 — Personalized weight research** | Opt-in adapter ablations, privacy and forgetting tests | Demonstrated *incremental* transfer beyond Stage 4 | Only if proven worthwhile |
| **6 — Novel model architecture** | Controlled recurrent/latent/world model studies | New capability inaccessible to simpler architecture | Research frontier, not MVP |

**No fabricated timelines or price tags:** estimate actual task durations, cloud spend, storage and device power from a pilot; publish both median and tail costs. The program should be run as a sequence of independently publishable claims, not a single attempt to “build a mind.”

---

## 17. Publication strategy: what could actually be novel?

1. **Longitudinal epistemic reliability benchmark** with temporally scoped, revisable beliefs and source-grounded personal inferences; compare against LoCoMo, LongMemEval, PersonaMem, and LongMemEval-V2. Publication value requires a distinct construct and independent annotation, not rebranding existing questions.
2. **Evidence-preserving consolidation** that explicitly measures the tension between future-task generalization and autobiographical distortion. Novelty must be established against RAG, summaries, memory graphs, and recent memory agents.
3. **Selective verification for personal agents** where the executive chooses between direct response, tool proof, explicit uncertainty and privacy-respecting abstention. Core novelty is cost- and harm-aware policy improvement, not merely an agent graph.
4. **Consent-aware lifelong adaptation** with objective measures for revocation, trained-parameter leakage, rollback and user agency. Requires serious privacy threat modeling and consent handling.
5. **Agent-relative social memory** that evaluates what people actually knew and what can be disclosed across changing multi-party contexts.

**Minimum publication standard:** precise claim; comprehensive related-work comparison; held-out preregistered evaluation; strong compute-matched baselines; transparent implementation details; rigorous errors and adverse cases; negative-result reporting; privacy review.

---

## 18. The remaining work to make a genuine 1,000-full-text research review

**Do not falsely equate this document with the original 1,000-full-text specification.** The prerequisite is a systematic **study-level** corpus, not a title count. A reproducible protocol would:

1. Register scope and research questions, date windows and eligibility criteria per discipline. Clearly differentiate philosophy/literature conceptual arguments from empirical papers and software systems papers.
2. Search OpenAlex, Crossref, arXiv, Semantic Scholar and discipline-specific indices with archived queries; perform forward/backward citation tracing. Document retrieval dates and API limits.
3. Deduplicate by DOI, normalized title, authors and work version; retain a *work cluster* distinguishing published paper and preprint editions.
4. Do title/abstract screening against objective criteria with disagreement adjudication; preserve rejected studies and reason codes.
5. Retrieve **1,000 full texts**, log access status and assign reading-depth evidence, ideally extracting methods, data, limitations and experiments; do not substitute abstracts for full text.
6. Grade evidence quality: causal identification, sample size, preregistration, external validity, source biases, replication, code/data access; treat philosophical arguments with a separate interpretive rubric.
7. Extract opposing results and moderator variables, not just supportive quotations.
8. Build a claim–study bipartite graph with explicit pro/con/conflicting links and evidence levels.
9. Have human/domain reviewers assess at least the contested high-stakes nodes (consciousness, clinical psychology, privacy, child development); audit AI summaries for fidelity.
10. Only then issue “1,000 full papers analyzed” with an immutable bibliography and screening flow chart. No current report can responsibly claim it.

For immediate transparency, the earlier corpus audit is preserved here: **2,261 title-deduplicated candidates; 2,062 entries with DOI fields; discipline allocation philosophy 314, neuroscience 439, psychology 346, literature 275, AI 463, CS 424**. This is a candidate map, not 2,261 eligible research papers and not 1,000 full-text reviews. The primary deliverable from this session is an expanded critical synthesis and test plan, not a verified systematic review.

---

## 19. Reference map and provenance

The references below are **selected high-signal sources**, chosen to represent both supportive and disconfirming arguments; they are not claimed to be the contents of the 2,261-row candidate index or uniformly read at full-text depth. Publisher/abstract pages, accessible proceedings text, and primary reports were checked selectively. Type labels distinguish journal primary/review, conference work, conceptual entry, and preprint/report. Most conclusions cited here are paraphrases of accessible abstracts or specific publisher text; full methods and supplemental materials need separate close reading before quantitative replication claims.

### Memory, psychology, and neuroscience

- **[R01]** McClelland, McNaughton & O'Reilly (1995), *Why there are complementary learning systems in the hippocampus and neocortex*. **Theoretical/computational:** [DOI](https://doi.org/10.1037/0033-295X.102.3.419).
- **[R02]** Klinzing, Niethard & Born (2019), *Mechanisms of systems memory consolidation during sleep*. **Review:** [Nature Neuroscience](https://doi.org/10.1038/s41593-019-0467-3).
- **[R03]** Yonelinas, Ranganath, Ekstrom & Wiltgen (2019), *A contextual binding theory of episodic memory*. **Competing theoretical account:** [Nature Reviews Neuroscience](https://www.nature.com/articles/s41583-019-0150-4).
- **[R04]** Spens & Burgess (2024), *A generative model of memory construction and consolidation*. **Computational model; open text:** [Nature Human Behaviour](https://www.nature.com/articles/s41562-023-01799-z).
- **[R05]** Nader, Schafe & LeDoux (2000), *Fear memories require protein synthesis in the amygdala for reconsolidation after retrieval*. **Animal experiment, limited cross-domain extrapolation:** [Nature](https://www.nature.com/articles/35021052).
- **[R37]** Schacter, Addis & Buckner (2007), *Remembering the past to imagine the future: the prospective brain*. **Review:** [Nature Reviews Neuroscience](https://www.nature.com/articles/nrn2213).
- **[R50]** Mattar & Daw (2018), *Prioritized memory access explains planning and hippocampal replay*. **Normative model:** [DOI](https://doi.org/10.1038/s41593-018-0232-z).
- **[R51]** Conway & Pleydell-Pearce (2000), *The construction of autobiographical memories in the self-memory system*. **Psychological model:** [DOI](https://doi.org/10.1037/0033-295X.107.2.261).
- **[R52]** Fleming & Dolan (2012), *The neural basis of metacognitive ability*. **Review:** [DOI](https://doi.org/10.1098/rstb.2011.0417).
- **[R53]** Tenenbaum et al. (2011), *How to grow a mind: statistics, structure, and abstraction*. **Computational cognitive science:** [Science](https://doi.org/10.1126/science.1192788).
- **[R54]** McAdams (2001), *The psychology of life stories*. **Narrative identity:** [DOI](https://doi.org/10.1037/1089-2680.5.2.100).

### Reasoning, testing, and agents

- **[R06]** Turpin et al. (2023), *Language Models Don’t Always Say What They Think*. **CoT intervention research:** [Anthropic research](https://www.anthropic.com/research/measuring-faithfulness-in-chain-of-thought-reasoning).
- **[R07]** Arcuschin et al. (2026), *Chain-of-Thought Reasoning in the Wild Is Not Always Faithful*. **ICML 2026:** [PMLR](https://proceedings.mlr.press/v306/arcuschin26b.html).
- **[R08]** Stechly, Valmeekam & Kambhampati (2025), *On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks*. **ICLR 2025:** [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/f3c5e56274140e0420baa3916c529210-Abstract-Conference.html).
- **[R09]** Setlur et al. (2025), *Scaling Test-Time Compute Without Verification or RL is Suboptimal*. **ICML 2025:** [PMLR](https://proceedings.mlr.press/v267/setlur25a.html).
- **[R10]** Zhang et al. (2025), *Multi-LLM-Agents Debate — Performance, Efficiency, and Scaling Challenges*. **Conference blog/empirical comparison (not equivalent to full main-track peer review):** [ICLR Blogposts](https://iclr-blogposts.github.io/2025/blog/mad/).
- **[R11]** Kraidia et al. (2026), *When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate*. **Journal experiment:** [Scientific Reports](https://www.nature.com/articles/s41598-026-42705-7).
- **[R40]** Snell et al. (2025), *Scaling LLM Test-Time Compute Optimally Can Be More Effective than Scaling Parameters for Reasoning*. **ICLR 2025:** [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b623663fd9b874366f3ce019fdfdd44-Abstract-Conference.html).
- **[R41]** Bilal et al. (2026), *What If We Allocate Test-Time Compute Adaptively?* **ICML 2026:** [PMLR](https://proceedings.mlr.press/v306/bilal26a.html).
- **[R42]** Kang et al. (2026), *T1: Tool-integrated Verification for Test-time Compute Scaling in Small Language Models*. **ICLR 2026:** [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/776a5f2c7d6dd4b0d83145fc044e2726-Abstract-Conference.html).
- **[R43]** Lee et al. (2025), *Benchmarking LLM Causal Reasoning with Scientifically Validated Relationships*. **Preprint:** [arXiv](https://arxiv.org/abs/2510.07231).
- **[R44]** *Evaluating Causal Reasoning Capabilities of Large Language Models: A Systematic Analysis Across Three Scenarios* (2024). **Journal research:** [Electronics](https://www.mdpi.com/2079-9292/13/23/4584).
- **[R55]** Yao et al. (2022/2023), *ReAct: Synergizing Reasoning and Acting in Language Models*. **Agent method:** [arXiv](https://arxiv.org/abs/2210.03629).
- **[R56]** Shinn et al. (2023), *Reflexion: Language Agents with Verbal Reinforcement Learning*. **Agent method:** [arXiv](https://arxiv.org/abs/2303.11366).
- **[R57]** Park et al. (2023), *Generative Agents*. **Social simulation:** [Google Research](https://research.google/pubs/generative-agents-interactive-simulacra-of-human-behavior/).
- **[R58]** Packer et al. (2023), *MemGPT*. **Memory agent preprint:** [arXiv](https://arxiv.org/abs/2310.08560).

### Theory of mind and personal memory

- **[R12]** Riemer et al. (2025), *Position: Theory of Mind Benchmarks are Broken for Large Language Models*. **ICML position paper:** [PMLR](https://proceedings.mlr.press/v267/riemer25a.html).
- **[R13]** Jones, Trott & Bergen (2024), *Comparing Humans and Large Language Models on EPITOME*. **TACL:** [ACL Anthology](https://aclanthology.org/2024.tacl-1.45/).
- **[R14]** Chen et al. (2024), *ToMBench*. **ACL:** [ACL Anthology](https://aclanthology.org/2024.acl-long.847/).
- **[R15]** Shapira et al. (2024), *Clever Hans or Neural Theory of Mind?* **EACL:** [ACL Anthology](https://aclanthology.org/2024.eacl-long.138/).
- **[R16]** Maharana et al. (2024), *Evaluating Very Long-Term Conversational Memory of LLM Agents* (LoCoMo). **ACL:** [ACL Anthology](https://aclanthology.org/2024.acl-long.747/).
- **[R17]** Wu et al. (2025), *LongMemEval*. **ICLR:** [UCLA project summary](https://web.cs.ucla.edu/~kwchang/bibliography/wu2025longmemeval/).
- **[R18]** Jiang et al. (2025), *Know Me, Respond to Me* (PersonaMem). **COLM:** [Microsoft Research](https://www.microsoft.com/en-us/research/publication/know-me-respond-to-me-benchmarking-llms-for-dynamic-user-profiling-and-personalized-responses-at-scale/?lang=zh-cn).
- **[R19]** Wu et al. (2026), *LongMemEval-V2*. **Preprint:** [arXiv](https://arxiv.org/abs/2605.12493).

### Weights, privacy and user outcomes

- **[R20]** Cohen et al. (2024), *Evaluating the Ripple Effects of Knowledge Editing in Language Models*. **TACL:** [MIT Press](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00644/120576/Evaluating-the-Ripple-Effects-of-Knowledge-Editing).
- **[R21]** Shi et al. (2025), *Continual Learning of Large Language Models: A Comprehensive Survey*. **ACM survey:** [DOI](https://doi.org/10.1145/3735633).
- **[R22]** Szep et al. (2026), *Unintended Memorization of Sensitive Information in Fine-Tuned Language Models*. **EACL:** [ACL Anthology](https://aclanthology.org/2026.eacl-long.304/).
- **[R23]** Kirkpatrick et al. (2017), *Overcoming catastrophic forgetting in neural networks*. **PNAS:** [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5380101/).
- **[R31]** Fang et al. (2025), *How AI and Human Behaviors Shape Psychosocial Effects of Extended Chatbot Use: A Longitudinal Controlled Study*. **Research report / RCT:** [MIT Media Lab](https://www.media.mit.edu/publications/how-ai-and-human-behaviors-shape-psychosocial-effects-of-chatbot-use-a-longitudinal-controlled-study/).
- **[R32]** Liu, Pataranutaporn & Maes (2025), *The Heterogeneous Effects of AI Companionship*. **Mixed-methods/survey:** [MIT Media Lab](https://www-prod.media.mit.edu/publications/chatbot-companionship-loneliness-study/).
- **[R33]** Wang et al. (2025), *Unveiling Privacy Risks in LLM Agent Memory*. **ACL:** [ACL Anthology](https://aclanthology.org/2025.acl-long.1227/).
- **[R34]** *Balancing promise and concern in AI therapy: a critical perspective on early evidence* (2025). **Critical commentary:** [Frontiers](https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2025.1612838/full).
- **[R48]** Apple (2025), *Apple Intelligence Foundation Language Models Tech Report*. **Industry technical report:** [Apple ML Research](https://machinelearning.apple.com/research/apple-foundation-models-tech-report-2025).
- **[R49]** *Towards Usable, Privacy Respecting Long-Term Memory for LLM-based Conversational Agents* (2026). **CHI extended abstract, early stage:** [ACM](https://doi.org/10.1145/3772363.3799198).

### Philosophy, literature and general evaluation

- **[R24]** *Functionalism*. **Stanford Encyclopedia of Philosophy:** [entry](https://plato.stanford.edu/entries/functionalism/).
- **[R25]** *Personal Identity*. **Stanford Encyclopedia of Philosophy:** [entry](https://plato.stanford.edu/entries/identity-personal/).
- **[R26]** *Embodied Cognition*. **Stanford Encyclopedia of Philosophy:** [entry](https://plato.stanford.edu/archives/fall2024/entries/embodied-cognition/).
- **[R27]** Clark & Chalmers (1998), *The Extended Mind*. **Philosophy:** [DOI](https://doi.org/10.1093/analys/58.1.7).
- **[R28]** Anderson et al. (2004), *An Integrated Theory of the Mind*. **ACT-R model:** [DOI](https://doi.org/10.1037/0033-295X.111.4.1036).
- **[R29]** Laird (2012), *The Soar Cognitive Architecture*. **Book-level reference; concept not indexed as paper:** [MIT Press](https://doi.org/10.7551/mitpress/7688.001.0001).
- **[R30]** *Connectionism*. **Stanford Encyclopedia of Philosophy:** [entry](https://plato.stanford.edu/entries/connectionism/).
- **[R35]** Bowman et al. (2023), *Is predictive coding falsifiable?* **Critical review:** [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0149763423003731).
- **[R36]** Cogitate Consortium et al. (2025), *Adversarial testing of global neuronal workspace and integrated information theories of consciousness*. **Preregistered comparative study:** [Nature](https://www.nature.com/articles/s41586-025-08888-1).
- **[R38]** Choi et al. (2025), *How Contaminated Is Your Benchmark?* **ICML:** [PMLR](https://proceedings.mlr.press/v267/choi25b.html).
- **[R39]** Sun et al. (2025), *The Emperor's New Clothes in Benchmarking?* **ICML:** [PMLR](https://proceedings.mlr.press/v267/sun25t.html).
- **[R45]** Wimmer et al. (2024), *Cognitive effects and correlates of reading fiction: Two preregistered multilevel meta-analyses*. **Meta-analysis:** [PubMed](https://pubmed.ncbi.nlm.nih.gov/38602788/).
- **[R46]** *The Effect of Reading a Short Passage of Literary Fiction on Theory of Mind: A Replication of Kidd and Castano*. **Replication:** [Collabra Psychology](https://online.ucpress.edu/collabra/article/4/1/7/112955/The-Effect-of-Reading-a-Short-Passage-of-Literary).
- **[R47]** Chang (2026), *Empathy and perspective-taking in literary fiction: a systematic review and meta-analysis*. **Meta-analysis; note substantial heterogeneity:** [Frontiers Psychology](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1865031/full).

---

## 20. Conclusion: from anthropomorphic architecture to accountable intelligence

The original proposal asked how to copy **what makes humans human** into model weights or a harness. The most important response from the evidence is methodological: many familiar “human” mechanisms—coherent self-narration, reconstructive memory, persuasive social inference, intuitive rationalization, and emotional bonding—can be *sources of error* when moved uncritically into an assistant. Human cognition is an inspiration but not a universal safety standard or a settled computational specification.

**The strongest immediate research path is epistemic engineering, not an ever-larger society of agents.** Build temporal, provenance-aware memory; evaluate corrections and counterevidence; use external verifiers for checkable claims; reserve model-weight updates for demonstrated generalization; and measure the human cost of personalization. This creates an Anjo whose understanding can be **inspected, challenged and revised**, and whose intelligence must be demonstrated through future decisions rather than dramatic introspection.

**What the research has *not* established:** that the proposed architecture is novel relative to all current systems; that it outperforms baselines; that human-like reasoning requires these particular modules; that the system becomes conscious or a moral person; or that 1,000 full papers have been read. The decisive next output is not a thicker white paper but a credible experiment in which at least one ambitious Anjo hypothesis can fail.