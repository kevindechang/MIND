"""The claims engine's semantics: locking, sealing, states, ladder, staleness.

Every verdict in the repository depends on these rules, so they are tested
directly, including git sealing in a throwaway repository.
"""
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest

from mind import stats
from mind.claims import Check, Claim, Compare, Evaluation, heldout_seeds, load_claims, seal_commit
from mind.knowledge import assess

CLAIM_SRC = textwrap.dedent('''\
    """{doc}"""
    from mind.claims import Claim, Compare
    CLAIM = Claim(id="C900", title="t", statement="s", kind="effect", scope="L2", about=("memory",),
                  test=Compare(world="vigil", a="organism", b="organism -memory", metric="kept",
                               direction=">", margin={margin}, seeds=16))
''')


def make(cid="C1", margin=0.1, kind="effect", about=("memory",), depends_on=(), retired=None):
    return Claim(id=cid, title=cid, statement="s", kind=kind, scope="L2", about=about,
                 depends_on=depends_on, retired=retired,
                 test=Compare("vigil", "organism", "organism -memory", "kept", ">", margin, 16))


def record(evals, by="alice", env="e1", at="2026-01-01T00:00:00Z", code="c"):
    return {"evaluations": {e.claim: e.to_dict() for e in evals}, "by": by, "environment_id": env,
            "code": code, "recorded_at": at, "mode": "full", "_path": f"knowledge/records/{at}.json"}


def ev(claim, verdict="HOLDS", robust=True, seeds="dev", rivals=None):
    return Evaluation(claim.id, claim.prediction_hash(), verdict, robust, seeds, {}, rivals or {})


BEATEN = {"window4": {"reference": False, "result": "BEATEN"}, "bayes": {"reference": True, "result": "NOT_BEATEN"}}


class PredictionLock(unittest.TestCase):
    def test_prose_is_free_but_the_prediction_is_locked(self):
        a = make()
        b = Claim(**{**a.__dict__, "title": "new words", "statement": "rephrased", "rationale": "more"})
        self.assertEqual(a.prediction_hash(), b.prediction_hash())
        self.assertNotEqual(a.prediction_hash(), make(margin=0.2).prediction_hash())

    def test_check_source_is_part_of_the_prediction(self):
        def f(ctx):
            return {"verdict": "HOLDS"}

        def g(ctx):
            return {"verdict": "FAILS"}
        a = Claim("X1", "t", "s", "fact", "instrument", Check(f))
        b = Claim("X1", "t", "s", "fact", "instrument", Check(g))
        self.assertNotEqual(a.prediction_hash(), b.prediction_hash())


class Statistics(unittest.TestCase):
    def test_nonsignificance_is_not_equivalence(self):
        noisy = stats.compare([0.0, 1.0, 0.0, 1.0, 0.5], [0.5] * 5, "~", 0.1)
        self.assertEqual(noisy["verdict"], stats.INCONCLUSIVE)
        tight = stats.compare([0.50, 0.51, 0.49, 0.50], [0.5] * 4, "~", 0.1)
        self.assertEqual(tight["verdict"], stats.HOLDS)

    def test_superiority_three_valued(self):
        self.assertEqual(stats.compare([1.0] * 8, [0.0] * 8, ">", 0.5)["verdict"], stats.HOLDS)
        self.assertEqual(stats.compare([0.0] * 8, [0.0] * 8, ">", 0.5)["verdict"], stats.FAILS)
        mixed = [0.0, 1.0] * 6
        self.assertEqual(stats.compare(mixed, [0.0] * 12, ">", 0.4)["verdict"], stats.INCONCLUSIVE)


