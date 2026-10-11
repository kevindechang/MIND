"""Matched-state report forks: sham identity, unchanged broadcasts, restore.

These tests check the instrument. They are not evidence about report validity.
"""
import unittest

from mind.kernel import Organism
from mind.ledger import MemoryLedger
from mind.report import (CONDITIONS, grounded_report, intention_in_broadcast, matched_fork,
                         parse_tag, probe_fingerprint)
from mind.runner import run


class ReportRuleTests(unittest.TestCase):
    def test_report_prefers_pending_then_memory_and_ignores_confidence_tags(self):
        actions = ("wait", "a", "b", "c")
        broadcast = (
            "self_model:self:a=sure",
            "perception:bell=1",
            "memory:was:request=b",
            "goals:pending=a",
        )
        self.assertEqual(grounded_report(broadcast, actions), "a")
        self.assertEqual(grounded_report(("perception:bell=1", "memory:was:request=c"), actions), "c")
        self.assertEqual(grounded_report(("perception:bell=1", "perception:noise0=1"), actions), "wait")
        self.assertEqual(grounded_report(("goals:pending=a",), actions), "wait")
        self.assertTrue(intention_in_broadcast(("memory:was:request=b",), actions))
        self.assertFalse(intention_in_broadcast(("self_model:self:a=doubt",), actions))

    def test_parse_tag_keeps_colons_inside_the_key(self):
        self.assertEqual(parse_tag("memory:was:request=a"), ("memory", "was:request", "a"))
        self.assertEqual(parse_tag("goals:pending=b"), ("goals", "pending", "b"))


