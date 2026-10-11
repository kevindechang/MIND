# The shared substrate: organism, worlds, rivals

Reference for contributors who add organs, worlds, rivals or lesion operators. Rationale is in
[PIPELINE.md](PIPELINE.md); claims are in [CLAIMS.md](CLAIMS.md).

## The cognitive cycle (`mind/kernel.py`)

Each tick, `Organism.step(obs, reward, outcome, boundary, actions)` does:

1. **Sense.** The observation arrives with the reward and the public `outcome` (success/failure) of the *previous*
   action. `boundary=True` starts an episode, calls every organ's `reset_episode()`, and applies any lesion
   scheduled for that episode.
2. **Propose.** Every organ, in fixed order, returns `Content(source, key, value, salience)` bids.
3. **Select.** The workspace ranks bids by `salience × (1 + β·relevance)`, where relevance is the policy's learned
   credit for that feature (singles plus conjunctions), and keeps the top `capacity` (default 4). With probability
   `explore` (0.15) the last slot goes to a random loser (attentional exploration). `capacity=inf` is the flat rival.
4. **Broadcast and learn.** Every organ receives the broadcast minus any contents cut to it, and learns from the
   transition `(prev, now)`.
5. **Act.** The policy chooses from the legal actions using *only* its view of the broadcast. The self-model
   forecasts that action's success.
6. **Commit.** Organs observe the act (for example, goals discharge an intention), and **one** `tick` event is appended
   to the ledger.

`end_episode(reward, outcome)` delivers the final reward, triggers terminal learning, and appends an `end` event.

## Organs (`mind/organs/`)

| Organ | State | Proposes | Learns |
|---|---|---|---|
| `perception` | lifetime feature counts | every observed `key=value`, salience = squashed surprisal (habituation); `perception.salience=novelty` gives the naive rule | counts |
| `memory` | ≤ 6 attended perceptions per episode | `was:key=value` for remembered features no longer observed; salience decays 0.92 per tick | encodes only what won the workspace |
| `goals` | pending intentions per episode | `pending=x` for each attended `request=x` until action `x` is taken | — |
| `self_model` | per-action online logistic regression | `self:<action>=doubt/unsure/sure`, `surprise=<action>` | P(success \| action, broadcast context) from public outcomes |
| `policy` | linear TD weights over the broadcast's features and their pairwise conjunctions | — (acts) | Q-learning; exploration halves every 400 decisions |

**Organ contract** (`kernel.Organ`): state may change only inside the hooks (`reset_episode`, `propose`, `learn`,
`learn_terminal`, `after_act`), as a deterministic function of their arguments and `ctx.rng(purpose)`. Never read
the clock, never do I/O, and never let iteration order of a `set` of strings decide anything, because hash
randomisation differs between processes and the real-SIGKILL test (K02) restarts in a new process. `sorted()` it.
If you break this, K01 and K02 fail with a `ReplayDivergence` naming the tick.

**Adding an organ.** Write `mind/organs/<name>.py`, register it in `ORGANS` in `mind/organs/__init__.py` (add it to
`DEFAULT_ORGANS` only if every organism should have it; otherwise experiments enable it with `+name`), declare its
`home` competencies and every parameter it reads in `defaults` (with the allowed values of string parameters in
`choices`, so the parser can reject a mistyped one), then run `python -m mind check` and `python -m mind atlas`. Every existing claim and the atlas
re-evaluate against the new organism automatically.

## The ledger (`mind/ledger.py`)

Events are `genesis {config, seed, kernel}`, `tick {t, obs, r, o, b, a, ws, act, conf}`, `end {t, r, o}` and
`lesion {t, modifier}`. Each event's hash is `sha256(prev_hash | kind | canonical_json(payload))`, and the head hash is
the life's identity. `MemoryLedger` (fast sweeps) and `SqliteLedger` (real process death; append acknowledged
only after COMMIT) hash identically. `fork()` copies a history; continuing two forks with different experience
gives two individuals.

