"""H070 integration probes using MIND's native organism and verified ledgers.

No LLMs, paid services, held-out seeds, or scientific outcome claims.
These are executable regression tests; they do not establish model-swap transfer.
"""
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mind.kernel import Organism
from mind.ledger import LedgerCorrupt, MemoryLedger, SqliteLedger
from mind.portable_state import PortableEventError, encode_event, project


def _event(kind, eid, *, epoch=0, **fields):
    return {
        "kind": kind, "event_id": eid, "subject": "synthetic-person",
        "epoch": epoch, **fields,
    }


def _step(organism, event, *, boundary=False):
    return organism.step(
        {"portable_event": encode_event(event)},
        boundary=boundary,
        actions=("wait", "review"),
    )


class NativeLedgerPortableStateTests(unittest.TestCase):
    def test_real_organism_restores_correction_and_repeated_projection(self):
        ledger = MemoryLedger()
        original = Organism("organism", seed=21, ledger=ledger)
        first_decision = _step(
            original,
            _event("belief", "b1", key="preferred_time", value="morning",
                   source_id="synthetic-turn-1"),
            boundary=True,
        )
        _step(original, _event(
            "correct", "b2", key="preferred_time", value="evening",
            source_id="synthetic-turn-2", supersedes="b1",
        ))
        prior = project(ledger, "synthetic-person")
        self.assertEqual(prior.beliefs[0].value, "evening")
        self.assertEqual(prior.beliefs[0].replaces, "b1")
        self.assertEqual(prior.ledger_head, ledger.head)

        recovered = Organism.restore(ledger)
        after = project(recovered.ledger, "synthetic-person")
        self.assertEqual(after.as_dict(), prior.as_dict())
        # An already-logged step must not act twice on an at-least-once retry.
        self.assertEqual(recovered.step_at(0, {"portable_event": "ignored"}), first_decision)

    def test_sqlite_close_reopen_restore_keeps_forget_fence(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "research-ledger.sqlite3"
            disk = SqliteLedger(path)
            org = Organism("organism", seed=22, ledger=disk)
            _step(org, _event("belief", "b1", key="food", value="old",
                              source_id="synthetic-source-1"), boundary=True)
            _step(org, _event("forget", "f1", epoch=1))
            _step(org, _event("belief", "b2", epoch=1, key="food", value="new",
                              source_id="synthetic-source-2"))
            snapshot = project(disk, "synthetic-person").as_dict()
            self.assertEqual(snapshot["epoch"], 1)
            self.assertEqual(snapshot["beliefs"][0]["value"], "new")
            disk.close()

            disk2 = SqliteLedger(path)
            try:
                restored = Organism.restore(disk2)
                self.assertEqual(project(restored.ledger, "synthetic-person").as_dict(), snapshot)
                with self.assertRaisesRegex(PortableEventError, "revoked"):
                    # Project a native fork with an attempted old-source resurrection.
                    fork = disk2.fork(Path(directory) / "fork.sqlite3")
                    try:
                        fork.append("tick", {"obs": {"portable_event": encode_event(
                            _event("belief", "b3", epoch=1, key="food",
                                   value="old", source_id="synthetic-source-1"))}})
                        project(fork, "synthetic-person")
                    finally:
                        fork.close()
            finally:
                disk2.close()

    def test_native_hash_chain_tampering_is_rejected_before_projection(self):
        ledger = MemoryLedger()
        org = Organism("organism", seed=23, ledger=ledger)
        _step(org, _event("belief", "b1", key="color", value="blue",
                          source_id="synthetic-source"), boundary=True)
        self.assertEqual(len(project(ledger, "synthetic-person").beliefs), 1)
        # Deliberately modify an event after hashing, leaving its saved hash intact.
        old = ledger._events[-1]
        altered = dict(old.payload)
        altered["obs"] = {"portable_event": encode_event(
            _event("belief", "b1", key="color", value="red",
                   source_id="synthetic-source"))}
        ledger._events[-1] = replace(old, payload=altered)
        with self.assertRaises(LedgerCorrupt):
            project(ledger, "synthetic-person")

    def test_real_ledger_keeps_foreign_subject_out_of_projection(self):
        ledger = MemoryLedger()
        org = Organism("organism", seed=24, ledger=ledger)
        _step(org, _event("belief", "a", key="k", value="mine",
                          source_id="a-source"), boundary=True)
        foreign = _event("belief", "b", key="k", value="theirs",
                         source_id="b-source")
        foreign["subject"] = "another-synthetic-person"
        _step(org, foreign)
        state = project(ledger, "synthetic-person")
        self.assertEqual([b.value for b in state.beliefs], ["mine"])


if __name__ == "__main__":
    unittest.main()
