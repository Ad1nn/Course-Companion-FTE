---
description: "Task list for Phase 1 FastAPI Backend implementation"
---

# Tasks: Phase 1 — FastAPI Backend

**Input**: Design documents from `/specs/001-fastapi-backend/`
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/openapi.md ✅

**Tests**: No test tasks — manual smoke testing via quickstart.md is the validation strategy.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US6)
- Paths are relative to repo root

---

## Phase 1: Setup

**Purpose**: Project initialization and dependency configuration

- [x] T001 Install Python dependencies: create `backend/requirements.txt` with fastapi, uvicorn[standard], supabase, python-dotenv, pydantic
- [x] T002 [P] Create `backend/main.py` — FastAPI app init with CORS middleware, health check `GET /`, and router registration stubs
- [x] T003 [P] Create `backend/database.py` — Supabase client singleton using `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` from environment
- [x] T004 [P] Create `backend/models.py` — all Pydantic request/response models (ChapterSummary, ChapterDetail, QuizQuestion, SubmitRequest, SubmitResponse, ProgressResponse, AuthRegisterRequest, AuthLoginRequest, AuthRegisterResponse, AuthLoginResponse, AccessCheckResponse, SearchResult, AdminUpgradeRequest)

**Checkpoint**: Run `cd backend && pip install -r requirements.txt && uvicorn main:app --reload` — server starts, `GET /` returns 200.

---

## Phase 2: Foundational

**Purpose**: Auth middleware that ALL protected routes depend on

**⚠️ CRITICAL**: No user story implementation can begin until T005 is complete.

- [x] T005 Create `backend/middleware/auth.py` — `get_current_user()` FastAPI dependency that extracts Bearer token from `Authorization` header, calls `supabase.auth.get_user(token)`, returns `user_id` and `tier` from the `users` table, raises 401 if missing/invalid

**Checkpoint**: Write a throwaway test route in `main.py` using `Depends(get_current_user)` — confirm it returns 401 without token and user data with valid token. Remove throwaway route after.

---

## Phase 3: User Story 4 — Register and Login (Priority: P1) 🎯 MVP Entry Point

**Goal**: Students can create accounts and authenticate. Provides JWT tokens for all other stories.

**Independent Test**: `POST /auth/register` creates user → `POST /auth/login` returns JWT → JWT works on `GET /chapters`.

### Implementation

- [x] T006 [US4] Implement `backend/routes/auth.py` — `POST /auth/register`: call `supabase.auth.sign_up()`, insert row into `users` table with `tier='free'`, return `AuthRegisterResponse`
- [x] T007 [US4] Implement `POST /auth/login` in `backend/routes/auth.py`: call `supabase.auth.sign_in_with_password()`, fetch user tier from `users` table, return `AuthLoginResponse`
- [x] T008 [US4] Register auth router in `backend/main.py` with prefix `/auth`
- [x] T009 [US4] Add error handling in `backend/routes/auth.py`: 400 for duplicate email, 401 for invalid credentials

**Checkpoint**: Run smoke test steps 1–2 from quickstart.md. Register and login return correct shapes.

---

## Phase 4: User Story 1 — Browse Chapters with Tier Enforcement (Priority: P1)

**Goal**: Students see all chapters listed; reading full content enforces tier access.

**Independent Test**: `GET /chapters` returns 10 chapters without content. `GET /chapters/4` returns 403 for free user, 200 for premium user.

### Implementation

- [x] T010 [P] [US1] Implement `backend/routes/chapters.py` — `GET /chapters`: query Supabase `chapters` table, return list of `ChapterSummary` (id, title, description, order_num, tier — NO content field)
- [x] T011 [P] [US1] Implement `GET /chapters/{id}` in `backend/routes/chapters.py`: fetch chapter, check `TIER_ORDER[user.tier] >= TIER_ORDER[chapter.tier]`, return `ChapterDetail` or 403 with `required_tier`, `user_tier`, `message`
- [x] T012 [US1] Implement `GET /chapters/{id}/next` and `GET /chapters/{id}/prev` in `backend/routes/chapters.py`: query by `order_num +/- 1`, return `ChapterSummary` or 404
- [x] T013 [US1] Register chapters router in `backend/main.py` with prefix `/chapters`

**Checkpoint**: Run smoke test steps 3–5 from quickstart.md. Tier blocking confirmed for chapters 4–10 for free user.

---

## Phase 5: User Story 5 — ChatGPT Content Search (Priority: P1)

**Goal**: `GET /search?q=` finds relevant chapters for the ChatGPT tutor.

