# E001 Stage-1 candidate: Causal Commitments workshop v0.1

**Status: prototype coded and locally tested on 2026-10-10. NOT preregistered. NOT an AI-agent experiment. H001 remains untested. G0 OPEN.**

## Why this exists

Iteration 002 showed that the original 3-bit XOR switchboard is exactly solvable from three diagnostic observations. It cannot discriminate rich graph memory from minimal sufficient-state storage. This Stage-1 **candidate** adds combinatorial intervention effects, delayed event feedback, past commitments, a simulated working-context reset, and action-level utility. It is a methodological scaffold, **not yet a valid demonstration of autobiographical graph necessity**.

## Formal generative process

- Sample a directed acyclic graph over \`n=7\` synthetic nodes, with each \`i<j\` edge included with probability 0.33 using seeded \`random.Random\`.
- An intervention at node i flips the binary states of i and all downstream reachable nodes. Two interventions compose by XOR; only one or two may be chosen in the decision phase.
- During phase 0, each node is probed exactly once. The observation is an event \`(event_id, action, affected_mask, due_tick, phase)\` delivered 1–3 *simulated* ticks later. These are **fully informative tests** of the action-to-effect matrix.
- The agent makes four distinct prior commitments \`(goal_node, desired_state, penalty)\` before reset. They persist as episodic information; the simulated reset only changes environment phase and **does not itself demonstrate a model process restart**.
- After reset, choose zero, one or two intervention sources. \`utility=-sum(penalty for each violated commitment)-number_of_actions\`. Ties use lexicographic plan ordering.
- A privileged simulator computes the optimal plan from the graph's transitive influence matrix. A **separate observation-only solver** computes the same plan using public diagnostic events and prior commitments, with no access to graph internals.

## Important counterexamples and restrictions

1. The observation-only compact action-effect matrix is **sufficient for this world**. A rich graph cannot beat it in attainable expected decision quality given identical observations. This is a deliberate hard baseline: no absolute 'graph memory is necessary' claim survives here.
2. The generated DAG is causal by *construction*, not learned causal identification under unknown confounding. A true hard benchmark should allow partial/noisy observations, controlled probes and identifiability screening.
3. Full diagnostics are required before a scored oracle comparison. If some events are withheld, the current prototype rejects rather than assigns a secretly informed target.
4. A commitment-removal intervention can change the optimal plan under identical graph/feedback. This supports **test sensitivity** to earlier decisions, not claims about a model's memory.
5. No models, vectors, embeddings, multi-agent systems or LLMs were run; no 40-minute durable worker is provisioned.

## Instrument check executed in interactive ephemeral Python

- \`python3 -m unittest discover -v\` — **10/10 tests passed** (oracle parity over 100 seeds, event ids and delayed ordering, absent diagnostics, pending feedback reset guard, phase guard, observable schema, informative commitment intervention, corrupt events, duplicate goals, deterministic replay).
- \`python3 causal_commitments.py\` — **100/100 seeded worlds** matched full-oracle action and utility to the observation-only solver.
- \`1,000\` seed enumeration: removing the last earlier commitment altered the selected optimal plan in **419/1000 (41.9%)** pairs. This descriptive value is a deterministic, generator-dependent frequency, **not an empirical treatment effect, model accuracy, inferential significance or external validity**.

## Open validity issues — G0 cannot close

- Observation-to-intervention mapping is too complete and permits a compact action-effect lookup.
- Late feedback is simulated ticks, not actual calendar-time separate sessions.
- Commitment intervention is only an ablation on a synthetic fixed goal record; no genuine belief updating, identity, feedback correction or learning has occurred.
- The world lacks noisy probes, unknown confounders, nonstationary causality, branching investigation and budget-limited information acquisition.
- Agents are not wired to an explicit process reset and memory serialization in an independent runtime.
- Before G2 freeze model/version, policy/controller baselines, storage serialization, equal budgets, held-out world families, interference conditions, seed sample size, power/CI, exclusion, and preregistered thresholds.

## Discriminative next experiment (NOT BUILT)

Add a delayed, stochastic, partially observed intervention stage with *selectable probes*. Use an enumerated belief-state oracle for small n and a blind-action scorer under partial identification. Compare (i) no memory, (ii) full transcript, (iii) retrieval, (iv) minimal sufficient belief-state, (v) causal graph and (vi) mislabeled/sham episodes at identical model/observation/compute budgets. Include paired commitments under identical world state, explicit feasible optimal-policy sets, negative controls, and out-of-distribution graph families.

**Ruling:** Don't design tests to guarantee graph victory; allow minimal belief state to outperform it. Any positive E001 finding is a component-level functional result (L2 candidate), not integrated mind (E900) or phenomenal experience (L3).
