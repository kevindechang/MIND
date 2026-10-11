# H014: receiver selection versus the update rule

Date: 2026-10-11. Scope: self-model prediction on this organism's logged lives.
This implements the first experiment from the owner's approved research direction.
It does not implement the separate recurrent-transfer or internal-failure projects.

## Question and alternatives

Can a consumer learn how much to use memory and goals, beyond changing the learning
rule or choosing a fixed input filter? C030/C036 distinguish informative contents
from their net cost; H014 asks whether receiver-side selection can remove that cost.
Issue #33 supplies the important competing explanation: normalising every update by
feature count may itself create the cost. None of this tests phenomenal experience.

The self-model is extended with optional `step=normalised|sqrt|adagrad` and
`gate=all|no_memory|no_goals|no_memory_goals|bias|learned|uniform`. Defaults are unchanged.
AdaGrad uses coordinate-wise accumulated squared logistic gradients and epsilon 1e-8.
The fixed filters remove sources before feature deduplication. Bias removes all inputs.

The learned condition combines five online logistic predictors, one for each fixed
filter, using per-action exponential weights from cumulative **pre-outcome** Brier
loss (eta=1, uniform initial weights). All experts receive the same public outcome.
The uniform control trains the same five predictors, tracks the same losses and
computes the weights, but outputs the unweighted mean. This is a prediction mixture
over fixed masks, not neural attention, per-tick sparse routing, or compute saving.
Five experts cost more than one. Only learned-versus-uniform matches expert count;
winning against a single predictor does not establish efficiency or unique architecture.

## Primary tests, specified before inspecting pilot results

- **C050:** on vigil/dev, AdaGrad with all inputs improves late-half Brier over the
  current normalised self-model by more than **0.008**. This is the pre-existing C017
  scale / issue #33 suggested relevance bar, not a margin fitted to this experiment.
  Bias-only, sqrt, drop-memory and load-matched-sham contrasts are descriptive controls.
- **C051:** AdaGrad plus learned selection improves Brier by more than **0.002** over
  each of (a) AdaGrad/all, (b) AdaGrad/uniform, (c) the strongest fixed step/filter
  selected on eight dev seeds, independently per world. The primary measure is the
  equally weighted average of vigil/dev (300 episodes) and outage/silent (120 episodes),
  pairing by lifetime seed. 0.002 is half C018's 0.004 silent-outage relevance bar.
  Every contrast must clear its margin (intersection-union claim); individual
  intervals are not a simultaneous confidence region. No claim is made that every
  world improves. World-specific scores, normalised/learned, and normalised/uniform
  are descriptive. The fixed-rival selection rule minimises mean late-half Brier
  among {normalised, adagrad} times five fixed filters plus sqrt/all; ties are broken
  lexicographically. The initial plan listed ten fixed candidates; the pilot also
  evaluated sqrt/all and found it strongest in vigil. It is retained as the stronger
  rival before sealing, with no change to the hypotheses or relevance margins.
- **K14:** all step/gate options reproduce logged confidence in shadow replay and
  survive restore, including fresh processes with different Python hash seeds.

C050/C051 use 32 paired seeds and the repository's conservative paired bootstrap/t
intervals. Failure means an interval is wholly at or below the relevance margin;
crossing the margin is inconclusive. No tuning or margin change follows held-out data.
The pilot uses seeds 0..7 solely to check the implementation and select fixed rivals;
the full dev evaluation overlaps that selection set and is not independent validation.
Predictions and selected rivals are committed before any held-out evaluation. Every
held-out record, including failure, is committed unchanged. Negative results are useful.

## Identification and controls

Use one baseline organism ledger per world/seed, then replay each consumer on its
logged broadcasts, actions and outcomes. Parameter overrides affect the shadow only.
No alternative confidence affects the policy, workspace, or future event distribution.
Thus the primary endpoint measures prediction at fixed behaviour, not improved action,
autonomous control, cross-world transfer, or general functional consciousness.

The unfiltered original shadow must exactly reproduce every logged confidence (K09).
Prefix tests prevent dependence on later events. For memory shams, K10 verifies source
presence and feature load before filtering; shams and filters are distinct controls.
The current self-model excludes its own broadcasts from input; alternative expert
reports are not inserted into the baseline stream. Existing and new live replay tests
exercise the optional mechanism as part of the shared organism.

## Research basis and limits

- Duchi, Hazan & Singer (2011), *Adaptive Subgradient Methods for Online Learning
  and Stochastic Optimization*, [JMLR](https://jmlr.org/papers/v12/duchi11a.html).
  Abstract and full-paper section 1.1 / equations 1 and 5 inspected. Diagonal
  accumulated-gradient scaling motivates the optimizer control. Convex online
  learning results do not guarantee better performance under MIND's changing inputs.
- Freund & Schapire (1997), *A Decision-Theoretic Generalization of On-Line Learning
  and an Application to Boosting*, [author manuscript](https://www.schapire.net/papers/FreundSc95.pdf).
  Sections 2.1 and 3.1 inspected. Exponential reweighting motivates the mixture.
  Fixed eta=1 and late-half scoring are experimental choices; no new regret theorem
  or reproduction of the paper's experiments is claimed. Cumulative losses can
  respond slowly when the best source changes.
- Goyal et al. (ICLR 2022), *Coordination Among Neural Modules Through a Shared
  Global Workspace*, [paper](https://arxiv.org/html/2103.01197v2).
  Abstract and architecture broadcast/consolidation description inspected. Learned
  read access motivates H014, but this small logistic mixture is not their neural
  architecture and their results are not evidence about this organism.

## Execution and handoff

Run new tests and the full suite, seal claims, evaluate dev and sealed held-out seeds,
and re-record all existing claims because result code changed. Run doctor and regenerate
STATUS. Preserve seals using merge commits. Record this session as `Codex (H014 session)`;
machine-generated replication labels on old claims do not establish independent review.
Deliver the implementation, immutable records, research report, and a reviewable PR.
NOT_READY_FOR_PRODUCT_TRANSFER.
