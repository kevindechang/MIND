# Digital Mind — Scientific Publication Standard v1

**Status:** adopted research governance, NOT an external journal standard or a guarantee of research quality. The goal is cumulative scientific understanding, not padding reports.

## Publication taxonomy

| Artifact | Intended purpose | Maturity signal | Invalid substitute |
|---|---|---|---|
| [Research Atlas](atlas/README.md) | Program vision, priorities, measurable dependencies | Traceability and explicit architecture alternatives | Grand philosophical prose with no tests |
| [Living dossiers](dossiers/README.md) | Deep targeted interdisciplinary synthesis | Distinct sections with primary-source provenance, theory contrast, novel argument and evidence limitations | Repeated summaries of the same 3 papers |
| [Experiment records](experiments/E001/README.md) | Preregistered plan separated from real observations | Locked stage 1, reproducible code/logs/results stage 2 | Simulator unit tests advertised as LLM performance |
| [Cross-stream synthesis](syntheses/README.md) | Decide which hypotheses/architectures survive and why | Contradiction, falsification, null, uncertainty and new decisions | Unchallenged consensus/vague recap |
| [Hourly runs](runs/) | Transaction log and handoff | Exact source/commands/commit and next blocker | Standalone 500-word 'research paper' |

## Dossier depth gate

A dossier must identify: (i) exact question and operational constructs, (ii) why the question matters for the digital entity, (iii) literature search methods *actually performed*, accessible corpus and blind spots, (iv) a primary-source evidence matrix that says whether abstract, methods or raw data was examined, (v) strongest contrary perspectives from **more than one discipline when relevant**, (vi) formal competing mechanisms and what data discriminate them, (vii) causal identification, samples/uncertainty and incentives to falsify, (viii) precise experiment links and result provenance, (ix) architecture and E900 consequences, (x) unresolved alternatives and revision log.

A draft without these is **SEED**, not a comprehensive scientific monograph. A substantial manuscript will often contain thousands of words, but length alone is never enough. Do not manufacture discoveries or make source count targets merely for optics. If an iteration only obtains one high-value falsification, a precise 500-word update and supporting code may be scientifically superior to padding.

## Review method transparency

A *targeted narrative review* may focus selectively but must say how sources were selected and what is missing. A *scoping review* or *systematic review* needs an actual documented database/repository search, search strings and dates, eligibility criteria, screening/exclusions/counts, transparent appraisal, and appropriate guideline reporting; cite [PRISMA-ScR](https://www.prisma-statement.org/scoping) or [PRISMA 2020](https://www.prisma-statement.org/prisma-2020) only when their methods/reporting are substantively satisfied. A *living systematic review* additionally needs a prospectively specified surveillance/update policy (see [Cochrane Ch22](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-22)). Never equate a GitHub page marked 'living' with Cochrane review status.

## Experimental rigor

Every scored experiment needs G2 registration BEFORE results, explicit outcome oracle, population and sample/power/precision, seed/held-out splits, baseline and ablation, resource parity, exclusion and stopping rules, statistical analysis and reproducible source artifact. Stage 2 holds results and transparent deviations. An *internal preregistration* borrows prospective discipline from [Registered Reports](https://www.cos.io/initiatives/registered-reports), but receives none of their formal peer review status.

## Claim/review gate

- Ground evidence as OBSERVED/PAPER-REPORTED/THEORETICAL/PROPOSED/SPECULATIVE/UNKNOWN, with grades E0–E3 used as defined in [protocol.md](protocol.md).
- Label reviewer `INDEPENDENT_SUBAGENT_VERIFIED` only when an actual independent invocation/review artifact is verified. Otherwise `SELF-REVIEW_ONLY`.
- If source method unread, mark ABS­TRACT_ONLY and do not generalize performance claims.
- Never advance H, A, G, E900, L1/L2/L3 based on a governance commit or persuasive writing.
- Every conclusion must state its strongest simpler alternative and a possible falsifier.

## Compounding publication transaction

Follow [research-cycle](research-cycle.md) and [research-records](research-records.md). Read live state, Atlas, active decision/dependencies and applicable asset versions. If substantive, update the dossier/method/result with bounded claims, source depth, contrary evidence and versions. Append a unique typed work record and index it; update decisions/assets where justified. Commit artifacts before state, which is written LAST and cites the artifact commit. Verify final publication. Interrupted transactions resume once from committed IDs; no rerun/double count. Missing writes means NOT_COMMITTED with full handoff.

Every result records an outcome-to-action decision delta and proposed E900 causal coupling/intervention. Invalid pivotal evidence flags direct/transitive dependent decisions and affected assets NEEDS_REASSESSMENT, not automatic rejection. No promotion may rely on unresolved stale pivotal premises. Reuse requires applicability checks and revalidation if assumptions changed.

## Attention and deep synthesis

Use substantive work records for allocation; pure governance, superficial repeats and SKIPs do not count. Reserve a non-leading-stream opportunity in every four new completed substantive records with documented exceptions. Scientific acceptance is distinct: count new distinct contributions only with SCIENTIFIC_ACCEPTED, verified persistence and intact evidence. Legacy 001–003 acceptance is UNKNOWN; 004 remains MAJOR_REVISION_REQUIRED. No inferred backfill.

Deep synthesis follows eight new distinct valid accepted contributions, or major validated findings/pivotal invalidation. Use milestone IDs to avoid retriggering after amendments or reassessment. Review scope includes W1–W4 missing/contrary evidence and E900 implications, and may conclude no architecture change. Word, paper or minute counts do not certify substance.

## Tool-neutral operation and scientific acceptance

No named skill/plugin is mandatory. Verify capabilities needed for the chosen work. Optional-tool absence does not certify a scientific failure or force a program-wide skip. Separate reviewer absent means SELF-REVIEW_ONLY; execution absent means NOT_EXECUTED/BLOCKED_ON_EXECUTION. All completion/acceptance claims still require actual evidence.

Apply [research-quality-gate](research-quality-gate.md). Stored instruments and successful tests are not accepted mechanism studies. Kind and verdict are separate; valid incomplete work may be indexed as a checkpoint without promoting G gates or hypotheses. [004 audit](reviews/2026-10-10-iteration-004-scientific-rigor-audit.md) remains MAJOR_REVISION_REQUIRED. A rigorous null, negative result, formal argument or critical synthesis may qualify; nonsignificance is not equivalence. Preserve historical predictions, deviations and review provenance.
