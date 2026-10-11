"""H004 recurrent organ: causal access, replay and negative controls."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

from mind.kernel import Config, Organism
from mind.ledger import MemoryLedger
from mind.organs.recurrent import Recurrent, projection
from mind.rivals import RIVALS, FeedbackTranscript


class RecurrentTests(unittest.TestCase):
    def test_projection_is_stable_and_signed(self):
        self.assertEqual(projection("request=a", 0), projection("request=a", 0))
        self.assertIn(projection("request=a", 2), (-1.0, 1.0))

    def test_new_organ_is_optional_and_lesionable(self):
        self.assertNotIn("recurrent", Config.parse("organism").organs)
        self.assertIn("recurrent", Config.parse("organism +recurrent").organs)
        scheduled = Config.parse("organism +recurrent @1:-recurrent")
        self.assertIn((1, "-recurrent"), scheduled.schedule)
        with self.assertRaises(ValueError):
            Config.parse("organism cut:recurrent>policy")

    def test_proposals_encode_previous_not_current_tick(self):
        agent = Organism("organism +recurrent capacity=inf explore=0", seed=11)
        first = agent.step({"request": "a"}, actions=("wait", "a"))
        self.assertFalse(any(x.startswith("recurrent:") for x in first.broadcast))
        second = agent.step({}, actions=("wait", "a"))
        self.assertTrue(any(x.startswith("recurrent:trace") for x in second.broadcast))

    def test_does_not_read_unattended_percepts(self):
        agent = Organism("organism +recurrent capacity=0 explore=0", seed=12)
        agent.step({"request": "a"}, actions=("wait", "a"))
        self.assertEqual(agent.organs["recurrent"].introspect()["trace"], [0.0] * 4)
        second = agent.step({}, actions=("wait", "a"))
        self.assertFalse(any(x.startswith("recurrent:") for x in second.broadcast))

    def test_cut_perception_to_recurrence_prevents_evidence_copy(self):
        agent = Organism("organism +recurrent cut:perception>recurrent capacity=inf explore=0")
        agent.step({"request": "b"}, boundary=True, actions=("wait", "b"))
        agent.step({"noise": "1"}, actions=("wait", "b"))
        self.assertEqual(agent.organs["recurrent"].introspect()["trace"], [0.0] * 4)

    def test_recurrent_exactly_once_retry_does_not_reappend(self):
        ledger = MemoryLedger()
        agent = Organism("organism +recurrent", seed=17, ledger=ledger)
        first = agent.step_at(0, {"request": "a"}, boundary=True, actions=("wait", "a"))
        first_head = ledger.head
        restored = Organism.restore(ledger)
        duplicate = restored.step_at(0, {"request": "a"}, boundary=True, actions=("wait", "a"))
        self.assertEqual(first, duplicate)
        self.assertEqual(ledger.head, first_head)
        self.assertEqual(len(ledger), 2)  # genesis + committed tick

    def test_hashseed_invariant_recurrence_in_new_processes(self):
        # K06-style check for the OPTIONAL organ: default-organ claims do not
        # exercise +recurrent, so this explicitly tests cross-process replay.
        script = """
import json
from mind.kernel import Organism
from mind.ledger import MemoryLedger
ledger = MemoryLedger()
agent = Organism("organism +recurrent capacity=4 explore=0.25", seed=83, ledger=ledger)
actions = []
for t in range(14):
    action = agent.step(
        {"request": "a"} if t == 0 else {"noise": str(t % 2)},
        outcome=None, boundary=(t == 0),
        actions=("wait", "a", "b")
    ).action
    actions.append(action)
restored = Organism.restore(ledger)
print(json.dumps({"head": ledger.head, "actions": actions,
                  "trace": restored.introspect()["recurrent"]}, sort_keys=True))
