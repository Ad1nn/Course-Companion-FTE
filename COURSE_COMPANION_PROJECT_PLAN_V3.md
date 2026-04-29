# Course Companion FTE — Project Plan
**Agentic AI Tutor | Hackathon IV | Solo | SDD with Claude Code**

---

## What We Are Building

A **Course Companion FTE (Full-Time Equivalent)** — a production-ready 24/7 AI tutor that teaches Agentic AI development. It replaces a human tutor at 99% lower cost by combining a deterministic FastAPI backend with ChatGPT's intelligence on the frontend.

The app has two completely separate frontends sharing one backend:

- **ChatGPT App** — student opens ChatGPT, finds our app, chats with it as a tutor. ChatGPT reads course content from our backend and does all the teaching. Our backend never generates a single word of explanation.
- **Next.js Web App** — a full LMS dashboard where students read chapters, take quizzes, and track progress without needing ChatGPT.

Both frontends hit the same FastAPI backend on Railway which reads and writes to Supabase.

---

## The Core Principle

**Phase 1 backend has ZERO LLM calls.**

```
Student asks "explain MCP"
      ↓
ChatGPT calls GET /chapters/4 on our backend
      ↓
Backend fetches raw text from Supabase, returns it
      ↓
ChatGPT reads that text and explains it to the student
      ↓
Our backend contributed zero words of explanation
```

The backend is a dumb data server. ChatGPT is the intelligent tutor. This keeps costs near zero and lets us scale to 100k users without linear cost increase. Violating this in Phase 1 is immediate hackathon disqualification.

---

## Tech Stack Decisions

```
Backend          → FastAPI (Python) on Railway
Database         → Supabase (PostgreSQL + Auth)
File storage     → Supabase Storage (NOT Cloudflare R2)
ChatGPT Frontend → OpenAI Apps SDK (config files, not code)
Web Frontend     → Next.js 14 App Router on Vercel
Styling          → Tailwind CSS
Auth             → Supabase Auth (email + password + JWT)
Phase 2 LLM      → Claude Sonnet API
Builder          → Claude Code (Spec-Driven Development)
```

---

## Course Content

**Topic:** Agentic AI Development sourced from Panaversity Agent Factory textbook (Part 6).

10 chapters, 3 textbook sub-pages of content each, 5 quiz questions each = 50 total quiz questions.

| # | Chapter Title | Textbook Source | Tier |
|---|--------------|----------------|------|
| 1 | Introduction to AI Agents | Ch 61 | free |
| 2 | OpenAI Agents SDK | Ch 62 | free |
| 3 | Anthropic Claude Agent SDK | Ch 65 | free |
| 4 | MCP Fundamentals | Ch 66 | premium |
| 5 | Advanced MCP Server Development | Ch 67 | premium |
| 6 | Agent Skills & MCP Code Execution | Ch 68 | premium |
| 7 | FastAPI for Agents | Ch 70 | premium |
| 8 | Vector Databases & RAG | Ch 73 | pro |
| 9 | Multi-Agent Reliability | Ch 69 | pro |
| 10 | Evals — Measuring Agent Performance | Ch 77 | pro |

---

## Freemium Tiers

```
free      → chapters 1, 2, 3 only     $0/month
premium   → chapters 1 through 7      $9.99/month
pro       → all 10 chapters           $19.99/month
           + adaptive learning path
           + LLM graded assessments
```

For the hackathon demo, tier upgrades are done manually via an admin API endpoint. No Stripe integration needed.

---

## Database Schema

```sql
create table chapters (
  id          serial primary key,
  title       text not null,
  description text,                    -- 2 sentence summary shown in chapter list
  content     text not null,           -- full text from 3 sub-pages concatenated
  order_num   integer not null unique,
  tier        text default 'free'      -- 'free' | 'premium' | 'pro'
);

create table quizzes (
  id             serial primary key,
  chapter_id     integer references chapters(id),
  question       text not null,
  option_a       text not null,
  option_b       text not null,
  option_c       text not null,
  option_d       text not null,
  correct_answer text not null,        -- 'A' | 'B' | 'C' | 'D'
  explanation    text not null,        -- shown after answer submitted
  order_num      integer
);

create table users (
  id         uuid references auth.users primary key,
  email      text not null,
  tier       text default 'free',      -- 'free' | 'premium' | 'pro'
  created_at timestamp default now()
);

create table progress (
  id           serial primary key,
  user_id      uuid references users(id),
  chapter_id   integer references chapters(id),
  completed    boolean default false,
  score        integer,                -- percentage 0-100
  attempts     integer default 0,
  last_accessed timestamp default now(),
  completed_at  timestamp,
  unique(user_id, chapter_id)
);

create table llm_costs (
  id         serial primary key,
  user_id    uuid references users(id),
  feature    text,                     -- 'adaptive_path' | 'assessment'
  tokens_in  integer,
  tokens_out integer,
  cost_usd   numeric(10,6),
  created_at timestamp default now()
);
```

