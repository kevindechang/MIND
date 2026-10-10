"""Regression tests for the owner's review of PR #17 (three P1 findings).

Each test reproduces the reviewer's counterexample. The third finding (rival standing
from an old panel) is pinned in test_claims.py next to the other ladder rules.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from mind.kernel import Config, Organism
from mind.runner import run

ROOT = Path(__file__).resolve().parents[1]


class LesionsThatWouldDoNothingAreRejected(unittest.TestCase):
    def test_misspelled_or_absent_targets(self):
        for text in ("organism cut:memory>polciy", "organism cut:memroy>policy", "organism freeze:memroy",
                     "organism shuffle:goal", "organism -memory freeze:memory", "organism -memory cut:memory>*",
                     "organism +memory"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                Config.parse(text)

    def test_unknown_or_mistyped_parameters(self):
        for text in ("organism memory.capcity=10", "organism nosuch.capacity=1", "organism memory.capacity=6.5",
                     "organism memory.decay=fast", "organism perception.salience=novelt",
                     "organism -memory memory.decay=0.5"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                Config.parse(text)

    def test_scheduled_lesions_are_checked_against_the_organs_alive_then(self):
        for text in ("organism @3:freeze:memroy", "organism @2:-memory @5:freeze:memory",
                     "organism @3:memory.decay=0.5", "organism @3:-policy"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                Config.parse(text)
        with self.assertRaises(ValueError):    # a lesion on a living organism cannot rebuild an organ
            Organism("organism", 0).lesion("memory.decay=0.5")
        with self.assertRaises(ValueError):    # scheduled after the life ends: it would never happen
            run("organism @500:-memory", "vigil", 0, episodes=10)

    def test_valid_lesions_still_parse(self):
        for text in ("organism", "organism cut:memory>policy", "organism cut:self_model>*",
                     "organism freeze:self_model shuffle:memory", "organism memory.capacity=10",
                     "organism perception.salience=novelty", "organism @2:-memory @5:+memory",
                     "organism -memory @4:+memory memory.decay=0.5", "organism @1:freeze:memory",
                     "organism capacity=inf", "organism -goals -memory"):
            with self.subTest(text=text):
                Config.parse(text)


@unittest.skipUnless((ROOT / ".git").exists() and shutil.which("git"), "needs a git checkout")
class RecordsCannotBeEdited(unittest.TestCase):
    def test_flipping_a_committed_heldout_verdict_is_caught(self):
        with tempfile.TemporaryDirectory() as tmp:
            box = Path(tmp) / "repo"
            subprocess.run(["git", "clone", "-q", str(ROOT), str(box)], check=True)
            shutil.rmtree(box / "mind")   # test this checkout's doctor against the clone's history
            shutil.copytree(ROOT / "mind", box / "mind", ignore=shutil.ignore_patterns("__pycache__"))
            probe = "from mind.doctor import record_integrity; print('\\n'.join(record_integrity()))"
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")

            def problems():
                p = subprocess.run([sys.executable, "-c", probe], cwd=box, capture_output=True, text=True,
                                   timeout=120, env=env)
                self.assertEqual(p.returncode, 0, p.stderr)
                return p.stdout.strip()

            def commit(message):
                subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", message],
                               cwd=box, check=True)

            self.assertEqual(problems(), "")
            rec = sorted((box / "knowledge" / "records").glob("*-heldout.json"))[0]
            data = json.loads(rec.read_text(encoding="utf-8"))
            cid, e = next((cid, e) for cid, e in sorted(data["evaluations"].items()) if e["verdict"] != "HOLDS")
            e["verdict"], e["robust"] = "HOLDS", True          # a failed confirmation, promoted
            rec.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
            self.assertIn(f"{rec.name} differs", problems())  # edited in the working tree
            commit("edit a record")
            self.assertIn(f"{rec.name} differs", problems())  # edited in a later commit
            rec.unlink()
            commit("delete a record")
            self.assertIn(f"{rec.name} was deleted", problems())


if __name__ == "__main__":
    unittest.main()
