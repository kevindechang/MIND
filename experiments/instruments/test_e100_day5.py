"""Instrument tests for E100 Day 5 selector lesion; integrity only."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def _load():
    p = Path(__file__).resolve().parents[1] / "e100" / "day5.py"
    spec = importlib.util.spec_from_file_location("e100_day5", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Day5SelectorTests(unittest.TestCase):
    def test_self_test_passes(self):
        script = Path(__file__).resolve().parents[1] / "e100" / "day5.py"
        p = subprocess.run([sys.executable, str(script), "--self-test"],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(p.returncode, 0, (p.stdout, p.stderr))
        d = json.loads(p.stdout)
        self.assertEqual(d["status"], "PASS")
        self.assertEqual(d["P2_external_tie"]["verdict"],
                         "NULL_NO_IDENTIFIED_ENDOGENOUS_ADVANTAGE")

    def test_null_tie(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            a = m.run_arm(td, "a")
            self.assertEqual(a["internal"]["action"], "EXEC_RECALIBRATE")
            self.assertEqual(a["external"]["action"], a["internal"]["action"])
            self.assertEqual(a["external"]["estimand"], a["internal"]["estimand"])
            self.assertEqual(a["selects"]["external"], a["selects"]["internal"])

    def test_cron_matched_but_worse(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            a = m.run_arm(td, "a")
            self.assertEqual(a["selects"]["cron"], a["selects"]["internal"])
            self.assertLess(a["cron"]["estimand"], a["internal"]["estimand"])

    def test_wipe_negative_probe(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(m.run_arm(td, "w", blank=True)["internal"]["action"], "IDLE")
            n = m.run_arm(td, "n", orders=(("a", 1, 5), ("b", 1, 5)))
            self.assertEqual(n["internal"]["action"], "IDLE")
            self.assertEqual(n["external"]["action"], "IDLE")
            q = m.run_arm(td, "q", orders=(("polish", 6, 2), ("sweep", 9, 3), ("log", 1, 9)))
            self.assertEqual(q["internal"]["action"], "EXEC_SWEEP")
            self.assertEqual(q["external"]["action"], "EXEC_SWEEP")


if __name__ == "__main__":
    unittest.main()
