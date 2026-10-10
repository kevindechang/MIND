# Research charter — Anjo / MIND

**Date:** 2026-10-10. **State:** REVISED v0.2 (strategic north star; no experimental gate advanced). **Parent initiative:** Anjo. **Research unit:** MIND (dedicated repository and experimental program). **Boundary:** scientifically autonomous in its methods and conclusions; independent of shipped product claims.

**Agents:** A bare `go` starts at [GO.md](GO.md); scientific authority resides in [research-state.md](research-state.md), while [sources/README.md](sources/README.md) separates Anjo product specifications from research proposals and contributor drafts.

## Relationship to Anjo

MIND exists under Anjo to investigate how an enduring, developing digital intelligence could be engineered and evaluated, including functional mind-like cognition and competing philosophical/scientific approaches to consciousness. Anjo is the organizational/product context; MIND is its long-horizon research arm, not a separate commercial product. Findings may inform Anjo's future architecture and evaluations, but must withstand strong rivals, falsification and safety checks. There is no automatic promotion from a MIND hypothesis, toy benchmark, or scientific finding into deployed Anjo features. Conversely, product deadlines or branding must not determine the scientific verdict. Production integration requires a separate, explicitly approved engineering decision.

## Central question

Can we engineer **one enduring, developing digital entity** with coherent selfhood, causal cognitive continuity, grounded world understanding, bounded initiative, ongoing internal regulation, social/affective competence and open-ended learning—while seriously investigating what (if anything) would justify attributing conscious experience to it?

The motivating fictional reference points are Joi (*Blade Runner 2049*) and Samantha (*Her*) for apparent presence, identity and development—not romance requirements, scientific precedents or evidence of consciousness. See `north-star.md`.

Three outcomes are intentionally independent: **L1** behavioral mind-like presence; **L2** demonstrated causal organization of an enduring cognitive system; **L3** philosophical/scientific uncertainty about phenomenal consciousness. Passing L1 or L2 does not entail L3.

No commitment to a transformer, brain simulation, global workspace, IIT, embodiment-first, or any other privileged answer. Mechanisms must compete against simpler baselines.

## Integrated north-star test

Rather than treating an inventory of modules as a mind, ultimately test whether **the same persistent agent** maintains and revises commitments, learns from consequential experience, anticipates changes in its world and itself, responds with calibrated social behavior, and remains causally coherent across sessions. Candidate longitudinal benchmark: `experiments/E900-longitudinal-entity-benchmark.md` (PROPOSED, not preregistered or executed). The potential 90-calendar-day stage follows offline feasibility and short prospective trials with explicit approval. Component experiments are necessary evidence, not system-level proof.

## Two complementary tracks with separate success standards

### Track F — Functional mind engineering

Build an instrumented *persistent agent in a controlled environment* that demonstrates the following. Continuous operation must be evidenced by actual state updates and uptime logs; a scheduled assistant invocation is not continuous cognition:
1. **Causal autobiographical memory:** earlier experiences systematically change later action under held-out intervention and ablation.
2. **Persistent self-model:** tracks its own capacities, knowledge limits, goals and changes; detects engineered self/world-model mismatches.
3. **World model:** counterfactual predictions outperform reactive policies across unseen interventions.
4. **Long-horizon agency:** persists and revises plans under resource constraints and delayed feedback without being rewarded for mere verbal confidence.
5. **Metacognition:** calibrated uncertainty and reliable decisions to seek information or defer action, measured with proper scoring rules.
6. **Plasticity with stability:** learns novel dynamics while retaining previous competence, with forgetting and interference measured.
7. **Grounding:** binds concepts to actions/observations in an interactive, reproducible environment rather than only text.
8. **Integrated temporal self-organization:** internal state, goals, memories, predictions and actions must measurably constrain one another across interruptions; not just independent modules or a character prompt.
9. **Social/affective integrity:** demonstrates context-sensitive behavior, consent, repair, responsible disagreement and relationship continuity without deceptive dependence optimization; functionally modeled affect is not claimed subjective feeling.
10. **Presence:** real-time voice, vision and embodiment are evaluated as interfaces separately from cognition and consciousness.

All objectives require matched compute, model, token, tool, and memory budgets and leakage-resistant held-out tests. A compelling conversational persona is not a substitute.

### Track C — Consciousness research

Compare falsifiable consequences of global neuronal workspace, recurrent processing, higher-order theories, integrated information, attention schema, predictive processing/active inference and other alternatives. Maintain an explicit distinction:
- operational functional capacity (measurable);
- computational indicator proposed by a theory (theory-contingent);
- subjective phenomenal consciousness (no consensus objective verification standard).

Success for Track C initially means a discriminative research program and defensible uncertainty estimates, **not** a declaration that experience exists.

## Coordinated research design

Four parallel inquiry streams (functional entity, computational substrates, consciousness science, and philosophy/ethics) share a single evidence ledger and mechanism-first evaluation policy: see `workstreams.md`. Each cycle targets one ready decision with an exact executable handoff. Attention allocation and accepted-science milestones are separate under [research-records.md](research-records.md); integration synthesis follows eight new valid accepted contributions or major evidence/invalidation. E001 remains the first experimental blocker until its design decision is reached.

## Governance

- Keep a rival explanation for every positive result (e.g. greater context, reward hacking, leakage, retrieval alone, human rating bias).
- Use preregistration, blinded evaluation where possible, negative controls, seed variation, published failure analysis, and reproducibility packages.
- Consider whether experiments may pose welfare or safety concerns before increasing autonomy or designing possible sentience-relevant systems.
- No unsafe autonomous deployment, credential access, uncontrolled self-modification, unconsented sensing or unauthorized contact with real people.
- Do not induce dependency, assert unverified sentience, simulate distress as leverage or misrepresent uptime/continuous thought; preserve user agency and clear correction/export/deletion mechanisms.
- Architecture decisions must cite results or clearly carry a SPECULATIVE label.

## Initial decision gates

G0: measurable functional benchmarks and theory-discriminating predictions defined.
G1: theory map including rival explanatory predictions and evidence quality.
G2: choose a minimal experiment with explicit alternatives and preregistered thresholds.
G3: implement reproducible test harness, with baseline and intervention conditions.
G4: run, replicate, assess error bars and counterfactual tests.
G5: revise architecture and research program; loop.

The overarching program has no scientifically credible fixed completion date. No eventual success guarantee.

## Functional-consciousness working target

Anjo sponsors a rigorous L2 study of **causally integrated mind-like cognitive organization**: persistent experience-dependent state, predictive self/world models, calibrated metacognition, cross-function access, adaptive agency and learning that measurably interact. This is a hypothesis and engineering target, not a validated 'functional consciousness' achievement or any proof of phenomenal L3. Use [decision memory](decision-register.md) and cross-function interventions in the [traceability matrix](atlas/traceability-matrix.md) to turn component results into falsifiable integration proposals. No architectural selection follows from adopting this research definition.
