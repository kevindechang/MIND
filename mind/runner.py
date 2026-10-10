"""Run any arm (organism configuration or rival) in any world, for many seeds.

An arm is a string: an organism configuration such as "organism -memory", or
"rival:<name>". One seed = one independent lifetime: world seed and organism
seed are both derived from it, and paired arms share it (paired design).

Metrics per run, each in three windows: `m` (late: second half of the
lifetime, i.e. after learning), `m@all`, `m@early` (first quarter).
Generic metrics for every world: `reward` (per episode) and `brier`
(confidence vs public outcome; an agent with no forecast scores as 0.5).
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from .kernel import Organism
from .ledger import Ledger, MemoryLedger
from .worlds import WORLDS, make_world

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / ".mind-cache"


# Files that can change a simulated result or a verdict. Tooling (cli, status,
# doctor, knowledge) is deliberately excluded: editing it must not make evidence stale.
RESULT_CODE = ("mind/kernel.py", "mind/ledger.py", "mind/runner.py", "mind/stats.py", "mind/legacy.py",
               "mind/claims.py", "mind/atlas.py", "mind/worker.py", "mind/organs/*.py", "mind/worlds/*.py",
               "mind/rivals/*.py", "experiments/instruments/e001_*.py")


def code_fingerprint() -> str:
    """Hash of everything that can change a run's result."""
    h = hashlib.sha256()
    paths = sorted({p for pattern in RESULT_CODE for p in ROOT.glob(pattern)})
    for path in paths:
        h.update(str(path.relative_to(ROOT)).encode())
        h.update(path.read_bytes())
    return h.hexdigest()[:16]


def make_agent(arm: str, world: str, variant: str, seed: int, ledger: Optional[Ledger] = None):
    if arm.startswith("rival:"):
        from .rivals import RIVALS
        name = arm[len("rival:"):]
        if name not in RIVALS:
            raise ValueError(f"unknown rival {name!r}; choose {sorted(RIVALS)}")
        rival = RIVALS[name]
        if rival.worlds and world not in rival.worlds:
            raise ValueError(f"rival {name!r} does not apply to world {world!r}")
        if rival.config is not None:
            return Organism(rival.config, seed, ledger)
        return rival.factory(world, variant, seed)
    return Organism(arm, seed, ledger)


def run(arm: str, world: str, seed: int, episodes: Optional[int] = None, variant: str = "dev",
        ledger: Optional[Ledger] = None, kill_at: Sequence[int] = (), trace: bool = False) -> Dict:
    """One lifetime. `kill_at` lists ticks after which the organism object is
    destroyed and rebuilt from its ledger alone (in-process death)."""
    episodes = WORLDS[world].default_episodes if episodes is None else episodes
    if kill_at and ledger is None:
        ledger = MemoryLedger()
    agent = make_agent(arm, world, variant, seed, ledger)
    if kill_at and not isinstance(agent, Organism):
        raise ValueError(f"{arm} is not an organism: only organisms can die and be reborn from a ledger")
    late = [when for when, _ in agent.cfg.schedule if when >= episodes] if isinstance(agent, Organism) else []
    if late:
        raise ValueError(f"{arm}: a lesion scheduled at episode {late[0]} never happens in a {episodes}-episode life")
    env = make_world(world, seed, variant)
    kills = sorted(set(kill_at))
    rows: List[Dict[str, float]] = []
    actions: List[str] = []
    tick = 0
    # Shadow forecaster scored on the agent's OWN events: a per-action success table
    # (the transcript rivals' rule). Forecasters must be compared on a common event
    # stream; comparing each agent on its own action mix confounds calibration with
    # behaviour (v2 review, finding 7). calib_gain = brier_table - brier.
    from .rivals import SuccessTable
    table = SuccessTable()
    for _ in range(episodes):
        obs = env.reset()
        reward, outcome, boundary = 0.0, None, True
        total, sq, sqt, n_fc = 0.0, 0.0, 0.0, 0
        while True:
            d = agent.step(obs, reward, outcome, boundary, env.legal())
            if trace:
                actions.append(d.action)
            s = env.step(d.action)
            total += s.reward
            if s.outcome is not None:
                conf = 0.5 if d.confidence is None else d.confidence
                sq += (conf - s.outcome) ** 2
                sqt += (table.forecast(d.action) - s.outcome) ** 2
                table.update(d.action, s.outcome)
                n_fc += 1
            if kills and tick == kills[0]:
                kills.pop(0)
                agent = Organism.restore(ledger)  # death: nothing survives but the ledger
            tick += 1
            if s.done:
                agent.end_episode(s.reward, s.outcome)
                break
            obs, reward, outcome, boundary = s.obs, s.reward, s.outcome, False
        row = env.summary()
        row["reward"] = total
        row["_sq"], row["_sqt"], row["_n"] = sq, sqt, float(n_fc)
        rows.append(row)
    result = {"arm": arm, "world": world, "variant": variant, "seed": seed, "episodes": episodes,
              "metrics": aggregate(rows)}
    if isinstance(agent, Organism) and agent.ledger is not None:
        result["head"] = agent.ledger.head
    if trace:
        result["trace"] = actions
    return result


