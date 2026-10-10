"""Real subprocess death regression for E100 Day 0; only instrument integrity."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


class Day0KillTest(unittest.TestCase):
    @unittest.skipUnless(os.name == 'posix', 'POSIX SIGKILL required')
    def test_real_death_and_ledger_controls(self):
        script = Path(__file__).resolve().parents[1] / 'e100' / 'day0.py'
        p = subprocess.run([sys.executable, str(script), '--self-test'],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(p.returncode, 0, (p.stdout, p.stderr))
        result = json.loads(p.stdout)
        self.assertEqual(result['signal'], 'SIGKILL')
        self.assertEqual(result['observed_worker_exit_code'], -9)
        self.assertEqual(result['on_restart']['action'], 'inspect_signal')
        self.assertEqual(result['wiped_ledger']['action'], 'NO_ACTION')
        self.assertEqual(result['alternate_ledger']['action'], 'record_measurement')


if __name__ == '__main__':
    unittest.main()
