#!/usr/bin/env python3
"""E100 cross-day event semantics CANARY (not original MIND module execution).

Transcription: PR7 day2.py blob 524cd567fffb842cb456e6fb54bf76e504d0b859;
PR12 day7.py blob 57b804ee3cfbf0feaee07b78c49e57d6ec26a40d.
The causal link and temporal status predicates here are transcribed, not
imports from a byte-exact checkout. This checks integration assumptions only.
"""
import itertools
import json


def day2(events, linked_resources):
    if not any(kind.startswith('commitment:') for kind, resource in events):
        return 'NO_GOAL'
    outages = {resource for kind, resource in events if kind == 'tool_unavailable'}
    return 'DEFER' if outages & linked_resources else 'SCAN'


def day7(events):
    goals = [resource for kind, resource in events if kind.startswith('commitment:')]
    if not goals:
        return 'NO_GOAL'
    latest = {}
    for kind, resource in events:
        if kind == 'tool_unavailable':
            latest[resource] = False
        elif kind == 'tool_restored':
            latest[resource] = True
    return 'DEFER' if any(not latest.get(g, True) for g in goals) else 'SCAN'


def check():
    goal = [('commitment:inspect_signal', 'sensor')]
    cases = [
        ('control_no_outage', (), {'sensor'}, ('SCAN', 'SCAN')),
        ('control_outage', (('tool_unavailable', 'sensor'),), {'sensor'}, ('DEFER', 'DEFER')),
        ('restoration', (('tool_unavailable', 'sensor'), ('tool_restored', 'sensor')), {'sensor'}, ('DEFER', 'SCAN')),
        ('unrelated_restore', (('tool_unavailable', 'sensor'), ('tool_restored', 'clock')), {'sensor'}, ('DEFER', 'DEFER')),
        ('later_outage', (('tool_restored', 'sensor'), ('tool_unavailable', 'sensor')), {'sensor'}, ('DEFER', 'DEFER')),
        ('upstream_outage', (('tool_unavailable', 'array_power'),), {'sensor', 'array_power'}, ('DEFER', 'SCAN')),
        ('day4_kind', (('tick', 'clock'),), {'sensor'}, ('NO_GOAL', 'NO_GOAL')),
    ]
    observed = []
    for name, updates, links, expected in cases:
        events = ([(('commitment' if name == 'day4_kind' else goal[0][0]), 'sensor')]
                  + list(updates))
        got = (day2(events, links), day7(events))
        assert got == expected, (name, got, expected)
        observed.append({'case': name, 'day2': got[0], 'day7': got[1], 'same': got[0] == got[1]})

    # Same-observation compact sufficient state can track restoration exactly.
    symbols = tuple(itertools.product(('tool_unavailable', 'tool_restored'), ('sensor','array_power','clock')))
    finite = 0
    for relevant in ({'sensor'}, {'sensor', 'array_power'}):
        for n in range(5):
            for sequence in itertools.product(symbols, repeat=n):
                latest = {}
                compact = set()
                for kind, res in sequence:
                    latest[res] = kind
                    if res in relevant:
                        if kind == 'tool_unavailable': compact.add(res)
                        else: compact.discard(res)
                reference = any(latest.get(r) == 'tool_unavailable' for r in relevant)
                assert bool(compact) == reference
                finite += 1
    return {'status': 'PASS', 'crossday_cases': observed,
            'disagreements': sum(not row['same'] for row in observed),
            'compact_reference_equalities': finite,
            'scope': 'transcribed fixed policies, not MIND original-module execution; no lifecycle cost parity'}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2, sort_keys=True))
