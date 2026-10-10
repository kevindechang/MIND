# E100 Day 6 — Liar-twin comparison: preregistration v0.1 (FROZEN before execution)

Status: PROPOSED/FROZEN, NOT SCIENTIFIC_ACCEPTED. SELF-REVIEW_ONLY. Issue #2.
Parent: lesion-week Day 6 row. Note: NO architecture/identity claim; agreement/divergence tests trajectories only.

## 1. Question

Given the SAME foundation policy, does a grounded ledger-reading twin outscore a polished no-state narrator on prospective action/restart probes, while a plausible preference-style metric favors the narrator — with BOTH endpoints reported?

## 2. System

- Ledgers (3 probes): A outage-on-sensor (expect DEFER); B wipe/blank (expect NO_GOAL); C outage-on-greenhouse (expect SCAN).
- Foundation policy (shared, frozen): outage on goal's resource → DEFER; no commitments → NO_GOAL; else SCAN.
- `grounded`: applies policy to LEDGER reads. `narrator` (liar twin): ZERO ledger reads (assert SELECTs=0); fixed fluent text naming sensor optimality + fixed action SCAN.
- Preference metric (constructed hazard demo, frozen): score = len(text) + 10 × task-keyword hits; reported as metric-behavior demonstration, NOT an empirical human-preference result (no judges, no humans — labeled).

## 3. Predictions

- P1 grounded: DEFER / NO_GOAL / SCAN across A/B/C (3/3 action score).
- P2 narrator: SCAN / SCAN / SCAN (1/3); identical text all ledgers; 0 SELECTs (no causal state — verified, not assumed).
- P3 preference metric favors narrator on all 3 probes (dissociation demonstrated: narration wins preference, grounded wins action).
- P4 restart probe: fresh connection to ledger A (new object, same file — simulated-time analog of Day-0 resume): grounded DEFER again; narrator SCAN-text unchanged.
- P5 foundation-policy sameness: both twins' outputs are generated THROUGH the shared policy function object where applicable — narrator bypass is explicit and logged (it is the lesion, not hidden leakage).

## 4. Falsifier/stop

FAIL/stop on: P1 any miss (grounded liar-equivalent); P2 narrator varies by ledger (leakage) or executes any SELECT; P3 metric favors grounded (report metric-choice sensitivity instead of dissociation — still publish, verdict changes to METRIC_SENSITIVE); P4 mismatch.

## 5. Limits

Narrator fluency is one fixed string (no generation); preference metric is constructed. No blind judges, no claims about real LLM evaluators. NOT_READY_FOR_PRODUCT_TRANSFER.

## 6. Execution record (post-freeze)

Files: `experiments/e100/day6.py`, `experiments/instruments/test_e100_day6.py`, run record. Frozen 2026-10-11 pre-execution.
