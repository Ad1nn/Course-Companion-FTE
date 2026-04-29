---
id: 002
title: Phase 2 Content Seeding Plan
stage: plan
date: 2026-04-28
surface: agent
model: claude-sonnet-4-6
feature: 002-content-seeding
branch: 002-content-seeding
user: Ad1nn
command: /sp.plan
labels: ["plan","content","seeding","phase-2"]
links:
  spec: specs/002-content-seeding/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-content-seeding/plan.md
  - specs/002-content-seeding/research.md
  - specs/002-content-seeding/data-model.md
  - specs/002-content-seeding/quickstart.md
tests:
  - none
---

## Prompt

/sp.plan (no args — current feature: 002-content-seeding)

## Response snapshot

Generated Phase 2 implementation plan. Constitution check: all 7 principles pass.

Key decisions:
- Single backend/seed.py script, content as inline Python strings
- Upsert on chapter id (1-10) and quiz (chapter_id, order_num) for idempotency
- No LLM calls — content authored manually from textbook summaries
- 600-1000 words per chapter targeting ChatGPT context window sweet spot

Artifacts: plan.md, research.md, data-model.md (chapter catalogue), quickstart.md (verify script)

## Outcome

- ✅ Impact: Full seeding plan ready; no blockers for /sp.tasks
- 🧪 Tests: Verification steps in quickstart.md
- 📁 Files: 4 planning artifacts
- 🔁 Next prompts: /sp.tasks then /sp.implement
- 🧠 Reflection: Inline content is the right call — simpler than files, easier to review and edit

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): constitution all passing
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): /sp.tasks for 002-content-seeding
