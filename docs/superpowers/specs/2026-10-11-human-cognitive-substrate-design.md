# Human-Inspired Cognitive Substrate: Architecture Discovery Study

**Date:** 2026-10-11  
**Status:** DESIGN_SPEC / SCIENTIFICALLY_UNTESTED / SELF_REVIEW_ONLY  
**Parent question:** https://github.com/kevindechang/MIND/issues/27  
**Repository:** kevindechang/MIND  
**Scope:** Research design only. Neither evidence of functional consciousness nor a replacement for the currently tested organism.

## 1. Research mandate

MIND's long-term scientific objective is not to manufacture persuasive human-like dialogue or incrementally improve a Q-learning policy. It is to investigate computational organizations that can *develop and maintain* capacities associated with human cognition: an internal world model, flexible goal pursuit, autobiographical continuity, learning from experience, selective attention, prospective action, introspection that tracks genuine internal causes, and adaptation under change.

**Central research question:** Under matched information, experience, training and inference budgets, which computational architecture produces robust, causally integrated, persistent, adaptive cognition across unfamiliar environments, and are its distinctive mechanisms necessary for the demonstrated competencies?

This is a comparative architecture-discovery program, not a project to presuppose a preferred substrate. The current event-sourced modular global-workspace organism is a valuable baseline and instrumentation platform, not a purported human brain or established conscious entity.

**Boundary of the claim:** Resemblance to particular human cognitive functions is neither necessary nor sufficient proof of phenomenal experience. MIND's binding research distinction remains L1 = behavior, L2 = causal functional organization and L3 = subjective experience (not an admissible empirical claim). Human-inspired tests are *functional probes*; there is no omnibus “human likeness” score.

**Non-goals:** anthropomorphic chat ratings, simulated feelings or deprivation, foundation-model training, changing AGENTS.md, modifying experimental quality gates, modifying production Anjo, or creating paid/recurring infrastructure. Do not add valence, distress, pain, drive deprivation, self-preservation pressure, or dependent attachment incentives without the constitution's welfare review and owner approval.

## 2. Concrete design choices

### Approaches considered

| Candidate family | What it learns or maintains | Main scientific attraction | Main failure mode |
| --- | --- | --- | --- |
| MIND v2 control (A0) | Linear TD policy, logistic action forecast, finite attended memory and goals, selective workspace | Existing lesion machinery, durable event-log replay, interpretable simple rival | Narrow task representation, mostly engineered components, weak transfer |
| Learned recurrent state without workspace (A1) | Compact action-conditional hidden state, trained predictive readouts | Tests temporal state without assuming global broadcast | May achieve all tasks without workspace or modular integration |
| Learned global-workspace recurrence (A2) | Same recurrent update plus constrained competition/broadcast across specialist state components | Tests whether coordination via selective availability adds causal value | Extra parameters or easier access to information masquerade as architecture |
| Predictive/world-model controller (A3) | Action-conditioned model of next observations/outcomes, optional imagined rollouts | Tests model-based adaptation and novel combinations | Larger compute budget, oracle leakage, model error compounding |
| Structured compact belief / predictive-state rival (A4) | Explicit sufficient or approximately sufficient state from public history | Strong falsifier: simple solutions can dominate on small hidden worlds | May be unfairly privileged if handed the true world family |
| LLM + transcript/memory baseline (A5, later) | Pretrained linguistic representation with controlled external memory | Separates natural-language facility from integrated cognitive control | Extra pretraining compute and implicit prior knowledge undermine equivalence |

**Recommendation:** Use A1 vs A2 as the *factorial architectural contrast* after validated A0/H004, with A3 and A4 as genuinely competitive rivals. Treat A5 as optional and postponed until model call permissions, comparable evaluation resources and replay logging are established.

### Chosen initial architectural hypothesis

