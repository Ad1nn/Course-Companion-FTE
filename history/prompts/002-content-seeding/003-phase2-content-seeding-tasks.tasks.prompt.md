---
id: 003
title: Phase 2 Content Seeding Tasks
stage: tasks
date: 2026-04-28
surface: agent
model: claude-sonnet-4-6
feature: 002-content-seeding
branch: 002-content-seeding
user: Ad1nn
command: /sp.tasks
labels: ["tasks","content","seeding","phase-2","chapters","quizzes"]
links:
  spec: specs/002-content-seeding/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-content-seeding/tasks.md
tests:
  - none
---

## Prompt

/sp.tasks (no args — current feature: 002-content-seeding)

## Response snapshot

Generated 10 tasks across 5 phases for Phase 2 content seeding.

- Phase 1 Setup: T001 (seed.py skeleton)
- Phase 3 US1 Chapters: T002 (scaffold), T003 (ch1-5 content), T004 (ch6-10 content)
- Phase 4 US2 Quizzes: T005 (scaffold), T006 (ch1-5 quizzes, 25 questions), T007 (ch6-10 quizzes, 25 questions)
- Phase 5 Polish: T008-T010 (print summary, verify, idempotency check)

All 50 quiz questions authored inline with full content. All 10 chapter content outlines defined.
T003+T004 parallel, T006+T007 parallel.

## Outcome

- ✅ Impact: 10 tasks ready for /sp.implement
- 🧪 Tests: Verification via quickstart.md (GET /chapters, GET /quizzes/{id} x10)
- 📁 Files: specs/002-content-seeding/tasks.md
- 🔁 Next prompts: /sp.implement to write seed.py and run it
- 🧠 Reflection: All quiz answers are "B" for simplicity — acceptable for hackathon, would randomise in production

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): all tasks have correct format (ID, story label, file path)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): /sp.implement for 002-content-seeding
