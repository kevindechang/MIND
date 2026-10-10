"""Independent deterministic G0 validation; not an agent performance experiment."""
import unittest
from fractions import Fraction as F
from itertools import combinations
from e001_finite_policy_v04 import (
    GRAPHS, PLANS, reach, effects, payoff, terminal, possible_statuses,
    likelihood, policy,
)

C=((2,1,2),(0,1,8),(1,1,2))
P=(1,1,1,2,1,2,2,2)
Z=((F(0),)*3,)*8

class PolicyCalibration(unittest.TestCase):
    def test_graph_family_eight_and_reachability_quotient_seven(self):
        signatures={effects(g) for g in GRAPHS}
        self.assertEqual((len(GRAPHS),len(signatures)),(8,7))
        self.assertEqual(effects(GRAPHS[5]),effects(GRAPHS[7]))

    def test_redundant_edge_never_changes_terminal_payoff(self):
        for a in PLANS:
            for goal in range(3):
                for desired in (0,1):
                    self.assertEqual(payoff(GRAPHS[5],a,((goal,desired,8),)),
                                     payoff(GRAPHS[7],a,((goal,desired,8),)))

    def test_priors_within_closure_class_cannot_change_decisions(self):
        p1=(0,0,0,0,0,3,0,1)
        p2=(0,0,0,0,0,1,0,3)
        self.assertEqual(terminal(tuple(map(F,p1)),C),terminal(tuple(map(F,p2)),C))

    def test_zero_budget_equals_terminal_reference(self):
        for prior in ((1,)*8,P):
            val,actions,_=policy(prior,C,Z,deadline=2,budget=0)
            self.assertEqual(val,terminal(tuple(map(F,prior)),C)[0])
            self.assertEqual(actions,(('WAIT',),))

    def test_deadline_too_late_probe_never_chosen_when_cost_positive(self):
        val,acts,_=policy(P,C,Z,deadline=1,budget=1,cost=F(1,4),delays=(2,))
        self.assertEqual(val,terminal(tuple(map(F,P)),C)[0])
        self.assertEqual(acts,(('WAIT',),))

    def test_noninformative_probe_not_worth_cost(self):
        # Restrict to a world pair differing only in redundant transitive edge.
        prior=(0,0,0,0,0,1,0,1)
        val,actions,_=policy(prior,C,Z,deadline=2,budget=2,cost=F(1,4))
        self.assertEqual(val,terminal(tuple(map(F,prior)),C)[0])
        self.assertEqual(actions,(('WAIT',),))

    def test_adaptive_two_probes_strictly_beat_one(self):
        one=policy(P,C,Z,deadline=2,budget=1,cost=F(1,10),delays=(1,))
        two=policy(P,C,Z,deadline=2,budget=2,cost=F(1,10),delays=(1,))
        self.assertEqual(one[0],-F(121,60))
        self.assertEqual(two[0],-F(47,24))
        self.assertEqual(two[0]-one[0],F(7,120))
        self.assertEqual(two[1],(('PROBE',0,1),))

    def test_adaptive_branch_selective_second_probe(self):
        branches=[]
        for status in possible_statuses(0):
            w=tuple(F(P[i])*likelihood(i,0,status,Z) for i in range(8))
            if sum(w):
                best=policy(w,C,Z,deadline=1,budget=1,cost=F(1,10),delays=(1,))
                branches.append((status,best[1]))
        self.assertEqual(branches,[(('D',1),(('WAIT',),)),
                                   (('D',3),(('WAIT',),)),
                                   (('D',5),(('PROBE',1,1),)),
                                   (('D',7),(('WAIT',),))])

    def test_censor_status_likelihood_normalized(self):
        c=tuple((F(1,4),F(1,2),F(3,4)) for _ in GRAPHS)
        for i in range(8):
            for node in range(3):
                self.assertEqual(sum(likelihood(i,node,s,c) for s in possible_statuses(node)),1)

    def test_graph_dependent_censor_can_inform_without_terminal_value(self):
        c=[list((F(1,2),)*3) for _ in GRAPHS]
        c[5][2]=F(1,4);c[7][2]=F(3,4)
        prior=(0,0,0,0,0,1,0,1)
        posterior_censored=(F(1,4),F(3,4))
        weights=[F(prior[i])*likelihood(i,2,('C',None),c) for i in range(8)]
        self.assertEqual((weights[5]/sum(weights),weights[7]/sum(weights)),posterior_censored)
        self.assertEqual(terminal(tuple(weights),C)[0],terminal(tuple(map(F,prior)),C)[0])

    def test_invalid_inputs_rejected(self):
        with self.assertRaisesRegex(ValueError,'prior'):policy((1,)*7,C)
        with self.assertRaisesRegex(ValueError,'censor'):policy((1,)*8,C,censor=((F(2),)*3,)*8)
        with self.assertRaisesRegex(ValueError,'time'):policy((1,)*8,C,deadline=0)
        with self.assertRaisesRegex(ValueError,'commitments'):policy((1,)*8,((0,1,8),(0,0,4)))

    def test_zero_cost_more_budget_not_worse(self):
        for prior in ((1,)*8,P):
            vals=[policy(prior,C,Z,deadline=2,budget=b,cost=0,delays=(1,))[0] for b in range(3)]
            self.assertEqual(vals,sorted(vals))

if __name__=='__main__':unittest.main()
