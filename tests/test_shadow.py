"""Shadow replay (mind/shadow.py): exact reproduction, filters, shams and refusals."""
import unittest

from mind.kernel import Content
from mind.ledger import MemoryLedger
from mind.runner import RESULT_CODE, run
from mind.shadow import content_from_tag, fixed_behaviour, late_brier, replay_self_model, sham_audit


def life(arm="organism", world="vigil", seed=3, episodes=40, variant="dev"):
    ledger = MemoryLedger()
    result = run(arm, world, seed, episodes, variant, ledger=ledger)
    return result, list(ledger)


class ShadowTest(unittest.TestCase):
    def test_unfiltered_shadow_reproduces_every_logged_confidence(self):
        for world in ("vigil", "outage", "workshop"):
            for arm in ("organism", "organism cut:memory>self_model", "organism self_model.lr=0.3"):
                result, events = life(arm, world)
                forecasts = replay_self_model(events)
                self.assertTrue(forecasts)
                self.assertTrue(all(f.confidence == f.logged for f in forecasts), (world, arm))
                n = result["episodes"]
                self.assertEqual(late_brier(forecasts, n), result["metrics"]["brier"])
                self.assertEqual(late_brier(forecasts, n, table=True), result["metrics"]["brier_table"])

    def test_a_ledger_does_not_change_the_life(self):
        r = fixed_behaviour("organism", "outage", 5, 30)
        self.assertTrue(r["exact"])
        self.assertEqual(r["metrics"], run("organism", "outage", 5, 30)["metrics"])

    def test_tags_round_trip(self):
        for c in (Content("memory", "was:result", "scan:ok", 0.3), Content("self_model", "self:do:01", "sure", 0.5),
                  Content("perception", "fx0", "012", 0.9)):
            self.assertEqual(content_from_tag(c.tag).tag, c.tag)

    def test_filtering_an_absent_source_changes_nothing(self):
        _, events = life(world="outage")          # outage never makes requests, so goals stay silent
        full = replay_self_model(events)
        self.assertEqual(full, replay_self_model(events, drop=("goals",)))
        self.assertEqual(full, replay_self_model(events, sham=("goals",)))

    def test_drop_and_sham_change_forecasts_but_not_events(self):
        _, events = life()
        full = replay_self_model(events)
        for spec in ({"drop": ("memory",)}, {"sham": ("memory",)}, {"drop": ("perception",)}):
            other = replay_self_model(events, **spec)
            self.assertEqual([(f.episode, f.action, f.outcome) for f in other],
                             [(f.episode, f.action, f.outcome) for f in full])
            self.assertNotEqual([f.confidence for f in other], [f.confidence for f in full], spec)

    def test_sham_keeps_presence_and_feature_load_with_intermittent_goals(self):
        # PR #29 review (P1): goals are present on only part of vigil's ticks, so a sham drawn
        # from earlier broadcasts used to inject or remove them and change the self-model's
        # feature count (its step is lr / len(feats)). The sham must change content only.
        result, events = life(world="vigil", seed=4, episodes=120)
        audit = []
        replay_self_model(events, sham=("goals",), audit=audit)
        present = [a for a in audit if a["real"]]
        self.assertTrue(present and len(present) < len(audit), "goals must be intermittent in this life")
        for a in audit:
            self.assertEqual(bool(a["real"]), bool(a["sham"]), a)
            self.assertEqual(len(a["real"]), len(a["sham"]), a)
            self.assertEqual(a["features_real"], a["features_sham"], a)
        self.assertTrue(any(a["real"] != a["sham"] for a in present))
        summary = sham_audit(events, "goals", result["episodes"])
        self.assertTrue(summary["presence_kept"] and summary["count_kept"] and summary["load_kept"])
        self.assertEqual(summary["fallback_scored"], 0)

    def test_sham_keeps_a_variable_number_of_memory_contents(self):
        result, events = life(world="outage", seed=2, episodes=60)
        summary = sham_audit(events, "memory", result["episodes"])
        counts = {len(a["real"]) for a in self._audit(events, "memory")}
        self.assertGreater(len(counts), 2, "memory's content count must vary in this life")
        self.assertTrue(summary["presence_kept"] and summary["count_kept"] and summary["load_kept"], summary)
        self.assertGreater(summary["changed"], 0)
        self.assertEqual(summary["fallback_scored"], 0)

    @staticmethod
    def _audit(events, name):
        audit = []
        replay_self_model(events, sham=(name,), audit=audit)
        return audit

    def test_sham_is_deterministic(self):
        _, events = life()
        self.assertEqual(replay_self_model(events, sham=("goals",)), replay_self_model(events, sham=("goals",)))

    def test_refusals(self):
        _, events = life()
        with self.assertRaises(ValueError):
            replay_self_model(events, drop=("memory",), sham=("memory",))
        with self.assertRaises(ValueError):
            replay_self_model(events, drop=("memroy",))
        with self.assertRaises(ValueError):
            replay_self_model(events, drop=("self_model",))
        for arm in ("organism -self_model", "organism @5:freeze:self_model", "organism @5:-memory"):
            _, other = life(arm)
            with self.assertRaises(ValueError):
                replay_self_model(other)
        with self.assertRaises(ValueError):
            fixed_behaviour("rival:window4", "vigil", 1, 10)    # transcript rivals keep no ledger

    def test_shadow_is_result_code(self):
        self.assertIn("mind/shadow.py", RESULT_CODE)


if __name__ == "__main__":
    unittest.main()
