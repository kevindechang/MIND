"""Issue #70 stage-1 tests: project existing tick-ledger records, not a new organism."""
import json
from dataclasses import dataclass
import unittest

from mind.portable_state import PortableEventError, encode_event, project


@dataclass(frozen=True)
class Tick:
    kind: str
    payload: dict


class Ledger:
    def __init__(self, events):
        self.events = events
        self.head = "verified-test-head"
        self.verification_calls = 0

    def verify(self):
        self.verification_calls += 1
        return self.head

    def __iter__(self):
        return iter(self.events)


def event(kind, eid, subject="person-A", epoch=0, **kwargs):
    return {"kind": kind, "event_id": eid, "subject": subject, "epoch": epoch, **kwargs}


def tick(e):
    return Tick("tick", {"obs": {"portable_event": encode_event(e)}})


class PortableStateTests(unittest.TestCase):
    def test_correct_and_replay(self):
        raw = [tick(event("belief", "b1", key="genre", value="jazz", source_id="turn-1")),
               tick(event("correct", "b2", key="genre", value="rock", source_id="turn-2", supersedes="b1"))]
        log = Ledger(raw)
        one = project(log, "person-A").as_dict()
        self.assertEqual(one["beliefs"][0]["value"], "rock")
        self.assertEqual(one["beliefs"][0]["replaces"], "b1")
        self.assertEqual(one, project(log, "person-A").as_dict())
        self.assertEqual(log.verification_calls, 2)

    def test_events_are_exactly_once_by_id(self):
        same = tick(event("belief", "b1", key="kind", value="A", source_id="s"))
        self.assertEqual(len(project(Ledger([same, same]), "person-A").beliefs), 1)

    def test_conflicting_event_id_rejected(self):
        items = [tick(event("belief", "b1", key="kind", value="A", source_id="s")),
                 tick(event("belief", "b1", key="kind", value="B", source_id="s"))]
        with self.assertRaisesRegex(PortableEventError, "collision"):
            project(Ledger(items), "person-A")

    def test_retract_must_target_current(self):
        items = [tick(event("belief", "b1", key="kind", value="A", source_id="s")),
                 tick(event("retract", "r1", target="b1"))]
        self.assertEqual(project(Ledger(items), "person-A").beliefs, ())
        with self.assertRaisesRegex(PortableEventError, "current"):
            project(Ledger(items + [tick(event("retract", "r2", target="b1"))]), "person-A")

    def test_commit_close(self):
        items = [tick(event("commit", "c1", task="call doctor", source_id="s"))]
        self.assertEqual(len(project(Ledger(items), "person-A").commitments), 1)
        items += [tick(event("close", "cl1", target="c1"))]
        self.assertEqual(project(Ledger(items), "person-A").commitments, ())

    def test_forget_fences_prior_beliefs_and_goals(self):
        items = [tick(event("belief", "b1", key="k", value="v", source_id="s")),
                 tick(event("commit", "c1", task="x", source_id="s")),
                 tick(event("forget", "f1", epoch=1))]
        state = project(Ledger(items), "person-A")
        self.assertEqual((state.epoch, state.beliefs, state.commitments), (1, (), ()))
        with self.assertRaisesRegex(PortableEventError, "out-of-epoch"):
            project(Ledger(items + [tick(event("belief", "b2", key="k", value="old", source_id="s"))]), "person-A")
        # Epoch 1 can legitimately contain new source evidence.
        after = items + [tick(event("belief", "b2", epoch=1, key="k", value="new", source_id="s2"))]
        self.assertEqual(project(Ledger(after), "person-A").beliefs[0].value, "new")

    def test_cross_subject_isolation(self):
        items = [tick(event("belief", "a1", key="k", value="A", source_id="s")),
                 tick(event("belief", "b1", "person-B", key="k", value="B", source_id="s"))]
        self.assertEqual(project(Ledger(items), "person-A").beliefs[0].value, "A")
        self.assertEqual(project(Ledger(items), "person-B").beliefs[0].value, "B")

    def test_cross_subject_correction_and_close_rejected(self):
        items = [tick(event("belief", "a1", key="k", value="A", source_id="s")),
                 tick(event("correct", "b1", "person-B", key="k", value="B", source_id="s", supersedes="a1"))]
        with self.assertRaises(PortableEventError):
            project(Ledger(items), "person-B")

    def test_forgery_or_malformed_event_fails_closed(self):
        with self.assertRaises(PortableEventError):
            encode_event({"kind": "belief", "event_id": "b", "subject": "p", "epoch": 0,
                          "key": "k", "value": "v", "source_id": "s", "allow_unknown": True})
        with self.assertRaises(PortableEventError):
            project(Ledger([Tick("tick", {"obs": {"portable_event": "not-json"}})]), "person-A")

    def test_verify_mandatory_and_no_non_tick_inference(self):
        good = tick(event("belief", "b", key="k", value="v", source_id="s"))
        self.assertEqual(len(project(Ledger([Tick("end", {"obs": {"portable_event": "bad"}}), good]), "person-A").beliefs), 1)
        with self.assertRaises(PortableEventError):
            project([good], "person-A")

    def test_source_revocation_invalidates_derived_beliefs_and_commitments(self):
        items = [tick(event("belief", "b1", key="genre", value="jazz", source_id="revoked-1")),
                 tick(event("correct", "b2", key="genre", value="rock", source_id="later-2", supersedes="b1")),
                 tick(event("commit", "c1", task="tell a friend", source_id="revoked-1")),
                 tick(event("revoke_source", "r1", target_source="revoked-1"))]
        state = project(Ledger(items), "person-A")
        self.assertEqual((state.beliefs, state.commitments), ((), ()))
        with self.assertRaisesRegex(PortableEventError, "revoked"):
            project(Ledger(items + [tick(event("belief", "b3", key="genre", value="rock", source_id="revoked-1"))]), "person-A")

    def test_forget_rejects_reuse_of_prior_epoch_source(self):
        items = [tick(event("belief", "b1", key="k", value="v", source_id="old-source")),
                 tick(event("forget", "f1", epoch=1)),
                 tick(event("belief", "b2", epoch=1, key="k", value="v", source_id="old-source"))]
        with self.assertRaisesRegex(PortableEventError, "revoked"):
            project(Ledger(items), "person-A")

    def test_projection_does_not_mutate_log(self):
        entries = [tick(event("belief", "b", key="k", value="v", source_id="s"))]
        log = Ledger(entries)
        project(log, "person-A")
        self.assertEqual(log.events, entries)


if __name__ == "__main__":
    unittest.main()
