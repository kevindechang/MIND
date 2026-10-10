# Run record: canonical Day-1 independent reproduction + Day-2 causal-link lesion (EXPLORATORY_CHECKPOINT)

Date: 2026-10-11. Executor: single agent (this session), SELF-REVIEW_ONLY. No independent reviewer.
Issues: #2 (Day-2 slice claimed via issue comment; prior PR #5 closed as superseded by merged #6, no conflicting edits committed).
Verdict: EXPLORATORY_CHECKPOINT. Accepted contributions: 0 (unchanged). No G-gate, D001, H-hypothesis, architecture, E900, or L2/L3 change.

## 1. Restore and conflict handling

- Fresh clone to `/tmp/MIND-main`, live `main` HEAD `3c22a93` (Merge PR #6). `git status` clean before work.
- Found PR #5 (own prior Day-1 parallel implementation) CONFLICTING with merged #6 (canonical Day-1: per-arm ledgers, real SIGKILL per arm, inbox delivery, compact tie). Per GO step 6 closed #5 with superseded comment + salvage review notes (budget-parity counter, leakage sweep, completion control); no merge, no force-push.
- Entry files re-read on new HEAD: GO/CURRENT/TASKS/RUNBOOK deltas (Day-1 executed, Day-2 NOT RUN), `experiments/E100-lesion-week.md` Day-1 section + Day-2 row, canonical `day1.py`/`test_e100_day1.py`.

## 2. Independent reproduction of canonical Day-1 (OBSERVED)

- `python3 experiments/e100/day1.py --self-test` → PASS on Python 3.9.6 Darwin ARM64 (prior report: Linux 3.13.5): intact routed DEFER_SENSOR_SCAN vs lesion SCAN_WITH_SENSOR; raw rows equal; observer inbox equal; compact ties intact; unrelated controls SCAN in both configs; worker_exit -9 in both arms (real SIGKILL reproduced).
- `python3 scripts/verify_instruments.py` → 75/75 OK, returncode 0.
- Blobs executed: day1.py `19783644...`, test `49623dbf...`.

## 3. Day-2 execution (prereg P1–P7, all PASS after one dev-defect fix)

- Prereg `experiments/e100/day2-preregistration.md` v0.1 frozen BEFORE any day2 code ran. Design: per-arm ledgers; events identical (goal commitment, outage on array_power, clock tick); links `goal→sensor requires`, `sensor→array_power depends_on`; availability snapshot preserved all arms; readers generic over ids.
- Dev defect (caught by P5, fixed before any PASS claimed): first setup() wrote the depends_on edge + sensor-ok=0 even for the unrelated resource, so the unrelated arm wrongly DEFERred. Fix: `link_outage` flag — unrelated arms write no outage path and snapshot sensor ok=1. Predictions unchanged; failed intermediate runs are not science.
- `python3 experiments/e100/day2.py --self-test` → PASS: P1 intact DEFER + 3 factual rows; P2 lesion SCAN with byte-identical factual, events 3=3, links 0v2, SELECT parity 1=1/2=2; P3 compact ties DEFER on both arms → retain simpler; P4 wipe factual [] + NO_GOAL; P5 unrelated SCAN both arms; P6 held-out goal-009/incident-009 DEFER/SCAN; P7 second path array_power_b DEFER/SCAN.
- `test_e100_day2.py` 7/7 OK. Full suite after: 82/82 OK (75+7).
- Blobs: day2.py `c3490b8c...`, prereg `7b6a1a5d...`, test `0c648fd0...`.

## 4. Gate self-assessment (why NOT accepted science)

Strongest rival (compact availability snapshot) ties on both arms → no link-necessity claim; single-edge SPA in zero-redundancy toy works by construction (Fakhar caution); no full-PDF literature replication this round; SELF-REVIEW_ONLY. Instrument check only.

## 5. Files (proposed delta)

`experiments/e100/day2-preregistration.md`, `experiments/e100/day2.py`, `experiments/instruments/test_e100_day2.py`, this record. No research-state.md edits (integrator owns state-last).

## 6. One next action

Clean-checkout rerun of Day-2 self-test + suite, then separate-reviewer adversarial review (hidden side channel via availability table? coalition masking? phantom correlation?), then Day-3 self-model lesion. Anjo: NOT_READY_FOR_PRODUCT_TRANSFER.
