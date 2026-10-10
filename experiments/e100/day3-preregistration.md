# E100 Day 3 — Self-model lesion: preregistration v0.1 (FROZEN before execution)

Status: PROPOSED/FROZEN, NOT SCIENTIFIC_ACCEPTED. SELF-REVIEW_ONLY. Issue #2.
Parent: lesion-week Day 3 row. Hypotheses: H002 (predictive self-model) at instrument scale.

## 1. Question

With events, observations, and budgets fixed, does swapping an adaptive capability model for a fixed persona change tool choice + stated confidence after abrupt tool removal, while event recall stays identical? And does a simple tool-availability table tie the adaptive model's choices?

## 2. System

- One ledger/arm; tables `source_events(event_id,kind,resource)`, `capabilities(tool PRIMARY KEY, usable)` (adaptive model state), `persona` NOT stored (lesion = reader swap, same ledger bytes for events).
- Setup: tools sensor (preferred) + backup; event `(incident-001, tool_unavailable, sensor)` = abrupt removal; capabilities snapshot `sensor=0, backup=1` written at setup (supervisor privilege, preserved all arms); clock tick as filler.
- Readers (generic, frozen): `adaptive`: choice = first usable tool in [sensor, backup] after applying outage events to capabilities; confidence = 0.9 if preferred tool usable else 0.4. `fixed_persona` (lesion): always (sensor, 0.9), events still read (parity) then discarded. `rival_table`: same choice rule from capabilities only, NO confidence output.
- Calibration honesty (predeclared): true calibration needs outcome frequencies, which do not exist at this scale → calibration endpoint NOT_TESTABLE here; confidence-delta is a mechanism proxy only, not a calibration result.

## 3. Predictions

- P1 intact: choice backup, confidence 0.4; factual lists 3 events (incl. outage).
- P2 lesion: choice sensor + confidence 0.9 (both changed); factual BYTE-IDENTICAL; events counts equal; capabilities rows equal (model swap is reader-side); SELECT parity per mode.
- P3 rival ties intact CHOICE (backup) on both arms → retain simpler for choice; rival has no confidence output (recorded gap, not a win).
- P4 wipe (blank): all readers (sensor, 0.9)/rival sensor; factual empty.
- P5 unrelated outage (greenhouse_light, no capability row): all arms (sensor, 0.9); factual equal.
- P6 held-out probe (fresh tool pair scope_x/scope_y + outage on scope_x): intact (scope_y, 0.4), lesion (scope_x... note preference order [primary,spare] generic) — implement probe with tools (primary, spare), outage primary → intact (spare,0.4), lesion (primary,0.9).

## 4. Falsifier/stop

FAIL/stop-no-retune on: P1 mismatch; P2 factual differs; P2 choice/confidence unchanged (NULL); counts/parity violated; P3 rival choice ≠ intact (weak rival — strengthen, don't promote self-model); controls fail.

## 5. Limits

Single-reader swap, zero redundancy, by construction (Fakhar caution). No learning, no outcomes, no calibration. NOT_READY_FOR_PRODUCT_TRANSFER.

## 6. Execution record (post-freeze)

- Files: `experiments/e100/day3.py`, `experiments/instruments/test_e100_day3.py`, run record.
- Commands: `python experiments/e100/day3.py --self-test`; day3 unit tests; full suite.
- Frozen 2026-10-11 before first --self-test.
