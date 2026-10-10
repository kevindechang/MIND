"""Executable claims: the unit of knowledge that compounds.

A claim is one Python file in knowledge/claims/ defining `CLAIM = Claim(...)`.
Its *prediction* (kind, scope and test specification) is hashed; prose may
change freely, the prediction may not change without becoming a new
registration. Claims cite premises (`depends_on`): when a premise breaks,
every dependent claim turns STALE automatically.

Seeds
  dev      seeds 0..n-1, for exploration and debugging
  heldout  n seeds derived from the git commit that first registered the
           current prediction. That commit's hash cannot be known before the
           prediction is committed, so held-out data cannot be tuned against:
           preregistration is enforced by construction, not by promise.
"""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field, replace
import hashlib
import importlib.util
import inspect
import linecache
import random
import subprocess
import time
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from . import stats
from .ledger import canonical

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
CLAIMS_DIR = KNOWLEDGE / "claims"

# Prediction-hash scheme. 1: test spec only (records written before the v2 review);
# 2: Check claims also hash their file's code. Records store the scheme they were made under.
SCHEME = 2
KINDS = ("effect", "equivalence", "threshold", "invariant", "fact")
# Empirical claims live at the instrument, behavioural (L1) or causal-organisation (L2)
# level. L3 (phenomenal experience) is deliberately NOT an admissible scope.
SCOPES = ("instrument", "L1", "L2")
LADDER = {
    "effect": ("PROPOSED", "OBSERVED", "ROBUST", "RIVAL-TESTED", "PREREGISTERED", "REPLICATED"),
    "equivalence": ("PROPOSED", "OBSERVED", "ROBUST", "PREREGISTERED", "REPLICATED"),
    "threshold": ("PROPOSED", "OBSERVED", "ROBUST", "PREREGISTERED", "REPLICATED"),
    "invariant": ("PROPOSED", "OBSERVED", "ROBUST", "PREREGISTERED", "REPLICATED"),
    "fact": ("PROPOSED", "OBSERVED", "ROBUST", "REPLICATED"),
}
GENERIC_METRICS = {"reward": ("control", "higher"), "brier": ("metacognition", "lower"),
                   # same-event-stream calibration (v2 review, finding 7): a per-action success table
                   # scored on the agent's OWN actions and outcomes, and its gap to the agent's forecasts
                   "brier_table": ("metacognition", "lower"), "calib_gain": ("metacognition", "higher")}


