# H002 comparison frozen before scoring

Reference: MIND PR #17 head e65f57b441618bc371fb62bba1cdd228be170a23.

Use exact-blob SelfModel and Outage world. Compare same-event forecasts from S (original SelfModel), T (original action-only table), F (compact event-aware filter), F0 (filter ignoring alerts), FS (filter with reversed alert labels).

Policy is independent: scan 60%, manual 35%, wait 5%; 120 episodes of 25 ticks. Development seeds 0..15; evaluation seeds 20000..20031. Compare dev and silent worlds. No predictor sees private world state.