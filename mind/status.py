"""Render STATUS.md: the live, generated state of MIND's knowledge.

Replaces the hand-maintained research-state handoff. Because it is computed
from claims, records and git, it cannot drift, and merge conflicts in it are
resolved by regenerating it.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import json
import sys
from typing import Any, Dict, List, Optional

from .claims import KNOWLEDGE, Check, Compare, Threshold, git
from .knowledge import ClaimState, Question

STATE_ORDER = ("BROKEN", "ERROR", "STALE", "HOLDS", "INCONCLUSIVE", "REFUTED", "UNTESTED", "RETIRED")
STATE_MARK = {"HOLDS": "✅", "REFUTED": "❌", "BROKEN": "💥", "STALE": "⚠️", "INCONCLUSIVE": "❔",
              "UNTESTED": "⬜", "ERROR": "🛑", "RETIRED": "🗄️"}
ATLAS_PATH = KNOWLEDGE / "atlas.json"


def _fmt(x: Optional[float]) -> str:
    if x is None:
        return "–"
    return f"{x:+.3f}" if abs(x) < 100 else f"{x:+.1f}"


def estimate_text(st: ClaimState) -> str:
    e = st.latest
    if not e:
        return "–"
    if e.get("verdict") == "ERROR":
        return f"error: {e.get('error')}"
    est = e.get("estimate", {})
    test = st.claim.test
    if isinstance(test, Compare) and "diff" in est:
        return (f"Δ {_fmt(est['diff'])} [{_fmt(est['lo'])}, {_fmt(est['hi'])}] "
                f"({est['a']:.3f} vs {est['b']:.3f}, n={est['n']})")
    if isinstance(test, Threshold) and "mean" in est:
        return f"{est['mean']:.3f} [{est['lo']:.3f}, {est['hi']:.3f}] {test.op} {test.value} (n={est['n']})"
    return str(est.get("summary", "see record"))


def seeds_text(st: ClaimState) -> str:
    e = st.latest
    if not e:
        return ""
    return "held-out" if str(e.get("seeds", "")).startswith("heldout:") else "dev"


def mermaid(states: Dict[str, ClaimState], questions: Dict[str, Question]) -> str:
    lines = ["graph LR"]
    style = {"HOLDS": "fill:#d4f4dd,stroke:#2e7d32", "REFUTED": "fill:#fde0dc,stroke:#c62828",
             "BROKEN": "fill:#ffcdd2,stroke:#b71c1c", "STALE": "fill:#fff3cd,stroke:#b8860b",
             "INCONCLUSIVE": "fill:#e8eaf6,stroke:#3949ab", "UNTESTED": "fill:#f5f5f5,stroke:#9e9e9e",
             "ERROR": "fill:#ffcdd2,stroke:#b71c1c", "RETIRED": "fill:#eeeeee,stroke:#757575"}
    for qid, q in sorted(questions.items()):
        lines.append(f'  {qid}(["{qid}"])')
    for cid, st in sorted(states.items()):
        safe = cid.replace("-", "_")
        lines.append(f'  {safe}["{cid}<br/>{st.level if st.state == "HOLDS" else st.state}"]')
        lines.append(f"  style {safe} {style.get(st.state, '')}")
        if st.claim.question and st.claim.question in questions:
            lines.append(f"  {safe} -.-> {st.claim.question}")
    for cid, st in sorted(states.items()):
        safe = cid.replace("-", "_")
        for dep in st.claim.depends_on:
            lines.append(f"  {dep.replace('-', '_')} --> {safe}")
        for parent in st.claim.extends:
            if parent in states:
                lines.append(f"  {parent.replace('-', '_')} -.->|extends| {safe}")
    return "\n".join(lines)


def atlas_section() -> List[str]:
    if not ATLAS_PATH.exists():
        return ["_No atlas computed yet: run `python -m mind atlas --write`._", ""]
    data = json.loads(ATLAS_PATH.read_text(encoding="utf-8"))
    s = data["summary"]
    out = [f"Computed on {len(data['seeds'])} dev seeds at code `{data.get('code', '?')}`. "
           f"**Causal density {s['causal_density']:.2f}** ({s['reliable']}/{s['pairs']} organ×metric pairs "
           f"with a reliable effect; {s['helps']} help, {s['hurts']} hurt). "
           f"**Cross-function effects: {s['cross_function']}**. "
           f"**Degenerate (mutually redundant) organ pairs: {len(s['degenerate_pairs'])}.**", ""]
    worlds: Dict[str, List[str]] = {}
    for c in data["cells"]:
        worlds.setdefault(c["world"], [])
        if c["metric"] not in worlds[c["world"]]:
            worlds[c["world"]].append(c["metric"])
    header = ["organ"] + [f"{w}.{m}" for w, ms in worlds.items() for m in ms]
    out.append("| " + " | ".join(header) + " |")
    out.append("|" + "---|" * len(header))
    for organ in data["organs"]:
        row = [organ]
        for w, ms in worlds.items():
            for m in ms:
                c = next(c for c in data["cells"] if c["organ"] == organ and c["world"] == w and c["metric"] == m)
                mark = "🟢" if c["helps"] else "🔴" if c["hurts"] else "·"
                home = "ᴴ" if c["home"] else ""
                row.append(f"{mark}{home} {c['effect']:+.2f}")
        out.append("| " + " | ".join(row) + " |")
    out += ["", "🟢 organ reliably helps (95% CI of the sign-normalised lesion effect > 0), 🔴 reliably hurts, "
            "· no reliable effect; ᴴ = a home competency the organ was designed for. Off-home 🟢 cells are "
            "cross-function effects.", ""]
    if s["cross_function_cells"]:
        out.append("Cross-function: " + ", ".join(f"`{x}`" for x in s["cross_function_cells"]))
    if s["degenerate_pairs"]:
        out.append("")
        out.append("Degenerate pairs: " + ", ".join(f"`{x}`" for x in s["degenerate_pairs"]))
    out.append("")
    return out


def registry_section() -> List[str]:
    from .organs import ORGANS
    from .rivals import RIVALS
    from .worlds import WORLDS
    out = ["### Organs", "", "| organ | home competencies | what it does |", "|---|---|---|"]
    for name, cls in ORGANS.items():
        doc = (sys.modules[cls.__module__].__doc__ or "").strip().splitlines()[0]
        out.append(f"| `{name}` | {', '.join(cls.home)} | {doc} |")
    out += ["", "### Worlds", "", "| world | variants (held-out) | metrics → competency |", "|---|---|---|"]
    for name, cls in WORLDS.items():
        doc = ", ".join(f"{m}→{c}" for m, (c, _) in cls.metrics.items())
        held = ", ".join(v + ("*" if v in cls.heldout_variants else "") for v in cls.variants)
        out.append(f"| `{name}` | {held} | {doc} |")
    out += ["", "### Rival zoo", "", "| rival | challenges | reference? | what it is |", "|---|---|---|---|"]
    for name, r in RIVALS.items():
        out.append(f"| `rival:{name}` | {', '.join(r.challenges)} | {'ceiling' if r.reference else 'must be beaten'} | {r.doc} |")
    out.append("")
    return out


def render(states: Dict[str, ClaimState], questions: Dict[str, Question], items: List[Dict[str, str]],
           code: str) -> str:
    head = (git("rev-parse", "--short", "HEAD") or "?").strip()
    counts = Counter(st.state for st in states.values())
    levels = Counter(st.level for st in states.values() if st.state == "HOLDS")
    out = ["# MIND — live knowledge status", "",
           "> **Generated** by `python -m mind status --write` from `knowledge/claims/`, `knowledge/records/` "
           "and git history. Do not edit by hand; if it conflicts in a merge, regenerate it.", "",
           f"Code fingerprint `{code}` · git `{head}` · generated "
           f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", "",
           "**Target: functional consciousness — NOT achieved.** Every claim below concerns a small "
           "learning organism in toy worlds, at instrument, behavioural (L1) or causal-organisation (L2) "
           "scope. Phenomenal experience (L3) is not an admissible empirical scope here.", "",
           "## At a glance", "",
           "| state | claims |", "|---|---|"]
    for state in STATE_ORDER:
        if counts.get(state):
            extra = ""
            if state == "HOLDS":
                extra = " (" + ", ".join(f"{lv} {n}" for lv, n in sorted(levels.items())) + ")"
            out.append(f"| {STATE_MARK[state]} {state} | {counts[state]}{extra} |")
    out += ["", "Evidence ladder (computed, never asserted): PROPOSED → OBSERVED → ROBUST → RIVAL-TESTED "
            "(effects only) → PREREGISTERED (commit-sealed held-out seeds) → REPLICATED (second contributor "
            "and environment). See [docs/CLAIMS.md](docs/CLAIMS.md).", "",
            "## Frontier — what to build next", "",
            "Derived from the knowledge itself (broken first, then stale, then promotions and open questions). "
            "Pick one, check open PRs for overlap, contribute. See [GO.md](GO.md).", ""]
    for i, item in enumerate(items[:20], 1):
        out.append(f"{i}. **[{item['kind']}]** {item['action']}")
    if len(items) > 20:
        out.append(f"\n…and {len(items) - 20} more: `python -m mind status --frontier`.")
    out += ["", "## Claims", "",
            "| claim | statement | kind · scope | state | level | evidence (latest strongest) | rivals not beaten | premises |",
            "|---|---|---|---|---|---|---|---|"]
    for cid, st in sorted(states.items(), key=lambda kv: (STATE_ORDER.index(kv[1].state), kv[0])):
        c = st.claim
        rivals = ", ".join(st.rivals_not_beaten) or ("–" if c.kind == "effect" else "n/a")
        prem = ", ".join(c.depends_on) or "–"
        notes = ("<br/>_" + "; ".join(n for n in st.notes if not n.startswith("unsealed")) + "_") if any(
            not n.startswith("unsealed") for n in st.notes) else ""
        level = st.level if st.state == "HOLDS" else "–"
        seeds = seeds_text(st)
        out.append(f"| [{cid}]({c.path}) | **{c.title}**{notes} | {c.kind} · {c.scope} | "
                   f"{STATE_MARK[st.state]} {st.state} | {level} | {estimate_text(st)}"
                   f"{' · ' + seeds if seeds else ''} | {rivals} | {prem} |")
    out += ["", "## Questions", "", "| question | status | claims bearing on it |", "|---|---|---|"]
    for qid, q in sorted(questions.items()):
        bearing = [f"{cid} {STATE_MARK[st.state]}" for cid, st in sorted(states.items()) if st.claim.question == qid]
        out.append(f"| [{qid}]({q.path}) {q.title} | {q.status} | {', '.join(bearing) or '—'} |")
    out += ["", "## Knowledge graph", "",
            "Solid arrows: premise → dependent (a failed premise turns dependents STALE). Dotted: lineage "
            "(`extends`) and the question a claim bears on.", "", "```mermaid", mermaid(states, questions),
            "```", "", "## Integration atlas", ""]
    out += atlas_section()
    out += ["## What you can build on", ""]
    out += registry_section()
    return "\n".join(out) + "\n"
