---
id: 0001
title: Next.js web app spec
stage: spec
date: 2026-04-28
surface: agent
model: claude-sonnet-4-6
feature: 004-nextjs-web-app
branch: 004-nextjs-web-app
user: Ad1nn
command: /sp.specify
labels: ["spec","nextjs","phase-4","lms","dashboard","auth","quiz","progress"]
links:
  spec: specs/004-nextjs-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-nextjs-web-app/spec.md
  - specs/004-nextjs-web-app/checklists/requirements.md
tests:
  - Checklist validation: all 16 items PASS
---

## Prompt

/sp.specify lets go for phase 4

## Response snapshot

Spec authored for Phase 4 — Next.js Web App LMS Dashboard. Branch: `004-nextjs-web-app`.

**5 User Stories:**
- US1 (P1): Visitor discovers course and signs up — landing page hero, pricing tiers, sign-up form, auth redirect to `/dashboard`
- US2 (P1): Student reads course chapters — chapter list with tier badges, two-panel reading layout (sidebar + content), locked chapter overlay, prev/next navigation
- US3 (P1): Student takes a chapter quiz — one question at a time, colour feedback (green/correct, red/wrong), explanation text, final score screen
- US4 (P2): Student tracks progress — per-chapter table with status/score/attempts, overall stats (completion %, streak, avg score)
- US5 (P2): Student sees personalised dashboard — stat cards (chapters completed, streak, avg score) + continue learning card

**18 Functional Requirements** across authentication, chapter browsing, quiz, progress, and dashboard.

**5 Success Criteria** (all measurable and technology-agnostic):
- SC-001: New student can reach dashboard, open chapter, and start quiz in under 5 minutes
- SC-002: All pages load with visible content in under 3 seconds
- SC-003: Free-tier student cannot see locked chapter content (DOM-verifiable)
- SC-004: Complete quiz session completes without errors in 100% of test runs
- SC-005: Progress page accurately reflects backend's stored progress

**Checklist**: All 16 items PASS — no NEEDS CLARIFICATION markers, all requirements testable.

## Outcome

- ✅ Impact: Phase 4 spec complete — 5 user stories, 18 FRs, 5 success criteria, full edge cases and assumptions documented
- 🧪 Tests: Checklist validation PASS (16/16 items)
- 📁 Files: specs/004-nextjs-web-app/spec.md, specs/004-nextjs-web-app/checklists/requirements.md
- 🔁 Next prompts: `/sp.plan` to generate tech stack, data model, API contracts, and implementation plan
- 🧠 Reflection: Three P1 stories (auth, chapter reading, quiz) form a complete independent demo path — the P2 stories (progress, dashboard) layer on top and depend on quiz completion data

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Requirements checklist PASS (16/16)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Run /sp.plan to confirm tech stack aligns with constitution and Railway/Supabase constraints
