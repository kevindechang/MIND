# Migration from v1 to v2

v1's last main commit is `3c22a93`. v2 keeps every v1 artifact. Science stays in place. Governance moved, unchanged,
to [archive/v1/](../archive/v1/README.md). Nothing from v1 was counted as v2 evidence by fiat: each v1 result that v2
relies on was **re-executed** as a claim and earned its level on its own.

## Where everything went

| v1 | v2 |
|---|---|
| `research-state.md` (hand-written, 23 KB, stacked handoffs) | [STATUS.md](../STATUS.md), generated; v1 text kept at `archive/v1/research-state.md` |
| `GO.md`, `AGENTS.md`, `CURRENT.md`, `TASKS.md`, `RUNBOOK.md` | new [GO.md](../GO.md) and [AGENTS.md](../AGENTS.md); the task queue is the computed STATUS frontier |
| `research-cycle.md`, `protocol.md`, `research-quality-gate.md`, `publication-standard.md`, `review-protocol.md` | [PIPELINE.md](PIPELINE.md) and [CLAIMS.md](CLAIMS.md); rules enforced in `mind/claims.py`, `mind/knowledge.py`, `mind/doctor.py` |
| `research-records.md` (work index; "accepted: 0") | `knowledge/records/` and the computed evidence ladder |
| `decision-register.md` (D001, manual NEEDS_REASSESSMENT) | claim premises (`depends_on`) with automatic STALE propagation; D001's question is [H001](../knowledge/questions/H001.md) |
| `asset-register.md` | the substrate itself: assets are imported and executed, not indexed |
| `hypotheses.md` H001–H012 | [knowledge/questions/](../knowledge/questions/) H001–H012, each with a `next:` step; v2 adds H013 (from Day 6) and P001 (a pipeline question) |
| `evidence-ledger.md` | [knowledge/literature.md](../knowledge/literature.md) (moved unchanged) |
| `north-star.md`, `charter.md`, `workstreams.md` | mission and ethics in [README.md](../README.md) and [AGENTS.md](../AGENTS.md); functional-consciousness operationalisation in [PIPELINE.md §5](PIPELINE.md) |
| `architecture.md` (A0), `candidates/A1` | A0's decomposition made executable (workspace, memory, self-model, goals, policy); A1 mechanisms are questions H002, H008, H010, H011, H012 |
| `atlas/` traceability matrix | the STATUS knowledge graph and the integration atlas (`python -m mind atlas`) |
| `scripts/agent_preflight.py` | a shim that runs `python -m mind doctor` |
| `scripts/verify_instruments.py` | unchanged; claim L01 runs the v1 suite on every check |
| `experiments/`, `dossiers/`, `reviews/`, `runs/`, `sources/` | unchanged (claims cite them through `extends`) |

## v1 experiments, re-expressed

