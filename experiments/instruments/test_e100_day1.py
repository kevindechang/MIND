"""E100 Day 1: subprocess lesion regression; NOT a consciousness evaluation."""
import json
from pathlib import Path
import os
import subprocess
import sys
import unittest


class Day1BroadcastLesion(unittest.TestCase):
    @unittest.skipUnless(os.name == 'posix', 'real SIGKILL requires POSIX')
    def test_broadcast_cut_and_compact_tie(self):
        script = Path(__file__).resolve().parents[1] / 'e100' / 'day1.py'
        run = subprocess.run([sys.executable, str(script), '--self-test'],
                             capture_output=True, text=True, timeout=20)
        self.assertEqual(run.returncode, 0, (run.stdout, run.stderr))
        data = json.loads(run.stdout)
        self.assertEqual(data['status'], 'PASS')
        self.assertEqual(data['intact']['raw'], data['lesion']['raw'])
        self.assertEqual(data['intact']['observer'], data['lesion']['observer'])
        self.assertEqual(data['intact']['routed_action'], 'DEFER_SENSOR_SCAN')
        self.assertEqual(data['lesion']['routed_action'], 'SCAN_WITH_SENSOR')
        self.assertTrue(data['compact_rival_matches_intact'])
        self.assertEqual(data['intact']['worker_exit'], -9)
        self.assertEqual(data['lesion']['worker_exit'], -9)
        self.assertEqual(data['unrelated_event_control'], 'SCAN_WITH_SENSOR')
        self.assertEqual(data['unrelated_event_lesion_control'], 'SCAN_WITH_SENSOR')


if __name__ == '__main__':
    unittest.main()