---

## API Endpoints

**Base URL:** `https://course-companion.railway.app`

All protected routes require `Authorization: Bearer <JWT>` header.

### Chapters

```
GET /chapters
Returns all chapters as a list. Titles and descriptions only.
No content field — content is heavy, loaded on demand.
Includes tier field so frontend can show lock icons.

GET /chapters/{id}
Returns one chapter with full content.
Checks user tier first. Returns 403 if chapter tier > user tier.
403 response includes: required_tier, user_tier, message.

GET /chapters/{id}/next
Returns the next chapter object.
Skips chapters the user cannot access.

GET /chapters/{id}/prev
Returns the previous chapter object.

GET /search?q={keyword}
Full text search across chapter titles and content.
Returns: id, title, excerpt (snippet around match), tier.
Max 5 results.
```

### Quizzes

```
GET /quizzes/{chapter_id}
Returns all 5 questions for a chapter.
NEVER includes correct_answer field.
Returns: id, question, option_a, option_b, option_c, option_d, order_num.

POST /quizzes/{quiz_id}/submit
Body: { "user_id": "uuid", "answer": "B" }
Compares answer to correct_answer in database.
If all 5 questions answered: calculates score, saves to progress table.
Returns: correct (bool), correct_answer, explanation, score (if final question).
```

### Progress

```
GET /progress/{user_id}
Returns complete progress object:
{
  tier, streak_days, avg_score, chapters_completed,
  chapters: [{ chapter_id, title, completed, score, attempts }]
}

streak_days: count of consecutive calendar days where at least
one chapter was completed_at. Resets if no activity for 24+ hours.

PUT /progress/{user_id}
Body: { "chapter_id": 3, "completed": true, "score": 80 }
Upserts into progress table.
```

### Access

```
GET /access/check?chapter_id={id}
Checks authenticated user's tier against chapter's tier requirement.
Returns: { "allowed": true }
or: { "allowed": false, "required_tier": "premium", "user_tier": "free" }

POST /admin/upgrade
Body: { "user_id": "uuid", "tier": "premium" }
Requires ADMIN_SECRET header for security.
For demo purposes only. Not exposed in ChatGPT App.
```

### Auth

```
POST /auth/register
Creates Supabase Auth user.
Then inserts row into users table with tier = 'free'.
Returns: { user_id, email, tier }

POST /auth/login
Validates credentials via Supabase Auth.
Returns: { access_token, user_id, tier }
```

### Phase 5 Hybrid (Pro tier only, isolated routes)

```
POST /hybrid/adaptive-path
Body: { "user_id": "uuid" }
Reads user's full progress from Supabase.
Builds prompt: scores per chapter, completion order, attempts.
Calls Claude Sonnet API.
Returns: {
  recommended_next_chapter_id,
  reasoning,
  weak_areas: [],
  estimated_study_time_minutes
}
Logs to llm_costs table.
Returns 403 for free and premium users.

POST /hybrid/assess
Body: { "user_id": "uuid", "chapter_id": 4, "question": "...", "answer": "..." }
Sends student's free-form written answer to Claude Sonnet with a rubric.
Returns: {
  score (0-100),
  feedback,
  strengths: [],
  areas_to_improve: []
}
Logs to llm_costs table.
Returns 403 for free and premium users.
```

---

## ChatGPT App

Three config files. Not a website.

```
chatgpt-app/
├── system-prompt.md
├── openapi.yaml
└── manifest.yaml
```

### System Prompt Behavior

The system prompt defines exactly how ChatGPT behaves as our tutor.

**Teaching flow:**
- Student asks about a topic → ChatGPT calls `/search` to find the right chapter → calls `/chapters/{id}` → explains using ONLY that content
- If topic not found in search → respond: "That topic isn't covered in this course"
- Never explain from general knowledge, always fetch first

**Quiz flow:**
- Student says "quiz me" → ChatGPT calls `/quizzes/{chapter_id}`
- Presents ONE question at a time
- Waits for student answer
- Calls `/quizzes/{quiz_id}/submit` with the answer
- If correct → celebrate warmly, show explanation
- If wrong → be encouraging, show correct answer and explanation
- After all 5 questions → calls `/progress/{user_id}` PUT to save score → shows final score
- Never show all questions at once

