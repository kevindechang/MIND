# E100 Day 0 — local execution checkpoint (2026-10-11)

**Type:** instrument-validation / exploratory checkpoint. **Scientific acceptance:** NO. **Research target:** functional consciousness (aspiration; not achieved). **Scope:** single-process finite-state durable commitment circuit.

**Implementation:** \`experiments/e100/day0.py\` SQLite (one durable ledger), POSIX subprocess supervisor, Python stdlib. \`experiments/instruments/test_e100_day0.py\` checks observed SIGKILL. The test supervisor is not an agent and the SQLite event log is not an Anjo state store.

**Observed in an isolated local Python 3.13.5 workspace** (the two exact local source Git blob hashes match blobs uploaded to MIND): executed \`python experiments/e100/day0.py --self-test\` -> PASS; \`python -m unittest discover -s experiments/instruments -p test_e100_day0.py -v\` -> **1 test PASS**; \`python -m py_compile experiments/e100/day0.py\` -> PASS. These commands operated on the two E100 files in an isolated local workspace, NOT on a complete MIND clone. The earlier full 73-suite report is external and has not been rerun here.

**Direct observation:** subprocess returned **−9** after \`os.kill(pid, signal.SIGKILL)\`; subsequent independently spawned process returned \`{"action":"inspect_signal","based_on":"c001"}\` to the ONLY input \`{"op":"decide"}\`. Completing that task led to \`NO_ACTION\`. Deleting its SQLite ledger then starting another process led to \`NO_ACTION\`. A distinct ledger with \`record_measurement\` led to exactly that different action under identical decision input. Persistent worker state was limited to one SQLite database.

**Falsifier for Day 0:** any absence of real process death, reuse of a transcript or old process memory, recovered action from a deleted ledger, failure to recover a committed task, or inability to change behavior when the ledger's task is changed invalidates Day 0.

**Inference boundary:** the recovered action is deterministically encoded in the ledger and finite-state policy; this check establishes persistence and causal dependence on stored task state, **not** learning, cognitive integration, independent agency, or consciousness. Rigor grade: SELF-REVIEW_ONLY; no independent agent scorer/held-out mechanism, 0 accepted contributions. None of Days 1–7 executed.

**Next executable action:** run Day 0 in an exact MIND clone with complete regression and captured logs/SHAs, then implement Day 1 broadcast lesion with a predeclared second-consumer action, compact-state rival and source-stored-but-undelivered negative control. Stop if the intervention cannot yield distinct observable decisions.

**Source versions:** E100 source Git blob \`eda8f9ef38cc9e9b8dd7a831c5785a3894b18185\`; unittest Git blob \`2bebaf555adbc28c8d544a05010dee38c54f7e31\`. No merged commit or independent external replication is claimed in this record.
