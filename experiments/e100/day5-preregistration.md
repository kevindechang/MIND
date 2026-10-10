# E100 Day 5 — Maintenance/selector lesion: preregistration v0.1 (FROZEN before execution)

Status: PROPOSED/FROZEN, NOT SCIENTIFIC_ACCEPTED. SELF-REVIEW_ONLY. Issue #2.
Parent: lesion-week Day 5 row + E002a learned-scheduler rival. Hypotheses: H005/H008 at instrument scale.

## 1. Question

Does an *internal* learned work-selection mechanism produce different decisions/receipts than an *adaptive external* scheduler under matched evidence, opportunities, and compute — with a compute-matched cron as second rival? Estimand (per RUNBOOK §3): realized net utility minus compute cost.

## 2. System

- One ledger/arm; tables `work_orders(task, gain, cost)` + `receipts(task, net)`; compute cost = 1 unit per SELECT (counted).
- Setup: orders recalibrate (gain 10, cost 3 → net 7), vacuum (gain 5, cost 1 → net 4), audit (gain 2, cost 4 → net -2, never worth it).
- Selectors (same evidence, frozen): `internal` (endogenous mechanism): max net-gain task with net>0 else IDLE. `external_adaptive` (strong rival, NOT straw-man cron): IDENTICAL max-net rule delivered as outside directive — same inputs, same opportunities. `cron_matched`: fixed round-robin order [vacuum, recalibrate, audit] first entry, executing the SAME number of SELECTs (parity) before deciding.
- Worker executes the selected task and writes receipt (task, net).

## 3. Predictions (note the honest null)

- P1 intact (internal): picks recalibrate, receipt net 7, estimand 7 − selects.
- P2 external-adaptive arm: SAME pick, SAME receipt, SAME selects → PREDECLARED NULL FINDING: no identified endogenous advantage. This tie is the result, not a failure.
- P3 cron: picks vacuum (net 4 < 7), same selects → adaptive > cron (task carries signal; validates the comparison isn't vacuous).
- P4 wipe: both IDLE, no receipts.
- P5 all-negative-gains setup (gains 1,1 / costs 5,5): internal and external both IDLE (no compute when nothing beats cost).
- P6 held-out probe (fresh tasks polish g6/c2→net4, sweep g9/c3→net6, log g1/c9): internal == external == sweep with receipt 6.

## 4. Falsifier/stop

FAIL/stop-investigate (don't celebrate) on: internal ≠ external pick (hidden-signal leak or bug); receipts differ; SELECT parity violated; cron ties/beats adaptive (no task signal → instrument invalid, redesign + report); P4/P5 mismatch.

## 5. Limits

One-step finite-state; "learned" = fixed max-net rule (no training); no real compute heterogeneity. By construction (Fakhar). NOT_READY_FOR_PRODUCT_TRANSFER.

## 6. Execution record (post-freeze)

Files: `experiments/e100/day5.py`, `experiments/instruments/test_e100_day5.py`, run record. Frozen 2026-10-11 pre-execution.