**Independent Test**: `GET /search?q=MCP` returns up to 5 results with `id`, `title`, `excerpt`, `tier`. Empty results for no-match query.

### Implementation

- [x] T014 [US5] Create `backend/routes/search.py` — `GET /search`: validate `q` param (400 if empty), query `chapters` table with `.ilike('title', f'%{q}%')` and `.ilike('content', f'%{q}%')`, merge deduplicated results (max 5), generate 150-char excerpt around first keyword match, return list of `SearchResult`
- [x] T015 [US5] Register search router in `backend/main.py` with prefix (no prefix — `/search` at root)

**Checkpoint**: Run smoke test step 9 from quickstart.md. Search returns results with excerpt snippets.

---

## Phase 6: User Story 2 — Student Takes a Quiz (Priority: P1)

**Goal**: Students answer 5 quiz questions per chapter; correct answers never exposed; score saved on final question.

**Independent Test**: `GET /quizzes/1` returns 5 questions with no `correct_answer` field. Submit all 5 answers; 5th response includes `score`. Check `progress` table in Supabase — score row created.

### Implementation

- [x] T016 [P] [US2] Implement `backend/routes/quizzes.py` — `GET /quizzes/{chapter_id}`: query quiz questions for chapter, return list of `QuizQuestion` with `correct_answer` field explicitly excluded from response
- [x] T017 [US2] Implement `POST /quizzes/{quiz_id}/submit` in `backend/routes/quizzes.py`:
  - Fetch quiz question from DB (including `correct_answer`)
  - Validate `answer` is one of A/B/C/D (400 otherwise)
  - Compare submitted answer to `correct_answer`
  - Count how many questions in this chapter the user has answered
  - If all 5 answered: calculate score (correct/5 * 100), upsert `progress` row with `completed=True`, `score`, `completed_at=now()`
  - Return `SubmitResponse` (with `score` only on final question)
- [x] T018 [US2] Register quizzes router in `backend/main.py` with prefix `/quizzes`

**Checkpoint**: Run smoke test steps 6–7 from quickstart.md. Verify `correct_answer` absent from GET response. Verify score returned on 5th submission.

---

## Phase 7: User Story 3 — Track Progress and Streak (Priority: P2)

**Goal**: Students see completed chapters, scores, and consecutive-day streak.

**Independent Test**: After completing a chapter quiz, `GET /progress/{user_id}` shows `chapters_completed: 1`, correct score, and `streak_days >= 1`.

### Implementation

- [x] T019 [US3] Implement `backend/routes/progress.py` — `GET /progress/{user_id}`:
  - Fetch all progress rows for user joined with chapter titles
  - Calculate `chapters_completed` (count where `completed=True`)
  - Calculate `avg_score` (mean of non-null scores)
  - Calculate `streak_days`: sort `completed_at` dates descending, count consecutive calendar days from today
  - Fetch user `tier` from `users` table
  - Return `ProgressResponse`
- [x] T020 [US3] Implement `PUT /progress/{user_id}` in `backend/routes/progress.py`: upsert into `progress` table using `(user_id, chapter_id)` as unique key, update `completed`, `score`, `last_accessed`, `completed_at` if completing
- [x] T021 [US3] Register progress router in `backend/main.py` with prefix `/progress`

**Checkpoint**: Run smoke test step 8 from quickstart.md. Progress response matches expected shape.

---

## Phase 8: User Story 6 — Admin Tier Upgrade (Priority: P2)

**Goal**: Admin can upgrade any student's tier via secret-protected endpoint.

**Independent Test**: `POST /admin/upgrade` with correct `ADMIN_SECRET` header updates user tier. Wrong/missing secret returns 403.

### Implementation

- [x] T022 [US6] Create `backend/routes/admin.py` — `POST /admin/upgrade`: check `ADMIN_SECRET` header against env var (403 if wrong/missing), update `users` table `tier` field for given `user_id`, return success message
- [x] T023 [US6] Register admin router in `backend/main.py` with prefix `/admin`

**Checkpoint**: Run smoke test steps 10–11 from quickstart.md. Tier upgrade confirmed; premium chapter accessible after upgrade.

---

## Phase 9: User Story 1 (continued) — Access Check Endpoint (Priority: P2)

**Goal**: `GET /access/check` convenience endpoint for frontend tier verification.

**Independent Test**: `GET /access/check?chapter_id=4` returns `{allowed: false, required_tier: "premium", user_tier: "free"}` for free user.

### Implementation

