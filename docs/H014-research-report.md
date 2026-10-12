# H014: better prediction from the update rule, without a selection advantage

Research conducted 2026-10-11–12 by `Codex (H014 session)`. Predictions sealed in
`04008e6`. Result-code fingerprint: `026d2e01a8f57715`.

## Finding

AdaGrad reduced the self-model's prediction error on fixed vigil event streams.
The learned mixture of input filters did not add value beyond the strongest
single predictor. It beat an equally sized uniform mixture, but lost to simpler
controls. MIND therefore has a useful optional optimizer and a recorded negative
result about this particular receiver-selection mechanism.

These findings concern prediction on this organism's logged actions and outcomes.
They do not establish improved policy control, transfer to new task families,
general functional consciousness, or phenomenal experience. Product transfer
remains `NOT_READY_FOR_PRODUCT_TRANSFER`.

## Registered outcomes

Both empirical claims use 32 paired seed-level observations per evaluation. C050
uses one baseline lifetime per seed; C051 averages two world-specific lifetimes
per seed (64 baseline lifetimes total). Positive Brier gain means the treatment
predicts better. Intervals are the repository's conservative
95% bootstrap/t intervals over independent lifetime seeds.

| Test | Dev gain [95% interval] | First sealed held-out gain [95% interval] | Registered outcome |
|---|---|---|---|
| C050: AdaGrad/all versus normalised/all, vigil/dev; margin > 0.008 | +0.0168 [+0.0140, +0.0197] | +0.0171 [+0.0149, +0.0193] | HOLDS; PREREGISTERED |
| C051: learned versus AdaGrad/all, equal average across vigil/dev and outage/silent; margin > 0.002 | −0.0015 [−0.0019, −0.0012] | −0.0013 [−0.0017, −0.0008] | FAILS |
| C051: learned versus AdaGrad/uniform; same endpoint and margin | +0.0128 [+0.0122, +0.0134] | +0.0129 [+0.0121, +0.0136] | HOLDS for this contrast |
| C051: learned versus strongest fixed predictor selected on dev; same endpoint and margin | −0.0019 [−0.0031, −0.0007] | −0.0027 [−0.0035, −0.0019] | FAILS |
| K14: all 21 options, shadow/restart/process replay | 126 lives, zero failures | 126 lives, zero failures | HOLDS; PREREGISTERED |

C051 requires all three controls to be beaten. Its conjunction is **REFUTED**.
The favourable uniform contrast does not rescue the claim. The first held-out
failure is preserved; its prediction and margin have not been changed.

On C050's held-out seeds, mean Brier fell from **0.05890 to 0.04178**, a **29.1%**
relative reduction. This is a reduction in squared probability prediction error,
not a 29.1% increase in task success or a pure calibration statistic.

## Why this experiment is informative

Previous MIND results showed that memory contents can be informative yet have a
negative net effect on prediction when extra features dilute a normalised update.
The experiment explicitly tested the simpler learning-rule explanation before
claiming an architectural advantage for learned selection.

All shadow conditions consume the baseline organism's identical broadcasts,
actions and public outcomes. Changing a shadow cannot affect later observations
or action selection. This avoids comparing forecasters on different event mixes.
K09 checks exact baseline replay; K10 checks the memory content sham's presence
and feature count. Bias-only conditions distinguish contextual benefit from merely
adapting action base rates.

The learned condition trains five fixed-filter logistic models and combines their
predictions using per-action exponential weights from past prediction losses.
The uniform condition trains the same models and tracks the same losses, but
averages predictions equally. This is a mixture over fixed masks, not sparse
attention or a mechanism that saves computation. The masks preserve all input,
omit memory, omit goals, omit both, or use only a bias.

The fixed rival was chosen on eight dev seeds, before sealing. The strongest
candidate was sqrt/all in vigil and AdaGrad/all in silent outages. Retaining the
sqrt rival strengthened the comparison. Full dev results overlap the rival-selection
data; the held-out confirmation is the independent seed set. The rival and treatment
share public information, but a single model uses less compute than five experts.

## Descriptive findings and limits

