# E002a G0 — Maintenance-Selection Instrument Validation v0.1

**Date:** 2026-10-10. **Workstream:** W2. **Hypotheses:** H005/H008. **Status:** G0 design + deterministic one-slot instrument checks; NOT a preregistered or executed AI-agent evaluation.

## Scope
A one-step abstract resource allocation benchmark for which synthetic task to maintain or simulate next. One optional compute slot, three policies (first-entry fixed, earliest deadline, maximal reported estimated value) and an evaluator-only true-to-estimated gain factor. Identical public task lists are supplied to all; evaluator-private actual factor is unavailable to policies. The code has no always-on computation, conversational input, environmental drift or real model memory; such claims are explicitly unsupported.

## Files and run evidence
- [One-slot policy code](instruments/e002a_maintenance_selection.py), [tests](instruments/test_e002a_maintenance_selection.py).
- Test design authored before code; `python -m unittest -v` initially failed with `ModuleNotFoundError` for missing implementation (observed RED).
- After implementation, `python -m unittest -v`: **10 tests passed** (exit code 0; Python 3.13.5).
- `python e002a_maintenance_selection.py`: synthetic demonstration fixed -0.03, earliest-deadline 0.3, estimated-value 2.4 (expected incremental utility under hand-authored input).
- An adversarial test shows forecast miscalibration may make gain-based choice worse than a deadline controller. Thus the benchmark does **not** assume gain policy always wins under truth.

## Analytical limitations
The benchmark outcome is largely mechanical given chosen assumptions, not a behavioral treatment effect. The demonstration favors estimated value because we wrote higher reported gain for that arm, so it cannot evaluate cognition. `actual_ratio` is evaluator-defined and unobserved by policies; multiplying it by a forecast is an arbitrary synthetic model. The test suite validates selections, input rejection and payoff separation, not actual inferred action consequences. Unlike the E002a proposal, there is no dynamic endogenous maintenance policy with logged background compute. A1 is neither selected nor implemented.

## Discriminative upgrade needed
Construct a partially observable multi-period maintenance world where all arms receive identical state and finite update opportunities, with hidden changes, deadlines, noisy estimate calibration and prospective decision outcomes. Compare a value-of-computation *external scheduler* to the proposed internally prioritized controller with exactly matched state, inference and update timing. Preregister an ablation of regulatory/internal goals and an interruption/resumption trace. G0 remains OPEN; no statistical threshold or inference cost bound has been frozen.

## Decision
Keep the toy as calibration-only. Its most consequential insight is that improvements over cron/fixed deadlines may arise from ordinary rational metareasoning without evidence of an independently maintained digital self. L1/L2/L3/E900 unchanged.

## Post-implementation mutation sensitivity check (2026-10-10)

The first missing-module `ModuleNotFoundError` is a setup failure, not the substantive failing assertion required by strict Superpowers TDD. After implementation, a temporary mutation eliminated the value-policy's skip rule. The specific test for high compute cost then **FAILED as intended** (exit 1, `AssertionError: 'valuable' is not None`). After restoring original code, full suite **10/10 PASS** (exit 0). This validates test sensitivity for one fault after implementation, but does not establish that every case followed textbook RED–GREEN before writing production code. Temporary mutation was *not* committed; GitHub retains the green version.