"""
        root = Path(__file__).resolve().parents[1]
        outputs = []
        for seed in ("1", "71", "919"):
            env = dict(os.environ, PYTHONHASHSEED=seed)
            completed = subprocess.run(
                [sys.executable, "-c", script], cwd=root, env=env,
                text=True, capture_output=True, check=True,
            )
            outputs.append(json.loads(completed.stdout))
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0], outputs[2])

    def test_frozen_recurrence_never_updates(self):
        agent = Organism("organism +recurrent freeze:recurrent capacity=inf explore=0")
        agent.step({"request": "b"}, actions=("wait", "b"))
        self.assertEqual(agent.organs["recurrent"].introspect()["trace"], [0.0] * 4)

    def test_access_cut_blocks_only_policy_view(self):
        agent = Organism("organism +recurrent cut:recurrent>policy capacity=inf explore=0")
        agent.step({"request": "a"}, actions=("wait", "a"))
        agent.step({}, actions=("wait", "a"))
        self.assertTrue(any(c.source == "recurrent" for c in agent.prev.broadcast))
        self.assertFalse(any(c.source == "recurrent"
                             for c in agent._view("policy", agent.prev.broadcast)))
        self.assertTrue(any(c.source == "recurrent"
                            for c in agent._view("memory", agent.prev.broadcast)))

    def test_episode_boundary_clears_state(self):
        agent = Organism("organism +recurrent capacity=inf explore=0")
        agent.step({"request": "a"}, boundary=True, actions=("wait", "a"))
        agent.end_episode()
        new = agent.step({}, boundary=True, actions=("wait", "a"))
        self.assertFalse(any(x.startswith("recurrent:") for x in new.broadcast))

    def test_restore_recovers_same_state_and_next_action(self):
        ledger = MemoryLedger()
        original = Organism("organism +recurrent capacity=inf explore=0", seed=23, ledger=ledger)
        original.step({"request": "a"}, boundary=True, actions=("wait", "a"))
        original.step({"noise": "0"}, actions=("wait", "a"))
        restored = Organism.restore(ledger)
        self.assertEqual(original.introspect(), restored.introspect())
        self.assertEqual(original.t, restored.t)
        # The two continuations must not both append to the same ledger.
        restored.ledger = None
        first = original.step({"bell": "1"}, actions=("wait", "a"))
        second = restored.step({"bell": "1"}, actions=("wait", "a"))
        self.assertEqual(first, second)

    def test_rejects_invalid_config(self):
        for params in ({"width": 0}, {"width": 17}, {"decay": 1.0},
                       {"decay": -0.1}, {"threshold": 0.0}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                Recurrent(params)

    def test_long_context_rivals_exist(self):
        for name in ("window16", "window32lin", "window16fb", "window32fb_lin"):
            with self.subTest(name=name):
                self.assertIn(name, RIVALS)
                self.assertIn("recurrent", RIVALS[name].challenges)

    def test_feedback_rival_receives_previous_action_outcome_as_policy_feature(self):
        rival = FeedbackTranscript(16, seed=31)
        rival.step({"request": "a"}, boundary=True, actions=("wait", "a"))
        first_action = rival.prev_action
        rival.step({"bell": "1"}, outcome=1, actions=("wait", "a"))
        self.assertEqual(rival.history[-1]["previous_action_outcome"], f"{first_action}:1")
        self.assertIn(f"lag0:previous_action_outcome={first_action}:1", rival.prev_feats)

    def test_feedback_rival_never_invents_outcomes_or_crosses_episode_boundary(self):
        rival = FeedbackTranscript(16, seed=13)
        rival.step({"request": "b"}, boundary=True, actions=("wait", "b"))
        rival.step({}, outcome=None, actions=("wait", "b"))
        self.assertNotIn("previous_action_outcome", rival.history[-1])
        # A boundary is a new episode, so no old action/outcome enters features.
        rival.step({"request": "a"}, outcome=1, boundary=True, actions=("wait", "a"))
        self.assertNotIn("previous_action_outcome", rival.history[-1])
        self.assertEqual(len(rival.history), 1)

    def test_feedback_rival_is_stronger_information_control_not_oracle(self):
        # A new rival gets previous public action/outcome as an input feature;
        # it must not read private world labels, and shares the actual TD learner.
        rival = RIVALS["window16fb"].factory("outage", "silent", 7)
        self.assertIsInstance(rival, FeedbackTranscript)
        self.assertTrue(rival.pairs)
        self.assertEqual(rival.k, 16)


if __name__ == "__main__":
    unittest.main()
