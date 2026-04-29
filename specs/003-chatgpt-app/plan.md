# Implementation Plan: ChatGPT App — AI Tutor Integration

**Branch**: `003-chatgpt-app` | **Date**: 2026-04-28 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/003-chatgpt-app/spec.md`

## Summary

Build the three configuration files that register the Course Companion backend as a custom GPT with Actions on the ChatGPT platform. No new backend code is written. The deliverables are:
1. `chatgpt-app/system-prompt.md` — full tutor behavior instructions
2. `chatgpt-app/openapi.yaml` — Actions schema describing all backend endpoints the tutor can call
3. `chatgpt-app/manifest.yaml` — app metadata for platform registration

The system prompt defines every conversational flow (teaching, quiz, progress, access control, personality). The OpenAPI spec must exactly mirror the Phase 1 backend's deployed endpoint signatures.

## Technical Context

**Language/Version**: YAML 1.2, Markdown — config files only, no programming language  
**Primary Dependencies**: OpenAI ChatGPT platform (custom GPT + Actions); Phase 1 FastAPI backend on Railway  
**Storage**: N/A — reads/writes go through the existing backend  
**Testing**: Manual — ChatGPT App opened in browser, all 3 user story flows exercised  
**Target Platform**: OpenAI ChatGPT (custom GPT with Actions)  
**Project Type**: Config-only — no source directories, no build step  
**Performance Goals**: N/A — all performance constraints are on the backend (Phase 1)  
**Constraints**: OpenAPI spec must be OpenAPI 3.1 compatible; action count limited by ChatGPT platform (max 30 per GPT); system prompt must fit within ChatGPT's instruction character limit (~32k chars)  
**Scale/Scope**: Single GPT registration; 3 files; ~500 lines total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Zero-LLM Backend | ✅ PASS | Phase 3 adds no backend code. No LLM calls added to the backend. ChatGPT (external) does all intelligence. |
| II. Tier Enforcement at Data Layer | ✅ PASS | Backend enforces tiers. The system prompt instructs the tutor to call `/access/check` before every chapter fetch — but backend enforcement is the authoritative gate. |
| III. JWT-First Authentication | ✅ PASS | OpenAPI spec uses `Bearer` token auth. The system prompt must instruct the tutor to pass the student's access token in every request header. |
| IV. Content Isolation | ✅ PASS | Tutor uses `GET /quizzes/{chapter_id}` which never returns `correct_answer`. Scoring goes through `POST /quizzes/{quiz_id}/submit`. |
| V. Smallest Viable Diff | ✅ PASS | Only 3 new files under `chatgpt-app/`. No existing files touched. |
| VI. Build-Order Discipline | ✅ PASS | Phase 1 (backend) ✅ and Phase 2 (content seeding) ✅ are complete. Phase 3 can begin. |
| VII. Observability at Every Write | ✅ PASS | All writes (quiz submit, progress update) go through the backend which persists to Supabase. The tutor itself does no direct DB writes. |

**All gates pass. Proceeding to Phase 0.**

## Project Structure

### Documentation (this feature)

```text
specs/003-chatgpt-app/
├── plan.md              ← this file
├── research.md          ← Phase 0 output
├── data-model.md        ← Phase 1 output (endpoint reference)
├── quickstart.md        ← Phase 1 output (registration + test guide)
└── tasks.md             ← Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
chatgpt-app/
├── system-prompt.md     ← Tutor instructions (pasted into GPT "Instructions" field)
├── openapi.yaml         ← Actions schema (uploaded to GPT "Actions" section)
└── manifest.yaml        ← App metadata (name, description, logo, contact)
```

No `backend/`, `web/`, or `src/` changes for this phase.

**Structure Decision**: Config-only. All three files live under `chatgpt-app/` at the repo root, matching the project plan's repo structure.

## Complexity Tracking

*No constitution violations — section not required.*
