"""H002 shift-world adversarial instrument tests (isolated mirror)."""
import unittest
from mind.worlds.shift import Shift, TICKS, _SETTINGS


def episode(world, actions):
    first = world.reset()
    trace = []
    for a in actions:
        step = world.step(a)
        trace.append(step)
    return first, trace, world.summary()


class ShiftInstrumentTest(unittest.TestCase):
    def test_public_observation_has_no_hidden_phase_or_reliability(self):
        w = Shift(7)
        for _ in range(26):
            obs, steps, _ = episode(w, ["probe_a"] * TICKS)
            for x in [obs] + [s.obs for s in steps]:
                self.assertFalse(set(x) & {"phase", "switch", "p_a", "p_b", "episode", "post_shift"})
                self.assertTrue(set(x) <= {"noise0", "noise1", "result"})
            self.assertTrue(all("phase" in s.info for s in steps))

    def test_counterfactual_coins_do_not_depend_on_action_history(self):
        a, b = Shift(17), Shift(17)
        for ep in range(55):
            obs_a, obs_b = a.reset(), b.reset()
            self.assertEqual(obs_a, obs_b)
            self.assertEqual(a._coins, b._coins)
            self.assertEqual((a.phase, a.p_a, a.p_b), (b.phase, b.p_a, b.p_b))
            for t in range(TICKS):
                left, right = a.step("probe_a"), b.step("probe_b" if t % 2 else "manual")
                self.assertEqual(left.info, right.info)
                self.assertEqual(left.obs.get("noise0"), right.obs.get("noise0"))
                self.assertEqual(left.obs.get("noise1"), right.obs.get("noise1"))

    def test_action_potential_matches_counterfactual_same_tick(self):
        a, b = Shift(18), Shift(18)
        for ep in range(30):
            a.reset(); b.reset()
            for t in range(TICKS):
                left = a.step("probe_a")
                right = b.step("probe_b")
                self.assertEqual(left.outcome, int(a._coins[(t, "probe_a")] < a.p_a))
                self.assertEqual(right.outcome, int(b._coins[(t, "probe_b")] < b.p_b))

    def test_random_shift_schedule_and_stationary_negative_control(self):
        for variant in ("dev", "fast", "subtle", "stationary"):
            w = Shift(3, variant)
            s = _SETTINGS[variant]
            last_phase, last_switch = 0, 0
            for ep in range(120):
                w.reset()
                self.assertIn(w.phase - last_phase, (0, 1))
                if w.phase != last_phase:
                    self.assertGreaterEqual(ep - last_switch, s["dwell"])
                    last_switch = ep
                flipped = bool(s["switch"] and w.phase % 2)
                self.assertEqual(w.p_a, s["low"] if flipped else s["high"])
                self.assertEqual(w.p_b, s["high"] if flipped else s["low"])
                since = ep - last_switch
                self.assertEqual(w.post_shift, bool(w.phase > 0 and since < s["window"]))
                for _ in range(TICKS):
                    w.step("manual")
                last_phase = w.phase
        # Dev and stationary share the exact pseudo-event schedule.
        a, b = Shift(3, "dev"), Shift(3, "stationary")
        for ep in range(120):
            a.reset(); b.reset()
            self.assertEqual((a.phase, a.post_shift, a.stable),
                             (b.phase, b.post_shift, b.stable))
            self.assertEqual((b.p_a, b.p_b), (0.85, 0.25))
            for _ in range(TICKS):
                a.step("wait"); b.step("wait")

    def test_regret_uses_expected_not_realized_reward(self):
        w = Shift(4)
        w.reset()
        expected_best = w._expected(w.p_a)
        for _ in range(TICKS):
            w.step("manual")
        self.assertAlmostEqual(w.summary()["regret"], expected_best - 0.35)
        self.assertAlmostEqual(w.summary()["stable_regret"], 0)

    def test_optimal_action_has_zero_expected_regret_even_on_failure(self):
        w = Shift(2)
        for _ in range(25):
            w.reset()
            action = "probe_a" if w.p_a > w.p_b else "probe_b"
            for _ in range(TICKS):
                w.step(action)
            self.assertAlmostEqual(w.summary()["regret"], 0)

    def test_replay_deterministic_across_instances(self):
        for variant in Shift.variants:
            a, b = Shift(11, variant), Shift(11, variant)
            for ep in range(31):
                actions = ["probe_a", "manual", "probe_b", "wait", "probe_a", "probe_b"]
                self.assertEqual(episode(a, actions), episode(b, actions))

    def test_exposure_windows_are_disjoint_and_nonzero(self):
        for variant in Shift.variants:
            w = Shift(6, variant)
            n_post = n_stable = 0
            for ep in range(120):
                w.reset()
                self.assertFalse(w.post_shift and w.stable)
                for _ in range(TICKS):
                    w.step("wait")
                row = w.summary()
                n_post += row["post_shift_exposure"]
                n_stable += row["stable_exposure"]
            self.assertGreater(n_stable, 0)
            self.assertGreater(n_post, 0)

    def test_actions_and_heldout_variants(self):
        self.assertIn("fast", Shift.heldout_variants)
        self.assertIn("subtle", Shift.heldout_variants)
        w = Shift(5)
        w.reset()
        with self.assertRaises(ValueError):
            w.step("not-an-action")
        for _ in range(TICKS):
            w.step("wait")
        with self.assertRaises(ValueError):
            w.step("wait")
        with self.assertRaises(ValueError):
            Shift(1, "invalid")


if __name__ == "__main__":
    unittest.main()


class StationaryMatchedControlTest(unittest.TestCase):
    def test_stationary_sham_matches_dev_exogenous_streams(self):
        # A sham differs only in whether the latent reliability reverses.
        # The exogenous uniforms and public distractors must be identical.
        a, b = Shift(33, "dev"), Shift(33, "stationary")
        for ep in range(80):
            self.assertEqual(a.reset(), b.reset())
            self.assertEqual(a._coins, b._coins)
            self.assertEqual(a.phase, b.phase)
            for tick in range(TICKS):
                sa, sb = a.step("manual"), b.step("manual")
                self.assertEqual(sa.obs, sb.obs)
