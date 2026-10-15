"""Read-only projection of portable evidence carried by the MIND tick ledger.

Issue #70, stage 1. This is *not* a second organism, memory organ, or
claim-scoring mechanism. The projection is optional and has no control over
Organism.step. LLM interpretation and policy integration are future work.

Input convention: a tick's obs may contain ``portable_event`` as a JSON
string. It is a deliberately explicit, bounded event protocol; arbitrary
user text must never be interpreted here as authoritative evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple

FIELD = "portable_event"
KINDS = frozenset({"belief", "correct", "retract", "commit", "close", "forget", "revoke_source"})


class PortableEventError(ValueError):
    """Malformed, conflicting or out-of-epoch evidence in the event stream."""


@dataclass(frozen=True)
class Belief:
    key: str
    value: str
    source_id: str
    event_id: str
    epoch: int
    replaces: Optional[str] = None


@dataclass(frozen=True)
class Commitment:
    task: str
    event_id: str
    source_id: str
    epoch: int


@dataclass(frozen=True)
class PortableState:
    subject: str
    epoch: int
    beliefs: Tuple[Belief, ...]
    commitments: Tuple[Commitment, ...]
    ledger_head: Optional[str]

    def as_dict(self) -> Dict[str, Any]:
        return {"subject": self.subject, "epoch": self.epoch,
                "beliefs": [b.__dict__.copy() for b in self.beliefs],
                "commitments": [c.__dict__.copy() for c in self.commitments],
                "ledger_head": self.ledger_head}


def encode_event(event: Mapping[str, Any]) -> str:
    """Canonical JSON suitable for a tick observation's portable_event value."""
    validate_event(event)
    return json.dumps(dict(event), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def _required_text(event: Mapping[str, Any], key: str) -> str:
    value = event.get(key)
    if not isinstance(value, str) or not value.strip() or len(value) > 1024:
        raise PortableEventError(f"{key} must be a nonempty string <= 1024 chars")
    return value


def validate_event(event: Mapping[str, Any]) -> None:
    if not isinstance(event, dict):
        raise PortableEventError("portable event must be a JSON object")
    kind = _required_text(event, "kind")
    if kind not in KINDS:
        raise PortableEventError(f"unknown portable kind {kind!r}")
    _required_text(event, "subject")
    _required_text(event, "event_id")
    if type(event.get("epoch")) is not int or event["epoch"] < 0:
        raise PortableEventError("epoch must be a nonnegative integer")
    if kind in ("belief", "correct"):
        _required_text(event, "key")
        if not isinstance(event.get("value"), str) or len(event["value"]) > 4096:
            raise PortableEventError("value must be a string <= 4096 chars")
        _required_text(event, "source_id")
        if kind == "correct":
            _required_text(event, "supersedes")
    elif kind == "retract":
        _required_text(event, "target")
    elif kind == "commit":
        _required_text(event, "task")
        _required_text(event, "source_id")
    elif kind == "close":
        _required_text(event, "target")
    elif kind == "revoke_source":
        _required_text(event, "target_source")
    elif kind == "forget":
        pass
    allowed = {"kind", "subject", "event_id", "epoch"}
    allowed |= {"key", "value", "source_id"} if kind == "belief" else set()
    allowed |= {"key", "value", "source_id", "supersedes"} if kind == "correct" else set()
    allowed |= {"target"} if kind in ("retract", "close") else set()
    allowed |= {"task", "source_id"} if kind == "commit" else set()
    allowed |= {"target_source"} if kind == "revoke_source" else set()
    if set(event) - allowed:
        raise PortableEventError(f"unexpected keys: {sorted(set(event) - allowed)}")


def _decode(raw: Any) -> Dict[str, Any]:
    if not isinstance(raw, str) or len(raw) > 8192:
        raise PortableEventError("portable_event must be bounded JSON text")
    try:
        event = json.loads(raw)
    except (TypeError, ValueError) as exc:
        raise PortableEventError("portable_event is not JSON") from exc
    validate_event(event)
    return event


def project(ledger: Iterable[Any], subject: str, *, verify: bool = True) -> PortableState:
    """Project a single subject from existing ``genesis/tick/end/lesion`` events.

    No writes, no model calls, no private scorer info. The actual MIND ledger
    is expected to implement verify() and head; in-memory test doubles can
    implement the same interface. Duplicate event IDs must have identical
    JSON; they are not applied twice. Forget increments the epoch and
    invalidates prior knowledge, including commitments and event targets.
    """
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("subject is required")
    if verify:
        checker = getattr(ledger, "verify", None)
        if not callable(checker):
            raise PortableEventError("ledger has no verify method")
        checker()
    epoch = 0
    seen: Dict[str, str] = {}
    beliefs_by_id: Dict[str, Belief] = {}
    current: Dict[str, str] = {}
    tasks: Dict[str, Commitment] = {}
    revoked_sources: set[str] = set()
    for item in ledger:
        if item.kind != "tick":
            continue
        obs = item.payload.get("obs", {})
        if not isinstance(obs, dict) or FIELD not in obs:
            continue
        e = _decode(obs[FIELD])
        if e["subject"] != subject:
            continue
        eid = e["event_id"]
        canonical = encode_event(e)
        if eid in seen:
            if seen[eid] != canonical:
                raise PortableEventError(f"event ID collision {eid!r}")
            continue
        if e["kind"] == "forget":
            if e["epoch"] != epoch + 1:
                raise PortableEventError("forget must advance the subject epoch by one")
            epoch += 1
            beliefs_by_id.clear()
            current.clear()
            tasks.clear()
            revoked_sources.clear()
        else:
            if e["epoch"] != epoch:
                raise PortableEventError("out-of-epoch evidence may not be resurrected")
            kind = e["kind"]
            if kind in ("belief", "correct", "commit") and e["source_id"] in revoked_sources:
                raise PortableEventError("cannot reuse revoked source")
            if kind == "belief":
                if e["key"] in current:
                    raise PortableEventError("existing belief requires explicit correction")
                b = Belief(e["key"], e["value"], e["source_id"], eid, epoch)
                beliefs_by_id[eid] = b
                current[b.key] = eid
            elif kind == "correct":
                prev = beliefs_by_id.get(e["supersedes"])
                if prev is None or current.get(prev.key) != prev.event_id or prev.key != e["key"]:
                    raise PortableEventError("correction must supersede current same-subject belief")
                b = Belief(e["key"], e["value"], e["source_id"], eid, epoch, prev.event_id)
                beliefs_by_id[eid] = b
                current[b.key] = eid
            elif kind == "retract":
                prev = beliefs_by_id.get(e["target"])
                if prev is None or current.get(prev.key) != prev.event_id:
                    raise PortableEventError("retraction must target current same-subject belief")
                del current[prev.key]
            elif kind == "commit":
                tasks[eid] = Commitment(e["task"], eid, e["source_id"], epoch)
            elif kind == "close":
                if e["target"] not in tasks:
                    raise PortableEventError("close must target a pending same-subject commitment")
                del tasks[e["target"]]
            elif kind == "revoke_source":
                revoked_sources.add(e["target_source"])
                for key, active_id in list(current.items()):
                    cursor = beliefs_by_id[active_id]
                    while True:
                        if cursor.source_id in revoked_sources:
                            del current[key]
                            break
                        if cursor.replaces is None:
                            break
                        cursor = beliefs_by_id[cursor.replaces]
                for cid, task in list(tasks.items()):
                    if task.source_id in revoked_sources:
                        del tasks[cid]
        seen[eid] = canonical
    head = getattr(ledger, "head", None)
    return PortableState(subject, epoch,
                         tuple(beliefs_by_id[current[k]] for k in sorted(current)),
                         tuple(tasks[k] for k in sorted(tasks)), head)
