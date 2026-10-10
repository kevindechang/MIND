"""Command line: python -m mind <command>.

  status   [--write] [--frontier]         computed state of all knowledge
  check    [IDS] [--quick|--heldout] [--record] [--by NAME] [-j N]
                                          evaluate claims; exit 1 on BROKEN/ERROR
  run      ARM WORLD [--variant V] [--seeds N] [--episodes E] [--metrics a,b]
                                          ad-hoc experiment (exploration, not evidence)
  atlas    [--seeds N] [--write]          lesion map of the organism across all worlds
  doctor                                  repository integrity checks
  new      ID TITLE                       scaffold a claim file
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import time
from typing import Dict, List, Optional

from . import stats
from .claims import (CLAIMS_DIR, KINDS, KNOWLEDGE, ROOT, SCOPES, Check, Compare, Threshold, dev_seeds,
                     evaluate, git, heldout_seeds, load_claims, rival_panel, seal_commit, QUICK_SEEDS)
from .knowledge import (assess, contributor, frontier, load_questions, load_records, write_record)
from .runner import Lab, code_fingerprint
from .worlds import WORLDS

STATUS_PATH = ROOT / "STATUS.md"


def _seals(claims) -> Dict[str, Optional[str]]:
    return {cid: seal_commit(c) for cid, c in claims.items()}


def _tasks(claim, mode: str, seal: Optional[str]) -> List[tuple]:
    test = claim.test
    if isinstance(test, Check):
        return []
    n = test.seeds
    if mode == "heldout":
        seeds = heldout_seeds(claim, seal, n)
    else:
        seeds = dev_seeds(min(n, QUICK_SEEDS) if mode == "quick" else n)
    eps = WORLDS[test.world].default_episodes if test.episodes is None else test.episodes
    arms = [test.a, test.b] if isinstance(test, Compare) else [test.arm]
    if mode != "quick":
        arms += [f"rival:{r.name}" for r in rival_panel(claim)]
    return [(arm, test.world, test.variant, s, eps) for arm in arms for s in seeds]


def cmd_check(args) -> int:
    claims = load_claims()
    selected = {cid: c for cid, c in claims.items() if not args.ids or cid in args.ids}
    missing = set(args.ids or []) - set(claims)
    if missing:
        print(f"unknown claim id(s): {', '.join(sorted(missing))}", file=sys.stderr)
        return 2
    mode = "heldout" if args.heldout else "quick" if args.quick else "full"
    if mode == "heldout" and not args.record:
        # an unrecorded held-out run burns the sealed seeds without leaving evidence
        print("held-out runs are always recorded (--record implied)")
        args.record = True
    if args.record and mode == "quick":
        print("quick runs are drafts and are never recorded; drop --quick", file=sys.stderr)
        return 2
    seals = _seals(selected)
    runnable = {}
    for cid, c in selected.items():
        if c.retired:
            continue
        if mode == "heldout":
            if c.kind == "fact" or getattr(c.test, "seeds", 0) == 0:
                print(f"  {cid}: skipped (deterministic claim; held-out seeds do not apply)")
                continue
            if seals[cid] is None:
                print(f"  {cid}: skipped (unsealed: commit the claim file first)")
                continue
        runnable[cid] = c
    lab = Lab(jobs=args.jobs, cache=not args.no_cache)
    start = time.time()
    tasks = [t for c in runnable.values() for t in _tasks(c, mode, seals.get(c.id))]
    if tasks:
        print(f"running {len(set(tasks))} lifetimes ({lab.jobs} workers, cache {'off' if args.no_cache else 'on'})...",
              flush=True)
        lab.runs(tasks)
    evaluations = {}
    for cid, c in sorted(runnable.items()):
        ev = evaluate(c, lab, mode, seals.get(cid))
        evaluations[cid] = ev
        rivals = " ".join(f"{n}:{'✓' if r['result'] == 'BEATEN' else '✗'}{'(ref)' if r['reference'] else ''}"
                          for n, r in ev.rivals.items())
        est = ev.estimate
        summary = (f"Δ {est['diff']:+.3f} [{est['lo']:+.3f},{est['hi']:+.3f}]" if "diff" in est else
                   f"{est['mean']:.3f} [{est['lo']:.3f},{est['hi']:.3f}]" if "mean" in est else
                   str(est.get("summary", ev.error or "")))
        print(f"  {cid:6s} {ev.verdict:12s} {summary}  {rivals}")
    print(f"done in {time.time() - start:.1f}s; {lab.executed} new lifetimes simulated")
    code = code_fingerprint()
    if args.record and evaluations:
        path = write_record(list(evaluations.values()), mode, contributor(args.by), code)
        print(f"recorded {path.relative_to(ROOT)}")
    states = assess(claims, load_records(), evaluations if not args.record else {}, code, _seals(claims),
                    live_mode=mode)
    bad = [cid for cid in evaluations if states[cid].state in ("BROKEN", "ERROR")]
    for cid in evaluations:
        st = states[cid]
        print(f"  → {cid}: {st.state}{' · ' + st.level if st.state == 'HOLDS' else ''}"
              f"{' · ' + '; '.join(st.notes) if st.notes else ''}")
    if bad:
        print(f"REGRESSION: {', '.join(bad)}", file=sys.stderr)
        return 1
    return 0


def cmd_status(args) -> int:
    claims = load_claims()
    states = assess(claims, load_records(), {}, code_fingerprint(), _seals(claims))
    questions = load_questions()
    items = frontier(states, questions)
    if args.frontier:
        for i, item in enumerate(items, 1):
            print(f"{i:3d}. [{item['kind']}] {item['action']}")
        return 0
    if args.write:
        from .status import render
        STATUS_PATH.write_text(render(states, questions, items, code_fingerprint()), encoding="utf-8")
        print(f"wrote {STATUS_PATH.relative_to(ROOT)}")
    for cid, st in sorted(states.items()):
        print(f"{cid:6s} {st.state:12s} {st.level if st.state == 'HOLDS' else '':14s} {st.claim.title}")
    print(f"\n{len(items)} frontier items; top: {items[0]['action'] if items else 'none'}")
    return 0


def cmd_run(args) -> int:
    lab = Lab(jobs=args.jobs, cache=not args.no_cache)
    metrics = args.metrics.split(",") if args.metrics else list(WORLDS[args.world].metrics) + ["reward"]
    eps = args.episodes or WORLDS[args.world].default_episodes
    res = lab.runs([(args.arm, args.world, args.variant, s, eps) for s in range(args.seeds)])
    print(f"{args.arm} in {args.world}/{args.variant}, {args.seeds} dev seeds × {eps} episodes "
          f"(exploration only: not evidence until stated as a claim)")
    for m in metrics:
        if m not in res[0]["metrics"]:
            continue
        mean, lo, hi = stats.bootstrap_ci([r["metrics"][m] for r in res])
        print(f"  {m:16s} {mean:9.4f}  [{lo:.4f}, {hi:.4f}]")
    return 0


def cmd_atlas(args) -> int:
    from .atlas import atlas
    lab = Lab(jobs=args.jobs, cache=not args.no_cache)
    data = atlas(lab, dev_seeds(args.seeds))
    data["code"] = code_fingerprint()
    s = data["summary"]
    print(f"causal density {s['causal_density']:.2f} ({s['reliable']}/{s['pairs']}), "
          f"cross-function {s['cross_function']}: {s['cross_function_cells']}")
    print(f"degenerate pairs: {s['degenerate_pairs']}")
    if args.write:
        path = KNOWLEDGE / "atlas.json"
        path.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


def cmd_doctor(args) -> int:
    from .doctor import doctor
    problems, warnings = doctor()
    for w in warnings:
        print(f"warning: {w}")
    for p in problems:
        print(f"PROBLEM: {p}")
    print("doctor: " + ("PASS" if not problems else f"{len(problems)} problem(s)"))
    return 1 if problems else 0


TEMPLATE = '''"""{title}

