"""H010 world-design checks; NOT claims about consciousness."""
import unittest
from mind.worlds.poltergeist import Poltergeist, _LENGTH


class PoltergeistTests(unittest.TestCase):
    def test_seeded_reproduction_for_each_variant(self):
        for variant in Poltergeist.variants:
            a, b = Poltergeist(7, variant), Poltergeist(7, variant)
            for _ in range(4):
                self.assertEqual(a.reset(), b.reset())
                for t in range(_LENGTH):
                    act = Poltergeist.actions[t % len(Poltergeist.actions)]
                    self.assertEqual(a.step(act), b.step(act))
                self.assertEqual(a.summary(), b.summary())

    def test_exogenous_events_unchanged_by_action_policy(self):
        for variant in Poltergeist.variants:
            a, b = Poltergeist(19, variant), Poltergeist(19, variant)
            for _ in range(3):
                a.reset(); b.reset()
                for _ in range(_LENGTH):
                    x = a.step("tap_a")
                    y = b.step("wait")
                    self.assertEqual(x.info["shock"], y.info["shock"])
                    self.assertEqual(x.info["slipped"], y.info["slipped"])
                self.assertEqual(a.polarity, b.polarity)

    def test_private_cause_never_sent_to_agent(self):
        w = Poltergeist(3)
        obs = w.reset()
        self.assertEqual(set(obs), {"dial"})
        for i in range(_LENGTH):
            s = w.step("tap_b")
            self.assertEqual(set(s.obs), {"dial"} if i < _LENGTH - 1 else set())
            self.assertEqual(set(s.info), {"shock", "actuation", "slipped", "polarity", "before", "after"})
            self.assertTrue(0 <= s.reward <= 1)

    def test_net_outcome_is_not_an_actuation_oracle(self):
        # Across predetermined independent exogenous events, net outcome must
        # sometimes disagree with whether the actuator moved toward zero.
        observed_confounds = 0
        for seed in range(50):
            w = Poltergeist(seed, "storm")
            w.reset()
            for _ in range(_LENGTH):
                before = w.position
                s = w.step("tap_a")
                if before and s.info["actuation"]:
                    actuator_helped = abs(before + s.info["actuation"]) < abs(before)
                    observed_confounds += (int(actuator_helped) != s.outcome)
        self.assertGreater(observed_confounds, 0)

    def test_heldout_variants_and_metric_contract(self):
        self.assertTrue(set(Poltergeist.heldout_variants).issubset(Poltergeist.variants))
        self.assertIn("reward", Poltergeist.atlas_metrics)
        for metric in Poltergeist.atlas_metrics:
            self.assertTrue(metric == "calib_gain" or metric in Poltergeist.metrics)
        with self.assertRaises(ValueError):
            Poltergeist(0, "nope")
        w = Poltergeist(0)
        w.reset()
        with self.assertRaises(ValueError):
            w.step("teleport")
