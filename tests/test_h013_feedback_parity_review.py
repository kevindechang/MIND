"""Adversarial information-parity regression for H013 PR #23.

Designed against exact source blob d326515a6f0592b6651f367f69720a30d51bab8b.
Two intentionally failing assertions expose missing public feedback information.
No full MIND checkout/runner/heldout run was available to the reviewer.
"""
import unittest
from mind.rivals.report_narrators import Transcript32Narrator


class TranscriptFeedbackParity(unittest.TestCase):
    def test_immediate_outcome_control(self):
        n = Transcript32Narrator()
        a = n.features({"dial": "0"}, 1.0, 1, False)
        b = n.features({"dial": "0"}, -1.0, 0, False)
        self.assertNotEqual(a, b)

    def test_lagged_observation_control(self):
        def trajectory(value):
            n = Transcript32Narrator()
            n.remember({"dial": value}, "tap_a")
            return n.features({"dial": "3"}, 0.0, None, False)
        self.assertNotEqual(trajectory("1"), trajectory("2"))

    def test_lagged_public_feedback_must_be_visible(self):
        def trajectory(prior_outcome):
            n = Transcript32Narrator()
            n.features({"dial": "1"}, 0.0, None, True)
            n.remember({"dial": "1"}, "tap_a")
            n.features({"dial": "2"}, 1.0 if prior_outcome else -1.0,
                       prior_outcome, False)
            n.remember({"dial": "2"}, "wait")
            return n.features({"dial": "3"}, 0.0, None, False)
        self.assertNotEqual(trajectory(1), trajectory(0))

    def test_current_public_reward_magnitude_must_be_visible(self):
        n = Transcript32Narrator()
        a = n.features({"dial": "0"}, 0.01, 1, False)
        b = n.features({"dial": "0"}, 100.0, 1, False)
        self.assertNotEqual(a, b)


if __name__ == "__main__":
    unittest.main()
