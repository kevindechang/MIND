"""Instrument tests for E100 Day 1 broadcast lesion; integrity only, not L2/L3."""
import json
import subprocess
import sys
import unittest
from pathlib import Path


def _load_day1():
    import importlib.util
    mod_path = Path(__file__).resolve().parents[1] / "e100" / "day1.py"
    spec = importlib.util.spec_from_file_location("e100_day1", str(mod_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Day1LesionTests(unittest.TestCase):
    def test_self_test_passes(self):
        script = Path(__file__).resolve().parents[1] / "e100" / "day1.py"
        p = subprocess.run([sys.executable, str(script), "--self-test"],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(p.returncode, 0, (p.stdout, p.stderr))
        result = json.loads(p.stdout)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["rival_verdict"],
                         "TIE_PREDECLARED_RETAIN_SIMPLER_NO_BROADCAST_ADOPTED")

    def test_intact_both_receive(self):
        m = _load_day1()
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            db = m.open_ledger(Path(td) / "l.sqlite3")
            try:
                m.append_commitment(db, "c101", "inspect_signal")
                out = m.decide_all(db, {"primary": True, "downstream": True}, [0])
                self.assertEqual(out["primary"]["action"], "inspect_signal")
                self.assertEqual(out["downstream"]["action"], "inspect_signal")
            finally:
                db.close()

    def test_lesion_changes_downstream_preserves_source_and_record(self):
        m = _load_day1()
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            db = m.open_ledger(Path(td) / "l.sqlite3")
            try:
                m.append_commitment(db, "c101", "inspect_signal")
                out = m.decide_all(db, {"primary": True, "downstream": False}, [0])
                self.assertEqual(out["primary"]["action"], "inspect_signal")
                self.assertEqual(out["downstream"]["action"], "NO_ACTION")
                self.assertEqual(m.ledger_row_count(db), 1)
            finally:
                db.close()

    def test_budget_parity_lesioned_read_still_executes(self):
        m = _load_day1()
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            db = m.open_ledger(Path(td) / "l.sqlite3")
            try:
                m.append_commitment(db, "c101", "inspect_signal")
                qc_intact, qc_les = [0], [0]
                m.decide_all(db, {"primary": True, "downstream": True}, qc_intact)
                m.decide_all(db, {"primary": True, "downstream": False}, qc_les)
                self.assertEqual(qc_intact[0], 2)
                self.assertEqual(qc_les[0], 2)
            finally:
                db.close()

    def test_wipe_control(self):
        m = _load_day1()
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            db = m.open_ledger(Path(td) / "l.sqlite3")
            try:
                out = m.decide_all(db, {"primary": True, "downstream": True}, [0])
                self.assertEqual(out["primary"]["action"], "NO_ACTION")
                self.assertEqual(out["downstream"]["action"], "NO_ACTION")
            finally:
                db.close()

    def test_alternate_ledger_counterexample(self):
        m = _load_day1()
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            db = m.open_ledger(Path(td) / "l.sqlite3")
            try:
                m.append_commitment(db, "c102", "record_measurement")
                out = m.decide_all(db, {"primary": True, "downstream": True}, [0])
                self.assertEqual(out["primary"]["action"], "record_measurement")
                self.assertEqual(out["downstream"]["action"], "record_measurement")
            finally:
                db.close()

    def test_completion_control(self):
        m = _load_day1()
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            db = m.open_ledger(Path(td) / "l.sqlite3")
            try:
                m.append_commitment(db, "c101", "inspect_signal")
                m.append_completion(db, "c101")
                out = m.decide_all(db, {"primary": True, "downstream": True}, [0])
                self.assertEqual(out["primary"]["action"], "NO_ACTION")
                self.assertEqual(out["downstream"]["action"], "NO_ACTION")
            finally:
                db.close()

    def test_rivals_tie_intact(self):
        m = _load_day1()
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            db = m.open_ledger(Path(td) / "l.sqlite3")
            try:
                m.append_commitment(db, "c101", "inspect_signal")
                intact = m.decide_all(db, {"primary": True, "downstream": True}, [0])
                self.assertEqual(m.rival_point_to_point(db, [0]), intact)
                self.assertEqual(m.rival_compact_shared_state(db, [0]), intact)
            finally:
                db.close()

    def test_no_leakage_across_tasks(self):
        m = _load_day1()
        import tempfile
        for task in ("inspect_signal", "record_measurement"):
            with tempfile.TemporaryDirectory() as td:
                db = m.open_ledger(Path(td) / "l.sqlite3")
                try:
                    m.append_commitment(db, "cx", task)
                    out = m.decide_all(db, {"primary": True, "downstream": False}, [0])
                    self.assertEqual(out["downstream"], {"action": "NO_ACTION", "based_on": None})
                finally:
                    db.close()


if __name__ == "__main__":
    unittest.main()
