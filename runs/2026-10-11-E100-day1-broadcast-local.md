# E100 Day 1 — broadcast lesion local execution record (2026-10-11)

**Kind:** INSTRUMENT_VALIDATION. **Verdict:** EXPLORATORY_CHECKPOINT / SCIENTIFIC_ACCEPTANCE=NO. **Research aim:** functional consciousness as unachieved mechanistic target. **Review:** SELF-REVIEW_ONLY. No Anjo product transfer.

## Hypothesis, controls, falsifier

A source-stored sensor outage delivered to a planner via a separate consumer inbox changes the planner's subsequent tool action. The only lesion is deleting event→planner broadcast delivery; source event and independent observer receipt must remain equal. Expected intact `DEFER_SENSOR_SCAN`, lesion `SCAN_WITH_SENSOR`. Unrelated clock event must not affect action; a compact policy allowed to read the public source ledger can tie intact. A same-action, changed source/observer, failed process death, or differential under unrelated clock falsifies a required toy-instrument check.

## Execution and provenance

**Execution context:** isolated local Linux sandbox, Python 3.13.5; source `experiments/e100/day1.py`, Git blob `bedfdd5da580bc6586d78a77566b202ffdd254b0`; dedicated test `experiments/instruments/test_e100_day1.py`, blob `9aaaf23e329879ab2778ad4ebb29f7ab78f802d2`. Both GitHub uploaded blobs exactly match locally executed bytes.

**Observed commands:** `python experiments/e100/day1.py --self-test` → PASS; `python -m unittest discover -s experiments/instruments -p test_e100_day1.py -v` → 1/1 PASS; `python -m py_compile experiments/e100/day1.py` → PASS. All four experimental arms actually killed the worker using POSIX SIGKILL (subprocess code -9) and recovered in a separate process using only the ledger path. Supervisor is not a second cognitive agent. Source and control records are synthetic, finite and explicitly specified before checks. Two source-development issues were fixed before success; no claim of flawless initial implementation. The full MIND integrated test suite was **NOT_EXECUTED** in this local-only workspace.

| Arm | Source outage persisted | Observer received outage | Planner routed action | Compact direct-state action |
|---|---|---|---|---|
| Intact broadcast | Yes | Yes | DEFER_SENSOR_SCAN | DEFER_SENSOR_SCAN |
| Planner broadcast cut | Yes | Yes | SCAN_WITH_SENSOR | DEFER_SENSOR_SCAN |
| No outage, intact | No (unrelated clock tick) | No | SCAN_WITH_SENSOR | SCAN_WITH_SENSOR |
| No outage, cut | No (unrelated clock tick) | No | SCAN_WITH_SENSOR | SCAN_WITH_SENSOR |

The source-row sets in the intact and lesioned cases were identical; only planner inbox delivery differed. The observer's delivered event was identical in both arms. Each arm's first worker was killed (exit -9) and the recovered policy ran in a new PID.

## Scientific limits and verdict

The intervention is a programmed information-deprivation test: route interruption predictably changes a deterministic rule's input. It does **not** demonstrate broadcast-specific necessity, cognition, learning, agency, phenomenal awareness, or a sufficient architecture for a functional mind. Indeed a one-bit sufficient-state lookup matches the intact system. Compute equalization and held-out task families are absent; no real-agent trial. **SCIENTIFIC_ACCEPTED=0, E001 G0 OPEN, E900 not run, SELF-REVIEW_ONLY.**

**Exactly one next executable research action:** implement E100 **Day 2** causal dependency-lesion instrument, preserving raw transcript/events and fully matched observation access, with predeclared held-out counterfactual action and strong compact predictive-state comparator. Stop when action changes due only to causal-edge loss, or when no such discrimination can be identified. Real full-checkout Day 1 reproduction and regression remain operational preflight items, not substitute scientific endpoints.
