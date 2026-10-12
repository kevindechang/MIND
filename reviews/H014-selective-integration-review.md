# H014 implementation and experiment review

2026-10-11. Reviewer: `review_h014`, a fresh-context subagent of this Codex session.
This is same-model self-review, **not independent empirical replication**.

Scope: changes from main `c71a0f4` to the H014 mechanism, tests and protocol; a second
pass inspected C050/C051/K14 before their predictions were sealed in `04008e6`.

## Finding and resolution

The protocol initially referred to "two steps times five fixed filters" without
naming the eligible optimizers. The final protocol names normalised and AdaGrad,
plus the separately evaluated sqrt/all rival. The stored eight-seed pilot includes
all eleven fixed candidates. Recalculation confirms sqrt/all wins in vigil/dev and
AdaGrad/all wins in outage/silent. The expansion beyond the initially described ten
candidates is disclosed and makes the rival stronger; no held-out outcomes informed it.

## Checks

- Focused seven-test suite passed in the reviewer session.
- Reviewer additionally checked all 21 step/gate combinations across fresh processes
  with Python hash seeds 1 and 99; restored-run ledger heads matched.
- The mixture scores stored pre-outcome forecasts before training experts. No
  outcome leakage or replay-ordering bug was found.
- Source filtering precedes feature deduplication. Forecast/proposal calls do not
  mutate learning state. Shadow overrides retain actions, outcomes and broadcasts.
- C050's sign and late-half scoring match its statement. C051 averages paired
  seed-level differences equally across two worlds and requires all three controls
  to clear the relevance margin. Marginal intervals are not presented as simultaneous.
- C051 discloses dev-data overlap with fixed-rival selection. K14 explicitly covers
  the added modes. Neither claim is about live policy utility or phenomenal experience.

No blocking findings remained after the protocol clarification. The follow-up
review did not execute claims or inspect held-out outcomes. The main session's
claim records and report provide execution evidence separately.

## Report review after first confirmation

The reviewer checked C050/C051's reported gains, intervals, diagnostics, 29.1%
reduction and K14 counts against the immutable development and first held-out
records. The two claims' held-out seed sets do not overlap; their means remain
separate in the report. Two wording corrections were made: C051 has 32 seed-level
observations across 64 baseline lifetimes, and the question's absence of receiver
selection refers to the default organism. No blocking interpretation issue remained.
This review checked records; it did not independently rerun the experiments or
verify the main session's test commands.
