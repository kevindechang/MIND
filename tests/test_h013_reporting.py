"""H013 design tests. Requires full MIND checkout; NOT_EXECUTED in design mode."""
import math
import unittest

from mind.kernel import Organism
from mind.rivals.report_learner import OnlineActionReadout
from mind.rivals.report_narrators import BroadcastNarrator, Transcript32Narrator
from mind.rivals.report_interventions import _cut_fork
from mind.rivals.reporting import run_report_probe


class ReportReadoutTests(unittest.TestCase):
    def test_predict_then_learn_no_current_action_leak(self):
        learner = OnlineActionReadout()
        features = ("broadcast:goals:pending=a",)
        prior = learner.predict(features, ("wait", "a"))
        self.assertAlmostEqual(prior["a"], 0.5)
        learner.learn(features, "a", prior)
        updated = learner.predict(features, ("wait", "a"))
        self.assertGreater(updated["a"], prior["a"])
        self.assertAlmostEqual(sum(updated.values()), 1.0)

    def test_readout_order_is_deterministic(self):
        a, b = OnlineActionReadout(), OnlineActionReadout()
        for learner, feats in ((a, ["z", "a"]), (b, ["a", "z"])):
            p = learner.predict(feats, ("wait", "a"))
            learner.learn(feats, "a", p)
        self.assertEqual(a.weights, b.weights)

    def test_transcript_rival_uses_public_history_and_resets(self):
        narrator = Transcript32Narrator()
        narrator.remember({"x": "1"}, "a")
        feats = narrator.features({"y": "2"}, 1.0, 1, False)
        self.assertIn("lag1:action=a", feats)
        self.assertIn("lag1:x=1", feats)
        self.assertIn("previous_outcome=1", feats)
        new_episode = narrator.features({"z": "3"}, 0.0, None, True)
        self.assertFalse(any(x.startswith("lag") for x in new_episode))
        self.assertNotIn("previous_outcome=1", new_episode)

    def test_broadcast_features_contain_no_action_label(self):
        features = BroadcastNarrator.features(("goals:pending=a", "memory:was:request=a"))
        self.assertEqual(len(features), 2)
        self.assertTrue(all(f.startswith("broadcast:") for f in features))

    def test_causal_cut_is_not_a_broadcast_knockout(self):
        org = Organism("organism", 0)
        org.step({"request": "a"}, boundary=True, actions=("wait", "a"))
        from copy import deepcopy
        before = deepcopy(org)
        decision = org.step({"bell": "1"}, actions=("wait", "a"))
        cut_action, sham_action = _cut_fork(before, {"bell": "1"}, 0.0, None, False,
                                            ("wait", "a"), decision.action, decision.broadcast)
        self.assertIn(cut_action, ("wait", "a"))
        self.assertEqual(sham_action, decision.action)
        self.assertEqual(org.t, 2)

    def test_invalid_world_is_rejected(self):
        with self.assertRaises(ValueError):
            run_report_probe(0, "workshop", "dev", episodes=4)

    def test_short_world_runs_are_deterministic(self):
        a = run_report_probe(0, "vigil", "long", episodes=20, probe_every=2)
        b = run_report_probe(0, "vigil", "long", episodes=20, probe_every=2)
        self.assertEqual(a, b)
        self.assertGreater(a["scored"], 0)
        self.assertGreater(a["probes"], 0)
        self.assertTrue(math.isfinite(a["report_gain"]))

    def test_second_world_runs_without_private_info(self):
        row = run_report_probe(1, "outage", "silent", episodes=20, probe_every=2)
        self.assertGreater(row["scored"], 0)
        self.assertGreater(row["probes"], 0)
        self.assertEqual(row["sham_changed"], 0)


if __name__ == "__main__":
    unittest.main()