On C050's held-out streams, removing memory from the AdaGrad predictor increased
Brier by **0.00774 [0.00576, 0.00972]**. Replacing memory content with a matched-load
sham increased it by **0.01029 [0.00785, 0.01273]**. Memory was useful under this
update rule. These were predeclared descriptive diagnostics, not separately
confirmed superiority claims or a multiplicity-corrected family.

AdaGrad did not improve the bias-only predictor in that diagnostic: its mean
gain was −0.00876. The main gain therefore is not explained by an overall advantage
on the action base rates alone. This does not isolate a unique cognitive mechanism.

The sqrt/all score was 0.04111 on C050's held-out lives, slightly below AdaGrad's
0.04178. This is descriptive; C050 does not establish AdaGrad as the best optimizer.
C051 uses its own sealed seeds, so its table should not be mixed with C050's means.

The tasks retain their existing world generators. Held-out seeds test fresh
lifetimes, not new causal structures or broad out-of-distribution generalisation.
The selector is per-action and uses cumulative losses. It does not condition its
weights on current context and can adapt slowly when the best source changes.
These limitations bound the negative finding: they do not show that every learned
receiver-selection architecture must fail.

## Relation to research literature

[Duchi, Hazan & Singer (2011)](https://jmlr.org/papers/v12/duchi11a.html) motivates
coordinate-wise accumulated-gradient scaling. The implementation uses the diagonal
AdaGrad update for each logistic weight. The paper's optimization theory does not
itself imply better cognition in MIND; C050 supplies this organism's evidence.

[Freund & Schapire (1997)](https://www.schapire.net/papers/FreundSc95.pdf) motivates
exponential weighting of experts after their losses become available. Here weights
use pre-outcome predictions and fixed eta=1. No new regret theorem or replication
of that paper's experiments is claimed. Its general rationale for online combination
does not guarantee superiority on this experiment's late-half endpoint.

[Goyal et al. (ICLR 2022)](https://arxiv.org/html/2103.01197v2) describes learned
communication and consolidation through a capacity-limited workspace. It motivates
the receiver-selection question; MIND's logistic mixture is a different mechanism.
These sources were reviewed at the specific depth recorded in
[the literature ledger](../knowledge/literature.md) and
[the protocol](H014-selective-integration-protocol.md).

## What to do next

Prioritize a sealed comparison of simple update rules under live control and hidden
capability shifts before promoting an optimizer into the default organism. Fixed-stream
prediction gains can alter bids, surprise reports and action distributions when enabled
live; their behavioural value is a separate empirical question.

A stronger future H014 experiment would make the reliability of public memory and
goal signals change within a life, then compare a context-dependent gate with a
matched generic predictor and change-point-aware fixed-source selectors. Register
the generator, margins and strongest controls before evaluating new held-out data.
The current result does not warrant expanding this five-expert mixture as a default.

The recurrent-transfer proposal remains a separate larger research direction. It
should inherit the stronger optimizer and fixed-state controls revealed here, and
still test first-opportunity transfer after process restart against compact-state,
feed-forward-history and recurrent non-workspace rivals.

## Evidence and reproducibility

- [Development record](../knowledge/records/2026-10-12T06-24-44Z-ae5cce04-full.json)
- [First sealed held-out record](../knowledge/records/2026-10-12T06-27-05Z-ae5cce04-heldout.json)
- [Exploratory rival-selection pilot](../runs/h014-selection-pilot.json)
- [Fresh-context self-review](../reviews/H014-selective-integration-review.md)

```bash
python -m mind check C050 C051 K14 --record --by "<contributor>"
python -m mind check C050 C051 K14 --heldout --record --by "<contributor>"
python -m unittest discover -s tests
python -m mind doctor
python -m mind run "organism self_model.step=adagrad" vigil --seeds 8
```

The new unit suite checks source filtering, per-coordinate gradient history,
pre-outcome loss accounting, read-only prediction hooks, exact restart replay,
event preservation and prefix invariance. All **69** project tests passed after
the session resumed; doctor passed. K14 additionally checks all 21 configurations
in three worlds and fresh processes with Python hash seeds 1 and 99.

This is one research contribution and same-model self-review. Re-recording older
claims from a differently identified environment may mechanically raise their
computed replication level; that does not establish independent empirical review.
Merge with a merge commit to preserve prediction seals.
