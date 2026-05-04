# Course Companion FTE

**A production-ready AI tutor for Agentic AI development.**

Built for Hackathon IV using Spec-Driven Development with Claude Code.

---

## What It Is

Course Companion is a full LMS (Learning Management System) that teaches Agentic AI development through 10 structured chapters and 50 quizzes. It has two frontends sharing one backend:

- **Next.js Web App** — students read chapters, take quizzes, track progress, and use AI-powered learning features
- **FastAPI Backend** — serves all content and handles auth, progress, and LLM features

The backend has zero LLM calls for standard features. GPT-4o is only invoked for the two Pro-tier hybrid features.

---

## Live Demo

| Service | URL |
|---|---|
| Web App | Vercel deployment |
| Backend API | Railway deployment |
| API Docs | `<railway-url>/docs` |

---

## Features

### All Users
- 10 chapters on Agentic AI development (free/premium/pro gating)
- 5 multiple-choice quiz questions per chapter with instant feedback
- Progress dashboard — completion %, day streak, average score
- Full-text chapter search
- Dark / light mode

### Pro Tier Only
- **AI Adaptive Learning Path** — GPT-4o analyses your progress and recommends exactly what to study next, with reasoning, weak areas, and estimated study time
- **AI-Graded Assessments** — two modes:
  - AI generates a chapter question → you answer → AI grades it
  - You explain a concept freely → AI assesses your understanding

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, uvicorn |
| Database | Supabase (PostgreSQL + Auth) |
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS |
| LLM | OpenAI GPT-4o (Pro tier only) |
| Backend hosting | Railway |
| Frontend hosting | Vercel |

---

## Project Structure

```
course-companion-fte/
├── backend/
│   ├── main.py               # FastAPI app + router registration
│   ├── database.py           # Supabase client singleton
│   ├── models.py             # Pydantic request/response models
│   ├── middleware/
│   │   └── auth.py           # JWT verification via Supabase Auth
│   └── routes/
│       ├── auth.py           # register, login, upgrade-tier
│       ├── chapters.py       # list, get, next, prev
│       ├── quizzes.py        # questions, submit answer
│       ├── progress.py       # get, update progress
│       ├── access.py         # tier-based access check
│       ├── admin.py          # manual tier upgrade (demo)
│       ├── search.py         # full-text search
│       └── hybrid.py         # GPT-4o adaptive path, assess, generate-question
├── web/
│   ├── app/                  # Next.js App Router pages
│   │   ├── page.tsx          # Landing page
│   │   ├── dashboard/        # Progress overview
│   │   ├── chapters/         # Chapter list + reading pages
│   │   ├── quiz/             # Quiz flow
│   │   ├── progress/         # Detailed progress
│   │   ├── adaptive/         # AI learning path (Pro)
│   │   ├── assess/           # AI assessment (Pro)
│   │   ├── profile/          # Account + logout
│   │   └── upgrade/          # Self-service tier upgrade
│   ├── components/           # Navbar, Sidebar, Cards, etc.
│   └── lib/                  # API client, auth helpers
├── backend/schema.sql        # Supabase table definitions + RLS
├── backend/seed.py           # Seeds 10 chapters + 50 quizzes
├── railway.toml              # Railway deployment config
└── nixpacks.toml             # Nixpacks build config
```

---

## API Endpoints

All protected routes require `Authorization: Bearer <JWT>`.

```
POST   /auth/register           Create account
POST   /auth/login              Login, returns JWT
POST   /auth/upgrade-tier       Self-service tier upgrade (demo)

GET    /chapters                List all chapters
GET    /chapters/{id}           Get chapter with full content
GET    /access/check            Check tier access for a chapter

GET    /quizzes/{chapter_id}    Get 5 questions (no correct answers)
POST   /quizzes/{id}/submit     Submit answer, get feedback + score

GET    /progress/{user_id}      Full progress with streak + avg score
PUT    /progress/{user_id}      Update chapter progress

GET    /search?q={keyword}      Full-text search across chapters

POST   /hybrid/adaptive-path    AI recommended next chapter (Pro)
POST   /hybrid/assess           AI-graded free-form answer (Pro)
POST   /hybrid/generate-question  AI-generated chapter question (Pro)
```

---

## Database Schema

5 tables in Supabase with RLS enabled:

```
chapters    — 10 rows, tiered content
quizzes     — 50 rows, 5 per chapter
users       — links to Supabase Auth, stores tier
progress    — per-user per-chapter completion + score
llm_costs   — token usage logging for Pro features
```

---

## Local Development

**Backend**
```bash
cd backend
pip install -r requirements.txt
# Create .env with SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY, ADMIN_SECRET
uvicorn main:app --reload
```

**Frontend**
```bash
cd web
npm install
# Create .env.local with NEXT_PUBLIC_API_BASE_URL
npm run dev
```

**Seed the database**
```bash
cd backend
python seed.py
```

---

## Environment Variables

**Backend (Railway)**
```
SUPABASE_URL
SUPABASE_SERVICE_KEY
OPENAI_API_KEY
ADMIN_SECRET
```

**Frontend (Vercel)**
```
NEXT_PUBLIC_API_BASE_URL
```

---

## Freemium Tiers

| Tier | Price | Chapters | AI Features |
|---|---|---|---|
| Free | $0 | 1–3 | — |
| Premium | $29/mo | 1–7 | — |
| Pro | $49/mo | 1–10 | Adaptive path + AI assessments |

---

## Course Content

10 chapters sourced from the Panaversity Agent Factory textbook (Part 6):

1. Introduction to AI Agents
2. OpenAI Agents SDK
3. Anthropic Claude Agent SDK
4. MCP Fundamentals
5. Advanced MCP Server Development
6. Agent Skills & MCP Code Execution
7. FastAPI for Agents
8. Vector Databases & RAG
9. Multi-Agent Reliability
10. Evals — Measuring Agent Performance

---

*Hackathon IV · Solo · April–May 2026*
