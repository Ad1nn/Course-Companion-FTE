# Feature Specification: Next.js Web App — LMS Dashboard

**Feature Branch**: `004-nextjs-web-app`  
**Created**: 2026-04-28  
**Status**: Draft  
**Input**: User description: "lets go for phase 4"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Visitor Discovers the Course and Signs Up (Priority: P1)

A first-time visitor lands on the home page, reads about the course, sees the three pricing tiers, and creates a free account. After signing up they are redirected to the dashboard.

**Why this priority**: Without a working landing page and auth flow, no other page can be reached. This is the entry point for all other user stories and the first thing judges see.

**Independent Test**: Open the app, read the landing page, click "Start Free", fill in the sign-up form, and confirm redirection to the dashboard. Can be verified without any course content in the database.

**Acceptance Scenarios**:

1. **Given** a visitor opens the home page, **When** they read the page, **Then** they see: a hero section with headline and CTA, three feature highlights, a pricing section with Free / Premium / Pro tier cards, and a footer.
2. **Given** a visitor clicks "Start Learning Free", **When** they fill in email and password and submit, **Then** an account is created and they are redirected to `/dashboard`.
3. **Given** an existing user visits the sign-up page, **When** they submit with a duplicate email, **Then** they see a clear error message and are not redirected.
4. **Given** a registered user clicks "Login" from the nav, **When** they enter valid credentials, **Then** they are redirected to `/dashboard`.
5. **Given** a user tries to visit `/dashboard` without being logged in, **When** the page loads, **Then** they are redirected to `/login`.

---

### User Story 2 — Student Reads Course Chapters (Priority: P1)

A logged-in student browses the chapter list, selects a chapter they have access to, reads the full content in a two-panel layout (sidebar + content area), and navigates to adjacent chapters.

**Why this priority**: Reading chapters is the primary learning activity. The sidebar navigation is shared across chapter and quiz pages.

**Independent Test**: Log in as a free-tier user, navigate to `/chapters`, confirm 10 chapter cards are shown with correct tier badges. Open chapter 1, confirm full content renders. Try to open chapter 4 — confirm it shows a locked/upgrade overlay instead of content.

**Acceptance Scenarios**:

1. **Given** a logged-in student visits `/chapters`, **When** the page loads, **Then** they see 10 chapter cards, each showing chapter number, title, description, tier badge, and completion status (checkmark or empty).
2. **Given** a free-tier student clicks chapter 1, **When** the page loads, **Then** they see the full content rendered as formatted text in the content area, with a left sidebar listing all 10 chapters (current chapter highlighted).
3. **Given** a free-tier student clicks chapter 4 (premium), **When** the page loads, **Then** the content is blurred and an upgrade prompt overlay is shown instead — the raw text is never visible.
4. **Given** a student is reading chapter 2, **When** they click "Next Chapter", **Then** they are navigated to chapter 3.
5. **Given** a student completes reading chapter 1, **When** they click "Start Quiz", **Then** they are navigated to `/quiz/1`.

---

### User Story 3 — Student Takes a Chapter Quiz (Priority: P1)

A logged-in student takes a 5-question multiple-choice quiz for a chapter. They answer questions one at a time, see immediate feedback (correct/wrong + explanation) after each, and view their final score on a summary screen.

**Why this priority**: Quizzes are the primary engagement and retention mechanism. They are independently reachable from the chapter page and from the chapter list.

**Independent Test**: Log in, navigate to `/quiz/1`, answer all 5 questions, confirm score appears at the end and matches what the backend returned. Confirm questions appear one at a time and correct/wrong feedback is shown after each.

**Acceptance Scenarios**:

1. **Given** a student navigates to `/quiz/1`, **When** the quiz loads, **Then** they see question 1 of 5 with a progress bar, the question text, and 4 answer option cards.
2. **Given** a student clicks an answer option, **When** they click "Submit Answer", **Then** the selected card changes colour (green for correct, red for wrong), the correct answer is highlighted green, and the explanation text appears below.
3. **Given** a student submits a correct answer, **When** the result is shown, **Then** a "Next Question →" button appears and clicking it shows question 2.
4. **Given** a student answers the 5th question and submits, **When** the result is shown, **Then** a final score screen appears: "4 / 5 Correct — 80%", plus a "Back to Chapter" button and a "Retake Quiz" button.
5. **Given** a student has not selected any option, **When** the "Submit Answer" button is visible, **Then** the button is disabled until an option is selected.

---

### User Story 4 — Student Tracks Their Progress (Priority: P2)

A logged-in student visits the progress page and sees an overview of all chapters: how many are completed, their scores, their current streak, and their average score across all quizzes.

**Why this priority**: Progress visibility drives return visits and reinforces the course's value. Depends on at least one completed quiz to show meaningful data.

**Independent Test**: Complete at least one quiz, navigate to `/progress`, confirm the chapter table shows the completed chapter with the correct score, and the overall stats match.

**Acceptance Scenarios**:

1. **Given** a student visits `/progress`, **When** the page loads, **Then** they see: overall completion percentage, streak count, average score, and a progress bar for total chapters.
2. **Given** a student has completed chapter 1 with 80%, **When** viewing the progress table, **Then** chapter 1 shows a green checkmark, "80%", and the attempt count.
3. **Given** a student has not completed any chapter, **When** viewing the progress page, **Then** all chapters show as "not started" and stats show zeroes.
4. **Given** a student with a pro tier views the page, **Then** all 10 chapters are listed. A free-tier student sees all 10 but locked chapters are marked with a padlock.

---

### User Story 5 — Student Sees a Personalised Dashboard (Priority: P2)

