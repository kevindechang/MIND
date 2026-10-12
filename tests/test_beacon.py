"""P001: held-out seeds from public randomness the registrant does not control.

The network is never touched here: the beacon and GitHub activity are injected.
"""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from mind import beacon, knowledge
from mind.claims import Claim, Compare, Evaluation, heldout_seeds
from mind.knowledge import _first_heldout

SEAL = "a" * 40
SIG = "b44679b9a59af2ec876b1a6b1ad52ea9b1615fc3982b19576350f93447cb1125e342b73a8dd2bacbe47e4b6b63ed5e39"
RAND = hashlib.sha256(bytes.fromhex(SIG)).hexdigest()


def claim():
    return Claim(id="C900", title="t", statement="s", kind="effect", scope="L2", about=("memory",),
                 test=Compare("vigil", "organism", "organism -memory", "kept", ">", 0.1, 16))


def receipt(round_=1000, push_time="2023-08-23T15:59:00Z"):
    return {"chain": beacon.QUICKNET["hash"], "round": round_, "randomness": RAND, "signature": SIG,
            "push": {"time": push_time, "activity_id": 1, "ref": "refs/heads/main", "after": SEAL}}


class RoundMath(unittest.TestCase):
    def test_round_time_matches_genesis_and_period(self):
        self.assertEqual(beacon.round_time(1), beacon.QUICKNET["genesis_time"])
        self.assertEqual(beacon.round_time(11), beacon.QUICKNET["genesis_time"] + 30)

    def test_round_after_is_strictly_later(self):
        g = beacon.QUICKNET["genesis_time"]
        self.assertEqual(beacon.round_after(g), 2)            # round 1 is AT t, not after
        self.assertEqual(beacon.round_after(g + 1), 2)
        self.assertEqual(beacon.round_after(g + 3), 3)
        for t in (g + 7, g + 10_000, g + 123_456):
            r = beacon.round_after(t)
            self.assertGreater(beacon.round_time(r), t)
            self.assertLessEqual(beacon.round_time(r - 1), t)


class Randomness(unittest.TestCase):
    def test_randomness_is_hash_of_signature(self):
        self.assertTrue(beacon.consistent({"randomness": RAND, "signature": SIG}))
        self.assertFalse(beacon.consistent({"randomness": "00" * 32, "signature": SIG}))

    def test_seeds_depend_on_beacon_randomness(self):
        c = claim()
        drawn = heldout_seeds(c, beacon.extended_seal(SEAL, {"randomness": RAND}), 16)
        self.assertNotEqual(heldout_seeds(c, SEAL, 16), drawn)
        self.assertEqual(drawn, heldout_seeds(c, beacon.extended_seal(SEAL, {"randomness": RAND}), 16))
        self.assertNotEqual(drawn, heldout_seeds(c, beacon.extended_seal(SEAL, {"randomness": "11" * 32}), 16))
        self.assertEqual(len(set(drawn)), 16)

    def test_commit_sealed_seeds_are_unchanged(self):
        self.assertEqual(beacon.extended_seal(SEAL, None), SEAL)


class FirstPush(unittest.TestCase):
    ACTIVITY = [
        {"id": 1, "timestamp": "2026-10-10T10:00:00Z", "ref": "refs/heads/main", "after": "c1",
         "activity_type": "push"},
        {"id": 2, "timestamp": "2026-10-10T11:00:00Z", "ref": "refs/heads/contrib/x", "after": "c2",
         "activity_type": "branch_creation"},
        {"id": 3, "timestamp": "2026-10-10T12:00:00Z", "ref": "refs/heads/main", "after": "c3",
         "activity_type": "pr_merge"},
        {"id": 4, "timestamp": "2026-10-10T13:00:00Z", "ref": "refs/heads/gone", "after": "0" * 40,
         "activity_type": "branch_deletion"},
    ]

    def test_earliest_push_containing_the_seal_wins(self):
        contains = {"c1": False, "c2": True, "c3": True}
        push = beacon.first_push(SEAL, self.ACTIVITY, lambda seal, after: contains.get(after, False))
        self.assertEqual(push["activity_id"], 2)
        self.assertEqual(push["time"], "2026-10-10T11:00:00Z")

    def test_order_of_listing_does_not_matter(self):
        contains = {"c2": True, "c3": True}
        push = beacon.first_push(SEAL, list(reversed(self.ACTIVITY)), lambda s, a: contains.get(a, False))
        self.assertEqual(push["activity_id"], 2)

    def test_unpushed_seal_has_no_push(self):
        self.assertIsNone(beacon.first_push(SEAL, self.ACTIVITY, lambda s, a: False))


