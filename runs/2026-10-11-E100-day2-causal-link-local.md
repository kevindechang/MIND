# E100 Day 2 — local synthetic lesion checkpoint

**Work ID:** E100-D2-2026-10-11-001. **Type:** INSTRUMENT_VALIDATION. **Scientific verdict:** EXPLORATORY_CHECKPOINT; SHORT_RUN / DURATION_NOT_ENFORCED. **Reviewer:** SELF-REVIEW_ONLY.

**Issue:** #2. **Main baseline inspected:** `3c22a93a6d15a909789bb6e40c387a34b183ee7c`. **Experiment:** [Day 2 report](../experiments/E100/E100-day2-causal-link-lesion-v0.1.md). **Source:** [worker](../experiments/e100/day2.py); [tests](../experiments/instruments/test_e100_day2.py).

**Observed local:** 12 real SIGKILL (-9)/new-PID arms, same raw rows, causal links cut, sham unchanged, two effect worlds, null and shift worlds. 7/7 dedicated tests PASS; py_compile PASS. Earlier combined command interrupted; later dedicated suite passed. Full repository regression NOT_EXECUTED (networkless sandbox; no exact checkout). No scored agent trials, no separate reviewer. Strong compact/predictive rivals TIE intact, refuting any unique graph-table necessity in this toy. Source and test local Git blobs: `bcdcd64957488c87452301dc418f27dd47ad31d5` and `dd1ab20523242a915842e27c797c92ecde074e9e` respectively; check connector readback for equality. Scientific acceptance remains 0; E001 G0 OPEN; E900 NOT STARTED; NOT_READY_FOR_PRODUCT_TRANSFER.

**One next action:** clean-checkout integrated `python scripts/verify_instruments.py` plus independent adversarial source/compute parity review before merge or Day 3.
