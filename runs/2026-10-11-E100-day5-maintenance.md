# Run record: E100 Day-5 maintenance selector lesion (EXPLORATORY_CHECKPOINT)

Date: 2026-10-11. SELF-REVIEW_ONLY. Accepted 0. No gate/decision change.
Slice claimed by issue comment; branch `research/2-day5-maintenance` from `origin/main@3c22a93`.

## Execution (OBSERVED, Python 3.9.6 Darwin ARM64)

- Prereg v0.1 frozen pre-code, NULL preregistered as the finding (not a failure).
- `day5.py --self-test` → PASS after one parity fix (cron burned 3 SELECTs vs 2; removed extra lookup so all arms cost 2): P1 internal EXEC_RECALIBRATE receipt 7 estimand 5.0; P2 external IDENTICAL action/receipt/selects/estimand → NULL_NO_IDENTIFIED_ENDOGENOUS_ADVANTAGE; P3 cron VACUUM estimand 2.0 < 5.0 (signal exists, comparison non-vacuous); P4 wipe IDLE; P5 all-negative IDLE both; P6 held-out probe EXEC_SWEEP both.
- `test_e100_day5.py` 4/4 OK. Full suite 79/79 returncode 0.

## Gate

Headline is a faithful negative: under matched evidence/opportunities/compute, internal selection shows no advantage over an adaptive external scheduler. Cron comparison keeps the test discriminating (adaptive beats fixed). By-construction toy; E002a's real learned-scheduler question still open at scale. NOT_READY_FOR_PRODUCT_TRANSFER.

## Next

Clean-checkout rerun + separate review, then Day-6 liar-twin lesion.
