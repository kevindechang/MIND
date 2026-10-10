# PR #7 — Review and remediation handoff (post-v0.1)

**Kind:** CODE_REVIEW_AND_INSTRUMENT_PATCH; **scientific status:** EXPLORATORY_CHECKPOINT / NOT_VERIFIED_v0.2; **accepted science:** 0; **reviewer provenance:** SELF-REVIEW_ONLY. Scope issue #2.

## Fixed-point review
- Original PR head: `859e4745860286b9d0e60f5e6b23dfc05d4eeb41`; target base: `3c22a93a6d15a909789bb6e40c387a34b183ee7c`.
- Review plugin instructions actually read: `engineering-suite-review/entry-review`, `code-review`, `code-review-and-quality`, `doubt-driven-development` (fresh reviewer unavailable; no subagent claim). Compared issue #2, E100 Day 2 row, GO, CONTRIBUTING, quality gate, actual GitHub diff and test file. No mandated external issue-tracker helper was present; the actual live GitHub issue was used.
- Comment review 5480430690 posted to PR. GitHub rejected REQUEST_CHANGES on author's own PR (HTTP 422), so COMMENT is the effective review status.
- **Spec findings (4 blocking):** Day2 function-only execution (no restarted worker); compact snapshot supervisor-injected truth and unmatched build cost; P6's renamed IDs mistaken for structural holdout; absent irrelevant-link sham and manually maintained query-count parity.
- **Standards findings:** no concrete project style violation; duplicative setup/check patterns are heuristic, not a hard blocker. SQLite queries use parameters; no new external dependencies or Anjo data.
- Initial author's reported v0.1 test evidence was 82/82 on their machine; NOT freshly reproduced during this review.

## v0.2 source revisions committed to the PR branch (not yet tested)
- `experiments/e100/day2.py`: seed, SIGKILL and new worker process per arm; resumed readback accepts only `{"op":"report"}` and SQLite path. Add actual SQL trace, derive compact sufficient state by querying the same initial event/graph facts before any lesion, add irrelevant-edge sham, and add a structurally longer held-out path.
- `experiments/instruments/test_e100_day2.py`: four additional tests, covering true subprocess restart, sham surgery, compact derivation provenance and changed dependency structure plus separately scored one-step supervisor action. Original seven retained.
- `experiments/e100/day2-preregistration.md`: **post hoc v0.2 amendment**, not a rewrite of the frozen v0.1 prediction; original runs and all previous verdicts preserved.

## Verification boundary and risks
- A local Python 3.13.5 interpreter exists, but the private MIND checkout could not be cloned from this execution environment (DNS failure); exact revised branch bytes were accessible through the GitHub connector only. **Revised code unit tests, Python py_compile, Day 2 self-test and full integrated suite: NOT_EXECUTED by this reviewer.**
- Original v0.1 82/82 must not be attributed to the revised branch. All v0.2 outputs remain **predictions**, not observed results.
- The score is a deterministic by-construction one-step rule. Although the compact state is now derived from the shared graph and events rather than simulator-truth parameter, offline compilation effort is not resource matched to a learned graph controller. Thus a tie is a useful strong upper-bound rival but does not identify a unique memory mechanism.
- No independent reviewer was dispatched. No entity-scale functional consciousness or phenomenology inferred. E001 G0 remains OPEN; E900 NOT STARTED; MIND state/index untouched. Anjo: NOT_READY_FOR_PRODUCT_TRANSFER.

## Required next action
Clone the exact latest PR #7 head in a local authenticated environment, run `python3 -m py_compile experiments/e100/day2.py experiments/instruments/test_e100_day2.py && python3 experiments/e100/day2.py --self-test && python3 -m unittest discover -s experiments/instruments -p test_e100_day2.py -v && python3 scripts/verify_instruments.py`, preserve byte hashes, exact stdout/stderr and Python/platform version, then independently review the evidence before merging. If any test fails, fix on same issue branch, do not silently retune results.
