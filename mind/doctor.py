"""Repository integrity: mechanical enforcement of the program's epistemic rules.

  * claims are never deleted, only retired (negative results cannot be buried)
  * L3 / phenomenal-experience claims are not an admissible empirical scope
  * premises exist and form no cycle (no circular self-justification, Anjo I5)
  * every test names a real world, variant, metric and arm
  * pinned source snapshots are byte-unchanged
  * relative links in the living docs resolve
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import re
from typing import Dict, List, Set, Tuple

from .claims import CLAIMS_DIR, KINDS, ROOT, SCOPES, Check, Compare, Threshold, git, load_claims
from .knowledge import load_questions, load_records

PINNED = {
    "sources/anjo/2026-10-02-persistent-mind-spec.md": "0ef98f0511d7eb235626e020f719e17082633c7b",
    "sources/anjo/2026-10-09-vera-research-monograph.md": "4168c120a729b468c624bb2d58d1baa081d991fc",
}
LIVING_DOCS = ("README.md", "GO.md", "AGENTS.md", "CONTRIBUTING.md", "STATUS.md")
LINK = re.compile(r"\]\(([^)]+)\)")


def _blob(content: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


def _check_arm(arm: str) -> None:
    if arm.startswith("rival:"):
        from .rivals import RIVALS
        if arm[6:] not in RIVALS:
            raise ValueError(f"unknown rival {arm}")
    else:
        from .kernel import Config
        Config.parse(arm)


def doctor() -> Tuple[List[str], List[str]]:
    from .organs import ORGANS
    from .rivals import RIVALS
    from .worlds import WORLDS
    problems: List[str] = []
    warnings: List[str] = []
    mechanisms = set(ORGANS) | {"workspace"}
    try:
        claims = load_claims()
    except Exception as exc:
        return [f"claims failed to load: {exc}"], warnings
    questions = load_questions()

    for cid, c in sorted(claims.items()):
        where = f"{cid} ({c.path})"
        if not Path(c.path).name.startswith(cid + "_"):
            problems.append(f"{where}: file name must start with '{cid}_'")
        if c.kind not in KINDS:
            problems.append(f"{where}: kind {c.kind!r} not in {KINDS}")
        if c.scope not in SCOPES:
            problems.append(f"{where}: scope {c.scope!r} not admissible "
                            f"(phenomenal/L3 claims cannot be settled by these instruments)")
        for dep in c.depends_on:
            if dep not in claims:
                problems.append(f"{where}: premise {dep} does not exist")
            if dep == cid:
                problems.append(f"{where}: a claim cannot be its own premise")
        for parent in c.extends:
            if parent not in claims and not (ROOT / parent).exists():
                problems.append(f"{where}: lineage {parent!r} is neither a claim nor a repo path")
        if c.question and c.question not in questions:
            problems.append(f"{where}: question {c.question} has no file in knowledge/questions/")
        for m in c.about:
            if m not in mechanisms:
                problems.append(f"{where}: about {m!r} is not a known mechanism {sorted(mechanisms)}")
        if c.kind == "effect" and not c.about and isinstance(c.test, Compare):
            warnings.append(f"{where}: effect claim with empty `about` skips the rival panel; "
                            f"fine for harm/side-effect findings, not for superiority claims")
        t = c.test
        try:
            if isinstance(t, (Compare, Threshold)):
                if t.world not in WORLDS:
                    raise ValueError(f"unknown world {t.world!r}")
                world = WORLDS[t.world]
                if t.variant not in world.variants:
                    raise ValueError(f"unknown variant {t.variant!r}")
                base = t.metric.split("@")[0]
                if base not in world.metrics and base not in ("reward", "brier"):
                    raise ValueError(f"{t.world} has no metric {base!r}")
                for arm in ([t.a, t.b] if isinstance(t, Compare) else [t.arm]):
                    _check_arm(arm)
                if isinstance(t, Compare) and t.direction not in (">", "<", "~"):
                    raise ValueError(f"direction {t.direction!r}")
                if t.seeds < 8 and c.kind != "fact":
                    warnings.append(f"{where}: {t.seeds} seeds is too few for a robust claim (use >= 12)")
                if c.kind == "equivalence" and getattr(t, "direction", "~") != "~":
                    raise ValueError("an equivalence claim must use direction '~'")
            elif not isinstance(t, Check):
                raise ValueError("test must be Compare, Threshold or Check")
        except Exception as exc:
            problems.append(f"{where}: invalid test: {exc}")

    # cycles
    state: Dict[str, int] = {}

    def visit(cid: str, stack: List[str]) -> None:
        if state.get(cid) == 1:
            problems.append("dependency cycle: " + " -> ".join(stack + [cid]))
            return
        if state.get(cid) == 2 or cid not in claims:
            return
        state[cid] = 1
        for dep in claims[cid].depends_on:
            visit(dep, stack + [cid])
        state[cid] = 2

    for cid in sorted(claims):
        visit(cid, [])

    # claims are retired, never deleted
    deleted = git("log", "--diff-filter=D", "--name-only", "--format=", "--", "knowledge/claims") or ""
    present_ids = set(claims)
    for line in sorted(set(deleted.split())):
        stem = Path(line).name.split("_", 1)[0]
        if line.endswith(".py") and stem not in present_ids:
            problems.append(f"claim file {line} was deleted from history; restore it with retired='reason'")

    # records reference real claims
    for rec in load_records():
        for cid in rec["evaluations"]:
            if cid not in claims:
                warnings.append(f"{rec['_path']}: evaluation for unknown claim {cid}")

    # registries
    for name, cls in WORLDS.items():
        if not cls.heldout_variants:
            problems.append(f"world {name} declares no held-out variant")
    for name, rival in RIVALS.items():
        for m in rival.challenges:
            if m not in mechanisms:
                problems.append(f"rival {name} challenges unknown mechanism {m!r}")

    # pinned sources
    for rel, expected in PINNED.items():
        path = ROOT / rel
        if not path.is_file():
            problems.append(f"pinned source missing: {rel}")
        elif _blob(path.read_bytes()) != expected:
            problems.append(f"pinned source changed: {rel}")

    # living docs and their links
    docs = [ROOT / d for d in LIVING_DOCS] + sorted((ROOT / "docs").glob("*.md")) + sorted(
        (ROOT / "knowledge" / "questions").glob("*.md"))
    for path in docs:
        if not path.exists():
            problems.append(f"missing living doc: {path.relative_to(ROOT)}")
            continue
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            dest = target.split("#", 1)[0]
            if not dest or dest.startswith(("http:", "https:", "mailto:")):
                continue
            if not (path.parent / dest).exists():
                problems.append(f"broken link in {path.relative_to(ROOT)}: {target}")
    return problems, warnings
