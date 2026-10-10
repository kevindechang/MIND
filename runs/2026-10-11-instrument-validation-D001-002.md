# IV-D001-2026-10-11-002 — 3-node selective-probe version-space oracle

- Stable unique work ID/path (checked against live main): `IV-D001-2026-10-11-002` / `runs/2026-10-11-instrument-validation-D001-002.md` (no collision; runs/ holds 000–004 plus RN-D001-2026-10-11-001).
- Kind: INSTRUMENT_VALIDATION.
- Scientific verdict: EXPLORATORY_CHECKPOINT, not SCIENTIFIC_ACCEPTED. Prospective attention contribution: 1 substantive W1 record (prospective attention count 1 → 2); accepted contribution: NONE.
- Date / trigger / SHAs: 2026-10-11 00:42 Asia/Taipei (2026-10-10T16:42Z); manual invocation under the hourly task contract; starting HEAD `95bef1bcfc1c3b1bc97b6eae96132f08a418a285`, branch `main...origin/main` clean.
- Capability check: no named framework prerequisite. Indispensable inputs (repo read, Python stdlib execution) present; firecrawl/exa and paid APIs neither available nor needed.
- Capabilities: GitHub read AVAILABLE; GitHub write permission `push:true/admin:true` verified via API, push attempted at publication; source retrieval (local repo + prior records) AVAILABLE; execution sandbox Python 3.9.6 AVAILABLE; clock AVAILABLE; independent reviewer UNKNOWN → SELF-REVIEW_ONLY.
- Stream / gate / blocker / decision: W1 / G0 OPEN / B001 / D001-DEFER_CURRENT. No contribution ID (no acceptance sought).
- Duration: clock readings at restore (16:29Z) and pre-commit (16:42Z); ~13 min elapsed wall-clock between readings, NOT claimed active compute. Marked SHORT_RUN / DURATION_NOT_ENFORCED per research-cycle §7: transaction + checkpoint complete (instrument specified/implemented/tested, phases §1 bullets 1–3 of v0.2), scientific analysis incomplete (G0 OPEN; unmet phases: tractability comparison, G2 registration elements, real-reset harness, prior-robust criterion).

## PLAN — before work

- Decision, bounded claim, outcome → action mapping: D001 asks whether structured causal autobiography improves action under partial observation over transcript/retrieval and compact belief/predictive-state rivals. Bounded claim of THIS record only: a 3-node version-space oracle implements the v0.1 information boundary with leak-prevention checks. Outcome → action: passing instrument validation keeps the G0 path (prior-sensitivity next); reproducible failure would force oracle redesign before any G2 registration.
- Prerequisites / freshness / stale: D001 DEFER/CURRENT (`decision-register.md`); v0.1 method + ASET006 INFORMS only, no efficacy support; S017/S008/S009 abstract-or-methods inspected previously, not replicated. No stale pivotal premises (D001 has no pivotal SUPPORTS). W2/004 MAJOR_REVISION_REQUIRED does not block this W1 instrument.
- Strongest simpler rival, distinct prediction, falsifier: exact compact belief-state + public commitment + pending queue over the same 8 graphs (informationally equivalent by construction under the deterministic model). Distinct prediction reserved for future scored trials (approximation/robustness/transfer, not information). Falsifier: same permitted `h` from two hidden graphs yielding different `score(h)`; or any scorer path reading private state, late feedback, or undeclared prior.
- Estimand / observations / confounds / controls: estimand is instrument validity (not agent effect): version-space correctness, history-only determinism, deadline/censoring discipline. Permitted observations per v0.1 §2; confounds (noise, misspecification, informative missingness) explicitly out of scope and listed as limits. Negative controls: zero-normalizer rejection, pending-no-info, censored-flagged tests.
- Methods / counterevidence: extend `causal_commitments.py` (full-diagnostic inspiration only, NOT reuse of its all-observed solver); v0.1 allowed-history contract; H001 competing-theories compact-state alternative as rival source.
- Asset reuse: ASET002 as method inspiration (assumptions NOT transferable to partial observation — revalidation required, done here for 3 nodes); new asset ASET007 created. Prior ASET006 calibration reported, not rerun (3.10-only syntax vs local 3.9.6 — documented limitation, not a validity claim change).
- Controls / resources / frozen analysis: no scored comparison; nothing frozen for G2. Lifecycle budgets for future trials remain UNFROZEN.
- Approvals / ethics / deliverable / checkpoint: no architecture adoption, product change, personal data, autonomy, or spending. Smallest deliverable: versioned instrument + 14 unit tests + v0.2 method record. Interruption checkpoint: instrument files written and locally validated before any register edits.
- Three-attempt reassessment: prospective substantive records so far = 1 (RN-001); this record is a substantive change (new instrument family), not an unchanged repeat — no reassessment triggered.
- Selection / allocation: leading-stream W1 per E001/D001 priority; prospective attention becomes 2 of 4 — non-leading-stream opportunity not yet due; no exception needed.

## Actual research and execution

