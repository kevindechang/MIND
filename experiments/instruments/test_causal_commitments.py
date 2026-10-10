"""Unittest checks for CausalWorkshop - standard library only."""
import unittest
from dataclasses import replace
from causal_commitments import CausalWorkshop, full_experiment


class WorkshopTests(unittest.TestCase):
    def test_oracle_parity_across_100_worlds(self):
        for seed in range(100):
            with self.subTest(seed=seed):
                w, feedback, commitments = full_experiment(seed)
                self.assertEqual(w.oracle(), w.oracle_from_observations(feedback, commitments))

    def test_out_of_order_feedback_and_unique_tags(self):
        w = CausalWorkshop(123, 6)
        events = []
        for n, d in [(0, 3), (1, 1), (2, 2), (3, 1), (4, 3), (5, 2)]:
            events.extend(w.probe(n, d))
        events.extend(w.drain())
        self.assertEqual({e.action for e in events}, set(range(6)))
        self.assertEqual(len({e.event_id for e in events}), 6)
        self.assertEqual(w.pending, 0)
        self.assertEqual({e.phase for e in events}, {0})

    def test_incomplete_history_not_scored(self):
        w, obs, commitments = full_experiment(3)
        with self.assertRaisesRegex(ValueError, "all interventions"):
            w.oracle_from_partial_observations(obs[:-1], commitments)

    def test_reset_before_drain_rejected(self):
        w = CausalWorkshop(3)
        w.probe(0, 3)
        with self.assertRaises(ValueError):
            w.hard_reset()

    def test_probes_after_reset_rejected(self):
        w, _, _ = full_experiment(4)
        with self.assertRaisesRegex(ValueError, "no diagnostics"):
            w.probe(2)

    def test_unknown_oracle_source_not_exposed(self):
        _, feedback, _ = full_experiment(5)
        self.assertEqual(set(feedback[0].__dataclass_fields__),
                         {"event_id", "action", "affected_mask", "due_tick", "phase"})
        self.assertFalse(hasattr(feedback[0], "_edges"))

    def test_memory_matters_on_some_matched_worlds(self):
        found = False
        for seed in range(200):
            w, feedback, commits = full_experiment(seed)
            if w.oracle(commits).plan != w.oracle(commits[:-1]).plan:
                self.assertEqual(w.oracle_from_observations(feedback, commits),
                                 w.oracle(commits))
                self.assertNotEqual(
                    w.oracle_from_observations(feedback, commits[:-1]).plan,
                    w.oracle(commits).plan)
                found = True
                break
        self.assertTrue(found, "no informative paired case generated")

    def test_corrupted_event_rejected(self):
        w, feedback, commits = full_experiment(7)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            w.oracle_from_observations(feedback + [feedback[0]], commits)
        with self.assertRaisesRegex(ValueError, "bad phase"):
            w.oracle_from_observations([replace(feedback[0], phase=1)] + feedback[1:], commits)

    def test_missing_or_duplicate_commitments(self):
        w = CausalWorkshop(4)
        w.commit(2, 1, 5)
        with self.assertRaises(ValueError):
            w.commit(2, 0, 4)
        with self.assertRaises(ValueError):
            w.commit(1, 2, 4)
        with self.assertRaises(ValueError):
            w.commit(-1, 0, 4)

    def test_replay_determinism(self):
        a = full_experiment(17)
        b = full_experiment(17)
        self.assertEqual(a[1:], b[1:])
        self.assertEqual(a[0].oracle(), b[0].oracle())


if __name__ == "__main__":
    unittest.main()
