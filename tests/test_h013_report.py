"""Design and regression tests for H013 action-report readouts.

These tests must run in a full git checkout; a syntax-only inspection is not
a substitute for executing them.
"""
import unittest

from mind.kernel import Organism
from mind.rivals.report_probe import run_report_probe
from mind.rivals.report_readout import Decoder, PublicTranscript
from mind.runner import RESULT_CODE


class H013ReportTests(unittest.TestCase):
    def test_decoder_is_prequential_and_proper(self):
        d = Decoder()
        f = ("bias", "request=a")
        p = d.forecast(f, ("a", "b"))
        self.assertAlmostEqual(p["a"], 0.5)
        self.assertAlmostEqual(d.brier(p, "a"), 0.25)
        d.learn(f, ("a", "b"), "a", p)
        q = d.forecast(f, ("a", "b"))
        self.assertGreater(q["a"], p["a"])
        self.assertAlmostEqual(sum(q.values()), 1.0)

    def test_transcript_contains_only_past_action_labels(self):
        h = PublicTranscript()
        before = h.features({"request": "a"}, 0.0, None, ("wait", "a"))
        self.assertFalse(any("lag1:action" in f for f in before))
        h.observe({"request": "a"}, "wait", 0.0, None)
        after = h.features({}, 0.0, None, ("wait", "a"))
        self.assertIn("lag1:action=wait", after)
        self.assertIn("lag1:request=a", after)
        h.reset_episode()
        new = h.features({}, 0.0, None, ("wait", "a"))
        self.assertFalse(any("lag1:" in f for f in new))
        self.assertIn("total:act:wait=1", new)

    def test_workspace_remains_reportable_under_policy_cut(self):
        cfg = ("organism capacity=inf policy.eps=0 policy.eps_min=0 "
               "cut:goals>policy cut:memory>policy")
        a = Organism(cfg, seed=1)
        a.step({"request": "a"}, boundary=True, actions=("wait", "a"))
        d = a.step({}, actions=("wait", "a"))
        self.assertIn("goals:pending=a", d.broadcast)
        self.assertFalse(any(x.source == "goals" for x in a._view(
            "policy", a.prev.broadcast)))

    def test_cut_and_intact_training_streams_match(self):
        intact = run_report_probe("vigil", "dev", 7, episodes=4, train_episodes=2)
        cut = run_report_probe("vigil", "dev", 7, episodes=4, train_episodes=2, cut=True)
        self.assertEqual(intact["training_digest"], cut["training_digest"])
        self.assertGreater(intact["steps"], 0)
        self.assertGreater(cut["steps"], 0)

    def test_probe_is_deterministic(self):
        a = run_report_probe("vigil", "crowded", 4, episodes=3, train_episodes=1)
        b = run_report_probe("vigil", "crowded", 4, episodes=3, train_episodes=1)
        self.assertEqual(a, b)

    def test_probe_is_result_affecting_code(self):
        self.assertIn("mind/rivals/*.py", RESULT_CODE)

    def test_bad_train_test_split_is_rejected(self):
        with self.assertRaises(ValueError):
            run_report_probe("vigil", "dev", 1, episodes=2, train_episodes=2)


if __name__ == "__main__":
    unittest.main()
