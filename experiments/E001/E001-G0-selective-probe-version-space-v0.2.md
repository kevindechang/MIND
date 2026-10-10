# E001 G0 — Selective-probe finite-world version-space oracle v0.2 (3-node)

**Date:** 2026-10-11 (Asia/Taipei). **Decision:** D001 / H001 / W1 / blocker B001.
**Artifact kind:** INSTRUMENT_VALIDATION; **scientific verdict:** EXPLORATORY_CHECKPOINT,
not SCIENTIFIC_ACCEPTED. **Status:** versioned 3-node instrument specified,
implemented, and locally validated with 14 unit checks; G0 remains OPEN, G2 NOT
FROZEN, no agent trial. **Review:** SELF-REVIEW_ONLY. No external API expense.
Supersedes nothing; extends [v0.1 permitted-history oracle](E001-G0-permitted-history-oracle-v0.1.md).

## 1. What v0.1 left open and what this version closes

v0.1 defined the permitted-history information boundary and a Bayes-admissible
history reference for a one-bit synthetic family, with 16 exact-arithmetic
calibration checks. Its §9 checklist left these G0 items open:

- [x] A version-space oracle over an explicit finite graph family for a minimal
      CausalWorkshop subset, emitting only selectively requested feedback with
      censoring/dropout and commitment/probe budgets.
- [x] At least one ambiguous and one separating intervention history, with no
      private graph access in the action scorer.
- [x] Explicit deadline and censoring tests; identical public histories yield
      identical posteriors/action sets regardless of the evaluator's private
      sampled graph.
- [ ] Tractability/approximation comparison and state-space scaling costs.
- [ ] Target populations, family splits, outcome estimands, scored-trial
      budgets, and statistical registration (G2 prerequisites).
- [ ] Real model process reset with allowed-state checksum and parity checks.
- [ ] Prior-robust vs Bayes reference criterion decision.

This v0.2 closes the first three bullets only. It does NOT close G0, freeze G2,
compare memories, or score any agent.

## 2. Predeclared family, prior, and public boundary

- **Family:** all 8 forward DAGs on nodes {0,1,2} (edges ⊆ {(0,1),(0,2),(1,2)}),
  canonical order in `all_three_node_dags()`. Seeded enumeration is trivially
  reproducible; the family is fixed, not fitted.
- **Prior:** uniform, `Fraction(1,8)` each. Hardcoded and disclosed; prior
  sensitivity is an explicit unresolved item (§6).
- **Likelihood:** deterministic exact reachability masks (self included, matching
  `causal_commitments.CausalWorkshop` semantics). A delivered outcome is
  consistent with a candidate graph iff every delivered `(node, mask)` pair
  equals that graph's reachability mask.
- **Permitted public history** (`PublicHistory`): commitments (goal/desired/
  penalty, same validity rules as CausalWorkshop), probe records (event_id,
  node, issue_tick, due_tick), delivered outcomes (event_id, node, mask),
  censored event flags, and decision deadline. Pending events (issued, neither
  delivered nor censored) are distinguished. Post-deadline delivery is rejected
  at construction; the queue is never drained past the deadline for scoring.
- **Evaluator private (never in scorer inputs):** sampled hidden graph, seed,
  full influence matrix, withheld labels, reward-generation internals.

## 3. Reference policy

Posterior is uniform over the version space `V(h)` (consistent graphs);
empty `V(h)` raises `ValueError("zero normalizer")` instead of assigning an
arbitrary label. For each feasible plan ((), 3 singles, 3 pairs — the same
length ≤ 2 enumeration as CausalWorkshop), expected utility is the uniform
average over `V(h)` of `-(commitment loss + len(plan))` with XOR effect
composition. The reference returns the full tied maximizer set in sorted order;
sorted-first is a software comparison convention only and a tied alternative is
never counted incorrect. This is the v0.1 Bayes reference restricted to the
declared family with deterministic likelihood — not a claim any deployed system
knows the prior or dynamics.

## 4. Discriminating histories (OBSERVED in local execution)

- **Ambiguous/colliding:** probing node 2 always yields mask `100` in all 8
  graphs, so `h` is byte-identical whether the evaluator sampled G_EMPTY or
  G_FULL. Asserted: equal version spaces (all 8), equal posteriors, equal
  `score()` outputs across hidden truths.
