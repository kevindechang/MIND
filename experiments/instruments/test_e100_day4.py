"""Instrument tests for E100 Day 4 goals/initiative lesion; integrity only."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def _load():
    p = Path(__file__).resolve().parents[1] / "e100" / "day4.py"
    spec = importlib.util.spec_from_file_location("e100_day4", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Day4GoalsTests(unittest.TestCase):
    def test_self_test_passes(self):
        script = Path(__file__).resolve().parents[1] / "e100" / "day4.py"
        p = subprocess.run([sys.executable, str(script), "--self-test"],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(p.returncode, 0, (p.stdout, p.stderr))
        self.assertEqual(json.loads(p.stdout)["status"], "PASS")

    def test_dissociation(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            a = m.run_arm(td, "a", include_initiative=True)
            b = m.run_arm(td, "b", include_initiative=False)
            self.assertEqual(a["tick"], "EXEC_INSPECT_SIGNAL")
            self.assertEqual(b["tick"], "IDLE")
            self.assertEqual(a["qa"], b["qa"])
            self.assertEqual(a["selects"], b["selects"])

    def test_rival_ties(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            for init in (True, False):
                a = m.run_arm(td, f"r{init}", include_initiative=init)
                self.assertEqual(a["rival"], a["tick"])

    def test_wipe_unrelated_probe(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            w = m.run_arm(td, "w", blank=True)
            self.assertEqual((w["tick"], w["qa"]), ("IDLE", []))
            u = m.run_arm(td, "u", include_initiative=True, extra_tick=True)
            self.assertEqual(u["tick"], "EXEC_INSPECT_SIGNAL")
            q = m.run_arm(td, "q", goal_id="goal-009", task="record_measurement",
                          include_initiative=True)
            self.assertEqual(q["tick"], "EXEC_RECORD_MEASUREMENT")
            self.assertEqual(q["qa"], ["record_measurement"])


if __name__ == "__main__":
    unittest.main()
