# Living Digital Mind Research Program — Design Specification

> **Historical publication design.** Current [compounding design](2026-10-10-compounding-research-system-design.md), [research cycle](../../research-cycle.md) and [work accounting](../../research-records.md) supersede older counter/allocation instructions below. Research remains tool-neutral; preserve historical source records.

**Date:** 2026-10-10. **Scope:** digital-mind only. **Status:** proposed publication workflow approved for implementation; not new scientific evidence.

## Objective
Replace a series of short research logs with cumulative, serious scientific publications while preserving reproducibility and falsifiability.

## The publication layers
1. `atlas/`: grand research vision, roadmap, scientific traceability (goal → hypothesis → observable → rival → experiment → status). Inspired by NIH BRAIN 2025, DARPA's Heilmeier questions and NASA science traceability matrices.
2. `dossiers/`: living question-specific monographs. Each contains scoped search methods and limitations, theories and rival mechanisms, primary-source evidence, disagreements, derivations, formal hypotheses, experimental connections, and dated revisions. The first dossier is H001 on autobiographical memory.
3. `experiments/E001/`: Stage 1 prospective protocol (not preregistered until frozen) separate from Stage 2 observations/results; index existing code without moving it. Internal preregistration does not mean formal peer-reviewed Registered Reports.
4. `syntheses/`: periodic cross-stream scientific audits at every eighth verified iteration, or on major valid findings. A governance-time baseline does not qualify as scientific synthesis.
5. `runs/`: concise actual execution records, not substitutes for dossiers.

## Quality standard
A dossier must openly indicate its coverage (e.g. abstract-only sources), strengths, conflicts and missing methods. Do not call it 'systematic' or 'PRISMA-compliant' without an actual documented search and screening. No arbitrary word counts or fabricated papers. Experiments require locked analyses and controls before scoring, matching budget and information, rejecting leakage and weak comparators. A deterministic simulator passing tests is not an AI-agent result. L1 behavioral evidence ≠ L2 integrated mechanisms ≠ L3 phenomenal experience.

## Continuity
ChatGPT is the sole research executor. GitHub is a durable, read-back verified record. No GitHub Actions, new API spending, daemon or production Anjo edits. The existing hourly ChatGPT task should read and improve the relevant dossier/experiment, append a short run for substantial scientific changes and update `research-state.md` last. Governance-only changes never increment the verified iteration. Read live canonical research state; this design was established when E001 G0, A0/A1 candidates and E900 proposals were active. Never hardcode an old iteration as current. The 40-minute duration remains a goal, not an enforceable feature.

## References (standards borrowed, not certifications)
- NIH BRAIN 2025: https://www.nih.gov/brain/about/vision/brain-2025-scientific-vision
- DARPA Heilmeier: https://www.darpa.mil/about/heilmeier-catechism
- NASA STM: https://science.nasa.gov/wp-content/uploads/2023/04/PILaunchpad__STM__JLeisner210615.pdf
- Cochrane living reviews: https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-22
- PRISMA-ScR: https://www.prisma-statement.org/scoping
- Center for Open Science Registered Reports: https://www.cos.io/initiatives/registered-reports