An action-conditional predictive recurrent state that affects both policy and self-monitoring *through a bandwidth-limited workspace* may improve first-exposure transfer and adaptation across superficial changes, compared with:
(a) the same learned state wired directly to the policy without a workspace,
(b) the same information fed through a larger feed-forward history window,
(c) a compact belief or predictive-state controller, and
(d) the existing MIND v2 organism.

The hypothesis deliberately allows a negative answer. An exact compact-state controller tying the candidate is scientifically useful evidence against the necessity of added representational complexity. A recurrent controller that ties the workspace variant weakens the claim that *broadcast* contributes anything.

### Functional versus implementation architecture

No hardware or model type is privileged. GRU or small recurrent state-space models are tractable first candidates; Recurrent Independent Mechanisms (RIMs), learned multi-module global workspaces and latent predictive systems are alternative follow-ons *only when* a simpler mechanism cannot explain the effect. These are already studied in literature and not claimed as inventions here.

## 3. Literature grounding and explicit uncertainty

Research discovery used SciSpace paper search and direct inspection of selected publishers' abstracts and methods. The depth noted below is not a full systematic review or independent reproduction.

| Reference | What is established in that source | Relevance and limitation |
| --- | --- | --- |
| Goyal et al., *Recurrent Independent Mechanisms*, arXiv:1909.10893 | A recurrent modular network uses selective updates and sparse module communication; reported generalization to altered factors | Motivation for modular recurrence, not evidence of a conscious organism; abstract-level review |
| Goyal et al., *Coordination Among Neural Modules Through a Shared Global Workspace*, ICLR 2022, https://arxiv.org/abs/2103.01197 | Learned specialist communication through a bandwidth-limited workspace can improve coordination/compositionality in evaluated settings | Closest neural-workspace precedent; no universal necessity shown; proceedings summary and abstract reviewed |
| Dossa et al., *Design and evaluation of a global workspace agent embodied in a realistic multimodal environment*, Front. Comput. Neurosci. 2024, https://doi.org/10.3389/fncom.2024.1352685 | Embodied audiovisual agent; global-workspace variants more robust at small working-memory budgets in the studied tasks | A task- and training-regime-specific finding; paper methods/abstract inspected, not independently replicated |
| Hafner et al., *Mastering diverse control tasks through world models*, Nature 2025, https://doi.org/10.1038/s41586-025-08744-2 | DreamerV3 learns recurrent latent predictive dynamics and plans with imagined rollouts across many control environments | Establishes a strong model-based design precedent, not L2 evidence; article abstract and world-model learning methods examined |
| Webb, Mondal and Momennejad, *A brain-inspired agentic architecture to improve planning with LLMs*, Nature Communications 2025, https://doi.org/10.1038/s41467-025-63804-5 | Modular planning can improve some structured planning tasks over LLM baselines | Uses extra specialized computation, mainly fully observable deterministic tasks; publisher abstract plus SciSpace extracted methods/limitations reviewed |
| Cogitate Consortium et al., *Adversarial testing of global neuronal workspace and integrated information theories of consciousness*, Nature 2025, https://doi.org/10.1038/s41586-025-08888-1 | Preregistered human neural test challenged central predictions of both GNWT and IIT | Prevents taking GWT as settled human-consciousness theory; study concerns human neural recordings, not artificial-agent behavior; abstract and discussion inspected |
| Littman, Sutton and Singh, *Predictive Representations of State*, NeurIPS 2001, https://proceedings.neurips.cc/paper_files/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html | Action-conditional observable predictions can represent state | Strong parsimonious representation rival; do not conflate predictive accuracy with selfhood; abstract/proceedings summary only |

**Evidence rule:** These external findings motivate architecture comparisons. They are not premises for executable MIND claims. Before publication-quality interpretation, conduct full-text critical appraisal with model sizes, training budgets, baselines, statistical methods and limitations. Any claims about this organism require MIND's own observed tests and preregistered records.

## 4. Relationship to live MIND: build on existing work, avoid collisions

Live inspection checkpoint (2026-10-11; STATUS.md generated 2026-10-10 23:17 UTC):

