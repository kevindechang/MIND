# Research decision register

This is decision memory, not a second hypothesis or evidence ledger. Claims remain in [hypotheses](hypotheses.md), [dossiers](dossiers/README.md) and the [evidence ledger](evidence-ledger.md). A decision status is distinct from hypothesis support and scientific acceptance.

## Rules

- Stable IDs D001, D002, …; do not reuse retired IDs. Add a record only for a concrete question with an outcome-to-action map.
- Status: ACCEPT / REVISE / REJECT / DEFER. Freshness: CURRENT / NEEDS_REASSESSMENT / SUPERSEDED. CURRENT means the cited justification is up to date, not that it is empirically validated.
- Cite pivotal evidence with paths, claim anchors and immutable versions/commits; label SUPPORTS / CONTRADICTS / INFORMS. Disclose common datasets or research lineages; paper count is not independent evidence.
- If pivotal evidence changes or fails, follow affected claim → direct decision → every transitive dependent decision; flag NEEDS_REASSESSMENT with the reason. Do not automatically reverse conclusions. Block promotions relying on the flagged premise until alternate justification or new evidence is reviewed and logged. Preserve originals and amendments.
- Each new record lists prerequisites, dependents, costs, actual review mode, scope limits, integration consequence and next falsifier. Dependency cycles must be resolved as one joint question or removed; never rely on circular justification.
- ACCEPT authorizes a bounded research conclusion only within existing approvals; architecture adoption, deployment and spending retain their approval gates.

## Index