def sha(text: str, n: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


# ----------------------------------------------------------------------------- tests

@dataclass(frozen=True)
class Compare:
    """Paired comparison of mean(metric[a] - metric[b]) over independent lifetimes."""
    world: str
    a: str
    b: str
    metric: str
    direction: str          # '>', '<' or '~' (equivalence within margin)
    margin: float = 0.0
    seeds: int = 16
    episodes: Optional[int] = None
    variant: str = "dev"

    def spec(self) -> Dict[str, Any]:
        return {"type": "compare", **asdict(self)}


@dataclass(frozen=True)
class Threshold:
    """The mean of a metric for one arm clears a bound."""
    world: str
    arm: str
    metric: str
    op: str                 # '>=' or '<='
    value: float
    seeds: int = 16
    episodes: Optional[int] = None
    variant: str = "dev"

    def spec(self) -> Dict[str, Any]:
        return {"type": "threshold", **asdict(self)}


@dataclass(frozen=True)
class Check:
    """Custom check: fn(ctx) -> dict(verdict=HOLDS|FAILS|INCONCLUSIVE, robust=bool, ...).
    The function's source text is part of the prediction hash."""
    fn: Callable[["Context"], Dict[str, Any]]
    seeds: int = 0           # >0 if the check consumes seeds (then held-out applies)

    def spec(self) -> Dict[str, Any]:
        return {"type": "check", "name": self.fn.__name__, "seeds": self.seeds,
                "source": sha(inspect.getsource(self.fn))}


Test = Union[Compare, Threshold, Check]


@dataclass(frozen=True)
class Claim:
    id: str
    title: str
    statement: str
    kind: str
    scope: str
    test: Test
    question: Optional[str] = None
    about: Tuple[str, ...] = ()         # mechanisms concerned; selects the rival panel
    depends_on: Tuple[str, ...] = ()    # premises: failure propagates as STALE
    extends: Tuple[str, ...] = ()       # lineage: the prior work this builds on
    sources: Tuple[str, ...] = ()       # literature IDs (motivation, not evidence)
    by: str = "unknown"
    created: str = ""
    rationale: str = ""
    retired: Optional[str] = None       # reason, if withdrawn (never delete a claim)
    path: str = ""
    module_hash: str = ""               # hash of the claim file's code minus prose (set by the loader)

    def prediction(self, scheme: int = SCHEME) -> Dict[str, Any]:
        p = {"id": self.id, "kind": self.kind, "scope": self.scope, "test": self.test.spec()}
        if scheme >= 2 and isinstance(self.test, Check):
            # helpers and constants a check relies on are part of what is predicted (v2 review, finding 4)
            p["module"] = self.module_hash
        return p

    def prediction_hash(self, scheme: int = SCHEME) -> str:
        return sha(canonical(self.prediction(scheme)))

    @property
    def ladder(self) -> Tuple[str, ...]:
        rungs = LADDER[self.kind]
        if self.kind == "effect" and not self.about:   # no mechanism superiority asserted
            rungs = tuple(r for r in rungs if r != "RIVAL-TESTED")
        return rungs


# ----------------------------------------------------------------------------- loading

def code_without_prose(text: str) -> str:
    """The claim file's source minus its module docstring, its `CLAIM = Claim(...)`
    block (prose and declarative spec, hashed separately) and blank lines. Raw text,
    so the hash does not depend on the Python version."""
    tree = ast.parse(text)
    drop = set()
    body = tree.body
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
            and isinstance(body[0].value.value, str):
        drop.update(range(body[0].lineno, body[0].end_lineno + 1))
    for node in body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CLAIM" for t in node.targets):
            drop.update(range(node.lineno, node.end_lineno + 1))
    lines = [line.rstrip() for i, line in enumerate(text.splitlines(), 1) if i not in drop]
    return "\n".join(line for line in lines if line.strip())


def _exec_claim(text: str, filename: str) -> Claim:
    # Register the source so inspect.getsource works for Check functions,
    # including historical versions read out of git.
    linecache.cache[filename] = (len(text), None, text.splitlines(True), filename)
    namespace: Dict[str, Any] = {"__name__": "mind_claim", "__file__": filename}
    exec(compile(text, filename, "exec"), namespace)
    claim = namespace.get("CLAIM")
    if not isinstance(claim, Claim):
        raise ValueError(f"{filename}: no CLAIM = Claim(...) defined")
    return replace(claim, module_hash=sha(code_without_prose(text)))


def load_claims(directory: Path = CLAIMS_DIR, root: Path = ROOT) -> Dict[str, Claim]:
    claims: Dict[str, Claim] = {}
    for path in sorted(directory.glob("*.py")):
        if path.name.startswith("_"):
            continue
        rel = str(path.relative_to(root))
        claim = replace(_exec_claim(path.read_text(encoding="utf-8"), str(path)), path=rel)
        if claim.id in claims:
            raise ValueError(f"duplicate claim id {claim.id} in {rel} and {claims[claim.id].path}")
        claims[claim.id] = claim
    return claims


# ----------------------------------------------------------------------------- git sealing

def git(*args: str, root: Path = ROOT) -> Optional[str]:
    try:
        p = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return p.stdout if p.returncode == 0 else None


def seal_commit(claim: Claim, root: Path = ROOT) -> Optional[str]:
    """Earliest commit containing a file for this claim id that carries the CURRENT
    prediction. Searched by id (file names must start with '<id>_'), so renaming a
    claim file does not move its seal or re-roll its held-out seeds."""
    folder = str(Path(claim.path).parent) if claim.path else "knowledge/claims"
    log = git("log", "--format=%x01%H", "--name-only", "--",
              f":(glob){folder}/{claim.id}_*.py", root=root)
    if not log:
        return None
    target = claim.prediction_hash()
    entries = []
    for block in log.split("\x01")[1:]:
        lines = [x for x in block.splitlines() if x.strip()]
        entries.append((lines[0], lines[1:]))
    for commit, paths in reversed(entries):          # oldest first
        for path in paths:
            text = git("show", f"{commit}:{path}", root=root)
            if text is None:
                continue
            try:
                old = _exec_claim(text, f"<git {commit[:12]}:{path}>")
            except Exception:
                continue
            if old.id == claim.id and old.prediction_hash() == target:
                return commit
    return None


def dev_seeds(n: int) -> List[int]:
    return list(range(n))


def heldout_seeds(claim: Claim, seal: str, n: int) -> List[int]:
    rng = random.Random(hashlib.sha256(f"{seal}|{claim.id}|{claim.prediction_hash()}".encode()).digest())
    return sorted(rng.sample(range(10_000, 10_000_000), n))


# ----------------------------------------------------------------------------- evaluation

@dataclass
class Context:
    """What a Check function receives."""
    lab: Any
    seeds: List[int]
    mode: str               # 'quick' | 'full' | 'heldout'
    claim: Claim


@dataclass
class Evaluation:
    claim: str
    prediction_hash: str
    verdict: str            # HOLDS | FAILS | INCONCLUSIVE | ERROR
    robust: bool
    seeds: str              # 'dev' or 'heldout:<seal commit>'
    estimate: Dict[str, Any] = field(default_factory=dict)
    rivals: Dict[str, Any] = field(default_factory=dict)
    seconds: float = 0.0
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def metric_orientation(world: str, metric: str) -> str:
    from .worlds import WORLDS
    base = metric.split("@")[0]
    spec = WORLDS[world].metrics.get(base) or GENERIC_METRICS.get(base)
    if spec is None:
        raise ValueError(f"{world} has no metric {base!r}")
    return spec[1]


def rival_panel(claim: Claim) -> List[Any]:
    """Standing rivals that challenge any mechanism this claim is about."""
    from .rivals import RIVALS
    test = claim.test
    if claim.kind != "effect" or not isinstance(test, Compare) or test.a.startswith("rival:"):
        return []
    out = []
    for rival in RIVALS.values():
        if not set(rival.challenges) & set(claim.about):
            continue
        if rival.worlds and test.world not in rival.worlds:
            continue
        if f"rival:{rival.name}" in (test.a, test.b) or rival.config in (test.a, test.b):
            continue
        out.append(rival)
    return out


def _direct_rival(arm: str) -> Optional[Any]:
    from .rivals import RIVALS
    if arm.startswith("rival:"):
        return RIVALS.get(arm[len("rival:"):])
    for rival in RIVALS.values():
        if rival.config is not None and rival.config == arm:
            return rival
    return None


QUICK_SEEDS = 4


def evaluate(claim: Claim, lab: Any, mode: str = "full", seal: Optional[str] = None) -> Evaluation:
    """Evaluate one claim. mode: 'quick' (few dev seeds, never ROBUST), 'full'
    (declared dev seeds) or 'heldout' (declared seeds sealed by `seal`)."""
    start = time.time()
    test = claim.test
    n = getattr(test, "seeds", 0)
    if mode == "heldout":
        if seal is None:
            raise ValueError("held-out evaluation requires a sealing commit")
        seeds, seed_label = heldout_seeds(claim, seal, n) if n else [], f"heldout:{seal}"
    else:
        seeds = dev_seeds(min(n, QUICK_SEEDS) if mode == "quick" else n)
        seed_label = "dev"
    ev = Evaluation(claim.id, claim.prediction_hash(), stats.INCONCLUSIVE, False, seed_label)
    try:
        if isinstance(test, Compare):
            eps = test.episodes
            from .worlds import WORLDS
            eps = WORLDS[test.world].default_episodes if eps is None else eps
            a = lab.metric(test.a, test.world, test.variant, seeds, eps, test.metric)
            b = lab.metric(test.b, test.world, test.variant, seeds, eps, test.metric)
            ev.estimate = stats.compare(a, b, test.direction, test.margin, seed=claim.id)
            ev.verdict = ev.estimate["verdict"]
            direct = _direct_rival(test.b)
            if direct is not None and claim.kind == "effect" and ev.verdict == stats.HOLDS:
                # beating a standing rival head-on is itself a rival test
                sign = 1.0 if metric_orientation(test.world, test.metric) == "higher" else -1.0
                lo, hi = sorted((sign * ev.estimate["lo"], sign * ev.estimate["hi"]))
                # a claim can hold because the RIVAL is better; only a reliable advantage beats it
                ev.rivals[direct.name] = {"reference": direct.reference, "advantage": sign * ev.estimate["diff"],
                                          "lo": lo, "hi": hi, "result": "BEATEN" if lo > 0 else "NOT_BEATEN"}
            if mode != "quick" and ev.verdict == stats.HOLDS:
                better = metric_orientation(test.world, test.metric)
                for rival in rival_panel(claim):
                    arm = f"rival:{rival.name}"
                    r = lab.metric(arm, test.world, test.variant, seeds, eps, test.metric)
                    diffs = [(x - y) if better == "higher" else (y - x) for x, y in zip(a, r)]
                    m, lo, hi = stats.bootstrap_ci(diffs, seed=claim.id + arm)
                    ev.rivals[rival.name] = {"reference": rival.reference, "advantage": m, "lo": lo,
                                             "hi": hi, "result": "BEATEN" if lo > 0 else "NOT_BEATEN"}
        elif isinstance(test, Threshold):
            from .worlds import WORLDS
            eps = WORLDS[test.world].default_episodes if test.episodes is None else test.episodes
            xs = lab.metric(test.arm, test.world, test.variant, seeds, eps, test.metric)
            ev.estimate = stats.threshold(xs, test.op, test.value, seed=claim.id)
            ev.verdict = ev.estimate["verdict"]
        elif isinstance(test, Check):
            result = test.fn(Context(lab, seeds, mode, claim))
            ev.verdict = result.pop("verdict")
            robust = bool(result.pop("robust", True))
            ev.estimate = result
            ev.robust = robust and mode != "quick" and ev.verdict == stats.HOLDS
        else:
            raise TypeError(f"unknown test type {type(test).__name__}")
        if not isinstance(test, Check):
            ev.robust = mode != "quick" and ev.verdict == stats.HOLDS
    except Exception as exc:  # a broken check is itself a finding: report, don't crash
        ev.verdict, ev.robust = "ERROR", False
        ev.error = "".join(traceback.format_exception_only(type(exc), exc)).strip()
        ev.estimate = {"traceback": traceback.format_exc(limit=6)}
    ev.seconds = round(time.time() - start, 3)
    return ev
