"""Records, computed evidence levels, staleness propagation, questions and the frontier.

Nothing here is asserted by hand. A claim's state and level are computed from
(a) its prediction hash, (b) recorded evaluations in knowledge/records/, and
(c) git history (for sealing). One record file per run means parallel
contributors never edit the same file.

States
  HOLDS         latest strongest evaluation holds
  REFUTED       fails and has never held (a negative result: knowledge, kept)
  BROKEN        held before, fails now (a regression someone must explain)
  INCONCLUSIVE  the interval straddles the margin (not a negative result!)
  STALE         holds, but a premise it depends on is broken/refuted/retired
  UNTESTED      registered, never evaluated
  ERROR         the check itself crashed
  RETIRED       withdrawn with a reason; kept forever
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
from typing import Any, Dict, List, Optional, Sequence

from .claims import KNOWLEDGE, SCHEME, Claim, Evaluation, canonical, git, sha

RECORDS_DIR = KNOWLEDGE / "records"
QUESTIONS_DIR = KNOWLEDGE / "questions"
BAD_PREMISE = {"BROKEN", "REFUTED", "RETIRED", "ERROR", "STALE", "MISSING"}


# ----------------------------------------------------------------------------- records

def environment() -> Dict[str, str]:
    return {"python": platform.python_version(), "implementation": platform.python_implementation(),
            "platform": platform.platform(), "host": sha(platform.node(), 8)}


def contributor(explicit: Optional[str] = None) -> str:
    if explicit:
        return explicit
    name = (git("config", "user.name") or "").strip()
    return name or "anonymous"


def write_record(evaluations: Sequence[Evaluation], mode: str, by: str, code: str) -> Path:
    if mode not in ("full", "heldout"):
        raise ValueError("only full or held-out evaluations are recorded (quick runs are drafts)")
    RECORDS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    env = environment()
    env_id = sha(canonical(env), 12)
    head = (git("rev-parse", "HEAD") or "").strip() or None
    dirty = bool((git("status", "--porcelain", "--", "mind", "knowledge/claims",
                      "experiments/instruments") or "").strip())
    payload = {"schema": SCHEME, "recorded_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "by": by,
               "environment": env, "environment_id": env_id,
               "git": {"head": head, "dirty_sources": dirty}, "code": code, "mode": mode,
               "evaluations": {e.claim: e.to_dict() for e in evaluations}}
    stem = f"{now.strftime('%Y-%m-%dT%H-%M-%SZ')}-{env_id[:8]}-{mode}"
    path = RECORDS_DIR / f"{stem}.json"
    i = 1
    while path.exists():
        path = RECORDS_DIR / f"{stem}-{i}.json"
        i += 1
    path.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_records() -> List[Dict[str, Any]]:
    out = []
    for path in sorted(RECORDS_DIR.glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        rec["_path"] = str(path.relative_to(KNOWLEDGE.parent))
        out.append(rec)
    out.sort(key=lambda r: (r["recorded_at"], r["_path"]))
    return out


# ----------------------------------------------------------------------------- assessment

@dataclass
class ClaimState:
    claim: Claim
    state: str
    rung: int
    level: str
    seal: Optional[str]
    latest: Optional[Dict[str, Any]] = None
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    rivals_not_beaten: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    current_code: bool = False


def ladder(claim: Claim) -> tuple:
    """The evidence rungs that apply to this claim. Deterministic checks (no seeds)
    have nothing to seal, so they skip PREREGISTERED."""
    rungs = claim.ladder
    if not getattr(claim.test, "seeds", 0):
        rungs = tuple(r for r in rungs if r != "PREREGISTERED")
    return rungs


def _evidence(claim: Claim, records: List[Dict[str, Any]], live: Dict[str, Evaluation],
              code: str, live_mode: str) -> List[Dict[str, Any]]:
    """Evaluations of THIS prediction. Each record is matched under the hashing scheme it was
    written with, so records made before a scheme change still count when the prediction
    itself is unchanged."""
    hashes = {scheme: claim.prediction_hash(scheme) for scheme in range(1, SCHEME + 1)}
    ev = []
    for rec in records:
        e = rec["evaluations"].get(claim.id)
        if e and e["prediction_hash"] == hashes.get(rec.get("schema", 1)):
            ev.append({**e, "_by": rec["by"], "_env": rec["environment_id"], "_code": rec["code"],
                       "_at": rec["recorded_at"], "_mode": rec["mode"], "_record": rec["_path"],
                       "_schema": rec.get("schema", 1)})
    if claim.id in live and live[claim.id].prediction_hash == h:
        e = live[claim.id].to_dict()
        ev.append({**e, "_by": "live", "_env": "live", "_code": code, "_at": "9999-live",
                   "_mode": live_mode, "_record": None})
    return ev


def _strength(e: Dict[str, Any]) -> int:
    """quick drafts < dev-seed runs < sealed held-out runs. A failed preregistered
    confirmation can therefore never be overwritten by re-running dev seeds."""
    if e.get("_mode") == "quick":
        return 0
    return 2 if str(e.get("seeds", "")).startswith("heldout:") else 1


def _rivals_clean(e: Dict[str, Any]) -> bool:
    contenders = [r for r in e.get("rivals", {}).values() if not r["reference"]]
    return bool(contenders) and all(r["result"] == "BEATEN" for r in contenders)


def assess(claims: Dict[str, Claim], records: List[Dict[str, Any]],
           live: Optional[Dict[str, Evaluation]] = None, code: str = "",
           seals: Optional[Dict[str, Optional[str]]] = None,
           live_mode: str = "full") -> Dict[str, ClaimState]:
    live = live or {}
    seals = seals or {}
    out: Dict[str, ClaimState] = {}
    for cid, claim in claims.items():
        evidence = _evidence(claim, records, live, code, live_mode)
        seal = seals.get(cid)
        st = ClaimState(claim, "UNTESTED", 0, ladder(claim)[0], seal, evidence=evidence)
        if evidence:
            latest = max(evidence, key=lambda e: (_strength(e), e["_at"]))
            st.latest = latest
            st.current_code = latest["_code"] == code
            v = latest["verdict"]
            # BROKEN = a regression on IDENTICAL inputs (same seed set: same label AND same hash,
            # since held-out seeds derive from both). Holding on dev seeds but failing on sealed
            # held-out seeds is not a regression: the prediction did not generalise.
            held_same = any(e["verdict"] == "HOLDS" and e["seeds"] == latest["seeds"] and _strength(e) >= 1
                            and e["prediction_hash"] == latest["prediction_hash"]
                            for e in evidence if e is not latest)
            st.state = {"HOLDS": "HOLDS", "INCONCLUSIVE": "INCONCLUSIVE", "ERROR": "ERROR"}.get(
                v, "BROKEN" if held_same else "REFUTED")
            if v == "FAILS" and not held_same and any(e["verdict"] == "HOLDS" for e in evidence):
                st.notes.append("held on dev seeds but failed on sealed held-out seeds: did not generalise")
            st.rivals_not_beaten = sorted(n for n, r in latest.get("rivals", {}).items()
                                          if not r["reference"] and r["result"] != "BEATEN")
        if claim.retired:
            st.state = "RETIRED"
            st.notes.append(f"retired: {claim.retired}")
        st.rung = _rung(claim, evidence, seal) if st.state == "HOLDS" else 0
        st.level = ladder(claim)[st.rung]
        first = _first_heldout(evidence, seal)
        if first is not None and not _confirmed(claim, first):
            st.notes.append(f"failed its first sealed confirmation ({first['_at'][:10]}: {first['verdict']}); "
                            f"later re-runs cannot earn PREREGISTERED")
        amended = _amendments(claim, records)
        if amended:
            st.notes.append(f"prediction amended: {amended} earlier evaluation(s) of {claim.id} were of a "
                            f"different prediction")
        if seal is None and claim.path and "PREREGISTERED" in ladder(claim):
            st.notes.append("unsealed: commit the claim file to enable held-out evaluation")
        out[cid] = st
    _propagate_staleness(claims, out)
    return out


def _needs_rival(claim: Claim) -> bool:
    # The rival rung applies only to claims asserting a mechanism's superiority (`about`
    # non-empty); a directional finding such as "memory degrades calibration" has no rival.
    return claim.kind == "effect" and bool(claim.about)


def _first_heldout(evidence: List[Dict[str, Any]], seal: Optional[str]) -> Optional[Dict[str, Any]]:
    """The first RECORDED evaluation on this claim's sealed seeds. Preregistration is
    decided by it alone: once held-out seeds have been seen, re-running them (after a code
    change, say) proves nothing about prediction (v2 review, finding 3)."""
    if not seal:
        return None
    sealed = [e for e in evidence if e["_record"] and e["seeds"] == f"heldout:{seal}"]
    return min(sealed, key=lambda e: (e["_at"], e["_record"])) if sealed else None


def _confirmed(claim: Claim, e: Dict[str, Any]) -> bool:
    return e["verdict"] == "HOLDS" and e["robust"] and (not _needs_rival(claim) or _rivals_clean(e))


def _amendments(claim: Claim, records: List[Dict[str, Any]]) -> int:
    """Evaluations recorded for this id under a DIFFERENT prediction (same scheme)."""
    n = 0
    for rec in records:
        e = rec["evaluations"].get(claim.id)
        if e and e["prediction_hash"] != claim.prediction_hash(rec.get("schema", 1)):
            n += 1
    return n


def _rung(claim: Claim, evidence: List[Dict[str, Any]], seal: Optional[str]) -> int:
    holds = [e for e in evidence if e["verdict"] == "HOLDS"]
    robust = [e for e in holds if e["robust"]]
    met = {"PROPOSED": True, "OBSERVED": bool(holds), "ROBUST": bool(robust)}
    needs_rival = _needs_rival(claim)
    met["RIVAL-TESTED"] = any(_rivals_clean(e) for e in robust) if needs_rival else bool(robust)
    first = _first_heldout(evidence, seal)
    met["PREREGISTERED"] = first is not None and _confirmed(claim, first)
    recorded = [e for e in robust if e["_record"]]
    met["REPLICATED"] = (len({e["_by"] for e in recorded}) >= 2
                         and len({e["_env"] for e in recorded}) >= 2)
    rung = 0
    for i, name in enumerate(ladder(claim)):
        if not met[name]:
            break
        rung = i
    return rung


def _propagate_staleness(claims: Dict[str, Claim], states: Dict[str, ClaimState]) -> None:
    resolving: set = set()
    done: Dict[str, str] = {}

    def visit(cid: str) -> str:
        if cid in done:
            return done[cid]
        if cid not in states:
            return "MISSING"
        st = states[cid]
        if cid in resolving:
            if "dependency cycle" not in st.notes:
                st.notes.append("dependency cycle")
            return "ERROR"
        resolving.add(cid)
        for dep in st.claim.depends_on:
            dep_state = visit(dep)
            if dep_state in BAD_PREMISE and st.state in ("HOLDS", "INCONCLUSIVE", "UNTESTED"):
                st.notes.append(f"premise {dep} is {dep_state}")
                st.state = "STALE"
            elif dep_state not in ("HOLDS",) and dep_state not in BAD_PREMISE:
                note = f"premise {dep} not yet established ({dep_state})"
                if note not in st.notes:
                    st.notes.append(note)
        resolving.discard(cid)
        done[cid] = st.state
        return st.state

    for cid in sorted(claims):
        visit(cid)


# ----------------------------------------------------------------------------- questions

@dataclass
class Question:
    id: str
    title: str
    status: str
    next: str
    path: str
    body: str


def load_questions() -> Dict[str, Question]:
    out: Dict[str, Question] = {}
    for path in sorted(QUESTIONS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta: Dict[str, str] = {}
        body = text
        if text.startswith("---\n"):
            head, _, body = text[4:].partition("\n---\n")
            for line in head.splitlines():
                key, _, value = line.partition(":")
                meta[key.strip()] = value.strip()
        qid = meta.get("id", path.stem)
        out[qid] = Question(qid, meta.get("title", qid), meta.get("status", "open"),
                            meta.get("next", ""), str(path.relative_to(KNOWLEDGE.parent)), body.strip())
    return out


# ----------------------------------------------------------------------------- frontier

KIND_ORDER = ("repair", "rejustify", "sharpen", "rival", "evaluate", "question", "promote", "confirm",
              "refresh", "replicate")


def frontier(states: Dict[str, ClaimState], questions: Dict[str, Question]) -> List[Dict[str, str]]:
    """Ranked list of the most valuable next contributions, derived from the knowledge itself."""
    items: List[Dict[str, str]] = []
    grouped: Dict[str, List[str]] = {"confirm": [], "replicate": [], "refresh": []}

    def add(priority: int, kind: str, target: str, action: str) -> None:
        items.append({"priority": str(priority), "kind": kind, "target": target, "action": action})

    for cid, st in sorted(states.items()):
        c = st.claim
        if st.state == "BROKEN":
            add(0, "repair", cid, f"{cid} held before and fails now on the same seeds: find the change that broke "
                                  f"it, fix it, or retire the claim with a reason")
        elif st.state == "ERROR":
            add(0, "repair", cid, f"{cid}'s check crashed: {(st.latest or {}).get('error')}")
        elif st.state == "STALE":
            add(1, "rejustify", cid, f"{cid} rests on a failed premise ({'; '.join(st.notes)}): re-derive it "
                                     f"independently or retire it")
        elif st.state == "INCONCLUSIVE":
            add(2, "sharpen", cid, f"{cid} ({c.title}) is inconclusive: the interval straddles its margin. Register "
                                   f"a sharper successor claim (more seeds, a cleaner world) — never edit {cid}'s "
                                   f"prediction to fit")
        elif st.state == "UNTESTED":
            add(2, "evaluate", cid, f"{cid}: run `python -m mind check {cid} --record`")
        elif st.state == "HOLDS":
            rungs = ladder(c)
            nxt = rungs[st.rung + 1] if st.rung + 1 < len(rungs) else None
            if st.rivals_not_beaten:
                add(2, "rival", cid, f"{cid}: rival(s) {', '.join(st.rivals_not_beaten)} match the mechanism. Beat "
                                     f"them with a better organ, or register that the simpler rival suffices")
            elif nxt == "ROBUST":
                add(4, "promote", cid, f"{cid}: run at full strength `python -m mind check {cid} --record`")
            elif nxt == "RIVAL-TESTED":
                add(3, "rival", cid, f"{cid}: no non-reference rival in the zoo challenges {', '.join(c.about)} in "
                                     f"{getattr(c.test, 'world', 'this world')}; contribute one to mind/rivals")
            elif nxt == "PREREGISTERED":
                grouped["confirm"].append(cid)
            elif nxt == "REPLICATED":
                grouped["replicate"].append(cid)
            if not st.current_code and st.latest and st.latest.get("_record"):
                grouped["refresh"].append(cid)
    asked = {st.claim.question for st in states.values() if st.claim.question}
    for qid, q in sorted(questions.items()):
        if q.status != "open":
            continue
        if qid not in asked:
            add(3, "question", qid, f"{qid} — {q.title} No claim yet. {q.next or 'Write the first falsifiable claim.'}")
        elif q.next:
            add(4, "question", qid, f"{qid} — {q.title} {q.next}")
    if grouped["refresh"]:
        add(4, "refresh", "+".join(grouped["refresh"]),
            f"evidence for {', '.join(grouped['refresh'])} predates the current code; re-run `python -m mind check --record`")
    if grouped["confirm"]:
        add(4, "confirm", "+".join(grouped["confirm"]),
            f"{', '.join(grouped['confirm'])}: commit, then confirm on sealed seeds with "
            f"`python -m mind check --heldout --record`")
    if grouped["replicate"]:
        add(5, "replicate", "+".join(grouped["replicate"]),
            f"{len(grouped['replicate'])} claims await independent replication: on a fresh clone, as a different "
            f"contributor, run `python -m mind check --record --by <you>` and `--heldout --record --by <you>`")
    items.sort(key=lambda x: (int(x["priority"]), KIND_ORDER.index(x["kind"]), x["target"]))
    return items
