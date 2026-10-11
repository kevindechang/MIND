"""C020 instrument counterexample: a public-only reporter can satisfy its cut contrast.

This is a logical negative control, NOT an empirical refutation of C020's
observed MIND-world numbers. score_life and both reporters are unmodified.
The fixture deliberately changes the policy's action without changing either
reporter's information, demonstrating that a report-accuracy drop alone does
not identify a self-report-specific causal path.
"""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from mind.report import score_life


class TwoTickWorld:
    def reset(self):
        self.tick = 0
        return {"request": "a"}

    def legal(self):
        return ("wait", "a")

    def step(self, action):
        self.tick += 1
        if self.tick == 1:
            return SimpleNamespace(obs={"bell": "1"}, reward=0.0, outcome=None, done=False)
        if self.tick == 2:
            return SimpleNamespace(obs={}, reward=1.0, outcome=True, done=True)
        raise AssertionError("unexpected tick")


class ControlledAgent:
    def __init__(self, arm):
        self.arm = arm

    def introspect(self):
        return {"goals": {"pending": ("a",)}, "memory": {"remembered": ()}}

    def step(self, obs, reward, outcome, boundary, actions):
        from mind.kernel import Decision
        if obs.get("bell") != "1":
            return Decision("wait", None, ("perception:request=a",))
        # Broadcast is identical across arms; only the policy changes.
        action = "wait" if "cut:" in self.arm else "a"
        return Decision(action, None, ("perception:bell=1", "goals:pending=a"))

    def end_episode(self, reward, outcome):
        pass


class C020PublicControl(unittest.TestCase):
    def test_public_narrator_has_same_dissociation_as_broadcast_report(self):
        with patch("mind.report.Organism", ControlledAgent), \
             patch("mind.runner.make_agent", side_effect=lambda arm, *args: ControlledAgent(arm)), \
             patch("mind.worlds.make_world", side_effect=lambda *args: TwoTickWorld()):
            intact = score_life("organism", "vigil", 0, 64)
            cut = score_life("organism cut:goals>policy cut:memory>policy cut:self_model>policy",
                             "vigil", 0, 64)
            sham = score_life("organism no-lesion", "vigil", 0, 64)
        g_drop = intact["grounded"] - cut["grounded"]
        n_drop = intact["narrator"] - cut["narrator"]
        self.assertEqual(g_drop, 1.0)
        self.assertEqual(n_drop, 1.0)
        self.assertEqual(g_drop - n_drop, 0.0)
        self.assertGreater(g_drop, 0.25)
        self.assertEqual(intact["reportable"], cut["reportable"])
        self.assertEqual(cut["reportable"], 1.0)
        self.assertEqual(sham, intact)
        print("H013 C020 NEGATIVE CONTROL: grounded_drop=1.0, "
              "public_narrator_drop=1.0, differential=0.0; reportable=1.0 both")


if __name__ == "__main__":
    unittest.main()
