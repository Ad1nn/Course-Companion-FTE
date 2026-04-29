# Implementation Plan: Next.js Web App — LMS Dashboard

**Branch**: `004-nextjs-web-app` | **Date**: 2026-04-28 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/004-nextjs-web-app/spec.md`

## Summary

Build a client-side Next.js 14 App Router web application that provides a complete LMS dashboard for the Course Companion Agentic AI course. The frontend authenticates via Supabase Auth (JWT), calls the existing FastAPI backend on Railway for all data, and renders five core pages: landing, dashboard, chapter list, chapter reader, quiz, and progress. Supabase Auth manages session tokens transparently; the app passes the JWT as a Bearer header to all protected API calls.

## Technical Context

**Language/Version**: TypeScript 5 / Next.js 14 (App Router)  
**Primary Dependencies**: `next@14`, `react@18`, `@supabase/supabase-js`, `@supabase/ssr`, `tailwindcss@3`, `react-markdown` (chapter content rendering)  
**Storage**: Supabase PostgreSQL — accessed only through FastAPI backend on Railway (no direct DB calls from frontend)  
**Testing**: Manual / smoke-test only — hackathon scope (no automated test suite for frontend)  
**Target Platform**: Modern browser (Chrome 120+, Firefox 120+) deployed on Vercel  
**Project Type**: Web application (frontend only — backend is Phase 1, already deployed)  
**Performance Goals**: All pages load with visible content in under 3 seconds on standard connection (SC-002)  
**Constraints**: Desktop-first (≥1280px), CSR-dominant SPA, no SEO requirement, no payment UI  
**Scale/Scope**: Hackathon demo — single-digit concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Zero-LLM Backend | ✅ PASS | Web app calls FastAPI only — no LLM calls from frontend |
| II. Tier Enforcement at Data Layer | ✅ PASS | Backend enforces tier on `/chapters/{id}`; frontend shows overlay only |
| III. JWT-First Authentication | ✅ PASS | Supabase Auth manages JWT; token from `session.access_token` sent as Bearer |
| IV. Content Isolation — Answers Never Leak | ✅ PASS | Quiz questions fetched without `correct_answer`; answer revealed only from submit response |
| V. Smallest Viable Diff | ✅ PASS | New `web-app/` directory; zero changes to backend or ChatGPT App |
| VI. Build-Order Discipline | ✅ PASS | Phase 1 (backend) deployed and smoke-tested; Phase 4 begins |
| VII. Observability at Every Write | ✅ PASS | Quiz submission calls `POST /quizzes/{id}/submit` which persists to Supabase |

All 7 principles PASS. No gate violations.

## Project Structure

### Documentation (this feature)

```text
specs/004-nextjs-web-app/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── api-calls.md
└── tasks.md             # Phase 2 output (/sp.tasks — not created here)
```

### Source Code (repository root)

```text
web-app/
├── src/
│   ├── app/                        # Next.js 14 App Router
│   │   ├── (public)/               # Unauthenticated routes (no auth check)
│   │   │   ├── page.tsx            # Landing page (/)
│   │   │   ├── login/
│   │   │   │   └── page.tsx        # Login form
│   │   │   └── signup/
│   │   │       └── page.tsx        # Sign-up form
│   │   ├── (protected)/            # Auth-gated routes (redirects to /login)
│   │   │   ├── layout.tsx          # Protected layout (session check)
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx        # Dashboard: stat cards + continue card
│   │   │   ├── chapters/
│   │   │   │   ├── page.tsx        # Chapter list: 10 chapter cards
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx    # Chapter reader: sidebar + content + quiz CTA
│   │   │   ├── quiz/
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx    # Quiz: question-by-question + score screen
│   │   │   └── progress/
│   │   │       └── page.tsx        # Progress: stats + per-chapter table
│   │   ├── layout.tsx              # Root layout: fonts, Tailwind, metadata
│   │   └── globals.css             # Tailwind base imports
│   ├── components/
│   │   ├── ui/                     # Primitive reusable components
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Badge.tsx           # Tier badge (free/premium/pro)
│   │   │   └── ProgressBar.tsx
│   │   ├── nav/
│   │   │   ├── Navbar.tsx          # Top navigation with login/logout
│   │   │   └── ChapterSidebar.tsx  # Left sidebar for chapter reader
│   │   ├── chapter/
│   │   │   ├── ChapterCard.tsx     # Card on chapter list page
│   │   │   ├── ChapterContent.tsx  # Rendered markdown content area
│   │   │   └── LockedOverlay.tsx   # Blur + upgrade prompt for locked chapters
│   │   ├── quiz/
│   │   │   ├── QuestionCard.tsx    # Single question + 4 option cards
│   │   │   ├── AnswerOption.tsx    # Option card (default/selected/correct/wrong)
│   │   │   └── ScoreScreen.tsx     # Final score display + action buttons
│   │   └── dashboard/
│   │       ├── StatCard.tsx        # Individual stat card
│   │       └── ContinueCard.tsx    # Continue learning / start chapter 1 card
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts           # Browser Supabase client (singleton)
│   │   │   └── server.ts           # Server-side Supabase client (SSR cookies)
│   │   └── api.ts                  # All FastAPI backend call functions
│   └── middleware.ts                # Route protection: redirects /protected/* to /login
├── public/
│   └── logo.svg
├── tailwind.config.ts               # violet primary colour
├── next.config.ts
├── tsconfig.json
└── package.json
```

**Structure Decision**: Single web-app directory at repo root, keeping backend/ and web-app/ as sibling directories. App Router route groups `(public)` and `(protected)` enforce auth boundaries at the routing layer. Middleware handles redirects server-side.

## Key Architecture Decisions

### Auth Strategy: Supabase Auth with SSR
- Use `@supabase/ssr` for Next.js middleware and server components
- Browser client (`@supabase/supabase-js`) for client components
- Session token auto-managed by Supabase client (stored in cookies via SSR)
- `session.access_token` injected as `Authorization: Bearer` header for every FastAPI call
- Middleware at `src/middleware.ts` protects all `/(protected)` routes

### API Integration: FastAPI Backend Only
- All data fetched from Railway FastAPI backend (no direct Supabase queries from frontend)
- `src/lib/api.ts` exports typed async functions: `getChapters()`, `getChapter(id)`, `checkAccess(id)`, `getQuizQuestions(id)`, `submitAnswer(quizId, answer, userId)`, `getProgress(userId)`
- Bearer token passed in every request header
- Error handling: network errors → toast/error state; 403 → tier locked overlay; 404 → not found message

### Quiz State Machine (Client-Side)
- `useState` manages quiz flow: `questions[]`, `currentIndex`, `selectedAnswer`, `submitted`, `result`, `score`
- No external state library (Zustand/Redux) — quiz is contained in a single page component
- Quiz answers are NOT stored locally between refreshes (acceptable for hackathon)

### Chapter Content Rendering
- Chapter `content` field is Markdown text — rendered with `react-markdown`
- Code blocks styled with Tailwind prose classes
- Content never rendered for locked chapters (component not mounted, not just hidden)

### Styling
- Tailwind CSS with violet primary colour (`violet-600` / `violet-700`)
- No CSS-in-JS, no styled-components (constitution requirement)
- Responsive: desktop-first at 1280px; sidebar collapses below md breakpoint (best-effort)

## Complexity Tracking

No constitution violations — no complexity tracking required.
