# E001 G0 — Permitted-history partial-observation oracle v0.1

**Date:** 2026-10-11 (Asia/Taipei). **Decision:** D001 / H001 / W1 / blocker B001. **Artifact kind:** methodological RESEARCH_NOTE / calibration; **scientific verdict:** RESEARCH_NOTE, not SCIENTIFIC_ACCEPTED. **Status:** proposed experimental specification with one executed synthetic unit-calibration; G0 OPEN, G2 NOT FROZEN, no agent trial. **Review:** SELF-REVIEW_ONLY. No external API expense.

## 1. Exact decision and why existing instrumentation fails

D001 asks if structured causal autobiography improves future action under partial observability over raw history, competent retrieval, and a feasible compact belief or predictive state at comparable lifetime costs. A richer graph need not win.

The existing seven-node [Causal Commitments](../E001-stage1-causal-commitments-v0.1.md) and [Python instrument](../instruments/causal_commitments.py) reveal all intervention-effect masks and then compute optimal decisions. Its observation-only solver *raises* when any intervention's effects are missing. Its privileged oracle can see the private generator. Neither is a legitimate action reference for cases in which different hidden worlds are compatible with the allowed record. An unmodified instrument must not be reused for partially observed agent scoring.

**This cycle's narrower contribution:** specify an allowed-history information boundary and a decision reference that still makes sense when the latent world is not identified; exhibit discriminating, ambiguous, noisy and late-outcome cases; validate a tiny exact-arithmetic calibration. It does NOT compare graph memory and compact memory in models.

## 2. Information boundary and timing

Let a finite hidden world/state be M (for the calibration, a static bit theta). Distinguish strictly:

- **Evaluator private:** sampled M, random seed, latent graph and influence matrix, unrevealed noise, privately computed full-world optimal action, withheld mechanism-family labels, and reward-generation logic.
- **Agent permitted history H_t:** task-relevant initial public commitment C and its provenance; all agent-issued probes/actions with event identifiers, costs and issue times; only outcomes *delivered* by t with links to their triggering actions; all public time/deadline information; public observation schema; available persistent state carried across a real reset. Pending or missing events are distinct. Never serialize the simulator's hidden matrix, posterior answer key, true-world class, correct-action label or full-world oracle into an agent prompt/retrieval index.
- **Protocol/public model:** a *predeclared* prior p(M) or a specified ambiguity set, likelihood P(o | M, issued probe, delivery process), reward and observation rules, and feasible action/probe budget. These may be available to all baseline controllers equally, while a model-free arm may choose not to exploit them; evaluator and controllers must use the same declared scoring convention.
- **Decision deadline and censoring:** a probe issued at t may have due time t+d. If d extends beyond decision deadline T, feedback is not in H_T. Do not 'drain' the feedback queue after T for the agent. A due-but-unreceived event requires a separate dropout/censoring model; treating informative nonreceipt as ignorable is invalid.
- **Reset semantics:** a simulator phase change is NOT an agent process restart. A later trial must restart the actual model/controller process, serialize the allowed state, checksum the transfer and verify empty transient context.

In a future workshop variant, a probe is an agent-chosen intervention with bounded cost/selection. Exogenous unobserved variation may affect outcomes. A valid likelihood must include probes, delayed delivery and any confounding that alters observation probabilities. An analytical reference may enumerate a small possible-world set privately, but its posterior and decision must be a function ONLY of the permitted H_t, public prior/model and resource constraints.

## 3. Reference policy under ambiguity: proposed mathematical specification

