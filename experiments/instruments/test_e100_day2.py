"""Instrument tests for E100 Day 2 causal-link lesion; integrity only, not L2/L3."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def _load():
    p = Path(__file__).resolve().parents[1] / "e100" / "day2.py"
    spec = importlib.util.spec_from_file_location("e100_day2", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Day2LinkTests(unittest.TestCase):
    def test_self_test_passes(self):
        script = Path(__file__).resolve().parents[1] / "e100" / "day2.py"
        p = subprocess.run([sys.executable, str(script), "--self-test"],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(p.returncode, 0, (p.stdout, p.stderr))
        d = json.loads(p.stdout)
        self.assertEqual(d["status"], "PASS")
        self.assertEqual(d["P3_compact_tie"]["verdict"],
                         "TIE_RETAIN_SIMPLER_NO_LINK_NECESSITY")

    def test_dissociation(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            i = m.run_arm(td, "i", setup_kwargs={"include_links": True})
            l = m.run_arm(td, "l", setup_kwargs={"include_links": False})
            self.assertEqual(i["linked_action"], m.DEFER)
            self.assertEqual(l["linked_action"], m.SCAN)
            self.assertEqual(l["factual"], i["factual"])
            self.assertEqual(l["selects"], i["selects"])

    def test_compact_ties(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            for links in (True, False):
                a = m.run_arm(td, f"c{links}", setup_kwargs={"include_links": links})
                self.assertEqual(a["compact_action"], m.DEFER)

    def test_wipe(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            w = m.run_arm(td, "w", blank=True)
            self.assertEqual(w["factual"], [])
            self.assertEqual(w["linked_action"], m.NO_GOAL)

    def test_unrelated(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            kw = {"outage_resource": "greenhouse_light", "link_outage": False}
            a = m.run_arm(td, "a", setup_kwargs={"include_links": True, **kw})
            b = m.run_arm(td, "b", setup_kwargs={"include_links": False, **kw})
            self.assertEqual((a["linked_action"], b["linked_action"]), (m.SCAN, m.SCAN))
            self.assertEqual(a["factual"], b["factual"])

    def test_held_out_probe(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            kw = {"goal_id": "goal-009", "incident_id": "incident-009"}
            a = m.run_arm(td, "a", setup_kwargs={"include_links": True, **kw})
            b = m.run_arm(td, "b", setup_kwargs={"include_links": False, **kw})
            self.assertEqual(a["linked_action"], m.DEFER)
            self.assertEqual(b["linked_action"], m.SCAN)
            self.assertEqual(a["factual"], b["factual"])

    def test_real_sigkill_and_ledger_only_restart(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            for name, links in (("intact", True), ("cut", False)):
                result = m.run_arm(td, name, setup_kwargs={"include_links": links})
                self.assertEqual(result["worker_exit"], -9)
                self.assertTrue(result["distinct_process"])
                self.assertEqual(result["events"], 3)

    def test_sham_cuts_irrelevant_edge_only(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            control = m.run_arm(td, "sham_before", setup_kwargs={
                "include_links": True, "unrelated_link": True})
            sham = m.run_arm(td, "sham_after", setup_kwargs={
                "include_links": True, "unrelated_link": True, "sham_cut": True})
            self.assertEqual(control["factual"], sham["factual"])
            self.assertEqual(control["linked_action"], sham["linked_action"])
            self.assertEqual(control["linked_action"], m.DEFER)
            self.assertEqual(control["links"] - sham["links"], 1)

    def test_compact_derived_from_same_initial_evidence(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            cut = m.run_arm(td, "cut", setup_kwargs={"include_links": False})
            control = m.run_arm(td, "unrelated", setup_kwargs={
                "include_links": False, "link_outage": False,
                "outage_resource": "greenhouse_light"})
            self.assertTrue(cut["build"]["compiled_from_events_and_links"])
            self.assertEqual(cut["build"]["compilation_selects"], 2)
            self.assertEqual(cut["compact_action"], m.DEFER)
            self.assertEqual(control["compact_action"], m.SCAN)
            self.assertEqual(cut["selects"]["compact"], 2)
            self.assertEqual(cut["selects"]["linked"], 2)

    def test_structural_holdout_and_heldout_action_score(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            kwargs = {"goal_id": "goal-010", "incident_id": "incident-010",
                      "outage_resource": "array_power_b", "extra_hop": True}
            intact = m.run_arm(td, "novel_intact", setup_kwargs={
                **kwargs, "include_links": True})
            cut = m.run_arm(td, "novel_cut", setup_kwargs={
                **kwargs, "include_links": False})
            self.assertEqual(intact["links"], 3)
            self.assertEqual(cut["links"], 0)
            self.assertEqual(intact["factual"], cut["factual"])
            self.assertEqual(intact["heldout_action_score"]["linked"], 1)
            self.assertEqual(cut["heldout_action_score"]["linked"], 0)
            self.assertEqual(cut["heldout_action_score"]["compact"], 1)

    def test_unknown_goal_without_links_scans(self):
        m = _load()
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.sqlite3"
            db = m.connect(p)
            try:
                m.setup(db, include_links=False)
                self.assertEqual(m.linked_planner(db), {"action": m.SCAN})
            finally:
                db.close()


if __name__ == "__main__":
    unittest.main()
