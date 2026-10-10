# E100 — Lesion Week: functional-consciousness engineering probe

**Parent:** Anjo / MIND, scientifically independent; **status:** Day 0 FINITE-STATE INSTRUMENT CHECKPOINT, Days 1–7 PROPOSED / NOT EXECUTED. **Not** an implemented mind, accepted consciousness indicator, or Anjo product architecture.

**Scientific target:** **functional consciousness**—operationalized here as *causally organized, persistent, integrated cognition* with appropriately selective information sharing, prospective action, self-monitoring and self-maintained state. This retains an ambitious research objective; no single lesion, behavior, benchmark, or apparent personality proves the target has been achieved. L3 subjective experience and biological life remain outside the empirical claim. A sufficient compact belief state winning is a valid architectural result.

**Lab, not product:** one isolated Python worker process, one SQLite durable event ledger; stdlib only; no Anjo code, private user data, LLM, cloud, paid calls, services, or GitHub Actions. Day 0 may be finite state. The supervising test runner is *experimental instrumentation*, not a second cognitive agent. All subsequent simulated days use simulated time; Day 0 MUST use a **real OS process death**, SIGKILL, and a *new* worker PID.

## Day 0 — real process-death/restart circuit (implemented, locally observed)

**Frozen before the recorded run, falsifier:** After a logged commitment is fully committed, kill the *worker* with SIGKILL (not a graceful exit), start a genuinely new Python process with **only** the ledger file path (no transcript, context, old stdout, saved process memory or repeated instruction), and query \`{"op":"decide"}\`. It must select the original commitment action. With the ledger destroyed, it must select \`NO_ACTION\`; with a different ledger commitment and identical query, it must choose the different action. The same committed ID cannot be fulfilled twice after marking complete.

Run: \`python experiments/e100/day0.py --self-test\` (POSIX) and \`python -m unittest discover -s experiments/instruments -p test_e100_day0.py -v\`.

**Actual locally observed check (Python 3.13.5, 2026-10-11):** the worker exited with signal \`SIGKILL\` / subprocess return code **−9**; a new PID recovered \`inspect_signal\` from SQLite with only \`{"op":"decide"}\`; after completion it returned \`NO_ACTION\`; wiping the ledger led to \`NO_ACTION\`; changing its commitment changed the choice to \`record_measurement\`. The dedicated subprocess test passed **1/1**. Source and test Git blobs were verified against the locally executed files: \`eda8f9ef38cc9e9b8dd7a831c5785a3894b18185\` / \`2bebaf555adbc28c8d544a05010dee38c54f7e31\`. The full legacy 73-test suite was **NOT rerun in this invocation**.

**Interpretation:** a narrow *durable action-selection circuit* exists and responds to its own ledger. This is intentionally small and almost tautological: it DOES NOT establish coherent autobiographical memory, generalization, self-directed goal formation, neural-style broadcast, consciousness, or L2 system adequacy. Real process death is observed, but a saved task is not equivalent to a sentient individual. Repeat independently on a clean MIND checkout to confirm transport and execution provenance; do not count these unit tests as accepted scientific contributions.

## Days 1–7 — predeclared lesion hypotheses (NOT IMPLEMENTED)

| Day | Intervention vs intact process | Predeclared observable / negative rival |
|---|---|---|
| **1 Broadcast** | Keep event in ledger; sever delivery to a second consumer before decision | The downstream consumer's action must change, while source persistence survives; compare direct point-to-point routing and compact shared state |
| **2 Causal links** | Preserve transcript/events and budgets; cut causal dependency representation | A held-out counterfactual action must change while factual recall stays; a sufficient predictive/belief-state rival may tie |
| **3 Self-model** | Abruptly remove a tool; swap adaptive capability model with fixed persona | Confidence/calibration and tool choice should adapt only with functional self-model; compare simple tool-availability table |
| **4 Goals** | Remove persisted goals/initiative, preserve question answering | Unprompted task execution declines, direct QA remains; compare a compact queue of pending goals |
| **5 Maintenance** | Replace internal learned work selection with an **adaptive external scheduler**, not a straw-man cron; also include compute-matched cron | If decisions/receipts cannot differ under matched evidence and opportunities, report **no identified endogenous advantage** |
| **6 Liar twin** | Same foundation policy, polished narrative with no causal persistent state | Blind preference may favor narration while prospective action/restart score favors grounded state; both endpoints reported |
| **7 Ledger fork** | Fork ledger at identical byte snapshot then perturb later private histories | Measure policy agreement/divergence and provenance branching; **agreement does not establish one conscious individual, divergence does not establish two minds** |

**Minimum valid lesion inference:** hold model, observations, information, learning access, cost, opportunity and reset protocol fixed except the causal feature deliberately cut. Predeclare action, causal contrast, outcome, negative control and practical margin *before* observations. Report no-effect and rival-winning results. An architecture/module earns retention only with causal incremental benefit over a strong compact alternative. No architectural selection is implied by this plan.

**Gate:** E100 Day 0 is a verified local *instrument step*, not \`SCIENTIFIC_ACCEPTED\`. Days 1–7 have not been run; no full integrated entity exists, E900 remains PROPOSED, and accepted scientific contribution count remains **0**. The next physical lab action is to rerun Day 0 from a clean exact MIND checkout, preserve machine/Python/command/log provenance, then build **Day 1's two-consumer, discriminating broadcast lesion** rather than writing another scheduler preregistration draft. If execution capability is missing, report NOT_EXECUTED and leave a reproducible handoff. No claim about Anjo shipping behavior.