**Progress flow:**
- Student asks "how am I doing" → calls `/progress/{user_id}` → presents stats encouragingly
- Suggest next chapter based on what is not yet completed

**Access flow:**
- Call `/access/check` BEFORE every `/chapters/{id}` call
- If denied → tell student warmly: "Chapter [X] is available on the Premium plan. You can upgrade at [url]"
- Never partially reveal locked content

**Personality:**
- Warm, patient, encouraging
- Adjusts explanation complexity to match student's apparent level
- Celebrates correct answers
- Frames wrong answers as learning opportunities
- Never condescending

---

## Next.js Web App — Pages

### Landing Page `/`
- Navbar: Logo left, Login + Start Free buttons right
- Hero: large heading "Learn Agentic AI. The right way." + subheading + "Start Learning Free" CTA button
- 3 feature highlights: "10 Chapters", "50 Quizzes", "24/7 Available"
- Pricing section: 3 tier cards (Free / Premium / Pro) with feature lists and CTA buttons
- Footer

### Login Page `/login`
- Supabase Auth UI component
- Email + password fields
- "Don't have an account? Sign up" link
- On success → redirect to `/dashboard`

### Sign Up Page `/signup`
- Supabase Auth UI component
- Email + password + confirm password
- On success → backend creates user row with tier=free → redirect to `/dashboard`

### Dashboard `/dashboard` (protected)
- Welcome: "Welcome back, [name]"
- 3 stat cards in a row:
  - Chapters Completed: "3 / 10"
  - Day Streak: "🔥 5 days"
  - Average Score: "78%"
- "Continue Learning" card: shows last accessed chapter title, progress bar, "Continue →" button
- If no progress yet: shows "Start with Chapter 1" card

### Chapters List `/chapters` (protected)
- Page title: "Course Chapters"
- Grid of 10 chapter cards
- Each card shows: chapter number, title, description, tier badge, completion status
- Free chapters: clickable
- Locked chapters: padlock icon overlay, clicking shows upgrade prompt modal
- Completed chapters: green checkmark badge

### Chapter Reading Page `/chapters/[id]` (protected)
- Fixed sidebar (240px):
  - App logo at top
  - List of all 10 chapters
  - Current chapter highlighted with violet left border
  - Completed chapters show checkmark
  - Locked chapters show padlock and are not clickable
- Content area:
  - Chapter title as H1
  - Tier badge
  - Full chapter content rendered as markdown
  - Bottom nav: "← Previous Chapter" left, "Next Chapter →" right
  - "Start Quiz" button above bottom nav
  - If chapter is locked: show blurred content with upgrade CTA overlay

### Quiz Page `/quiz/[chapter_id]` (protected)
- Header: "Quiz — [Chapter Title]"
- Progress indicator: "Question 2 of 5" + progress bar
- Question text as H2
- 4 option cards in a 2×2 grid:
  - Default: white card with border
  - Hovered: violet border
  - Selected: violet background light
- "Submit Answer" button (disabled until option selected)
- After submit:
  - Correct: card turns green, show explanation below
  - Wrong: selected card turns red, correct card turns green, show explanation
  - "Next Question →" button appears
- After question 5 (final screen):
  - Score: large "4 / 5 Correct" display
  - Percentage: "80%"
  - "Back to Chapter" button
  - "Retake Quiz" button
  - Progress automatically saved

### Progress Page `/progress` (protected)
- Page title: "Your Progress"
- Overall stats row: completion %, streak, avg score
- Overall progress bar: violet fill, shows X/10 chapters
- Chapter table: title, tier badge, status (completed/in progress/locked), score, attempts
- Completed rows show green checkmark and score
- Locked rows show padlock
- "🔥 [N] Day Streak" card
- "Best Score" highlight card

---

## UI Design System

