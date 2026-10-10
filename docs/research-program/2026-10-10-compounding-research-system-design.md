# Compounding research toward functional consciousness

Date: 2026-10-10.
Status: APPROVED FOR IMPLEMENTATION by sponsor instruction “just implement and finish”; adopted governance becomes canonical on main publication.
Artifact kind: GOVERNANCE_DESIGN. This document is not a scientific finding, protocol registration or architecture adoption.

## 1. Intended outcome

The sponsor wants Digital Mind to become a compounding research system aimed primarily at building functional consciousness. The existing [north star](../../north-star.md) defines the enduring, developing digital entity; this refinement makes the route toward that target cumulative and decision-driven.

For this program, **functional consciousness is an operational research target within L2**: persistent experience-dependent state, predictive self/world modeling, calibrated metacognition, selective information availability across cognitive functions, adaptive agency and learning that demonstrably interact and affect action. This working definition is not a consensus scientific definition, a required biological imitation, or a claim about phenomenal experience. Each capacity must receive its own test and rival; passing a collection of tests does not automatically establish integration.

L1 remains interaction behavior. L2 remains causal cognitive organization. L3 remains unresolved phenomenal experience. Do not introduce a single consciousness score or reinterpret an existing functional result as evidence of L3.

Success for the pipeline means that later work demonstrably reuses validated instruments, incorporates contrary evidence, resolves decisions, and improves or simplifies candidate systems. No fixed completion date or guarantee of consciousness is credible.

## 2. Observed starting point

Repository inspection supports these governance observations:

