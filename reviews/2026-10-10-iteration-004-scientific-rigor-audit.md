# Scientific referee report: iteration 004 / W2 endogenous maintenance

**Review date:** 2026-10-10. **Review type:** retrospective internal scientific audit, **SELF-REVIEW_ONLY**, not an independent peer review, not a new numbered scientific iteration. **Object:** [004 operational log](../runs/2026-10-10-iteration-004.md), [W2 dossier](../dossiers/W2-endogenous-maintenance/synthesis.md), [E002a v0.1 instrument](../experiments/E002a-G0-maintenance-selection-v0.1.md). **Verdict:** scientifically *preliminary/incomplete*; do not claim a rigorous study of endogenous cognition or a completed high-depth interdisciplinary synthesis.

## Referee summary

004 is accurately labeled as a short operational log (about 500 words), and the associated W2 living dossier is longer (about 2,000 words), but neither provides a rigorous answer to the ambitious question of endogenously maintained cognition. It is useful as a calibration and non-identification warning. Superpowers skill reads and a passing Python unit suite are verifiable engineering/procedural facts; neither is a proxy for source-depth, a representative research design, or scientific validation.

**Major revision required.** Keep the original run and simulator findings as historical records; do not delete, retroactively relabel tests, fabricate stronger findings, or advance H005/H008. The research record can be VERIFIED AS PERSISTED while simultaneously failing a separate SCIENTIFIC PUBLICATION ACCEPTANCE gate.

## Major concerns

### C1 — central claim is conditional by construction

The dossier argues that an adaptive external scheduler can reproduce an 'internal' maintenance controller if both have identical histories, state, policy and compute opportunities. Let h_t be the observable history and m_t the state. If C and S implement the same transition map F, with the same input sequence and m_0, then by induction m_t^C=m_t^S and a_t^C=a_t^S. This is mathematically sound, but **its equality follows directly from the stipulated same transition map and information**; it is not evidence that the proposed endogenous alternative is in general reducible or inferior. It reveals that the proposed observable is insufficient to establish implementation source under the assumed model class.

The document does not present a nontrivial theorem covering asynchronous, delayed, partially observed, interruptible systems with different event opportunities. Stronger claims must explicitly specify timing, observation sigma-algebras, intervention access and resource models. Adding an internal telemetry trace may resolve a particular implementation question but does not automatically resolve whether the computation is subjectively experienced.

### C2 — experiment and estimand misaligned

A one-slot scheduler choosing between hand-authored gain/deadline numbers cannot test ongoing deliberation, internally learned control policies, actual model improvement, cross-interaction self-continuity or a latent drive. The deterministic unit tests establish that Python selects according to supplied numbers. The favorable value-policy example is engineered: policy scores directly reuse estimated gains; better behavior than a fixed-index rule is predictable. An adverse misspecification case is useful *instrument sensitivity*, but not empirical agent outcome.

No independent random world sample with held-out transitions, confidence intervals, model budget accounting, history-equivalence checks, agent process restarts, or human observation exists. Therefore the experiment cannot estimate H008's claim.

### C3 — important rival mechanism omitted from depth of source review

The 1991 Russell/Wefald, 2012 Hay et al. and 1991 Sutton references were mainly publisher abstracts, and the previous dossier offered no critical extracted methods and numerical comparison. An important primary full-text source, **Lieder, Shenhav, Musslick & Griffiths (2018), 'Rational metareasoning and the plasticity of cognitive control,' PLOS Computational Biology 14:e1006043**, directly concerns *learning the policy for selecting computations/control*, not simply fixed one-slot VOC. It represents a more pertinent rival to vague 'endogenous' initiative.

In the inspected full-text Models and Results/Discussion sections (publisher HTML, main article), Lieder et al. describe a learned value-of-control approach with feature-conditioned value prediction, probabilistic control selection and model comparisons against an associative Rescorla–Wagner learner and a win-stay/lose-shift learner, applied to previously published empirical phenomena in visual search, Stroop and Flanker tasks. Some source data were **earlier human experiments**; this paper primarily models/simulates those patterns, not a newly run E002a study. The authors report that simple rivals fit several phenomena less well, but **that does not prove LVOC is optimal, uniquely neural or necessary for digital minds**. The Results section includes cases of imperfect quantitative fit; the model makes predictions about feature-based transfer and failure under wrong linear assumptions. Sources: [full publisher article](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006043) and [PLOS figures/tables](https://journals.plos.org/ploscompbiol/article/figures?id=10.1371/journal.pcbi.1006043).

004 did not compare a *learned policy* against a strong learned external adaptive scheduler. A study that only compares an expressive candidate to weak deadline/cron heuristics is predictably misleading.

### C4 — identification and model capacity are underspecified

'Endogenous' can refer to (i) locus of policy computation, (ii) triggering without current user input, (iii) persistent learned regulation, (iv) adaptive state-driven resource allocation, or (v) subjective experience. These are different constructs. If the same algorithm can be placed outside or inside the labeled agent boundary, then the boundary alone is not an explanatory variable. A causal intervention on state must not simply give one arm information unavailable to the other. Model performance must be assessed against an *adaptively learned, budget matched and state-access matched* controller if making the distinctive claim.

### C5 — no reproducible comparative study

There is no frozen seed/design/outcome protocol, actual agent evaluation, confidence interval, prospective model comparison or independent replicator. A collection of formal arguments + unit tests therefore cannot justify G2, G4 or architectural promotion.

### C6 — weak interdisciplinary connection to research target

The dossier discusses computational metareasoning, but not the relevant competing cognitive-control mechanisms in sufficient depth, nor what would distinguish the chosen target from conscious ongoing experience. Basic behavioral resemblance cannot validate L3. The ethical issue of scheduling more intimate or persuasive social engagement remains an independent safety gate; making a program compute while idle is not a welfare result.

## Decision rules

- **Preserve** 004 as a previously persisted, accurately qualified **G0 exploratory instrument-calibration record**.
- **Mark** scientific-rigor outcome **MAJOR REVISION REQUIRED**. 'Verified iteration' denotes source persistence and bounded valid logic/testing, not publication-quality science or an independently validated research finding.
- **Do not** upgrade H005/H008, A0/A1, E900, L2 or L3.
- **Narrow** any claim to: under identical input, computational opportunity, initial state and identical decision/transition policy, checkpoint-visible state/actions are the same by construction.
- **Next scientific gate:** choose a testable comparison between externally scheduled *learned* policy and an internally maintained/learned regulation mechanism, or explicitly acknowledge there is no observable distinction under equal algorithms. Freeze a longitudinal trial with genuine update computations and held-out mechanism changes before rating agent performance.

## Proposed substantive acceptance criteria for future research

A full scientific report should (a) answer a precise question against a defensible rival; (b) give source-by-source *methods, sample/environment, actual comparison, result, caveat and transfer limit* for the literature most central to the claim, with full-text where accessible; (c) provide an explicit model/estimand and identify hidden assumptions; (d) offer a protocol that could genuinely falsify the result; (e) distinguish actual measurement from hand-created unit tests; and (f) include an adversarial referee report. If any are absent, the output is **RESEARCH CHECKPOINT / REVISION REQUIRED**, not high-rigor research—even if it reaches thousands of words or uses Superpowers.

## Provenance and limits of this audit

This is a self-review informed by direct GitHub reads of 004 and its living dossier, and inspected portions of the full publisher HTML for Lieder et al. (2018) plus earlier abstract-level entries S013–S015. It is **not** a full systematic literature review, external peer review or new randomized experiment. It adds a falsifiable *assessment* of the existing work and a candidate stronger research design; it does not add a confirmed agent result.
