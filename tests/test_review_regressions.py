"""Regression tests for the v2 adversarial review (reviews/2026-10-10-v2-pipeline-adversarial-review.md).

Each test pins one confirmed finding so it cannot silently return. Two of them are
tests of the tests: they break the substrate in a throwaway copy of the package
and check that the claim procedures (K06, K07) catch the breakage.
"""
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

from mind import stats
from mind.claims import Claim, Compare, Evaluation, _exec_claim, evaluate
from mind.kernel import Organism
from mind.knowledge import assess
from mind.ledger import LedgerCorrupt, MemoryLedger
from mind.runner import run
from mind.worlds import WORLDS, make_world

ROOT = Path(__file__).resolve().parents[1]

CHECK_SRC = textwrap.dedent('''\
    """doc"""
    from mind.claims import Check, Claim
    LIMIT = {limit}

    def helper():
        return LIMIT

    def check(ctx):
        return {{"verdict": "HOLDS" if helper() > 0 else "FAILS", "robust": True}}

    CLAIM = Claim(id="X01", title="t", statement="s", kind="invariant", scope="instrument",
                  test=Check(check, seeds=4))
''')


def record(evals, at, schema=2):
    return {"evaluations": {e.claim: e.to_dict() for e in evals}, "by": "a", "environment_id": "e",
            "code": "c", "recorded_at": at, "mode": "full", "schema": schema, "_path": f"r/{at}.json"}


class Finding4HelpersAreHashed(unittest.TestCase):
    def test_editing_a_helper_constant_changes_the_prediction(self):
        a = _exec_claim(CHECK_SRC.format(limit=1), "<a>")
        b = _exec_claim(CHECK_SRC.format(limit=2), "<b>")
        self.assertEqual(a.prediction_hash(1), b.prediction_hash(1))      # the old scheme was blind to it
        self.assertNotEqual(a.prediction_hash(), b.prediction_hash())     # scheme 2 is not
        prose = _exec_claim(CHECK_SRC.format(limit=1).replace('"""doc"""', '"""better words"""'), "<c>")
        self.assertEqual(a.prediction_hash(), prose.prediction_hash())


class Finding8RivalOrientation(unittest.TestCase):
    def test_a_claim_that_holds_because_the_rival_is_better_does_not_beat_it(self):
        class Lab:
            def metric(self, arm, world, variant, seeds, episodes, metric):
                return [0.5 + 0.01 * i for i in range(len(seeds))] if arm == "rival:flat" else [0.0] * len(seeds)
        c = Claim("C9", "t", "s", "effect", "L2",
                  Compare("vigil", "organism", "rival:flat", "kept", "<", 0.1, 8), about=("workspace",))
        ev = evaluate(c, Lab(), "quick")
        self.assertEqual(ev.verdict, "HOLDS")
        self.assertEqual(ev.rivals["flat"]["result"], "NOT_BEATEN")


class Finding3FirstHeldoutDecides(unittest.TestCase):
    def test_rerunning_heldout_after_a_failure_cannot_earn_preregistration(self):
        c = Claim("C1", "t", "s", "effect", "L2", Compare("vigil", "organism", "organism -memory", "kept", ">", 0.1, 16))
        h = c.prediction_hash()
        fail = Evaluation("C1", h, "FAILS", False, "heldout:s")
        later = Evaluation("C1", h, "HOLDS", True, "heldout:s")
        st = assess({"C1": c}, [record([fail], "2026-01-01"), record([later], "2026-02-01")], seals={"C1": "s"})["C1"]
        self.assertEqual(st.state, "HOLDS")
        self.assertNotEqual(st.level, "PREREGISTERED")
        self.assertTrue(any("first sealed confirmation" in n for n in st.notes))

    def test_amended_predictions_stay_visible(self):
        old = Claim("C1", "t", "s", "effect", "L2", Compare("vigil", "organism", "organism -memory", "kept", ">", 0.1, 16))
        new = Claim("C1", "t", "s", "effect", "L2", Compare("vigil", "organism", "organism -memory", "kept", ">", 0.3, 16))
        st = assess({"C1": new}, [record([Evaluation("C1", old.prediction_hash(), "HOLDS", True, "dev")], "2026-01-01")])["C1"]
        self.assertEqual(st.state, "UNTESTED")
        self.assertTrue(any("prediction amended" in n for n in st.notes))


