"""E100 Day2: subprocess, SQL ledger and compact rival instrument tests."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'e100' / 'day2.py'
spec = importlib.util.spec_from_file_location('e100_day2', SCRIPT)
d2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d2)


class Day2Lesion(unittest.TestCase):
    @unittest.skipUnless(os.name == 'posix', 'requires real SIGKILL')
    def test_real_restart_and_controls(self):
        run = subprocess.run([sys.executable, str(SCRIPT), '--self-test'],
                             capture_output=True, text=True, timeout=45)
        self.assertEqual(run.returncode, 0, (run.stdout, run.stderr))
        result = json.loads(run.stdout)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['arm_count'], 12)
        for world, arms in result['worlds'].items():
            self.assertEqual(len({x['source_sha256'] for x in arms.values()}), 1)
            self.assertTrue(all(x['worker_exit'] == -9 for x in arms.values()))
            self.assertEqual(arms['intact']['causal_action'], arms['sham']['causal_action'])
            self.assertEqual(arms['intact']['causal_action'], arms['lesion']['compact_action'])
            if world in ('A', 'B'):
                self.assertNotEqual(arms['intact']['causal_action'], arms['lesion']['causal_action'])
            if world == 'NONE':
                self.assertEqual(arms['intact']['causal_action'], arms['lesion']['causal_action'])
            if world == 'SHIFT':
                self.assertEqual(arms['intact']['causal_reward'], 0)

    def test_no_observational_leakage(self):
        with tempfile.TemporaryDirectory() as td:
            db = d2.connect(Path(td) / 'd.sqlite3')
            d2.seed(db, d2.history('B'))
            d2.extract(db)
            self.assertEqual(d2.decide(db, 'causal'), 'DO_B')
            self.assertEqual(d2.decide(db, 'compact'), 'DO_B')
            self.assertEqual(d2.decide(db, 'predictive'), 'DO_B')
            db.close()

    def test_absent_intervention_abstains(self):
        with tempfile.TemporaryDirectory() as td:
            db = d2.connect(Path(td) / 'd.sqlite3')
            d2.seed(db, [['obs-a','observe','A',1,'train'],['obs-b','observe','B',0,'train']])
            d2.extract(db)
            self.assertEqual(d2.decide(db, 'causal'), 'NO_ACTION')
            self.assertEqual(d2.decide(db, 'compact'), 'NO_ACTION')
            db.close()

    def test_lesion_preserves_source(self):
        with tempfile.TemporaryDirectory() as td:
            db = d2.connect(Path(td) / 'd.sqlite3')
            d2.seed(db, d2.history('A'))
            d2.extract(db)
            original = d2.raw(db)
            d2.cut(db, 'lesion')
            self.assertEqual(d2.raw(db), original)
            self.assertEqual(d2.decide(db, 'causal'), 'NO_ACTION')
            self.assertEqual(d2.decide(db, 'compact'), 'DO_A')
            self.assertEqual(d2.links(db), [['clock', 'beacon', 1]])
            db.close()

    def test_duplicate_seed_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            db = d2.connect(Path(td) / 'd.sqlite3')
            d2.seed(db, d2.history('A'))
            with self.assertRaises(ValueError):
                d2.seed(db, d2.history('B'))
            db.close()

    def test_no_privileged_decision_payload(self):
        with tempfile.TemporaryDirectory() as td:
            p = d2.spawn(Path(td) / 'd.sqlite3')
            try:
                p.stdin.write(json.dumps({'op':'decide','mode':'causal','future_winner':'A'})+'\n')
                p.stdin.flush()
                response = json.loads(p.stdout.readline())
                self.assertIn('error', response)
            finally:
                d2.stop(p)

    def test_future_shift_nonidentifiable_from_public_history(self):
        self.assertEqual(d2.history('A'), d2.history('A'))
        self.assertEqual(d2.reward('DO_A','A'), 1)
        self.assertEqual(d2.reward('DO_A','B'), 0)


if __name__ == '__main__':
    unittest.main()
