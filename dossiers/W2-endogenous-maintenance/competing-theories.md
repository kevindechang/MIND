# W2 H005/H008 — Metareasoning Competition and Identifiability Matrix
**Status: PROPOSED comparative framework, not a completed controlled trial.**

| Arm | When work occurs | How work selected | Information permitted | Strongest vulnerability |
|---|---|---|---|---|
| A: dormant | Only on next user interaction | Prompt re-evaluation | All past serialized observations | No prospective update when time-sensitive changes occur |
| B: fixed periodic | Exogenous fixed schedule | Index/round-robin | Same live state when woken | May waste effort on low value |
| C: priority queue | Event trigger or fixed slot | Deadline/urgency heuristic | Same task values/deadlines | Can ignore uncertainty and action consequence |
| D: value-of-computation scheduler | Exogenous event trigger with same budget | Estimated expected improvement in future decision | Same state and estimates as E | Could be fully functionally equivalent to E |
| E: 'endogenous' controller | Self-chosen bounded updates | Internal estimate of gain/goal pressure | Same state and estimates as D | If D can emulate it, no architecture-specific benefit |
| F: shuffled-state E | Same E scheduling opportunities | Internal motive or state randomly permuted | Same public inputs | Reveals whether claimed regulatory coupling actually matters |
| G: oracle benchmark | Privileged evaluator | Hidden-world best | Hidden truth forbidden to A–F | Unfair as direct arm; diagnostic only |

## Key adversarial predictions

1. If E beats A/B but not D, the benefit is rational active computation, not a uniquely endogenous mechanism.
2. If E beats D only when given additional hidden information or tokens, claim a resource/observability advantage, not improved cognition.
3. If regulatory-state ablation F does not alter correct future policy, the claimed drive may be epiphenomenal.
4. If maintenance gains are overestimated, D/E may overinvest and lose to no-idle A or priority C.
5. If two systems have the exact same future action and verified state given every tested history, ordinary black-box observation cannot distinguish their internal scheduling implementations. Require controlled internal interventions or exact code/process traces.
6. Greater uptime, repeated background messages, user belief that a system 'cares', and a model's assertion that it 'thought while you were gone' do not prove self-originated goals or L3 subjective experience.

## Registration blockers

Environment event distribution, uncertainty model, actual model/policy variants, paired random seeds, compute/token budgets, state logging, true uptime logging, stop rules, effect floor and power are all unset. E002a is G0, not ready for G2; actual multi-policy AI experiment is NOT_EXECUTED.

Sources S013–S015: see [living synthesis](synthesis.md) and [project evidence ledger](../../evidence-ledger.md).