class Receipt(unittest.TestCase):
    def test_draw_binds_round_to_push_time(self):
        push = {"time": "2026-10-10T11:00:00Z", "activity_id": 2, "ref": "refs/heads/x", "after": "c2"}
        seen = []

        def fetch(r):
            seen.append(r)
            return {"round": r, "randomness": RAND, "signature": SIG}

        rec = beacon.draw(push, fetch)
        self.assertEqual(seen, [beacon.round_after(beacon.parse_time(push["time"]))])
        self.assertEqual(rec["round"], seen[0])
        self.assertEqual(rec["push"], push)
        self.assertEqual(beacon.verify_offline(rec), [])

    def test_draw_waits_for_the_round_to_be_published(self):
        push = {"time": "2023-08-23T15:59:00Z", "activity_id": 2, "ref": "refs/heads/x", "after": "c2"}
        due = beacon.round_time(beacon.round_after(beacon.parse_time(push["time"])))
        waits = []
        beacon.draw(push, fetch=lambda r: {"randomness": RAND, "signature": SIG},
                    clock=lambda: due - 10, pause=waits.append)
        self.assertEqual(waits, [11])                         # until due + 1s
        waits.clear()
        beacon.draw(push, fetch=lambda r: {"randomness": RAND, "signature": SIG},
                    clock=lambda: due + 60, pause=waits.append)
        self.assertEqual(waits, [])                           # already published: no wait

    def test_offline_verification_catches_tampering(self):
        good = receipt(round_=beacon.round_after(beacon.parse_time("2023-08-23T15:59:00Z")))
        self.assertEqual(beacon.verify_offline(good), [])
        early = dict(good, round=good["round"] - 1)          # a round already public at push time
        self.assertTrue(any("round" in p for p in beacon.verify_offline(early)))
        forged = dict(good, randomness="00" * 32)
        self.assertTrue(any("randomness" in p for p in beacon.verify_offline(forged)))
        other = dict(good, chain="ff" * 32)
        self.assertTrue(any("chain" in p for p in beacon.verify_offline(other)))

    def test_label_round_trip(self):
        self.assertEqual(beacon.label(SEAL, None), f"heldout:{SEAL}")
        self.assertEqual(beacon.label(SEAL, {"randomness": RAND}), f"heldout:{SEAL}+drand:{RAND}")
        self.assertEqual(beacon.parse_label(f"heldout:{SEAL}+drand:{RAND}"), (SEAL, RAND))
        self.assertEqual(beacon.parse_label(f"heldout:{SEAL}"), (SEAL, None))
        self.assertEqual(beacon.parse_label("dev"), (None, None))


class DoctorReceipts(unittest.TestCase):
    def setUp(self):
        from mind.doctor import _beacon_problems
        self.check = _beacon_problems
        self.rec = receipt(round_=beacon.round_after(beacon.parse_time("2023-08-23T15:59:00Z")))

    def problems(self, seeds, rec):
        e = {"seeds": seeds, **({"beacon": rec} if rec is not None else {})}
        return self.check("C900", "r.json", e, online=False)

    def test_commit_sealed_records_need_no_receipt(self):
        self.assertEqual(self.problems(f"heldout:{SEAL}", None), [])

    def test_valid_receipt_passes(self):
        self.assertEqual(self.problems(beacon.label(SEAL, self.rec), self.rec), [])

    def test_label_without_matching_receipt_fails(self):
        self.assertTrue(self.problems(beacon.label(SEAL, self.rec), None))
        self.assertTrue(self.problems(f"heldout:{SEAL}+drand:{'11' * 32}", self.rec))
        self.assertTrue(self.problems(f"heldout:{SEAL}", self.rec))

    def test_tampered_receipt_fails(self):
        bad = dict(self.rec, round=self.rec["round"] - 1)       # a round already public at push time
        self.assertTrue(self.problems(beacon.label(SEAL, bad), bad))


class RecordWriting(unittest.TestCase):
    def test_receipt_is_stored_beside_its_evaluation(self):
        rec = receipt()
        evs = [Evaluation("C900", "h", "HOLDS", True, beacon.label(SEAL, rec)),
               Evaluation("C901", "h", "HOLDS", True, f"heldout:{SEAL}")]
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(knowledge, "RECORDS_DIR", Path(tmp)):
            path = knowledge.write_record(evs, "heldout", "tester", "code", beacons={"C900": rec})
            data = json.loads(path.read_text())
        self.assertEqual(data["evaluations"]["C900"]["beacon"], rec)
        self.assertNotIn("beacon", data["evaluations"]["C901"])


class Preregistration(unittest.TestCase):
    def ev(self, seeds, at):
        return {"seeds": seeds, "_record": f"r{at}", "_at": at, "verdict": "HOLDS", "robust": True}

    def test_first_heldout_of_either_kind_decides(self):
        plain = self.ev(f"heldout:{SEAL}", "2026-10-10")
        drawn = self.ev(f"heldout:{SEAL}+drand:{RAND}", "2026-10-11")
        self.assertIs(_first_heldout([drawn, plain], SEAL), plain)
        self.assertIs(_first_heldout([drawn], SEAL), drawn)
        self.assertIsNone(_first_heldout([self.ev(f"heldout:{'b' * 40}+drand:{RAND}", "x")], SEAL))


if __name__ == "__main__":
    unittest.main()
