# H001 Literature and Evidence Matrix — targeted source inventory v0.1

**Coverage date: 2026-10-10. Status: SEED; NOT a systematic or PRISMA-ScR-compliant review.** S001–S012 citations are defined in the canonical [evidence ledger](../../evidence-ledger.md). The following evaluations predominantly inherit previously inspected abstracts/metadata; no full-method audit is asserted here.

## Search method and evidence boundary

This initial inventory was curated through the preceding research iterations 001–003, focusing on conversational memory, action-based memory benchmarks and compact-state/causal reasoning rivals. **Not performed:** reproducible database-wide query strings, systematic deduplication, inclusion/exclusion screening, reference chasing, dual-reviewer extraction, formal risk-of-bias scoring or meta-analysis. Papers were not collected prospectively under a preregistered review protocol. Therefore citation count is neither a comprehensive inventory nor a measure of consensus.

| Source | Topic/type (reported) | Inspection state | What it can illuminate | What it cannot establish |
|---|---|---|---|---|
| [S003 LongMemEval](https://arxiv.org/abs/2410.10813), Wu et al. 2024/ICLR 2025 | Long-term chat memory evaluation | ABSTRACT/METADATA previously checked | Temporal updates, abstention and retrieval | Necessity of autobiographical causal graphs |
| [S004 MemoryAgentBench](https://arxiv.org/abs/2507.05257), Hu et al. 2025, 2026 v4 | Incremental agent memory and selective forgetting | ABSTRACT + selected APPENDIX previously checked | Baselines under different context budgets; forgetting | Fair FLOP-matched causal action effect in E001 |
| [S005 LoCoMo](https://arxiv.org/abs/2402.17753), Maharana et al. 2024 | Longitudinal dialogue QA/event summaries | ABSTRACT/METADATA checked | Long-session temporal consistency | Downstream intervention-regret after process reset |
| [S006 MemoryArena](https://proceedings.mlr.press/v306/he26am.html), He et al. ICML 2026 | Interdependent agentic multi-session benchmark | ABSTRACT/METADATA checked | Real decisions dependent on earlier sessions | Proof that graph memory beats optimal belief state |
| [S007 EMBER-Bench](https://arxiv.org/abs/2610.05013), Cai et al. 2026 preprint | Cross-event embodied historical constraints | ABSTRACT/METADATA checked | Causal traceback and next-action challenge | Replicated E001 agent performance |
| [S008 Kaelbling–Littman–Cassandra](https://doi.org/10.1016/S0004-3702(98)00023-X), 1998 | Partially observed stochastic decision theory | PUBLISHER ABSTRACT/THEORETICAL lead | Belief state as strong information-state rival | Real-world tractability or a graph impossibility theorem |
| [S009 Littman–Sutton–Singh](https://proceedings.neurips.cc/paper_files/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html), 2001 | Predictive-state representation | PROCEEDINGS ABSTRACT/THEORETICAL lead | Action-conditional predictive compression | The best learned representation on present benchmarks |
| [S010 AMA-Bench](https://proceedings.mlr.press/v306/zhao26bs.html), Zhao et al. ICML 2026 | Long action-observation memory | ABSTRACT/METADATA checked | Action and state-update benchmark design | E001 mechanism necessity or replication |
| [S011 CausalGame](https://proceedings.mlr.press/v306/chen26l.html), Chen et al. ICML 2026 | Interactive causal thinking | ABSTRACT/METADATA checked | Noisy/biased intervention design | Autobiographical identity or consciousness |
| [S012 Causal Memory Intervention](https://arxiv.org/abs/2605.17641), 2026 preprint | Intervention-informed memory selection | ABSTRACT checked | Retrieval/admission baselines | Prospective action-level causal memory gains |

All interpretations above are limited to the reported source scope. Dates/type should be cross-checked from the original manuscripts before citation in a mature dossier. Do not inflate a source's provenance grade simply by including it in this table.

## Preliminary across-study reading

The published benchmark set includes multiple distinct targets: QA, temporal updating, agentic actions, and causal environment interaction. Their results are not interchangeable or eligible for a pooled numerical effect under present extraction. The central *disagreement* is methodological: improved retrieval performance may not imply improved control after altered causal conditions, and a task explicitly depending on history does not force any specific representation of that history.

Key missing evidence: human autobiographical-memory and identity literature; causal credit assignment under feedback delay; formal partial observability/robust planning; deep methods inspection for all 2026 action benchmarks; direct benchmark implementation comparisons under matched information/FLOPs; falsification of graph-based memory superiority; ethics and artificial welfare literature.

## Next source review protocol

Before calling this a scoping review, freeze a research question with population/agent type, constructs (causal memory vs sufficient belief), environments, outcomes, languages, year coverage, eligible source types and databases. Record each executable database query and date, counts retrieved/screened/excluded with reasons, study-level methods and limitation, and at least one disconfirming result per central claim. Report review limitations and accessible/full-text proportions. [PRISMA-ScR](https://www.prisma-statement.org/scoping) can guide the reporting when the actual method meets its requirements; it is **not** a label to award in advance.

## Provenance

Source IDs and descriptions adapted from [evidence-ledger.md](../../evidence-ledger.md), [iteration 001](../../runs/2026-10-10-iteration-001.md), [002](../../runs/2026-10-10-iteration-002.md), [003](../../runs/2026-10-10-iteration-003.md). No new independent experiments or full-text review were carried out to seed this document.
