# Research operating protocol v0.3 — decision-centered

## Each manual or scheduled cycle

Follow [research-cycle.md](research-cycle.md) as the operative sequence: restore live state/dependencies and verify relevant capabilities → select one ready decision → discriminate/research/test → review → bounded decision/reusable delta → artifacts first/state last → one executable handoff. [Decision](decision-register.md), [asset](asset-register.md) and [work](research-records.md) registers carry compounding memory. Scientific gates below remain authoritative; governance and checkpoints do not promote them.

Functional consciousness is an operational L2 target, not L3 verification. A decision names its rival, intervention, outcome-to-action mapping and E900 coupling consequence. After three substantive unchanged blocker attempts, record reassessment before attempt four. Choose by decision impact, uncertainty reduction, feasible tools/dependencies and costs; ready independent streams need not wait for E001.

## Active research time budget (40-minute target; runtime enforcement pending)

**Schedule:** one start per hour. **Desired work:** at least 40 minutes of active investigation per iteration, leaving approximately 20 minutes for handoff/recovery. This is a target, **not a guaranteed capability of a ChatGPT Scheduled Task**. The scheduler only sets trigger cadence; it does not expose a reliable minimum-run-duration control to this protocol.

### High-effort research contract

Do not treat one literature summary as a completed research cycle. Within the actual available runtime, pursue this sequence, adapting time spent to the blocker rather than mechanically writing four essays:

1. **Restore and specify:** read the canonical state, inspect the latest verified artifacts, identify one decision whose outcome could change a theory or architecture.
2. **Triangulate and attack:** interrogate primary research methods/results, find conflicting evidence, and identify at least one genuinely competing simpler implementation or theory, not a straw man.
3. **Build or falsify:** derive predictions and controls; when execution is authorized, construct/tests small reproducible artifacts. Record failed experiments and impossibility/identifiability arguments, which are substantive advances.
4. **Independent critical audit and handoff:** check for data leakage, alternative explanations, overclaiming, cost parity, confounding, and possible welfare/ethics concerns. Version the evidence and decision artifacts and update the state LAST.

Where clock readings and logs are accessible, record **start UTC, end UTC, elapsed minutes, periods of real research work, checkpoint artifacts and limitations**. Never infer elapsed minutes from prompt size, claimed tokens, or number of tool calls. Never sleep/idly wait merely to meet 40 minutes, invent start/end times, or say a short execution lasted 40 minutes. When the runtime terminates early, log `DURATION_NOT_ENFORCED`, actual measured duration if known (otherwise `UNKNOWN`), remaining open work and next precise step. Do not advance a science gate without its exit criteria. A legitimately short completed subtask may be recorded honestly; it must not masquerade as a 40-minute research session.

### Requirement for a *guaranteed* 40-minute run (not enabled)

Guaranteeing a timed execution requires a separately deployed **durable, externally controlled research worker**, not merely stronger wording in the ChatGPT task prompt. An approved implementation would have:

- A monotonic clock and 40-minute *active-work target*, with deadline around 55 minutes to avoid overlap; one job per hourly slot, concurrency lock, checkpoint/resume, and per-stage work logs.
- Research-model and tool API integration configured explicitly, with real invocation accounting, model/version audit, evidence provenance, retry/backoff and failure handling. No dummy idle loop should count toward active work.
- GitHub compare-and-swap commits, append-only iteration outputs, crash recovery, experiment reproducibility checks, controlled code execution and bounded write permissions.
- Budget/kill-switch limits for API spending, inference and repository runner time, plus approval for any autonomous experiments or potentially consequential actions.
- Separate measurement of wall-clock runtime, active tool/model work, idle periods and quality gates.

**Operational status:** No GitHub Actions cron workflow, paid API daemon, self-hosted background service, or guaranteed 40-minute job is enabled by this protocol. Hosting in this private repo on GitHub-hosted Actions may consume substantial billable runner minutes and model API usage; obtain explicit budget approval before activation. Scheduled ChatGPT remains a best-effort research trigger until a true runner is configured.

### Gate exit criteria

