"""H013 report probe: broadcast readout vs transcript narrator, and replay.

The probe is read-only. These tests pin its contract: it names an action from
the broadcast alone, the narrator never sees that broadcast, a life scored with
the probe matches `runner.run` action for action, and death-and-restore leaves
both the actions and the report scores unchanged (the K01 property for a probe).
"""
import unittest

from mind.kernel import Organism
from mind.report import (Narrator, grounded_report, intention_in_broadcast, score_life)
from mind.runner import run

ACTIONS = ("wait", "a", "b", "c")


class ReportProbeTests(unittest.TestCase):
    def test_report_reads_intentions_and_ignores_confidence_labels(self):
        self.assertEqual(grounded_report(("goals:pending=a", "perception:bell=1"), ACTIONS), "a")
        self.assertEqual(
            grounded_report(("memory:was:request=b", "perception:bell=1", "perception:noise0=1"), ACTIONS),
            "b")
        # pending outranks a remembered request; broadcast order is workspace rank
        self.assertEqual(
            grounded_report(("goals:pending=c", "memory:was:request=a", "perception:bell=1"), ACTIONS),
            "c")
        # no act cue: the intention is not a claim about this tick
        self.assertEqual(grounded_report(("goals:pending=a", "perception:noise0=1"), ACTIONS), "wait")
        # self: is a confidence label, not the next action
        self.assertEqual(
            grounded_report(("self_model:self:a=sure", "perception:bell=1"), ACTIONS), "wait")
        self.assertEqual(
            grounded_report(("self_model:self:b=sure", "goals:pending=a", "perception:bell=1"), ACTIONS),
            "a")
        # an intention that is not legal cannot be the report
        self.assertEqual(grounded_report(("goals:pending=nope", "perception:bell=1"), ACTIONS), "wait")
        self.assertTrue(intention_in_broadcast(("goals:pending=a",), ACTIONS))
        self.assertFalse(intention_in_broadcast(("self_model:self:a=sure", "perception:bell=1"), ACTIONS))

    def test_narrator_uses_the_transcript_only(self):
        narrator = Narrator()
        self.assertEqual(narrator.predict({"bell": "1"}, ACTIONS), "wait")
        narrator.observe({"request": "b", "noise0": "1"})
        self.assertEqual(narrator.predict({"noise0": "0"}, ACTIONS), "wait")
        self.assertEqual(narrator.predict({"bell": "1", "noise0": "1"}, ACTIONS), "b")
        narrator.reset_episode()
        self.assertEqual(narrator.predict({"bell": "1"}, ACTIONS), "wait")
        # the current observation's request counts; a broadcast is not an argument
        self.assertEqual(narrator.predict({"request": "c", "bell": "1"}, ACTIONS), "c")

    def test_organism_broadcast_is_what_the_report_reads(self):
        actions = ACTIONS
        org = Organism("organism", seed=1)
        org.step({"request": "a", "noise0": "0", "noise1": "1"}, boundary=True, actions=actions)
        later = org.step({"bell": "1", "noise0": "1", "noise1": "0"}, actions=actions)
        self.assertIn("goals:pending=a", later.broadcast)
        self.assertEqual(grounded_report(later.broadcast, actions), "a")

    def test_access_cut_keeps_the_intention_reportable(self):
        actions = ACTIONS
        cut = Organism("organism cut:memory>policy cut:goals>policy", seed=1)
        cut.step({"request": "a", "noise0": "0", "noise1": "1"}, boundary=True, actions=actions)
        later = cut.step({"bell": "1", "noise0": "1", "noise1": "0"}, actions=actions)
        self.assertIn("goals:pending=a", later.broadcast)
        self.assertEqual(grounded_report(later.broadcast, actions), "a")
        delivered = [c.source for c in cut._view("policy", cut.prev.broadcast)]
        self.assertNotIn("goals", delivered)
        self.assertNotIn("memory", delivered)

    def test_scored_life_matches_the_runner_and_replays(self):
        scored = score_life("organism", "vigil", 2, 12, trace=True)
        again = score_life("organism", "vigil", 2, 12, trace=True)
        died = score_life("organism", "vigil", 2, 12, kill_at=(0, 3, 8, 15), trace=True)
        ref = run("organism", "vigil", 2, 12, trace=True)
        self.assertEqual(scored["trace"], ref["trace"])
        self.assertEqual(scored["trace"], again["trace"])
        self.assertEqual(scored["trace"], died["trace"])
        for key in ("grounded", "narrator", "reportable", "held", "n"):
            self.assertEqual(scored[key], died[key], key)
        cut = score_life("organism cut:memory>policy cut:goals>policy", "vigil", 2, 12,
                         kill_at=(1, 6, 11), trace=True)
        cut_ref = run("organism cut:memory>policy cut:goals>policy", "vigil", 2, 12, trace=True)
        self.assertEqual(cut["trace"], cut_ref["trace"])

    def test_narrator_rival_keeps_every_vigil_commitment(self):
        life = run("rival:narrator", "vigil", 0, 40)
        self.assertEqual(life["metrics"]["kept@all"], 1.0)
        self.assertEqual(life["metrics"]["false_starts@all"], 0.0)
        with self.assertRaises(ValueError):
            run("rival:narrator", "outage", 0, 2)


if __name__ == "__main__":
    unittest.main()