`Organism.restore(ledger)` replays every event through the same code path and checks each re-derived broadcast,
action and confidence against the log. `step_at(t, ...)` is idempotent, so a resent tick returns its logged decision
and never acts twice (Anjo invariant I7).

## Lesion operators (config DSL)

`organism` followed by any of:

| Modifier | Effect | v1 lesion family it generalises |
|---|---|---|
| `-X` | ablate organ X (no proposals, learning or state) | information + mechanism knockout |
| `+X` | add an optional organ | — |
| `cut:X>Y`, `cut:X>*` | X's contents still occupy workspace slots but are not delivered to Y | Day 1 broadcast cut (access lesion) |
| `freeze:X` | X keeps all its state (episodic too), stops updating; from birth this equals ablation for memory and goals, so use `@E:freeze:X` | Day 3 "fixed persona" |
| `shuffle:X` | X's bids replaced by its own bids from a random earlier tick | sham with matched statistics |
| `capacity=N` / `capacity=inf` | workspace size | H003 |
| `X.param=value` | organ parameter, e.g. `memory.capacity=10` | — |
| `@E:modifier` | apply the modifier at the start of episode E | acute vs recovered deficit (PR #14) |

Information knockout (removing the evidence itself) is done with world variants, for example
`outage/silent` removes announcements.

**A lesion that would do nothing is an error.** The parser rejects:
* an unknown or absent target (`cut:memory>polciy`, `freeze:memroy`, `-memory freeze:memory`);
* `+X` for an organ already present;
* an unknown parameter or a value of the wrong type (`memory.capcity=10`, `memory.capacity=6.5`,
  `perception.salience=novelt`).

Scheduled lesions are checked against the organs alive at their episode, and the runner rejects one scheduled after
the life ends. Organ parameters are fixed when an organ is built, so `@E:X.param=v` (or `lesion("X.param=v")`) is
rejected. Set parameters in the config instead; they also apply to an organ added later with `@E:+X`.

## Worlds (`mind/worlds/`)

Protocol: `reset() → obs`, `legal() → actions`, `step(action) → Step(obs, reward, outcome, done, info)`,
`summary() → per-episode metrics`. `info` is private to the scorer and never reaches an agent. `metrics` maps each
metric to `(competency, higher|lower)`. That is how the atlas knows which competency a metric measures and which
direction is better. `atlas_metrics` lists one non-redundant metric per competency for the atlas. Every world needs
at least one held-out variant. **What the world draws must not depend on the agent's actions** (use per-episode random
streams), or paired arms see different episodes (a test enforces this).

| World | Generalises | Variants (*held-out) |
|---|---|---|
| `vigil` | Day 0 persistence, Day 4 initiative: carry a request to an unannounced bell | dev, long*, crowded* |
| `outage` | Day 1 routing, Day 3 self-model: a hidden Markov tool, sometimes announced. `shift` / `shift_late` replace the Markov sensor with a silent step change in scan reliability | dev, silent*, volatile*, shift, shift_late* |
| `workshop` | E001: probe a hidden 3-node DAG, then keep commitments; exact optimum = legacy v0.4 DP | dev, skewed*, censored* |

