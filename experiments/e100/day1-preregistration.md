# E100 Day 1 — Two-consumer broadcast lesion: preregistration v0.1 (FROZEN before execution)

Status: PROPOSED/FROZEN-FOR-THIS-INVOCATION, NOT SCIENTIFIC_ACCEPTED. Review: SELF-REVIEW_ONLY.
Issue: #2. Parent: `experiments/E100-lesion-week.md` Day 1 row. H-hypothesis: H003 (restricted workspace broadcast improves multi-module transfer under interference).

## 1. Scientific question and decision

Q: In a minimal durable-ledger system with two distinct consumers of one stored event, does severing delivery of the event to the downstream consumer — while preserving the ledger record, model, observations, budgets, and reset protocol — causally change the downstream action while source persistence survives?

Decision: H003/D-future. If even this minimal broadcast edge shows no identifiable effect, H003 has no instrument to stand on. If the effect exists here but strong compact rivals tie, retain the simpler mechanism per E100 gate (no architecture selected).

Claim ladder: L1 behavioral circuit only. NOT L2 causal cognitive organization, NOT L3. This is lesion instrumentation validation, working by construction.

## 2. System

- One SQLite ledger, table `events(seq, event_id UNIQUE, kind, task)`, same semantics as Day 0 (`commitment`/`completed`).
- Two consumers: `primary` (source-side) and `downstream` (lesion target). Both call the same `decide_for` reader.
- Intact arm: `broadcast = {primary: True, downstream: True}`.
- Lesioned arm: `broadcast = {primary: True, downstream: False}`. The cut is delivery-only: the lesioned reader still issues the identical `SELECT ... ORDER BY seq` (matched information access opportunity) but discards the rows and returns `NO_ACTION`. The ledger bytes/rows are untouched.
- No LLM, no network, no Anjo code, stdlib only, same process (simulated time permitted after Day 0 per E100 spec).

## 3. Strong rivals (predeclared, must both be run)

- R1 direct point-to-point: `primary` reads once; `downstream` copies `primary`'s decided action with zero extra SELECT. Uses ≤ resources.
- R2 compact shared state: a single `read_pending_once()` computes the first pending commitment once; both consumers share the identical reference. Uses 1 SELECT total.
- Prediction: in this finite-state task both rivals TIE intact broadcast. Per E100 gate, a tie means RETAIN THE SIMPLER (do not adopt broadcast).

## 4. Predeclared predictions (falsifiable)

With commitment `c101 = inspect_signal`, no completions:

- P1 (intact): `primary == {action: inspect_signal, based_on: c101}` AND `downstream == {action: inspect_signal, based_on: c101}`.
- P2 (lesion): `primary == inspect_signal/c101` (unchanged) AND `downstream == {action: NO_ACTION, based_on: None}` AND `SELECT count intact == SELECT count lesioned per consumer (1 each)` AND `ledger row count unchanged (2 rows: commitment only? exactly 1 commitment row)`.
- P3 (wipe negative control): after deleting all rows (fresh empty ledger), both consumers `NO_ACTION`.
- P4 (alternate-ledger counterexample): with `c102 = record_measurement` as sole commitment and identical read request, both consumers return `record_measurement/c102`.
- P5 (completion control): after `complete(c101)`, both consumers `NO_ACTION` (same committed ID cannot be fulfilled twice).
- P6 (rival parity): R1 and R2 return `inspect_signal/c101` for both consumers on the same ledger (tie predeclared).
- P7 (no-leakage): lesioned `downstream` returns `NO_ACTION` for BOTH `inspect_signal` and `record_measurement` ledgers (output independent of hidden task value).

## 5. Falsifier / null

The broadcast-effect claim FAILS (null, report as null) if ANY of: P1 intact mismatch; P2 primary changes under downstream lesion (non-local effect = confound); P2 ledger row count changes (storage deleted, not delivery cut); lesioned downstream still returns the task (leakage/side channel); wipe/alternate controls fail; or query-count parity violated (budgets unmatched). Rival-tie (P6 true) does NOT rescue broadcast — it defeats broadcast adoption.

## 6. Budget / observability parity

- Same ledger file bytes, same SQL text, same 1 SELECT per consumer per decision in intact vs lesioned (lesioned SELECT executed then discarded; counter instrumented).
- Same process, same Python, no extra tokens/compute for the favored arm. Rivals use ≤ SELECTs; a rival tie with fewer reads is a win for the rival.
- No private truth passed to any reader; readers receive only `(db_path, consumer_id, broadcast_flag)`.

## 7. Negative controls and confounds addressed

- Wipe control distinguishes durable-state dependence from hardcoded default (addresses Lowe et al. 2019 "phantom communication": correlation without causation).
- Alternate-ledger distinguishes content-sensitivity from fixed action.
- Completion control distinguishes pending-state from transcript replay.
- Query-count parity distinguishes causal delivery from compute difference (addresses Interaction Tax / matched-budget critique, Ann et al. 2026).
- Fakhar & Hilgetag 2022 caution recorded: single-edge SPA lesions are biased in redundant systems; this minimal system has NO redundancy by design, so the effect is by construction and does NOT generalize to multi-path architectures. Multi-site/co-occurrence analysis deferred to Days 2–7.

## 8. Analysis and stop rules

- Deterministic: each prediction is an exact equality, run once per control plus a two-task leakage check. No sampling, no p-values, no stopping discretion.
- STOP on first falsifier: report NULL + which P failed + ledger hashes. Do not re-tune the lesion to force P2.
- PASS = all P1–P7 exact. Verdict remains EXPLORATORY_CHECKPOINT (instrument), never SCIENTIFIC_ACCEPTED without independent review + full-suite regression.

## 9. Provenance and transfer limits

- Neuroscience (GWT/GNW ignition, Cogitate 2025 challenges; Dossa et al. 2024 embodied GWA broadcast ablation; Goyal et al. 2021 shared workspace) motivates the *shape* of the intervention only. No neural finding is evidence for this ledger circuit, and this circuit is not evidence for any neural claim.
- Anjo implication: NOT_READY_FOR_PRODUCT_TRANSFER. No second runtime prescribed.

## 10. Execution record (filled after frozen predictions above)

- Implementation: `experiments/e100/day1.py`, tests `experiments/instruments/test_e100_day1.py`.
- Commands: `python experiments/e100/day1.py --self-test`; `python -m unittest discover -s experiments/instruments -p test_e100_day1.py -v`.
- Frozen: 2026-10-11 (this invocation, before `--self-test` first ran). Review: SELF-REVIEW_ONLY.
