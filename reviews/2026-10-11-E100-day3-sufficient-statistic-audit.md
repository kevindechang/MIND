# E100 Day 3 independent-as-possible adversarial audit: a sufficient-state rival closes the confidence gap

**Status:** REVISE / EXPLORATORY_CHECKPOINT / SELF-REVIEW_ONLY. **Issue:** #2. **Target:** PR #8, `research/2-day3-self-model`, immutable head `90e7aadf9f71cf202d4af75e27915d15626d8dd5`. **No main/research-state edits; accepted scientific contributions remain 0.** This is a source-level audit and retrospective deterministic challenge, *not* a preregistered agent comparison, human trial, calibrated confidence result, independent peer review, or evidence of L2/L3 consciousness.

## Question and decision effect

Does Day 3 identify a *predictive self-model* over an information-matched compact state controller, once **all declared outputs** (choice, action, confidence and NO_GOAL) are evaluated? A useful positive result would favor a maintained self-model for H002 and eventual E900 self-monitoring. A tie on all endpoints supports keeping a cheaper sufficient-state policy as the baseline and **deferring** architecture selection. Negative tool-choice safety results would require an abstention/action-validity endpoint before any downstream transfer.

### Exact inspected source and provenance

- PR #8 `experiments/e100/day3.py`, Git blob `fbf35c6c3875664790f1db9643229950a95564f2`; `experiments/e100/day3-preregistration.md`, blob `6dcef1f8c60a04f6df4bc7f83db76d0e9ff9e7e6`; `experiments/instruments/test_e100_day3.py`, blob `e1ec811f428df29c8a0d064ffa09395229f4db1f`.
- The original frozen predictions P1–P6 were inspected **in full**. Source `setup` preloads the preferred tool's availability from the scenario generator; `adaptive` reads events, goals and capabilities; `rival_table` reads **capabilities only** and emits **no confidence**; `fixed_persona` ignores both event conclusions and missing goals. No scientific literature inference is needed for the deterministic program argument below.
- Direct git clone failed due to DNS. The PR source was transcribed into a temporary sandbox file and verified **byte-identical** by `git hash-object` = `fbf35c6c3875664790f1db9643229950a95564f2`, then executed. This validates that single source file only, not a full checkout of main or PR #8's test file. The audit probe refuses to run against a changed source blob.

## Constructive rival and proof boundary

Let **E** be the observed source-events rows and **C** the supplied capability table; **G(E)** means some event kind begins `commitment:`. Let **O(E)** be the tools with an observed `tool_unavailable` event, and define:

`usable(t) = bool(C.get(t, 1)) and t not in O(E)`.

For a goal, select the first usable tool in `(preferred, spare)`, else fall back to `preferred`; emit `confidence = 0.9` exactly when the selected tool is preferred and `0.4` otherwise. Without a goal, emit `(None, None, NO_GOAL)`. These rules are an extensional specification of PR #8's `adaptive` reader. They require only flat scans of **the same events and capability rows**; neither a self-model object nor inferred latent state is necessary for these declared outputs. Thus a flat, **event-aware** rival can tie **choice, action and confidence** for every database state within this two-tool rule family. This is an equality of source-defined functions, **not** proof of parity for actual runtime, training, accuracy, semantics of the word self-model or model learning.

PR #8 already observes a choice tie in the default scenario. Its constructed “confidence gap” is **output-schema asymmetry**, because `rival_table` simply omits confidence. Adding the same deterministic confidence output to the event-aware table closes this gap without new information. The original P1–P6 instrument results remain valid as tests of the source implementation; the inference that richer self-modelling is uniquely required does not follow (and the original PR explicitly does not claim calibration).

## Executed adversarial probes (not frozen scored trials)

From the PR source at the pinned blob, run `python3 experiments/e100/day3.py --self-test`, then `python3 -m py_compile reviews/e100-day3-audit/probe.py experiments/e100/day3.py`, then `python3 reviews/e100-day3-audit/probe.py --day3 experiments/e100/day3.py`. Local Python **3.13.5**; all three commands exited 0. Raw structured probe output: `reviews/e100-day3-audit/observed.json`.

