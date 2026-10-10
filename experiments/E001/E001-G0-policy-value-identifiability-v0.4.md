# E001 G0 v0.4 — Adaptive probes and reachability non-identification

**2026-10-11 | D001/H001/B001/W1 | INSTRUMENT_VALIDATION | EXPLORATORY_CHECKPOINT | SHORT_RUN / DURATION_NOT_ENFORCED | SELF-REVIEW_ONLY.** E001 G0 OPEN, G2 UNFROZEN, no scored agent trials. Continuation of v0.1–v0.3. The [annex](E001-G0-policy-value-identifiability-v0.4-annex.md) contains source-method inspection, six analytical lenses and limitations.

## Formal model

Eight forward DAGs over nodes {0,1,2}, edges subsets of {(0,1),(0,2),(1,2)}. Public prior p(G), graph/node-specific censor probability c(G,n), commitments C=(goal,desired,penalty), deadline T, probe budget B, cost k and delays d. At most one probe is issued per tick before T; each has public event ID, node, issue and due ticks. At due tick <=T, either a deterministic reachability mask or a CENSORED marker is delivered, paired to its ID. Due-after-T feedback stays pending. Conditional on G and probe, censor draws are independent. Evaluator-private sampled G never enters the controller.

Terminal action a has at most two interventions, with XOR of their reachability masks and utility U(a,G,C)= -len(a) - sum of violated-commitment penalties (CausalWorkshop semantics). The estimand is **ex-ante expected net utility** of an optimal permitted-history policy, not hindsight true-graph success. State (t,b,q,r) comprises public tick, posterior, pending queue and remaining budget. At deadline V=max_a E_b U. Before deadline:

`V(t,b,q,r)=max_x [-k*1{x is probe}+sum_z P(z|b,q,x)V(t+1,Bayes(b,z),q',r-1{x is probe})]`

where x is WAIT or feasible PROBE(node,delay); z includes only statuses due at t+1. The [standalone exact Fraction source](../instruments/e001_finite_policy_v04.py) and [12 tests](../instruments/test_e001_finite_policy_v04.py) implement this finite-horizon reference, not an agent.

## Non-identification and counterexample

**THEORETICAL and locally enumerated:** graph index5={(0,1),(1,2)} and index7=index5 plus (0,2) have identical reachability signature **(7,6,4)**, hence identical probe masks and XOR utility for all plans/commitments. Under graph-independent or closure-class-dependent delivery, all adaptive probe policies produce the same public-history distributions. Eight DAGs yield **seven reachability-equivalence classes**. Direct-edge graph identity is not identifiable even with unlimited perfect reachability probes; a compact closure belief can be sufficient for the declared decision problem.

**Counterexample:** with graph-specific censor c(index5,node2)=1/4 and c(index7,node2)=3/4, a censored node2 probe shifts equal prior to (1/4,3/4) despite equal delivered masks. Terminal utility remains the same within that pair, but future observation delivery may differ. Therefore naive closure-only state is not universally sufficient under informative missingness; retain an observation-process predictive state.

## Observed local tests

Python 3.13.5 stdlib; no LLM calls. Source blob **5572e564ab3715f8c4c606ac9a8ef25866ef3e5c**, test blob **08471227fb85761432919f11dd61f0646ae4a601** match local git hash-object. `python -m unittest -v test_e001_finite_policy_v04` **12/12 PASS**; `python -m py_compile` both files exit0. Independent direct one-probe enumeration vs dynamic program: **128/128 seeded exact Fraction equalities PASS** (seed 11012026), not 128 empirical trials. Direct reference file is local only.

With commitments ((2,1,2),(0,1,8),(1,1,2)), prior (1,1,1,2,1,2,2,2), zero censor, T2, delay1, cost1/10: no-probe value **-7/3**, B1 **-121/60**, B2 **-47/24**, adaptive gain **7/120**. B2 first probes node0; second probes node1 only after mask5 (probability 1/4), otherwise waits. Synthetic acquisition value, **not** autobiographical-memory efficacy.

## Decision

Strongest rival: compact belief over control/observation state + commitments + queue + budget/time. Transcript/retrieval and predictive-state also remain unscored. D001 **DEFER/CURRENT**, H001 untested, E001 G0 OPEN, G2 unfrozen, E900 proposed, L3 unresolved. No independent reviewer. **Next:** run byte-exact integrated v0.2/v0.3/v0.4/legacy Python suites (14+20+12+10) and py_compile; stop at reproducible failure or verified parity. W2–W4 attention due next; this W1 continuation is an execution-critical exception.
