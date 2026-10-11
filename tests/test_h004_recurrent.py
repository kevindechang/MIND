"""H004 recurrent organ: causal access, replay and negative controls."""
import unittest

from mind.kernel import Config, Organism
from mind.ledger import MemoryLedger
from mind.organs.recurrent import Recurrent, projection
from mind.rivals import RIVALS


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
        first = original.step({"bell": "1"}, actions=("wait", "a"))
        second = restored.step({"bell": "1"}, actions=("wait", "a"))
        self.assertEqual(first, second)

    def test_rejects_invalid_config(self):
        for params in ({"width": 0}, {"width": 17}, {"decay": 1.0},
                       {"decay": -0.1}, {"threshold": 0.0}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                Recurrent(params)

    def test_long_context_rivals_exist(self):
        self.assertIn("window16", RIVALS)
        self.assertIn("window32lin", RIVALS)
        self.assertIn("recurrent", RIVALS["window16"].challenges)
        self.assertIn("recurrent", RIVALS["window32lin"].challenges)


if __name__ == "__main__":
    unittest.main()
