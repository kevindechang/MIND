"""Adversarial unit checks for the independent E100 dynamic-state calibration."""
import itertools
import unittest
from dynamic_probe import GOALS, RESOURCES, Base, Eager, Lazy, replay_oracle, generate, run_episode, controls


class DynamicCrossdayTests(unittest.TestCase):
    def test_predeclared_controls(self):
        self.assertEqual(controls()['restoration_reversal'], 'SCAN')

    def test_exhaustive_two_resources_status_sequences(self):
        edges=[('goal-0','resource-0'), ('goal-0','resource-1')]
        choices=list(itertools.product(('tool_unavailable','tool_restored'),('resource-0','resource-1')))
        cases=0
        for size in range(6):
            for seq in itertools.product(choices, repeat=size):
                stream=[{'event_id':f'e-{i:03d}','type':t,'resource':r}
                        for i,(t,r) in enumerate(seq)]
                expected=replay_oracle(edges,stream,'goal-0')
                for cls in (Base,Eager,Lazy):
                    a=cls(edges)
                    for e in stream:a.public_update(e)
                    self.assertEqual(a.act('goal-0'),expected,(cls.__name__,seq))
                cases+=1
        self.assertEqual(cases,1365)  # 1+4+16+64+256+1024

    def test_link_change_and_sham_after_outage(self):
        edges=[('goal-0','resource-0')]
        stream=[{'type':'tool_unavailable','resource':'resource-0'},
                {'type':'link_removed','goal':'goal-0','resource':'resource-9'},
                {'type':'link_removed','goal':'goal-0','resource':'resource-0'},
                {'type':'link_added','goal':'goal-0','resource':'resource-0'}]
        expect=['DEFER','DEFER','SCAN','DEFER']
        for cls in (Base,Eager,Lazy):
            a=cls(edges)
            for e,correct in zip(stream,expect):
                a.public_update(e)
                self.assertEqual(a.act('goal-0'),correct,cls.__name__)

    def test_deliberate_stale_cache_mutation_detected(self):
        edges=[('goal-0','resource-0')]
        a=Lazy(edges)
        outage={'type':'tool_unavailable','resource':'resource-0'}
        restored={'type':'tool_restored','resource':'resource-0'}
        a.public_update(outage)
        self.assertEqual(a.act('goal-0'),'DEFER')
        # Deliberately skip update on a restored event (simulate faulty consumer).
        reference=replay_oracle(edges,[outage,restored],'goal-0')
        self.assertNotEqual(a.act('goal-0'),reference)
        # Applying omitted event repairs the discrepancy.
        a.public_update(restored)
        self.assertEqual(a.act('goal-0'),reference)

    def test_data_parity_and_counterfactual_seed(self):
        one=run_episode(10012,0.4,0.8)
        two=run_episode(10012,0.4,0.8)
        self.assertEqual(one,two)
        self.assertTrue(all(z==0 for z in one['errors'].values()))
        initial, stream=generate(10012,0.4,0.8)
        self.assertEqual(len(stream),180)
        self.assertEqual(len({e['event_id'] for e in stream}),180)
        self.assertTrue(len(initial)>0)


if __name__ == '__main__':
    unittest.main()
