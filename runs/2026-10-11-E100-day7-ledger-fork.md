# Run record: E100 Day-7 ledger fork (EXPLORATORY_CHECKPOINT; Lesion Week instrument-complete)

Date: 2026-10-11. SELF-REVIEW_ONLY. Accepted 0. No gate/decision change.
Slice claimed by issue comment; branch `research/2-day7-ledger-fork` from `origin/main@3c22a93`.

## Execution (OBSERVED, Python 3.9.6 Darwin ARM64)

- Prereg v0.1 frozen pre-code, interpretive rule hard-coded (agreement≠one individual, divergence≠two minds).
- `day7.py --self-test` → PASS first run: P1 four sha256 identical at fork; P2 all DEFER pre-perturbation; P3 fork1 DEFER (ticks inert), fork2 SCAN (restoration flips), fork3 DEFER (history diverges, policy agrees), fork4 DEFER (idempotent); P4 shared prefix [goal-001, incident-001, clock-001], fork2 cites incident-002; P5 wipe NO_GOAL.
- `test_e100_day7.py` 4/4 OK (incl. no-individual-claims source grep). Full suite 79/79 returncode 0.

## Gate

Fork agreement/divergence lawful and provenance-branched; says nothing about individuals by preregistered rule. By-construction toy. NOT_READY_FOR_PRODUCT_TRANSFER.

## Week status

Lesion-week instruments Day 0 (canonical + external repro) through Day 7 now all locally executed as EXPLORATORY_CHECKPOINTs; accepted contributions remain 0; E900 still PROPOSED. Next: integrator serialization + independent adversarial review passes before any synthesis or E900 design.
