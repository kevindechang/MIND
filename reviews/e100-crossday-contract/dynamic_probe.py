#!/usr/bin/env python3
"""E100 dynamic causal status: exact public-event, resource-aware instrument.

Scope: synthetic fixed bipartite DAG. Not a MIND original-module run or agent trial.
Frozen design: reviews/e100-crossday-contract/dynamic-protocol-v02.md, commit 54f8465.
"""
import argparse
import hashlib
import itertools
import json
import random
import statistics
from collections import defaultdict

GOALS = tuple(f'goal-{n}' for n in range(8))
RESOURCES = tuple(f'resource-{n}' for n in range(10))


def event_bytes(events):
    return json.dumps(events, sort_keys=True, separators=(',', ':')).encode()


def initial_world(seed, density):
    rng = random.Random(seed)
    edges = sorted((goal, resource) for goal in GOALS for resource in RESOURCES if rng.random() < density)
    return edges, [], rng


def update_ledger(events, row):
    assert row['event_id'] == f'e-{len(events):03d}', row
    events.append(row)


def generate(seed, density, pquery, horizon=180):
    edges, _, rng = initial_world(seed, density)
    public = []
    for t in range(horizon):
        if rng.random() < pquery:
            e = {'event_id':f'e-{t:03d}', 'type':'query', 'goal':rng.choice(GOALS)}
        elif rng.random() < 0.7:
            e = {'event_id':f'e-{t:03d}', 'type':rng.choice(('tool_unavailable','tool_restored')),
                 'resource':rng.choice(RESOURCES)}
        else:
            e = {'event_id':f'e-{t:03d}', 'type':rng.choice(('link_added','link_removed')),
                 'goal':rng.choice(GOALS), 'resource':rng.choice(RESOURCES)}
        update_ledger(public, e)
    return edges, public


def replay_oracle(initial_edges, events, goal):
    """Independent oracle: reconstruct public graph and most recent status by replay.
    No class shared with algorithms; uses sorted pair tuple membership, not caches.
    """
    if goal not in GOALS:
        return 'NO_GOAL'
    pairs = set(tuple(x) for x in initial_edges)
    last = {}
    for e in events:
        t = e['type']
        if t == 'link_added': pairs.add((e['goal'],e['resource']))
        elif t == 'link_removed': pairs.discard((e['goal'],e['resource']))
        elif t == 'tool_unavailable': last[e['resource']] = True
        elif t == 'tool_restored': last[e['resource']] = False
    return 'DEFER' if any(g == goal and last.get(r,False) for g,r in pairs) else 'SCAN'


class Base:
    def __init__(self, edges):
        self.graph = {g:set() for g in GOALS}
        self.down = set()
        self.cost = {'initial':0, 'update':0, 'query':0}
        for g,r in edges:
            self.graph[g].add(r)
            self.cost['initial'] += 1

    def public_update(self, e):
        kind = e['type']
        if kind in ('tool_unavailable','tool_restored'):
            if kind == 'tool_unavailable': self.down.add(e['resource'])
            else: self.down.discard(e['resource'])
            self.cost['update'] += 1
        elif kind in ('link_added','link_removed'):
            edges = self.graph[e['goal']]
            if kind == 'link_added': edges.add(e['resource'])
            else: edges.discard(e['resource'])
            self.cost['update'] += 1

    def compute(self, goal):
        if goal not in self.graph: return 'NO_GOAL'
        blocked = False
        for r in self.graph[goal]:
            self.cost['query'] += 2  # adjacency visit + status membership check
            if r in self.down: blocked=True
        return 'DEFER' if blocked else 'SCAN'

    def act(self, goal):
        return self.compute(goal)

    def total(self): return sum(self.cost.values())


class Eager(Base):
    def __init__(self, edges):
        super().__init__(edges)
        self.blocked = {}
        self.recompute_all('initial')

    def recompute_all(self, cost_bucket):
        for goal in GOALS:
            block = False
            for r in self.graph[goal]:
                self.cost[cost_bucket] += 2
                if r in self.down: block = True
            self.blocked[goal] = block

    def public_update(self, e):
        super().public_update(e)
        kind = e['type']
        if kind in ('link_added','link_removed'):
            self.recompute_all('update')
        elif kind in ('tool_unavailable','tool_restored'):
            r = e['resource']
            for g in GOALS:
                self.cost['update'] += 1  # membership test: does changed resource touch g?
                if r in self.graph[g]:
                    block = False
                    for r0 in self.graph[g]:
                        self.cost['update'] += 2
                        if r0 in self.down: block = True
                    self.blocked[g] = block

    def act(self, goal):
        self.cost['query'] += 1  # cached scalar lookup
        return 'NO_GOAL' if goal not in self.blocked else ('DEFER' if self.blocked[goal] else 'SCAN')


class Lazy(Base):
    def __init__(self, edges):
        super().__init__(edges)
        self.cache = {}

    def public_update(self, e):
        super().public_update(e)
        if e['type'] != 'query':
            self.cost['update'] += len(self.cache)  # charged invalidations
            self.cache.clear()

    def act(self, goal):
        self.cost['query'] += 1 # lookup
        if goal not in self.cache:
            self.cache[goal] = self.compute(goal)
        return self.cache[goal]


