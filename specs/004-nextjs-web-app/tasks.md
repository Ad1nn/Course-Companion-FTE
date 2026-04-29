# Tasks: Next.js Web App — LMS Dashboard

**Input**: Design documents from `/specs/004-nextjs-web-app/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/api-calls.md ✅, quickstart.md ✅

**Organization**: Tasks grouped by user story. No tests requested — implementation tasks only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no shared dependencies)
- **[Story]**: Maps to user story from spec.md (US1–US5)
- All paths relative to repo root

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Bootstrap the Next.js 14 project with all dependencies and base config.

- [X] T001 Create web/package.json with next@14, react@18, react-markdown, @tailwindcss/typography
- [X] T002 Create web/next.config.ts, web/postcss.config.js, web/tsconfig.json
- [X] T003 [P] Create web/tailwind.config.ts — extend theme with violet primary colour and enable typography plugin
- [X] T004 [P] Create web/.env.example with NEXT_PUBLIC_API_BASE_URL
- [X] T005 [P] Create web/.gitignore covering: node_modules/, .next/, .env.local, *.log, dist/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared infrastructure that MUST be complete before any user story can be built.

**⚠️ CRITICAL**: All user story work blocks on this phase.

- [X] T006 Create web/lib/auth.ts — localStorage auth session helpers (getSession, setSession, clearSession) with cookie sync for middleware
- [X] T007 Create web/lib/useAuth.ts — useAuth() hook: reads session, redirects to /login if missing
- [X] T008 Create web/middleware.ts — Next.js middleware matching protected routes, reads cc_auth cookie, redirects unauthenticated requests to /login
- [X] T009 Create web/lib/api.ts — centralized FastAPI client: ApiError class, 6 typed async functions + apiRegister/apiLogin auth functions
- [X] T010 Create web/app/layout.tsx — root layout with Inter font, Tailwind globals import, metadata
- [X] T011 Create web/app/globals.css — Tailwind @tailwind directives
- [X] T012 [P] Create web/components/TierBadge.tsx — tier badge (free=green, premium=violet, pro=amber)
- [X] T013 [P] Create web/components/ProgressBar.tsx — horizontal progress bar with value (0-100) and optional label
- [X] T014 [P] Create web/components/StatCard.tsx — stat card with label, value, optional icon
- [X] T015 [P] Create web/components/QuizQuestion.tsx — full quiz question card with progress bar, 4 answer options, submit button, explanation
- [X] T016 Create web/components/Navbar.tsx — top navigation: logo + conditional login/logout links based on localStorage session

**Checkpoint**: Foundation complete — run `npm install && npm run dev` in web/, verify app starts at localhost:3000.

---

## Phase 3: User Story 1 — Visitor Discovers Course and Signs Up (Priority: P1) 🎯 MVP

**Goal**: Landing page → sign-up → redirect to /dashboard. Login returns existing users to /dashboard. Protected routes redirect unauthenticated users to /login.

**Independent Test** (quickstart.md Scenario 1 + 7):
1. Open localhost:3000 — verify hero, feature highlights, pricing cards (Free/Premium/Pro), footer
2. Click "Start Learning Free" → fill email+password → submit → verify redirect to /dashboard
3. Open incognito → navigate to /dashboard → verify redirect to /login

- [X] T017 [US1] Create web/app/page.tsx — landing page: hero section, 3 feature cards, pricing (Free/Premium/Pro), footer
- [X] T018 [US1] Create web/app/signup/page.tsx — sign-up form: calls apiRegister then apiLogin, stores session, redirects to /dashboard
- [X] T019 [US1] Create web/app/login/page.tsx — login form: calls apiLogin, stores session, redirects to /dashboard

**Checkpoint**: Auth flow fully functional — sign up, log in, protected redirect all work.

---

## Phase 4: User Story 2 — Student Reads Course Chapters (Priority: P1)

**Goal**: Chapter list with 10 cards → open chapter → two-panel layout (sidebar + content) → locked overlay for premium/pro chapters → prev/next navigation → "Start Quiz" button.

**Independent Test** (quickstart.md Scenarios 2 + 3):
1. Log in → /chapters → verify 10 cards with tier badges and completion status
2. Click chapter 1 → verify sidebar + formatted content renders
3. Navigate to /chapters/4 as free-tier user → verify locked overlay, NO content in DOM

- [X] T021 [P] [US2] Create web/components/ChapterCard.tsx — chapter card with tier badge, completion/lock icons, links to /chapters/[id] when not locked
- [X] T022 [P] [US2] Create web/components/LockedOverlay.tsx — locked chapter overlay (REPLACES content — never receives content prop)
- [X] T023 [P] [US2] Create web/components/Sidebar.tsx — chapter sidebar with current highlight, completed marks, locked non-clickable
- [X] T025 [US2] Create web/app/chapters/page.tsx — chapter list: fetches getChapters + getProgress in parallel, renders 10 ChapterCards
- [X] T026 [US2] Create web/app/chapters/[id]/page.tsx — chapter reader: checkAccess → LockedOverlay or getChapter + ReactMarkdown content + prev/next nav + "Start Quiz" button

**Checkpoint**: Chapter browsing complete — list, reading, locked overlay, navigation all work.

---

## Phase 5: User Story 3 — Student Takes a Chapter Quiz (Priority: P1)

**Goal**: Quiz page loads 5 questions → one at a time → colour feedback after submit → explanation shown → score screen after Q5.

**Independent Test** (quickstart.md Scenario 4):
1. Navigate to /quiz/1 → verify Q1 of 5, progress bar, 4 option cards, Submit disabled
2. Select option → Submit enabled → click → verify colour feedback + explanation
3. Advance through all 5 → verify score screen with "N/5 Correct — X%"

- [X] T030 [US3] Create web/app/quiz/[chapter_id]/page.tsx — quiz page: QuizState machine (questions, currentIndex, selectedAnswer, submitted, result, finalScore, isComplete); QuizQuestion component → score screen on isComplete

**Checkpoint**: Full quiz flow works — one question at a time, colour feedback, score screen.

---

## Phase 6: User Story 4 — Student Tracks Their Progress (Priority: P2)

**Goal**: Progress page shows overall stats (completion %, streak, avg score) + per-chapter table.

- [X] T031 [US4] Create web/app/progress/page.tsx — progress page: getProgress → 3 StatCards + ProgressBar + per-chapter table with TierBadge, status, score, attempts

**Checkpoint**: Progress page shows accurate live data from backend.

---

## Phase 7: User Story 5 — Student Sees a Personalised Dashboard (Priority: P2)

**Goal**: Dashboard shows 3 stat cards + "Continue Learning" card (or "Start with Chapter 1" for new users).

- [X] T034 [US5] Create web/app/dashboard/page.tsx — dashboard: getProgress → 3 StatCards + Continue/Start card based on progress

**Checkpoint**: Dashboard reflects live progress.

---

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T035 Loading spinners added to all protected pages (spinner shown while API data loads)
- [X] T036 [P] Error state displays added to all pages (red banner on API failure)
- [ ] T037 [P] Install dependencies: run `npm install` in web/
- [ ] T038 Run all 7 quickstart.md scenarios against the running app
- [ ] T039 [P] Verify SC-003: open /chapters/4 as free-tier user, confirm NO chapter content in DOM

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
- **Phase 3 (US1 Auth)**: Depends on Phase 2
- **Phase 4 (US2 Chapters)**: Depends on Phase 3
- **Phase 5 (US3 Quiz)**: Depends on Phase 3
- **Phase 6 (US4 Progress)**: Depends on Phase 5
- **Phase 7 (US5 Dashboard)**: Depends on Phase 6
- **Phase 8 (Polish)**: Depends on all phases complete

---

## Notes

- All code in `web/` directory (pre-existing skeleton, filled with implementation)
- Auth uses FastAPI backend `/auth/register` + `/auth/login` endpoints (NOT Supabase client directly)
- Token stored in localStorage + synced to `cc_auth` cookie for middleware route protection
- `<LockedOverlay>` REPLACES `<ChapterContent>` — never mounted together (SC-003 compliance)
- Quiz state never persists across page refresh (acceptable per spec edge case)
- Run `npm install && npm run dev` from `web/` directory
