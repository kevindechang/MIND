# Run record: E100 Day 0 independent reproduction + Day 1 broadcast lesion (EXPLORATORY_CHECKPOINT)

Date: 2026-10-11. Executor: single agent (this session), SELF-REVIEW_ONLY. No independent reviewer invoked.
Issues: #2 (executable lab; this work), #1 (preflight evidence below), #3 (rival logic reused, not executed as review).
Verdict: EXPLORATORY_CHECKPOINT. Accepted contributions: 0 (unchanged). No G-gate, D001, H003, A0/A1, E900, or L2/L3 change.

## 1. Restore

- Repo: `kevindechang/MIND`, fresh clone to `/tmp/MIND-fresh`, branch `main`, HEAD `7b9ebcc641086fed8e6c97d9d526669e18fc4b6f` (Merge PR #4).
- `git status --short` before work: clean (no modifications).
- Entry files read: GO.md, AGENTS.md, CURRENT.md, research-state.md, TASKS.md, RUNBOOK.md, research-quality-gate.md, CONTRIBUTING.md, hypotheses.md (H003), workstreams.md (W2), evidence-ledger.md, experiments/E100-lesion-week.md, experiments/e100/day0.py, experiments/instruments/test_e100_day0.py, issues #1/#2/#3 bodies.

## 2. Capability check

- Python 3.9.6, Darwin 25.6.0 ARM64, POSIX SIGKILL available. `gh` authenticated as `kevinconquerer` (repo+workflow scopes). No paid APIs, no Actions, no Anjo production access used.

## 3. Issue #1 preflight (exact reproduction)

- Command: `python3 scripts/verify_instruments.py` on byte-exact checkout (only additions afterwards are the untracked Day 1 files listed in §5; preflight ran BEFORE they were added... correction: Day 0 self-test ran before; full verify ran after Day 1 files added — see §4 for both counts).
- Day 0 first: `python3 experiments/e100/day0.py --self-test` → PASS, `observed_worker_exit_code: -9`, `signal: SIGKILL`, `first_worker_pid: 9094`, `resumed_worker_pid: 9095`, `on_restart: {inspect_signal/c001}`, `after_completion: NO_ACTION`, `wiped: NO_ACTION`, `alternate: record_measurement/c002`. Independent reproduction on Python 3.9.6 (prior report: 3.13.5).
- Full regression BEFORE Day 1 files: 74 tests OK (prior external report said 73; delta = +1 test in current HEAD, `test_real_death_and_ledger_controls` included; exact per-suite counts in log). AFTER adding Day 1 files: **83/83 OK** (74 + 9 new `test_e100_day1` tests), `test_returncode: 0`, `instrument_files: 14→15` (new test file; source `day1.py` lives outside instruments dir so not counted). Syntax: 0 errors.
- Hashes (pre-Day-1 HEAD): `day0.py 646bcba1...`, `test_e100_day0.py c30610f0...`; full SHA map in verify output (14 files). New files: see §5.

## 4. Issue #2 Day 1 execution (preregistered P1–P7, all PASS)

- Preregistration: `experiments/e100/day1-preregistration.md` v0.1 written BEFORE first `--self-test` in this invocation; predictions frozen (§P1–P7), falsifier + stop rule stated.
- Command: `python3 experiments/e100/day1.py --self-test` → `status: PASS`. P1 intact both `inspect_signal/c101`; P2 lesioned downstream `NO_ACTION` with primary unchanged, `intact_selects == lesioned_selects == 2`, ledger rows `1`; P5 completion both `NO_ACTION`; P3 wipe both `NO_ACTION`; P4 alternate both `record_measurement/c102`; P7 lesioned `NO_ACTION` on both tasks (no leakage); P6 rivals tie intact (point-to-point == compact == intact).
- Command: `python3 -m unittest discover -s experiments/instruments -p test_e100_day1.py -v` → 9/9 OK.
- Strongest rival: compact shared-state + point-to-point TIE broadcast → per frozen gate RETAIN SIMPLER, NO broadcast adoption. Fakhar single-lesion caution recorded: effect is by construction in zero-redundancy ledger; Lowe phantom-communication controlled via wipe/alternate/CIC-style downstream change.
- Failures: none in this scope. Not executed: real-SIGKILL variant of Day 1 (not required; simulated time permitted), multi-seed statistics (deterministic equalities), independent review, Days 2–7.

## 5. Files (proposed delta, NOT committed by this record)

- `experiments/e100/day1-preregistration.md` (new, frozen predictions/falsifier/parity)
- `experiments/e100/day1.py` (new, two-consumer lesion + rivals + self-test)
- `experiments/instruments/test_e100_day1.py` (new, 9 tests)
- `experiments/e100/day1-literature-synthesis.md` (new, source-level extraction with inspection depths, gaps)
- This run record (new).

## 6. Quality-gate self-assessment (why NOT accepted science)

- Q1 question/decision: yes (H003 instrument, D-future). Q2 strongest competitor: yes (two rivals, matched/≤ budgets). Q3 source method extraction: partial (depths honestly labeled; no full-PDF replication) — FAILS full-depth bar. Q4 causal validity: yes for toy (estimand = downstream-action difference under delivery cut; falsifier + 3 negative controls + leakage check). Q5 substantive: instrument only, by construction — correctly below acceptance bar. Q6 independent review: NONE (SELF-REVIEW_ONLY). Q7 provenance/L1-L3: labeled (OBSERVED local execution; PAPER-REPORTED secondaries; L1 circuit only). → EXPLORATORY_CHECKPOINT.

## 7. Anjo implication

NOT_READY_FOR_PRODUCT_TRANSFER. No architecture prescribed; no production change; no user data.

## 8. One next executable action

On a clean checkout of THIS PR's branch, rerun `python3 scripts/verify_instruments.py` + `python3 experiments/e100/day1.py --self-test`, confirm 83/83 (or updated count) and P1–P7, then a SEPARATE reviewer invocation adversarially reviews the preregistration (attempt: hidden side-channel, budget mismatch, coalition masking per Fakhar, phantom correlation per Lowe) before any Day 2 work. Stop on first falsifier or a concrete identifiability blocker.
