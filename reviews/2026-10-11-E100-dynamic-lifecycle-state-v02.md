# E100 cross-day dynamic-state parity and lifecycle-cost counterexample — v0.2

**Research ID:** `E100-XDAY-2026-10-11-002` · **Kind:** experimental instrument / RESEARCH_NOTE · **Scientific quality:** `EXPLORATORY_CHECKPOINT` · **Review:** `SELF-REVIEW_ONLY` · **Date:** October 11, 2026 (Asia/Taipei) · **Parent:** Anjo / MIND · **Decision:** D001 remains DEFER/CURRENT · **Accepted science:** 0 · **E001:** G0 OPEN · **E900:** NOT STARTED · **L2 functional consciousness:** UNACHIEVED · **L3 phenomenal consciousness:** UNRESOLVED · **Product:** NOT_READY_FOR_PRODUCT_TRANSFER.

## Executive decision

Under complete, shared *dependency-edge* and *resource-status* evidence, a causal-link reader is **not uniquely necessary** for the chosen prospective one-step action: a continually updated compact state and an invalidated lazy state reproduce the same action under all 11,530 sampled queries. This result is an **elementary state-update equivalence** inside a predeclared finite simulator, not a new mind mechanism, result about learned agents, proof of optimal compression, or resolution of Day 2's causal-identifiability problem.

The **operationally relevant finding** is that a state alternative which ties the graph reader at fixed workload can impose drastically different maintenance costs in a changing environment. In a query-heavy, denser stratum, the lazy cache incurred 12.6% fewer *author-defined primitive operations* than repeated direct graph reading; in three other strata, direct graph reading was cheaper. But on the actual Python CPU-time diagnostic, direct graph reading was faster or approximately tied in all four strata. **Do not promote an architecture on either ranking:** primitive-operation weights are stylized and CPU timings are uncontrolled, small, implementation-dependent measurements. The result warrants *revised resource-parity criteria*, not special graph-memory support.

## Live provenance and selection

GitHub `main` at start of this attempt, verified via GitHub commit compare: `3c22a93a6d15a909789bb6e40c387a34b183ee7c`. Read canonical GO.md, AGENTS.md, CURRENT.md, research-state.md, TASKS.md, RUNBOOK.md, research-quality-gate.md and sources/README.md at that ref. Inspected current issues #1–#3, open PRs #7–#16 and their head/review status. #14 independently reproduces Day2 v0.2 (11 dedicated tests and 86 integrated tests, **reported by its contributor**, not rerun in this invocation), and #15 audits Day3; #13 audits Day5. PR #16 already contains a seven-case *transcribed* cross-day event-contract canary. We continued that same scoped PR, not a new competing PR or a fresh Day2–Day7 implementation.

Relevant source evidence and version pins:

| Input | Revision/identity | What it establishes, and what it does not |
|---|---|---|
| MIND Day2 PR #7 `day2.py` | Head `a0be278445c4119ac038204ea710bdd5af5bdd00`, Git blob `524cd567fffb842cb456e6fb54bf76e504d0b859` | The reader collects historical `tool_unavailable` resources without temporal retraction and traverses dependency edges; not a multi-period longitudinal agent. |
| MIND Day7 PR #12 `day7.py` | Head `f15de4cf62007c221da0ba5d531f4ce838b1ce56`, Git blob `57b804ee3cfbf0feaee07b78c49e57d6ec26a40d` | Public `tool_restored` can cancel older outage; direct-resource rather than Day2's dependency scope. |
| Previous cross-day review PR #16 | Initial head `bfa3ffc23d1aa17a6753e65941621b0f9d2f260c` | Identified the restoration and dependency-scope policy disagreements; used source-policy transcriptions only. |
| Day2 independent execution / information-boundary PR #14 | Head `ae537b448da64fcf017c9485a474e1f476352d9d` | Reported clean-checkout Day2 replication and a same-event/different-edge counterexample. Our experiment explicitly reveals edges to all compared controllers, avoiding its known information mismatch. No claim of fresh #14 reproduction. |
| New fixed protocol | `reviews/e100-crossday-contract/dynamic-protocol-v02.md`, committed **before** execution at `54f8465ea090b89babaaff821992ded818fb2157` | Freezes seeds, strata, outcomes and stop criteria. |

## Operational construct, estimands, assumptions

Public initial facts consist of a bipartite dependency graph `G ⊆ Goals × Resources` (8 known goals, 10 known resources) and initially usable resources. Each subsequently **public** event has a unique event_id and one of five kinds: unavailable/resource, restored/resource, added-edge, removed-edge, or goal query. A query should `DEFER` iff any current resource connected to the queried goal is unavailable, `SCAN` otherwise, and `NO_GOAL` for an unknown goal. This is an author-chosen prospective action *label*, not a scored consequence of real-world action.

Let `H_t` be the public ordered event history and `f(H_t,G_0,g)` be the reference action after replaying it. The planned **integrity estimand** is `err_π = (# queries with π(H_t,g) != f(H_t,G_0,g)) / # queries`. The planned **maintenance-cost contrast** is `Δ_C(π,graph) = C_π - C_graph`, where `C` is a fixed code-defined primitive operation count combining initialization, update processing and queries; components remain separately reported. This cost is NOT compute-equivalent to wall-clock, RAM, energy, network or training budget. A CPU-time diagnostic is secondary and explicitly not used as the primary adjudication.

