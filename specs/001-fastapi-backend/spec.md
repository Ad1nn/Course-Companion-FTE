# Feature Specification: Phase 1 — FastAPI Backend

**Feature Branch**: `001-fastapi-backend`
**Created**: 2026-04-28
**Status**: Draft
**Input**: User description: "write specification for phase 1"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Student Browses Course Chapters (Priority: P1)

A student opens the Course Companion and wants to see what chapters are available
and which ones they can access with their current subscription tier.

**Why this priority**: Entry point for all learning activity. Without chapter listing,
no other feature is reachable.

**Independent Test**: Call `GET /chapters` with a valid JWT — verify the chapter list
returns titles, descriptions, and tier fields but no content. Then call
`GET /chapters/4` as a free-tier user and verify a 403 is returned.

**Acceptance Scenarios**:

1. **Given** an unauthenticated request, **When** `GET /chapters` is called, **Then** a 401 response is returned.
2. **Given** a free-tier student, **When** `GET /chapters` is called, **Then** all 10 chapters are returned with `title`, `description`, `tier`, `order_num` — and no `content` field.
3. **Given** a free-tier student, **When** `GET /chapters/4` is called (premium chapter), **Then** a 403 response is returned with `required_tier`, `user_tier`, and `message`.
4. **Given** a premium-tier student, **When** `GET /chapters/4` is called, **Then** the full chapter including `content` is returned.
5. **Given** any authenticated student, **When** `GET /chapters/{id}/next` or `/prev` is called, **Then** the adjacent accessible chapter is returned.

---

### User Story 2 — Student Takes a Quiz (Priority: P1)

A student who has read a chapter wants to test their knowledge by answering the
5 quiz questions for that chapter. The system records their score.

**Why this priority**: Quizzes are the core assessment mechanism and a primary
hackathon evaluation criterion.

**Independent Test**: Call `GET /quizzes/{chapter_id}` and verify `correct_answer`
is never in the response. Submit all 5 answers via `POST /quizzes/{quiz_id}/submit`
and verify score is returned on the final submission.

**Acceptance Scenarios**:

1. **Given** a student, **When** `GET /quizzes/1` is called, **Then** 5 questions are returned each with `id`, `question`, `option_a–d`, `order_num` — and `correct_answer` is NEVER present.
2. **Given** a student submits a correct answer, **When** `POST /quizzes/{quiz_id}/submit` is called, **Then** response includes `correct: true`, `correct_answer`, and `explanation`.
3. **Given** a student submits a wrong answer, **When** the submit endpoint is called, **Then** `correct: false`, the correct answer, and explanation are returned.
4. **Given** a student submits the 5th and final answer, **When** the submit endpoint is called, **Then** the score (0–100) is returned and saved to the `progress` table.

---

### User Story 3 — Student Tracks Their Progress (Priority: P2)

A student wants to see their overall learning progress: chapters completed, scores,
and current streak.

**Why this priority**: Progress tracking drives retention and is displayed on the
Next.js dashboard.

**Independent Test**: After submitting quiz results, call `GET /progress/{user_id}`
and verify the chapter's score and completion status appear.

**Acceptance Scenarios**:

1. **Given** a student with no activity, **When** `GET /progress/{user_id}` is called, **Then** a valid response is returned with `chapters_completed: 0`.
2. **Given** a student who completed chapter 1 with 80%, **When** `GET /progress/{user_id}` is called, **Then** `avg_score: 80`, `chapters_completed: 1`, and the chapter entry shows `completed: true, score: 80`.
3. **Given** a student active on 3 consecutive calendar days, **When** `GET /progress/{user_id}` is called, **Then** `streak_days: 3` is returned.
4. **Given** a valid PUT body, **When** `PUT /progress/{user_id}` is called, **Then** the progress record is upserted and 200 is returned.

---

### User Story 4 — Student Registers and Logs In (Priority: P1)

A new student creates an account and an existing student authenticates to access
protected content.

**Why this priority**: Authentication is a prerequisite for all other protected endpoints.

**Independent Test**: Call `POST /auth/register` with a new email/password, then
`POST /auth/login` with the same credentials. Verify a JWT is returned and can be
used to call `GET /chapters`.

**Acceptance Scenarios**:

1. **Given** a new email/password, **When** `POST /auth/register` is called, **Then** a user is created in auth, a row is inserted into `users` with `tier: free`, and `{ user_id, email, tier }` is returned.
2. **Given** valid credentials, **When** `POST /auth/login` is called, **Then** `{ access_token, user_id, tier }` is returned.
3. **Given** invalid credentials, **When** `POST /auth/login` is called, **Then** a 401 response is returned.
4. **Given** a duplicate email, **When** `POST /auth/register` is called, **Then** a 400 response is returned.

---