| v1 | v2 |
|---|---|
| E100 Day 0 restart circuit | [L02](../knowledge/claims/L02_e100_day0_restart_circuit.py) re-runs it unchanged; generalised to the whole learning organism by [K01](../knowledge/claims/K01_continuity_replay.py) (any death, any lesion), [K02](../knowledge/claims/K02_real_sigkill_exactly_once.py) (real SIGKILL), [K06](../knowledge/claims/K06_cross_process_replay.py) (fresh processes, any hash seed) and [K07](../knowledge/claims/K07_exactly_once_after_commit.py) (exactly-once after a durable commit) |
| Day 1 broadcast lesion | [L03](../knowledge/claims/L03_e100_day1_routing_lesion.py) re-runs it; the lesion is now the kernel operator `cut:X>Y`; the broadcast question became [C005](../knowledge/claims/C005_bottleneck_helps_under_distractors.py) / [C006](../knowledge/claims/C006_bottleneck_neutral_without_distractors.py) |
| Day 2 causal links | the `workshop` world plus the H001 frontier item (a causal organ, then `-causal` with memory intact) |
| Day 3 self-model | the `outage` world; [C017](../knowledge/claims/C017_self_model_beats_table_same_events.py) / [C018](../knowledge/claims/C018_self_model_beats_table_when_silent.py) (learned self-model vs the success-table rule, scored on the same events; first-round C007/C008 retired after review); #15's announcement-reading rival is the next step of [H002](../knowledge/questions/H002.md) |
| Day 4 goals / initiative | the `vigil` world; [C001](../knowledge/claims/C001_commitment_needs_memory_or_goals.py)–[C004](../knowledge/claims/C004_memory_goals_degeneracy.py) (necessity is context-dependent; memory and goals are degenerate) |
| Day 5 maintenance | [H008](../knowledge/questions/H008.md) next step: maintenance organ vs learned external scheduler |
| Day 6 liar twin | [H013](../knowledge/questions/H013.md): an introspection-validity probe (does the organism's report predict its next action better than a narrator without access to its internal state?) |
| Day 7 ledger fork | the kernel's `Ledger.fork()`; claim K05 was retired after review (divergence by construction) |
| E001 v0.1–v0.4 | facts [L04](../knowledge/claims/L04_e001_reachability_quotient.py)–[L07](../knowledge/claims/L07_e001_prior_flips_plan.py) re-executed by the original instruments; the v0.4 DP is the workshop's exact optimum and `rival:bayes` ([K04](../knowledge/claims/K04_workshop_matches_legacy_optimum.py)); [C011](../knowledge/claims/C011_no_causal_advantage_in_workshop.py)/[C012](../knowledge/claims/C012_organism_far_from_bayes_optimum.py) measure the organism against it |
| E002 / E003 / E900 | questions H005, H008, H010, H011, H012; E900's integration aim is the atlas and [C016](../knowledge/claims/C016_integration_holm_corrected.py) |

## The open PRs (#7–#16) and issues (#1–#3)

They were built as separate toys, so merging them as-is would reintroduce exactly the fragmentation v2 removes.
Their *findings* are worth keeping, and v2 keeps them:

| PR / issue | Finding | v2 |
|---|---|---|
| #7 Day 2 | the lesion removed a cached answer; the "rival" was that cache | superseded: the workshop world, plus a causal organ on the H001 frontier |
| #8 Day 3 | confidence was a constant (0.9/0.4) | superseded: C017/C018, a learned self-model scored by Brier on the same events |
| #9 Day 4 | the rival was AST-identical to the mechanism | superseded: C001–C004 on a learning organism |
| #10 Day 5 | the "null" was an identity; the cron loss was planted | H008 next step |
| #11 Day 6 | the grounded reader acted better (3 vs 1), yet a constructed preference metric favoured the zero-read narrator | [H013](../knowledge/questions/H013.md): report validity scored by prediction, never by preference, with the narrator as its rival |
| #12 Day 7 | divergence was injected by the supervisor | superseded by `Ledger.fork()` on the shared organism (the fork claim K05 was itself retired as by-construction) |
| #13 Day 5 review | payoff-shift and all-negative counterexamples; learned scheduler as rival | carried into H008 |
| #14 Day 2 audit | equal events ≠ equal information; reconstruction/access/knockout lesions; acute vs recovered | lesion operators and `@E:` scheduled lesions ([SUBSTRATE.md](SUBSTRATE.md)); H012 |
| #15 Day 3 audit | an event-aware controller, which reads the outage announcements, reproduces the hand-written self-model (72/72) | partly answered. On the same events the learned self-model beats a per-action success table with announcements (C017) and without them (C018). The announcement-updated table is now a same-event scorer: C041 is inconclusive at C017's 0.008 margin, and on a silent reliability step the surprise broadcast does not speed re-adaptation (C042, C043 refuted). See [H002](../knowledge/questions/H002.md). |
| #16 cross-day contract | the days contradict each other on one ledger | resolved by construction: one organism, one vocabulary, one ledger |
| #1 regression suite | — | L01 plus `python -m mind check` |
| #2 E100 queue | — | replaced by the computed frontier |
| #3 E002a identifiability | — | H008 |

With the owner's approval, #7–#16 are closed with a pointer to this table, and #1–#3 close when v2 merges. Their
branches are kept, so any of them can be reopened.

## Scheduled runners

The owner's existing hourly research task reads GO.md first. The new GO.md works for any agent with a checkout and
Python. An agent without code execution can still add questions, literature, or claims that show as UNTESTED.

## Adversarial review of v2

Before publication, a separately invoked reviewer attacked the v2 pipeline itself and found 1 critical and 7
important defects. They were fixed, the affected claims were retired with stated reasons and successors were
registered. Every claim was re-confirmed on held-out seeds afterwards. See
[reviews/2026-10-10-v2-pipeline-adversarial-review.md](../reviews/2026-10-10-v2-pipeline-adversarial-review.md).