- [E001 registration](../../experiments/E001/preregistration.md) is draft, G0 open; resource budgets, oracle, uncertainty analysis and scored evaluation are unfrozen.
- [The traceability matrix](../../atlas/traceability-matrix.md) links goals to hypotheses and proposed tests, but lacks explicit downstream decision and invalidation links.
- [Iteration 004's audit](../../reviews/2026-10-10-iteration-004-scientific-rigor-audit.md) assigns MAJOR_REVISION_REQUIRED. [State](../../research-state.md) acknowledges this but also contains older advancement and allocation language.
- [The research cycle](../../research-cycle.md) retains permissive skill-unavailability text followed by a mandatory fail-closed override. Readers must currently resolve policy history themselves.
- Instruments exist and prior records report local deterministic tests. This design has not rerun those tests or verified agent efficacy. No scored AI-agent trial is reported in the inspected canonical records.

These observations concern the repository's records, not independent scientific validation of their claims.

## 3. Selected approach and alternatives

**Selected: strengthen the existing GitHub documents and ChatGPT execution loop.** Add a small decision/dependency register and a reusable-asset index; revise existing protocols and templates rather than creating a second research operating system. GitHub Markdown remains inspectable durable memory.

Alternative: expand publications alone. Low implementation cost, but more dossiers do not resolve selection, invalidation or experimental readiness.

Alternative: build an autonomous runner or database-backed knowledge graph. Better automation potential, but introduces cost, execution and maintenance before the first scored comparison. Outside this refinement's authorized scope.

Preserve the newer tool-neutral main policy (commits 89000f8 and 6879977), no paid APIs/background workers, truthful execution provenance and current approval boundaries. No named framework is mandatory; relevant capabilities are verified independently. This governance spec changes no scheduled task, production Anjo code or research gate.

## 4. Canonical research loop

**Restore → select decision → discriminate rivals → research/test → review → decide → persist reusable delta → hand off.**

1. Restore the latest canonical main commit, state, active blocker and authoritative records; verify task-relevant capabilities. Check dependency freshness before treating a conclusion as a premise.
2. Select one decision whose prerequisites and tools are available. State what each plausible outcome would change. An unresolved blocker is not automatically the best executable task.
3. Specify competing predictions, observations, intervention, measurement and decisive falsifier. A weaker baseline may calibrate an instrument but cannot carry a superiority claim.
4. Inspect primary methods or execute authorized work. Separate instrument construction, exploratory pilots and frozen scored trials. Preserve null findings and impossibility/identifiability arguments.
5. Apply the existing scientific quality gate. Record actual reviewer independence; SELF-REVIEW_ONLY remains valid disclosure, not external certification.
6. Choose ACCEPT, REVISE, REJECT or DEFER for a bounded claim/decision. Record scope, costs, alternatives and unresolved conditions. A null result is not automatically equivalence or rejection.
7. Update claim/evidence links, dependent decisions and reusable assets only where justified. Append the appropriate artifact; update state last and verify persistence.
8. Hand off one executable action with its inputs, required tools, expected artifact and stopping condition. If execution is unavailable, name that dependency rather than scheduling the same impossible action repeatedly.

## 5. Decisions and dependency memory

Add `decision-register.md`, a Markdown index plus bounded records. IDs are stable D001, D002, etc.; existing H, E and source IDs retain their meanings.

Each decision record contains:

- question, workstream and candidate architectural choice;
- linked hypothesis/claim, strongest viable rival and bounded claim scope;
- prerequisite decision IDs and claim/evidence links;
- outcome-to-action mapping, including negative, null and invalid results;
- current ACCEPT/REVISE/REJECT/DEFER status and rationale;
- evidence references with artifact paths and exact versions/commits;
- whether evidence supports, contradicts or merely informs the decision;
- confidence with reasoning, review provenance and limitations;
- affected downstream decisions, architecture and E900 observable/intervention;
- freshness CURRENT, NEEDS_REASSESSMENT or SUPERSEDED;
- next disconfirming test and revision history.

Use claim anchors within existing hypotheses and dossiers rather than duplicating their scientific prose. Do not assign unsupported numeric belief probabilities or count papers as independent evidence. Multiple papers using the same dataset or research lineage must disclose that dependence.

When pivotal evidence is corrected, invalidated or superseded, mark direct and transitive dependent decisions NEEDS_REASSESSMENT. This flag means their justification needs review; it does not assert their conclusions are false. Block new promotions that rely on an unresolved pivotal dependency. A reviewer may restore CURRENT with explicit alternate justification. Preserve historical records and amendments.

Initialize D001 for E001 representation choice. Other decisions enter only with a concrete question and dependency; do not invent a comprehensive graph for its own sake.

## 6. Reusable assets and research transfer

Add `asset-register.md` with links to existing instruments, protocols, datasets/seed generators, evidence-method extractions and reproducible analyses. This is an index, not a parallel source of scientific truth.

Each entry records owner question, path/version, admissible purpose, inputs/outputs, observed verification command/log, dependencies and limitations. Maturity is PROPOSED, LOCALLY_CHECKED, COMPARATIVELY_EVALUATED or INDEPENDENTLY_REPRODUCED. Only actual supporting records permit promotion. Unverified historic verification reports are labeled as such until reproduced.

Reuse must identify which prior asset it uses, whether its assumptions hold and whether any changes require revalidation. Unit-tested calibration instruments remain useful assets without being evidence of an agent mechanism. Do not require every valid research result to yield code; source-method extraction or an identifiability argument may be reusable.

## 7. Progress accounting and consistent state

Keep the legacy `latest_verified_iteration: 004` as a historical persistence identifier, not an accepted-science count. Do not rewrite runs 000–004 or infer scientific acceptance for 001–003 from their commit status.

Add an artifact index `research-records.md` containing ID, kind, source commit, related decision, scientific verdict, evidence depth and review provenance. Allowed kinds: GOVERNANCE_CHANGE, EXPLORATORY_CHECKPOINT, RESEARCH_NOTE, INSTRUMENT_VALIDATION, AGENT_COMPARISON and SYNTHESIS. Kind describes work; the existing scientific quality verdict separately describes acceptance.

Existing IDs remain. Future records use unique dated IDs with collision checks, so repeated checkpoints do not masquerade as the next accepted scientific iteration. A single decision may span many checkpoints. Count accepted contributions only from explicit SCIENTIFIC_ACCEPTED verdicts with verified persistence and intact pivotal evidence. If historical acceptance is unknown, report UNKNOWN; initialize prospective counting from adoption rather than inventing a backfill.

`research-state.md` becomes a short handoff with:

- legacy persistence identifier and latest record link;
- latest scientific acceptance record, or NONE_VERIFIED;
- prospective accepted-contribution count and counting start;
- gate, active decision/blocker, execution readiness and required capability;
- latest quality verdict, stale dependencies and reassessment queue;
- architecture/claim-ladder status;
- exactly one next executable step and linked record index;
- pending publication transaction, if any.

Move lengthy historical summaries into existing linked records rather than deleting evidence. Align the older iteration-004 advancement wording with its current audited verdict. An exploratory W2 checkpoint records attention spent, but does not certify an accepted W2 scientific contribution.

Allocation and synthesis serve different purposes. Retain one non-leading-stream opportunity in every four completed substantive work records, with documented exceptions; governance and skipped invocations do not count. This prevents difficult work from disappearing when acceptance is rare. Trigger deep synthesis after every eight prospectively accepted contributions or earlier after a major validated finding or dependency invalidation. Do not manufacture a due synthesis by treating legacy persisted artifacts as accepted science.

## 8. Selection and stop-or-pivot rule

Choose among ready decisions using qualitative expected decision impact, uncertainty reduction, cost, feasibility and integration relevance. Record the rationale; no arbitrary numeric priority formula is required.

After three substantive attempts on the same blocker without a gate change, resolved uncertainty or changed decision, the next attempt must begin with a reassessment. This threshold is a proposed operational trigger, not a scientific result or an automatic rejection rule. Choose a smaller discriminating test, acquire a missing capability within approved boundaries, switch to a ready dependency, retire an invalid benchmark, or explicitly justify continued effort with a new expected information gain.

Preserve partial progress with its gap list. New wording, references, templates or repeated toy checks alone cannot reset the attempt history. Necessary instrument work is allowed; state exactly which validity requirement it closes.

## 9. First decision: E001 causal autobiographical representation

D001 asks: under specified partial observation and equal available resources, does structured causal autobiographical memory improve action regret, repair or efficiency over strong transcript/retrieval and feasible compact belief/predictive-state competitors?

Next executable scientific step remains an observation-history-valid partial-observation instrument specification. Its oracle must use only permitted information and an explicitly chosen prior/robust criterion, including genuinely unidentifiable histories. Private simulator truth is available for instrument diagnostics, never silently as the agent scoring oracle.

Development pilots must be separated from held-out scoring. Before G2, freeze model/decoding, observations, total lifecycle memory-construction/retrieval/inference cost, arms, paired worlds, mechanism-family splits, estimand, practical effect threshold, sample/precision rationale, uncertainty estimator, exclusions, multiplicity and stop rules. If real model execution is unavailable, record BLOCKED_ON_EXECUTION and continue only ready design work; no API procurement is implied.

Prospective decision mapping:

| Result, interpreted using the frozen analysis | Consequence |
|---|---|
| Advantage over strong rivals plus mechanism-sensitive ablation and valid held-out comparison | Support scoped utility of the representation; propose replication and an E900 integration test |
| Strong simpler rival matches within a preregistered equivalence/noninferiority margin or outperforms at fair resources | Prefer simpler representation for that tested scope; weaken necessity, retain open transfer questions |
| Imprecise null or mixed result | INCONCLUSIVE; inspect precision and failure strata without declaring equivalence |
| Leakage, invalid oracle or confounded resource comparison | Invalidate affected comparison; repair instrument/protocol and flag dependents |
| Benefit vanishes under fair controls | Reject the asserted advantage for the tested scope; preserve useful assets and negative evidence |

This design does not freeze numerical thresholds, execute E001 or promote G0. D001 may conclude that a richer memory graph is unnecessary; the program's target is functional organization, not loyalty to that mechanism.

## 10. Integration path

Every mechanism decision names an E900 observable, cross-function causal prediction and intervention. Integration requires evidence that state in one function changes behavior in another under matched alternatives; independently successful modules are insufficient.

Sequence: a valid E001 comparison → scoped representation decision → approved minimal integrated candidate and strong simple persistent baseline → E900 P0 feasibility → separately approved/frozen P1 prospective sessions → only then consideration of P2. Independent self-model, learning and theory work may advance in parallel in scope when their dependencies are ready; E001 need not freeze all inquiry.

Minimal candidate selection follows evidence and may use compact state rather than graphs. It must expose persistent state, self/world predictions, goals, actions and learning changes to controlled intervention. Production deployment, continuous execution and 90-calendar-day trials remain separate approvals. No runner or system is implemented by this spec.

## 11. Persistence and failure handling

Publish governance changes on a reviewable branch, with canonical adoption occurring only after review/merge. Scientific runs continue to read main until adoption. Preserve a main-head snapshot; reconcile ordinary conflicts without force pushes or overwriting concurrent research.

For scientific transactions, commit substantive artifacts and records first, then state last. State references the immutable artifact commit. A final commit cannot contain its own hash: record the final read-back SHA externally or in a later audit. If interruption occurs between commits, restore by comparing indexed artifacts with state and finalize the handoff; do not rerun or double-count the same experiment.

Missing optional skills does not block feasible research. Missing indispensable task inputs blocks that task until resolved; choose ready independent work or an honest checkpoint. Missing execution: NOT_EXECUTED or BLOCKED_ON_EXECUTION. Missing independent reviewer: SELF-REVIEW_ONLY. Missing GitHub writes: NOT_COMMITTED with self-contained delta. Invalid evidence: quarantine affected interpretations, preserve logs and reassess dependents. A paused or unavailable scheduler is not continuous cognition.

## 12. Implementation scope after specification approval

| Files | Change |
|---|---|
| `README.md`, `AGENTS.md`, `protocol.md`, `research-cycle.md` | One consistent current workflow and tool-neutral capability policy; link new registers |
| `decision-register.md`, `asset-register.md`, `research-records.md` (new) | Minimal decision dependencies, reusable assets and separate work/acceptance accounting |
| `research-state.md` | Compact handoff, truthful historical status and explicit readiness; write last |
| `hypotheses.md`, `atlas/traceability-matrix.md` | Decision, rival, intervention and downstream integration links without hypothesis promotion |
| `workstreams.md`, `atlas/research-roadmap.md`, `publication-standard.md`, `research-quality-gate.md`, `review-protocol.md` | Align selection, counting, invalidation, synthesis and review semantics |
| Existing iteration template and related template/overview references | Add decision delta, reusable asset, dependency freshness, readiness and one next action; remove conflicting current instructions |

All paths in this table are relative to `digital-mind/`. Preserve upstream deletion/rename of obsolete framework-specific files; mark retained historical publication designs where their counter instructions conflict. Scope excludes instrument changes, scored research, new scientific sources, scheduled-task edits, paid resources and architecture adoption. The implementation plan must identify all affected references before editing.

## 13. Acceptance and verification

The implementation is acceptable when document inspection and link/status checks demonstrate:

1. Functional target is operationalized with rival/intervention links and no L3 inference.
2. D001 has complete dependency and outcome-to-action fields; no invented results or budgets.
3. A hypothetical invalidated evidence item can be traced to direct/transitive dependent decisions and NEEDS_REASSESSMENT without erasing history. Demonstrate this as a labeled governance walkthrough, not a research finding.
4. Reusable assets distinguish reported checks, observed local verification and actual comparative/independent evidence.
5. Iteration 004 remains historically persisted and MAJOR_REVISION_REQUIRED everywhere current status is stated; 001–003 are not silently accepted.
6. A checkpoint can preserve progress without advancing a scientific gate; accepted contributions and allocation records use distinct rules.
7. Repeated unchanged blockers trigger reassessment; unavailable execution yields a feasible handoff or explicit block.
8. Current operative files agree on tool-neutral research, verified task capabilities, review provenance, state-last persistence and no external paid executor.
9. Relative links resolve, IDs are unique, all status changes are justified, and the Git diff touches only intended Digital Mind files.
10. Publication commit and read-back are verified; governance introduces no science iteration, architecture promotion or scheduler claim.

This document's review is SELF-REVIEW_ONLY. Its scientific premises are taken from the repository's existing records; no literature search, new experiment or independent referee review was performed for this governance design.

## Concurrency amendment — tool-neutral main policy

During publication, live main advanced to `6879977355c89eb91e96e4ef11b5e9fe5c6e03c4`, explicitly retiring the older required-skills gate and deleting/renaming framework-specific documents. This implementation preserves that newer policy instead of restoring the earlier prerequisite. Prior descriptions of the old mandatory-skills state in section 2 are historical observations; this amendment and the revised operative rules govern future runs. The design/plan live under `docs/research-program/`; the iteration template is `templates/research-iteration.md`. No scored experiment, scientific acceptance or scheduler edit accompanies reconciliation.