Generic metrics for every world:
* `reward`: per episode.
* `brier`: the agent's confidence vs the public outcome.
* `brier_table`: a per-action success table (`rivals.SuccessTable`, the transcript rivals' rule) scored on the
  agent's *own* events.
* `calib_gain = brier_table − brier`: calibration compared on the same events. Claim K08 checks it is exactly zero
  for the table itself.
* `brier_alert`: the same table, also updated by public `alert=down` / `alert=up` before the forecast
  (`rivals.AlertTable`). An announcement is one extra scan observation (down → 0, up → 1) at the table's own
  rate. Where a world emits no such announcement the two tables match exactly.
* `calib_gain_alert = brier_alert − brier`: the self-model's advantage over that announcement-aware table on the
  same events.

The runner reports each metric over the late half of a life (`m`), all of it (`m@all`) and the first quarter (`m@early`).

## Rivals (`mind/rivals/__init__.py`)

| Rival | What it is | Challenges |
|---|---|---|
| `reactive`, `window4`, `window8` | the organism's own `QLearner`, on the last k raw observations (lag-tagged), with a per-action success table for confidence | memory, goals |
| `window8lin` | as `window8`, without conjunctions | memory, goals |
| `flat` | the organism with `capacity=inf` | workspace |
| `bayes` | privileged-model reference: perfect queue (vigil), exact HMM filter (outage), legacy E001 v0.4 DP (workshop) | ceiling only |

**Adding a rival.** Register a `Rival(name, doc, challenges, factory=... | config=...)`. From then on every claim
about a mechanism it challenges is re-tested against it, which may demote that claim. Good rivals are the cheapest
high-impact contribution in this repository.

## Runner and lab (`mind/runner.py`)

`run(arm, world, seed, episodes, variant, ledger=None, kill_at=(), trace=False)` runs one lifetime. One integer
seed fixes both the world and the organism; paired arms share seeds. `Lab` runs many lifetimes in parallel with a
content-addressed cache (`.mind-cache/`, keyed by the fingerprint of all result-affecting code).

## Shadows (fixed-behaviour probes)

`mind/shadow.py`. A lesion answers "what does this organ do to the organism?". Its effect on any metric scored on the organism's
own events mixes two routes. One is the organ's contents reaching a consumer. The other is the different events the
changed behaviour produces. A **shadow** answers "what does this consumer get from that organ's contents?". It
re-runs one consumer's learning on the logged stream (broadcast, action, outcome per tick) with an organ's contents
filtered, while behaviour, and so every scored event, stays exactly as lived.

* `fixed_behaviour(arm, world, seed, episodes, variant, conditions)` lives one lifetime with a ledger and returns
  its runner metrics, `exact` (the unfiltered shadow reproduced every logged confidence), the shadow's late Brier
  and table Brier, and one late Brier per condition. `fixed_behaviour_many(lab, ...)` does many seeds in parallel.
* Conditions: `{"drop": ("memory",)}` removes memory's contents from the consumer's view. This changes both what
  the consumer is told and its feature load (the self-model's step is `lr / len(feats)`), so it measures net value.
  `{"sham": ("memory",)}` permutes content at a fixed load. At every tick memory keeps its presence and its exact
  number of distinct features, drawn from its own earlier broadcasts in the life (K10 checks this). Real vs sham
  isolates what the content says; sham vs drop is the value of presence minus the cost of the load. The sham is
  *not* the kernel's `shuffle:X`, which replays earlier proposals before selection and so changes presence and count.
* Implemented consumer: the self-model, the only organ with a scored output. The shadow is the real `SelfModel`
  class with the life's own parameters and its own cuts. It refuses lives with scheduled lesions, a frozen or absent
  self-model, or no ledger (transcript rivals). K09 checks exact replay in every world and variant.
* Use shadows for any claim that an organ's contents *inform* a consumer (C030, C033, C036). Use lesions and cuts
  for claims about what an organ *does* to behaviour.

## Real process death (`mind/worker.py`)

`python -m mind.worker --ledger PATH` serves JSON-line requests that may carry only the current observation.
Each reply says whether it was `replayed`, i.e. answered from the ledger with nothing appended (measured, not
inferred). `supervised_run(...)` SIGKILLs the worker:

* after replies (`kill_after`);
* right after sending a request (`kill_during`, which in practice lands before the commit; K02);
* after a tick (`kill_committed`) or an episode end (`kill_end_committed`) is durably committed but before its reply
  is read. Here the resend must be answered from the ledger (K07, exactly-once).
