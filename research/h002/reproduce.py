#!/usr/bin/env python3
"""H002 controlled same-event calibration probe; NOT original C017 organism replay."""
import json, random, statistics, sys
from types import SimpleNamespace
from mind.kernel import Content
from mind.organs.self_model import SelfModel
from mind.rivals import SuccessTable
from mind.worlds.outage import Outage, LENGTH

class Filter:
    def __init__(self, mode='real'):
        self.p, self.mode, self.manual = .5, mode, SuccessTable()
    def observe(self, obs):
        alert=obs.get('alert')
        if self.mode=='blind' or not alert:return
        if self.mode=='swapped':alert='up' if alert=='down' else 'down'
        self.p=.08 if alert=='down' else .92
    def forecast(self, action):
        return self.p if action=='scan' else self.manual.forecast(action)
    def update(self, action, outcome):
        if action=='scan' and outcome is not None:self.p=float(outcome)
        if action=='manual' and outcome is not None:self.manual.update(action,outcome)
        self.p=.04+.92*self.p

def lifetime(seed, variant):
    env=Outage(seed,variant); rng=random.Random(f'policy|{variant}|{seed}')
    model=SelfModel({}); table=SuccessTable()
    filters={'F':Filter(),'F0':Filter('blind'),'FS':Filter('swapped')}
    sums={a:0. for a in ('S','T','F','F0','FS')}; count=0
    for ep in range(120):
        obs=env.reset(); prev=None; previous_outcome=None
        for tick in range(LENGTH):
            view=tuple(Content('perception',k,v,1.) for k,v in sorted(obs.items()))
            model.learn(prev,SimpleNamespace(outcome=previous_outcome),view,None)
            for f in filters.values():f.observe(obs)
            u=rng.random(); action='scan' if u<.60 else 'manual' if u<.95 else 'wait'
            predictions={'S':model.forecast(view,action),'T':table.forecast(action)}
            predictions.update({k:f.forecast(action) for k,f in filters.items()})
            model.after_act(SimpleNamespace(action=action),view,action,None)
            step=env.step(action)
            if ep>=60 and action=='scan':
                count+=1
                for a,p in predictions.items():sums[a]+=(p-step.outcome)**2
            if step.outcome is not None:table.update(action,step.outcome)
            for f in filters.values():f.update(action,step.outcome)
            if step.done:
                model.learn_terminal(SimpleNamespace(action=action),step.reward,step.outcome,None)
                break
            prev=SimpleNamespace(action=action);previous_outcome=step.outcome;obs=step.obs
    return {a:sums[a]/count for a in sums}

def bootstrap(values, rng, draws=10000):
    n=len(values)
    means=sorted(sum(values[rng.randrange(n)] for _ in range(n))/n for _ in range(draws))
    return [means[int(.025*draws)],means[int(.975*draws)-1]]

def main():
    n=2 if '--quick' in sys.argv else 32
    result={'scope':'targeted fixed-policy, not C017 organism stream','n':n,'variants':{}}
    rng=random.Random(70017)
    for variant in ('dev','silent'):
        rows=[lifetime(seed,variant) for seed in range(20000,20000+n)]
        diffs=[r['F']-r['S'] for r in rows]
        result['variants'][variant]={
            'brier':{a:statistics.mean(r[a] for r in rows) for a in rows[0]},
            'delta_F_minus_S':statistics.mean(diffs),
            'paired_bootstrap_ci95':bootstrap(diffs,rng),
            'silent_filter_parity':all(r['F']==r['F0']==r['FS'] for r in rows) if variant=='silent' else None}
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
