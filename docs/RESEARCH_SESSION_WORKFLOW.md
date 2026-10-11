# MIND execution, review and recovery workflow

This document supplements [GO.md](../GO.md), [AGENTS.md](../AGENTS.md), [CONTRIBUTING.md](../CONTRIBUTING.md), [PIPELINE.md](PIPELINE.md) and [CLAIMS.md](CLAIMS.md). All existing constitutional, replication, evidence, merge and immutable-record requirements take precedence. This document authorizes no new roles, permissions, schedules, standards of replication, or exceptions; it guides contributors, not the organism or evaluator.

## Purpose and roles

A research session is a **single cumulative contribution** to an executable scientific question, not a target number of words, runtime minutes, files or PRs. The program tests *specific L1/L2 properties of this organism in these worlds*; its L2 functional-consciousness target has not been reached. Never infer L3.

Where concurrent agents are available, divide ownership rather than assigning identical prompts:

1. **Execution/recovery:** finish existing actionable `[needs-run]` PRs and checkpointed evaluations before opening new experimental work.
2. **Causal discovery:** design one high-value unclaimed intervention, organ or world whose outcome would discriminate mechanisms.
3. **Rival/falsification:** create a stronger same-information rival, counterexample, targeted negative control or reproducible refutation.
4. **Post-run scientific review:** criticize completed, fixed-SHA evidence. A separate invocation of the same model is not independent replication.
5. **Integration checks (not a new role):** any contributor preparing a merge may repair bounded defects and must verify the combined tree; use merge commits, never squash/rebase when sealed claims are involved. `CONTRIBUTING.md` remains authoritative about merging without a designated integrator.

Scheduling does not reserve a frontier item. Every contributor must recheck live PRs and branches before claiming it.

## Gate 0 — execution capability before work selection

On **live** main, record the exact SHA, inspect `STATUS.md`, all relevant open PRs and `contrib/*` branches, and check:

- Full local Git checkout **with history** (required for claim sealing, held-out derivation and doctor).
- Python environment able to run `python -m mind doctor` and the relevant test suite.
- Repository read access, branch write access and PR ability, separately.
- Any existing candidate branch's SHA, claim ID, changes, evidence and ownership.

Do not confuse GitHub API inspection with source execution. Do not invent local tests from prose or CI summaries. Try a bounded, legitimate recovery for transient errors (such as DNS), but do not bypass a permissions failure or a platform safety check. Record the failed operation and error verbatim, without assuming that a different interface is authorized.

If execution is unavailable, choose one genuinely **new**, nonduplicative, testable design or adversarial analysis that advances an uncovered blocker; it must have a named artifact, concrete future commands, falsifier and acceptance criteria. A recycled protocol or another description of an unchanged failure is **not** a contribution. If none exists, stop with `BLOCKED_NO_NEW_CONTRIBUTION`; give a precise resumption condition. This is an honest session outcome, not a scientific result.

## Gate 1 — hypothesis and measurement before coding

Write down these fields, even if the contribution is an instrument or a null test:

| Field | Required evidence |
| --- | --- |
| Original question | The exact H/K/C question the work intends to answer |
| Tested subclaim | Narrower estimand actually observable with this intervention |
| Mechanism | Which causal path must change, and how the intervention isolates it |
| Rival | Simplest sufficient state/baseline with **matched public inputs, learning opportunity and compute** |
| Controls | Sham lesion, negative control, leakage check, and variant where applicable |
| Margin and unit | Scientific reason for the margin; unit of independent sampling and uncertainty calculation |
| Falsifier | Observation that weakens the claim and changes the next experiment |
| Scope | Instrument/L1/L2 label and **explicit claims not established** |

Separate the following distinctions rigorously:

