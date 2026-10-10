"""Records, computed evidence levels, staleness propagation, questions and the frontier.

Nothing here is asserted by hand. A claim's state and level are computed from
(a) its prediction hash, (b) recorded evaluations in knowledge/records/, and
(c) git history (for sealing). One record file per run means parallel
contributors never edit the same file.

States
  HOLDS         the latest evaluation on every seed set holds
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

from .claims import KNOWLEDGE, SCHEME, Claim, Compare, Evaluation, canonical, git, sha

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
    rivals_unrun: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    current_code: bool = False
    suspended: Optional[str] = None   # the level its evidence earned, while CURRENT_CODE_UNVERIFIED caps it


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
    if claim.id in live and live[claim.id].prediction_hash == hashes[SCHEME]:
        e = live[claim.id].to_dict()
        ev.append({**e, "_by": "live", "_env": "live", "_code": code, "_at": "9999-live",
                   "_mode": live_mode, "_record": None})
    return ev


def _strength(e: Dict[str, Any]) -> int:
    """quick drafts < dev-seed runs < sealed held-out runs."""
    if e.get("_mode") == "quick":
        return 0
    return 2 if str(e.get("seeds", "")).startswith("heldout:") else 1


_SEVERITY = {"ERROR": 0, "FAILS": 1, "INCONCLUSIVE": 2, "HOLDS": 3}


def _seed_set(e: Dict[str, Any]) -> str:
    # quick drafts run a prefix of the dev seeds under the same label, so they are a set of their own
    return "quick" if e.get("_mode") == "quick" else str(e["seeds"])


def _decisive(evidence: List[Dict[str, Any]]) -> tuple:
    """The evaluation that decides the state, and the latest evaluation on each seed set.

    Each seed set (dev, the sealed held-out seeds) speaks through its latest run, and the most
    conservative of those decides. So a failure on any seed set is never hidden by older or
    stronger success on another: a dev regression in `mind check` is not masked by a held-out
    record, and re-running dev seeds cannot overwrite a failed sealed confirmation. Quick drafts
    count only when nothing else exists."""
    pool = [e for e in evidence if _strength(e) >= 1] or evidence
    heads: Dict[str, Dict[str, Any]] = {}
    for e in sorted(pool, key=lambda e: e["_at"]):
        heads[_seed_set(e)] = e
    decisive = max(heads.values(), key=lambda e: (-_SEVERITY.get(e["verdict"], 0), _strength(e), e["_at"]))
    return decisive, [heads[k] for k in sorted(heads)]


def _seeds_name(label: str) -> str:
    return label[:15] if label.startswith("heldout:") else label


def _rivals_clean(e: Dict[str, Any]) -> bool:
    contenders = [r for r in e.get("rivals", {}).values() if not r["reference"]]
    return bool(contenders) and all(r["result"] == "BEATEN" for r in contenders)


def _contenders(claim: Claim) -> set:
    """The non-reference rivals that challenge this claim in today's zoo: its rival panel, plus a
    rival its own test names. A current evaluation must have run, and beaten, every one."""
    from .claims import _direct_rival, rival_panel
    names = {r.name for r in rival_panel(claim) if not r.reference}
    direct = _direct_rival(claim.test.b) if isinstance(claim.test, Compare) else None
    if direct is not None and not direct.reference:
        names.add(direct.name)
    return names


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
        heads: List[Dict[str, Any]] = []
        if evidence:
            latest, heads = _decisive(evidence)
            st.latest = latest
            # current standing needs RECORDED evidence from the current result code on every seed set;
            # a live run can revoke standing (a regression) but never restore it
            recorded: Dict[str, Dict[str, Any]] = {}
            for e in sorted((e for e in evidence if e["_record"] and _strength(e) >= 1), key=lambda e: e["_at"]):
                recorded[_seed_set(e)] = e
            st.current_code = bool(recorded) and all(e["_code"] == code for e in recorded.values())
            v = latest["verdict"]
            if len({e["verdict"] for e in heads}) > 1:
                st.notes.append("mixed evidence: " + ", ".join(
                    f"{e['verdict']} on {_seeds_name(str(e['seeds']))}" for e in heads))
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
            # rival standing comes from the latest run on every seed set, against today's zoo
            st.rivals_not_beaten = sorted({n for e in heads for n, r in e.get("rivals", {}).items()
                                           if not r["reference"] and r["result"] != "BEATEN"})
            if v == "HOLDS" and _needs_rival(claim):
                st.rivals_unrun = sorted({n for e in heads for n in _contenders(claim) - set(e.get("rivals", {}))})
                if st.rivals_unrun:
                    st.notes.append(f"rival(s) {', '.join(st.rivals_unrun)} not yet run against its latest "
                                    f"evaluation: RIVAL-TESTED and above wait for a re-run")
        if claim.retired:
            st.state = "RETIRED"
            st.notes.append(f"retired: {claim.retired}")
        st.rung = _rung(claim, evidence, seal, heads) if st.state == "HOLDS" else 0
        robust = ladder(claim).index("ROBUST")
        if st.rung > robust and not st.current_code:
            # Evidence from other result code says nothing certain about this code: RIVAL-TESTED and
            # above are suspended until re-recorded. The original sealed confirmation stays historical
            # fact; re-running exposed held-out seeds never counts as a new one (`_first_heldout`).
            st.suspended = ladder(claim)[st.rung]
            st.rung = robust
            st.notes.append(f"CURRENT_CODE_UNVERIFIED: its {st.suspended} standing rests on evidence recorded "
                            f"under other result code, so it is suspended at ROBUST until `python -m mind check "
                            f"--record` and `--heldout --record` re-record it on the current code")
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


def _rung(claim: Claim, evidence: List[Dict[str, Any]], seal: Optional[str],
          heads: Sequence[Dict[str, Any]] = ()) -> int:
    holds = [e for e in evidence if e["verdict"] == "HOLDS"]
    robust = [e for e in holds if e["robust"]]
    met = {"PROPOSED": True, "OBSERVED": bool(holds), "ROBUST": bool(robust)}
    if _needs_rival(claim):
        # Not "beat its rivals once": the latest run on every seed set must have beaten every rival
        # in today's zoo. A newer NOT_BEATEN, or a rival added since, revokes the rung (and, the
        # ladder being cumulative, everything above it) until a re-run earns it back.
        contenders = _contenders(claim)
        met["RIVAL-TESTED"] = bool(heads) and all(
            e["robust"] and _rivals_clean(e) and contenders <= set(e.get("rivals", {})) for e in heads)
    else:
        met["RIVAL-TESTED"] = bool(robust)
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
            spent = any(n.startswith("failed its first sealed confirmation") for n in st.notes)
            if spent:
                add(2, "sharpen", cid, f"{cid} ({c.title}) holds now but failed its first sealed confirmation, so its "
                                       f"held-out seeds are spent: register a successor claim (new id, fresh seeds) "
                                       f"to confirm it prospectively")
            if st.suspended:
                pass   # re-recording comes first: see the refresh item
            elif st.rivals_not_beaten or st.rivals_unrun:
                if st.rivals_not_beaten:
                    add(2, "rival", cid, f"{cid}: rival(s) {', '.join(st.rivals_not_beaten)} match the mechanism. "
                                         f"Beat them with a better organ, or register that the simpler rival suffices")
                if st.rivals_unrun:
                    add(2, "rival", cid, f"{cid}: rival(s) {', '.join(st.rivals_unrun)} joined the zoo after its latest "
                                         f"evaluation; re-run `python -m mind check {cid} --record` and `--heldout "
                                         f"--record` to test it against them")
            elif nxt == "ROBUST":
                add(4, "promote", cid, f"{cid}: run at full strength `python -m mind check {cid} --record`")
            elif nxt == "RIVAL-TESTED":
                add(3, "rival", cid, f"{cid}: no non-reference rival in the zoo challenges {', '.join(c.about)} in "
                                     f"{getattr(c.test, 'world', 'this world')}; contribute one to mind/rivals")
            elif nxt == "PREREGISTERED" and not spent:
                grouped["confirm"].append(cid)
            elif nxt == "REPLICATED":
                grouped["replicate"].append(cid)
            if st.suspended or (not st.current_code and st.latest and st.latest.get("_record")):
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
        suspended = [cid for cid in grouped["refresh"] if states[cid].suspended]
        add(1 if suspended else 4, "refresh", "+".join(grouped["refresh"]),
            f"CURRENT_CODE_UNVERIFIED: evidence for {', '.join(grouped['refresh'])} predates the current result "
            f"code" + (f", so the RIVAL-TESTED-or-higher standing of {', '.join(suspended)} is suspended"
                       if suspended else "") +
            "; re-run `python -m mind check --record`, and `--heldout --record` for claims with sealed seeds")
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
