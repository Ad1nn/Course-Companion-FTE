# Implementation Plan: Phase 1 — FastAPI Backend

**Branch**: `001-fastapi-backend` | **Date**: 2026-04-28 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-fastapi-backend/spec.md`

## Summary

Build a deterministic FastAPI backend that serves course content, enforces subscription
tier access, manages quiz submissions, and tracks student progress — all without making
any LLM or AI API calls. The backend is the shared data layer for both the ChatGPT App
(Phase 3) and the Next.js web app (Phase 4). It reads and writes to Supabase PostgreSQL
and delegates all intelligence to ChatGPT on the client side.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, uvicorn, supabase-py, python-dotenv, pydantic v2
**Storage**: Supabase (PostgreSQL) — 5 tables: chapters, quizzes, users, progress, llm_costs
**Testing**: Manual smoke testing via curl / Swagger UI at `/docs`
**Target Platform**: Linux server on Railway (Docker-less, uvicorn direct)
**Project Type**: Backend API (single project under `backend/`)
**Performance Goals**: All endpoints <500ms p95 under single-user Supabase latency
**Constraints**: Zero LLM calls in Phase 1. `service_role` key used server-side only — never exposed to clients. `ADMIN_SECRET` never in OpenAPI spec.
**Scale/Scope**: Hackathon demo — single-digit concurrent users, 10 chapters, 50 quizzes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Status |
|-----------|-------|--------|
| I. Zero-LLM Backend | No LLM calls anywhere in Phase 1 routes. `/hybrid/*` returns 501. | ✅ PASS |
| II. Tier Enforcement at Data Layer | Every `GET /chapters/{id}` checks tier before returning content. 403 includes `required_tier`, `user_tier`, `message`. | ✅ PASS |
| III. JWT-First Auth | All protected routes call `supabase.auth.get_user(token)`. No cookies. No hardcoded secrets. | ✅ PASS |
| IV. Content Isolation | `GET /quizzes/{chapter_id}` never returns `correct_answer`. Only `/submit` reveals it post-answer. | ✅ PASS |
| V. Smallest Viable Diff | Each route file implements only its endpoint group. No speculative abstractions. | ✅ PASS |
| VI. Build-Order Discipline | Phase 1 before Phase 2 content seeding. Hybrid routes stubbed, not skipped. | ✅ PASS |
| VII. Observability at Every Write | All mutations persisted to Supabase before response returned. | ✅ PASS |

**Gate result: ALL PASS — proceed to Phase 0.**

## Project Structure

### Documentation (this feature)

```text
specs/001-fastapi-backend/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── openapi.md
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI app init, router registration, CORS
├── database.py          # Supabase client singleton
├── models.py            # Pydantic request/response models
├── requirements.txt     # Python dependencies
├── middleware/
│   ├── __init__.py
│   └── auth.py          # get_current_user() dependency — JWT validation
└── routes/
    ├── __init__.py
    ├── auth.py          # POST /auth/register, POST /auth/login
    ├── chapters.py      # GET /chapters, /chapters/{id}, /next, /prev
    ├── quizzes.py       # GET /quizzes/{chapter_id}, POST /quizzes/{id}/submit
    ├── progress.py      # GET /progress/{user_id}, PUT /progress/{user_id}
    ├── access.py        # GET /access/check
    ├── admin.py         # POST /admin/upgrade
    ├── search.py        # GET /search (moved from chapters for clarity)
    └── hybrid.py        # POST /hybrid/* — all return 501 (Phase 5 stubs)
```

**Structure Decision**: Single backend project under `backend/`. Routes split by domain
(one file per endpoint group) to keep each file under 100 lines and independently
reviewable. No service layer abstraction — routes call Supabase client directly.
This is the smallest viable structure for a hackathon-scoped API.

## Complexity Tracking

> No constitution violations — complexity tracking not required.