Why this matters / what it builds on: <one paragraph>.
Strongest simpler rival: <which rival in mind/rivals could explain the result>.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="{cid}",
    title="{title}",
    statement="<one falsifiable sentence; the test below is what is actually checked>",
    kind="effect",            # effect | equivalence | threshold | invariant | fact
    scope="L2",               # instrument | L1 | L2   (L3 is not an empirical scope)
    question=None,            # e.g. "H003"
    about=(),                 # mechanisms concerned, e.g. ("workspace",): selects the rival panel
    depends_on=(),            # premise claim ids
    extends=(),               # lineage: claim ids or paths of prior work this builds on
    test=Compare(world="vigil", a="organism", b="organism -memory", metric="kept",
                 direction=">", margin=0.05, seeds=16),
    by="{by}",
    created="{date}",
)
'''


def cmd_new(args) -> int:
    if not re.fullmatch(r"[A-Z][0-9]{2,4}", args.id):
        print("claim ids look like C123 (letter + 2-4 digits)", file=sys.stderr)
        return 2
    slug = re.sub(r"[^a-z0-9]+", "_", args.title.lower()).strip("_")[:40]
    path = CLAIMS_DIR / f"{args.id}_{slug}.py"
    if any(p.name.startswith(args.id + "_") for p in CLAIMS_DIR.glob("*.py")):
        print(f"{args.id} already exists", file=sys.stderr)
        return 2
    path.write_text(TEMPLATE.format(cid=args.id, title=args.title.replace('"', "'"),
                                    by=contributor(None), date=time.strftime("%Y-%m-%d")), encoding="utf-8")
    print(f"created {path.relative_to(ROOT)}")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="python -m mind", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-j", "--jobs", type=int, default=None, help="parallel workers (default: all CPUs)")
    common.add_argument("--no-cache", action="store_true", help="ignore the .mind-cache run cache")

    s = sub.add_parser("status", help="computed state of all knowledge")
    s.add_argument("--write", action="store_true", help="regenerate STATUS.md")
    s.add_argument("--frontier", action="store_true", help="print the full frontier")
    s.set_defaults(fn=cmd_status)

    c = sub.add_parser("check", parents=[common], help="evaluate claims")
    c.add_argument("ids", nargs="*")
    g = c.add_mutually_exclusive_group()
    g.add_argument("--quick", action="store_true", help=f"{QUICK_SEEDS} dev seeds; a draft, never recorded")
    g.add_argument("--heldout", action="store_true", help="commit-sealed held-out seeds (preregistration; always recorded)")
    c.add_argument("--record", action="store_true", help="write a record under knowledge/records/")
    c.add_argument("--by", default=None, help="contributor label for the record (default: git user.name)")
    c.set_defaults(fn=cmd_check)

    r = sub.add_parser("run", parents=[common], help="ad-hoc experiment")
    r.add_argument("arm")
    r.add_argument("world", choices=sorted(WORLDS))
    r.add_argument("--variant", default="dev")
    r.add_argument("--seeds", type=int, default=8)
    r.add_argument("--episodes", type=int, default=None)
    r.add_argument("--metrics", default=None)
    r.set_defaults(fn=cmd_run)

    a = sub.add_parser("atlas", parents=[common], help="lesion map across all worlds")
    a.add_argument("--seeds", type=int, default=12)
    a.add_argument("--write", action="store_true")
    a.set_defaults(fn=cmd_atlas)

    d = sub.add_parser("doctor", help="repository integrity checks")
    d.set_defaults(fn=cmd_doctor)

    n = sub.add_parser("new", help="scaffold a claim")
    n.add_argument("id")
    n.add_argument("title")
    n.set_defaults(fn=cmd_new)

    args = p.parse_args(argv)
    return args.fn(args)
