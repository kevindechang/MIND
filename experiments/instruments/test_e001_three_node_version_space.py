"""Unittest checks for the 3-node version-space oracle — standard library only.

Covers: ambiguous vs separating histories, identical-public-history equality
across hidden graphs (leak prevention), pending/delayed/censored feedback,
deadline discipline, zero-normalizer rejection, determinism, and exact
Fraction arithmetic. Simulator/world-generation helpers are evaluator-side
test scaffolding, not agent results.
"""

import unittest
from fractions import Fraction

from e001_three_node_version_space import (
    NODES,
    ORDERED_EDGES,
    PublicCommitment,
    PublicHistory,
    PublicOutcome,
    PublicProbe,
    all_plans,
    all_three_node_dags,
    influence_of,
    make_history,
    pending_ids,
    posterior,
    reachability_mask,
    score,
    simulate_delivered,
    version_space,
)

FAMILY = all_three_node_dags()
G_EMPTY = frozenset()
G_FULL = frozenset(ORDERED_EDGES)
G_CHAIN = frozenset({(0, 1), (1, 2)})  # 0->1->2 transitively reaches {0,1,2} from 0


def history_with(probes, delivered, censored=(), commitments=(), deadline=2):
    return make_history(commitments, probes, delivered, censored, deadline)


