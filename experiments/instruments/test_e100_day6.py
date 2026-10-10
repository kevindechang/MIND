"""Instrument tests for E100 Day 6 liar-twin comparison; integrity only."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def _load():
    p = Path(__file__).resolve().parents[1] / "e100" / "day6.py"
    spec = importlib.util.spec_from_file_location("e100_day6", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Day6TwinTests(unittest.TestCase):
    def test_self_test_passes(self):
        script = Path(__file__).resolve().parents[1] / "e100" / "day6.py"
        p = subprocess.run([sys.executable, str(script), "--self-test"],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(p.returncode, 0, (p.stdout, p.stderr))
        d = json.loads(p.stdout)
        self.assertEqual(d["status"], "PASS")
        self.assertEqual(d["endpoints"]["action_score"], {"grounded": 3, "narrator": 1})

    def test_grounded_adapts_narrator_fixed_zero_reads(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            pa = Path(td) / "a.sqlite3"
            m.build(pa, "outage_sensor")
            qcg, qcn = [0], [0]
            self.assertEqual(m.grounded(pa, qcg)["action"], "DEFER_SENSOR_SCAN")
            nr = m.narrator(pa, qcn)
            self.assertEqual(nr["action"], "SCAN_WITH_SENSOR")
            self.assertEqual(qcn[0], 0)
            self.assertGreater(qcg[0], 0)

    def test_blank_and_restart(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            pb = Path(td) / "b.sqlite3"
            m.connect(pb).close()
            self.assertEqual(m.grounded(pb)["action"], "NO_GOAL")
            pa = Path(td) / "a.sqlite3"
            m.build(pa, "outage_greenhouse")
            self.assertEqual(m.grounded(pa)["action"], "SCAN_WITH_SENSOR")

    def test_preference_hazard(self):
        m = _load()
        self.assertGreater(m.preference_score(m.NARRATOR_TEXT),
                           m.preference_score("DEFER_SENSOR_SCAN"))


if __name__ == "__main__":
    unittest.main()