- [x] T024 [US1] Create `backend/routes/access.py` — `GET /access/check?chapter_id={id}`: fetch chapter tier, fetch user tier, return `AccessCheckResponse`
- [x] T025 [US1] Register access router in `backend/main.py` with prefix `/access`

---

## Phase 10: Phase 5 Stubs — Hybrid Routes

**Goal**: `/hybrid/*` routes exist and return 501 — proving zero LLM calls in Phase 1.

- [x] T026 Implement `backend/routes/hybrid.py` — `POST /hybrid/adaptive-path` and `POST /hybrid/assess`: both return `HTTPException(status_code=501, detail="Not implemented — available in Phase 5")`
- [x] T027 Register hybrid router in `backend/main.py` with prefix `/hybrid`

**Checkpoint**: Run smoke test final step from quickstart.md. 501 returned. Zero LLM calls ever made.

---

## Phase 11: Polish & Cross-Cutting Concerns

- [x] T028 [P] Add `.env.example` at project root documenting all required env vars with placeholder values (never real values)
- [x] T029 [P] Verify `backend/main.py` CORS config allows requests from `localhost:3000` (Next.js dev) and the future Vercel domain (`*` for hackathon)
- [x] T030 Add `GET /` health check in `backend/main.py` returning `{"status": "ok", "version": "1.0.0"}`
- [x] T031 [P] Run full 11-step smoke test from `specs/001-fastapi-backend/quickstart.md` end-to-end and confirm all pass
- [x] T032 [P] Verify `backend/requirements.txt` is complete and `pip install -r requirements.txt` succeeds in a clean venv

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately. T002, T003, T004 are parallel.
- **Foundational (Phase 2)**: Depends on T003 (database.py) — BLOCKS all user story routes.
- **US4 Auth (Phase 3)**: Depends on T005 — must complete before other stories (provides JWT).
- **US1 Chapters (Phase 4)**: Depends on T005. T010, T011 are parallel within phase.
- **US5 Search (Phase 5)**: Depends on T005. Independent of US1/US4.
- **US2 Quizzes (Phase 6)**: Depends on T005. T016 is parallel within phase.
- **US3 Progress (Phase 7)**: Depends on T017 (quiz submit writes to progress).
- **US6 Admin (Phase 8)**: Depends on T005 only — fully independent.
- **Access Check (Phase 9)**: Depends on T011 tier logic (can reuse TIER_ORDER constant).
- **Hybrid Stubs (Phase 10)**: No dependencies — can do any time after T002.
- **Polish (Phase 11)**: Depends on all phases complete.

### Critical Path

```
T001 → T002+T003+T004 (parallel) → T005 → T006+T007 → T010+T011+T014+T016 (parallel) → T017 → T019+T020 → T022 → T024 → T026 → T028–T032
```

### Parallel Opportunities Within Each Story

```bash
# Phase 1 parallel launch:
T002: Create main.py
T003: Create database.py
T004: Create models.py

# Phase 4 (US1) parallel launch:
T010: GET /chapters
T011: GET /chapters/{id}

# Phase 9+10 parallel launch (after T005):
T024: access.py
T026: hybrid.py
```

---

## Implementation Strategy

### MVP First (Auth + Chapters only)

1. Complete Phase 1: Setup (T001–T004)
2. Complete Phase 2: Foundational — auth middleware (T005)
3. Complete Phase 3: Auth routes (T006–T009)
4. Complete Phase 4: Chapter routes (T010–T013)
5. **STOP and VALIDATE**: Register → Login → List chapters → Read chapter → Tier block working
6. This is a deployable MVP that proves the core concept

### Incremental Delivery

1. MVP (above) → deploy to Railway → verify live
2. Add Search (Phase 5) → ChatGPT App can now function
3. Add Quizzes (Phase 6) → assessment works
4. Add Progress (Phase 7) → dashboard data available
5. Add Admin + Access + Stubs (Phases 8–10) → feature complete
6. Polish (Phase 11) → ready for Phase 2 content seeding

---

## Notes

- [P] tasks = different files, no shared state — safe to run in parallel
- [USn] label maps task to user story for traceability
- `TIER_ORDER = {"free": 0, "premium": 1, "pro": 2}` — define once in `models.py` or `database.py`, import everywhere
- `correct_answer` must be excluded at the Pydantic model level in `QuizQuestion` — use `model_config` with `exclude` or a separate response model
- Streak resets if no `completed_at` within last 24h — check most recent date against `datetime.utcnow().date()`
- All routes should import `get_current_user` from `middleware.auth` via `Depends()`
