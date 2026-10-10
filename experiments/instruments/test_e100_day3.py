"""Instrument tests for E100 Day 3 self-model lesion; integrity only."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def _load():
    p = Path(__file__).resolve().parents[1] / "e100" / "day3.py"
    spec = importlib.util.spec_from_file_location("e100_day3", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Day3SelfModelTests(unittest.TestCase):
    def test_self_test_passes(self):
        script = Path(__file__).resolve().parents[1] / "e100" / "day3.py"
        p = subprocess.run([sys.executable, str(script), "--self-test"],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(p.returncode, 0, (p.stdout, p.stderr))
        d = json.loads(p.stdout)
        self.assertEqual(d["status"], "PASS")
        self.assertEqual(d["calibration"], "NOT_TESTABLE_AT_TOY_SCALE")

    def test_switch_and_persona(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            a = m.run_arm(td, "a")
            self.assertEqual(a["adaptive"]["choice"], m.SPARE)
            self.assertEqual(a["adaptive"]["confidence"], m.LO)
            self.assertEqual(a["persona"]["choice"], m.PREF)
            self.assertEqual(a["factual"], m.run_arm(td, "b")["factual"])

    def test_parity(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            a = m.run_arm(td, "a")
            self.assertEqual(a["selects"]["persona"], a["selects"]["adaptive"])

    def test_rival_tie_no_confidence(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            a = m.run_arm(td, "a")
            self.assertEqual(a["rival"]["choice"], a["adaptive"]["choice"])
            self.assertNotIn("confidence", a["rival"])

    def test_wipe_and_unrelated(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            w = m.run_arm(td, "w", blank=True)
            self.assertEqual(w["adaptive"]["action"], "NO_GOAL")
            u = m.run_arm(td, "u", outage="greenhouse_light")
            self.assertEqual(u["adaptive"], {"choice": m.PREF, "confidence": m.HI,
                                             "action": "USE_SENSOR"})

    def test_probe_pair(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            a = m.run_arm(td, "a", pref="primary", spare="spare", outage="primary")
            self.assertEqual(a["adaptive"]["choice"], "spare")
            self.assertEqual(a["persona"]["choice"], "primary")


if __name__ == "__main__":
    unittest.main()