class VersionSpaceTests(unittest.TestCase):
    def test_family_has_eight_forward_dags(self):
        self.assertEqual(len(FAMILY), 8)
        for edges in FAMILY:
            for a, b in edges:
                self.assertLess(a, b)

    def test_empty_history_keeps_full_version_space(self):
        h = history_with((), ())
        self.assertEqual(version_space(h), tuple(range(8)))
        post = posterior(h)
        self.assertEqual(post, {i: Fraction(1, 8) for i in range(8)})

    def test_ambiguous_history_identical_reference_across_hidden_graphs(self):
        # Probing node 2 always observes mask 100 in every candidate graph,
        # so the public history collides for G_EMPTY and G_FULL.
        probes = (PublicProbe(1, 2, 0, 1),)
        d_empty = simulate_delivered(G_EMPTY, probes)
        d_full = simulate_delivered(G_FULL, probes)
        self.assertEqual(d_empty, d_full)
        h_empty = history_with(probes, d_empty)
        h_full = history_with(probes, d_full)
        self.assertEqual(h_empty, h_full)
        self.assertEqual(version_space(h_empty), tuple(range(8)))
        self.assertEqual(posterior(h_empty), posterior(h_full))
        self.assertEqual(score(h_empty), score(h_full))

    def test_ambiguous_history_preserves_tied_action_set(self):
        # Commitment: goal 0 desired 1, penalty 4. With the full version
        # space the reference must be identical no matter which hidden graph
        # the evaluator sampled, since the public record is the same.
        commits = (PublicCommitment(0, 1, 4),)
        probes = (PublicProbe(1, 2, 0, 1),)
        delivered = simulate_delivered(G_CHAIN, probes)
        h = history_with(probes, delivered, commitments=commits)
        best, value, values = score(h)
        self.assertTrue(len(best) >= 1)
        for plan in best:
            self.assertEqual(values[plan], value)
        # Rebuild the same public history "as if" sampled from another graph.
        h2 = history_with(probes, simulate_delivered(G_EMPTY, probes),
                          commitments=commits)
        self.assertEqual(h, h2)
        self.assertEqual(score(h), score(h2))

    def test_separating_probe_splits_version_space(self):
        # Probe node 0: G_EMPTY observes 001, G_FULL observes 111.
        probes = (PublicProbe(1, 0, 0, 1),)
        d_empty = simulate_delivered(G_EMPTY, probes)
        d_full = simulate_delivered(G_FULL, probes)
        self.assertNotEqual(d_empty, d_full)
        h_empty = history_with(probes, d_empty)
        h_full = history_with(probes, d_full)
        vs_empty = version_space(h_empty)
        vs_full = version_space(h_full)
        self.assertIn(FAMILY.index(G_EMPTY), vs_empty)
        self.assertNotIn(FAMILY.index(G_FULL), vs_empty)
        self.assertIn(FAMILY.index(G_FULL), vs_full)
        self.assertNotIn(FAMILY.index(G_EMPTY), vs_full)
        self.assertTrue(len(vs_empty) >= 1 and len(vs_full) >= 1)
        self.assertTrue(set(vs_empty).isdisjoint(set(vs_full)))

    def test_separating_history_contains_truth_excludes_liars(self):
        probes = (PublicProbe(1, 0, 0, 1), PublicProbe(2, 1, 0, 1))
        delivered = simulate_delivered(G_CHAIN, probes)
        h = history_with(probes, delivered)
        vs = version_space(h)
        self.assertIn(FAMILY.index(G_CHAIN), vs)
        for idx in vs:
            for d in delivered:
                self.assertEqual(reachability_mask(FAMILY[idx], d.node), d.affected_mask)

    def test_pending_probe_carries_no_information(self):
        # Probe due at tick 3 with deadline 2: issued but not delivered.
        late = (PublicProbe(1, 0, 0, 3),)
        h_pending = history_with(late, (), deadline=2)
        h_noprobe = history_with((), (), deadline=2)
        self.assertEqual(pending_ids(h_pending), (1,))
        self.assertEqual(version_space(h_pending), version_space(h_noprobe))
        self.assertEqual(posterior(h_pending), posterior(h_noprobe))
        self.assertEqual(score(h_pending), score(h_noprobe))

    def test_censored_feedback_flagged_not_silently_dropped(self):
        probes = (PublicProbe(1, 0, 0, 1),)
        h = history_with(probes, (), censored=(1,))
        self.assertEqual(h.censored, (1,))
        self.assertEqual(h.delivered, ())
        # Version space uses delivered only: censoring widens, never invents.
        self.assertEqual(version_space(h), tuple(range(8)))
        # A censored event must be recorded; an undocumented drop would be
        # indistinguishable from never probing, which is exactly the leak
        # this flag prevents.
        h_silent = history_with((), ())
        self.assertNotEqual(h, h_silent)

    def test_deadline_no_drain(self):
        # Delivered outcome past the deadline is rejected, not scored.
        probes = (PublicProbe(1, 0, 0, 5),)
        late_outcome = simulate_delivered(G_FULL, probes)
        with self.assertRaisesRegex(ValueError, "after deadline"):
            history_with(probes, late_outcome, deadline=2)

    def test_zero_normalizer_rejected_not_labeled(self):
        # Mask 111 for node 2 is impossible in every candidate graph
        # (node 2 reaches only itself), so the history is invalid.
        probes = (PublicProbe(1, 2, 0, 1),)
        impossible = (PublicOutcome(1, 2, 0b111),)
        h = history_with(probes, impossible)
        with self.assertRaisesRegex(ValueError, "zero normalizer"):
            version_space(h)
        with self.assertRaisesRegex(ValueError, "zero normalizer"):
            score(h)

    def test_private_state_never_enters_scorer(self):
        # Same public history built from two different hidden truths.
        probes = (PublicProbe(1, 2, 0, 1),)
        ha = history_with(probes, simulate_delivered(G_EMPTY, probes))
        hb = history_with(probes, simulate_delivered(G_FULL, probes))
        self.assertEqual(ha, hb)
        ra = score(ha)
        rb = score(hb)
        self.assertEqual(ra, rb)
        # Scorer signature takes only (history, family): no edges/influence arg.
        import inspect
        from e001_three_node_version_space import score as score_fn
        params = list(inspect.signature(score_fn).parameters)
        self.assertEqual(params, ["history", "family"])

    def test_replay_determinism(self):
        probes = (PublicProbe(1, 0, 0, 1), PublicProbe(2, 2, 0, 2))
        commits = (PublicCommitment(1, 0, 3),)
        delivered = simulate_delivered(G_CHAIN, (probes[1],))
        h1 = history_with((probes[1],), delivered, commitments=commits, deadline=2)
        h2 = history_with((probes[1],), simulate_delivered(G_CHAIN, (probes[1],)),
                          commitments=commits, deadline=2)
        self.assertEqual(score(h1), score(h2))
        self.assertEqual(posterior(h1), posterior(h2))

    def test_plan_enumeration_and_exact_values(self):
        self.assertEqual(len(all_plans()), 7)  # () + 3 singles + 3 pairs
        self.assertEqual(NODES, 3)
        # Empty history + no commitments: empty plan has utility 0 in every
        # world, any action only adds cost, so () is uniquely optimal at 0.
        h = history_with((), ())
        best, value, _ = score(h)
        self.assertEqual(best, ((),))
        self.assertEqual(value, Fraction(0))
        # Influence sanity: chain graph reaches transitively from 0.
        self.assertEqual(reachability_mask(G_CHAIN, 0), 0b111)
        self.assertEqual(reachability_mask(G_CHAIN, 1), 0b110)
        self.assertEqual(reachability_mask(G_CHAIN, 2), 0b100)
        self.assertEqual(influence_of(G_EMPTY), (0b001, 0b010, 0b100))

    def test_malformed_histories_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate commitment"):
            history_with((), (), commitments=(PublicCommitment(0, 1, 2),
                                              PublicCommitment(0, 0, 2)))
        with self.assertRaisesRegex(ValueError, "duplicate probe"):
            history_with((PublicProbe(1, 0, 0, 1), PublicProbe(1, 1, 0, 1)), ())
        with self.assertRaisesRegex(ValueError, "unissued probe"):
            history_with((), (PublicOutcome(9, 0, 0b001),))
        with self.assertRaisesRegex(ValueError, "both delivered and censored"):
            probes = (PublicProbe(1, 0, 0, 1),)
            delivered = simulate_delivered(G_EMPTY, probes)
            history_with(probes, delivered, censored=(1,))


if __name__ == "__main__":
    unittest.main()
