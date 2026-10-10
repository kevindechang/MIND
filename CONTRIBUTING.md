# Contributing research to Anjo / MIND

MIND is an **Anjo-sponsored, scientifically independent** research effort. Product specs in Anjo bind the **product**; they are not proofs of the research hypotheses, and MIND does not choose a replacement production architecture.

## Start / ownership
1. Given "go", follow [GO.md](GO.md), not an agent-specific implicit plan. Read live `main` HEAD, state and open issues/PRs.
2. Prefer a ready issue in [TASKS.md](TASKS.md). Comment with task ID, **specific file scope**, expected discriminating deliverable and intended branch; check for active claim/PR again. Comments are advisory, **not a distributed mutex**. If duplicated, do not commit conflicting edits.
3. Create `research/<issue>-<slug>` from live main; one branch/PR per scientific question. Never force push main. When write tools do not support branches/PRs, use a collision-safe new artifact path if authorized or return NOT_COMMITTED; do not bypass the safety protocol.
4. Keep human/agent review provenance explicit. Multiple model voices in one context are **not independent reviewers**. Do not conflate activity time with wall-clock or network latency.

## Scientific submission
A contribution needs: question, target decision, source versions and inspection depth, strongest viable baseline (including belief-state/external learned controller), null and alternative predictions, falsifier, negative controls, budget/observability parity, method and failures, precise result/uncertainty, limitations, and one next executable action. Prefer smaller decisive counterexamples and negative findings over long speculative essays.

- `OBSERVED` means this agent saw execution/result; `PAPER-REPORTED` records somebody else's; `PROPOSED` is not evidence; `NOT_EXECUTED` is explicit. Label research L1/L2/L3 separately.
- Draft designs are **not preregistered or scored**. Freeze a versioned plan before generating scored results. No silent held-out leakage or use of private simulator truth as agent input.
- A clean test suite supports executable integrity, **not** memory efficacy, endogenous cognition, digital personhood or consciousness.
- Do not consume paid model APIs, run GitHub Actions, access private Anjo user data, deploy production, self-modify unrestrictedly or contact external humans without separate consent.
- Anjo product transfer requires distinct design/security/privacy/release approval. State `NOT_READY_FOR_PRODUCT_TRANSFER` by default.

## Merge and serialization
- Submit a PR with issue reference, changed-file list, exact commands/logs (or NOT_EXECUTED), source references, scientific verdict and unresolved falsifier. Avoid modifying `research-state.md` directly on parallel working branches unless the PR clearly marks a **proposed** delta and a single integrator owns reconciliation.
- A designated integrator (human or one explicitly authorized agent with exclusive write ownership) rereads live main, checks no duplicate work ID, and merges under current HEAD. Publish artifact and research-record/index **before** `research-state.md` LAST, linking an immutable artifact commit; read back. Rebase/review conflicts; never force push or count failed commits as completed work.
- No accepted science from PR approval alone. Apply [research-quality-gate.md](research-quality-gate.md); annotate failed pivotal evidence and dependent decisions instead of deleting history.
- Issue can be closed only when linked merged artifacts satisfy its explicit acceptance. Otherwise leave precise blocking status / next action.

## Agent adapters
`AGENTS.md` and `GO.md` are **the authority**. `CLAUDE.md`, `.cursor/rules/mind.mdc`, and `.github/copilot-instructions.md` are pointers only. Do not copy the full research runbook into multiple framework-specific prompts.