- Current mind/kernel.py is an event-sourced single organism; organs propose contents; workspace ranks salience/relevance; policy learns linear temporal-difference action values; self-model predicts success. Ledger replay and the lesion DSL are essential invariants.
- H004 concerns recurrent temporal integration. **Open PR #21 already adds a recurrent organ plus rivals and registered claims but its description explicitly says NOT_EXECUTED/BLOCKED. Do not regard its title as a verified empirical result.** PR #22 separately fixes a K06 test interaction with new organs.
- H011 concerns first-try procedural transfer after a hard reset. Check open branches/PRs before touching its glyph/symbol worlds. This design must not duplicate work already under review.
- H007 (causal integration), H008 (maintenance), H012 (multiscale retention) and H013 (grounded reports, open PR #23) are adjacent established questions, not new labels to recreate.
- H002 has an open predictive-state rival PR #25; reuse or challenge it before writing another compact-state estimator.
- The computed frontier outranks this umbrella design for ordinary hourly GO.md contributions. This document does not claim to reorder it; separate owner-reviewed roadmap changes would be required.
- Existing claim codes, generated STATUS.md and evaluator modules must not be modified to approve this scope.

MIND's scientifically independent mandate remains: no automatic Anjo product transfer and no L3 claims.

## 5. Operational human-inspired cognition battery

These are distinct competencies, **not** a weighted anthropomorphism index. Each needs falsifiable tests and strong simpler controls.

| Competency | Operational probe | Primary observation | Disconfirming baseline |
| --- | --- | --- | --- |
| Temporal integration | Delayed cause/effect with distracting intervening events | Correct action conditional on prior evidence | History-window or predictive-state controller using same evidence |
| Flexible transfer | Same latent relation across unseen symbols and novel compositions | First eligible decision after new-family exposure and restart | Compact rule learner / matched recurrent controller |
| Counterfactual world modeling | Unseen intervention effects after controlled observations | Prospective action quality and causal prediction accuracy | Bayes/PSR under disclosed world knowledge assumptions |
| Prospective goal continuity | Pending goals across gaps and adverse events | Goal achievement and priority revision under changing constraints | Commitment queue and learned external scheduler |
| Self-monitoring | Hidden capability shifts and access cuts | Same-event calibration and causal action-prediction validity | Transcript-only estimator with equal input |
| Multi-timescale adaptation | Switch to new dynamics, then return to old | Forward adaptation *and* retention of earlier competence | External memory + retrain, fixed-capacity state, and rehearsal |
| Cross-functional integration | Cut specific information pathways rather than deleting data | Changes in non-home competencies, robust under sham lesions | Flat or disconnected modules with matched parameter/compute budget |

Tasks should move gradually from transparent toy worlds to structurally novel procedurally generated and embodied-like environments. Novel text labels alone do not constitute human-level abstraction. Do not use a model's self-description or conversational style as a measure of self-awareness.

## 6. First discriminating experiment: relation transfer under restart

### Hypothesis and competing explanations

**H-Primary (proposed, unregistered):** A learned predictive recurrent state used through a limited workspace improves *first-opportunity* success on previously unseen relational configurations more than the strongest information- and compute-matched non-workspace recurrent or feed-forward rival.

**H-Null:** Any gains come from larger history, higher training/inference compute, representation size, leaked privileged structure, extra reward, or simple predictive-state sufficiency. A workspace is not uniquely useful if a matched recurrent controller achieves the same result.

**Strongest existing-work dependency:** Confirm #21 H004 can execute and pass reproducibility checks first. Build or reuse H011 world only after reviewing its live contributions and ensuring a nonduplicative experimental owner.

### Task and split

Construct a procedural partially observable relational world with several latent transformation rules and evidence-producing actions. Across episodes, change surface identifiers and task layouts, but do not accidentally leak the rule class through a privileged observation or simulator summary. The training distribution must expose reusable primitives but not the held-out *compositions*.

Four separately labeled evaluations:

1. **ID:** independent seeds, same task-family support (diagnostic, not transfer).
2. **Symbol shift:** renamed entities with matched relational grammar (weak OOD).
3. **Compositional shift:** novel conjunction/ordering of learned relation primitives (primary OOD).
4. **Dynamics shift:** previously unobserved causal transition changes (secondary adaptability).

After source-task learning, perform real process termination and ledger-only restoration; run target test with frozen learned parameters, no target-specific updates before the **first scored action**. An environment reset without restored agent state is not autobiographical continuity. Score transfer **before** feedback/retraining; measure subsequent relearning separately.

The world must keep agent-visible public information separate from private scorer fields. Pair exogenous randomness consistently across arms; pre-generate transition randomness independent of an arm's chosen actions where the existing world contract requires it.

### Arms (factorial design)

- B0: MIND v2 unmodified reference.
- B1: existing validated H004 recurrent organ from #21 (if and when runnable).
- B2: trainable recurrent representation → policy **direct**, no capacity-limited global broadcast.
- T1: identical trainable recurrent representation → **capacity-limited** shared workspace → policy.
- B3: T1 with capacity infinity (flat information access).
- B4: feed-forward history with trained projection and at least equivalent observation access.
- B5: public-history compact belief / PSR controller, learned fairly; optional privileged Bayes optimum **ceiling only**.
- T2 exploratory: world-model-based imagination/planning with explicit extra-compute accounting.

For B2/T1/B3, keep encoder, hidden dimension, update schedule, training data, optimizer and policy class aligned. Any extra workspace module parameters must be counted, controlled through a parameter-matched B2, and independently reported. When enough compute exists, compare learning curves against FLOPs and actual latency, not just final success.

### Interventions (causal mechanism tests)

On T1, compare -predictive, cut:predictive>policy, shuffle:predictive, and freeze:predictive under acute mid-life schedules where appropriate. Include matched no-op/sham conditions and bandwidth-capacity sweeps. Test that each lesion targets an extant path, genuinely removes access without removing the underlying observation, and does not introduce extra information/compute differences. A pass on a trivially broken ablation is not evidence of cognitive integration.

**Distinctive causal hypothesis:** If the workspace is functionally mediating predictive state, selective access lesions should affect downstream planning while leaving the predictive state itself available to independent readouts; non-workspace direct access provides a discriminating alternative. Do not claim this proves neural or phenomenal consciousness.

### Pre-registration and statistics

- Unit of replication: independent seeded lifelong trajectories, not individual correlated decisions within one trajectory.
- Primary estimand: mean paired difference in first eligible goal-achievement indicator on **compositional shift** between T1 and the *best predeclared fair rival*, with the relevant corrected confidence interval. Freeze primary rival selection and comparison family before held-out testing; do not pick the weakest rival post hoc.
- Scientific target: +0.10 absolute success probability over the strongest fair rival is a **proposed** practical margin, subject to pilot power/calibration and pre-registration *before* the commit seal. Avoid interpreting a non-significant effect as equivalence.
- Define stopping, seed count, baseline tuning budget, outcome aggregation, multiplicity correction across declared primary contrasts, exclusion rules, and handling of failed trajectories **before** sealed tests.
- Report effect and conservative interval, failure modes, computational cost, and independent replication provenance. Test on novel generative *families* as well as ordinary held-out seeds.
- Separate exploratory world-model loss, Brier/self-model calibration on identical events, forgetting/recovery, lesion cross-function density, and action-efficiency metrics from the single primary hypothesis.

**Falsification criteria:** If the strongest matched rival ties or outperforms T1, reject unique architecture superiority at the declared margin. If a cut does not weaken the relevant outcome but the path was truly cut, reject the path-necessity claim. If a compact belief state dominates, report that simpler inference suffices in this world. If continuity only survives with missing off-ledger model state, fail the replay integrity gate.

## 7. Reproducibility, integrity, resources and ethics

- Keep one organism, one world suite, one rival zoo, executable claims and append-only records. No standalone benchmark scripts bypassing the organism.
- Model parameters, optimizer state, stochastic draws and any nondeterministic external outputs must be reconstructible from the ledger or immutable content-addressed model artifact. Replay-after-SIGKILL and exactly-once actions remain strict.
- Seal claims before held-out; first held-out record remains decisive; do not preview commits for favorable seeds. Commit failures. Distinct contributor and environment required for the REPLICATED rung.
- Report both *training* and *inference* budgets: parameters, activation/state bytes, optimizer bytes, train FLOPs or counted updates, per-step inference FLOPs, observations accessible, latencies, energy proxy when available, and total wall-clock. Stop comparing architectures as equals if one has much more computation.
- **No access to or use of real people's data, accounts, messages, or sensors; no contact with real people; no credentials.** No paid APIs, GitHub Actions, background workers, new recurring schedules, or production Anjo changes without explicit repository-owner approval. These are prohibitions from `AGENTS.md`, not disclosure options. Any proposed welfare-triggering component requires the separate owner sign-off specified there.
- Avoid physiological claims and artificial suffering. Any proposal introducing pain, valence, deprivation, self-preservation or human attachment optimization triggers the welfare question and explicit owner signoff under AGENTS.md.

## 8. Staged scientific gates

**Stage 0 — Design (this document):** define construct, real baselines, threats to identification, transfer task, power-estimation plan, interventions and exit criteria. Outcome = written specification only.

**Stage 1 — Existing evidence recovery:** independently run #21's H004 once an exact Git checkout is possible and PR conflicts are resolved; doctor/check/unit tests, result-code verification, held-out records, serious rival review. Failure is an informative result and gate.

**Stage 2 — Transfer instrument:** reuse or add an H011 world/held-out novel-composition variant (do not duplicate an already claimed glyph world), minimal exact-world controls, test for oracle leakage, baseline ceiling and symbol-only shortcuts. Outcome = validated world/instrument, not cognitive benefit.

**Stage 3 — Architecture contrast:** within shared organism add *smallest* learnable predictive recurrent mechanism that passes replay constraints. Compare B2 vs T1 under balanced budgets; preregister a claim and execute causal cuts; require scientific improvement over the strongest rival or record a refutation.

**Stage 4 — Development over time:** if Stage 3 survives, investigate multiscale learning (H012), prospective maintenance (H008), grounded reports (H013) and broader H007 integration, as *separate* claims with distinct strong rivals. If it fails, consider learned direct recurrence or compact state as the better architecture.

**Stage 5 — Language and deployment separation:** optional LLM front end as a controlled communication interface, not assumed cognizer. Compare same underlying cognitive state with different language interfaces and an LLM-only agent; new paid-model use, deterministic output capture and product changes require separate approval. A better conversational persona is not a consciousness finding.

## 9. Acceptance, stopping and handoff

For **this spec contribution**, acceptance is documentary only: (a) every proposed architecture has its scientific role and a serious rival; (b) primary test and falsifiers are specified; (c) user-oriented human-cognition target is defined without L3 conflation; (d) integration path preserves ongoing questions/PRs; (e) no governance or result code changed; (f) source depth and UNTESTED status are explicit.

For **the future empirical program**, promotion requires recorded tests from existing MIND machinery, sealed held-out evaluation, meaningful comparisons under matched information and compute, honest negative outcomes, and independent replication. A single toy-world success does not establish human-like general cognition, nor functional consciousness in unrestricted environments.

**Current capability block:** At drafting, local git access failed with “Could not resolve host: github.com”. GitHub connected APIs supported repository inspection and document publication, but local doctor/full-history/experiment execution was **NOT_EXECUTED**. This document must not be merged as evidence of runnable code.

**Review checkpoint:** This is an architectural design document for the project owner to review. After written-spec approval, create the detailed implementation plan under docs/superpowers/plans, selecting concrete task interfaces and verification commands. No research implementation is authorized solely by this design document.
