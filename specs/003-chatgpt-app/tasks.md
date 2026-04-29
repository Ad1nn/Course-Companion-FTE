---
description: "Task list for Phase 3 — ChatGPT App AI Tutor Integration"
---

# Tasks: Phase 3 — ChatGPT App

**Input**: Design documents from `/specs/003-chatgpt-app/`
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | quickstart.md ✅

**Tests**: Manual verification via ChatGPT App after registration (see quickstart.md).

**Organization**: Config-only — tasks author content in 3 files under `chatgpt-app/`. Organized by user story so each flow can be independently tested after its tasks complete.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different sections, no file conflicts)
- **[Story]**: US1 = teaching flow, US2 = quiz flow, US3 = progress flow
- All paths relative to repo root

---

## Phase 1: Setup

**Purpose**: Create `chatgpt-app/` directory and author the app metadata file.

- [X] T001 Create `chatgpt-app/` directory and write `chatgpt-app/manifest.yaml` — include: `name_for_human: "Course Companion — Agentic AI Tutor"`, `name_for_model: "course_companion"`, `description_for_human` (1-2 sentences), `description_for_model` (detailed tutor context for GPT Builder), `contact_email`, `legal_info_url`, `logo_url` (placeholder)

**Checkpoint**: `chatgpt-app/manifest.yaml` exists with no placeholder tokens.

---

## Phase 2: Foundational

**Purpose**: Author the skeleton of both primary config files. These must exist before US-specific content is added.

- [X] T002 Write `chatgpt-app/openapi.yaml` skeleton — include: `openapi: "3.1.0"`, `info` block (title: "Course Companion API", version: "1.0.0", description), `servers` block with production Railway URL `https://course-companion.railway.app`, empty `paths: {}`, and `components.schemas` section with reusable schema definitions for: `ChapterSummary` (id, title, excerpt, tier), `ChapterFull` (id, title, description, content, order_num, tier), `QuizQuestion` (id, chapter_id, question, option_a, option_b, option_c, option_d, order_num), `SubmitResult` (correct, correct_answer, explanation, score), `AccessResult` (allowed, required_tier, user_tier), `ProgressRecord` (tier, streak_days, avg_score, chapters_completed, chapters[])

- [X] T003 [P] Write `chatgpt-app/system-prompt.md` skeleton — create 7 labelled sections with headers: `## Identity & Role`, `## Teaching Flow`, `## Quiz Flow`, `## Progress Flow`, `## Access Control`, `## Personality Rules`, `## Hard Rules`. Fill Identity & Role (tutor name, what it teaches, model context) and Hard Rules (never fabricate, always fetch first, never show all quiz questions at once, never reveal locked content) in full. Leave the other 5 sections with `[TODO: see tasks]` placeholders.

**Checkpoint**: Both files exist; YAML parses without error; skeleton sections are present.

---

## Phase 3: User Story 1 — Teaching Flow (Priority: P1)

**Goal**: Student asks a topic question and the tutor searches, checks access, fetches the chapter, and explains using only the fetched content. Locked chapters are blocked warmly.

**Independent Test**: Register the GPT with the skeleton files. Ask "What is the agent loop?" — tutor must call `/search`, then `/access/check`, then `/chapters/1`, then explain. Ask "Tell me about blockchain" — tutor must decline. Ask about a premium chapter with free-tier account — tutor must block without leaking content.

- [X] T004 [US1] Add `GET /search` to `chatgpt-app/openapi.yaml` paths — operationId: `searchChapters`, description: "Search course chapters by keyword to find teaching content", query param `q` (string, required, description: "Topic keyword to search for"), response 200: array of `$ref: '#/components/schemas/ChapterSummary'`, response 400: `{detail: string}`

- [X] T005 [P] [US1] Add `GET /access/check` to `chatgpt-app/openapi.yaml` paths — operationId: `checkAccess`, description: "Check if the authenticated student can access a chapter before fetching it", query param `chapter_id` (integer, required), response 200: `$ref: '#/components/schemas/AccessResult'`

- [X] T006 [P] [US1] Add `GET /chapters/{id}` to `chatgpt-app/openapi.yaml` paths — operationId: `getChapter`, description: "Fetch the full content of a chapter for teaching. Only call after checkAccess confirms allowed: true.", path param `id` (integer, required), response 200: `$ref: '#/components/schemas/ChapterFull'`, response 403: `{detail: string, required_tier: string, user_tier: string, message: string}`, response 404: `{detail: string}`