```
Font:            Inter (Google Fonts)
Primary:         #7C3AED  violet-600   buttons, links, progress bars, active states
Primary Light:   #EDE9FE  violet-100   hover backgrounds, badges
Primary Dark:    #5B21B6  violet-800   button hover
Background:      #FFFFFF               main content
Surface:         #FAFAFA               sidebar, cards, inputs
Border:          #E5E7EB  gray-200     card borders, dividers
Text Primary:    #111827  gray-900     headings, body
Text Secondary:  #6B7280  gray-500     captions, metadata
Success:         #059669  emerald-600  correct, completed
Error:           #DC2626  red-600      wrong answers
Warning:         #D97706  amber-600    streak, highlights

Layout:
  Navbar:  h-16, border-b border-gray-200, sticky top-0
  Sidebar: w-60, fixed, full height, border-r border-gray-200
  Content: ml-60, p-12, max-w-3xl

Components:
  Cards:       bg-white rounded-xl border border-gray-200 shadow-sm
  Buttons:     rounded-lg px-4 py-2 font-medium
  Sidebar item active:  bg-violet-50 text-violet-700 border-l-4 border-violet-600
  Sidebar item locked:  text-gray-400 opacity-60 cursor-not-allowed
  Tier badge free:      bg-gray-100 text-gray-600
  Tier badge premium:   bg-violet-100 text-violet-700
  Tier badge pro:       bg-amber-100 text-amber-700
  Progress bar track:   bg-gray-200 rounded-full h-2
  Progress bar fill:    bg-violet-600 rounded-full h-2
```

---

## Auth Flow

```
Signup:
Student submits email + password
→ Supabase Auth creates user in auth.users
→ Backend inserts into users table (tier = 'free')
→ JWT token returned
→ Stored in browser (Supabase handles this)
→ Redirect to /dashboard

Login:
Student submits email + password
→ Supabase Auth validates
→ JWT token returned and stored
→ Redirect to /dashboard

Every protected API call:
→ Frontend sends: Authorization: Bearer <token>
→ Backend calls supabase.auth.get_user(token)
→ Gets user_id → looks up tier in users table
→ Proceeds or returns 403
```

---

## Deployment

```
Backend → Railway
  root dir: /backend
  start:    uvicorn main:app --host 0.0.0.0 --port $PORT
  env vars: SUPABASE_URL
            SUPABASE_ANON_KEY
            SUPABASE_SERVICE_KEY
            ADMIN_SECRET
            ANTHROPIC_API_KEY  (Phase 5 only)

Web App → Vercel
  root dir: /web
  env vars: NEXT_PUBLIC_SUPABASE_URL
            NEXT_PUBLIC_SUPABASE_ANON_KEY
            NEXT_PUBLIC_API_URL
```

---

## Repo Structure

```
course-companion-fte/
├── CLAUDE.md
├── SPEC.md
├── PROJECT_PLAN.md
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── middleware/
│   │   └── auth.py
│   ├── routes/
│   │   ├── chapters.py
│   │   ├── quizzes.py
│   │   ├── progress.py
│   │   ├── access.py
│   │   ├── auth.py
│   │   ├── admin.py
│   │   └── hybrid.py
│   └── requirements.txt
├── web/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── login/page.tsx
│   │   ├── signup/page.tsx
│   │   ├── dashboard/page.tsx
│   │   ├── chapters/page.tsx
│   │   ├── chapters/[id]/page.tsx
│   │   ├── quiz/[chapter_id]/page.tsx
│   │   └── progress/page.tsx
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── Sidebar.tsx
│   │   ├── ChapterCard.tsx
│   │   ├── QuizQuestion.tsx
│   │   ├── ProgressBar.tsx
│   │   ├── StatCard.tsx
│   │   ├── TierBadge.tsx
│   │   └── LockedOverlay.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   └── supabase.ts
│   └── middleware.ts
└── chatgpt-app/
    ├── system-prompt.md
    ├── openapi.yaml
    └── manifest.yaml
```

---

## Build Order

```
Phase 0 → CLAUDE.md + SPEC.md + GitHub repo + Supabase + Railway + Vercel accounts
Phase 1 → FastAPI backend, all endpoints, deployed on Railway
Phase 2 → Content: 10 chapters + 50 quizzes inserted into Supabase
Phase 3 → ChatGPT App: 3 config files registered on ChatGPT platform
Phase 4 → Next.js web app, all pages, deployed on Vercel
Phase 5 → Hybrid features (cut if time is short)
Phase 6 → README, architecture diagram, cost doc, demo video, submit
```

## If Time Runs Out

```
Never cut → Phase 1 + Phase 3   (45 hackathon points)
Never cut → Phase 4             (30 hackathon points)
Cut first → Phase 5             (20 hackathon points)
```

---

## Commit Convention

```
feat:   new feature or endpoint
fix:    bug fix
chore:  config, setup, env, deployment
test:   adding or fixing tests
docs:   readme, diagrams, cost analysis
```

---

*Course Companion FTE | Hackathon IV | Solo | April 2026*
