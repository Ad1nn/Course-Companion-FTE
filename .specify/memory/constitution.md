<!--
  SYNC IMPACT REPORT
  ==================
  Version change: (none) → 1.0.0 (initial ratification)

  Modified principles: N/A (first version)

  Added sections:
  - Core Principles (I–VII)
  - Tech Stack & Constraints
  - Development Workflow
  - Governance

  Removed sections: N/A

  Templates requiring updates:
  - ✅ .specify/templates/plan-template.md — Constitution Check section aligns with principles below
  - ✅ .specify/templates/spec-template.md — FR/SC structure compatible; no updates needed
  - ✅ .specify/templates/tasks-template.md — Phase/task structure compatible; no updates needed

  Deferred items: none
-->

# Course Companion FTE Constitution

## Core Principles

### I. Zero-LLM Backend (Phase 1 NON-NEGOTIABLE)

The FastAPI backend MUST NOT make any LLM or AI API calls during Phase 1.
All intelligence is delegated entirely to ChatGPT on the client side.
The backend is a deterministic data server: it reads from and writes to Supabase,
performs tier-access enforcement, and returns raw structured data.

**Rationale:** Keeps Phase 1 costs at near-zero and allows linear-cost-free scaling.
Violating this constraint is grounds for immediate hackathon disqualification.

**Rule:** Any route that calls an external LLM API MUST live exclusively under `/hybrid/*`
and MUST be gated behind a `pro` tier check. These routes are Phase 5 only.

### II. Tier Enforcement at the Data Layer

Every request for chapter content MUST enforce tier access before returning any data.
The backend MUST check the authenticated user's tier against the chapter's required tier
on every `/chapters/{id}` call. A `403` response MUST include `required_tier`,
`user_tier`, and `message` fields.

**Rule:** Tier checks MUST happen inside the route handler using the authenticated JWT.
Frontend access checks (`/access/check`) are convenience only — they do NOT replace
server-side enforcement.

### III. JWT-First Authentication

All protected routes MUST validate the `Authorization: Bearer <token>` header by calling
`supabase.auth.get_user(token)` to extract `user_id`. No session cookies. No API keys
for user identity. Secrets (env vars) MUST never be hardcoded.

**Rule:** Every protected route dependency MUST derive `user_id` from the verified JWT.
The `ADMIN_SECRET` header is the sole exception for `/admin/*` routes (demo only).

### IV. Content Isolation — Answers Never Leak

Quiz answer fields (`correct_answer`) MUST NEVER be returned by `GET /quizzes/{chapter_id}`.
Only `POST /quizzes/{quiz_id}/submit` may compare and reveal the correct answer,
and only after receiving the student's submitted answer.

**Rationale:** Prevents trivial cheating and preserves quiz integrity for all frontends.

### V. Smallest Viable Diff

Every implementation task MUST represent the smallest change that satisfies the
acceptance criteria. Refactoring unrelated code, adding speculative abstractions,
or introducing helpers for one-time operations is prohibited without an explicit
spec change.

**Rule:** PRs MUST NOT touch files outside the scope of their linked task unless
a dependency forces it. Justify every out-of-scope edit inline.

### VI. Build-Order Discipline

Phases are executed in order: 1 → 2 → 3 → 4 → 5 → 6.
Phase 5 (Hybrid/LLM) is the only cuttable phase.
Phases 1 and 3 (backend + ChatGPT App) are highest-value deliverables and
MUST NEVER be cut. Phase 4 (Next.js web app) MUST NOT be cut if time allows.

**Rule:** No phase may begin until its predecessor is deployed and smoke-tested.

### VII. Observability at Every Write

Every mutation (quiz submission, progress update, tier upgrade, LLM call) MUST
be persisted to the appropriate Supabase table before the response is returned.
Phase 5 LLM calls MUST log `tokens_in`, `tokens_out`, and `cost_usd` to `llm_costs`.

**Rationale:** Enables cost tracking, debugging, and audit without external tooling.

## Tech Stack & Constraints

**Backend:** FastAPI (Python 3.11+) deployed on Railway.
**Database:** Supabase (PostgreSQL). Schema is authoritative as defined in the project plan.
**File Storage:** Supabase Storage. Cloudflare R2 is explicitly excluded.
**ChatGPT Frontend:** OpenAI Apps SDK — config files only (`system-prompt.md`, `openapi.yaml`,
`manifest.yaml`). No custom code.
**Web Frontend:** Next.js 14 App Router on Vercel. Tailwind CSS. No CSS-in-JS.
**Auth:** Supabase Auth (email + password). JWT stored and managed by Supabase client.
**Phase 5 LLM:** Claude Sonnet API (`claude-sonnet-4-6`) via `anthropic` SDK. Pro tier only.
**Builder:** Claude Code with Spec-Driven Development (SDD).

**Performance budget (Phase 1):** All non-LLM endpoints MUST respond within 300 ms p95
under normal Supabase latency. No caching layer required for hackathon scope.

**Security non-negotiables:**
- No secrets in source code. Use `.env` + Railway/Vercel env vars.
- `ADMIN_SECRET` MUST NOT be exposed in the ChatGPT App openapi spec.
- SQL MUST use parameterized queries (Supabase client handles this via PostgREST/SDK).

## Development Workflow

1. **Spec first.** Every feature starts with a `spec.md` capturing user stories and
   acceptance criteria before any code is written.
2. **Plan second.** `plan.md` documents architecture decisions and file structure.
   ADR suggestions MUST be raised for significant decisions.
3. **Tasks third.** `tasks.md` lists dependency-ordered, independently testable tasks.
4. **Implement last.** Code is written task-by-task, smallest diff first.
5. **PHR always.** A Prompt History Record MUST be created after every significant
   user–agent exchange (implementation, planning, debugging, spec creation).
6. **Commit convention:** `feat:` / `fix:` / `chore:` / `test:` / `docs:` prefixes required.
   Every commit references the task ID where applicable.

**Branching:** Work on `master` for this solo hackathon. Feature branches are optional
but recommended for phases.

## Governance

- This constitution supersedes all other development practices within this project.
- Amendments require: (1) a written rationale, (2) a version bump per semantic versioning,
  (3) a sync pass across all affected templates and command files.
- MAJOR bump: principle removal, redefinition, or backward-incompatible governance change.
- MINOR bump: new principle or section added.
- PATCH bump: clarification, wording, or typo fix.
- All PRs (or task completions) MUST verify compliance with the principles above before
  marking done. The plan-template.md `Constitution Check` gate enforces this.
- Use `.specify/memory/constitution.md` as the single authoritative source. Do not
  duplicate principle text in README or other docs — link back here.

**Version**: 1.0.0 | **Ratified**: 2026-04-28 | **Last Amended**: 2026-04-28
