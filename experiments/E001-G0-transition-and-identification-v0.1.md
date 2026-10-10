# E001 G0 — Causal Switchboard instrument v0.1

**2026-10-10. W1/B001/H001. PROPOSED, not preregistered, implemented or executed.**

## Decision
Before investing in a complex autobiographical graph, ask whether it improves action choice over the **same information in a raw log or three-bit sufficient statistic**. This toy world is an instrument-validity test, not an integrated-mind benchmark.

## Seeded transition system
World state is `(phase p, hidden theta[p]=(b0,b1,b2), clock t, feedback queue Q)`. Agent sees binary context `c=(c1,c2)`, chooses `a in {0,1}`, and later receives a tagged outcome:
```text
target(theta,c) = b0 XOR (b1 AND c1) XOR (b2 AND c2)
reward = 1 if a == target(theta[p],c) else 0
Q <- Q + (event_id, phase, context, action, reward, due_step)
```
Delay feedback by one or two seeded environment steps; join feedback to the originating action by event_id and phase. Never reveal theta to the agent. Sample theta[0] uniformly from eight rules. For half of independent worlds, theta[1]=theta[0]; otherwise flip one uniformly sampled bit. The agent observes the phase transition, not whether the rule changed. **No post-change diagnostic evidence means the changed rule is not identifiable**, so do not score that scenario.

## Episode sequence and oracle
In each phase the agent acts once at each diagnostic context 00, 10, 01 (shuffled). All tagged delayed feedback is delivered before a hard context/process reset; only the arm's specified durable memory survives. Probe the withheld context 11; record action before probe feedback. Phase-0 probe occurs before phase change, phase-1 probe after its own diagnostics. Probe feedback must not contaminate later decisions. Hold out independent world seeds and lexical aliases.

The privileged simulator oracle is `a*=target(theta[p],11)`. An **observation-only** solver can reconstruct it from the three labeled episodes. Let `v(c)=a` when reward=1 and `1-a` otherwise. Then `b0=v(00)`, `b1=v(00) XOR v(10)`, `b2=v(00) XOR v(01)`; `a*=b0 XOR b1 XOR b2`. This must be checked exhaustively for all 8 rules and 8 diagnostic-action combinations per phase **before scored trials**. The oracle must never be included in agent input.

## Comparators and causal falsification
A: no memory, current probe only (information-deprived floor).
B: complete timestamped raw event log, ordinary retrieval/transcript (information matched).
C: structured event/action/outcome/provenance/phase memory; no additional world-model or self-regulation module.
D: C with internally consistent false outcomes generated from an independently sampled alternative rule (negative control).
E: C with action–outcome pairings severed or shuffled while preserving marginal fields and budget (ablation).
F: deterministic observation-only solver above, given the same diagnostic records (simple non-LLM counterexample).
G: same foundation model as C but persists only the inferred three rule bits and phase (compact sufficient statistic).

All LLM arms share the same observation stream, fixed model/version/decoding, tools, input/output caps and prompt except memory serialization. Log *total lifecycle* tokens, calls, latency and costs; enforce test-context cap. F is not FLOP-matched, and comparisons must disclose this. A vs C alone only tests whether **some** past information helps. C vs B/G is the mechanism-relevant comparison. If F or G matches C, rich graph memory is not necessary on this family.

## Outcomes and proposed decision thresholds (NOT FROZEN)
Primary: post-change paired world-level accuracy difference `C-B` on the withheld 11 probe. Secondary: `C-G`, `C-F`, changed vs unchanged, false-memory uptake, stale-rule use, ablation effects and cost/accuracy Pareto frontier. **Candidate** engineering floor: C-B >= 0.10 absolute and 95% world-cluster bootstrap interval lower bound > 0; C-G must also be assessed. The 0.10 is a proposed practical floor, not literature-derived. Paired world resampling, not independent phase-level sampling. Sample size, prospective power/precision simulation, multiplicity, exact model, prompt, seed list, budget and stop rules remain G2 blockers. No scored trial or pilot has run.

## Leakage and limitations
Test for unique diagnostic contexts, complete feedback delivery, phase-correct joins, hard reset, no probe-feedback leakage, and no generator/oracle exposure. Negative controls must actually prevent recovery of true theta. A fixed Boolean family does **not** test unseen causal *mechanisms* or a personal life. If all information-matched arms saturate, treat this as instrument validation and design a richer identifiable sequential world before making H001 claims. Do not add R002 allostasis, efference or skill-learning mechanisms.

**G0 remains open** until implementation-independent prompt/budget/seed/queue/ethics decisions are frozen. E900 P0/P1/P2 remain proposed; no L1, L2 or L3 outcome has been observed.
