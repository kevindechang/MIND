"""Announcement-aware table and the silent capability-shift variant.

The alert table is the plain success table plus public alert=down / alert=up.
Where those announcements are absent it must match the plain table exactly, including
on outage/shift, so the two scorers are equally informed there.
"""
import unittest

from mind.organs.self_model import SelfModel
from mind.rivals import AlertTable, SuccessTable
from mind.runner import run
from mind.worlds import make_world
from mind.worlds.outage import _SHIFT


class AlertTableTests(unittest.TestCase):
    def test_no_announcement_matches_the_plain_table(self):
        plain, alert = SuccessTable(), AlertTable()
        script = [("scan", 1), ("manual", 1), ("scan", 0), ("scan", 1), ("wait", None)]
        for action, outcome in script:
            alert.observe({})
            alert.observe({"noise0": "1", "result": "manual:ok"})
            self.assertEqual(alert.forecast(action), plain.forecast(action))
            if outcome is not None:
                plain.update(action, outcome)
                alert.update(action, outcome)
        self.assertEqual(alert.p, plain.p)

    def test_alert_down_and_up_are_one_scan_observation(self):
        alert, down, up = AlertTable(), SuccessTable(), SuccessTable()
        alert.observe({"alert": "down"})
        down.update("scan", 0)
        self.assertEqual(alert.forecast("scan"), down.forecast("scan"))
        self.assertEqual(alert.forecast("manual"), down.forecast("manual"))
        alert.observe({"alert": "up"})
        up.update("scan", 0)
        up.update("scan", 1)
        self.assertEqual(alert.forecast("scan"), up.forecast("scan"))
        self.assertLess(down.forecast("scan"), 0.5)
        self.assertGreater(alert.forecast("scan"), down.forecast("scan"))

    def test_runner_matches_on_silent_worlds_and_moves_on_announced_outages(self):
        for world, variant, episodes in (("outage", "silent", 20), ("outage", "shift", 30),
                                         ("vigil", "dev", 8), ("workshop", "dev", 6)):
            metrics = run("organism", world, 1, episodes, variant)["metrics"]
            for suffix in ("", "@all", "@early"):
                self.assertEqual(metrics["brier_alert" + suffix], metrics["brier_table" + suffix],
                                 (world, variant, suffix))
        announced = run("organism", "outage", 1, 40, "dev")["metrics"]
        self.assertNotEqual(announced["brier_alert@all"], announced["brier_table@all"])

    def test_existing_metrics_are_unchanged(self):
        # Pinned before the alert scorer existed, so adding it cannot move the old metrics.
        baseline = {
            "organism|outage|dev|1|20": {
                "reward": 14.77, "brier": 0.08940371356355085, "brier_table": 0.09341340421271574,
                "calib_gain": 0.004009690649164885},
            "rival:reactive|outage|dev|5|12": {"calib_gain": 0.0, "calib_gain@all": 0.0, "reward": 8.108333333333329},
            "rival:reactive|vigil|dev|3|10": {"calib_gain": 0.0, "brier": 0.14734471099363866},
        }
        for key, expected in baseline.items():
            arm, world, variant, seed, eps = key.split("|")
            metrics = run(arm, world, int(seed), int(eps), variant)["metrics"]
            for name, value in expected.items():
                self.assertEqual(metrics[name], value, (key, name))


class ShiftWorldTests(unittest.TestCase):
    def test_reliability_steps_silently_and_independent_of_actions(self):
        for variant, spec in _SHIFT.items():
            seen = []
            for policy in (("scan",), ("manual", "wait")):
                env = make_world("outage", 4, variant)
                ps, alerts = [], []
                for ep in range(env.default_episodes):
                    obs = env.reset()
                    self.assertNotIn("alert", obs)
                    self.assertNotIn("up", obs)
                    self.assertNotIn("p", obs)
                    s = env.step(policy[ep % len(policy)])
                    ps.append(s.info["p"])
                    alerts.append("alert" in (s.obs or {}))
                    # finish the episode so the next reset is the next episode
                    while not s.done:
                        obs = s.obs
                        self.assertNotIn("alert", obs)
                        s = env.step(policy[ep % len(policy)])
                seen.append(ps)
                self.assertFalse(any(alerts))
                self.assertEqual(ps[:spec["at"]], [spec["before"]] * spec["at"])
                self.assertEqual(ps[spec["at"]:], [spec["after"]] * (env.default_episodes - spec["at"]))
            self.assertEqual(seen[0], seen[1])

    def test_surprise_threshold_above_any_error_never_flags(self):
        loud, quiet = SelfModel({}), SelfModel({"surprise": 2})
        for model in (loud, quiet):
            model.w[("scan", "bias")] = 20.0
            model._update("scan", ["bias"], 0)
        self.assertEqual(loud.surprised, "scan")
        self.assertIsNone(quiet.surprised)
        self.assertEqual(loud.w[("scan", "bias")], quiet.w[("scan", "bias")])

    def test_shift_oracle_runs(self):
        metrics = run("rival:bayes", "outage", 0, 8, "shift")["metrics"]
        self.assertIn("reward", metrics)


if __name__ == "__main__":
    unittest.main()