- [X] T007 [US1] Write `## Teaching Flow` section in `chatgpt-app/system-prompt.md` — numbered steps: (1) Extract a 1-3 word keyword from the student's question. (2) Call `searchChapters` with that keyword. (3) If no results: respond "That topic isn't covered in this course." and stop. (4) Identify the most relevant chapter from results. (5) Call `checkAccess` with that chapter_id. (6) If `allowed: false`: go to Access Control section. (7) If `allowed: true`: call `getChapter` with that id. (8) Explain using ONLY the content field returned — do not add facts from general knowledge. (9) Offer to quiz the student on the chapter.

- [X] T008 [US1] Write `## Access Control` section in `chatgpt-app/system-prompt.md` — exact response script for denied access: "Chapter [title] is part of our [required_tier] plan. Your current plan gives you access to [describe free/premium chapters]. To unlock this chapter, upgrade at [course URL]. In the meantime, I'm happy to teach you any of your available chapters!" — never quote or paraphrase the locked content under any circumstances.

**Checkpoint**: With these tasks complete, register the GPT and confirm the teaching flow works end-to-end. Locked chapter test must pass.

---

## Phase 4: User Story 2 — Quiz Flow (Priority: P1)

**Goal**: Student says "quiz me on chapter N" and the tutor administers all 5 questions one at a time, scores each answer via the backend, shows the explanation, and displays a final score after question 5.

**Independent Test**: Say "quiz me on chapter 1" — confirm question 1 appears alone. Answer it. Confirm score and explanation shown before question 2 appears. Complete all 5. Confirm final score displayed.

- [X] T009 [US2] Add `GET /quizzes/{chapter_id}` to `chatgpt-app/openapi.yaml` paths — operationId: `getQuizQuestions`, description: "Fetch all 5 quiz questions for a chapter. Do NOT show all questions at once — present them one at a time.", path param `chapter_id` (integer, required), response 200: array of `$ref: '#/components/schemas/QuizQuestion'`, response 404: `{detail: string}`

- [X] T010 [US2] Add `POST /quizzes/{quiz_id}/submit` to `chatgpt-app/openapi.yaml` paths — operationId: `submitQuizAnswer`, description: "Submit the student's answer to a single quiz question and get the result. Call this after every student answer.", path param `quiz_id` (integer, required), request body (required): `{user_id: string (uuid of the authenticated student), answer: string (exactly one of: A, B, C, D)}`, response 200: `$ref: '#/components/schemas/SubmitResult'`

- [X] T011 [US2] Write `## Quiz Flow` section in `chatgpt-app/system-prompt.md` — numbered steps: (1) When student says "quiz me on chapter N", call `getQuizQuestions` with that chapter_id. Store all 5 questions internally. (2) Present question 1 only — show the question text and all four options (A/B/C/D) clearly. Do NOT show questions 2-5. (3) Wait for student's answer. Parse their response to extract A, B, C, or D. (4) Call `submitQuizAnswer` with the question's id and the parsed answer. Use the student's known user_id. (5) If `correct: true`: celebrate warmly. Show the explanation. (6) If `correct: false`: respond encouragingly. Show the correct answer and explanation. (7) If more questions remain: present the next question. (8) After submitting question 5: if `score` is in the response, display "You scored [score]% — [correct]/5 correct!" Confirm "Your progress has been saved." (9) Offer to review the chapter or move to the next one.

**Checkpoint**: Complete a full 5-question quiz via the ChatGPT App. Confirm each question appears individually, scoring is correct, and final score matches.

---

## Phase 5: User Story 3 — Progress Flow (Priority: P2)

**Goal**: Student asks "how am I doing?" and receives accurate progress stats plus a recommendation for what to study next.

**Independent Test**: After completing at least one quiz, ask "how am I doing?" — the tutor must fetch live progress, display chapter completions and scores, and suggest the next chapter.

- [X] T012 [US3] Add `GET /progress/{user_id}` to `chatgpt-app/openapi.yaml` paths — operationId: `getProgress`, description: "Fetch the student's full progress record including completed chapters, scores, streak, and average score.", path param `user_id` (string, required, description: "The student's UUID from their user account"), response 200: `$ref: '#/components/schemas/ProgressRecord'`, response 404: `{detail: string}`

