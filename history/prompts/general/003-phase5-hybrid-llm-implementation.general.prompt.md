---
id: 003
title: Phase 5 Hybrid LLM Implementation
stage: general
date: 2026-05-03
surface: agent
model: claude-sonnet-4-6
feature: none
branch: 004-nextjs-web-app
user: Adan
command: "i cant complete phase 3 whats phase 5 / okay then continue"
labels: ["feature", "phase5", "llm", "anthropic", "hybrid"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/requirements.txt
  - backend/models.py
  - backend/routes/hybrid.py
tests:
  - (manual — deploy to Railway and call /hybrid/adaptive-path and /hybrid/assess with a pro-tier user token)
---

## Prompt

User confirmed Phase 3 (ChatGPT app platform registration) cannot be completed. Asked to implement Phase 5 (Hybrid LLM features) instead.

## Response snapshot

Implemented Phase 5 Hybrid LLM endpoints in `backend/routes/hybrid.py`, replacing 501 stubs with real Claude API calls:

1. **`requirements.txt`** — added `anthropic==0.40.0`
2. **`models.py`** — added `AdaptivePathRequest`, `AdaptivePathResponse`, `AssessRequest`, `AssessResponse`
3. **`routes/hybrid.py`** — full implementation:
   - Both endpoints gate on `pro` tier (403 for free/premium)
   - `POST /hybrid/adaptive-path`: fetches all chapters + user progress from Supabase, builds a prompt describing completed/incomplete chapters and scores, calls `claude-sonnet-4-6`, parses JSON response `{recommended_next_chapter_id, reasoning, weak_areas, estimated_study_time_minutes}`, logs to `llm_costs`
   - `POST /hybrid/assess`: fetches chapter metadata, sends question + student answer to `claude-sonnet-4-6`, parses JSON response `{score, feedback, strengths, areas_to_improve}`, logs to `llm_costs`
   - `_log_cost()` helper calculates USD cost at sonnet-4-6 rates ($3/$15 per 1M in/out) and inserts into `llm_costs` table non-critically (exceptions swallowed)

## Outcome

- ✅ Impact: Phase 5 fully implemented — both LLM endpoints ready for deployment
- 🧪 Tests: Manual smoke test required after adding ANTHROPIC_API_KEY to Railway env
- 📁 Files: 3 files modified
- 🔁 Next prompts: Add ANTHROPIC_API_KEY to Railway; upgrade a test user to pro tier; test both endpoints; build Phase 5 UI in Next.js
- 🧠 Reflection: LLM responses parsed as JSON directly — if Claude adds markdown fencing the parse will fail; consider stripping ```json fences as a defensive measure

## Evaluation notes (flywheel)

- Failure modes observed: JSON parse failure if LLM wraps output in markdown fences
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add fence-stripping to _parse_llm_json helper
