# Research: Phase 3 — ChatGPT App

**Date**: 2026-04-28 | **Feature**: 003-chatgpt-app

---

## Decision 1: ChatGPT App Registration Format

**Decision**: A custom GPT with Actions (OpenAI platform). Three files are required:
- `system-prompt.md` → pasted into the GPT "Instructions" field in the GPT Builder
- `openapi.yaml` → uploaded in the GPT "Actions" section as the schema
- `manifest.yaml` → human-readable metadata (name, description, logo, contact); referenced during registration

**Rationale**: This is the standard mechanism for registering a backend-connected AI tutor on the ChatGPT platform. GPT Actions replace the deprecated ChatGPT Plugins format. The "Actions" section in GPT Builder accepts an OpenAPI 3.1 schema that defines exactly which backend endpoints ChatGPT may call.

**Alternatives considered**:
- ChatGPT Plugins (legacy): deprecated, being phased out — rejected
- OpenAI Assistants API: requires custom frontend code — rejected (Phase 3 is config-only)

---

## Decision 2: Authentication Strategy

**Decision**: API Key authentication using the student's Supabase JWT as the key. In the GPT Builder, auth type is set to "API Key" with "Auth Type: Bearer". The student (or demo operator) pastes their JWT into the GPT's auth configuration once.

**Rationale**: The project plan explicitly states: "For the hackathon demo, a single test user account with a known JWT is used to demonstrate all flows — full OAuth wiring is out of scope." API Key / Bearer is the simplest mechanism available in GPT Actions and requires no OAuth server.

**Alternatives considered**:
- OAuth2: correct for production (user-specific JWTs, no shared credential) — deferred to post-hackathon
- No auth: backend routes are all protected — impossible without auth
- Service key: would bypass user-level tier checks — rejected (breaks tier enforcement)

**Implementation note**: The demo JWT is obtained by calling `POST /auth/login` with the demo credentials. The resulting `access_token` is pasted into the GPT's "API Key" field. All Actions calls include `Authorization: Bearer <token>` automatically.

---

## Decision 3: Endpoints to Expose in OpenAPI Actions Schema

**Decision**: Expose exactly 6 endpoints — sufficient for all three user story flows. Never expose admin or hybrid endpoints.

| Endpoint | Purpose | User Story |
|----------|---------|------------|
| `GET /search` | Find chapter by topic keyword | US1 — Teach |
| `GET /access/check` | Check tier before fetching | US1 — Teach |
| `GET /chapters/{id}` | Fetch full chapter content | US1 — Teach |
| `GET /quizzes/{chapter_id}` | Fetch 5 quiz questions | US2 — Quiz |
| `POST /quizzes/{quiz_id}/submit` | Submit answer, get score | US2 — Quiz |
| `GET /progress/{user_id}` | Fetch full progress record | US3 — Progress |

**Excluded endpoints and rationale**:
- `POST /auth/register`, `POST /auth/login`: Auth is handled via the GPT API Key config — ChatGPT manages the token, not the tutor
- `POST /admin/upgrade`: Security — MUST NOT be in the ChatGPT App schema (constitution: "ADMIN_SECRET MUST NOT be exposed in the ChatGPT App openapi spec")
- `POST /hybrid/*`: Phase 5 only
- `GET /chapters` (list all): Optional convenience; tutor uses search flow instead — omitted to keep schema minimal
- `GET /chapters/{id}/next`, `GET /chapters/{id}/prev`: Navigation aids; not needed for the tutor flow

---

## Decision 4: user_id Handling in Quiz Submit

**Decision**: The system prompt instructs the tutor to ask the student for their user_id once at the start of the session (or use a demo constant during hackathon presentation), and reuse it for all `POST /quizzes/{quiz_id}/submit` calls.

**Rationale**: The backend requires `user_id` in the quiz submit body for progress tracking. Without OAuth, the GPT cannot automatically determine the user's UUID. The demo workaround is to have the system prompt instruct the tutor to ask for the user_id early and remember it.

**Alternatives considered**:
- Encode user_id in the API key: not possible with Supabase JWTs (user_id is in the JWT payload but GPT cannot parse it)
- Add a `/me` endpoint that returns the user_id from the JWT: cleaner solution — added as a note for the backend to support; for hackathon demo the constant approach suffices

---

## Decision 5: OpenAPI Schema Version

**Decision**: OpenAPI 3.1.0. Required fields: `openapi`, `info` (title, version, description), `servers` (production Railway URL), `paths`, `components/schemas` for all request/response bodies.

**Rationale**: ChatGPT Actions supports both 3.0.x and 3.1.x. Using 3.1.0 is preferred for JSON Schema alignment and is what OpenAI's documentation now recommends. The schema must be valid and parseable by the GPT Builder validator.

---

## Decision 6: System Prompt Structure

**Decision**: The system prompt is divided into clearly labelled sections for each conversational flow. This makes the tutor predictable and debuggable.

Sections:
1. **Identity & Role** — who the tutor is, what it teaches
2. **Teaching Flow** — step-by-step: search → access check → fetch → explain
3. **Quiz Flow** — step-by-step: fetch questions → one at a time → submit → explain → score
4. **Progress Flow** — fetch and present progress, suggest next
5. **Access Control** — how to handle locked chapters warmly
6. **Personality Rules** — tone, depth adaptation, no condescension
7. **Hard Rules** — never fabricate, always fetch first, never show all quiz questions at once

**Rationale**: Structured prompts are more reliable than prose instructions. Each flow is independently testable by following its section.
