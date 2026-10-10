"""Append-only, hash-chained event ledger: the organism's ONLY durable state.

Every organ state is a deterministic fold over these events, so a process can be
SIGKILLed at any point and a fresh process rebuilds the identical organism from
the ledger alone (generalising E100 Day 0). Each event's hash chains to the
previous one; the head hash is the ledger's identity, which makes forks
(E100 Day 7) and tampering visible.

Two interchangeable backends: MemoryLedger (fast experiments) and SqliteLedger
(real process-death tests). Python standard library only.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
from typing import Any, Dict, Iterator, List, Optional

GENESIS_HASH = "0" * 64


class LedgerCorrupt(Exception):
    """The hash chain does not verify."""


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def link(prev_hash: str, kind: str, payload_json: str) -> str:
    return hashlib.sha256(f"{prev_hash}|{kind}|{payload_json}".encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Event:
    seq: int
    kind: str
    payload: Dict[str, Any]
    hash: str


class Ledger:
    """Common interface. Events are numbered from 0 and never rewritten."""

    def append(self, kind: str, payload: Dict[str, Any]) -> Event:
        raise NotImplementedError

    def __iter__(self) -> Iterator[Event]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    @property
    def head(self) -> str:
        raise NotImplementedError

    def fork(self, path: Optional[Path] = None) -> "Ledger":
        """An independent copy sharing this ledger's exact history."""
        raise NotImplementedError

    def close(self) -> None:
        pass

    def verify(self) -> str:
        """Recompute the whole chain; return the head or raise LedgerCorrupt."""
        prev = GENESIS_HASH
        for expected_seq, event in enumerate(self):
            if event.seq != expected_seq:
                raise LedgerCorrupt(f"sequence gap at {expected_seq}")
            h = link(prev, event.kind, canonical(event.payload))
            if h != event.hash:
                raise LedgerCorrupt(f"hash mismatch at seq {event.seq}")
            prev = h
        if prev != self.head:
            raise LedgerCorrupt("head does not match chain")
        return prev


class MemoryLedger(Ledger):
    def __init__(self) -> None:
        self._events: List[Event] = []
        self._head = GENESIS_HASH

    def append(self, kind: str, payload: Dict[str, Any]) -> Event:
        text = canonical(payload)
        h = link(self._head, kind, text)
        # Store a JSON round-trip so live and replayed payloads are identical objects.
        event = Event(len(self._events), kind, json.loads(text), h)
        self._events.append(event)
        self._head = h
        return event

    def __iter__(self) -> Iterator[Event]:
        return iter(list(self._events))

    def __len__(self) -> int:
        return len(self._events)

    @property
    def head(self) -> str:
        return self._head

    def fork(self, path: Optional[Path] = None) -> "MemoryLedger":
        other = MemoryLedger()
        other._events = list(self._events)
        other._head = self._head
        return other


class SqliteLedger(Ledger):
    """File-backed ledger. An append is acknowledged only after its commit returns,
    so a SIGKILL can lose an unacknowledged tick but never half of one."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self._db = sqlite3.connect(str(self.path), timeout=10, isolation_level=None)
        self._db.execute("PRAGMA journal_mode=DELETE")
        self._db.execute("PRAGMA synchronous=FULL")
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS events ("
            " seq INTEGER PRIMARY KEY, kind TEXT NOT NULL,"
            " payload TEXT NOT NULL, hash TEXT NOT NULL UNIQUE)")
        row = self._db.execute("SELECT hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
        self._head = row[0] if row else GENESIS_HASH
        self._len = self._db.execute("SELECT COUNT(*) FROM events").fetchone()[0]

    def append(self, kind: str, payload: Dict[str, Any]) -> Event:
        text = canonical(payload)
        h = link(self._head, kind, text)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            self._db.execute("INSERT INTO events(seq, kind, payload, hash) VALUES (?,?,?,?)",
                             (self._len, kind, text, h))
            self._db.execute("COMMIT")
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        event = Event(self._len, kind, json.loads(text), h)
        self._len += 1
        self._head = h
        return event

    def __iter__(self) -> Iterator[Event]:
        rows = self._db.execute("SELECT seq, kind, payload, hash FROM events ORDER BY seq").fetchall()
        return iter([Event(seq, kind, json.loads(text), h) for seq, kind, text, h in rows])

    def __len__(self) -> int:
        return self._len

    @property
    def head(self) -> str:
        return self._head

    def fork(self, path: Optional[Path] = None) -> "SqliteLedger":
        if path is None:
            raise ValueError("a file-backed fork needs a destination path")
        shutil.copyfile(self.path, path)
        return SqliteLedger(Path(path))

    def close(self) -> None:
        self._db.close()
