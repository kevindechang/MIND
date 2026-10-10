# Run record: E100 Day-3 self-model lesion (EXPLORATORY_CHECKPOINT)

Date: 2026-10-11. SELF-REVIEW_ONLY. Accepted 0. No gate/decision change.
Issue #2 slice claimed by comment; branch `research/2-day3-self-model` from `origin/main@3c22a93`.

## Execution (OBSERVED)

- Prereg `day3-preregistration.md` v0.1 frozen before any day3 code ran.
- `python3 experiments/e100/day3.py --self-test` → PASS: intact (backup, 0.4); persona lesion (sensor, 0.9); factual byte-identical; SELECT parity persona==adaptive (4=4); rival ties choice both arms (no confidence key — recorded gap); wipe NO_GOAL; unrelated (sensor,0.9); held-out primary/spare probe (spare,0.4)/(primary).
- `test_e100_day3.py` 6/6 OK. Full `verify_instruments.py` returncode 0 (suite PASS).
- One dev fix pre-PASS: persona SELECT parity (added discarded goal-read so counts match; predictions unchanged).

## Gate self-assessment

Choice effect demonstrated but rival-tied → retain simpler for choice. Calibration endpoint NOT_TESTABLE (no outcomes) — stated in prereg, code, and tests. By-construction instrument; no L2/L3. NOT_READY_FOR_PRODUCT_TRANSFER.

## Next

Clean-checkout rerun + separate review, then Day-4 goals lesion.
