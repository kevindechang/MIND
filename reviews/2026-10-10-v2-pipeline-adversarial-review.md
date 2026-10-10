# Adversarial review of the v2 pipeline (2026-10-10)

**Reviewed:** branch `pipeline/v2-compounding` at `a089e8e` (substrate, claims engine, 27 claims, two records).
**Reviewer:** a separately invoked agent of the same model family, with no write access and its own context.
That makes it a *self-review in a separate context*, not independent replication. Its repro scripts were run and
their outputs inspected before acting.
**Outcome:** 1 critical, 7 important and 5 minor findings. All were confirmed except the inherent limit on seed
grinding (2a), which is documented rather than fixed. Every disposition below is visible in the claims and
records. Nothing was deleted.

| # | Finding (severity) | Evidence | Disposition |
|---|---|---|---|
| 1 | **C014 tested cells, not organs (CRITICAL).** Its statement said "≥ 3 organs" but the test counted organ×metric cells, and only 2 organs qualify. The cells included re-labelled home effects (vigil.reward ≈ kept), action-mix Brier artifacts, one effect counted three times (workshop utility/regret/success) and interactions on metrics pinned by a lesion. No multiplicity control. | atlas recomputed on dev and held-out seeds | C014 **retired**. Atlas rebuilt: curated `atlas_metrics`, same-stream calibration, pinned pairs skipped, **Holm** family-wise correction, organs counted distinctly. Successor **C016**. |
| 2a | **Held-out seeds can be chosen before sealing (IMPORTANT).** A contributor can compute candidate commit hashes offline (`git hash-object -t commit`) and commit only one whose seeds pass. | 5 seals predicted, 1 committed, prediction exact | **Documented limit.** Single-actor grinding cannot be prevented without external randomness. Docs no longer claim otherwise, AGENTS.md forbids it, and the frontier lists external randomness as an open item. |
| 2b | Renaming a claim file moved its seal (no `--follow`). | C006 renamed → new seal, doctor passed | **Fixed:** sealing searches by claim id across renames. |
| 2c | A squash or rebase merge reseals every claim (re-rolled seeds). | all 16 PREREGISTERED dropped in a squashed clone | **Fixed (detected):** the doctor rejects held-out records whose seal is not in history. Merge with merge commits. |
| 3 | **A failed confirmation could be overwritten or erased (IMPORTANT).** Re-running known held-out seeds after a code change gave PREREGISTERED. Editing a prediction under the same id hid its history. Deleting a record went unnoticed. | `assess_hide.py`, `pred_edit.py`, record deleted in a clone | **Fixed:** PREREGISTERED is decided only by the *first* recorded held-out evaluation, and a failure is noted permanently. Amended predictions are noted in STATUS, and the doctor rejects amendment after a held-out run. The doctor rejects deleted records. `--heldout` always records. |
| 4 | **Check logic outside the hash (IMPORTANT).** Helpers and constants in claim files (K01's configs, C015's `_live`, K05's seeds) could change with the prediction hash unchanged. | 3 edits, identical hashes | **Fixed:** prediction scheme 2 hashes the claim file's code minus prose. Scheme-1 hashes stay computable, so older records still match unchanged predictions. Records store their scheme. |
| 5 | **K02 never exercised exactly-once (IMPORTANT).** In-flight kills landed before the commit 18/18 times, and removing duplicate suppression still passed. | `k02_race.py`, `k02_broken.py` | K02's prose corrected. New **K07** kills after the durable commit of ticks and of episode ends. The worker's `replayed` flag is now *measured* (did the ledger grow?), and a test of the test breaks exactly-once in a sandbox and checks that the procedure catches it. |
| 6 | **K01 cannot see hash-order hazards (IMPORTANT).** In-process replay shares PYTHONHASHSEED. | a hazard organ passed K01 9/9 and diverged across seeds | K01's prose corrected. New **K06** replays every lesion config in fresh processes under 3 hash seeds. A test of the test injects a hazard organ and checks K06's procedure fails. |
| 7 | **Brier compared on different events (IMPORTANT).** Each agent was scored on its own action mix. C008's "tie" was an artifact, and on the same events the self-model is better even when silent. C007 survived, though 13–22% of its gap was action mix. C010 measured behaviour. | `brier_confound.py`, `brier_heldout.py` | Runner adds a shadow success-table forecaster scored on the agent's own events (`brier_table`, `calib_gain`). **K08** checks the metric is exactly 0 for the table itself. C007, C008, C010 **retired**; successors **C017** and **C018** (C008's reading reversed). |
| 8 | The rival BEATEN label ignored which side won (latent). | stub-lab repro | **Fixed:** BEATEN only if arm `a` is reliably better. Regression test added. |
| m1 | The percentile bootstrap under-covered at n = 16 (92.7% normal, 88.7% skewed). | 800 simulations | **Fixed:** the interval is now the wider of the percentile-bootstrap and Student-t intervals (measured 95.3% normal, 91.3% skewed). The remaining under-coverage on skewed data is documented. |
| m2 | Workshop arms were not fully paired: probe censoring consumed the world RNG. | 48/300 episodes matched | **Fixed:** per-episode and per-probe world streams. A test enforces action-independence for every world. |
| m3 | `freeze:memory/goals` equals ablation (reset each episode). | identical traces | **Fixed:** frozen organs keep their episodic state too; docs explain that freezing from birth equals ablation and mid-life `@E:freeze:X` is the meaningful form. |
| m4 | `restore` did not verify the hash chain. | — | **Fixed:** `restore` calls `ledger.verify()`. Regression test added. |
| m5 | By-construction or mislabelled claims: C015 and K05 follow from K01; C011's title credited memory; K03 is narrower than its uses. | — | C015 and K05 **retired** without successor. C011's title and K03's scope corrected (prose only). |

## What the review confirmed as correct

There is no undeclared leakage of private world state to agents. Organism and transcript rivals are matched (learner,
defaults, RNG streams, TD and terminal updates, boundaries). The `compare`/`threshold` sign and margin logic, the
aggregation windows, the atlas sign normalisation and the C004 interaction formula are correct. Every replayed tick is
verified on action, broadcast and confidence. Held-out evidence outranks dev evidence. K04's world semantics match the
legacy dynamic program.

## Why this review is part of the knowledge

It is itself a contribution that built on everything before it, and the pipeline absorbed it the way it absorbs any
contribution:
* claims were retired with stated reasons, not deleted;
* successors were registered under new ids and sealed by a new commit;
* missing guarantees became new standing claims (K06, K07, K08) and tests;
* every claim was re-confirmed on held-out seeds after the fixes.

The first-held-out rule means the original held-out results still decide preregistration for unchanged predictions.
Their histories stay visible in STATUS.md.