A logged-in student lands on `/dashboard` and sees a welcome message, three stat cards (chapters completed, streak, average score), and a "Continue Learning" card pointing to their most recently accessed chapter (or chapter 1 if no progress).

**Why this priority**: The dashboard is the hub page students see after every login. It orients them quickly. Depends on progress data from User Story 4.

**Independent Test**: Log in as a user with some progress. Navigate to `/dashboard`. Confirm stat cards show correct values and the "Continue" card links to the correct chapter.

**Acceptance Scenarios**:

1. **Given** a student logs in, **When** they arrive at `/dashboard`, **Then** they see a welcome message with their name or email, and three stat cards: "Chapters Completed X/10", "Day Streak 🔥 N days", "Average Score N%".
2. **Given** a student has completed chapters 1 and 2, **When** they view the dashboard, **Then** the "Continue Learning" card shows their most recently accessed chapter title with a "Continue →" button.
3. **Given** a brand-new student with no progress, **When** they view the dashboard, **Then** a "Start with Chapter 1" card is shown instead of "Continue Learning", and all stats show zero.

---

### Edge Cases

- What if a student's session expires while they are mid-quiz? They are redirected to `/login` and their partial answers are lost — acceptable for hackathon scope.
- What if a chapter fails to load (backend error)? A user-friendly error message is shown; the rest of the page remains functional.
- What if a student navigates directly to `/quiz/4` but is on the free tier? They see a locked state with an upgrade prompt — same behaviour as the locked chapter page.
- What if there is no "next" chapter (student is on chapter 10)? The "Next Chapter" button is hidden.
- What if the backend is unreachable? A generic "Something went wrong — please try again" message is shown.

---

## Requirements *(mandatory)*

### Functional Requirements

**Authentication:**
- **FR-001**: Students MUST be able to create an account with email and password.
- **FR-002**: Students MUST be able to log in with their credentials and be redirected to the dashboard.
- **FR-003**: All pages except the landing page, login, and sign-up MUST redirect unauthenticated visitors to `/login`.

**Chapter browsing:**
- **FR-004**: The chapter list MUST show all 10 chapters with title, description, tier badge, and completion status.
- **FR-005**: Locked chapters MUST show a padlock overlay and an upgrade prompt — the content MUST NOT be visible.
- **FR-006**: The chapter reading page MUST show a fixed left sidebar with all 10 chapters listed, the current chapter highlighted, completed chapters marked, and locked chapters non-clickable.
- **FR-007**: The chapter reading page MUST render chapter content as formatted text (paragraphs, headings, code blocks).
- **FR-008**: The chapter reading page MUST have "Previous Chapter" and "Next Chapter" navigation buttons.

**Quiz:**
- **FR-009**: The quiz MUST show one question at a time with a progress indicator ("Question N of 5").
- **FR-010**: The "Submit Answer" button MUST be disabled until the student selects an option.
- **FR-011**: After submission, the selected option MUST change colour (green = correct, red = wrong) and the correct option MUST be highlighted green.
- **FR-012**: The explanation text MUST appear below the options after submission.
- **FR-013**: The final screen MUST show the score as both "N / 5 Correct" and a percentage.
- **FR-014**: The final screen MUST have "Back to Chapter" and "Retake Quiz" buttons.

**Progress:**
- **FR-015**: The progress page MUST show overall stats (completion %, streak, average score) and a per-chapter table.
- **FR-016**: The per-chapter table MUST show: chapter title, tier badge, status (completed / not started / locked), score (if attempted), and attempt count.

**Dashboard:**
- **FR-017**: The dashboard MUST show three stat cards: chapters completed, day streak, and average score.
- **FR-018**: The dashboard MUST show a "Continue Learning" card with the most recently accessed chapter, or a "Start with Chapter 1" card if no progress exists.

### Key Entities

- **Student**: Authenticated user with an email, tier, and associated progress records.
- **Chapter**: Course unit with title, tier, and content — read from the backend.
- **Quiz Question**: Multiple-choice question for a chapter — fetched per chapter, answered one at a time.
- **Progress Record**: Per-chapter completion status, score, and attempt count for a student.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new student can create an account, reach the dashboard, open a chapter, and start a quiz in under 5 minutes from landing on the home page.
- **SC-002**: All 5 pages (landing, dashboard, chapters list, chapter reading, quiz, progress) load with visible content in under 3 seconds on a standard connection.
- **SC-003**: A free-tier student cannot see any locked chapter content — verified by inspecting the page DOM and confirming the content field is absent.
- **SC-004**: A complete quiz session (5 questions, submit, score) completes without errors in 100% of test runs.
- **SC-005**: The progress page accurately reflects the backend's stored progress — score shown matches what the backend returned after quiz submission.

## Assumptions

- The FastAPI backend (Phase 1) is deployed on Railway and all endpoints are accessible at a public URL.
- All 10 chapters and 50 quiz questions are seeded in Supabase (Phase 2 complete).
- Supabase Auth handles session token storage in the browser automatically — the web app does not manage tokens manually.
- The design system uses violet as the primary colour (as defined in the project plan) — specific hex values are implementation details and not part of this spec.
- Tier upgrades are done via the admin endpoint for hackathon demo purposes — no payment UI is needed.
- The web app is a client-side rendered single-page application — SEO is not a requirement for the hackathon.
- Mobile responsiveness is desirable but not required for the hackathon demo — desktop-first is acceptable.

## Out of Scope

- Payment or subscription management UI — tier upgrades handled by the admin endpoint only.
- Email verification or password reset flows — out of scope for hackathon.
- Phase 5 hybrid features (adaptive path, LLM assessment) — separate feature.
- Mobile app or native application — web only.
- Internationalisation or accessibility compliance beyond semantic HTML.
