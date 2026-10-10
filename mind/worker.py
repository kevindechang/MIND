"""Real-process organism worker and a supervisor that SIGKILLs it (E100 Day 0, generalised).

Worker: `python -m mind.worker --ledger PATH [--config CFG --seed N]`.
Speaks JSON lines on stdin/stdout. A decision request carries only the current
observation -- never history, transcript or task -- so after a SIGKILL the new
process can know the past ONLY through the ledger file.

Exactly-once semantics (Anjo invariant I7): a step whose tick is already
committed returns the logged decision instead of acting twice, so the
supervisor may blindly resend after a crash.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
from typing import Dict, List, Sequence

from .kernel import Organism
from .ledger import SqliteLedger
from .worlds import make_world

ROOT = Path(__file__).resolve().parents[1]


def serve(ledger_path: Path, config: str, seed: int) -> None:
    ledger = SqliteLedger(ledger_path)
    org = Organism.restore(ledger) if len(ledger) else Organism(config, seed, ledger)
    ended_at = None
    for event in ledger:
        if event.kind == "end":
            ended_at = event.payload["t"]
    try:
        for line in sys.stdin:
            msg = json.loads(line)
            if msg["op"] == "step":
                if set(msg) != {"op", "t", "obs", "r", "o", "b", "a"}:
                    raise ValueError("a step may carry only the current observation")
                before = len(ledger)
                d = org.step_at(msg["t"], msg["obs"], msg["r"], msg["o"], msg["b"], msg["a"])
                # 'replayed' is MEASURED: the answer came from the ledger iff nothing was appended
                reply = {"t": msg["t"], "act": d.action, "conf": d.confidence, "replayed": len(ledger) == before}
            elif msg["op"] == "end":
                before = len(ledger)
                if ended_at != msg["t"]:          # idempotent: never end the same episode twice
                    org.end_episode(msg["r"], msg["o"])
                    ended_at = msg["t"]
                reply = {"ok": True, "replayed": len(ledger) == before}
            elif msg["op"] == "head":
                reply = {"head": ledger.head, "events": len(ledger), "pid": os.getpid()}
            else:
                raise ValueError(f"unknown op {msg['op']!r}")
            print(json.dumps(reply), flush=True)
    finally:
        ledger.close()


class WorkerProcess:
    def __init__(self, ledger_path: Path, config: str, seed: int):
        self.proc = subprocess.Popen(
            [sys.executable, "-u", "-m", "mind.worker", "--ledger", str(ledger_path),
             "--config", config, "--seed", str(seed)],
            cwd=str(ROOT), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, bufsize=1)

    def send(self, msg: Dict) -> None:
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

    def ask(self, msg: Dict) -> Dict:
        self.send(msg)
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError(f"worker died: {self.proc.stderr.read()}")
        return json.loads(line)

    def kill(self) -> int:
        os.kill(self.proc.pid, signal.SIGKILL)   # real death, not a graceful exit
        code = self.proc.wait(timeout=10)
        for stream in (self.proc.stdin, self.proc.stdout, self.proc.stderr):
            stream.close()
        return code

    def close(self) -> None:
        self.proc.stdin.close()
        self.proc.wait(timeout=10)
        self.proc.stdout.close()
        self.proc.stderr.close()


def _last_event(path: Path):
    """(kind, payload) of the newest COMMITTED ledger event, read by the supervisor."""
    import sqlite3
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=5)
    try:
        row = db.execute("SELECT kind, payload FROM events ORDER BY seq DESC LIMIT 1").fetchone()
    finally:
        db.close()
    return (row[0], json.loads(row[1])) if row else (None, None)


def _wait_committed(path: Path, kind: str, t: int, timeout: float = 10.0) -> None:
    import time
    deadline = time.time() + timeout
    while time.time() < deadline:
        k, payload = _last_event(path)
        if k == kind and payload.get("t") == t:
            return
        time.sleep(0.001)
    raise RuntimeError(f"{kind} for t={t} was never committed")


def supervised_run(config: str, world: str, seed: int, episodes: int, variant: str = "dev",
                   kill_after: Sequence[int] = (), kill_during: Sequence[int] = (),
                   kill_committed: Sequence[int] = (), kill_end_committed: Sequence[int] = (),
                   workdir: Path = None) -> Dict:
    """Run a lifetime in a worker process and SIGKILL it at chosen moments:

      kill_after          ticks: after the reply has been read
      kill_during         ticks: right after sending the request (usually before it commits)
      kill_committed      ticks: after the tick is durably COMMITTED but before the reply
                          is read, so the resend must be answered from the ledger
      kill_end_committed  episode indices: after the episode's end event is committed

    Returns the action trace, the deaths, and how many resends were answered as
    replays (the exactly-once path)."""
    if os.name != "posix" or not hasattr(signal, "SIGKILL"):
        return {"status": "NOT_EXECUTED", "reason": "POSIX SIGKILL required"}
    own_dir = workdir is None
    tmp = tempfile.TemporaryDirectory(prefix="mind-death-") if own_dir else None
    path = Path(tmp.name if own_dir else workdir) / "ledger.sqlite3"
    after, during = set(kill_after), set(kill_during)
    committed, end_committed = set(kill_committed), set(kill_end_committed)
    replays = {"step": 0, "end": 0}
    deaths: List[Dict] = []
    worker = WorkerProcess(path, config, seed)
    env = make_world(world, seed, variant)
    trace: List[str] = []
    tick = 0
    try:
        for episode in range(episodes):
            obs = env.reset()
            reward, outcome, boundary = 0.0, None, True
            while True:
                msg = {"op": "step", "t": tick, "obs": obs, "r": reward, "o": outcome,
                       "b": boundary, "a": list(env.legal())}
                if tick in during:
                    during.discard(tick)
                    worker.send(msg)              # die while (possibly) committing this tick
                    pid = worker.proc.pid
                    deaths.append({"tick": tick, "mode": "during", "exit": worker.kill(), "pid": pid})
                    worker = WorkerProcess(path, config, seed)
                if tick in committed:
                    committed.discard(tick)
                    worker.send(msg)
                    _wait_committed(path, "tick", tick)   # durably committed, reply never read
                    pid = worker.proc.pid
                    deaths.append({"tick": tick, "mode": "committed", "exit": worker.kill(), "pid": pid})
                    worker = WorkerProcess(path, config, seed)
                reply = worker.ask(msg)           # resend: exactly-once via the ledger
                replays["step"] += bool(reply.get("replayed"))
                trace.append(reply["act"])
                if tick in after:
                    after.discard(tick)
                    pid = worker.proc.pid
                    deaths.append({"tick": tick, "mode": "after", "exit": worker.kill(), "pid": pid})
                    worker = WorkerProcess(path, config, seed)
                s = env.step(reply["act"])
                tick += 1
                if s.done:
                    end = {"op": "end", "t": tick, "r": s.reward, "o": s.outcome}
                    if episode in end_committed:
                        end_committed.discard(episode)
                        worker.send(end)
                        _wait_committed(path, "end", tick)
                        pid = worker.proc.pid
                        deaths.append({"tick": tick, "mode": "end-committed", "exit": worker.kill(), "pid": pid})
                        worker = WorkerProcess(path, config, seed)
                    replays["end"] += bool(worker.ask(end).get("replayed"))
                    break
                obs, reward, outcome, boundary = s.obs, s.reward, s.outcome, False
        head = worker.ask({"op": "head"})
        worker.close()
    finally:
        if worker.proc.poll() is None:
            worker.proc.kill()
            worker.proc.wait(timeout=10)
        if tmp is not None:
            tmp.cleanup()
    return {"status": "RUN", "trace": trace, "deaths": deaths, "head": head["head"],
            "final_pid": head["pid"], "events": head["events"], "replays": replays}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--config", default="organism")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    serve(args.ledger, args.config, args.seed)
