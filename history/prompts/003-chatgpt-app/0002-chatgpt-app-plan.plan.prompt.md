---
id: 0002
title: ChatGPT App plan
stage: plan
date: 2026-04-28
surface: agent
model: claude-sonnet-4-6
feature: 003-chatgpt-app
branch: 003-chatgpt-app
user: Ad1nn
command: /sp.plan
labels: ["plan","chatgpt-app","phase-3","openapi","system-prompt","gpt-actions"]
links:
  spec: specs/003-chatgpt-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-chatgpt-app/plan.md
  - specs/003-chatgpt-app/research.md
  - specs/003-chatgpt-app/data-model.md
  - specs/003-chatgpt-app/quickstart.md
tests:
  - Manual verification via quickstart.md (GPT registration + 3 flow tests)
---

## Prompt

/sp.plan (no args — current feature: 003-chatgpt-app)

## Response snapshot

Generated full Phase 3 implementation plan. All 7 constitution principles PASS.

Key decisions:
- Config-only phase: 3 files under chatgpt-app/ (system-prompt.md, openapi.yaml, manifest.yaml)
- Auth: API Key / Bearer using demo JWT for hackathon — OAuth2 deferred
- 6 endpoints exposed in OpenAPI Actions schema; admin and hybrid endpoints explicitly excluded
- user_id passed explicitly by tutor (system prompt instructs asking student once)
- OpenAPI 3.1.0 format
- System prompt structured in 7 sections (identity, teach flow, quiz flow, progress flow, access control, personality, hard rules)

Artifacts: plan.md, research.md, data-model.md, quickstart.md

## Outcome

- ✅ Impact: Full plan ready for /sp.tasks — all decisions made, no blockers
- 🧪 Tests: Manual via quickstart.md — register GPT, test all 3 user story flows
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md
- 🔁 Next prompts: /sp.tasks then /sp.implement
- 🧠 Reflection: Phase 3 is the most demo-impactful phase — system prompt quality is the highest-leverage variable; investing time there pays off disproportionately

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): all 7 constitution principles PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): /sp.tasks for 003-chatgpt-app
