# E100 Day 2 — Causal-link lesion: preregistration v0.1 (FROZEN before execution)

Status: PROPOSED/FROZEN-FOR-THIS-INVOCATION, NOT SCIENTIFIC_ACCEPTED. Review: SELF-REVIEW_ONLY.
Issue: #2. Parent: `experiments/E100-lesion-week.md` Day 2 row. Related hypothesis: H001/H007 (causal autobiographical/dependency representation) at instrument scale only.

## 1. Question and decision

Q: With the complete raw-event history, observations, and query budgets held fixed, does removing a *causal dependency representation* (a links table) causally change a held-out counterfactual-planning action while factual recall stays byte-identical?

Decision relevance: if no identifiable effect exists even here, dependency-edge machinery has no instrument standing; if the effect exists but a compact sufficient-state rival ties, retain the simpler per E100 gate. No architecture selected either way.

Claim ladder: L1 behavioral circuit only. NOT L2, NOT L3. Lesion-instrumentation validation, working by construction.

## 2. System (mirrors canonical Day-1 conventions)

- One SQLite ledger PER arm; supervisor runs arms sequentially (instrumentation, not an agent). Simulated time (permitted after Day 0). Stdlib only.
- Tables: `source_events(event_id PK, kind, resource)`; `causal_links(effect, cause, relation)` with `requires` (goal→capability) and `depends_on` (capability→resource) rows; `availability(resource PK, ok)` — a flat sufficient-state snapshot written at setup time with full knowledge, preserved in ALL arms.
- Setup (per arm, same events): goal commitment `(goal-001, commitment:inspect_signal, sensor)`, outage `(incident-001, tool_unavailable, array_power)`, unrelated tick `(clock-001, clock_tick, clock)`. Links (intact only): `(goal-001, sensor, requires)`, `(sensor, array_power, depends_on)`. The outage resource (`array_power`) reaches the goal ONLY via the transitive link path — no direct kind/resource match exists, so a links-blind reader cannot attribute it.
- Readers (generic over ids; frozen before probe ids observed):
  - `factual`: `SELECT ... FROM source_events ORDER BY event_id` (events only).
  - `linked_planner`: resolve requires/depends_on transitively from each goal; DEFER_SENSOR_SCAN if any reached resource has a `tool_unavailable` event, else SCAN_WITH_SENSOR; NO_GOAL if no commitments.
  - `compact_rival`: read `availability` for the goal's direct resource only (no link traversal); DEFER iff `ok=0`.

## 3. Arms

1. **intact**: events + links + availability. 2. **lesion**: identical events + availability, `causal_links` EMPTY (cut). 3. **wipe**: fresh ledger, no setup. 4. **unrelated**: outage on `greenhouse_light` (no link path to sensor), links otherwise intact.

## 4. Predeclared predictions

- P1 intact: factual lists exactly the 3 setup events; linked planner = DEFER_SENSOR_SCAN.
- P2 lesion: factual BYTE-IDENTICAL to intact; linked planner = SCAN_WITH_SENSOR (changed); events row count equal (3=3); links 2 vs 0; SELECT counts equal per mode (factual 1=1; planner 2=2 — lesioned link SELECT executes, returns empty; OA discipline).
- P3 compact rival ties intact planner (DEFER) on BOTH intact and lesion arms → predeclared simpler win; no link-necessity claim.
- P4 wipe: factual empty; planner NO_GOAL (DEFER abolished).
- P5 unrelated: both arms SCAN_WITH_SENSOR; factual equal across arms (outage listed, correctly ignored).
- P6 held-out probe (fresh ids `goal-009`/`incident-009`, same structure; reader code frozen first): intact DEFER, lesion SCAN, factual equal.
- P7 no-leakage: lesioned planner returns SCAN for BOTH `array_power` and a second held-out resource path (`array_power_b` with mirrored links), i.e. output independent of which Hideable resource failed — plus intact still DEFERs on the second path (sensitivity check).

## 5. Falsifier / null / stop

FAIL (report, stop, no retune) if ANY: P1 mismatch; P2 factual differs (non-local confound); P2 planner unchanged (NULL: no identifiable link effect — the honest Day-2 outcome, report as null); events counts differ; SELECT parity violated; P3 rival fails to tie intact (rival too weak — strengthen rival, do NOT promote links); wipe/unrelated controls fail.

## 6. Transfer limits (predeclared)

