---
id: 002
title: Auth Debugging and Fix Session
stage: general
date: 2026-05-03
surface: agent
model: claude-sonnet-4-6
feature: none
branch: 004-nextjs-web-app
user: Adan
command: "authentication issue and supabase is showing rls disabled"
labels: ["bugfix", "auth", "supabase", "rls", "debugging"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/middleware/auth.py
  - backend/routes/auth.py
  - backend/routes/chapters.py
  - backend/routes/progress.py
  - backend/routes/quizzes.py
  - backend/schema.sql
  - web/app/chapters/page.tsx
  - web/app/chapters/[id]/page.tsx
tests:
  - (manual smoke test — app working end-to-end after fixes)
---

## Prompt

Authentication issue after deployment. Supabase showing RLS disabled. Later: 401 on all protected endpoints after logout+login cycle.

## Response snapshot

Diagnosed and fixed a chain of four bugs:

1. **supabase-py v2 `.single()` raises on no rows** — replaced all `.single()` with `.maybe_single()` across auth middleware, chapters, quizzes, progress routes.
2. **Missing public.users row** — added auto-create in `get_current_user` when a valid Supabase Auth token exists but no profile row is found (handles orphaned auth users from failed registrations).
3. **Missing database schema** — generated `backend/schema.sql` and ran `seed.py` to create tables and populate 10 chapters + 50 quizzes.
4. **Service-role singleton corruption (root cause of logout+login 401s)** — `supabase.auth.sign_in_with_password()` on the shared client overwrites the internal `Authorization` header from `Bearer <service_role_key>` to `Bearer <user_jwt>`. After that all PostgREST queries run as `authenticated` role; with RLS enabled and no policies this returns nothing → 401 "User not found" on every subsequent request. Fixed by using an isolated `create_client()` just for login, keeping the singleton untouched.

Also decoupled `getProgress` from chapters page `Promise.all` so a missing/failing progress table never blocks chapter loading.

## Outcome

- ✅ Impact: App fully working — login, chapters, quiz, progress all functional. Logout+login cycle stable.
- 🧪 Tests: Manual smoke test confirmed by user ("our app is working allright now")
- 📁 Files: 8 files modified, 1 new file (schema.sql)
- 🔁 Next prompts: Run schema.sql in Supabase SQL Editor to create users/progress tables; demo recording
- 🧠 Reflection: The service-role singleton corruption is a non-obvious supabase-py v2 footgun. Any call to sign_in_with_password on a shared client must use an isolated instance.

## Evaluation notes (flywheel)

- Failure modes observed: DNS error (wrong Railway env var), .single() exception (supabase-py v2 breaking change), singleton auth state corruption (supabase-py sign_in side effect)
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
