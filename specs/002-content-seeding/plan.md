# Implementation Plan: Phase 2 — Course Content Seeding

**Branch**: `002-content-seeding` | **Date**: 2026-04-28 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-content-seeding/spec.md`

## Summary

Write a single Python seeding script that inserts all 10 chapters and 50 quiz questions
into Supabase. Content is authored inline in the script (no external API calls, no file
parsing). The script uses upsert so it is safe to re-run. This phase unlocks both the
ChatGPT App (Phase 3) and the Next.js dashboard (Phase 4) which both depend on real data.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: supabase-py, python-dotenv (already in requirements.txt)
**Storage**: Supabase (PostgreSQL) — `chapters` and `quizzes` tables
**Testing**: Manual — call all 10 `GET /chapters/{id}` and `GET /quizzes/{chapter_id}` endpoints
**Target Platform**: Local execution (not deployed; run once to seed)
**Project Type**: Single script under `backend/seed.py`
**Performance Goals**: Script completes in under 60 seconds
**Constraints**: Idempotent (upsert, not insert). No LLM calls. Content authored by hand from textbook summaries.
**Scale/Scope**: 10 chapter rows + 50 quiz rows — trivial data volume

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Status |
|-----------|-------|--------|
| I. Zero-LLM Backend | Seed script makes no LLM calls. Content is static strings. | ✅ PASS |
| II. Tier Enforcement | Tiers assigned per spec: ch 1–3 free, 4–7 premium, 8–10 pro. Enforcement is in the backend (Phase 1). | ✅ PASS |
| III. JWT-First Auth | Seed script uses service_role key directly — not a user-facing route. N/A for this phase. | ✅ PASS |
| IV. Content Isolation | Quiz `correct_answer` is stored in DB; exposure is controlled by Phase 1 routes. | ✅ PASS |
| V. Smallest Viable Diff | One script, one file. No abstractions. | ✅ PASS |
| VI. Build-Order Discipline | Phase 2 runs after Phase 1 backend is live. Supabase tables exist. | ✅ PASS |
| VII. Observability | All writes persisted before script exits. Console output confirms row counts. | ✅ PASS |

**Gate result: ALL PASS — proceed.**

## Project Structure

### Documentation (this feature)

```text
specs/002-content-seeding/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (references Phase 1 schema)
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
└── seed.py              # Single seeding script — all content inline
```

**Structure Decision**: One file. Content as Python dicts. No YAML, no CSV, no JSON files
to manage. Easiest to edit, review, and re-run. Upsert on `id` for chapters, upsert on
`(chapter_id, order_num)` for quizzes to ensure idempotency.

## Complexity Tracking

> No constitution violations — complexity tracking not required.
