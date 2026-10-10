#!/usr/bin/env python3
"""Offline MIND agent-onboarding consistency checks, NOT a science experiment."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CORE = (
    "GO.md", "AGENTS.md", "CURRENT.md", "TASKS.md", "RUNBOOK.md",
    "CONTRIBUTING.md", "README.md", "research-state.md",
    "research-quality-gate.md", "sources/README.md",
    "sources/anjo/2026-10-02-persistent-mind-spec.md",
    "sources/anjo/2026-10-09-vera-research-monograph.md",
    "CLAUDE.md", ".cursor/rules/mind.mdc", ".github/copilot-instructions.md",
)
DOCS = ("GO.md", "AGENTS.md", "CURRENT.md", "TASKS.md", "CONTRIBUTING.md",
        "README.md", "RUNBOOK.md", "sources/README.md")
EXPECTED_BLOBS = {
    "sources/anjo/2026-10-02-persistent-mind-spec.md": "0ef98f0511d7eb235626e020f719e17082633c7b",
    "sources/anjo/2026-10-09-vera-research-monograph.md": "4168c120a729b468c624bb2d58d1baa081d991fc",
}
LINK = re.compile(r"\]\(([^)]+)\)")


def blob_id(content: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


def main() -> int:
    errors = []
    for name in CORE:
        if not (ROOT / name).is_file():
            errors.append(f"missing: {name}")

    for name in DOCS:
        path = ROOT / name
        if not path.exists():
            continue
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            dest = target.split("#", 1)[0]
            if not dest or dest.startswith(("http:", "https:", "mailto:", "/")):
                continue
            if not (path.parent / dest).exists():
                errors.append(f"broken link in {name}: {target}")
    for name, expected in EXPECTED_BLOBS.items():
        path = ROOT / name
        if path.is_file() and (actual := blob_id(path.read_bytes())) != expected:
            errors.append(f"source blob changed: {name}: {actual} != {expected}")

    state = (ROOT / "research-state.md")
    if state.is_file():
        text = state.read_text(encoding="utf-8")
        for required in ("repository: kevindechang/MIND", "parent_initiative: Anjo",
                         "next_substantive_workstream: W2", "agent_entrypoint: GO.md"):
            if required not in text:
                errors.append(f"state missing: {required}")
    try:
        p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        head = p.stdout.strip() if p.returncode == 0 else "NOT_A_GIT_CHECKOUT"
    except OSError:
        head = "GIT_UNAVAILABLE"

    result = {"status": "FAIL" if errors else "PASS", "head": head,
              "core_files": len(CORE), "links_scanned": list(DOCS),
              "source_snapshots_checked": len(EXPECTED_BLOBS),
              "errors": errors,
              "scope": "agent onboarding consistency ONLY; not agent cognition or E001 efficacy"}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