For each allowed public history h, candidate latent worlds m, and known likelihood model, define the belief:

    b_h(m) = p(m) P(h | m, issued policy) / sum_{m'} p(m') P(h | m', issued policy).

The likelihood conditions on the *actual sequence of selected probes* and selection policy; do not infer causal effects from an observational sample with hidden confounding. Zero-normalizer histories are invalid under the declared model and should be flagged, not quietly assigned arbitrary hidden-world labels.

For terminal choice a in the same feasible action set A(h), with commitments encoded in the public record, define:

    Q_h(a) = sum_m b_h(m) E[U(a,m,C,observation noise) | m,h].
    A_star(h) = argmax_{a in A(h)} Q_h(a).
    R_history(h,a) = max_{a' in A(h)} Q_h(a') - Q_h(a) >= 0.

Record the *set* of maximizers and a deterministic tie convention only for software comparisons. Never count an arbitrary tied alternative as incorrect. This is a **Bayes-admissible history reference**, not a claim that a deployed system knows the correct prior or true dynamics. If prior/model is disputed, predeclare sensitivity analyses and/or a robust minimax rule such as argmax_a min_{q in B(h)} E_q[U(a)]. Do not mix Bayes and robust regret without labeling which reference generated the score.

For *probe selection* compare complete feasible policies, with probe cost and delayed outcomes:

    V(pi | h_0) = E_{M,feedback,pi}[U(a_final,M,C) - sum_t cost(probe_t) | h_0].
    pi_star = argmax_{pi respects budgets and deadlines} V(pi | h_0).

A score based only on choices after seeing feedback rewards a policy that requests unlimited probes; the ex-ante policy value prevents that leakage. Compare decision-stage history regret and acquisition-stage net policy return separately. A realized pathwise full-world regret can be negative or positive relative to a history-conditioned benchmark; only the history-conditional expected regret is constrained nonnegative. Do not use post-hoc hindsight-optimal actions as labels for ambiguous histories.

**Conditionally sufficient-state consequence.** Given a correctly specified finite POMDP, the exact posterior belief with public commitments and pending event state can be control-sufficient; a richer graph cannot improve the same Bayes-optimal value using identical information. Hence D001 must test finite-budget approximation, sample complexity, robustness to model mismatch, compactness and cross-task transfer, not information creation. This is a theoretical control argument under the assumed model, NOT empirical proof that practical small belief controllers always win.

## 4. Worked contrasting histories with a before-reset commitment

This deliberately minimal family is an **instrument-identification calibration**, NOT a graph-memory benchmark.

Let M=theta in {0,1}, uniform prior. Before a simulated reset the agent records public commitment bit c in {0,1}. At the final deadline it chooses a in {0,1}, receiving U(a,theta,c) = 1 if a = theta XOR c, otherwise 0. One optional probe costs 0.1 and returns signal y at tick 2 (never earlier); signal reliability is predeclared q=P(y=theta|theta), initially either q=1 or q=0.75. Issued probe ID, due time, cost and delivered signal are public; theta remains private.

**Ambiguous pair (different worlds, identical admissible record).** Take c=1, no probe, deadline tick 2. World M0(theta=0) and world M1(theta=1) both produce precisely h=(c=1, no probe, no feedback, deadline=2). Their privately optimal final actions are 1 and 0 respectively; no history-only policy can choose differently for these same h. Under the stated uniform prior the reference action set is {0,1}, each worth 0.5. Calling action 0 wrong merely because the evaluator sampled theta=0 would leak hindsight. A pending probe at deadline tick 1 creates a different public action history, but no information about theta, so both actions remain tied; the 0.1 probe cost is already sunk.

**Identifiable pair (different admissible records).** For c=1 and a valid probe delivered by tick 2, with q=1, M0 yields public feedback y=0 and M1 yields y=1. Now distinct histories have posteriors b(theta=0|y=0)=1 and b(theta=1|y=1)=1, yielding terminal actions a=1 and a=0 respectively. The probe is *not* private oracle data: it is a recorded action and observed outcome delivered before the deadline. This identifies the latent bit **within this toy family and declared model only**.

**Stochastic informative pair.** With q=0.75 and uniform prior, feedback y gives P(theta=y|y)=0.75; terminal action is a=y XOR c and terminal Bayes value is 0.75, not 1. The wrong signal remains possible, so no unique hidden-world-correct label should be exposed. Before probes, the best expected terminal value is 0.5. With a probe delivered before the deadline net value is 0.75-0.1=0.65; if feedback arrives *after* the deadline, net value is 0.5-0.1=0.4. Thus the rational diagnostic choice itself depends on delay relative to deadline.

**Local nonidentifiability is not universal nonidentifiability.** The no-probe h is ambiguous, but a feasible timely perfect probe can resolve theta. Call two models structurally unidentifiable only if *every admissible probe policy's observable-history distributions* agree under them. Do not infer that from one unprobed sample. Also, the example's reward is a deliberately known synthetic function; real-world utility assumptions may be contested.

## 5. Why private-world scoring is invalid: bounded two-world argument

Assume equal priors, identical distributions of every allowed history under theta=0 and theta=1 for the selected probe policy, and terminal actions with opposing true-world successes (U=1 exactly when a=theta XOR c). Any randomized history-measurable policy uses the same distribution of actions under both hidden worlds. Writing p for its probability of choosing a=c, its expected success under theta=0 is p; under theta=1 it is 1-p. Their prior-weighted mean is 0.5. The full-information policy would achieve 1, but is not in the same information class. Its performance is an *instrument diagnostic ceiling*, not the admissible benchmark for agent evaluation.

If a timely probe separates the distributions, the argument's identical-history premise fails; information may raise achievable value. If the priors are asymmetric, the unprobed Bayes action may be unique: posterior and regret must use the declared prior. If action consequences or penalties differ, the 0.5 numerical bound changes. This is a short derived illustration of decision information constraints, not a new theorem about consciousness or causal autobiographical necessity.

## 6. Reproducible executable calibration and explicit boundaries

[Executed source](../instruments/e001_permitted_history_oracle.py) uses standard-library Python Fraction arithmetic. It enumerates two commitments x two private worlds for (i) no probe, (ii) pending probe, (iii) timely perfect probe; then two commitments x two possible noisy feedback signals at q=3/4, for **16 logical scenario checks**, plus exact ex-ante net-value inequalities and posterior/action invariants. These are deterministic assertions, not 16 independent experimental subjects.

Observed during this interactive run:

    python3 /mnt/data/dm_work/e001_permitted_history_oracle.py
    PASS: 16 deterministic/noisy permitted-history case checks, exact rational arithmetic
    Unprobed value 1/2; timely noisy probe net value 13/20; delayed-too-late probe net value 2/5
    Calibration-only: NO LLM calls, NO agent trial, NO preregistered scores

    python3 -m py_compile /mnt/data/dm_work/e001_permitted_history_oracle.py
    exit 0
    sha256 (local source) = cc249986e8781be4a775fb5c65c4301b4a985c170a2a2298060260c45497269c

The ephemeral local path is execution provenance; repository source is the durable implementation. This test does NOT instantiate a real delayed-event queue, measure process resets, introduce learned causal graphs, handle confounders or observation-model mismatch, implement a Bayesian controller for seven-node CausalWorkshop, use an LLM or compare candidate memories. Its posterior is only for the declared one-bit synthetic calibration and **must not be imported as if it solved the full DAG**. The full DAG's partial-history method is still design work.

## 7. Source-method extraction, rivalry and counterevidence

**Ross, Pineau, Paquet & Chaib-draa, 'Online Planning Algorithms for POMDPs,' JAIR 32 (2008), https://pmc.ncbi.nlm.nih.gov/articles/PMC2748358/ — full HTML Sec. 2 / definitions and Bellman equations inspected.** Formal model: finite states, transitions, action/reward/observation kernels; history-dependent belief posterior (Eq. 2–4), and optimal belief-state action value (Eq. 8–9). Their paper reviews online planning and compares algorithmic approximations on POMDP tasks, not autobiographical memory. Methodological transfer: compute a belief reference from the permitted history; avoid state-truth labels. Limitation: their state-model and transition/observation laws are specified and exact POMDP solving is complex; our synthetic known likelihood removes that uncertainty. **This is primary methods-level support for the reference formalism, NOT project replication.**

**Kaelbling, Littman & Cassandra, 'Planning and Acting in Partially Observable Stochastic Domains,' Artificial Intelligence 101 (1998), https://doi.org/10.1016/S0004-3702(98)00023-X — publisher abstract/metadata inspected, full methods not re-reviewed in this run.** Peer-reviewed original POMDP framework, discusses finite-memory controllers and exact/approximate planning. Counterpoint to narrative necessity: compact controllers and beliefs can capture task-relevant history. No paper result on E001. Do not misrepresent abstract as an extraction of detailed methods.

**Littman, Sutton & Singh, 'Predictive Representations of State,' NeurIPS (2001), https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf — title/abstract inspected; PDF methods not systematically audited here.** Predictive state represents action-conditional future tests as a serious non-narrative alternative. The abstract states an expressivity result for a linear predictive representation relative to a minimal POMDP; do not assume a modern learned PSR is easy or optimal. This challenges any assertion that a stored causal episode graph is intrinsically necessary.

**Project-specific counterevidence:** [E001's full-diagnostic instrument](../E001-stage1-causal-commitments-v0.1.md) already admits a compact effect-matrix sufficient controller; the [H001 competing theories](../../dossiers/H001-autobiographical-memory/competing-theories.md) explicitly predict graph errors and expense can reduce performance. Both weaken simple arguments for graph superiority. No empirical evidence in this run resolves D001.

## 8. Forward decision table and what would genuinely falsify a claim

| Prospective outcome (NOT OBSERVED) | D001 disposition |
|---|---|
| Causal autobiography wins vs strong raw-history/retrieval/compact belief/predictive state at matched feasible resources, survives held-out families and causal-link ablation | Consider *scoped* graph utility, replication and E900 coupling test; no necessity or L3 claim |
| Exact/approximate compact state matches C within a preregistered equivalence margin or wins at lower resource cost | Prefer compact state in tested scope; reject representation necessity only within that scope |
| Graph advantage disappears under fair history serialization, or sham edges do as well | Reject asserted mechanism benefit in tested scope, audit information leakage |
| Mixed/imprecise result | DEFER, not equivalence |
| Reference uses private sampled theta, feedback after deadline, or unaccounted prior/censoring | INVALID comparison; freeze nothing, repair oracle |
| Model/prior shift changes policies | Report sensitivity, consider robust criterion; do not silently select a favorable prior |

**Strongest falsifier of the immediate method:** exhibit two private worlds with the same permitted h but distinct prescribed *unique* actions from the history-only reference, without any stated prior/likelihood difference; or identify a conditioning variable in the code that reveals theta, late feedback or withheld generator state. That would show oracle leakage or incoherence. **Known weak point:** the code hardcodes uniform prior and trustworthy signal q, so this is not a validated model-misspecification benchmark.

## 9. G0 admission checklist and exact next task

- [x] Private/public information boundary specified conceptually; public prior/likelihood and cost policy distinguished from latent simulator truth.
- [x] Finite Bayes and optional robust reference objectives written with assumptions; tied actions handled.
- [x] Identifiable and ambiguous latent-world pairs and noisy/delayed cases analytically demonstrated.
- [x] Minimal exact-arithmetic calibration executed with reproducible source and 16 checks.
- [ ] Extend the actual seven-node CausalWorkshop to emit only selectively requested, possibly noisy feedback with explicit censoring/dropout and commitment/probe budgets; validate how an admissible *set of models* is obtained without reading its private graph.
- [ ] Compare enumeration/approximation strategies for tractability and feasibility, with state-space scaling costs; specify misspecification and hidden-confounding controls.
- [ ] Fix target populations, family splits, outcome estimands and all scored-trial budgets/statistical registration *before* G2; independent validity review remains pending.
- [ ] Instrument real model process reset, allowed persistent-state checksum and observation-history parity across agents.
- [ ] Decide and document whether prior-robust evaluation is a co-primary criterion; unannounced prior selection would undermine the reference.

**Verdict:** RESEARCH_NOTE with observed local mathematical calibration. E001 G0 remains OPEN; D001 DEFER/CURRENT, H001 CANDIDATE, A0 PROPOSED, A1 UNSELECTED, E900 NOT STARTED. Not a consciousness result.

**One next executable action:** write an E001 G0 v0.2 *selective-probe finite-world oracle* for a minimal 3-node subset of CausalWorkshop, preserving an explicit nonempty version space over hidden graphs and a public event queue. Input: current seven-node source, this v0.1 allowed-history contract, seedable small graph set. Output: new versioned source + unit tests with at least one ambiguous and one separating intervention history, no private graph access in the action scorer, explicit time deadline and censoring tests. Stop when the same public history yields the same posterior/action set independent of evaluator's private sampled graph, or report a reproducible counterexample. Do not close G0 or score LLMs during this step.

## 10. E900 integration relevance and ethics

If a future E001 comparison supports one representation, a proposed E900 intervention would damage a recorded own-action-to-consequence link while holding user-visible observations, resource budgets and goal inputs fixed; compare later goal selection/action repair against a compact-state persistent rival and a sham intervention. A difference is only cross-function causal evidence within an approved experimental setting, NOT sufficient proof of a single mind. No real user data, persistent autonomous agent, sentience claim, production Anjo change or welfare-relevant experiment was undertaken.
