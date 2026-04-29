---
id: 001
title: Project Constitution Initial Ratification
stage: constitution
date: 2026-04-28
surface: agent
model: claude-sonnet-4-6
feature: none
branch: master
user: Ad1nn
command: /sp.constitution
labels: ["constitution","governance","principles","course-companion-fte"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-project-constitution-initial.constitution.prompt.md
tests:
  - none
---

## Prompt

start with writing a constitution for our entire project

## Response snapshot

Created the Course Companion FTE Constitution v1.0.0 at `.specify/memory/constitution.md`.

Seven core principles ratified:
1. Zero-LLM Backend (Phase 1 NON-NEGOTIABLE) — backend makes no LLM calls, all AI delegated to ChatGPT
2. Tier Enforcement at the Data Layer — server-side tier checks on every content request
3. JWT-First Authentication — all protected routes validate Bearer token via Supabase
4. Content Isolation — quiz correct_answer never returned by GET endpoints
5. Smallest Viable Diff — no speculative abstractions, only task-scoped changes
6. Build-Order Discipline — phases executed in order, Phase 5 is only cuttable phase
7. Observability at Every Write — all mutations persisted before response returned

Also includes Tech Stack & Constraints section and Development Workflow (spec → plan → tasks → implement → PHR).

## Outcome

- ✅ Impact: Project governance established; all future work must comply with 7 principles
- 🧪 Tests: No tests applicable (governance artifact)
- 📁 Files: .specify/memory/constitution.md (created/ratified)
- 🔁 Next prompts: /sp.specify to create feature specs for each phase
- 🧠 Reflection: Zero-LLM backend principle is the most critical — it determines hackathon scoring

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): run /sp.specify for Phase 1 backend feature