| Decision | Question / linked claim | Status | Freshness | Gate |
|---|---|---|---|---|
| [D001](#d001-causal-autobiographical-representation) | Representation for [H001](hypotheses.md#h001-decision-link) / E001 | DEFER | CURRENT | G0 OPEN |

## D001 causal autobiographical representation

**Question:** Under specified partial observation and fair total lifecycle resources, does structured causal autobiography improve action regret, repair or efficiency over transcript/retrieval and feasible compact belief/predictive-state rivals?

**Choice:** richer causal memory vs simpler sufficient state/history. A0 and A1 remain unvalidated candidates; no representation adopted.

**Prerequisites:** no prerequisite decision IDs yet. E001 requires observation-history-valid oracle, identifiable/unidentifiable case definitions, lifecycle resource parity, held-out mechanism families and frozen G2 analysis before scores can adjudicate D001.

**Pivotal support/contradiction:** NONE; no agent comparison. **INFORMS:** [E001 draft protocol](experiments/E001/preregistration.md), [instrument v0.2](experiments/E001-G0-instrument-validation-v0.2.md) and [commitments candidate](experiments/E001-stage1-causal-commitments-v0.1.md), as inspected at baseline commit `4ec49fa45878ec33a4a07658fc418f535a5ee86f`. These document sufficient-statistic rivals and instrument limitations, not H001 efficacy. Primary-source entries are not independent project replications.

**New methodological input (INFORMS only; no efficacy support):** [E001 permitted-history oracle v0.1](experiments/E001/E001-G0-permitted-history-oracle-v0.1.md), initial method commit `578adb5bd10d65f84bd72f7dccf73370f51a2e6f`, includes a history-only belief reference, ambiguous/identifiable toy worlds and 16 locally executed synthetic checks; [ASET006](asset-register.md) lists the calibration. This does not close E001 G0 or adjudicate graph utility; the actual multi-node partial-observation oracle remains unimplemented.

**Outcome → action (apply the prospectively frozen analysis):**

| Outcome | Decision consequence |
|---|---|
| Fair held-out advantage over strong rivals plus targeted causal-ablation sensitivity | Scoped support for utility; propose replication and integration test, not graph necessity or L3 |
| Simple rival outperforms, or matches within a preregistered equivalence/noninferiority margin | Prefer simpler representation in tested scope; weaken necessity; retain transfer questions |
| Imprecise null or mixed effects | INCONCLUSIVE; inspect precision/failure strata; never infer equivalence from nonsignificance |
| Leaked oracle, invalid identification or confounded budgets | Invalidate affected comparison; repair and flag dependents |
| Asserted advantage disappears under fair controls | Reject asserted advantage in tested scope; preserve negative evidence and reusable assets |

**Decision:** DEFER. **Confidence:** LOW regarding advantage; no scored trials. **Review:** SELF-REVIEW_ONLY for initial governance mapping. **Freshness:** CURRENT for these proposal/limitation records, not scientific validation.

**Costs:** record construction, storage, correction, retrieval, inference and tool costs; numeric ceilings and effect thresholds remain UNFROZEN in E001. Exact inference capabilities are checked per invocation; no paid execution implied.

**Downstream dependents:** no adopted downstream decision yet. E900 memory↔goal coupling and candidate representation choices must cite D001 if they rely on an eventual result.

**E900 intervention:** after a scoped result and separately approved candidate, remove/corrupt an experience-to-consequence link while holding observations and resources fixed; measure downstream goal/planning changes against simpler persistent baseline and sham. This is PROPOSED, not integration evidence.

**Next disconfirming step:** implement and validate an enumerated version-space, selective-probe oracle on a three-node CausalWorkshop subset; vary the evaluator's private sampled graph while holding public histories fixed and assert equal admissible action sets. Test delayed/censored feedback; reject any hidden-state-dependent output. This is still G0, before a scored comparison.

**Revision history:** 2026-10-10 — initialized from existing E001 records as governance; no gate, hypothesis or architecture promoted.

**2026-10-11 update:** D001 remains DEFER/CURRENT. The v0.1 method is only INFORMS, not pivotal SUPPORTS; independent scientific review remains unavailable and no dependent decision is promoted.

**2026-10-11 update (IV-D001-2026-10-11-003):** D001 remains DEFER/CURRENT, no scored efficacy and G0 OPEN. [v0.3 robustness](experiments/E001/E001-G0-prior-censoring-robustness-v0.3.md) exposes a concrete methodological counterexample: non-ignorable censoring changes a history-only posterior despite identical delivered masks; non-uniform prior can change best action without changing public history. ASET008's new instrument was locally checked with 20 assertions against a reconstructed compatibility fixture, not a canonical integration execution. This evidence INFORMS the need for registered prior/delivery sensitivity and fair compact-state rivals; it SUPPORTS no autobiographical graph-memory efficacy. Review SELF-REVIEW_ONLY. No pivotal efficacy dependency invalidated because none exists.

**2026-10-11 update (IV-D001-2026-10-11-002):** D001 remains DEFER/CURRENT. New [v0.2 3-node version-space oracle](experiments/E001/E001-G0-selective-probe-version-space-v0.2.md) ([ASET007](../asset-register.md)) is INFORMS only: it implements the enumerated version-space selective-probe oracle requested as the next disconfirming step, with 14 local unit checks passing and no private-state leakage detected. No scored agent comparison ran, so there is still no efficacy SUPPORTS; G0 stays OPEN, G2 unfrozen, and no dependent decision is promoted. Review SELF-REVIEW_ONLY.

**2026-10-11 update (IV-D001-2026-10-11-004):** D001 remains DEFER/CURRENT, E001 G0 OPEN, no agent efficacy. [v0.4](experiments/E001/E001-G0-policy-value-identifiability-v0.4.md) INFORMS: 8 forward DAGs have 7 reachability classes (graphs 5/7 redundant-edge equivalence); exact public-history finite-horizon acquisition reference yields synthetic adaptive B2>B1 gain 7/120. No SUPPORTS for graph-memory necessity; compact closure-belief + queue and predictive-state rivals strengthened. Graph-dependent censor requires predictive observation-model state. ASET009 standalone locally checked; canonical integration, real reset, G2 and agent trials OPEN. SELF-REVIEW_ONLY; no dependent promotion.
