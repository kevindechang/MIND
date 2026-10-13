"""H001 causal organ: its predictions must equal the workshop's own scoring rule, it must learn only
from what it attended, and a late bid must reach the decision of the tick that produced it."""
from itertools import combinations, product
import random
import unittest

from mind.kernel import Content, Organism
from mind.ledger import MemoryLedger
from mind.organs.causal import Causal, label_of, mask_of, plan_nodes, predicted_utility
from mind.runner import run
from mind.worlds.workshop import GRAPHS, PENALTY, PLANS, V04

LEGAL = ("wait", "probe0", "probe1", "probe2") + tuple(PLANS)
WANTS = ((0, 1), (1, 0))


def perceived(key, value, salience=0.5):
    return Content("perception", key, value, salience)


class StubContext:
    """The organism's per-tick random streams, seeded as the kernel seeds them."""
    def rng(self, purpose):
        return random.Random(f"1|2|{purpose}")


def tick(org, facts=(), wants=WANTS, actions=LEGAL, t=2):
    """One late phase: the attended contents of a tick, as the kernel hands them to the organ."""
    view = tuple(facts) + tuple(perceived(f"want{g}", str(d)) for g, d in wants)
    now = type("Now", (), {"actions": tuple(actions), "t": t})()
    return org.late_propose(now, view, StubContext())


class PredictionMatchesWorld(unittest.TestCase):
    def test_predicted_utility_equals_workshop_payoff_for_every_graph_plan_and_commitment(self):
        checked = 0
        for g, graph in enumerate(GRAPHS):
            reach = {n: V04.reach(graph, n) for n in range(3)}
            for goals in combinations(range(3), 2):
                for wants in product((0, 1), repeat=2):
                    commitments = tuple(zip(goals, wants))
                    for name, plan in PLANS.items():
                        expected = V04.payoff(graph, plan, [(goal, want, PENALTY) for goal, want in commitments])
                        predicted = predicted_utility(reach, name, commitments, PENALTY)
                        self.assertEqual(predicted, expected, f"graph {g} plan {name} commitments {commitments}")
                        checked += 1
        self.assertEqual(checked, 8 * 3 * 4 * len(PLANS))

    def test_unprobed_nodes_make_a_plan_unpredictable(self):
        self.assertIsNone(predicted_utility({0: 0b011}, "do:12", ((0, 1), (1, 0)), PENALTY))
        self.assertEqual(predicted_utility({0: 0b011}, "do:none", ((0, 1), (1, 0)), PENALTY), -PENALTY)
        self.assertIsNone(predicted_utility({0: 0b011}, "probe1", ((0, 1), (1, 0)), PENALTY))

    def test_mask_and_label_round_trip(self):
        for label in ("0", "1", "02", "012"):
            self.assertEqual(label_of(mask_of(label)), label)
        self.assertEqual(plan_nodes("do:none"), ())
        self.assertEqual(plan_nodes("do:02"), (0, 2))
        self.assertIsNone(plan_nodes("probe0"))


class WhatItLearns(unittest.TestCase):
    def test_learns_attended_uncensored_probe_results_only(self):
        org = Causal({})
        tick(org, facts=(perceived("fx0", "02"), Content("memory", "was:fx1", "1", 0.9),
                         perceived("fx2", "censored")))
        self.assertEqual(org.reach, {0: mask_of("02")})

    def test_forgets_everything_between_episodes(self):
        org = Causal({})
        tick(org, facts=(perceived("fx1", "1"),))
        org.reset_episode()
        self.assertEqual(org.reach, {})
        self.assertEqual(org.wants, {})

    def test_the_best_plan_is_proposed_on_the_tick_the_result_is_attended(self):
        org = Causal({})
        self.assertEqual([c.key for c in tick(org)], [])          # nothing learned yet
        out = tick(org, facts=(perceived("fx0", "0"),))            # attended now, used now
        self.assertIn("best", [c.key for c in out])

    def test_no_recommendation_until_both_commitments_are_known(self):
        org = Causal({})
        out = tick(org, facts=(perceived("fx0", "0"),), wants=((0, 1),))
        self.assertNotIn("best", [c.key for c in out])
        self.assertIn("reach0", [c.key for c in out])

    def test_derived_plan_follows_the_learned_reach(self):
        org = Causal({})
        best = [c for c in tick(org, facts=(perceived("fx0", "0"),), actions=("do:none", "do:0", "do:1"))
                if c.key == "best"]
        self.assertEqual(best[0].value, "do:0")                   # toggling 0 reaches only 0
        org = Causal({})
        best = [c for c in tick(org, facts=(perceived("fx0", "01"),), actions=("do:none", "do:0", "do:1"))
                if c.key == "best"]
        self.assertEqual(best[0].value, "do:none")                # toggling 0 also flips node 1


class Controls(unittest.TestCase):
    FACTS = (perceived("fx0", "0"), perceived("fx1", "1"))

    def test_derive_zero_keeps_the_same_load_with_a_constant_in_place_of_the_plan(self):
        derived = tick(Causal({}), facts=self.FACTS)
        flat = tick(Causal({"derive": 0}), facts=self.FACTS)
        self.assertEqual(len(derived), len(flat))
        self.assertEqual([c.key for c in flat if c.key != "pad"], [c.key for c in derived if c.key != "best"])
        self.assertEqual([c.value for c in flat if c.key == "pad"], ["0"])

    def test_sham_proposes_a_random_legal_plan_at_the_same_ticks(self):
        real = tick(Causal({}), facts=self.FACTS)
        sham = tick(Causal({"sham": 1}), facts=self.FACTS)
        self.assertEqual([c.key for c in real], [c.key for c in sham])
        drawn = [c.value for c in sham if c.key == "best"][0]
        self.assertIn(drawn, [a for a in LEGAL if plan_nodes(a) is not None])
        self.assertEqual(drawn, [c.value for c in tick(Causal({"sham": 1}), facts=self.FACTS)
                                 if c.key == "best"][0])          # deterministic per organism state


class ReplayAndSameTick(unittest.TestCase):
    def test_a_probe_result_changes_the_decision_of_the_tick_that_shows_it(self):
        org = Organism("organism +causal capacity=inf", seed=1)
        org.step({"want0": "1", "want1": "0", "t": "0"}, boundary=True, actions=LEGAL)
        decision = org.step({"want0": "1", "want1": "0", "t": "1", "fx0": "0"},
                            reward=-0.25, actions=LEGAL)
        self.assertTrue(any(tag.startswith("causal:best=") for tag in decision.broadcast), decision.broadcast)

    def test_a_causal_life_replays_from_its_ledger(self):
        ledger = MemoryLedger()
        run("organism +causal", "workshop", seed=3, episodes=40, ledger=ledger)
        restored = Organism.restore(ledger)   # raises ReplayDivergence if any logged decision differs
        self.assertEqual(restored.cfg.organs[-1], "causal")
        self.assertGreater(restored.t, 0)


if __name__ == "__main__":
    unittest.main()