- [X] T013 [US3] Write `## Progress Flow` section in `chatgpt-app/system-prompt.md` — numbered steps: (1) When student asks about their progress, ensure you have their user_id. If not known, ask: "Could you share your user ID? You can find it in your account settings." (2) Call `getProgress` with the user_id. (3) Present a friendly summary: "Here's how you're doing: ✅ [chapters_completed] of 10 chapters complete | 📊 Average score: [avg_score]% | 🔥 [streak_days]-day streak". (4) List completed chapters with their scores. (5) Identify the first chapter in the chapters list where `completed: false` and the student's tier allows access — suggest it warmly: "I'd suggest tackling [title] next — want me to start teaching it?" (6) If no progress yet: "You haven't started yet — let's change that! Chapter 1 (Introduction to AI Agents) is free and a great starting point."

**Checkpoint**: Ask "how am I doing?" after completing a quiz. Confirm correct chapter count, score, and a valid next-chapter recommendation.

---

## Phase 6: Polish & Verification

**Purpose**: Complete the personality section, validate YAML, and run end-to-end registration + test.

- [X] T014 Write `## Personality Rules` section in `chatgpt-app/system-prompt.md` — bullet-point rules: always warm and encouraging; celebrate correct answers with genuine enthusiasm; frame wrong answers as learning opportunities, never as failures; adjust explanation depth based on the complexity of the student's questions (simpler questions → simpler explanations, technical questions → deeper responses); never be condescending or impatient; use plain language first, technical terms second; when a student seems confused, rephrase rather than repeat

- [X] T015 Validate `chatgpt-app/openapi.yaml` — confirm: (a) YAML parses without error, (b) all 6 operationIds are present (searchChapters, checkAccess, getChapter, getQuizQuestions, submitQuizAnswer, getProgress), (c) all `$ref` schema references resolve, (d) no admin or hybrid endpoints are present, (e) servers block contains the Railway production URL

- [X] T016 Run full verification from `specs/003-chatgpt-app/quickstart.md` — register the GPT in ChatGPT Builder using the completed config files, complete all 7 checklist items in quickstart.md, confirm all three user story flows pass

---

## Dependencies & Execution Order

- **Phase 1** (T001): No dependencies — start immediately
- **Phase 2** (T002, T003): Depends on T001. T002 and T003 can run in parallel (different files)
- **Phase 3** (T004–T008): Depends on T002 + T003. T005 and T006 can run in parallel with T004 (different openapi.yaml paths). T007 and T008 depend on T004–T006 (conceptually) but can be authored once the Teaching Flow is understood.
- **Phase 4** (T009–T011): Depends on Phase 2. T009 and T010 can run in parallel (different paths). T011 depends on T009 and T010.
- **Phase 5** (T012–T013): Depends on Phase 2. Can start in parallel with Phases 3 and 4.
- **Phase 6** (T014–T016): Depends on all previous phases complete.

### Parallel Opportunities

```
T001 → T002 + T003 (parallel, different files)
     → T004 → T005 + T006 (parallel, different paths) → T007 → T008
     → T009 + T010 (parallel) → T011
     → T012 → T013
→ T014 → T015 → T016
```

---

## Implementation Strategy

### MVP (US1 Teaching Flow only — proves the core value)
1. Complete Phase 1 (T001)
2. Complete Phase 2 (T002, T003)
3. Complete Phase 3 (T004–T008)
4. Register GPT and test teaching flow + access control
5. **DEMO**: Student can ask about any topic, get a chapter-based explanation

### Full Delivery
1. Complete MVP
2. Add US2 quiz flow (T009–T011)
3. Add US3 progress flow (T012–T013)
4. Polish (T014–T016) and full verification

---

## Notes

- `chatgpt-app/openapi.yaml` must use the exact endpoint signatures from the Phase 1 backend — any schema mismatch causes silent failures in ChatGPT Actions
- The `user_id` in `submitQuizAnswer` must be the student's actual Supabase UUID — the system prompt must instruct the tutor to ask for it once if not known
- `ADMIN_SECRET` and all `/admin/*`, `/hybrid/*` endpoints are explicitly excluded from the OpenAPI schema (constitution requirement)
- For the hackathon demo, the demo JWT is entered as an API Key in GPT Builder — the tutor automatically sends `Authorization: Bearer <token>` on every action call
