# Day 7 exact-head adversarial results

Python 3.13.5 Linux. Source/test Git blobs verified: `57b804ee3cfbf0feaee07b78c49e57d6ec26a40d` / `ff735f28de10fa1d097ce702d8cc4270b118c552`. Main `3c22a93`; PR12 `f15de4c`.

Original: `python3 day7.py --self-test` PASS; `python3 -m unittest discover -s experiments/instruments -p test_e100_day7.py -v` 4/4 PASS; `python3 -m py_compile` PASS. Exact original files were reconstructed, not a full checkout. Independent pure event-replay rival: 4/4 canonical fork actions and 256/256 seeded synthetic histories match. Seed 1707.

Frozen counterexamples, original `based_on` -> correct minimal attribution:

- goal-999 outage: `[goal-001,out-999]` -> `[goal-999,out-999]` (nonexistent citation).
- goal-002 sensor blocked: `[goal-001,out-002]` -> `[goal-002,out-002]` (wrong goal).
- unrelated light restored: `[goal-001,restored-light]` -> `[goal-001]` (irrelevant evidence).

All original actions match rival; 3/3 provenance checks fail. The single public `source_events` table contains all post-fork changes; no private-state-specific lesion was executed. Not a learned-agent, resource-parity or consciousness result. Full regression, preflight, Day7 SIGKILL, and external review NOT_EXECUTED. Verdict EXPLORATORY_CHECKPOINT / SELF-REVIEW_ONLY, accepted 0, NOT_READY_FOR_PRODUCT_TRANSFER.