class MinorFindings(unittest.TestCase):
    def test_restore_verifies_the_hash_chain(self):
        led = MemoryLedger()
        run("organism", "vigil", 1, 3, ledger=led)
        led._events[2] = led._events[2].__class__(2, "tick", {**led._events[2].payload, "r": 9.0},
                                                  led._events[2].hash)
        with self.assertRaises(LedgerCorrupt):
            Organism.restore(led)

    def test_midlife_freeze_keeps_episodic_state(self):
        org = Organism("organism @1:freeze:memory", 0)
        org.step({"request": "a", "x": "1"}, boundary=True, actions=("wait", "a"))
        org.step({"x": "2"}, actions=("wait", "a"))
        org.end_episode(0.0)
        before = org.organs["memory"].introspect()["remembered"]
        self.assertTrue(before)
        org.step({"y": "1"}, boundary=True, actions=("wait", "a"))     # episode 1: frozen from here
        self.assertEqual(org.organs["memory"].introspect()["remembered"], before)

    def test_world_randomness_never_depends_on_the_agents_actions(self):
        for name, cls in WORLDS.items():
            for variant in cls.variants:
                lives = []
                for policy_seed in (1, 2):
                    # episode lengths may legitimately differ between policies; what must not differ
                    # is what the world draws for each episode (its first private state)
                    env, pol, seen = make_world(name, 3, variant), random.Random(policy_seed), []
                    for _ in range(25):
                        env.reset()
                        first = None
                        while True:
                            s = env.step(pol.choice(env.legal()))
                            first = first or tuple(sorted(s.info.items()))
                            if s.done:
                                break
                        seen.append(first)
                    lives.append(seen)
                self.assertEqual(lives[0], lives[1], (name, variant))

    def test_success_table_shadow_is_exactly_the_rival_rule(self):
        for world in WORLDS:
            self.assertEqual(run("rival:reactive", world, 2, 20)["metrics"]["calib_gain@all"], 0.0)

    def test_conservative_interval_contains_the_t_interval(self):
        xs = [0.1, 0.4, 0.2, 0.9, 0.3, 0.5, 0.2, 0.6]
        m, lo, hi = stats.bootstrap_ci(xs)
        sd = (sum((x - m) ** 2 for x in xs) / 7) ** 0.5
        self.assertLessEqual(lo, m - stats.t975(7) * sd / 8 ** 0.5 + 1e-12)
        self.assertGreaterEqual(hi, m + stats.t975(7) * sd / 8 ** 0.5 - 1e-12)


def _sandbox(tmp: Path) -> Path:
    """A throwaway copy of the package (plus the legacy instruments it imports)."""
    shutil.copytree(ROOT / "mind", tmp / "mind", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / "experiments" / "instruments", tmp / "experiments" / "instruments",
                    ignore=shutil.ignore_patterns("__pycache__"))
    return tmp


@unittest.skipUnless(os.name == "posix", "real SIGKILL requires POSIX")
class TestsOfTheTests(unittest.TestCase):
    def test_k07_procedure_catches_a_broken_exactly_once(self):
        with tempfile.TemporaryDirectory() as d:
            box = _sandbox(Path(d))
            kernel = box / "mind" / "kernel.py"
            src = kernel.read_text()
            broken = src.replace("        if t < self.t:\n            return self._decisions[t]\n",
                                 "        if t < self.t:\n            self.t = t  # BROKEN: act again\n")
            self.assertNotEqual(src, broken)
            kernel.write_text(broken)
            probe = ("from mind.worker import supervised_run\n"
                     "from mind.runner import run\nfrom mind.ledger import MemoryLedger\n"
                     "ref = run('organism', 'vigil', 1, 6, ledger=MemoryLedger(), trace=True)\n"
                     "r = supervised_run('organism', 'vigil', 1, 6, kill_committed=[4])\n"
                     "print(r['replays']['step'], r['head'] == ref['head'])\n")
            p = subprocess.run([sys.executable, "-c", probe], cwd=box, capture_output=True, text=True, timeout=120)
            # K07 requires replays == kills AND an identical life; the broken copy must fail one of them
            self.assertTrue(p.returncode != 0 or p.stdout.split() != ["1", "True"], (p.stdout, p.stderr[-400:]))

    def test_k06_procedure_catches_a_hash_order_hazard(self):
        with tempfile.TemporaryDirectory() as d:
            box = _sandbox(Path(d))
            (box / "mind" / "organs" / "hazard.py").write_text(textwrap.dedent('''\
                from ..kernel import Content, Organ

                class Hazard(Organ):
                    name = "hazard"
                    def propose(self, sense, ctx):
                        keys = list(set(sense.obs))          # iteration order depends on PYTHONHASHSEED
                        return [Content(self.name, "first", keys[0], 2.0)] if keys else []
                '''))
            init = box / "mind" / "organs" / "__init__.py"
            init.write_text(init.read_text().replace(
                "from .goals import Goals", "from .goals import Goals\nfrom .hazard import Hazard").replace(
                "(Perception, Memory, Goals, SelfModel, Policy)", "(Perception, Memory, Goals, SelfModel, Policy, Hazard)"))
            probe = textwrap.dedent('''\
                import json, os, subprocess, sys
                from mind.ledger import MemoryLedger
                from mind.runner import run
                led = MemoryLedger()
                head = run("organism +hazard", "vigil", 1, 6, ledger=led)["head"]
                events = [(e.kind, e.payload) for e in led]
                script = ("import json,sys\\nfrom mind.kernel import Organism\\nfrom mind.ledger import MemoryLedger\\n"
                          "l=MemoryLedger()\\nfor k,p in json.load(sys.stdin): l.append(k,p)\\nOrganism.restore(l)\\nprint(l.head)")
                bad = 0
                for hs in ("1", "2", "3", "4"):
                    p = subprocess.run([sys.executable, "-c", script], input=json.dumps(events), capture_output=True,
                                       text=True, env=dict(os.environ, PYTHONHASHSEED=hs))
                    bad += p.returncode != 0 or p.stdout.strip() != head
                print(bad)
                ''')
            p = subprocess.run([sys.executable, "-c", probe], cwd=box, capture_output=True, text=True, timeout=300,
                               env=dict(os.environ, PYTHONHASHSEED="99"))
            self.assertEqual(p.returncode, 0, p.stderr[-400:])
            self.assertGreater(int(p.stdout.strip()), 0)


if __name__ == "__main__":
    unittest.main()
