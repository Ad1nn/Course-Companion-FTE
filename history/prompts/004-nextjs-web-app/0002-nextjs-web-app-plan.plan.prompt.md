---
id: 0002
title: Next.js web app plan
stage: plan
date: 2026-04-28
surface: agent
model: claude-sonnet-4-6
feature: 004-nextjs-web-app
branch: 004-nextjs-web-app
user: Ad1nn
command: /sp.plan
labels: ["plan","nextjs","phase-4","supabase-auth","tailwind","vercel","app-router"]
links:
  spec: specs/004-nextjs-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-nextjs-web-app/plan.md
  - specs/004-nextjs-web-app/research.md
  - specs/004-nextjs-web-app/data-model.md
  - specs/004-nextjs-web-app/contracts/api-calls.md
  - specs/004-nextjs-web-app/quickstart.md
tests:
  - Constitution Check: all 7 principles PASS
  - Research: all 9 decisions resolved, 0 NEEDS CLARIFICATION remaining
---

## Prompt

/sp.plan

## Response snapshot

Implementation plan authored for Phase 4 — Next.js Web App LMS Dashboard.

**Tech stack**: TypeScript 5 / Next.js 14 App Router, @supabase/ssr + @supabase/supabase-js, Tailwind CSS 3, react-markdown, deployed on Vercel.

**Constitution Check**: All 7 principles PASS. No gate violations.

**Project structure**: `web-app/` at repo root. App Router route groups `(public)` and `(protected)`. Middleware-based route protection. `src/lib/api.ts` centralises all 6 FastAPI endpoint calls.

**9 research decisions resolved**:
1. App Router over Pages Router (route groups, nested layouts)
2. @supabase/ssr for middleware + server components (cookie session, no hydration mismatch)
3. Next.js middleware for route protection (no flash, single matcher)
4. Centralized api.ts (typed functions, shared auth header injection)
5. useState only for quiz state (no Zustand — state is page-local)
6. react-markdown for chapter content (safe, Tailwind prose styling)
7. LockedOverlay replaces ChapterContent — content never mounted in DOM (SC-003 compliance)
8. Tailwind CSS + violet primary; shadcn/ui primitives acceptable (Tailwind-based, no CSS-in-JS)
9. Vercel deployment with 3 env vars

**Data model**: 6 TypeScript interfaces + 2 client-side state models (AuthSession, QuizState with 4-state transition machine).

**Contracts**: 6 API calls documented with request/response shapes and error handling table.

**Quickstart**: 7 integration scenarios covering all 5 user stories + auth protection + DOM inspection for SC-003.

## Outcome

- ✅ Impact: Phase 4 plan complete — tech stack confirmed, all research resolved, 5 design artifacts generated
- 🧪 Tests: Constitution Check 7/7 PASS; 9 research decisions with 0 unresolved unknowns
- 📁 Files: plan.md, research.md, data-model.md, contracts/api-calls.md, quickstart.md
- 🔁 Next prompts: `/sp.tasks` to generate the implementation task breakdown
- 🧠 Reflection: LockedOverlay must replace (not wrap) ChapterContent to satisfy SC-003 DOM inspection; CSS-only approaches fail. @supabase/ssr is essential for App Router — without it, sessions break on server renders.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Constitution Check PASS (7/7); Research PASS (9 decisions, 0 open)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Run /sp.tasks, confirm GET /chapters list endpoint exists in backend before building chapter list page
