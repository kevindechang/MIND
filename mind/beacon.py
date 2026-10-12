"""Held-out seeds from public randomness the registrant does not control (P001).

Commit-sealed seeds stop accidental tuning but not grinding: a commit's hash, and so
its held-out seeds, can be previewed before the commit is pushed. A beacon draw adds
randomness nobody can know at push time:

  push    the earliest entry in GitHub's repository activity log whose new tip contains
          the seal commit. GitHub's clock, not the registrant's, timestamps it.
  round   the first drand quicknet round published strictly after that push.
  seeds   heldout_seeds(claim, "<seal>+drand:<randomness>", n): the existing sealed-seed hash
          over an extended seal, so result code (mind/claims.py) is unchanged.

The receipt (push + round + randomness + signature) is stored in the record. Offline,
the doctor checks that the round follows from the push time and that randomness ==
sha256(signature). With `doctor --online` it also re-fetches the round from drand and
the push from GitHub. Not checked: the BLS signature itself (stdlib only), so online
verification trusts the drand HTTP relays.

Residual risk, by design visible rather than prevented: a registrant can push several
registrations and keep the luckiest. Every push is in the public activity log, and
successors carry new ids.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import re
import urllib.request
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

QUICKNET = {
    "hash": "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971",
    "genesis_time": 1692803367,
    "period": 3,
}
RELAYS = ("https://api.drand.sh", "https://drand.cloudflare.com", "https://api2.drand.sh")
GITHUB_API = "https://api.github.com"
NULL_SHA = "0" * 40
TIMEOUT = 20

Push = Dict[str, Any]
Receipt = Dict[str, Any]


# ----------------------------------------------------------------------------- drand

def round_time(r: int) -> int:
    return QUICKNET["genesis_time"] + (r - 1) * QUICKNET["period"]


def round_after(t: float) -> int:
    """The first round published strictly after unix time t."""
    elapsed = max(0.0, t - QUICKNET["genesis_time"])
    return int(elapsed // QUICKNET["period"]) + 2


def consistent(beacon: Dict[str, Any]) -> bool:
    """drand's randomness is sha256 of the round signature."""
    try:
        return hashlib.sha256(bytes.fromhex(beacon["signature"])).hexdigest() == beacon["randomness"]
    except (KeyError, TypeError, ValueError):
        return False


def _get_json(url: str, headers: Optional[Dict[str, str]] = None) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": "mind-beacon", **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_round(r: int) -> Dict[str, Any]:
    """Round r from the first relay that answers consistently."""
    errors = []
    for relay in RELAYS:
        try:
            data = _get_json(f"{relay}/{QUICKNET['hash']}/public/{r}")
        except Exception as exc:          # network errors differ per platform; try the next relay
            errors.append(f"{relay}: {exc}")
            continue
        if data.get("round") == r and consistent(data):
            return data
        errors.append(f"{relay}: inconsistent answer for round {r}")
    raise RuntimeError("no drand relay answered: " + "; ".join(errors))


# ----------------------------------------------------------------------------- GitHub push

def parse_time(stamp: str) -> float:
    return datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def first_push(seal: str, activity: Iterable[Dict[str, Any]],
               contains: Callable[[str, str], bool]) -> Optional[Push]:
    """The earliest activity whose new tip has `seal` in its history. `contains(seal, tip)`
    answers ancestry. No date filter: committer dates are the registrant's to forge."""
    entries = sorted((a for a in activity if a.get("after") and a["after"] != NULL_SHA),
                     key=lambda a: (a["timestamp"], a["id"]))
    for a in entries:
        if contains(seal, a["after"]):
            return {"time": a["timestamp"], "activity_id": a["id"], "ref": a.get("ref"), "after": a["after"]}
    return None


def list_activity(repo: str, token: Optional[str] = None) -> List[Dict[str, Any]]:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    out: List[Dict[str, Any]] = []
    url: Optional[str] = f"{GITHUB_API}/repos/{repo}/activity?per_page=100&direction=asc"
    while url:
        req = urllib.request.Request(url, headers={"User-Agent": "mind-beacon", **headers})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            out.extend(json.loads(resp.read().decode("utf-8")))
            nxt = re.search(r'<([^>]+)>;\s*rel="next"', resp.headers.get("Link", ""))
        url = nxt.group(1) if nxt else None
    return out


