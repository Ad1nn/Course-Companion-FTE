# Quickstart & Integration Scenarios: Next.js Web App

**Date**: 2026-04-28 | **Branch**: `004-nextjs-web-app`

---

## Prerequisites

- Node.js 18+ installed
- Backend (Phase 1) deployed and accessible at `NEXT_PUBLIC_API_BASE_URL`
- Supabase project with `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- At least 3 chapters and 15 quiz questions seeded (Phase 2 complete)

## Local Development Setup

```bash
cd web-app
npm install
cp .env.example .env.local
# Fill in .env.local:
# NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
# NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
# NEXT_PUBLIC_API_BASE_URL=https://course-companion.railway.app
npm run dev
# → http://localhost:3000
```

---

## Scenario 1 — New User Sign-up and Reach Dashboard

**Goal**: Verify US1 auth flow end-to-end.

```
1. Open http://localhost:3000
2. Verify: hero section, 3 feature highlights, pricing cards (Free/Premium/Pro), footer visible
3. Click "Start Learning Free" CTA
4. Fill: email=test@example.com, password=Test1234!
5. Click "Create Account"
6. Verify: redirected to /dashboard
7. Verify: welcome message shows email, stat cards show "0/10 chapters", "0 day streak", "0% avg"
8. Verify: "Start with Chapter 1" card shown (not "Continue Learning")
```

**Expected**: Clean redirect to /dashboard, zero-state stats, no errors in console.

---

## Scenario 2 — View Chapter List and Open Chapter 1

**Goal**: Verify US2 chapter list and free-tier chapter reading.

```
1. Navigate to /chapters
2. Verify: 10 chapter cards shown, each with title, description, tier badge
3. Verify: chapters 1–3 show green "Free" badge
4. Verify: chapters 4–7 show violet "Premium" badge
5. Verify: chapters 8–10 show amber "Pro" badge
6. Click chapter 1 card
7. Verify: two-panel layout — left sidebar lists all 10 chapters, chapter 1 highlighted
8. Verify: content area shows formatted text (headings, paragraphs)
9. Verify: "Start Quiz" button visible at bottom
10. Click "Next Chapter"
11. Verify: navigated to /chapters/2
```

**Expected**: All 10 chapters listed, content renders from backend, navigation works.

---

## Scenario 3 — Locked Chapter (Free Tier User)

**Goal**: Verify SC-003 content isolation for locked chapters.

```
1. Log in as free-tier user (default)
2. Navigate to /chapters/4
3. Verify: locked overlay shown, NOT chapter content
4. Verify: upgrade prompt mentions "Premium plan"
5. Open browser DevTools → Elements tab
6. Search DOM for any text from chapter 4 content
7. Verify: chapter content string is ABSENT from the DOM
```

**Expected**: Zero content in DOM. Overlay shown with tier info.

---

## Scenario 4 — Complete a Quiz

**Goal**: Verify US3 quiz flow.

```
1. Navigate to /chapters/1, click "Start Quiz"
2. Verify: /quiz/1 loads, "Question 1 of 5" shown with progress bar
3. Verify: 4 option cards shown, "Submit Answer" button disabled
4. Click any option card
5. Verify: "Submit Answer" button becomes enabled
6. Click "Submit Answer"
7. Verify: selected card turns green (correct) or red (wrong)
8. Verify: correct answer highlighted green
9. Verify: explanation text appears below options
10. Click "Next Question →"
11. Repeat for questions 2–5
12. After question 5: verify score screen "N / 5 Correct — X%" appears
13. Verify: "Back to Chapter" and "Retake Quiz" buttons present
14. Click "Back to Chapter" → verify navigated to /chapters/1
```

**Expected**: One question at a time, correct colour feedback, score matches backend response.

---

## Scenario 5 — Progress Page After Quiz

**Goal**: Verify US4 progress tracking.

```
1. After completing quiz from Scenario 4:
2. Navigate to /progress
3. Verify: overall stats show correct values:
   - Completion: 1/10 (10%)
   - Streak: 1 day
   - Average score: [score from quiz]%
4. Verify: chapter 1 row shows green checkmark, correct score %, "1 attempt"
5. Verify: chapters 2–10 show "not started"
6. Verify: locked chapters (4–10 for free tier) show padlock icon
```

**Expected**: Progress data matches what backend returned during quiz submission.

---

## Scenario 6 — Dashboard "Continue Learning" After Progress

**Goal**: Verify US5 dashboard with existing progress.

```
1. After Scenario 4 (quiz complete):
2. Navigate to /dashboard
3. Verify: stat cards updated — "1/10 chapters", "1 day streak", "[score]% avg"
4. Verify: "Continue Learning" card shown (not "Start with Chapter 1")
5. Verify: card shows chapter 2 title (next after most recently completed)
6. Click "Continue →"
7. Verify: navigated to /chapters/2
```

**Expected**: Dashboard reflects live progress; continue card links to correct next chapter.

---

## Scenario 7 — Unauthenticated Access Protection

**Goal**: Verify FR-003 redirect behaviour.

```
1. Sign out (or open incognito window)
2. Attempt to navigate to /dashboard
3. Verify: redirected to /login (not shown dashboard content)
4. Attempt to navigate to /chapters/1
5. Verify: redirected to /login
6. Attempt to navigate to /quiz/1
7. Verify: redirected to /login
8. Attempt to navigate to /progress
9. Verify: redirected to /login
```

**Expected**: All protected routes redirect to /login without flashing content.

---

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | `https://abc.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key (public) | `eyJ...` |
| `NEXT_PUBLIC_API_BASE_URL` | FastAPI backend URL | `https://course-companion.railway.app` |

---

## Known Limitations (Hackathon Scope)

- Partial quiz answers lost on page refresh — acceptable per spec edge case
- Mobile layout is best-effort only — desktop (1280px+) is the demo target
- No password reset or email verification flow
- Tier upgrade done via admin endpoint only — no UI