The probe exhausts **72 deterministic finite cases**: commitment present/absent (2) × missing/0/1 snapshot for preferred (3) × missing/0/1 snapshot for spare (3) × preferred-outage flag (2) × spare-outage flag (2). **72/72** match between PR `adaptive` and the compact event-aware rival on **all three output fields**. This is exhaustive only for this deliberately restricted case family; it is not a random sample or generalized empirical estimate. The original six test cases were **not** rerun as a suite in this session; the source's own self-test was rerun.

Three extra diagnostic counterexamples were observed, all **outside** the frozen PR seed domain and therefore **not** registered-prediction failures:

1. **Both tools unusable** (`C[preferred]=C[spare]=0`, goal present): PR `adaptive` chooses `USE_PRIMARY` with confidence **0.9** anyway, even though its own feasibility lookup returned neither tool. A policy with an `ABSTAIN/REPLAN` action would avoid this particular contradiction. This demonstrates that its confidence number is a fixed choice label, **not** calibrated reliability.
2. **Stale snapshot** (`C[preferred]=C[spare]=1` followed by observed outage for preferred): PR's original `rival_table` chooses unavailable `primary`, while PR `adaptive` and the fair event-aware table choose `spare`. An advantage against the original table in this case would come entirely from the original rival **not reading the available event**, not from the existence of a sophisticated self-model.
3. **No goal** (`G(E)=false`): `adaptive` returns `NO_GOAL`, while `fixed_persona` still chooses `USE_PRIMARY`. The lesion changes **goal authorization/guarding** as well as capability dependence, so it is not a surgical test of self-model content alone.

The manually incremented `qc` counters in Day 3 count selected query *classes* in different branches; they are not actual matched wall time, SQLite trace counts, serialized state bytes, update/preprocessing costs or external-agent opportunity parity. The event-aware rival might be cheaper or dearer in a real implementation; costs must be measured, not assumed.

## Falsifier, limitations, and revision recommendation

**Falsifier of the review's narrow theorem:** identify a valid source database state within the two-tool interface for which `adaptive(db)` and the flat event-aware rival differ, under identical observation and tie-breaking rules. The 72-case check supports the equivalence in a finite subdomain; the line-by-line rule extraction supplies its conditional general argument. A hidden learned policy, feedback-dependent preference, invalid schema row, multi-step partial observation, stochastic execution or altered implementation falls outside that claim. Confidence cannot be calibrated without outcome labels; a by-construction confidence match is neither a useful prediction nor a safety guarantee.

**Disposition:** PR #8 is acceptable as a bounded **instrument checkpoint** only with its existing honesty labels intact. Do not promote H002, L2, E900 readiness, or Anjo adoption. In the next prospective self-model comparison, both arms should receive the same histories and capability observations, support an explicit *no-safe-tool* action, learn/predict changing tool success over multiple held-out episodes and score **actual outcomes** plus confidence with Brier/log loss, regret and net compute/maintenance cost. Compare a maintained predictive self-model with a jointly trained, event-aware compact belief-state policy and report ties or failures. Register resource limits, seeds, scenario families, distribution shift, reset protocol and practical margins before trials. Avoid scoring on these retrospective fixtures.

**E900 implication:** a future self-monitoring organ must show incremental cross-session *prediction/action* benefit on unanticipated tool degradation beyond adequate compact state, not merely a preference for a module's narration. **D001/E001 G0:** unchanged/open. **Accepted count:** 0. **Anjo:** NOT_READY_FOR_PRODUCT_TRANSFER.

**One next executable action:** the PR #8 owner or an independent integrator should add an *event-aware, full-output compact competitor* and an explicit abstention rule to a separately frozen Day-3-v0.2 comparison, then run it on held-out changing-reliability trajectories under measured parity; stop and retain the simple baseline if incremental net outcome benefit is absent.
