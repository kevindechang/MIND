"""Poltergeist: the confound is real, private causes stay private, and the new organ replays.

These pin the failures that closed the previous H010 world: action-dependent
randomness, a sensation that revealed polarity in one step, and a missing
positive control on the information the rival is allowed to see.
"""
import ast
import inspect
import os
import subprocess
import sys
import textwrap
import unittest

from mind.kernel import Organism
from mind.ledger import MemoryLedger
from mind.rivals import Estimator, RIVALS, _PolarityBayes
from mind.runner import run
from mind.worlds.poltergeist import (EXT, confound_problems, observation_model, sensation)


class ConfoundTests(unittest.TestCase):
    def test_one_transition_hides_polarity_and_the_external_label(self):
        for variant in ("dev", "gusty", "slippy"):
            self.assertEqual(confound_problems(variant), [], variant)

    def test_concrete_alias_two_causes_one_sensation(self):
        # A push under polarity +1 with no impulse, and a push under polarity -1
        # with an impulse of +2, are the same public sensation and different labels.
        quiet = sensation(1, 1, False, 0)
        impulse = sensation(-1, 1, False, 2)
        self.assertEqual(quiet, impulse)
        self.assertEqual(quiet, 1)
        self.assertFalse(0 != 0)
        self.assertTrue(2 != 0)

    def test_every_external_value_can_produce_each_clipped_sensation(self):
        # Support, not a fitted frequency: the model used by the reference filter
        # must give every (polarity, command, sensation) positive probability.
        lik, _ = observation_model("dev")
        for polarity in (1, -1):
            for command in (1, -1):
                for sense in (-1, 0, 1):
                    self.assertGreater(lik[(polarity, command, sense)], 0.0)
        self.assertEqual(EXT, (-2, -1, 0, 1, 2))

    def test_private_causes_never_enter_the_observation(self):
        from mind.worlds import make_world
        banned = {"polarity", "external", "slip", "cause", "label", "applied"}
        for variant in ("dev", "gusty", "slippy"):
            env = make_world("poltergeist", 3, variant)
            obs = env.reset()
            for _ in range(env.trials * 2 * 3):
                self.assertTrue(banned.isdisjoint(obs), (variant, obs))
                step = env.step(env.legal()[0] if env.phase == "act" else "yes")
                if step.done:
                    obs = env.reset()
                else:
                    obs = step.obs

    def test_schedule_does_not_depend_on_the_actions(self):
        from mind.worlds import make_world
        def schedule(policy):
            env = make_world("poltergeist", 11, "gusty")
            seen = []
            for _ in range(5):
                env.reset()
                while True:
                    action = policy(env)
                    step = env.step(action)
                    seen.append((step.info["polarity"], step.info["trial"],
                                 step.info["external"], step.info["slip"]))
                    if step.done:
                        break
            return seen
        follow = lambda env: env.legal()[0]
        defy = lambda env: "no" if env.phase == "judge" else env.legal()[0]
        self.assertEqual(schedule(follow), schedule(defy))

    def test_constant_yes_is_near_the_base_rate(self):
        from mind.worlds import make_world
        env = make_world("poltergeist", 0, "dev")
        hits = []
        for _ in range(80):
            env.reset()
            while True:
                action = env.legal()[0] if env.phase == "act" else "yes"
                step = env.step(action)
                if step.done:
                    break
            hits.append(env.summary()["attributed"])
        mean = sum(hits) / len(hits)
        self.assertGreater(mean, 0.42)
        self.assertLess(mean, 0.58)


