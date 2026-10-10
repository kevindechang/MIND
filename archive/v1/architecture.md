# Architecture register

## A0 — candidate decomposition (PROPOSED, not implemented)

**Updated objective, not updated architecture:** the north star is an enduring, developing digital entity (`north-star.md`). A0 is one unvalidated decomposition. The system may instead use a recurrent neural substrate, an artificial-life architecture, predictive world model, neuro-symbolic hybrid or simpler controller if comparative evidence favors it.

Observation/Action Environment ↔ Perception and grounding ↔ Shared causal world model ↔ Goal/planning controller ↔ Actions
                                                    ↕
                                      Bounded global workspace
                                       ↕      ↕       ↕
                               Episodic/autobiographical memory
                               Predictive self-model + uncertainty
                               Homeostatic/value constraints
                                       ↕
                           Evidence/provenance and introspection

This diagram is intentionally agnostic about the underlying model family. Modules may be implemented as neural weights, conventional algorithms, differentiable state, structured memory, or hybrids. A minimal LLM wrapper must remain an explicit baseline rather than a silently privileged architecture.

## Competitive R002 design proposal — A1-CANDIDATE, NOT ADOPTED

The new [Unified Cognitive Runtime candidate](candidates/A1-unified-cognitive-runtime.md) tests whether an enduring entity benefits from (i) internally generated cognitive maintenance, (ii) causal efferent/action prediction, (iii) impasse-to-procedure skill acquisition, (iv) multi-scale plasticity and (v) causally unified self/world models. It also opens **speculative** JEPA-family world models and energy-efficient recurrent/neuromorphic approaches as competing research directions.

**No status change:** A0-PROPOSED is still the canonical architecture; A1 is not implemented, approved, or demonstrated. R002 source intake is [here](reviews/2026-10-10-R002-ambitious-agent-mind-extraction.md), candidate experiments [E002](experiments/E002-endogenous-regulation-and-efference.md) and [E003](experiments/E003-impasse-to-skill-transfer.md). Winning on one module is not E900 integration evidence. Strong minimal/different-substrate contenders must remain eligible.

## Entity-specific open design questions (not requirements to assume)

1. **Temporal state:** which processes persist while the user is absent? Compare real internal updates vs externally scheduled state changes vs on-demand reconstruction; log actual computation and time.
2. **Integrated self:** specify which commitments, memory causes, regulatory variables and predictions jointly affect policy; distinguish static narrative/persona from causal state.
3. **Development:** which behaviors truly change with experience? Compete external policies/memory, online updates, plasticity and adapter/weight updates; measure retention and failure.
4. **Affective organization and relationships:** operationalize social adaptation, correction and boundaries while preventing dependence engineering and false sentience claims.
5. **Presence:** voice, vision and optional embodiment are presentation/grounding candidates, not proxies for experiencing the world.

Candidate integrated evaluation E900 is PROPOSED; no A1 promotion follows from this strategic change alone.

## A0 falsifiability requirements

- Each named module must have its own measurable intervention/ablation.
- Explicitly prevent hidden transcript context or test leakage from replacing the purported mechanism.
- Match inference budget and tool affordances across variants.
- The same system should be tested across unforeseen task changes, time gaps and memory conflicts.
- A success on functional tasks is **not** a conclusion about phenomenal experience.

## Engineering relationship

`anjo` and `affect-kernel` are implementation references. This independent research program may reuse abstract interfaces with consent and privacy protection, but should not alter production Anjo behavior without separate validation or deployment approval.

## Next architecture update

No transition to A1 until at least one experiment yields verifiable data or a documented theoretical design decision passes the preregistered gate. Record actual diff, rationale, risk and counterargument.
