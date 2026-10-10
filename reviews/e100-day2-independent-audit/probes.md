# Reproducible adversarial probes

These probes were specified in `probe-plan.md` at commit `30aa31d` before execution. They do not modify the target source. Run with Python 3.9+ on POSIX; the pinned target checkout must be at `/private/tmp/MIND-pr7-validation` or adjust the explicit path. This is synthetic code auditing, not agent efficacy.

```python
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

source = Path('/private/tmp/MIND-pr7-validation/experiments/e100/day2.py')
assert hashlib.sha256(source.read_bytes()).hexdigest() == '0fe96c98b53435d9da514b4203010c04f96f02e5a73f9514b464913715711a63'
spec = importlib.util.spec_from_file_location('day2_audited', source)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
observations = {}

with tempfile.TemporaryDirectory(prefix='mind-day2-audit-') as td:
    # Paired public event histories, differing dependency knowledge.
    first = m.run_arm(td, 'connected', setup_kwargs={'link_outage': True})
    second = m.run_arm(td, 'disconnected', setup_kwargs={'link_outage': False})
    assert first['factual'] == second['factual']
    assert (first['linked_action'], second['linked_action']) == (m.DEFER, m.SCAN)
    assert (first['compact_action'], second['compact_action']) == (m.DEFER, m.SCAN)
    observations['information_collision'] = {
        'same_events': first['factual'],
        'connected': first, 'disconnected': second,
        'interpretation': 'source_events alone omits action-relevant dependency knowledge'}

    db = m.connect(Path(td) / 'update.sqlite3')
    try:
        m.setup(db, link_outage=False, outage_resource='greenhouse_light')
        # New public initial dependency observation, not simulator truth.
        db.execute('INSERT INTO causal_links VALUES (?,?,?)',
                   ('sensor', 'array_power', 'depends_on'))
        reached = m._linked_resources(db, 'goal-001')
        outages = {r[0] for r in db.execute(
            "SELECT resource FROM source_events WHERE kind='tool_unavailable'")}
        db.execute('UPDATE availability SET ok=? WHERE resource=?',
                   (0 if reached & outages else 1, 'sensor'))
        db.commit()
        before = m.report(db)
        assert before['linked_action'] == before['compact_action'] == m.SCAN
        # Future public event after both representations have been initialized.
        db.execute('INSERT INTO source_events VALUES (?,?,?)',
                   ('incident-new', 'tool_unavailable', 'array_power'))
        db.commit()
        db.close()
        fresh = m.connect(Path(td) / 'update.sqlite3')
        try:
            after = m.report(fresh)
        finally:
            fresh.close()
        assert (after['linked_action'], after['compact_action']) == (m.DEFER, m.SCAN)
        observations['unrefreshed_compact_state'] = {
            'before': before, 'after': after,
            'interpretation': 'compiled feature is sufficient for fixed initial query, not demonstrated for future evidence updates'}
    finally:
        db.close()

    db = m.connect(Path(td) / 'relations.sqlite3')
    try:
        m.setup(db, link_outage=False, outage_resource='array_power', unrelated_link=True)
        before = m.report(db)
        assert before['linked_action'] == m.SCAN
        db.execute("UPDATE causal_links SET effect=?,cause=? WHERE relation='unrelated'",
                   ('goal-001', 'array_power'))
        db.commit()
        after = m.report(db)
        assert before['factual'] == after['factual']
        assert after['linked_action'] == m.DEFER
        observations['relation_semantics'] = {
            'before': before, 'after': after,
            'interpretation': 'planner uses untyped reachability; unrelated relation label is ignored; outside original seed domain'}
    finally:
        db.close()

print(json.dumps(observations, indent=2, sort_keys=True))
```
