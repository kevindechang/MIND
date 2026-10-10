"""Instrument tests for E100 Day 7 ledger fork; integrity only. No individual-count claims."""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def _load():
    p = Path(__file__).resolve().parents[1] / "e100" / "day7.py"
    spec = importlib.util.spec_from_file_location("e100_day7", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Day7ForkTests(unittest.TestCase):
    def test_self_test_passes(self):
        script = Path(__file__).resolve().parents[1] / "e100" / "day7.py"
        p = subprocess.run([sys.executable, str(script), "--self-test"],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(p.returncode, 0, (p.stdout, p.stderr))
        d = json.loads(p.stdout)
        self.assertEqual(d["status"], "PASS")
        self.assertIn("not one/two individuals", d["interpretation"])

    def test_fork_divergence(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            base = Path(td) / "b.sqlite3"
            m.build_base(base)
            f1, f2 = Path(td) / "f1.sqlite3", Path(td) / "f2.sqlite3"
            shutil.copyfile(base, f1)
            shutil.copyfile(base, f2)
            self.assertEqual(m.sha(base), m.sha(f1))
            self.assertEqual(m.decide(f1)["action"], "DEFER_SENSOR_SCAN")
            db = m.connect(f2)
            try:
                m.add(db, "incident-002", "tool_restored", "sensor")
            finally:
                db.close()
            d2 = m.decide(f2)
            self.assertEqual(d2["action"], "SCAN_WITH_SENSOR")
            self.assertEqual(d2["based_on"], ["goal-001", "incident-002"])

    def test_no_individual_claims_in_code(self):
        src = (Path(__file__).resolve().parents[1] / "e100" / "day7.py").read_text()
        self.assertNotIn("conscious individual", src)
        self.assertIn("not one/two individuals", src)

    def test_wipe(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            b = Path(td) / "blank.sqlite3"
            m.connect(b).close()
            self.assertEqual(m.decide(b)["action"], "NO_GOAL")


if __name__ == "__main__":
    unittest.main()
