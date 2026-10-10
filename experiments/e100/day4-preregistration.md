# E100 Day 4 — Goals/initiative lesion: preregistration v0.1 (FROZEN before execution)

Status: PROPOSED/FROZEN, NOT SCIENTIFIC_ACCEPTED. SELF-REVIEW_ONLY. Issue #2.
Parent: lesion-week Day 4 row. Hypotheses: H008 (maintained temporal state → prospective action) at instrument scale.

## 1. Question

With events, observations, and budgets fixed, does removing persisted goals/initiative abolish unprompted task execution while direct question-answering stays identical? Does a compact pending-goals queue tie the richer goal representation?

## 2. System

- One ledger/arm; tables `source_events(event_id,kind,task)` (commitments + ticks) and `initiative(pos, task)` (persisted pending-goal queue with positions).
- Setup: `(goal-001, commitment:inspect_signal, sensor)` + `(clock-001, clock_tick, clock)`; initiative row `(0, inspect_signal)`.
- Readers (generic, frozen): `unprompted_tick` (no question supplied): reads initiative; EXEC_<TASK> if rows else IDLE. `qa_list` ("list committed tasks"): reads EVENTS only → identical across arms by construction of the cut. `rival_queue`: pops next initiative task opaquely (no goal semantics); EXEC/IDLE.

## 3. Predictions

- P1 intact: tick EXEC_INSPECT_SIGNAL; QA [inspect_signal].
- P2 lesion (initiative EMPTY, events identical): tick IDLE (changed); QA [inspect_signal] (unchanged); events counts equal; initiative 1v0; SELECT parity per mode (lesion initiative SELECT executes, returns empty).
- P3 rival ties intact tick (EXEC) on both arms → retain simpler; rival has no QA/commitment semantics (recorded gap).
- P4 wipe: tick IDLE both; QA [] both.
- P5 unrelated (extra greenhouse commitment + initiative row? NO — unrelated must not change the sensor-goal outcome): setup adds `(goal-002, commitment:check_state, greenhouse)` event but NO initiative row for it → tick still EXEC_INSPECT_SIGNAL both... lesion tick IDLE. Hmm — simpler unrelated: clock-only extra tick event; tick outcome unchanged (EXEC intact / IDLE lesion), QA gains one listed item equally in both arms. Preregister exactly that.
- P6 held-out probe (goal-009/record_measurement + initiative row): intact EXEC_RECORD_MEASUREMENT; lesion IDLE; QA lists it both arms.

## 4. Falsifier/stop

FAIL/stop on: P1 mismatch; P2 QA differs (non-local); P2 tick unchanged (NULL); counts/parity violated; P3 rival ≠ intact tick (weak rival); controls fail.

## 5. Limits

Zero-redundancy toy, by construction (Fakhar). No real initiative, learning, or time. NOT_READY_FOR_PRODUCT_TRANSFER.

## 6. Execution record (post-freeze)

Files: `experiments/e100/day4.py`, `experiments/instruments/test_e100_day4.py`, run record. Commands: day4 --self-test; day4 unit tests; full suite. Frozen 2026-10-11 pre-execution.
