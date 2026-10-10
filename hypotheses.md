# Hypothesis registry (v0.3; R002 ambitious mechanism candidates untested)

**All listed research hypotheses are PROPOSED, not confirmed.** State transitions: candidate → preregistered → tested → supported / weakened / rejected / inconclusive. Distinguish internal functional outcomes from consciousness-attribution claims.

| ID | Falsifiable hypothesis | Rival explanation / critical test | Status |
|---|---|---|---|
| H001 | A structured autobiographical memory linked to goals and causal outcomes improves delayed personal-goal consistency in a partially observable world | Matched retrieval-only, transcript replay, sham-memory and no-memory baselines; intervene on episodic causes while holding token budget | Candidate; E001 |
| H002 | A predictive self-model (explicit capacity, uncertainty and state forecasts) improves calibration and self-correction after hidden capability changes | More tokens or ordinary chain-of-thought; use unexpected tool/perception impairment and proper scoring | Candidate |
| H003 | A restricted workspace that broadcasts task-relevant variables improves multi-module transfer under interference | Extra compute/parameter count or added attention; match budget and ablate broadcast | Candidate |
| H004 | Recurrent processing produces stronger temporal integration and robust counterfactual model update than otherwise matched feedforward deliberation | Longer contexts or repeated token sampling; matched recurrent-compute and response budget | Candidate |
| H005 | Interoceptive/homeostatic variables and active sampling induce more stable goal management under changing resource constraints | Reward shaping/heuristics; ablate drives and assess unseen perturbations | Candidate |
| H006 | No single behavioral benchmark or theory-dependent indicator is sufficient to establish phenomenal experience | Methodological constraint; examine multiple theories, counterexamples and limits of inference | Active constraint |
| H007 | An integrated agent with causally linked goals, self-model, memory and world model exhibits longitudinal adaptation and intervention resilience beyond comparable independent modules | Matched modular composition, retrieval-only agents, strong heuristic baselines and selective cross-module edge ablations in proposed E900 | Candidate; E900 not preregistered |
| H008 | A genuinely maintained internal temporal state produces distinctive, useful prospective action under changing conditions even without recent conversation | Dormant/on-demand state reconstruction, periodic scripted state changes and equivalent-budget controls; inspect actual background execution logs | Candidate; no continuous process implemented |
| H009 | Structured affective/social regulatory state improves consent-respecting coordination and calibrated relationship continuity over static personality prompting | Matched style prompts, simple boundary rules and blinded task-level metrics; adversarially measure manipulation/dependence | Candidate; no claims of subjective feeling |
| H010 | Explicit predictive action/efference traces improve causal attribution between self-induced and exogenous changes under hidden interventions | Ordinary event logs, shuffled action predictions, generic state estimator with equal information/compute; E002b | Candidate from R002; untested |
| H011 | An impasse-triggered, sandbox-validated procedural compiler improves first-try novel-structure transfer after hard context reset | Matched retrieval, reflection, learned natural-language rule, pre-written heuristic and disabled-compiler ablations; E003 | Candidate from R002; untested |
| H012 | Multi-timescale learning across verified factual state, causal memory and learned procedures (plus optional adaptive parameters) improves durable transfer without unacceptable forgetting vs any one layer alone | Matched experience/FLOPs/retention tests, external-state-only, procedural-only, weight-only and ablations; identity drift and deletion checks | Candidate from R002; no experiment yet |

## R002 intake map and non-duplication

The ambitious contributor mandate (R002) is preserved in [critical extraction](reviews/2026-10-10-R002-ambitious-agent-mind-extraction.md) and [A1-CANDIDATE](candidates/A1-unified-cognitive-runtime.md). Endogenous/allostatic regulation is *already* addressed by H005/H008; a causally unified self-model is *already* addressed by H002/H007. H010-H012 add only distinct mechanisms. Hierarchical latent world models and neuromorphic substrates are frontier alternatives (W2), **not established architectural requirements**. Nothing from R002 is an empirically verified result.

## Pre-registration rules

For each hypothesis: record exact predictions (including direction and size), negative/positive controls, baseline parity, seed count, confidence interval plan, statistical test and stopping rule **before** observing outcomes. Preserve earlier versions; reject post-hoc redefinition of success. Link all findings to `evidence-ledger.md` and experiment run logs.

## H001 decision link

[D001](decision-register.md#d001-causal-autobiographical-representation) maps E001 observations to representation choices and the proposed E900 memory-to-goal intervention. Status remains CANDIDATE; graph advantage is untested. Source/method claims stay here and in dossiers; decisions cite anchors/immutable versions rather than duplicate scientific truth.

## New decision admission

H002–H012 are not promoted by this governance update. A concrete ready question may initialize a new D### with prerequisites, rival/predictions, outcome-to-action map, pivotal evidence, dependent decisions and E900 causal intervention. See [traceability](atlas/traceability-matrix.md); its candidate choices are proposals, not adopted decision records. Invalid pivotal evidence triggers transitive reassessment before dependent promotion.