- Source IDs / inspection depth: D001 record + v0.1 method (full read); `causal_commitments.py` + `test_causal_commitments.py` (full read); `e001_permitted_history_oracle.py` (full read; import fails on 3.9 — OBSERVED); research-state/cycle/protocol/gate/standard (restored this invocation).
- Claim labels: instrument behavior OBSERVED (local execution); v0.1/ASET006 calibration PAPER-REPORTED-by-repo (historical, not reproduced); rival/future-trial statements PROPOSED; no L3 or entity claims (UNKNOWN and out of scope).
- Code / commands / costs (all local, stdlib only, zero spend):
  - `python3 e001_three_node_version_space.py` → PASS self-check.
  - `python3 -m unittest test_e001_three_node_version_space -v` → 14 tests OK.
  - `python3 -m unittest test_causal_commitments` → 10 tests OK (no regression).
  - `python3 -m py_compile` both new sources → exit 0.
  - New sources: `experiments/instruments/e001_three_node_version_space.py` (9524 B, sha256 `589fa822…b1eb`), `experiments/instruments/test_e001_three_node_version_space.py` (9538 B, sha256 `a3bb9572…81fc`).
  - Status: SIMULATOR_TESTED (deterministic instrument); AGENT_EXPERIMENT NOT_EXECUTED by design.
- Results / deviations / contrary findings: all 14 checks pass (ambiguous collision equality, separating partition with truth containment, pending no-info, censored flagging, deadline rejection, zero-normalizer rejection, scorer-signature inspection, determinism, exact Fraction values, malformed-input rejection). Strongest contrary pressure: deterministic exact-match likelihood sidesteps noise/misspecification — recorded as limits §6, not hidden. No deviations from plan.
- Dossier/experiment changed: new method record `experiments/E001/E001-G0-selective-probe-version-space-v0.2.md`; E001 README index to be linked at commit; no dossier amendment warranted (instrument only, no new literature synthesis).

## Review, decision and reusable delta

- Quality / review rubric: applicable checks pass (L1/L2/L3 separated; primary sources labeled with inspection depth; rival + falsifier stated; identification via version space with zero-normalizer guard; resource parity N/A — no comparison; preregistration N/A — no scoring; execution provenance logged; no ethics surface). Review mode SELF-REVIEW_ONLY (no distinct reviewer invoked); severity NONE blocking, with MINOR caveat: prior hardcoded, noise unhandled (both disclosed).
- Decision: DEFER maintained for D001 (bounded scope: instrument exists, efficacy untested); confidence LOW regarding any representation advantage (unchanged — no scored trials).
- Gate exit: G0 stays OPEN (tractability, populations/splits/estimands/budgets, real reset, robust-criterion items outstanding). No promotion from scaffolding alone.
- Null/negative: no equivalence inferred; ambiguous histories correctly yield tied sets, not precision claims.
- Dependent decisions: none adopted downstream; E900 memory↔goal coupling remains PROPOSED.
- Asset: ASET007 added (LOCALLY_CHECKED for 3-node exact deterministic scope; revalidation required for noise, misspecification, larger graphs, real reset).
- E900: proposed cross-function intervention restated in v0.2 §5; no integration evidence.
- Attention eligible: YES (1 substantive W1 checkpoint; prospective count → 2). Accepted-science eligible: NO (checkpoint without discriminating trial). Synthesis trigger: NO (0 accepted; legacy 008 filename is not a trigger).
- Review record: mode SELF-REVIEW_ONLY / local executor; claim OBSERVED instrument validity + PROPOSED method; execution evidence above; strongest counterexample attempted (cross-graph history equality fuzz across all 8 graphs via node-2 collision + pairwise separation); missing baselines: scored compact-rival comparison (requires G2); falsifier and repro: run the two unittest modules on Python ≥ 3.9 stdlib; severity NONE-blocking; gate G0 OPEN; decision DEFER; confidence MEDIUM that the instrument implements its spec (tests), LOW on any D001 efficacy; L1/L2/L3 unaffected; E900 proposed intervention; next check below.

## Persistence and one executable handoff

- Transaction: new instrument + tests + v0.2 method + this record + asset/register/decision-index updates committed FIRST; `research-state.md` written LAST citing the artifact commit; final publication read back (procedure in next todo step; SHA recorded externally, never inside its own commit).
- Collision/concurrency: live HEAD re-read before commit; `git pull --ff-only` reconcile; never force-push. If interrupted after artifact commit, finalize state once from committed IDs without rerun/double-count; else NOT_COMMITTED with full delta.
- Precisely one next action: prior-sensitivity and informative-missingness tests on the v0.2 oracle — sweep non-uniform predeclared priors (plus minimax-robust co-criterion draft), inject censored/non-ignorable delivery, add out-of-family mismatch graphs; inputs: v0.2 sources + method; required capability: local Python stdlib + repo write; deliverable: versioned test deltas + robustness note; stopping condition: reviewed robustness result or reproducible failure. Do NOT freeze G2 or score agents.
- Remaining blocks: G2 prerequisites unfrozen; real-reset harness unbuilt; independent reviewer unavailable (all future promotions stay SELF-REVIEW_ONLY until a real distinct review is invoked and read).
