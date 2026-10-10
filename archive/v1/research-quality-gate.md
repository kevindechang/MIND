# Digital Mind — Scientific Rigor Admission Gate v2

**Applies to all future scheduled and manual research cycles.** Scientific quality is determined by evidence and methods, not a named skill framework. [Iteration 004 referee review](reviews/2026-10-10-iteration-004-scientific-rigor-audit.md) motivated this rule after a short toy-instrument exercise was presented as substantial research.

## Two independent things must be verified

**A. Persistence validation:** files exist, commits were successful, tests/commands reported truthfully, state is consistent. This is what the legacy `latest_verified_iteration` counter principally attests; not peer review or causal proof.

**B. Scientific acceptance:** a discriminative contribution survives the rubric below. A run can satisfy A while failing B. Record `scientific_quality: EXPLORATORY_CHECKPOINT | RESEARCH_NOTE | SCIENTIFIC_ACCEPTED | MAJOR_REVISION_REQUIRED`. Never describe a checkpoint as a peer-reviewed paper or a comprehensive research outcome.

## Required research-grade submission packet

Before an hourly run is promoted to `SCIENTIFIC_ACCEPTED`, it must satisfy **all** the following within its own linked artifacts (a dossier, method, executable experiment, formal proof, or review):

1. **Question/construct:** target operationalized with controlled versus contested claims, and explanation of why this result would change a named hypothesis or architectural choice.
2. **Strongest competitor:** one genuinely competitive simpler mechanism with matched permissible observations/resources, plus a distinct predicted result; not an intentionally weak fixed timer or no-memory foil.
3. **Source-level method extraction when invoking literature:** for every major paper on which the claim rests, record research design/data or theorem assumptions, what was *actually inspected* (abstract/full-methods/results), baseline, reported result, limitation, transfer caveat and contrary evidence. Abstract-only references can generate leads but cannot carry a full-depth empirical conclusion.
4. **Formal causal/test validity:** explicit quantities being estimated/compared, assumptions, identifiability argument, potential confounds, falsifier and negative-control/ablation logic. A conditional equality obtained by assuming identical algorithms must be labeled elementary equivalence, not a discovered mechanism.
5. **Substantive contribution:** at least one of (i) a nontrivial, assumption-explicit theoretical result challenged against counterexamples; (ii) a critical multi-source synthesis that changes a concrete experimental/architectural decision through real methods analysis; (iii) a preregistered, instrumented comparative empirical finding with uncertainty, full command/source provenance. Documentation reshuffling, test scaffolds and examples that work by construction do **not** alone qualify.
6. **Independent validity discipline:** disclose independent reviewer dispatch if real; otherwise SELF-REVIEW_ONLY; provide strongest reason conclusion could fail and reproducible next disconfirming test. Critic must assess the claim, not merely correct Markdown formatting.
7. **Claims and provenance:** separate observations/paper reports/theory/proposals; distinguish real agent experiments from deterministic simulator and code unit tests; distinguish L1/L2 from unresolved L3 and staged E900.

This is a **substance-based threshold**, not a numeric paper/word/time quota. A one-page valid proof or well-controlled negative experimental result can pass; a ten-thousand-word superficial essay must fail.

## Fail-closed publication decision

- **Rigorous packet complete:** `SCIENTIFIC_ACCEPTED` only after accurate substantive evidence, review and persistence; commit dossiers/results and a typed indexed work record, then update state last; count the distinct contribution only after verified persistence and intact pivotal evidence.
- **Rigorous packet incomplete:** `MAJOR_REVISION_REQUIRED` or `EXPLORATORY_CHECKPOINT`. Preserve genuine partial progress with explicitly dated versioned notes or proposals; **do not promote it as a completed high-rigor scientific research iteration**, do not advance G gates, hypotheses or architecture, and state which checks are missing. A checkpoint may be committed but needs its own artifact kind; do not mislabel it as a journal-ready review.
- **Experimental execution impossible:** write a rigorous hypothesis/protocol or literature synthesis with appropriate statuses; never imply a scored trial was run.

## Operational output

The next task must return a short status table: `available research tools | source depth | decisive rival | real execution | falsifier | independent review | publication verdict | persistence SHA | next work`. A brief run log is acceptable **only if** substantive scientific content exists in the linked dossier, analytic review or experimental record. Rigor is assessed on that content, not on the run log's length.

## Retrospective ruling

Iteration 004 remains a **verified stored research artifact** in `runs/`, but its scientific publication verdict is `MAJOR_REVISION_REQUIRED` (see [referee report](reviews/2026-10-10-iteration-004-scientific-rigor-audit.md)). This does not invalidate the 10 unit tests nor require destructive rewriting of the historical record. The subsequent critical reassessment is governance/methodology review, **not another accepted scientific experiment**.

## Compounding acceptance checks

Use [decision-register](decision-register.md), [assets](asset-register.md) and [work index](research-records.md). The packet names the decision and outcome-to-action map, exact reused assets/assumptions, pivotal evidence and dependent claims, and an E900 observable/cross-function intervention. Invalid evidence triggers transitive NEEDS_REASSESSMENT; unresolved pivotal stale dependencies block promotion. CURRENT is freshness, not proof.

Kind is independent of verdict. A persisted checkpoint counts only for eligible substantive attention, never automatically for accepted science or gate advancement. Count a distinct SCIENTIFIC_ACCEPTED contribution once, with immutable provenance; amendments don't create another. Legacy 001–003 acceptance UNKNOWN, 004 MAJOR_REVISION_REQUIRED. A nonsignificant or underpowered result cannot establish equivalence: apply frozen estimand, uncertainty and practical margin. Null/negative/critical findings can qualify on their own validity. Governance implementation contributes zero accepted science.
