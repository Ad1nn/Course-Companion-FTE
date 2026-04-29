---
id: 001
title: Phase 2 Content Seeding Spec
stage: spec
date: 2026-04-28
surface: agent
model: claude-sonnet-4-6
feature: 002-content-seeding
branch: 002-content-seeding
user: Ad1nn
command: /sp.specify
labels: ["spec","content","seeding","phase-2","chapters","quizzes"]
links:
  spec: specs/002-content-seeding/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-content-seeding/spec.md
  - specs/002-content-seeding/checklists/requirements.md
tests:
  - none
---

## Prompt

write for phase 2

## Response snapshot

Created Phase 2 content seeding specification at `specs/002-content-seeding/spec.md`.

2 user stories:
- US1 (P1): Student reads full chapter content — 10 chapters, 500+ words each, correct tiers
- US2 (P1): Student takes complete chapter quiz — 50 questions, 5 per chapter, idempotent seeding

9 functional requirements covering: exact chapter/quiz counts, tier assignments, content quality,
idempotency, and description format.

6 success criteria all measurable and verifiable via existing API endpoints.

Chapter catalogue embedded in spec for traceability (all 10 titles, tiers, textbook sources).

## Outcome

- ✅ Impact: Phase 2 scope fully specified; ready for /sp.tasks (plan not needed — seeding is straightforward)
- 🧪 Tests: Verifiable via GET /chapters and GET /quizzes/{id} for all 10 chapters
- 📁 Files: specs/002-content-seeding/spec.md, checklists/requirements.md
- 🔁 Next prompts: /sp.tasks then /sp.implement to write and run the seeding script
- 🧠 Reflection: Idempotency (FR-008) is the most important constraint — seeding must be safe to re-run

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): checklist all passing
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): /sp.tasks for 002-content-seeding
