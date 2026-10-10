"""Targeted H002 checks. Full MIND regression must be run separately."""
import unittest
from reproduce import Filter, lifetime

class ShadowTests(unittest.TestCase):
    def test_no_future_outcome(self):
        f=Filter()
        self.assertEqual(f.forecast('scan'),.5)
        f.update('scan',0)
        self.assertAlmostEqual(f.forecast('scan'),.04)
    def test_alert_sham(self):
        f=Filter();s=Filter('swapped')
        f.observe({'alert':'down'});s.observe({'alert':'down'})
        self.assertEqual((f.forecast('scan'),s.forecast('scan')),(.08,.92))
    def test_silent_negative_control(self):
        r=lifetime(20000,'silent')
        self.assertEqual(r['F'],r['F0'])
        self.assertEqual(r['F'],r['FS'])
    def test_known_seed_replay(self):
        r=lifetime(20000,'dev')
        self.assertAlmostEqual(r['F'],.07569457059132818,places=10)
        self.assertAlmostEqual(r['S'],.12417087355951795,places=10)

if __name__=='__main__':unittest.main()
