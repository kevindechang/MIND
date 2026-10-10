# H002 comparison frozen before scoring

Reference: MIND PR #17 head e65f57b441618bc371fb62bba1cdd228be170a23.

Use exact-blob SelfModel and Outage world. Compare same-event forecasts from S (original SelfModel), T (original action-only table), F (compact event-aware filter), F0 (filter ignoring alerts), FS (filter with reversed alert labels).

Policy is independent: scan 60%, manual 35%, wait 5%; 120 episodes of 25 ticks. Development seeds 0..15; evaluation seeds 20000..20031. Compare dev and silent worlds. No predictor sees private world state.
F starts p(up)=0.5, updates after scan outcome to 1 or 0, then evolves p=0.04+0.92*p each tick; at next observation, alert down sets p=0.08, alert up sets p=0.92. Manual uses T; wait has no scored outcome. F0 ignores alerts; FS reverses them. These are declared approximate parameters, not the world's hidden transition rates.

Primary metric: late-half scan-only Brier difference F-S, paired by seed. Secondary: T, F0, FS, all-outcome Brier, early-quarter and silent-world results. Paired percentile bootstrap: 10000 draws, seed 70017. S wins if F-S >0.008 and lower 95% CI>0; F wins if F-S <-0.008 and upper 95% CI<0; otherwise inconclusive. No parameter tuning after observing results.
