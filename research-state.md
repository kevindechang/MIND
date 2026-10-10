# research-state.md has been retired

MIND v2 does not keep hand-written state. The live, computed state of all knowledge is **[STATUS.md](STATUS.md)**,
which `python -m mind status --write` generates from executable claims, their records and git history. The task queue
is the Frontier section at the top of STATUS.md. Agents start at [GO.md](GO.md).

The final v1 state file is preserved unchanged at [archive/v1/research-state.md](archive/v1/research-state.md). The
v1 → v2 map is [docs/MIGRATION-v2.md](docs/MIGRATION-v2.md).
