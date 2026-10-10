# E100 Day 2 — causal-memory lesion, synthetic instrument v0.1

**Issue:** #2. **Research date:** 2026-10-11 (Asia/Taipei). **Kind:** EXPLORATORY_CHECKPOINT / SHORT_RUN / DURATION_NOT_ENFORCED. **Reviewer:** SELF-REVIEW_ONLY. **Scientific acceptance:** ZERO; E001 G0 OPEN; E900 NOT STARTED; L3 unresolved. **Status:** local 12-arm real-process execution observed; not a scored agent experiment. This report is not a claim of functional consciousness or of an architectural benefit.

## Predeclared comparison and decision

Target: does selectively deleting an explicitly stored action-to-goal causal-dependency representation, without deleting raw history, alter a **future held-out intervention action** after true process death? In a toy world with two available interventions A and B and one goal, the worker has four public source records per world: one do(A), one do(B), plus two *contradictory observational* records. A compact sufficient-statistic controller is permitted to read the **same raw source** and recover the action outcome without causal-link storage. No transcript text is supplied to the resumed process; it reads its SQLite ledger only. Each policy receives one decision opportunity, the same action choices and no new probe budget. Exact CPU/SQL operation parity is NOT demonstrated; raw-source reconstruction may have a different cost.

**Before executing** the deterministic self-test, the expected contrasts were specified in code assertions: intact and sham choose DO_A in A-world and DO_B in B-world, lesion removes only action→GOAL links and abstains, compact/predictive rivals match intact despite the lesion, null world abstains in all arms, future-shift world defeats the apparent generalization of intact and compact. The private future reward table belongs only to the supervisor, never the worker decision request. Each arm has a distinct SQLite file, source event rows identical across intact/lesion/sham, and a true SIGKILL followed by a new PID. This is local predeclaration in the test source, **not** an independently timestamped/preregistered scored study.

**Estimand (instrument only):** deterministic within-world difference in supervisor utility of the causal-link-only policy, intact minus lesioned, for the same public event history; compare with the raw-history sufficient-state and predictive rivals. Utility is 1 if the one allowed future action matches the evaluator's future target (or abstains in NONE), else 0. It is **not** a causal estimate for a real learned agent or any population of environments. Null: deleting a redundant derived link does not reduce attainable action quality when the source history remains accessible.

## Results actually observed (local Python 3.13.5, POSIX)

Commands: `python -m py_compile experiments/e100/day2.py experiments/instruments/test_e100_day2.py` (PASS); `python experiments/e100/day2.py --self-test` (PASS, 12 arms in four world conditions); `python -m unittest discover -s experiments/instruments -p test_e100_day2.py -v` (7/7 PASS, ~26s on the available sandbox). One earlier combined test invocation was interrupted by an execution timeout after six checks; a later complete dedicated run succeeded. **Full canonical checkout/instrument regression NOT_EXECUTED:** the local sandbox could not resolve github.com, so byte-exact complete MIND checkout unavailable. Day 0/Day 1 were inspected by GitHub source, not rerun. The connector-published source/test Git blobs must be compared with locally observed hashes; if mismatch, mark branch source NOT VERIFIED rather than silently claiming parity.

| Training world / hidden future | Intact causal action / reward | Lesioned causal action / reward | Sham causal action | Compact/predictive action on lesioned ledger | Interpretation |
|---|---|---|---|---|---|
| A → A | DO_A / 1 | NO_ACTION / 0 | DO_A | DO_A / 1 | Intended representation lesion response |
| B → B | DO_B / 1 | NO_ACTION / 0 | DO_B | DO_B / 1 | Symmetric response |
| NONE → NONE | NO_ACTION / 1 | NO_ACTION / 1 | NO_ACTION | NO_ACTION / 1 | Negative-control null |
| A → B (unannounced shift) | DO_A / 0 | NO_ACTION / 0 | DO_A | DO_A / 0 | Identical public history to A-world cannot identify future change |

Every one of 12 arms observed a true subprocess return code -9 and distinct restart PIDs. The source row SHA256 matched across three arms in each world; the only manipulated table was `causal_links`. Sham removed an irrelevant clock→beacon edge; no change to goal action. Conflicting observational records were ignored; without any do() rows, both causal and compact readers abstained. A forbidden `future_winner` decision payload was rejected.

## Strong rival and rejected claim

**Most important result is negative:** the raw-history compact controller (and the simple predictive policy) ties the intact graph reader on all tested worlds, including after the stored causal links are deleted. This directly defeats a claim that the dedicated causal-link table is necessary for the tested future decision. The lesion hurts only a **policy engineered to read that table without reconstruction**. It is therefore a routing/storage dependency, not evidence that causal autobiography is uniquely required, nor a demonstration of cross-functional L2 cognition.

The future-shift counterexample proves an information limitation: worlds A→A and A→B have identical permitted predecision histories but different optimal future actions. No history-only controller can be uniformly correct on both absent an extra assumption/signal. A one-shot do(A) record and do(B) record do not identify a transportable causal mechanism without stability assumptions; observational decoys do not magically solve confounding.

**Decision:** E100 Day 2 instrument locally implemented and exercised; scientific status EXPLORATORY_CHECKPOINT. Retain compact/predictive-state rival as a required baseline, reject any claim of unique graph-memory necessity, no architecture adoption, no Anjo production transfer. E900 would require joint memory↔planning↔goal intervention in an integrated entity; this test is not it.

## Threats and next gate

This is a deterministic two-action lookup, with no stochastic observations, no multiple interacting causes, no continual updating, no unknown priors, no learned model, no uncertainty interval, no compute-parity benchmark, no agent population, no independent replication and no human-neuroscience correspondence. Its `do` events are synthetic labels, not randomized causal experiments in the world. The hidden future is evaluated by the supervisor but not genuinely out-of-distribution except in the explicit SHIFT falsifier. The same model wrote tests and interpreted results (SELF-REVIEW_ONLY). This cannot pass the MIND scientific quality gate.

**One next action:** on a clean exact checkout of the Day 2 branch, run `python scripts/verify_instruments.py` including the new suite and conduct a separate adversarial review of causal sufficiency/compute matching; report exact blobs, outputs and failures before merging or considering Day 3.

## Source depth

- MIND `experiments/E100-lesion-week.md`, `day0.py`, `day1.py`, issue #2, `research-quality-gate.md`, `sources/README.md` read directly from live main `3c22a93a6d15a909789bb6e40c387a34b183ee7c` (source-level methods).
- Pearl, *Causality*, 2nd ed. (2009), Ch. 3 publisher **chapter abstract** inspected; conceptual difference between intervention and observational association, NOT a replication or full-methods review. DOI: 10.1017/CBO9780511803161.005.
- Kaelbling, Littman & Cassandra, *Planning and Acting in Partially Observable Stochastic Domains* (1998), publisher/author **abstract** inspected, not full methods; motivates strong belief-state rival. DOI: 10.1016/S0004-3702(98)00023-X.
- No literature source above empirically validates this synthetic implementation. No claim of independent neuroscience evidence is made.
