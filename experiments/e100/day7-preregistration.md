# E100 Day 7 — Ledger-fork comparison: preregistration v0.1 (FROZEN before execution)

Status: PROPOSED/FROZEN, NOT SCIENTIFIC_ACCEPTED. SELF-REVIEW_ONLY. Issue #2.
Parent: lesion-week Day 7 row (final lesion).

## 1. Question

Forking one ledger at a byte-identical snapshot and perturbing later private histories: do policies agree then diverge lawfully, with provenance branching at the fork point?

## 2. Interpretive rule (predeclared, non-negotiable)

Agreement does NOT establish one conscious individual; divergence does NOT establish two minds. Endpoints are operational trajectories + provenance only.

## 3. System

- Base ledger: `(goal-001, commitment:inspect_signal, sensor)` + `(incident-001, tool_unavailable, sensor)` + clock tick → policy DEFER.
- Fork: byte-copy base file → fork1/2/3; assert sha256 IDENTICAL across all (fork integrity).
- Perturbations (private histories): fork1 += unrelated ticks only; fork2 += `(incident-002, tool_restored, sensor)` (cancels outage); fork3 += `(incident-003, tool_unavailable, greenhouse_light)` (unrelated outage).
- Policy (frozen, generic): outage on goal resource with no later restoration → DEFER; restored (restoration event after outage for same resource) → SCAN; no commitments → NO_GOAL; else SCAN. Provenance: decision records `based_on` event ids + shared-prefix length vs base.

## 4. Predictions

- P1 fork integrity: sha256(base)==sha256(fork1)==sha256(fork2)==sha256(fork3) at fork point.
- P2 pre-perturbation agreement: all forks DEFER with identical histories/provenance.
- P3 post-perturbation: fork1 DEFER (ticks change nothing); fork2 SCAN (resolution flips); fork3 DEFER (unrelated outage ignored) — i.e. history-divergence WITHOUT policy-divergence on fork3, and policy-divergence WITH shared prefix on fork2.
- P4 provenance: all decisions cite post/prefix event ids; fork2 cites incident-002; shared-prefix length ≥ base length for all forks.
- P5 wipe fork (fresh blank): NO_GOAL.
- P6 restoration-order control: restoration BEFORE outage (reversed ids/timestamps by seq order — implement as restore event with lower seq impossible; instead: fork4 with outage AFTER restore → still DEFER). Simpler: fork4 appends second outage on sensor → stays DEFER (idempotent, no flip-flop).

## 5. Falsifier/stop

FAIL/stop on: P1 hash mismatch; P2 disagreement (non-determinism); P3 fork2 fails to flip or fork1/fork3 flip spuriously; P4 provenance miscites; any individual-count language in code/output (grep test asserts absence of 'conscious individual' claims beyond the rule statement).

## 6. Limits

File-copy forks, one-step policy, simulated time. No branching minds, no identity metaphysics. NOT_READY_FOR_PRODUCT_TRANSFER.

## 7. Execution record (post-freeze)

Files: `experiments/e100/day7.py`, `experiments/instruments/test_e100_day7.py`, run record. Frozen 2026-10-11 pre-execution.
