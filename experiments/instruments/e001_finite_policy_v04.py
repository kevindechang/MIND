"""E001 G0 finite-horizon probe policy, synthetic calibration only."""
from fractions import Fraction as F
from itertools import combinations, product
from functools import lru_cache

EDGES=((0,1),(0,2),(1,2))
GRAPHS=tuple(frozenset(e for j,e in enumerate(EDGES) if i&(1<<j)) for i in range(8))
PLANS=((),)+tuple(combinations(range(3),1))+tuple(combinations(range(3),2))

def reach(graph,node):
    seen={node}
    while True:
        new=seen|{v for u,v in graph if u in seen}
        if new==seen:break
        seen=new
    return sum(1<<j for j in seen)

def effects(graph):return tuple(reach(graph,node) for node in range(3))

def payoff(graph,plan,commitments):
    e=0
    for a in plan:e^=reach(graph,a)
    return -len(plan)-sum(p for goal,desired,p in commitments if int(bool(e&(1<<goal)))!=desired)

def terminal(weights,commitments):
    norm=sum(weights)
    if norm<=0:raise ValueError('zero posterior')
    values={plan:sum(weights[i]*payoff(g,plan,commitments) for i,g in enumerate(GRAPHS))/norm for plan in PLANS}
    best=max(values.values())
    return best,tuple(a for a in PLANS if values[a]==best)

def possible_statuses(node):
    return (('C',None),)+tuple(('D',y) for y in sorted({reach(g,node) for g in GRAPHS}))

def likelihood(i,node,status,censor):
    c=censor[i][node]
    return c if status[0]=='C' else (F(1)-c if status[1]==reach(GRAPHS[i],node) else F(0))

def policy(prior,commitments,censor=None,deadline=2,budget=2,cost=F(1,4),delays=(1,2)):
    """History-only optimal net utility: public queue, event IDs, posterior and budget."""
    if censor is None:censor=((F(0),)*3,)*8
    prior=tuple(F(x) for x in prior)
    censor=tuple(tuple(F(x) for x in row) for row in censor)
    cost=F(cost)
    if len(prior)!=8 or any(x<0 for x in prior) or sum(prior)<=0:raise ValueError('prior')
    if len(censor)!=8 or any(len(row)!=3 for row in censor) or any(not 0<=x<=1 for row in censor for x in row):raise ValueError('censor')
    if type(deadline)!=int or deadline<1 or type(budget)!=int or budget<0:raise ValueError('time/budget')
    if cost<0 or not delays or any(type(d)!=int or d<1 for d in delays):raise ValueError('cost/delay')
    goals=set()
    for g,d,p in commitments:
        if g in goals or type(g)!=int or g not in (0,1,2) or d not in (0,1) or type(p)!=int or p<1:raise ValueError('commitments')
        goals.add(g)
    commitments=tuple(commitments)
    delays=tuple(sorted(set(delays)))
    calls=0
    @lru_cache(maxsize=None)
    def V(t,weights,pending,remaining,next_id):
        nonlocal calls
        calls+=1
        if t==deadline:
            if any(ev[3]<=t for ev in pending):raise AssertionError('due unprocessed')
            return terminal(weights,commitments)[0],('TERMINAL',)
        choices=[]
        for action in (('WAIT',),)+tuple(('PROBE',n,d) for n in range(3) for d in delays if remaining):
            if action[0]=='WAIT':
                q=pending;remain=remaining;fee=F(0);newid=next_id
            else:
                _,node,delay=action
                q=pending+((next_id,node,t,t+delay),)
                remain=remaining-1;fee=cost;newid=next_id+1
            due=tuple(sorted((ev for ev in q if ev[3]==t+1),key=lambda ev:(ev[3],ev[0])))
            later=tuple(ev for ev in q if ev[3]>t+1)
            if any(ev[3]<t+1 for ev in q):raise AssertionError('overdue queue')
            expected=-fee
            for statuses in product(*(possible_statuses(ev[1]) for ev in due)):
                newweights=tuple(weights[i]*_likelihood_product(i,due,statuses,censor) for i in range(8))
                mass=sum(newweights)
                if not mass:continue
                posterior=tuple(x/mass for x in newweights)
                expected+=mass/sum(weights)*V(t+1,posterior,later,remain,newid)[0]
            choices.append((action,expected))
        best=max(v for _,v in choices)
        return best,tuple(a for a,v in choices if v==best)
    initial=tuple(p/sum(prior) for p in prior)
    value,actions=V(0,initial,(),budget,1)
    return value,actions,calls

def _likelihood_product(i,due,statuses,censor):
    ans=F(1)
    for ev,status in zip(due,statuses):ans*=likelihood(i,ev[1],status,censor)
    return ans
