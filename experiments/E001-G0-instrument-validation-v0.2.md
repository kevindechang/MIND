# E001 G0 — instrument validation v0.2

**2026-10-10 | W1/B001/H001 | G0 OPEN.** Tested: deterministic simulator/oracle only. **No AI agent arms have been executed; no agent-performance claim is supported.**

## Instrument code and executed checks

Research-only Python standard-library files:
- [e001_switchboard.py](instruments/e001_switchboard.py): phase-specific hidden XOR rule, event ID/phase tagging, 1–2-step delayed reward queue, flush before phase change, withheld 11 probe oracle and phase-validated observation-only inversion.
- [test_e001_switchboard.py](instruments/test_e001_switchboard.py): exhaustive inversion, phase transition, stale feedback, missing/duplicate observations, probe leakage, invalid bits.

Executed in local ephemeral Python environment (not GitHub Actions): `python3 -m unittest discover -v` → **7 tests PASS**, and `python3 e001_switchboard.py` → **768 single-phase cases + 64 two-phase cases PASS**. These cases are finite enumerated simulator combinations, not independent statistical subjects or LLM trials. There is no random-state sampling or external data.

## Identifiability audit — the real result

For contexts `00, 10, 01`, an agent with action `a` and binary correct/incorrect reward `r` knows the latent action target `v=a` if `r=1`, else `v=1-a`. Then `b0=v00`, `b1=v00 XOR v10`, `b2=v00 XOR v01`. Thus the three records *deterministically identify all three hidden bits*. An observation-only 3-bit memory is a perfect sufficient statistic for the 11 probe if all diagnostics are delivered.

**Consequences:**
1. A deterministic solver with only three bits obtains exact probe predictions in all checked cases, including rule flips. This does **not** imply the same accuracy from an LLM.
2. C (rich graph memory) cannot have an information-theoretic advantage over G (three-bit memory) or F (minimal deterministic solver) on this family. C might only change model reliability/engineering complexity.
3. C vs A (no memory) can show *value of past evidence* but cannot identify a specifically autobiographical-graph mechanism.
4. Delay/phase/feedback confusion is an engineering confound, not evidence of deficient mind-like memory. Score it separately.
5. The condition labeled 'changed' is **not a hidden-change detection task** because fresh three-item diagnostics in phase 1 identify its rule anew.

**Design ruling:** Keep XOR Switchboard as a **stage-0 calibration instrument** for reset, event pairing, evidence flow and oracle tests; never make a positive result on it sufficient to support H001. If a simple solver beats an LLM graph design, prefer the solver on this task.

## Primary literature synthesis (metadata/abstract level; not replicated)

- S006 MemoryArena, He et al., ICML 2026, https://proceedings.mlr.press/v306/he26am.html: multi-session interdependent tasks jointly probe memory and action rather than QA alone. Provides a stronger ecological next step; no causal advantage for H001 is proven by abstract.
- S007 EMBER-Bench, Cai et al., arXiv 2026-10-04, https://arxiv.org/abs/2610.05013: cross-event next-action/causal-traceback tasks and historical annotations; study reports gaps even when recall-style benchmarks succeed. Preprint; benchmark reports are not our replication.
- S008 Kaelbling, Littman & Cassandra, *Artificial Intelligence* (1998), https://doi.org/10.1016/S0004-3702(98)00023-X: POMDP planning makes compact belief-state/controller alternatives serious competitors to a narrative memory graph.
- S009 Littman, Sutton & Singh, NeurIPS 2001, https://proceedings.neurips.cc/paper_files/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html: action-conditional predictive state as another non-autobiographical compression alternative. Neither paper says rich memory is impossible or useless.

## Next discriminative design question

Can we construct a **partially observable multi-event action** world where history about an agent's *own commitments, attempts, consequences and corrections* controls optimal policy across a true reset, while simple event logs, a compact causal state estimator and rich autobiographical graph memory all have access to exactly the same observations?

A candidate Stage-1 environment must (a) contain interventionally identifiable delayed dependencies, (b) prevent the current session's three observations from fully reconstructing all relevant historical constraints, (c) test policy selection and regret over multi-step choices, not just terminal next-action QA, (d) include false-memory and credit-assignment controls, (e) independently certify that every scored case is identifiable from allowed history and disallow oracle exposure, and (f) match model, time, tokens, inference/search budget and retrieval opportunities across arms. Specify predeclared minimal-controller rival *before* graph implementation.

**G0/G2 status:** OPEN. No numeric success threshold, power plan, model/decoding pin, seed set, experimental budget, or safety review has been frozen for agent trials. The previous 10-point C–B threshold remains illustrative, not preregistered. No H001 status change or architecture promotion.

## L1/L2/L3 and E900

L1: No social/voice evaluation. L2: simulator correctness and a negative **identification finding** against the simple toy instrument; *not* causal evidence of an integrated entity. L3: No consciousness inference. E900 is unchanged and proposed.