class StatesAndLadder(unittest.TestCase):
    def test_untested_then_ladder(self):
        c = make()
        self.assertEqual(assess({"C1": c}, [])["C1"].state, "UNTESTED")
        st = assess({"C1": c}, [record([ev(c)])])["C1"]
        self.assertEqual((st.state, st.level), ("HOLDS", "ROBUST"))
        st = assess({"C1": c}, [record([ev(c, rivals=BEATEN)])])["C1"]
        self.assertEqual(st.level, "RIVAL-TESTED")

    def test_rival_not_beaten_caps_the_ladder_and_is_reported(self):
        c = make()
        tied = {"window4": {"reference": False, "result": "NOT_BEATEN"}}
        st = assess({"C1": c}, [record([ev(c, rivals=tied, seeds="heldout:abc")])], seals={"C1": "abc"})["C1"]
        self.assertEqual(st.level, "ROBUST")
        self.assertEqual(st.rivals_not_beaten, ["window4"])

    def test_preregistered_needs_matching_seal_and_replicated_needs_two_contributors(self):
        c = make()
        recs = [record([ev(c, rivals=BEATEN, seeds="heldout:abc")])]
        self.assertEqual(assess({"C1": c}, recs, seals={"C1": "abc"})["C1"].level, "PREREGISTERED")
        self.assertEqual(assess({"C1": c}, recs, seals={"C1": "zzz"})["C1"].level, "RIVAL-TESTED")
        recs.append(record([ev(c, rivals=BEATEN, seeds="heldout:abc")], by="bob", env="e2",
                           at="2026-02-01T00:00:00Z"))
        self.assertEqual(assess({"C1": c}, recs, seals={"C1": "abc"})["C1"].level, "REPLICATED")
        same_person = recs[:1] + [record([ev(c, rivals=BEATEN)], by="alice", env="e2", at="2026-03-01T00:00:00Z")]
        self.assertEqual(assess({"C1": c}, same_person, seals={"C1": "abc"})["C1"].level, "PREREGISTERED")

    def test_side_effect_claims_skip_the_rival_rung(self):
        c = make(about=())
        self.assertNotIn("RIVAL-TESTED", c.ladder)
        st = assess({"C1": c}, [record([ev(c, seeds="heldout:s")])], seals={"C1": "s"})["C1"]
        self.assertEqual(st.level, "PREREGISTERED")

    def test_broken_versus_refuted(self):
        c = make()
        held = record([ev(c)], at="2026-01-01T00:00:00Z")
        regress = record([ev(c, "FAILS", robust=False)], at="2026-02-01T00:00:00Z")
        self.assertEqual(assess({"C1": c}, [held, regress])["C1"].state, "BROKEN")
        self.assertEqual(assess({"C1": c}, [regress])["C1"].state, "REFUTED")
        heldout_fail = record([ev(c, "FAILS", robust=False, seeds="heldout:s")], at="2026-02-01T00:00:00Z")
        st = assess({"C1": c}, [held, heldout_fail], seals={"C1": "s"})["C1"]
        self.assertEqual(st.state, "REFUTED")
        self.assertTrue(any("did not generalise" in n for n in st.notes))

    def test_dev_reruns_cannot_overwrite_a_failed_heldout_confirmation(self):
        c = make()
        recs = [record([ev(c, "FAILS", robust=False, seeds="heldout:s")], at="2026-01-01T00:00:00Z"),
                record([ev(c)], at="2026-06-01T00:00:00Z")]
        self.assertEqual(assess({"C1": c}, recs, seals={"C1": "s"})["C1"].state, "REFUTED")

    def test_amended_prediction_starts_over(self):
        old, new = make(margin=0.1), make(margin=0.3)
        st = assess({"C1": new}, [record([ev(old)])])["C1"]
        self.assertEqual(st.state, "UNTESTED")

    def test_staleness_propagates_transitively_and_retirement_counts(self):
        a, b, c = make("A"), make("B", depends_on=("A",)), make("C", depends_on=("B",))
        fail_a = record([ev(a, "FAILS", robust=False), ev(b), ev(c)])
        states = assess({"A": a, "B": b, "C": c}, [fail_a])
        self.assertEqual([states[x].state for x in "ABC"], ["REFUTED", "STALE", "STALE"])
        retired = make("A", retired="superseded by D")
        states = assess({"A": retired, "B": b, "C": c}, [record([ev(retired), ev(b), ev(c)])])
        self.assertEqual([states[x].state for x in "ABC"], ["RETIRED", "STALE", "STALE"])
        self.assertEqual(states["C"].notes.count("premise B is STALE"), 1)


class Sealing(unittest.TestCase):
    def test_seal_is_the_registering_commit_and_unknowable_in_advance(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            run = lambda *a: subprocess.run(["git", *a], cwd=root, check=True, capture_output=True, text=True)
            run("init", "-q")
            run("config", "user.email", "t@example.com")
            run("config", "user.name", "t")
            claims_dir = root / "knowledge" / "claims"
            claims_dir.mkdir(parents=True)
            path = claims_dir / "C900_x.py"
            path.write_text(CLAIM_SRC.format(doc="v1", margin=0.1))
            claim = load_claims(claims_dir, root)["C900"]
            self.assertIsNone(seal_commit(claim, root))           # uncommitted: no held-out seeds exist
            run("add", ".")
            run("commit", "-q", "-m", "register")
            first = run("rev-parse", "HEAD").stdout.strip()
            self.assertEqual(seal_commit(claim, root), first)
            path.write_text(CLAIM_SRC.format(doc="clearer prose", margin=0.1))
            run("commit", "-qam", "prose")
            self.assertEqual(seal_commit(load_claims(claims_dir, root)["C900"], root), first)
            path.write_text(CLAIM_SRC.format(doc="v2", margin=0.3))
            run("commit", "-qam", "amend prediction")
            amended = load_claims(claims_dir, root)["C900"]
            second = run("rev-parse", "HEAD").stdout.strip()
            self.assertEqual(seal_commit(amended, root), second)
            self.assertNotEqual(heldout_seeds(claim, first, 16), heldout_seeds(amended, second, 16))
            self.assertEqual(heldout_seeds(claim, first, 16), heldout_seeds(claim, first, 16))
            self.assertTrue(all(s >= 10_000 for s in heldout_seeds(claim, first, 16)))


if __name__ == "__main__":
    unittest.main()
