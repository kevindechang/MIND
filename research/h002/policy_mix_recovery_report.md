# H002-S2 policy-mixture stress: exploratory evidence (2026-10-11)

Status: SELF-REVIEW_ONLY; EXPLORATORY_CHECKPOINT; NOT_READY_FOR_PRODUCT_TRANSFER.

This record is a recovery publication of a previously executed isolated experiment, NOT a new execution or full MIND regression. The complete source, test and numerical JSON are in the local reproducibility package MIND_H002_S2_Policy_Mixture_Research_FULL.zip; these are not yet fully persisted here.

## Frozen comparison and observations

Fixed-policy synthetic outage traces; compact capability-state filter versus original contextual self-model; identical public observations and feedback. 32 seeds per condition, 960,000 simulated ticks across five scan rates and two outage conditions. Brier score compact minus self-model (negative favors compact):

| Scan rate | Announced | Silent |
|---|---:|---:|
| 5% | -0.0430 | -0.0086 |
| 15% | -0.0678 | -0.0262 |
| 35% | -0.0676 | -0.0306 |
| 60% | -0.0517 | -0.0258 |
| 90% | -0.0173 | -0.0080 |

At 5% scan/silent outage, paired 95% interval [-0.0192,+0.0018] includes zero: INCONCLUSIVE. At 90% scan, alert-blind filter loses to self-model while alert-aware filter wins, highlighting dependence on public alerts.

## Reported local verification (previous sprint; not re-run in this GitHub publication)

Dedicated new tests 8/8 PASS; previous H002 tests 12/12 PASS; source blob checks 3/3 PASS; fresh-package numerical reproduction 10/10 identical. Full checkout regression, independent review, organism action-stream C017/C018 replication: NOT_EXECUTED. The original logs and exact files must be independently reviewed before promotion.

## Scientific decision

The compact rival has favorable point estimates in this synthetic fixed-policy comparison; no causal demonstration of functional consciousness or unique self-model advantage. Strong rival result is valid negative evidence. L2 UNACHIEVED, L3 unresolved, accepted science 0, E001 G0 OPEN, E900 NOT STARTED. No product transfer.

## Falsifier and next action

Reproduce the full archived package from byte-exact source, then test original organism action streams and matched public information/resources. A tie, reversed effect, or alert dependence is admissible negative evidence. Do not merge without review. Duration UNKNOWN / DURATION_NOT_ENFORCED.