class RivalInformationTests(unittest.TestCase):
    def test_estimator_source_does_not_read_the_world_model_or_private_info(self):
        src = textwrap.dedent(inspect.getsource(Estimator))
        tree = ast.parse(src)
        imported = [a.name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
                    for a in node.names]
        modules = [node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        names = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
        banned = {"observation_model", "_SETTINGS", "confound_problems", "sensation"}
        self.assertTrue(banned.isdisjoint(imported))
        self.assertTrue(banned.isdisjoint(names))
        self.assertFalse(any("poltergeist" in module for module in modules))

    def test_moment_ignores_history_and_the_filter_uses_it(self):
        def drive(agent, senses):
            agent.step({"phase": "act", "request": "push"}, boundary=True, actions=("push",))
            last = None
            for i, sense in enumerate(senses):
                if i:
                    agent.step({"phase": "act", "request": "push"}, actions=("push",))
                last = agent.step({"phase": "judge", "sense": str(sense)}, actions=("yes", "no"))
            return last.action

        # Repeated +1 sensations pull a trace toward polarity +1; repeated -1
        # sensations pull it toward -1. A following +1 is "no external" under the
        # first trace and "external" under the second. A moment judge, with no
        # trace, answers both histories the same.
        moment_a = drive(_PolarityBayes("dev", trace=False), [1, 1, 1, 1, 1, 1, 1])
        moment_b = drive(_PolarityBayes("dev", trace=False), [-1, -1, -1, -1, -1, -1, 1])
        filter_a = drive(_PolarityBayes("dev", trace=True), [1, 1, 1, 1, 1, 1, 1])
        filter_b = drive(_PolarityBayes("dev", trace=True), [-1, -1, -1, -1, -1, -1, 1])
        self.assertEqual(moment_a, moment_b)
        self.assertNotEqual(filter_a, filter_b)

    def test_bayes_reference_does_not_silently_cover_the_new_world(self):
        self.assertNotIn("poltergeist", RIVALS["bayes"].worlds)
        with self.assertRaises(ValueError):
            run("rival:bayes", "poltergeist", 0, 2)


class ReplayTests(unittest.TestCase):
    def test_efference_replays_through_death(self):
        ref = run("organism +efference", "poltergeist", 2, 6, ledger=MemoryLedger(), trace=True)
        died = run("organism +efference", "poltergeist", 2, 6, kill_at=[1, 7, 20], trace=True)
        self.assertEqual(died["trace"], ref["trace"])
        self.assertEqual(died["head"], ref["head"])

    def test_stripped_organism_matches_the_reactive_rival(self):
        a = run("organism -memory -goals -self_model", "poltergeist", 5, 30, trace=True)
        b = run("rival:reactive", "poltergeist", 5, 30, trace=True)
        self.assertEqual(a["trace"], b["trace"])

    def test_efference_replay_is_stable_across_hash_seeds(self):
        led = MemoryLedger()
        head = run("organism +efference shuffle:efference", "poltergeist", 4, 4, ledger=led)["head"]
        events = [(e.kind, e.payload) for e in led]
        script = textwrap.dedent("""\
            import json, sys
            from mind.kernel import Organism
            from mind.ledger import MemoryLedger
            led = MemoryLedger()
            for kind, payload in json.load(sys.stdin):
                led.append(kind, payload)
            Organism.restore(led)
            print(led.head)
            """)
        for hashseed in ("1", "2", "3"):
            proc = subprocess.run([sys.executable, "-c", script], input=__import__("json").dumps(events),
                                  capture_output=True, text=True,
                                  env=dict(os.environ, PYTHONHASHSEED=hashseed), timeout=60)
            self.assertEqual(proc.returncode, 0, proc.stderr[-400:])
            self.assertEqual(proc.stdout.strip(), head)

    def test_organ_proposes_a_residual_from_the_public_sense_only(self):
        org = Organism("organism +efference", 0)
        org.step({"phase": "act", "request": "push"}, boundary=True, actions=("push",))
        decision = org.step({"phase": "judge", "sense": "1"}, actions=("yes", "no"))
        tags = set(decision.broadcast)
        self.assertTrue(any(tag.startswith("efference:res=") for tag in tags), tags)
        self.assertFalse(any("external" in tag or "polarity" in tag for tag in tags))
        self.assertIn(org.organs["efference"].introspect()["motor"], (1, -1))


if __name__ == "__main__":
    unittest.main()