def aggregate(rows: List[Dict[str, float]]) -> Dict[str, float]:
    n = len(rows)
    windows = {"": rows[n // 2:], "@all": rows, "@early": rows[: max(1, n // 4)]}
    out: Dict[str, float] = {}
    keys = sorted(k for k in rows[0] if not k.startswith("_"))
    for suffix, part in windows.items():
        for k in keys:
            out[k + suffix] = sum(r[k] for r in part) / len(part)
        count = sum(r["_n"] for r in part)
        out["brier" + suffix] = sum(r["_sq"] for r in part) / count if count else 0.25
        out["brier_table" + suffix] = sum(r["_sqt"] for r in part) / count if count else 0.25
        out["calib_gain" + suffix] = out["brier_table" + suffix] - out["brier" + suffix]
    return out


# ---------------------------------------------------------------------------- sweeps

def _task(args: Tuple[str, str, str, int, int]) -> Dict:
    arm, world, variant, seed, episodes = args
    return run(arm, world, seed, episodes, variant)


class Lab:
    """Runs (arm, world, variant, seed, episodes) tasks in parallel, with a
    content-addressed disk cache keyed by the code fingerprint."""

    def __init__(self, jobs: Optional[int] = None, cache: bool = True):
        self.jobs = jobs if jobs is not None else (os.cpu_count() or 1)
        self.fingerprint = code_fingerprint()
        self.memo: Dict[str, Dict] = {}
        self.cache_path = CACHE_DIR / f"runs-{self.fingerprint}.jsonl" if cache else None
        if self.cache_path is not None and self.cache_path.exists():
            for line in self.cache_path.read_text().splitlines():
                rec = json.loads(line)
                self.memo[rec["key"]] = rec["result"]
        self.executed = 0

    @staticmethod
    def key(arm: str, world: str, variant: str, seed: int, episodes: int) -> str:
        if arm.startswith("organism"):
            from .kernel import Config
            arm = Config.parse(arm).text      # '-a -b' and '-b -a' are one experiment
        return json.dumps([arm, world, variant, seed, episodes])

    def runs(self, tasks: Iterable[Tuple[str, str, str, int, int]]) -> List[Dict]:
        tasks = list(tasks)
        todo = []
        for t in tasks:
            k = self.key(*t)
            if k not in self.memo and t not in todo:
                todo.append(t)
        if todo:
            if self.jobs > 1 and len(todo) > 1:
                with ProcessPoolExecutor(max_workers=self.jobs) as pool:
                    results = list(pool.map(_task, todo, chunksize=1))
            else:
                results = [_task(t) for t in todo]
            self.executed += len(todo)
            lines = []
            for t, r in zip(todo, results):
                self.memo[self.key(*t)] = r
                lines.append(json.dumps({"key": self.key(*t), "result": r}))
            if self.cache_path is not None:
                self.cache_path.parent.mkdir(exist_ok=True)
                with self.cache_path.open("a") as fh:
                    fh.write("\n".join(lines) + "\n")
        return [self.memo[self.key(*t)] for t in tasks]

    def metric(self, arm: str, world: str, variant: str, seeds: Sequence[int], episodes: int,
               metric: str) -> List[float]:
        res = self.runs([(arm, world, variant, s, episodes) for s in seeds])
        return [r["metrics"][metric] for r in res]