def run_episode(seed, density, pquery):
    edges, stream = generate(seed, density, pquery)
    agents = {'graph':Base(edges),'eager':Eager(edges),'lazy':Lazy(edges)}
    errors = defaultdict(int)
    queries=0
    for t,e in enumerate(stream):
        if e['type'] != 'query':
            for a in agents.values(): a.public_update(e)
        else:
            queries += 1
            expected = replay_oracle(edges, stream[:t+1], e['goal'])
            for name,a in agents.items():
                if a.act(e['goal']) != expected: errors[name] += 1
    assert all(a.graph == agents['graph'].graph and a.down == agents['graph'].down for a in agents.values())
    return {'seed':seed,'queries':queries,'event_sha256':hashlib.sha256(event_bytes(stream)).hexdigest(),
            'errors':{n:errors[n] for n in agents},
            'costs':{n:dict(a.cost, total=a.total()) for n,a in agents.items()}}


def controls():
    edges=[('goal-0','resource-0')]
    initial=[{'event_id':'e-000','type':'tool_unavailable','resource':'resource-0'}]
    restored=initial + [{'event_id':'e-001','type':'tool_restored','resource':'resource-0'}]
    unrelated=initial + [{'event_id':'e-001','type':'tool_restored','resource':'resource-9'}]
    cut=initial + [{'event_id':'e-001','type':'link_removed','goal':'goal-0','resource':'resource-0'}]
    sham=initial + [{'event_id':'e-001','type':'link_removed','goal':'goal-0','resource':'resource-9'}]
    duplicate=initial + [{'event_id':'e-001','type':'tool_unavailable','resource':'resource-0'}]
    checks={'restoration_reversal':(restored,'SCAN'), 'unrelated_restoration':(unrelated,'DEFER'),
            'causal_edge_cut':(cut,'SCAN'),'irrelevant_edge_sham':(sham,'DEFER'),
            'idempotent_outage':(duplicate,'DEFER')}
    output={}
    for name,(seq,want) in checks.items():
        assert replay_oracle(edges,seq,'goal-0')==want
        for cls in (Base,Eager,Lazy):
            a=cls(edges)
            for e in seq:a.public_update(e)
            assert a.act('goal-0')==want, (name, cls.__name__)
        output[name]=want
    assert replay_oracle(edges,initial,'missing')=='NO_GOAL'
    for cls in (Base,Eager,Lazy):assert cls(edges).act('missing')=='NO_GOAL'
    output['unknown_goal']='NO_GOAL'
    # Deliberately stale snapshot ignores public restoration (negative control)
    stale=Eager(edges)
    stale.public_update(initial[0]); stale_before=stale.act('goal-0')
    assert stale_before=='DEFER'
    assert stale.act('goal-0') != replay_oracle(edges,restored,'goal-0')
    output['negative_stale_snapshot']='EXPECTED_MISMATCH'
    return output


def summarize():
    results={}
    for p in (0.2,0.8):
        for density in (0.1,0.4):
            label=f'q{p}_d{density}'
            episodes=[run_episode(10000+i,density,p) for i in range(32)]
            results[label]={
                'n_episodes':len(episodes),'event_count_each':180,
                'total_queries':sum(x['queries'] for x in episodes),
                'accuracy_errors':{arm:sum(x['errors'][arm] for x in episodes) for arm in ('graph','eager','lazy')},
                'total_ops':{arm:sum(x['costs'][arm]['total'] for x in episodes) for arm in ('graph','eager','lazy')},
                'mean_ops':{arm:round(statistics.mean(x['costs'][arm]['total'] for x in episodes),3) for arm in ('graph','eager','lazy')},
                'min_max_ops':{arm:[min(x['costs'][arm]['total'] for x in episodes),max(x['costs'][arm]['total'] for x in episodes)] for arm in ('graph','eager','lazy')},
                'cost_by_phase':{arm:{phase:sum(x['costs'][arm][phase] for x in episodes) for phase in ('initial','update','query')}
                     for arm in ('graph','eager','lazy')},
                'all_episode_stream_sha256':hashlib.sha256(''.join(x['event_sha256'] for x in episodes).encode()).hexdigest()
            }
    assert sum(v['total_queries'] for v in results.values())>0
    assert all(sum(v['accuracy_errors'].values()) == 0 for v in results.values())
    return {'status':'PASS','python_scope':'synthetic_online_fixed_bipartite_public_stream','controls':controls(),
            'strata':results,'accepted_science':0,'review':'SELF_REVIEW_ONLY',
            'not_executed':['original MIND combined modules','full repo regression','learned-agent trials','SIGKILL process recovery','hardware cost matching']}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--self-test',action='store_true')
    a=ap.parse_args()
    if not a.self_test:ap.error('use --self-test')
    print(json.dumps(summarize(),indent=2,sort_keys=True))


if __name__=='__main__':main()
