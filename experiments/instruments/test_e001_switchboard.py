"""Behavioral and negative-control tests for E001 instrument."""
import unittest
from e001_switchboard import (DIAGNOSTICS, PROBE, Event, Switchboard,
                              diagnostic_episode, exhaustive_oracle_check,
                              reconstruct_rule, target)


class TestSwitchboard(unittest.TestCase):
    def test_exhaustive_inversion_and_phase_transition(self):
        self.assertEqual(exhaustive_oracle_check(), (768, 64))

    def test_no_feedback_before_due_step(self):
        w = Switchboard(((0, 1, 0), (0, 1, 0)))
        self.assertEqual(w.act((0, 0), 1, delay=2), [])
        self.assertEqual(w.pending, 1)
        delivered = w.advance()
        self.assertEqual(len(delivered), 1)
        self.assertEqual(delivered[0].event_id, 1)
        self.assertEqual(delivered[0].due_step, 2)

    def test_pending_feedback_blocks_phase_change(self):
        w = Switchboard(((0, 0, 0), (0, 0, 1)))
        w.act((0, 0), 1, delay=2)
        with self.assertRaises(ValueError):
            w.transition()
        w.flush()
        w.transition()
        self.assertEqual(w.phase, 1)

    def test_wrong_phase_rejected(self):
        w = Switchboard(((0, 0, 0), (1, 0, 1)))
        rec = diagnostic_episode(w, 0, (0, 0, 1), DIAGNOSTICS, delay=2)
        with self.assertRaisesRegex(ValueError, "phase mismatch"):
            reconstruct_rule(rec, 1)

    def test_missing_and_duplicate_diagnostics_rejected(self):
        w = Switchboard(((1, 0, 1), (1, 0, 1)))
        rec = diagnostic_episode(w, 0, (1, 1, 0), DIAGNOSTICS, delay=1)
        with self.assertRaisesRegex(ValueError, "three distinct"):
            reconstruct_rule(rec[:-1], 0)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            reconstruct_rule(rec + [rec[0]], 0)

    def test_probe_feedback_cannot_be_used_as_diagnostic(self):
        w = Switchboard(((1, 1, 0), (1, 1, 0)))
        rec = diagnostic_episode(w, 0, (0, 0, 0), DIAGNOSTICS, delay=1)
        fake_probe = Event(99, 0, PROBE, 0, 1, 99)
        with self.assertRaisesRegex(ValueError, "probe event"):
            reconstruct_rule(rec + [fake_probe], 0)

    def test_invalid_bit_rejected(self):
        with self.assertRaises(ValueError):
            target((1, 2, 0), (0, 1))
        with self.assertRaises(ValueError):
            target((1, 0, 0), (0, -1))


if __name__ == "__main__":
    unittest.main()