**Arms:** (A) fresh graph adjacency check per query; (B) eager, fully recomputed cached blocked flags after dependency updates and affected-goal updates after status changes; (C) lazy cache invalidated on every public update, recomputed per goal on next query. Both B and C preserve the initial graph; **C is not a graph-free PSR**. The stateless reference independently replays all public events for each query with a separate set-of-edge implementation. Its cost is excluded from agent comparisons because it is a scoring oracle. All active arms see the exact same input edges, statuses, event sequence and goal queries; their *algorithms and costs* are deliberately different, then separately measured.

**Admissible domain:** deterministic, fully observed, instantaneous public events; known bipartite graph, no hidden parents/censoring, no uncertain evidence, no adversarial input, no multi-hop cycles, no human cognition, no learned agent and no actual integration of Day2 and Day7 Python modules. Under this restricted setup, information parity is maintained by construction; it is **not established for the original PRs' APIs**.

## Prospective protocol and executions

The protocol fixed four strata before code scoring: query rate 0.2 or 0.8 × edge probability 0.1 or 0.4, each 32 seeds `10000..10031`, each 180 sequential public events. Every non-query step selects a status event with probability 0.70 or an edge mutation with 0.30. There are 128 episodes = **23,040 generated events**, **11,530 prospective decision queries**. Each query is checked against an exact independent replay of the complete history; decisions are not allowed to read generator-hidden randomness or the oracle output. Full input-stream hashes and exact per-stratum costs are in `dynamic-results-v02.json`.

Observed Python 3.13.5 standard library, local Linux; no paid API/Actions:

```
python -m py_compile dynamic_probe.py
python dynamic_probe.py --self-test > results.json
python -m unittest -v test_dynamic_probe.py
python -m py_compile dynamic_probe.py test_dynamic_probe.py
python cpu_diagnostics.py > cpu_diagnostics.json
```

**OBSERVED:** main probe PASS; 5/5 dedicated unit tests PASS; independent action replay equality for all sampled queries. Independent exhaustive test enumerated **1,365** resource-status sequences (2 resources, both outage/restored, lengths 0–5) and checked all three active policies against replay. Also observed six explicit control responses; deliberately stale cache fails restoration as expected, and correcting its missing update restores parity. A tested link deletion and irrelevant-edge sham did not confuse the controllers. All three readers retained the same final graph and down-status sets per episode. The original MIND `agent_preflight.py`, `verify_instruments.py`, combined source modules, real SIGKILL worker recovery and LLM-agent trials were **NOT_EXECUTED** because direct GitHub clone fails DNS in this container. PR #14's reported 86/86 regression should not be attributed to this run.

### Main measured results — primitive operations, lower is better *under this declared proxy*

| Stratum | Query count | Graph direct | Eager compact | Lazy cache | Lazy vs graph |
|---|---:|---:|---:|---:|---:|
| 20% queries, sparse links (p=0.1) | 1,162 | **9,720** | 110,476 | 11,883 | +22.3% |
| 20% queries, denser links (p=0.4) | 1,162 | **15,845** | 244,131 | 17,896 | +12.9% |
| 80% queries, sparse links | 4,603 | **14,285** | 25,638 | 17,684 | +23.8% |
| 80% queries, denser links | 4,603 | 40,712 | 65,647 | **35,593** | −12.6% |

**Errors:** graph=0, eager=0, lazy=0 in each stratum, across all 11,530 queries. Results exclude learned update policies, alternative optimized eager algorithms and logging/IO overhead. Eager's very high cost is partly **by the chosen naïve recompute-all algorithm**, not a lower bound for compact representations. `lazy` still stores the graph; its 12.6% advantage is an incremental cache engineering result within this cost function, not an ontological or autobiographical-memory difference. A graph direct reader also could cache results.

### Secondary measured CPU diagnostic (not predeclared as primary metric)

`cpu_diagnostics.py` replays each episode in five iterations, rotating arm order; records `process_time_ns` per complete 180-event episode, 160 samples/arm/stratum. Medians in microseconds:

| Stratum | Graph | Eager | Lazy |
|---|---:|---:|---:|
| q=.2, density=.1 | **50.4** | 257.8 | 71.3 |
| q=.2, density=.4 | **59.8** | 442.5 | 81.3 |
| q=.8, density=.1 | **56.6** | 83.3 | 65.9 |
| q=.8, density=.4 | **87.9** | 139.5 | 89.6 |

**Adversarial contradiction to simplistic ranking:** On q=.8/density=.4, lazy wins the proxy by 12.6% but is marginally *slower* by this median CPU diagnostic (89.6 vs 87.9 µs). Relative difference is small and not supported by controlled microbenchmark uncertainty analysis. Never present proxy savings as measured latency savings. Python object allocation, interpreter operations, cache implementation and CPU timing noise can dominate the chosen primitive weights. CPU maxima reveal outliers; full range and exact durations in JSON. No independent hardware replication performed.

