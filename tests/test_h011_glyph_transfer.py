"""H011 world/organ integration tests; full-repository execution pending."""
import unittest
from types import SimpleNamespace
from mind.kernel import Config
from mind.ledger import MemoryLedger
from mind.organs.analogy import Analogy
from mind.rivals import RIVALS
from mind.runner import run
from mind.worlds import WORLDS, make_world

class GlyphTests(unittest.TestCase):
    def test_registry(self):
        self.assertIn("glyph", WORLDS)
        self.assertIn("analogy", Config.parse("organism +analogy").organs)
        self.assertNotIn("analogy", Config.parse("organism").organs)
        self.assertEqual(RIVALS["equality"].worlds, ("glyph",))
        self.assertNotIn("glyph", RIVALS["bayes"].worlds)

    def test_action_independent_streams(self):
        for variant in ("dev", "shift"):
            a, b = make_world("glyph", 19, variant), make_world("glyph", 19, variant)
            for _ in range(200):
                self.assertEqual(a.reset(), b.reset())
                self.assertEqual(a.step("press_a").info, b.step("press_b").info)

    def test_disjoint_train_transfer_alphabets(self):
        for variant in ("dev", "shift"):
            env = make_world("glyph", 8, variant)
            train, transfer = set(), set()
            for episode in range(200):
                obs = env.reset()
                self.assertFalse({"rule", "same", "phase", "expected"} & set(obs))
                (train if episode < 100 else transfer).update((obs["sample"], obs["candidate"]))
                step = env.step("press_a")
                self.assertEqual(step.obs, {})
            self.assertFalse(train & transfer)

    def test_public_equality_is_symbol_invariant(self):
        organ = Analogy({})
        for a, b, expected in (("old001", "old001", "1"), ("Y-01", "Y-02", "0")):
            p = organ.propose(SimpleNamespace(obs={"sample": a, "candidate": b}), None)
            self.assertEqual((p[0].source, p[0].key, p[0].value), ("analogy", "equal", expected))

    def test_replay(self):
        a = run("organism +analogy", "glyph", 3, 24, ledger=MemoryLedger(), trace=True)
        b = run("organism +analogy", "glyph", 3, 24, kill_at=[0, 5, 13], trace=True)
        self.assertEqual((a["trace"], a["head"]), (b["trace"], b["head"]))

    def test_rival_receives_public_observations(self):
        rival = RIVALS["equality"].factory("glyph", "dev", 3)
        d = rival.step({"sample": "x", "candidate": "x"}, boundary=True,
                       actions=("press_a", "press_b"))
        self.assertIn(d.action, ("press_a", "press_b"))
        rival.end_episode(1.0, 1)

if __name__ == "__main__":
    unittest.main()
