"""Deterministic adversarial instrument tests; not scientific agent trials."""
import inspect
import unittest
from fractions import Fraction as F
from e001_three_node_version_space import (PublicCommitment, PublicProbe,
 PublicOutcome, make_history, all_three_node_dags, simulate_delivered)
from e001_three_node_robustness import (conditional_posterior, conditional_score,
 robust_score, uniform_censor)

EMPTY=frozenset()
FULL=frozenset(((0,1),(0,2),(1,2)))
PAIR=(EMPTY,FULL)
PRIOR=(F(1,2),F(1,2))
IGN=uniform_censor(PAIR)
MNAR=((F(1,4),)*3,(F(3,4),)*3)

def h(node=2, delivered=False, censored=False, deadline=2, due=1, commitments=()):
    probes=(PublicProbe(7,node,0,due),)
    outcomes=(PublicOutcome(7,node,4),) if delivered else ()
    return make_history(commitments,probes,outcomes,(7,) if censored else (),deadline)

class Robustness(unittest.TestCase):
 def test_prior_without_probe(self):
    hist=make_history((),(),(),(),2)
    self.assertEqual(conditional_posterior(hist,(3,1),IGN,PAIR),{0:F(3,4),1:F(1,4)})
 def test_ignorable_censor(self):
    self.assertEqual(conditional_posterior(h(censored=True),PRIOR,IGN,PAIR),{0:F(1,2),1:F(1,2)})
 def test_informative_censor_updates(self):
    self.assertEqual(conditional_posterior(h(censored=True),PRIOR,MNAR,PAIR),{0:F(1,4),1:F(3,4)})
 def test_delivery_status_is_informative_even_when_mask_collides(self):
    self.assertEqual(conditional_posterior(h(delivered=True),PRIOR,MNAR,PAIR),{0:F(3,4),1:F(1,4)})
 def test_same_public_history_independent_of_hidden_truth(self):
    p=(PublicProbe(7,2,0,1),)
    a=make_history((),p,simulate_delivered(EMPTY,p),(),2)
    b=make_history((),p,simulate_delivered(FULL,p),(),2)
    self.assertEqual(a,b)
    self.assertEqual(conditional_score(a,PRIOR,MNAR,PAIR),conditional_score(b,PRIOR,MNAR,PAIR))
 def test_outcome_separates_worlds(self):
    p=(PublicProbe(7,0,0,1),)
    for ix,g in enumerate(PAIR):
      hist=make_history((),p,simulate_delivered(g,p),(),2)
      self.assertEqual(conditional_posterior(hist,PRIOR,IGN,PAIR),{ix:F(1)})
 def test_deadline_pending_is_not_a_missingness_signal(self):
    pending=h(deadline=2,due=3)
    base=make_history((),(),(),(),2)
    self.assertEqual(conditional_posterior(pending,PRIOR,MNAR,PAIR),conditional_posterior(base,PRIOR,MNAR,PAIR))
 def test_matured_without_status_fails_closed(self):
    with self.assertRaisesRegex(ValueError,'matured'):
      conditional_posterior(h(),PRIOR,MNAR,PAIR)
 def test_pre_due_censor_fails_closed(self):
    with self.assertRaisesRegex(ValueError,'before event due'):
      conditional_posterior(h(censored=True,deadline=2,due=3),PRIOR,MNAR,PAIR)
 def test_out_of_family_reachability_fails_closed(self):
    probe=(PublicProbe(7,2,0,1),)
    novel=make_history((),probe,(PublicOutcome(7,2,0b101),),(),2)
    with self.assertRaisesRegex(ValueError,'zero normalizer'):
      conditional_posterior(novel,(1,)*8,uniform_censor())
 def test_hidden_mismatch_is_undetectable_without_separating_probe(self):
    hist=make_history((),(),(),(),2)
    self.assertEqual(conditional_posterior(hist,PRIOR,IGN,PAIR),{0:F(1,2),1:F(1,2)})
 def test_no_support_history_fails_closed(self):
    with self.assertRaisesRegex(ValueError,'zero normalizer'):
      conditional_posterior(h(censored=True),PRIOR,((0,)*3,)*2,PAIR)
 def test_parameter_checking(self):
    hist=make_history((),(),(),(),2)
    for prior,cen in [((-1,2),IGN),((0,0),IGN),(PRIOR,((F(2),)*3,)*2)]:
      with self.assertRaises(ValueError): conditional_posterior(hist,prior,cen,PAIR)
 def test_robust_reference_never_treat_as_bayes(self):
    hist=make_history((PublicCommitment(0,1,8), PublicCommitment(2,1,8)),(),(),(),2)
    a,_,_=robust_score(hist,[(9,1),(1,9)],[IGN,IGN],PAIR)
    self.assertTrue(a)
    self.assertEqual(a,robust_score(hist,[(1,9),(9,1)],[IGN,IGN],PAIR)[0])
 def test_sensitive_to_wrong_missingness_assumption(self):
    hist=h(censored=True)
    b1=conditional_posterior(hist,PRIOR,MNAR,PAIR)
    b2=conditional_posterior(hist,PRIOR,((F(3,4),)*3,(F(1,4),)*3),PAIR)
    self.assertEqual((b1[0],b2[0]),(F(1,4),F(3,4)))
 def test_no_private_truth_parameter(self):
    self.assertEqual(list(inspect.signature(conditional_score).parameters),['history','prior','censor','family'])
 def test_censor_beyond_deadline_rejected_by_base(self):
    with self.assertRaisesRegex(ValueError,'after deadline'):
      make_history((),(PublicProbe(7,0,0,3),),(PublicOutcome(7,0,1),),(),2)

if __name__=='__main__': unittest.main()

# Extended exhaustive properties. Each observation is a deterministic unit scenario,
# not an independent sampled empirical episode.
class ExhaustiveProperties(unittest.TestCase):
 def test_uniform_reference_all_single_probes_and_graphs(self):
    from e001_three_node_version_space import reachability_mask
    graphs=all_three_node_dags()
    for node in range(3):
      probe=(PublicProbe(11,node,0,1),)
      for graph in graphs:
        y=reachability_mask(graph,node)
        hist=make_history((),probe,(PublicOutcome(11,node,y),),(),2)
        got=conditional_posterior(hist,(1,)*8,uniform_censor())
        expected=[i for i,g in enumerate(graphs) if reachability_mask(g,node)==y]
        self.assertEqual(got,{i:F(1,len(expected)) for i in expected})
 def test_informative_nonreceipt_cannot_be_treated_as_no_probe(self):
    no_probe=make_history((),(),(),(),2)
    censored=h(censored=True)
    self.assertNotEqual(conditional_posterior(no_probe,PRIOR,MNAR,PAIR),
                        conditional_posterior(censored,PRIOR,MNAR,PAIR))
 def test_prior_action_reversal_and_minimax(self):
    hist=make_history((PublicCommitment(0,1,8), PublicCommitment(2,1,8)),(),(),(),2)
    self.assertEqual(conditional_score(hist,(9,1),IGN,PAIR)[0],((0,2),))
    self.assertEqual(conditional_score(hist,(1,9),IGN,PAIR)[0],((0,),))
    self.assertEqual(robust_score(hist,[(9,1),(1,9)],[IGN,IGN],PAIR)[:2],(((0,),),-F(41,5)))