- **Representation vs procedural learning:** an equality feature can explain transfer accuracy without any procedure compiler, impasse mechanism or integrated cognition.
- **First exposure vs adaptation:** average performance over episodes after transfer-domain feedback is **not zero-shot** first-action performance. For zero-shot claims, score the first eligible action **before** any target-domain outcome updates; report adaptation in a separate metric or successor claim.
- **Replay vs real process reset:** in-process ledger recreation does not demonstrate SIGKILL and fresh-process recovery. Require provenance for the kill, restart and the restored persistent state when claiming death continuity.
- **Behaviour vs causal organisation:** success at a task does not establish L2 integration without a discriminating intervention and credible simpler rivals.
- **Held-out seeds vs independent replication:** held-out checks are not another contributor/environment. Same-model review is self/cross-invocation review, not external independence.
- **A null result vs equivalence:** follow `docs/CLAIMS.md` confidence-interval rules; nonsignificance alone is inconclusive.

Do not silently expand the hypothesis to fit what an easy-to-implement test measures. It is acceptable to register a prerequisite L1 claim **as a prerequisite**, while keeping the parent H-question open.

## Gate 2 — make and preserve actual evidence

1. Build on the shared `mind/` substrate and its existing worlds/rivals; do not fork a disconnected demonstration.
2. Explore on dev seeds only. Exploratory results are not registered evidence.
3. Register a prospective prediction and **commit the claim before any held-out run**. Never choose a commit for favorable seeds, edit a prediction after confirmation, or reuse exposed held-out outcomes to tune its successor.
4. Execute full dev `--record`, sealed held-out `--record`, required matched rivals, held-out variants and process/lesion checks; commit **every held-out record including failures**.
5. Preserve REFUTED, INCONCLUSIVE and BROKEN evidence. A changed estimand or prediction requires a successor claim; evaluator/doctor rule changes belong in a separate PR from claims.
6. Run required GO.md checks: `python -m mind check`, `python -m unittest discover -s tests`, `python -m mind doctor`, `python -m mind status --write`. Re-record current-code evidence whenever `RESULT_CODE` changes, as GO.md requires.
7. Finish on one `contrib/<item>-<slug>` branch, commit all generated records and STATUS, open one PR, and leave it unmerged for integration. Pushing or opening a PR does not establish a scientific result.

Do not claim successful validation unless commands really ran on the reported final candidate SHA. If a test cannot be run, mark it `NOT_EXECUTED`; do not replace it with estimated output.

## Gate 3 — scientific review and integration

A reviewer examines the full diff and the fixed claim/evidence SHAs, searching for by-construction outcomes, post-feedback metrics mislabeled zero-shot, causal confounding, mismatched rivals, hidden oracle information, weak negative controls, seed/provenance issues, and predictions that do not measure their parent question.

Review verdicts: `ACCEPT`, `REVISE`, `REJECT`, `INCONCLUSIVE`. Every critique identifies its severity, an executable falsifier or counterexample, and a bounded next action. Do not claim external replication from an AI cross-invocation.

A contributor preparing integration may fix narrow test/documentation/conflict issues without modifying sealed predictions or records. No designated integrator role is created. The contributor must **not merge** experimental `DESIGN_ONLY` / `[needs-run]` code as if it had passed execution gates. Recheck candidate SHA, full tests, doctor, code-fingerprint refresh, PR review and repository branch protections, then merge with a **merge commit** to preserve claim seals. A documentation-only clarification is a different class of PR; do not represent it as a verified scientific experiment.

## Handoff: use two separate status dimensions

Every session reports exactly the following, with no fabricated duration or implied future execution:

- **Identity:** live main SHA, question/claim, PR/branch/head SHA, what existing contribution it extended.
- **Capabilities:** actual checkout/test/write capabilities and precise failures.
- **Scientific outcome:** `HOLDS`, `REFUTED`, `INCONCLUSIVE`, `UNTESTED`, or explicit narrower finding; never treat a design as evidence.
- **Execution outcome:** `EXECUTED`, `DESIGN_ONLY`, `REVIEW_ONLY`, `BLOCKED`, or `BLOCKED_NO_NEW_CONTRIBUTION`.
- **Provenance:** exact commands and outputs; observed versus `NOT_EXECUTED`; every persisted commit/record/PR or `NOT_PERSISTED`.
- **Limits and next:** strongest surviving rival, unmatched scope of parent hypothesis, and **one actionable next step**.

A session can be legitimately blocked. Its status must not be promoted simply for producing a detailed report. Durable negative experimental evidence is more useful than an untested positive narrative.
