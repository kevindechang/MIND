# MIND v1 governance (archived)

These files governed MIND until main commit `3c22a93` (the v1 front page is [README-v1.md](README-v1.md)). They were moved here unchanged with `git mv`, so `git log --follow`
shows their full history. **They are superseded and carry no authority.** See
[docs/MIGRATION-v2.md](../../docs/MIGRATION-v2.md) for where each one's function went, and
[docs/PIPELINE.md](../../docs/PIPELINE.md) for why.

Links between archived files still resolve. Links from these files to folders that were *not* archived
(`experiments/`, `dossiers/`, `reviews/`, `runs/`, `sources/`, `scripts/`) are off by two directory levels; prefix
them with `../../`, or browse the repository at commit `3c22a93`.

Their values were carried forward rather than discarded: strong rivals, preregistration, L1/L2/L3 separation, honest
negative results, no by-construction claims, and transitive invalidation of failed premises. v2 implements most of
these in code (`mind/claims.py`, `mind/knowledge.py`, `mind/doctor.py`) instead of prose.
