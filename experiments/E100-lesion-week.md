# E100 — Lesion Week: functional-consciousness engineering probe

**Parent:** Anjo / MIND, scientifically independent; **status:** Day 0 real-death circuit reproduced externally; Day 1 BROADCAST LESION LOCALLY EXECUTED (deterministic instrument); Days 2–7 PROPOSED / NOT EXECUTED. **Not** an implemented mind, accepted consciousness indicator, or Anjo product architecture.

**Scientific target:** **functional consciousness**—operationalized here as *causally organized, persistent, integrated cognition* with appropriately selective information sharing, prospective action, self-monitoring and self-maintained state. This retains an ambitious research objective; no single lesion, behavior, benchmark, or apparent personality proves the target has been achieved. L3 subjective experience and biological life remain outside the empirical claim. A sufficient compact belief state winning is a valid architectural result.

**Lab, not product:** one isolated Python worker process, one SQLite durable event ledger; stdlib only; no Anjo code, private user data, LLM, cloud, paid calls, services, or GitHub Actions. Day 0 may be finite state. The supervising test runner is *experimental instrumentation*, not a second cognitive agent. All subsequent simulated days use simulated time; Day 0 MUST use a **real OS process death**, SIGKILL, and a *new* worker PID.

## Day 0 — real process-death/restart circuit (implemented, locally observed)

**Frozen before the recorded run, falsifier:** After a logged commitment is fully committed, kill the *worker* with SIGKILL (not a graceful exit), start a genuinely new Python process with **only** the ledger file path (no transcript, context, old stdout, saved process memory or repeated instruction), and query \`{"op":"decide"}\`. It must select the original commitment action. With the ledger destroyed, it must select \`NO_ACTION\`; with a different ledger commitment and identical query, it must choose the different action. The same committed ID cannot be fulfilled twice after marking complete.

Run: \`python experiments/e100/day0.py --self-test\` (POSIX) and \`python -m unittest discover -s experiments/instruments -p test_e100_day0.py -v\`.

**Actual locally observed check (Python 3.13.5, 2026-10-11):** the worker exited with signal \`SIGKILL\` / subprocess return code **−9**; a new PID recovered \`inspect_signal\` from SQLite with only \`{"op":"decide"}\`; after completion it returned \`NO_ACTION\`; wiping the ledger led to \`NO_ACTION\`; changing its commitment changed the choice to \`record_measurement\`. The dedicated subprocess test passed **1/1**. Source and test Git blobs were verified against the locally executed files: \`eda8f9ef38cc9e9b8dd7a831c5785a3894b18185\` / \`2bebaf555adbc28c8d544a05010dee38c54f7e31\`. The full legacy 73-test suite was **NOT rerun in this invocation**.

**Interpretation:** a narrow *durable action-selection circuit* exists and responds to its own ledger. This is intentionally small and almost tautological: it DOES NOT establish coherent autobiographical memory, generalization, self-directed goal formation, neural-style broadcast, consciousness, or L2 system adequacy. Real process death is observed, but a saved task is not equivalent to a sentient individual. Repeat independently on a clean MIND checkout to confirm transport and execution provenance; do not count these unit tests as accepted scientific contributions.

## Days 1–7 — planned lesions (Day 1 locally instrument-tested; Days 2–7 NOT IMPLEMENTED)

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

**Gate and active next action:** E100 Days 0–1 have been exercised as deterministic instrument checks; neither is `SCIENTIFIC_ACCEPTED`. Days 2–7 remain NOT EXECUTED; no integrated entity exists, E900 remains PROPOSED, and the accepted-contribution count remains **0**. Day 0 has an external clean-clone reproduction report, but the full integrated regression was NOT rerun in this invocation. The sole next experimental lesion is **Day 2 causal memory**, preserving raw events while ablating links; compare a compact sufficient belief-state rival. No Anjo product transfer.

## Day 1 — action-changing broadcast lesion (locally executed, exploratory)

**Predeclared exact action contrast, not an externally frozen trial:** An isolated finite-state worker uses **one SQLite ledger per experimental arm**, with (i) an immutable source event for a sensor-tool outage, (ii) a source-stored commitment to inspect a signal, and (iii) two event consumers: an **observer** and a **planner**. The worker sends the outage event to both consumers in the intact arm. The experimental lesion cuts **only the event → planner inbox delivery**, leaving the source row and observer's receipt intact. All arms run with the same deterministic worker policy and source records; the runner is a supervisor, not another cognitive agent. The worker is really SIGKILLed after commit/broadcast and a fresh worker resumes from its own ledger path. No transcript is provided to the resumed decision call.

**Expected observations before run:** intact routed planner `DEFER_SENSOR_SCAN`; cut routed planner `SCAN_WITH_SENSOR`; *identical* source rows and observer inbox in both arms; a no-outage/unrelated clock tick must not change the action in either route configuration; a **compact direct source-state reader** must match the intact planner even if broadcast is cut. Any mismatch falsifies this toy instrument.

**Observed in local isolated Linux/Python 3.13.5 execution (2026-10-11):**
- Intact planner: `DEFER_SENSOR_SCAN`. Planner-delivery lesion: `SCAN_WITH_SENSOR`.
- Source rows byte-equivalent in semantic content across arms, including stored commitment and outage; separate observer receipt **identical**.
- Compact direct ledger-state policy on lesioned arm: `DEFER_SENSOR_SCAN` — **ties the intact routed policy**.
- Unrelated-clock-event controls in both delivery configurations: `SCAN_WITH_SENSOR` (no spurious action change).
- Each of the four arms killed its worker using POSIX `SIGKILL`, observed subprocess return `-9`, then a genuinely new worker performed the decisions. No old transcript supplied.
- Commands actually run: `python experiments/e100/day1.py --self-test` → PASS; `python -m unittest discover -s experiments/instruments -p test_e100_day1.py -v` → **1/1 PASS**; `python -m py_compile experiments/e100/day1.py` → PASS. The test succeeded after correcting two development defects (missing parenthesis and mistyped commitment event kind); failed intermediate local runs are not scientific failures.
- Executed file identity: source Git blob `bedfdd5da580bc6586d78a77566b202ffdd254b0`; unittest blob `9aaaf23e329879ab2778ad4ebb29f7ab78f802d2`; GitHub blobs **matched the exact executed local files**. The **complete repository regression suite was not executed** in this invocation.

**Strongest competing account and negative interpretation:** This effect is **by construction**: deny a consumer the outage notice and a rule that checks its inbox changes action. It shows *causal sensitivity to routing*, not that a broad global workspace is uniquely required. A one-bit public sufficient-state feature (the compact reader) ties the elaborate routed arrangement, and computation parity, generalization, learning, and useful downstream-world outcomes have **not** been evaluated. This is an exploratory synthetic instrument, **NOT** `SCIENTIFIC_ACCEPTED`, not achievement of functional consciousness and not support for L3. Neither broadcast necessity nor entity-scale integration is identified.

**Immediate next research action:** Implement **Day 2 causal-memory lesion**, holding the complete raw-event history, observations and budgets fixed while removing a *causal dependency representation*. Predeclare a held-out *future counterfactual action* and compare against a compact sufficient belief/predictive-state rival; stop if no differential prediction is identifiable. Avoid another protocol-only iteration. See [Day 1 local work record](../runs/2026-10-11-E100-day1-broadcast-local.md).