| Gate | Exit |
|---|---|
| G0 Operationalize | Metrics with definitions, baselines, target populations/environments and leakage risks |
| G1 Theory | At least two competing mechanisms make mutually distinguishable predictions |
| G2 Preregister | Control + intervention + ablation, trial design, sample/seed plan, metrics, thresholds, stop rules |
| G3 Implement | Executable code, stable datasets/seeds, smoke tests and instrumentation |
| G4 Evaluate | Actual logs, effect sizes, uncertainty, failure cases, reproducible comparison |
| G5 Synthesize | Explicit accept/revise/reject/defer decision and next architecture version |

Advance gates only after their exit criteria. The program may iterate across G1–G4 repeatedly. Synthesize after eight new distinct valid accepted contributions or a major validated finding/pivotal invalidation. Track contribution IDs and milestones using [research-records.md](research-records.md); legacy stored iterations do not trigger accepted-science milestones.

### Additional system-level validity requirements

- Treat L1 interactive credibility, L2 causal cognitive integration and L3 possible phenomenal experience as separate reporting categories. No synthetic agent, self-report, simulated pain or emotionally persuasive speech establishes L3.
- Integrated-entity claims need **within-agent longitudinal intervention** evidence: state audit, goal/memory/self/world/affect dynamics, reboots/pauses, selective ablation and matched reactive/retrieval/simpler baselines.
- A 90-day evaluation must denote actual calendar days, uptime and downtime; accelerated simulated days are labeled as such. Never claim continuous processing without real execution traces.
- Record boundary-respecting social behavior, privacy/consent, non-manipulation and reversible autonomy as gated outcomes, not marketing claims.

### Evidence grading

- **E0**: exploratory proposal or uncited conjecture
- **E1**: direct verified source with reported findings, but unreplicated in project
- **E2**: result independently reproduced in project with valid controls
- **E3**: replicated across tasks, environments and/or independent groups

E0–E3 are *evidence provenance levels*, not probabilities of consciousness. Report confidence separately as low / medium / high with reasoning.

### Required record transaction

Use unique dated work IDs and kind/verdict fields from [research-records.md](research-records.md). Preserve legacy runs and `latest_verified_iteration: 004` as historical persistence; no inferred scientific acceptance. Commit artifacts/index/decision/asset changes first; write state LAST referencing the artifact commit and read back final publication. Reconcile SHA conflicts without force pushes. Resume artifacts-ahead-of-state transactions once, without duplicate execution or counting. A file cannot contain its own final commit hash. Missing writes means NOT_COMMITTED and self-contained delta; canonical counts unchanged.

### Model and infrastructure

Use strongest reasoning capability that is confirmed available in the runtime. Do not assert a specific model is selected without inspection. True multi-agent work, external execution and cross-run GitHub writes require verified tool access. Scheduled ChatGPT Tasks do not constitute a continuously running process.

### Quality and ethics

Track experiment execution costs, privacy exposure, model-vendor terms, intervention safety, and possible artificial welfare issues. Halt escalation if the ethics gate is unresolved; preserve safety controls as independent from any personalized mind architecture.

## Mandatory tools and current publication contract

No named external skill framework is required. Verify sources, actual execution, GitHub writes and independent review separately. Missing execution means NOT_EXECUTED/BLOCKED_ON_EXECUTION; missing separate reviewer means SELF-REVIEW_ONLY. Missing indispensable inputs blocks that task, not feasible independent research. Never claim unavailable capabilities.

Consult [quality gate](research-quality-gate.md), [publication standard](publication-standard.md), [Atlas](atlas/README.md), active dossier/experiment, and [review protocol](review-protocol.md). Substance, causal validity and rival discrimination determine acceptance; storage and passing toy tests do not. Evidence/dossiers and experimental artifacts first, work index/log next, state last. Record asset reuse, decision delta and stale dependencies. Invalid pivotal evidence flags direct/transitive dependent decisions and assets for reassessment; block dependent promotion until reviewed justification is current.

Deep synthesis and attention allocation use separate rules in the work index. Governance-only work changes no scientific gate/iteration or architecture; preserve E001 G0, all untested candidates, E900 not started and unresolved L3. No scheduler edit, paid runner or guaranteed-duration claim follows from this protocol.