Single-edge SPA lesion in a zero-redundancy toy works by construction (Fakhar & Hilgetag 2022: single-site lesions bias redundant systems; this system has no redundancy BY DESIGN — no generality claimed). Counterfactual is one-step and finite-state; no learning, no held-out world families with seeds (deferred to E001-G2/E900 designs). Lowe et al. 2019 phantom-communication controlled via P4/P5 interchanges. Anjo: NOT_READY_FOR_PRODUCT_TRANSFER.

## 7. Execution record (filled after frozen predictions above)

- Implementation: `experiments/e100/day2.py`; tests `experiments/instruments/test_e100_day2.py`.
- Commands: `python experiments/e100/day2.py --self-test`; `python -m unittest discover -s experiments/instruments -p test_e100_day2.py -v`.
- Frozen: 2026-10-11, before first `--self-test`. Review: SELF-REVIEW_ONLY.


## 8. Post-v0.1 review amendment v0.2 — not a retrospective preregistration

**Provenance:** This section was written AFTER the initial v0.1 test results and after PR #7's Review-plugin audit (review 5480430690). The original P1–P7 remain historical, not silently revised. All v0.2 code/test changes are **NOT_EXECUTED in the reviewing ChatGPT invocation** because an authenticated, byte-exact checkout of the private repository was unavailable in its local Python container. The v0.1 worker's reported 82/82 tests do not verify v0.2.

### Changes to be tested prospectively

- **Fresh process:** Each arm now seeds an isolated SQLite ledger in a worker, receives a commit acknowledgement, kills that process with real POSIX SIGKILL (expect -9), then starts a new worker with only the ledger path. The new worker receives only `{"op":"report"}`; no pre-intervention history or scenario is passed at readback. Every arm must show distinct PIDs.
- **Rival provenance:** Both arms first store identical causal dependencies. A compiled availability state is computed from the same persisted event/edge information **before** the lesion and preserved in both arms. The graph-dependent reader accesses the remaining graph; the compact reader accesses the compiled state. Compilation currently requires two SELECT statements plus graph traversal and writes, and cost parity is **NOT ESTABLISHED**. This represents an admissible offline sufficient-state upper bound, not an online compute-matched rival or evidence of representational necessity.
- **True sham cut:** Insert an irrelevant clock-to-light edge; remove only that edge for sham while preserving goal-to-outage dependency. Expected planned action in both intact-sham and cut-sham is DEFER; complete source-event recall identical; edge counts differ by exactly one.
- **Actual query trace:** Use SQLite's statement trace during reporting to count executed SELECTs. This is measured SQL count, **not** matched CPU time, training cost, serialized bytes, update latency, or memory budget.
- **Structural variation:** The P7 alternate path now includes an extra relay node on the dependency chain; this tests simple graph-closure structural variation. P6 remains **ID invariance only** and must not be described as a generalization result. The eventual held-out causal-world trial is still unexecuted.
- **Supervisor-only score:** The separate test supervisor scores a single future one-step action as 1 when it matches the planted availability world's prescribed action, 0 otherwise. For the outage world the expected action is DEFER, so the lesion is scored 0 and intact/compact are 1. This is a deterministic calibration label, **not** prospective agent efficacy, causal transfer or consciousness.

### v0.2 falsifiers and stop

- F8: In any arm, the seeded worker fails to exit with SIGKILL, recovered PID is not distinct, or the recovered worker needs transcript/scenario in its report request.
- F9: Sham deletion changes source rows or action, or changes more than one edge.
- F10: Source-event parity fails, compact-state preprocessing reads injected truth instead of the stored public evidence, or actual traced query counts vary across intact and link-lesion arms without acknowledgment.
- F11: An extra-hop structural path fails to resolve while intact, or the lesioned policy fails to change its decision; label it as instrument defect, not cognition.
- F12: Local `python experiments/e100/day2.py --self-test`, `python -m unittest discover -s experiments/instruments -p test_e100_day2.py -v`, and `python scripts/verify_instruments.py` must be run on a clean checkout pinned to the **revised** PR head before any verified result is attributed to v0.2.

**Scientific status remains EXPLORATORY_CHECKPOINT.** The next substantive design must freeze a genuinely separate counterfactual-world distribution, varied interventions, same-information/same-compute compact rivals with state-update costs, and a decision-relevant effectiveness margin. Until then there is no identified special memory architecture, no L2 functional consciousness finding, and no L3 inference.
