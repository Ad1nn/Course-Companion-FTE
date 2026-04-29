---
id: 0003
title: ChatGPT App tasks
stage: tasks
date: 2026-04-28
surface: agent
model: claude-sonnet-4-6
feature: 003-chatgpt-app
branch: 003-chatgpt-app
user: Ad1nn
command: /sp.tasks
labels: ["tasks","chatgpt-app","phase-3","openapi","system-prompt","gpt-actions"]
links:
  spec: specs/003-chatgpt-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-chatgpt-app/tasks.md
tests:
  - Manual via quickstart.md (GPT registration + 3 flow tests)
---

## Prompt

/sp.tasks (no args — current feature: 003-chatgpt-app)

## Response snapshot

Generated 16 tasks across 6 phases for Phase 3 ChatGPT App config.

- Phase 1 Setup: T001 (manifest.yaml)
- Phase 2 Foundational: T002 (openapi.yaml skeleton), T003 (system-prompt.md skeleton + Identity + Hard Rules)
- Phase 3 US1 Teaching: T004-T008 (3 openapi paths + 2 system-prompt sections)
- Phase 4 US2 Quiz: T009-T011 (2 openapi paths + quiz flow section)
- Phase 5 US3 Progress: T012-T013 (1 openapi path + progress flow section)
- Phase 6 Polish: T014-T016 (personality rules, YAML validation, full GPT registration + test)

T005+T006 parallel (different openapi paths), T009+T010 parallel, T002+T003 parallel.
All tasks include exact file paths and full content specifications for /sp.implement.

## Outcome

- ✅ Impact: 16 tasks ready for /sp.implement
- 🧪 Tests: Manual via quickstart.md — register GPT, verify 7-item checklist
- 📁 Files: specs/003-chatgpt-app/tasks.md
- 🔁 Next prompts: /sp.implement to author chatgpt-app/ files
- 🧠 Reflection: Tasks are content-authoring not code-writing — descriptions are detailed enough to produce the exact content needed; sp.implement should write the actual YAML and markdown

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): all 16 tasks have correct checkbox format, IDs, story labels, and file paths — PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): /sp.implement for 003-chatgpt-app
