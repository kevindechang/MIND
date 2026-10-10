# E100 Day 7 adversarial audit (exploratory)

Target: PR #12 head f15de4cf62007c221da0ba5d531f4ce838b1ce56; original source blob 57b804ee3cfbf0feaee07b78c49e57d6ec26a40d; test blob ff735f28de10fa1d097ce702d8cc4270b118c552.

Observed on Python 3.13.5: original self-test PASS; dedicated 4/4 PASS; independent stateless replay matches original actions in 4/4 canonical forks and 256/256 seeded histories (seed 1707). Three frozen adversarial provenance fixtures reveal hard-coded goal-001 citation for goal-999, misattribution when goal-002 is blocked, and citation of unrelated light restoration. Original actions still match the stateless rival. This does not establish a unique private-state benefit.

EXPLORATORY_CHECKPOINT / SELF-REVIEW_ONLY. No full checkout, integration suite, model trials, or independent reviewer. Accepted 0; E001 G0 OPEN; E900 NOT STARTED; L2 unachieved; L3 unresolved. NOT_READY_FOR_PRODUCT_TRANSFER.

Next: make provenance citations derive from the actual blocking commitment and resource-specific latest relevant status, add all three negative-control fixtures, and rerun original plus integrated regression on a byte-exact checkout before considering mechanistic claims.
