# H010 — poltergeist world: adversarial design SELF-REVIEW (2026-10-11)

**Reviewer identity:** SELF_REVIEW_ONLY, same model/session as author. No independent reviewer agent was available or contacted. This document is not a scientific review or empirical confirmation.

## Mechanism and causal question

New optional *world* on the shared `mind.worlds.World` contract; no new organ, claim or rival panel. Hidden lifetime polarity determines the signs of two actuator commands. Exogenous impulses and slips are pre-drawn for every tick independent of the agent's policy. The observed `dial` is the resulting sum. The actor's success `outcome` reports only net improvement, which can disagree with the causal contribution of its own command. Ground-truth shocks and actuation remain in private `Step.info`; the world never gives an `external` label in observations.

A future test should ask whether an action-conditioned predictive efference representation provides more *control* than a compact state estimator with exactly the same information. The world itself does not provide evidence for that proposition. A transcript estimator may fully match or outperform efference.

## Findings and attempted falsification

1. **Leakage / true-by-construction:** inspect each `_obs()` path. Only the resulting position is exposed. Private causal decomposition is on `Step.info`, which the shared runner does not send to agents. Unit test guards the separation. Still requires full-run trace inspection (NOT_EXECUTED).
2. **Action-dependent environment random numbers:** generating randomness conditionally on selected actions would invalidate paired arms. Pre-draw the entire episode's shocks and slips before any action; unit test checks two divergent policies receive identical hidden exogenous draws. Full-history K01/K06 verification remains NOT_EXECUTED.
3. **Metric gaming:** `wrong_corrections` alone rewards refusing to act; do not register a standalone claim on it. Mean reward is the primary outcome; wrong attempts are diagnostic. The score counts the **intended** wrong correction even if the actuator slips, preventing equipment luck from hiding a poor choice. Explicit test added.
4. **Saturating gradient:** initial clipped linear reward became zero beyond a dial magnitude of 8, hiding progress in bad trajectories. Replaced it *before any organism experiment* with `1/(1+abs(dial))`. Six local isolated instrument tests pass after revision.
5. **Reference rival compatibility:** existing `rival:bayes` advertises all worlds but its `ORACLES` mapping implements only vigil, outage and workshop. A new world would cause a KeyError in reference-rival invocations. Its registry is now explicitly limited to the implemented oracle worlds. Integration test remains NOT_EXECUTED.
6. **Episodic observational shortcuts:** stable actuator polarity can be inferred by averaging outcomes; this is intentional, not evidence of self-awareness. If a strong same-information estimator matches, H010's proposed special-mechanism effect fails. The design must not use the weaker action-blind `reactive` baseline as its only comparator.
7. **Calibration / unequal action mix:** comparison of Brier scores across different agents on their own event streams is invalid for causal calibration (C007/C008 precedent). Future claims should use paired same-world control scores for agency and, if comparing forecasts, a shadow scorer on the **same** actions and events.
8. **World adequacy:** this is a small synthetic control problem, not open-ended cognition. It has no affect, drive, valence, pain, deprivation, self-preservation or person data. Even robust results would support only a narrow L2 causal-organisation claim in the tested worlds.
9. **Hidden evaluation contamination:** engineering tests exercise `storm` for leaks and nontrivial confounds but do not inspect any git-sealed held-out seeds. No registered prediction exists. Do not tune a margin to these diagnostic tests.

## Verification and blockers

**Observed terminal results in isolated sandbox** (world protocol mirrored from main `0debeea`, *not* the full repo checkout):

```text
test_exogenous_events_unchanged_by_action_policy ... ok
test_heldout_variants_and_metric_contract ... ok
test_net_outcome_is_not_an_actuation_oracle ... ok
test_private_cause_never_sent_to_agent ... ok
test_seeded_reproduction_for_each_variant ... ok
test_wrong_corrections_score_choice_not_slip_luck ... ok

Ran 6 tests in 0.004s
OK
```

**Observed clone blocker** from container:

```text
fatal: unable to access 'https://github.com/kevindechang/MIND.git/': Could not resolve host: github.com
```

**NOT_EXECUTED on a full MIND checkout:** all existing unit tests, tests on branch head, `python -m mind doctor`, `python -m mind check`, `python -m mind atlas`, `python -m mind status --write`, baseline `mind run`, dev claim `--record`, and first `--heldout --record`. No claim or record was produced, and there are no verbatim `mind check` results to quote. `STATUS.md` was deliberately not manually edited.

The new world and the existing-reference registration guard are result-affecting code. **Every standing claim must be re-recorded under the new fingerprint before merge**, including all held-out records with their preexisting seals; their original preregistration standing cannot be rewritten. C016 and K01/K06/K07 may need special attention because they quantify over the expanded world suite.

## Next step and approval gate

Obtain a networked, full-history checkout on this branch. Run `python -m mind doctor`, `python -m unittest discover -s tests`, `python -m mind check`, and `python -m mind atlas` before any acceptance. Inspect the world with dev-only organism and action-conditioned transcript agents; determine whether reward is learnable rather than floor-limited and whether every paired arm gets the same disturbances. Do not alter any sealed claim based on the outcome. Build one efference organ and a same-information state-estimator rival **only after** this gate, seal a new claim, and record both dev and held-out including all failures. Re-run every standing claim with `--record` / `--heldout --record` because the result code changed, regenerate STATUS, and request a distinct reviewer. Never merge this PR before that work.