### User Story 5 — ChatGPT Searches Course Content (Priority: P1)

The ChatGPT tutor searches for relevant chapters before explaining a topic to a student.

**Why this priority**: Primary way ChatGPT discovers content. Without search, the
ChatGPT App cannot function.

**Independent Test**: Call `GET /search?q=MCP` and verify up to 5 results are returned
with `id`, `title`, `excerpt`, and `tier`.

**Acceptance Scenarios**:

1. **Given** a keyword matching chapter titles or content, **When** `GET /search?q={keyword}` is called, **Then** up to 5 results are returned with `id`, `title`, `excerpt`, and `tier`.
2. **Given** a keyword with no matches, **When** `GET /search?q=xyz123` is called, **Then** an empty array is returned (not a 404).

---

### User Story 6 — Admin Upgrades a Student's Tier (Priority: P2)

A hackathon demo admin manually upgrades a student's subscription tier to demonstrate
premium/pro content access.

**Why this priority**: No Stripe integration — tier upgrades are demo-only via admin endpoint.

**Independent Test**: Call `POST /admin/upgrade` with a valid `ADMIN_SECRET` header,
verify the user's tier is updated, then confirm the upgraded user can access previously
locked chapters.

**Acceptance Scenarios**:

1. **Given** a valid `ADMIN_SECRET` header and `{ user_id, tier: "premium" }`, **When** `POST /admin/upgrade` is called, **Then** the user's tier is updated and 200 is returned.
2. **Given** a missing or wrong `ADMIN_SECRET`, **When** `POST /admin/upgrade` is called, **Then** a 403 response is returned.

---

### Edge Cases

- What happens when a chapter ID does not exist? → 404 with a clear message.
- What happens when a quiz ID does not exist on submit? → 404.
- What happens when `answer` in submit body is not A/B/C/D? → 400 validation error.
- What happens when `GET /progress/{user_id}` is called for a non-existent user? → 404.
- What happens when search query is empty? → 400 validation error.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose all chapter, quiz, progress, auth, access, admin, and search endpoints defined in the project plan.
- **FR-002**: System MUST validate the student's identity token on every protected route before processing the request.
- **FR-003**: System MUST enforce tier-based access control on `GET /chapters/{id}`, returning 403 with `required_tier`, `user_tier`, and `message` when access is denied.
- **FR-004**: System MUST NEVER include quiz answer data in `GET /quizzes/{chapter_id}` responses.
- **FR-005**: System MUST calculate and return the quiz score on the final (5th) question submission and persist it to the progress record.
- **FR-006**: System MUST calculate `streak_days` as consecutive calendar days with at least one chapter completed, resetting if no activity for 24+ hours.
- **FR-007**: System MUST make zero calls to any external AI or LLM service in Phase 1. Routes under `/hybrid/*` MUST return 501 Not Implemented.
- **FR-008**: System MUST require the admin secret on `POST /admin/upgrade` and return 403 if absent or incorrect.
- **FR-009**: `GET /chapters` MUST return titles, descriptions, tier, and order only — never the full content field.
- **FR-010**: `GET /search` MUST search across chapter titles and content, returning at most 5 results with an excerpt snippet around the match.
- **FR-011**: `POST /auth/register` MUST create the auth user AND insert the user row into the users table before returning success.
- **FR-012**: All mutations (quiz submissions, progress updates, tier upgrades) MUST be persisted before the HTTP response is returned.
- **FR-013**: `GET /access/check` MUST return `{ allowed: true }` or `{ allowed: false, required_tier, user_tier }` based on the authenticated student's tier.

### Key Entities

- **Chapter**: Course unit with title, description, full content, order position, and tier gate (free/premium/pro).
- **Quiz**: Set of 5 multiple-choice questions per chapter; correct answers stored server-side only and never returned in list responses.
- **User**: Authenticated student with email and a subscription tier (free/premium/pro).
- **Progress**: Per-user, per-chapter record of completion status, score (0–100), attempt count, and timestamps.
- **LLM Cost**: Audit log table for Phase 5 AI usage — exists in the database but unused in Phase 1.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All API endpoints return correct responses for happy-path requests as verified by manual smoke testing.
- **SC-002**: Tier enforcement correctly blocks and allows chapter access for all three tiers in 100% of test cases.
- **SC-003**: Quiz answer data is absent from 100% of chapter quiz list responses.
- **SC-004**: A complete student journey (register → login → read chapter → take quiz → view progress) succeeds end-to-end without errors.
- **SC-005**: The backend makes zero calls to any external AI or LLM service during Phase 1.
- **SC-006**: All endpoints respond within 500ms under normal single-user conditions.
- **SC-007**: The admin upgrade endpoint correctly updates tier and rejects unauthorized requests in 100% of test cases.