class MatchedForkTests(unittest.TestCase):
    def test_sham_forks_match_and_cuts_leave_the_broadcast(self):
        # Short lives still have a late half. Exposure is not required: an untrained
        # organism often has no intention in the workspace, and the instrument must
        # hold on those ticks too.
        row = matched_fork(1, episodes=6, variant="dev", require_exposed=False)
        self.assertEqual(row["sham_identical"], 1)
        self.assertEqual(row["sham_action"], row["sham_b_action"])
        self.assertEqual(row["broadcasts_identical"], 1)
        self.assertGreaterEqual(row["episode"], 3)
        sham = row["arms"]["sham"]
        self.assertTrue(sham["frozen"])
        self.assertEqual(sham["cuts"], ())
        self.assertEqual(sham["t"], row["t"])
        for name, _cuts in CONDITIONS:
            arm = row["arms"][name]
            self.assertEqual(arm["broadcast"], sham["broadcast"], name)
            self.assertEqual(arm["report"], sham["report"], name)
            self.assertEqual(arm["t"], sham["t"], name)
            self.assertEqual(arm["seed"], sham["seed"], name)
            self.assertTrue(arm["frozen"], name)
        triple = row["arms"]["triple"]
        self.assertEqual(triple["cuts"], tuple(sorted((
            ("goals", "policy"), ("memory", "policy"), ("self_model", "policy")))))

    def test_checkpoint_is_before_the_bell_and_forks_do_not_share_a_ledger(self):
        row = matched_fork(2, episodes=8, variant="dev", require_exposed=False)
        self.assertEqual(row["sham_identical"], 1)
        # A second call is a new life and a new restore, not a continuation.
        again = matched_fork(2, episodes=8, variant="dev", require_exposed=False)
        self.assertEqual(row["sham_action"], again["sham_action"])
        self.assertEqual(row["t"], again["t"])
        self.assertEqual(tuple(row["arms"]["triple"]["broadcast"]),
                         tuple(again["arms"]["triple"]["broadcast"]))

    def test_fork_action_matches_a_hand_restored_copy(self):
        # The scored tick is the action of a restored, frozen organism, not of the
        # training loop's own object.
        from mind.report import _arm_step
        from mind.runner import make_agent
        from mind.worlds import make_world

        seed, episodes = 4, 6
        ledger = MemoryLedger()
        agent = make_agent("organism", "vigil", "dev", seed, ledger)
        env = make_world("vigil", seed, "dev")
        late = episodes // 2
        caught = None
        for episode in range(episodes):
            obs = env.reset()
            reward, outcome, boundary = 0.0, None, True
            while True:
                legal = tuple(env.legal())
                if episode >= late and str(obs.get("bell")) == "1":
                    caught = (ledger.fork(), {str(k): str(v) for k, v in obs.items()},
                              float(reward), outcome, legal)
                    break
                decision = agent.step(obs, reward, outcome, boundary, legal)
                step = env.step(decision.action)
                if step.done:
                    agent.end_episode(step.reward, step.outcome)
                    break
                obs, reward, outcome, boundary = step.obs, step.reward, step.outcome, False
            if caught:
                break
        self.assertIsNotNone(caught)
        checkpoint, obs, reward, outcome, legal = caught
        hand = _arm_step(checkpoint, obs, reward, outcome, False, legal, ("cut:goals>policy",))
        row = matched_fork(seed, episodes=episodes, variant="dev", require_exposed=False)
        self.assertEqual(hand["action"], row["arms"]["goals"]["action"])
        self.assertEqual(hand["broadcast"], row["arms"]["goals"]["broadcast"])
        restored = Organism.restore(checkpoint.fork())
        self.assertEqual(restored.t, row["t"])

    def test_scored_tick_is_the_first_late_bell(self):
        from mind.worlds import make_world

        episodes = 6
        row = matched_fork(3, episodes=episodes, variant="dev", require_exposed=False)
        env = make_world("vigil", 3, "dev")
        bell_at = {}
        t = 0
        for episode in range(episodes):
            obs = env.reset()
            while True:
                if str(obs.get("bell")) == "1":
                    bell_at[episode] = t
                step = env.step("wait")
                t += 1
                if step.done:
                    break
                obs = step.obs
        first_late = min(ep for ep in bell_at if ep >= episodes // 2)
        self.assertEqual(row["episode"], first_late)
        self.assertEqual(row["t"], bell_at[first_late])
        # The frozen sham can differ from the unfrozen life at that tick: freeze
        # skips the policy update that normally happens before the action.
        ordinary = run("organism", "vigil", 3, episodes, trace=True)
        self.assertEqual(len(ordinary["trace"]), t)

    def test_intervened_ledger_replays_the_forked_action(self):
        from mind.report import _arm_step
        from mind.runner import make_agent
        from mind.worlds import make_world

        ledger = MemoryLedger()
        agent = make_agent("organism", "vigil", "dev", 5, ledger)
        env = make_world("vigil", 5, "dev")
        obs = env.reset()
        reward, outcome, boundary = 0.0, None, True
        # Walk to the first bell of episode 2 (late half of 4 episodes).
        for episode in range(4):
            if episode:
                obs = env.reset()
                reward, outcome, boundary = 0.0, None, True
            while True:
                legal = tuple(env.legal())
                if episode >= 2 and str(obs.get("bell")) == "1":
                    checkpoint = ledger.fork()
                    org = Organism.restore(checkpoint.fork())
                    org.lesion("freeze:policy")
                    org.lesion("cut:memory>policy")
                    decision = org.step({str(k): str(v) for k, v in obs.items()},
                                        float(reward), outcome, False, legal)
                    replayed = Organism.restore(org.ledger)
                    self.assertEqual(replayed.t, org.t)
                    self.assertEqual(replayed.ledger.head, org.ledger.head)
                    hand = _arm_step(checkpoint, {str(k): str(v) for k, v in obs.items()},
                                     float(reward), outcome, False, legal, ("cut:memory>policy",))
                    self.assertEqual(hand["action"], decision.action)
                    self.assertEqual(hand["broadcast"], tuple(decision.broadcast))
                    return
                decision = agent.step(obs, reward, outcome, boundary, legal)
                step = env.step(decision.action)
                if step.done:
                    agent.end_episode(step.reward, step.outcome)
                    break
                obs, reward, outcome, boundary = step.obs, step.reward, step.outcome, False
        self.fail("did not reach a late bell")

    def test_fingerprint_is_stable_for_unchanged_source(self):
        self.assertEqual(probe_fingerprint(), probe_fingerprint())
        self.assertEqual(len(probe_fingerprint()), 16)

    def test_claims_seal_this_probe_fingerprint(self):
        import importlib.util
        from pathlib import Path
        fp = probe_fingerprint()
        root = Path(__file__).resolve().parents[1] / "knowledge" / "claims"
        sealed = (
            "K11_matched_fork_sham_is_identical.py",
            "C025_matched_fork_triple_cut_changes_action.py",
            "C026_matched_fork_cut_redundancy.py",
        )
        for name in sealed:
            spec = importlib.util.spec_from_file_location(name, root / name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.assertEqual(module.PROBE, fp, name)


if __name__ == "__main__":
    unittest.main()