- **Separating:** probing node 0 yields `001` under G_EMPTY vs `111` under
  G_FULL; version spaces are disjoint, each contains its truth and excludes the
  liar. Two-probe history under G_CHAIN contains the truth and every member
  satisfies all delivered masks.
- **Pending:** probe due tick 3 with deadline 2 contributes no information;
  posterior/score equal the no-probe history (sunk cost recorded in the probe
  log, not in the belief).
- **Censored:** a due-but-withheld event is flagged in `history.censored`,
  excluded from the version space, and the history is unequal to a never-probed
  history — preventing silent informative-missingness leakage.
- **Zero normalizer:** mask `111` for node 2 (impossible in all candidates)
  raises instead of labeling.

## 5. Rival, falsifier, and E900 coupling

- **Strongest simpler rival (PROPOSED, not tested):** exact compact belief-state
  (posterior over the same 8 graphs) plus public commitment record and
  pending-event queue — no stored causal-episode graph. Under the declared
  deterministic model it is informationally equivalent by construction; D001
  must therefore be decided on finite-budget approximation, robustness to model
  mismatch, compactness, and cross-task transfer, not on information creation.
- **Falsifier for this instrument:** exhibit two private graphs producing the
  same permitted `h` but different `score(h)` outputs without any
  prior/likelihood difference; or find any code path where `score` reads hidden
  edges, influence, late feedback, or the sampled theta. `test_private_state_
  never_enters_scorer` plus signature inspection (`score(history, family)`)
  guards this; a counterexample invalidates the instrument.
- **E900 coupling (PROPOSED):** after a scoped D001 result under separate
  approval, corrupt one recorded own-action→consequence link while holding
  observations and budgets fixed; compare downstream goal repair against the
  compact-state rival and a sham. No integration evidence is claimed here.

## 6. Exact limitations (what this is not)

1. Deterministic exact-match likelihood only; the v0.1 noisy-feedback regime
   (q=0.75) is not carried over, and model misspecification / hidden
   confounding have no controls yet.
2. Uniform prior hardcoded; no sensitivity sweep or robust-minimax co-criterion.
3. No tractability analysis; 8-graph enumeration does not scale and no
   approximation strategy is compared.
4. No real process reset, checksum, or observation-parity harness; reset
   semantics are specified (v0.1 §2) but unimplemented.
5. No LLM/controller arms, no scored trials, no preregistered thresholds —
   G2 prerequisites (populations, splits, estimands, budgets, seeds, stopping)
   remain unfrozen.
6. Runtime note: existing `e001_permitted_history_oracle.py` uses `int | None`
   annotations requiring Python ≥ 3.10 and fails to import under this
   invocation's Python 3.9.6; ASET006's historical 16-check calibration is
   therefore reported, not freshly reproduced here. The v0.2 sources avoid
   post-3.9 syntax and compile under 3.9 (`py_compile` PASS).

## 7. Execution provenance (OBSERVED)

- `python3 e001_three_node_version_space.py` → self-check PASS (family,
  collision, history-only scoring).
- `python3 -m unittest test_e001_three_node_version_space -v` → 14 tests OK.
- `python3 -m unittest test_causal_commitments` → 10 tests OK (no regression).
- `python3 -m py_compile` on both new sources → exit 0.
- Sources: `experiments/instruments/e001_three_node_version_space.py`
  (9524 bytes, sha256 `589fa822be1d8a6e18f2df4aecb2a7cf05f093db6bfe944831b0988e043ba1eb`),
  `experiments/instruments/test_e001_three_node_version_space.py`
  (9538 bytes, sha256 `a3bb95729565c789acceba8bd888dd09b70883a0b862220f88436af881182fc1`).
- L1/L2/L3: calibration of an evaluation instrument only; no agent behavior,
  no causal-organization evidence, no phenomenal claim. E900 NOT STARTED.

**Verdict:** EXPLORATORY_CHECKPOINT with observed local instrument validation.
D001 stays DEFER/CURRENT; H001 CANDIDATE; A0 PROPOSED; A1 UNSELECTED.

**One next executable action:** prior-sensitivity and informative-missingness
tests on this v0.2 oracle — sweep non-uniform predeclared priors (including a
minimax-robust co-criterion draft), inject censored/non-ignorable delivery
processes, and model-mismatch graphs outside the 8-family; deliver versioned
test deltas and stop at a reviewed robustness result or reproducible failure.
Do NOT freeze G2 or score agents during that step.
