"""Receiver selection must learn prequentially, preserve events, and replay exactly."""
import copy
import math
import pickle
from types import SimpleNamespace
import unittest

from mind.kernel import Config, Content
from mind.ledger import MemoryLedger
from mind.organs.self_model import SelfModel
from mind.runner import run
from mind.shadow import replay_self_model


class SelectiveSelfModelTests(unittest.TestCase):
    def require_options(self):
        self.assertIn("step", SelfModel.defaults)
        self.assertIn("gate", SelfModel.defaults)

    def test_options_and_typos(self):
        self.require_options()
        Config.parse("organism self_model.step=adagrad self_model.gate=learned")
        for arg in ("step=adgard", "gate=learnd"):
            with self.assertRaises(ValueError):
                Config.parse("organism self_model." + arg)

    def test_default_update_and_adagrad_coordinate_history(self):
        self.require_options()
        default = SelfModel({})
        default._update("a", ["bias", "x"], 1)
        self.assertEqual(default.w, {("a", "bias"): 0.15, ("a", "x"): 0.15})
        model = SelfModel({"step": "adagrad"})
        model._update("a", ["bias"], 1)
        first = 0.6 * 0.5 / (math.sqrt(0.25) + 1e-8)
        self.assertAlmostEqual(model.w[("a", "bias")], first)
        grad = 1 - 1 / (1 + math.exp(-first))
        model._update("a", ["bias", "new"], 1)
        old_change = model.w[("a", "bias")] - first
        self.assertAlmostEqual(old_change, 0.6 * grad / (math.sqrt(0.25 + grad**2) + 1e-8))
        self.assertGreater(model.w[("a", "new")], old_change)

    def test_fixed_filter_matches_an_external_cut_including_feature_collision(self):
        self.require_options()
        filtered, manual = SelfModel({"gate": "no_memory"}), SelfModel({})
        for i in range(8):
            # Sources may share feature strings: filter sources before deduplication.
            view = (Content("memory", "same", str(i % 2), 1),
                    Content("perception", "same", str(i % 2), 1))
            cut = tuple(c for c in view if c.source != "memory")
            for m, v in ((filtered, view), (manual, cut)):
                m.learn(None, SimpleNamespace(outcome=None), v, None)
                m.after_act(None, v, "a", None)
                m.learn_terminal(SimpleNamespace(action="a"), 0, i % 2, None)
            self.assertEqual(filtered.forecast(view, "a"), manual.forecast(cut, "a"))
            self.assertEqual(filtered.w, manual.w)

    def test_gate_uses_only_pre_outcome_predictions_and_reads_are_pure(self):
        self.require_options()
        model = SelfModel({"gate": "learned"})
        for i in range(40):
            outcome = i % 2
            view = (Content("memory", "cue", str(outcome), 1),)
            model.learn(None, SimpleNamespace(outcome=None), view, None)
            before = pickle.dumps(model.__dict__)
            model.forecast(view, "a")
            model.propose(None, None)
            self.assertEqual(before, pickle.dumps(model.__dict__))
            model.after_act(None, view, "a", None)
            predictions = list(model.expert_predictions)
            old = list(model.losses.get("a", [0.0] * len(predictions)))
            model.learn_terminal(SimpleNamespace(action="a"), 0, outcome, None)
            self.assertEqual(model.losses["a"], [l + (p - outcome)**2 for l, p in zip(old, predictions)])
        weights = model.gate_weights("a")
        self.assertAlmostEqual(sum(weights), 1)
        self.assertGreater(weights[0], weights[-1])  # informative cue beats a bias-only expert

    def test_uniform_control_trains_the_same_experts(self):
        self.require_options()
        models = [SelfModel({"gate": g}) for g in ("learned", "uniform")]
        for i in range(20):
            view = (Content("memory", "cue", str(i % 2), 1),)
            for model in models:
                model.learn(None, SimpleNamespace(outcome=None), view, None)
                model.after_act(None, view, "a", None)
                model.learn_terminal(SimpleNamespace(action="a"), 0, i % 2, None)
        for a, b in zip(models[0].experts, models[1].experts):
            self.assertEqual(a.w, b.w)
        self.assertEqual(models[0].losses, models[1].losses)
        self.assertEqual(models[1].gate_weights("a"), [0.2] * 5)

    def test_live_restore_and_shadow_match_for_all_new_options(self):
        self.require_options()
        for step in ("normalised", "sqrt", "adagrad"):
            for gate in SelfModel.choices["gate"]:
                arm = f"organism self_model.step={step} self_model.gate={gate}"
                ledger = MemoryLedger()
                ref = run(arm, "vigil", 3, 12, ledger=ledger)
                restored = run(arm, "vigil", 3, 12, kill_at=[5, 29])
                self.assertEqual(ref["head"], restored["head"], arm)
                forecasts = replay_self_model(list(ledger))
                self.assertTrue(all(f.confidence == f.logged for f in forecasts), arm)

    def test_shadow_parameter_override_preserves_logged_stream_and_prefix(self):
        self.require_options()
        ledger = MemoryLedger()
        run("organism", "vigil", 3, 20, ledger=ledger)
        events = list(ledger)
        before = copy.deepcopy(events)
        full = replay_self_model(events)
        alternate = replay_self_model(events, model_params={"step": "adagrad", "gate": "learned"})
        key = lambda f: (f.episode, f.action, f.outcome)
        self.assertEqual(list(map(key, full)), list(map(key, alternate)))
        self.assertEqual(events, before)
        self.assertNotEqual([f.confidence for f in full], [f.confidence for f in alternate])
        end = next(i for i, e in enumerate(events) if e.kind == "end") + 1
        prefix = replay_self_model(events[:end], model_params={"step": "adagrad", "gate": "learned"})
        self.assertEqual(prefix, alternate[:len(prefix)])
        with self.assertRaises(ValueError):
            replay_self_model(events, model_params={"gate": "typo"})


if __name__ == "__main__":
    unittest.main()