def repo_slug(remote_url: str) -> Optional[str]:
    m = re.search(r"github\.com[:/]([^/]+/[^/]+?)(?:\.git)?/?$", remote_url.strip())
    return m.group(1) if m else None


# ----------------------------------------------------------------------------- receipts

def draw(push: Push, fetch: Callable[[int], Dict[str, Any]] = fetch_round) -> Receipt:
    r = round_after(parse_time(push["time"]))
    b = fetch(r)
    return {"chain": QUICKNET["hash"], "round": r, "randomness": b["randomness"],
            "signature": b["signature"], "push": dict(push)}


def verify_offline(rec: Receipt) -> List[str]:
    problems = []
    if rec.get("chain") != QUICKNET["hash"]:
        problems.append(f"beacon chain {str(rec.get('chain'))[:12]} is not drand quicknet")
    if not consistent(rec):
        problems.append(f"beacon randomness for round {rec.get('round')} is not sha256(signature)")
    try:
        expected = round_after(parse_time(rec["push"]["time"]))
    except (KeyError, TypeError, ValueError):
        return problems + ["beacon receipt has no valid push time"]
    if rec.get("round") != expected:
        problems.append(f"beacon round {rec.get('round')} is not the first round after the push "
                        f"at {rec['push']['time']} (expected {expected})")
    return problems


def verify_online(rec: Receipt, seal: str, activity: Iterable[Dict[str, Any]],
                  contains: Callable[[str, str], bool],
                  fetch: Callable[[int], Dict[str, Any]] = fetch_round) -> List[str]:
    problems = []
    push = first_push(seal, activity, contains)
    if push is None:
        problems.append(f"GitHub activity shows no push containing seal {seal[:12]}")
    elif push["time"] != rec["push"].get("time"):
        problems.append(f"seal {seal[:12]} was first pushed at {push['time']}, "
                        f"not {rec['push'].get('time')} as the receipt says")
    live = fetch(rec["round"])
    if live.get("randomness") != rec.get("randomness"):
        problems.append(f"drand round {rec['round']} randomness differs from the receipt")
    return problems


def extended_seal(seal: str, rec: Optional[Receipt]) -> str:
    """What the sealed-seed hash consumes: the commit, plus the drawn randomness if any."""
    return f"{seal}+drand:{rec['randomness']}" if rec else seal


def label(seal: str, rec: Optional[Receipt]) -> str:
    return f"heldout:{extended_seal(seal, rec)}"


def parse_label(seeds: str) -> Tuple[Optional[str], Optional[str]]:
    """(seal commit, drawn randomness or None); (None, None) for dev seeds."""
    if not seeds.startswith("heldout:"):
        return None, None
    seal, _, randomness = seeds[len("heldout:"):].partition("+drand:")
    return seal, (randomness or None)


# ----------------------------------------------------------------------------- repository glue

def ancestry(git: Callable[..., Optional[str]], repo: str, token: Optional[str] = None) -> Callable[[str, str], bool]:
    """`contains(seal, tip)` from local history, falling back to GitHub's compare API for
    tips this clone never fetched (deleted branches, say)."""
    def contains(seal: str, tip: str) -> bool:
        if git("cat-file", "-e", f"{tip}^{{commit}}") is not None:
            return git("merge-base", "--is-ancestor", seal, tip) is not None
        headers = {"Accept": "application/vnd.github+json", **({"Authorization": f"Bearer {token}"} if token else {})}
        try:
            data = _get_json(f"{GITHUB_API}/repos/{repo}/compare/{seal}...{tip}", headers)
        except Exception:                 # unknown to GitHub too: it cannot contain the seal
            return False
        return data.get("status") in ("ahead", "identical")
    return contains


def locate(git: Callable[..., Optional[str]], token: Optional[str] = None) -> Tuple[str, Callable[[str, str], bool]]:
    slug = repo_slug(git("remote", "get-url", "origin") or "")
    if slug is None:
        raise RuntimeError("beacon draws need an 'origin' remote on GitHub")
    return slug, ancestry(git, slug, token)
