---
id: 0003
title: Next.js web app tasks
stage: tasks
date: 2026-04-29
surface: agent
model: claude-sonnet-4-6
feature: 004-nextjs-web-app
branch: 004-nextjs-web-app
user: Ad1nn
command: /sp.tasks
labels: ["tasks","nextjs","phase-4","app-router","supabase-auth","quiz","chapters"]
links:
  spec: specs/004-nextjs-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-nextjs-web-app/tasks.md
tests:
  - Format validation: all 39 tasks follow checklist format (checkbox, ID, [P?], [Story?], file path)
---

## Prompt

/sp.tasks

## Response snapshot

39 tasks across 8 phases generated for Phase 4 — Next.js Web App LMS Dashboard.

**Phase breakdown**:
- Phase 1 Setup: 5 tasks (T001–T005) — Next.js init, deps, tailwind, .env.example, .gitignore
- Phase 2 Foundational: 11 tasks (T006–T016) — Supabase clients, middleware, api.ts, layout, globals, 4 UI primitives, Navbar
- Phase 3 US1 Auth: 4 tasks (T017–T020) — landing page, signup, login, protected layout
- Phase 4 US2 Chapters: 6 tasks (T021–T026) — ChapterCard, LockedOverlay, ChapterContent, ChapterSidebar, chapter list page, chapter reader page
- Phase 5 US3 Quiz: 4 tasks (T027–T030) — AnswerOption, QuestionCard, ScoreScreen, quiz page
- Phase 6 US4 Progress: 1 task (T031) — progress page
- Phase 7 US5 Dashboard: 3 tasks (T032–T034) — StatCard, ContinueCard, dashboard page
- Phase 8 Polish: 5 tasks (T035–T039) — loading states, error display, logo, quickstart validation, SC-003 DOM check

**Parallel opportunities**: T012–T015 (Phase 2 UI primitives), T021–T023 (Phase 4 chapter components), T027–T029 (Phase 5 quiz components), T032–T033 (Phase 7 dashboard components).

**MVP scope**: Phase 1 + 2 + 3 + 4 + 5 (T001–T030) — landing → auth → chapter list → read → quiz → score.

**Key dependency**: US1 (T020 protected layout) must complete before US2 and US3 can start. US3 must complete before US4 (progress needs quiz data). US4 before US5 (same data source).

## Outcome

- ✅ Impact: 39 implementation tasks ready for /sp.implement — complete coverage of all 5 user stories
- 🧪 Tests: Format validation PASS — all tasks have checkbox, sequential ID (T001–T039), [P] and [Story] labels where applicable, explicit file paths
- 📁 Files: specs/004-nextjs-web-app/tasks.md
- 🔁 Next prompts: `/sp.implement` to execute all tasks phase by phase
- 🧠 Reflection: T026 (chapter reader page) is the most complex single task — it orchestrates checkAccess + getChapter + renders either LockedOverlay or ChapterContent, plus prev/next navigation. T030 (quiz page) manages the 4-state QuizState machine. Both warrant careful implementation.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Format validation PASS (39/39 tasks conform to checklist format)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Run /sp.implement; watch for backend gap — GET /chapters list endpoint may need to be added to FastAPI before T025 can be completed
