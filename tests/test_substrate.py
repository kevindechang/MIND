"""Substrate integrity: ledger, kernel determinism, replay, lesions, death, worlds, rivals.

These are engineering guarantees that every scientific claim rests on. They are
NOT evidence about cognition. Run: python -m unittest discover -s tests
"""
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest

from mind.kernel import Config, Organism, ReplayDivergence
from mind.ledger import LedgerCorrupt, MemoryLedger, SqliteLedger
from mind.runner import run
from mind.worlds import WORLDS, make_world


class LedgerTests(unittest.TestCase):
    def test_chain_verifies_and_detects_tampering(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "l.sqlite3"
            led = SqliteLedger(path)
            for i in range(5):
                led.append("tick", {"t": i, "x": [i, "a"]})
            head = led.verify()
            led.close()
            reopened = SqliteLedger(path)
            self.assertEqual(reopened.head, head)
            self.assertEqual(len(reopened), 5)
            reopened.close()
            db = sqlite3.connect(str(path))
            db.execute("UPDATE events SET payload=? WHERE seq=2", ('{"t":99,"x":[2,"a"]}',))
            db.commit()
            db.close()
            tampered = SqliteLedger(path)
            with self.assertRaises(LedgerCorrupt):
                tampered.verify()
            tampered.close()

    def test_memory_and_sqlite_backends_hash_identically(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = MemoryLedger(), SqliteLedger(Path(d) / "l.sqlite3")
            for led in (a, b):
                led.append("genesis", {"config": "organism", "seed": 1})
                led.append("tick", {"obs": {"k": "v"}, "r": 0.5, "o": None})
            self.assertEqual(a.head, b.head)
            b.close()

    def test_fork_shares_history_then_diverges(self):
        a = MemoryLedger()
        a.append("x", {"i": 1})
        b = a.fork()
        self.assertEqual(a.head, b.head)
        a.append("x", {"i": 2})
        b.append("x", {"i": 3})
        self.assertNotEqual(a.head, b.head)


class KernelTests(unittest.TestCase):
    def test_config_canonical_and_validated(self):
        self.assertEqual(Config.parse("organism capacity=inf -memory").text,
                         Config.parse("organism -memory capacity=inf").text)
        for bad in ("organism -policy", "organism -nonexistent", "organism wat", "brain",
                    "organism @x:-memory", "organism cut:memory"):
            with self.assertRaises(ValueError, msg=bad):
                Config.parse(bad)

    def test_same_seed_same_life(self):
        a = run("organism", "vigil", 3, 30, trace=True)
        b = run("organism", "vigil", 3, 30, trace=True)
        self.assertEqual(a["trace"], b["trace"])
        self.assertEqual(a["metrics"], b["metrics"])

    def test_replay_restores_identical_organism_in_every_world_and_lesion(self):
        for world in WORLDS:
            for config in ("organism", "organism -memory", "organism capacity=inf cut:memory>policy",
                           "organism shuffle:memory freeze:self_model", "organism @3:-goals"):
                episodes = 12
                ref = run(config, world, 2, episodes, ledger=MemoryLedger(), trace=True)
                died = run(config, world, 2, episodes, kill_at=[0, 5, 17, 31], trace=True)
                self.assertEqual(ref["trace"], died["trace"], (world, config))
                self.assertEqual(ref["head"], died["head"], (world, config))

    def test_replay_rejects_a_forged_decision(self):
        led = MemoryLedger()
        run("organism", "vigil", 1, 5, ledger=led)
        forged = MemoryLedger()
        for event in led:
            payload = dict(event.payload)
            if event.kind == "tick" and payload["t"] == 3:
                payload["act"] = "c" if payload["act"] != "c" else "b"
            forged.append(event.kind, payload)
        with self.assertRaises(ReplayDivergence):
            Organism.restore(forged)

    def test_ablation_removes_organ_contents(self):
        org = Organism("organism -goals", seed=0)
        d = org.step({"request": "a"}, boundary=True, actions=("wait", "a"))
        d = org.step({"x": "1"}, actions=("wait", "a"))
        self.assertFalse(any(tag.startswith("goals:") for tag in d.broadcast))

    def test_cut_blocks_delivery_but_not_competition(self):
        intact, cut = Organism("organism", 0), Organism("organism cut:goals>policy", 0)
        for org in (intact, cut):
            org.step({"request": "a"}, boundary=True, actions=("wait", "a"))
        di = intact.step({"y": "1"}, actions=("wait", "a"))
        dc = cut.step({"y": "1"}, actions=("wait", "a"))
        self.assertEqual(di.broadcast, dc.broadcast)          # goals still won the workspace
        self.assertIn("goals:pending=a", dc.broadcast)
        self.assertNotIn("goals", [c.source for c in cut._view("policy", cut.prev.broadcast)])

    def test_capacity_limits_broadcast(self):
        org = Organism("organism capacity=2", 0)
        d = org.step({f"k{i}": "1" for i in range(6)}, boundary=True, actions=("wait",))
        self.assertEqual(len(d.broadcast), 2)

    def test_idempotent_step_never_acts_twice(self):
        org = Organism("organism", 0, MemoryLedger())
        d0 = org.step_at(0, {"a": "1"}, boundary=True, actions=("wait", "x"))
        again = org.step_at(0, {"a": "DIFFERENT"}, boundary=True, actions=("wait", "x"))
        self.assertEqual(d0, again)
        self.assertEqual(len(org.ledger), 2)  # genesis + one tick


class DeathTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "posix", "real SIGKILL requires POSIX")
    def test_sigkill_mid_request_is_exactly_once_and_byte_identical(self):
        from mind.worker import supervised_run
        ref = run("organism", "vigil", 4, 12, ledger=MemoryLedger(), trace=True)
        res = supervised_run("organism", "vigil", 4, 12, kill_after=[3], kill_during=[9, 20])
        self.assertEqual([d["exit"] for d in res["deaths"]], [-9, -9, -9])
        self.assertEqual(len({d["pid"] for d in res["deaths"]} | {res["final_pid"]}), 4)
        self.assertEqual(res["trace"], ref["trace"])
        self.assertEqual(res["head"], ref["head"])


class WorldTests(unittest.TestCase):
    def test_every_world_is_seeded_and_variants_differ(self):
        for name, cls in WORLDS.items():
            self.assertTrue(cls.heldout_variants, name)
            for variant in cls.variants:
                a = run("rival:reactive", name, 7, 6, variant, trace=True)
                b = run("rival:reactive", name, 7, 6, variant, trace=True)
                self.assertEqual(a["metrics"], b["metrics"], (name, variant))

    def test_private_info_never_in_observations(self):
        env = make_world("outage", 1)
        obs = env.reset()
        for _ in range(60):
            self.assertNotIn("up", obs)
            s = env.step("scan")
            obs = s.obs if not s.done else env.reset()

    def test_workshop_bayes_reference_realises_legacy_v04_value(self):
        # The new world + oracle reproduce the legacy E001 v0.4 DP: mean regret ~ 0.
        r = run("rival:bayes", "workshop", 0, 400, "dev")
        self.assertLess(abs(r["metrics"]["regret@all"]), 0.08)

    def test_organism_minus_memory_and_self_model_is_the_reactive_rival(self):
        # Matched-learner fairness: with those organs removed the organism reduces
        # exactly to the reactive transcript rival when the workspace is not saturated.
        a = run("organism -memory -self_model", "outage", 1, 30, trace=True)
        b = run("rival:reactive", "outage", 1, 30, trace=True)
        self.assertEqual(a["trace"], b["trace"])


if __name__ == "__main__":
    unittest.main()
