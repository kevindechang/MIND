import unittest
from e002a_maintenance_selection import Task, choose_expected_value, choose_deadline, choose_fixed, expected_outcome, compare


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            Task('first', 5, 0.7, 0.1, 1),
            Task('soon', 1, 2.0, 0.2, 1),
            Task('valuable', 3, 5.0, 0.5, 1),
        ]

    def test_value_based_controller_selects_max_net_gain(self):
        self.assertEqual(choose_expected_value(self.tasks, cost=0.1), 'valuable')

    def test_earliest_deadline_control_differs(self):
        self.assertEqual(choose_deadline(self.tasks), 'soon')

    def test_fixed_control_is_fixed_independent_of_values(self):
        self.assertEqual(choose_fixed(self.tasks), 'first')

    def test_no_compute_when_every_gain_below_cost(self):
        self.assertIsNone(choose_expected_value(self.tasks, cost=10.0))

    def test_observed_expected_utility_uses_true_gain_not_estimate(self):
        self.assertAlmostEqual(expected_outcome(self.tasks, 'valuable', cost=0.1), 2.4)

    def test_estimation_errors_can_make_metareasoner_worse_than_deadline(self):
        misleading = [Task('first', 5, 5.0, 0.05, 1),
                      Task('soon', 1, 2.0, 0.9, 1),
                      Task('valuable', 3, 0.1, 0.9, 1)]
        selected = choose_expected_value(misleading, cost=0.1)
        self.assertEqual(selected, 'first')
        self.assertLess(expected_outcome(misleading, selected, cost=0.1),
                        expected_outcome(misleading, choose_deadline(misleading), cost=0.1))

    def test_comparison_is_explicitly_one_slot_budget(self):
        result = compare(self.tasks, cost=0.1)
        self.assertEqual({k for k in result}, {'fixed','deadline','estimated_value'})
        self.assertTrue(all(isinstance(row['action'], (str, type(None))) for row in result.values()))

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            choose_expected_value(self.tasks + [self.tasks[0]], cost=0.1)

    def test_negative_cost_rejected(self):
        with self.assertRaises(ValueError):
            choose_expected_value(self.tasks, cost=-1)

    def test_no_positive_tasks(self):
        self.assertIsNone(choose_expected_value([], cost=0))


if __name__ == '__main__':
    unittest.main()