## Evidence matrix and literature boundaries

| Claim or methodological lead | Actual inspection | Strong contrary explanation / scope limit |
|---|---|---|
| Predictive state can be information-sufficient without graph autobiography | Littman, Sutton & Singh, *Predictive Representations of State* (NeurIPS 2001), full paper definitions §1 and theorem/proof §2, [original proceedings PDF](https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf), particularly printed theorem around PDF p7 and proof through p11. It constructs a finite linear PSR from a known finite POMDP with number of tests ≤ minimal POMDP states. | Predicts *action-observation tests*, not reward-optimal policies; it assumes known environment and gives no bound on online training/refresh time for these MIND worlds. Our lazy cache is not a learned PSR. Does not justify choosing compact memory automatically. |
| Graph dependency queries can be maintained incrementally; costs shift to updates | Szárnyas, *Incremental View Maintenance for Property Graph Queries*, arXiv:1712.04108v1 (2017/2018 six-page manuscript), full text §§1–4 (graph relational algebra, typed edge/path structure, transform GRA→NRA→FRA, paths as atomic list updates), [PDF](https://arxiv.org/pdf/1712.04108). | A proposed query-language compilation method, not a controlled cognitive trial or CPU benchmark for our controllers. Shows methodological need to price updates and path type/order; cannot supply any empirical speedup value for MIND. |
| Day2 data-parity deficit | PR #14's independently reported execution/addendum, source-level methods and same-event/different-link counterexample, read at exact PR head. | The *initial causal graph is additional input* in PR7; equal events alone do not imply information parity. Our explicit initial edge visibility removes this particular confound by construction, not by repairing PR7. |
| Cross-day restoration semantics | PR #7 vs PR #12 original source and PR #16 transcribed test, exact blobs above. | Isolated lesion programs are not required to use a shared temporal ontology; the disagreement only blocks claiming an integrated single policy without adapter tests. |

No claim to systematic review: method-led selection of two decision-critical full-text papers; no comprehensive search/exclusions or effect-size synthesis. The papers supply mathematical/engineering context only, not external validation of this program's observed results. The experimental program remains self-authored and self-audited.

## Doubt-driven self-audit (degraded; no fresh-context reviewer)

The available `doubt-driven-development` and `code-review-and-quality` installed skill instructions were read; **Superpowers' named skills/tools were NOT exposed in this task runtime**, although plugin discovery reports its installation. The required fresh-context reviewer step of doubt-driven was unavailable. This is explicitly **SELF-REVIEW_ONLY** (degraded). In lieu of fictional reviewers, adversarial falsification used an intentionally stale-cache mutation, exhaustive small-world sequences, a separate replay algorithm, and cost-metric disagreement.

Specific remaining critiques:
1. The reference and agents share declared event semantics; agreement may be tautological. No independent ground-truth counterfactual intervention or reward uncertainty.
2. The eager baseline is intentionally not optimized; an incremental reverse-index or priority scheduling could reduce update work. Declining performance is not evidence against all compact memory.
3. The lazy cache holds the full graph; it is not a graph-free sufficient predictive representation and uses an unconstrained cache-memory footprint. Comparing it to the graph reader does not identify unique memory semantics.
4. All events are complete, immediate and public. Historical source-truth conflation, informatively censored observations, delayed reports, hierarchy and multi-hop dependencies are excluded.
5. Operation weights are arbitrary: the CPU diagnostic contradicts an apparent proxy win in one stratum. No cost parity against actual MIND hardware is established.
6. Fixed seeds and small sample world family restrict external validity; no error bars for stochastic model performance (there is no learned stochastic model here). No legitimate inferential statistical agent efficacy claim.
7. Original independent Day 2/Day 7 subprocesses and SQLite ledgers were not invoked; current results concern the newly published standalone simulator, not a combined MIND entity.

### Quality gate and ledger impact

`research-quality-gate.md` checks: constructs, strong alternative, explicit estimand, frozen method and actual instrument execution are present. **SCIENTIFIC_ACCEPTED FAILS**: no empirical *mechanism-discriminating* advantage, no held-out learned agent outcome, no true resource-parity test or independent science review, no end-to-end original code integration. Verdict **EXPLORATORY_CHECKPOINT**; keep one work ID, no new H, architecture promotion, accepted-count change, or G0–G5 advancement. New knowledge is a *methodological requirement*: preserve temporal event retractions and publicly learned dependency edges, include lifecycle update cost, and test actual original modules. D001 stays DEFER; no Anjo transfer.

**Exactly one next executable action:** an authorized separate integration reviewer should assemble byte-exact current PR #7–#12 sources and tests in a disposable checkout, run `python scripts/agent_preflight.py` and `python scripts/verify_instruments.py`, then run a shared public-history adapter (outage→restoration, graph-link changes, indirect dependencies) through the **original** Day2/Day7 SQLite worker modules, contrasting fresh graph, graph reconstruction and maintained compact state with *measured* initialization+refresh+decision CPU/memory/SQL costs and distinct process recovery. Stop and report incompatibilities rather than merging until input parity and the scientific gate are satisfied.
