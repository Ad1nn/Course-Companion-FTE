# Feature Specification: Phase 2 — Course Content Seeding

**Feature Branch**: `002-content-seeding`
**Created**: 2026-04-28
**Status**: Draft
**Input**: User description: "write for phase 2"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Student Reads a Full Chapter (Priority: P1)

A student navigating the course opens any of the 10 chapters and reads the full
textbook content. Content must be rich enough to be educationally meaningful and
sufficient for ChatGPT to explain the topic when asked.

**Why this priority**: Without chapter content, the entire product — both the
ChatGPT tutor and the web app — has nothing to teach. This is the core deliverable
of Phase 2.

**Independent Test**: Open `GET /chapters/1` through `GET /chapters/10` — each
returns a non-empty `content` field of at least 500 words covering the chapter topic.
All 10 chapters exist in the database with correct titles, tiers, and order numbers.

**Acceptance Scenarios**:

1. **Given** the database is seeded, **When** `GET /chapters` is called, **Then** exactly 10 chapters are returned in order (1–10) with correct titles, tiers, and descriptions.
2. **Given** the database is seeded, **When** `GET /chapters/1` is called, **Then** full content for "Introduction to AI Agents" is returned with at least 500 words.
3. **Given** the database is seeded, **When** `GET /chapters/4` is called, **Then** the chapter tier is `premium` and content covers MCP Fundamentals.
4. **Given** the database is seeded, **When** `GET /chapters/8` is called, **Then** the chapter tier is `pro` and content covers Vector Databases & RAG.
5. **Given** the database is seeded, **When** a ChatGPT user asks "explain MCP", **Then** `GET /search?q=MCP` returns chapter 4 and 5 as results.

---

### User Story 2 — Student Takes a Complete Chapter Quiz (Priority: P1)

A student finishes reading a chapter and takes the 5-question quiz. Every chapter
must have exactly 5 multiple-choice questions with clear correct answers and
educational explanations.

**Why this priority**: Quizzes are the primary assessment mechanism and a scored
hackathon criterion. Without quiz data, the quiz endpoints are untestable.

**Independent Test**: Call `GET /quizzes/{chapter_id}` for all 10 chapters — each
returns exactly 5 questions. Submit all answers for chapter 1 quiz and verify a score
is returned. Verify `correct_answer` is never in the list response.

**Acceptance Scenarios**:

1. **Given** the database is seeded, **When** `GET /quizzes/{chapter_id}` is called for any of the 10 chapters, **Then** exactly 5 questions are returned.
2. **Given** 50 total quiz questions exist, **When** all chapter quizzes are listed, **Then** each question has `question`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_answer`, and `explanation` populated.
3. **Given** a student submits all 5 answers for chapter 1, **When** the 5th answer is submitted, **Then** a percentage score (0–100) is returned.
4. **Given** quiz questions are stored, **When** `GET /quizzes/{chapter_id}` is called, **Then** `correct_answer` is never present in the response.

---

### Edge Cases

- What if a chapter has fewer than 5 quiz questions? → Content is incomplete; seeding script must validate count before finishing.
- What if chapter content is too short for meaningful teaching? → Minimum 500 words per chapter enforced as acceptance gate.
- What if chapter IDs are not contiguous (1–10)? → IDs must be exactly 1 through 10 to match tier access rules and nav logic.
- What if duplicate chapters are seeded? → Seeding must use upsert (insert-or-replace) to be idempotent and safe to re-run.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST contain exactly 10 chapters in the database with IDs 1–10.
- **FR-002**: Each chapter MUST have: `title`, `description` (2-sentence summary), `content` (minimum 500 words), `order_num` (1–10), and `tier` (`free`, `premium`, or `pro`).
- **FR-003**: Tier assignments MUST follow the project plan: chapters 1–3 = `free`, chapters 4–7 = `premium`, chapters 8–10 = `pro`.
- **FR-004**: Chapter content MUST be sourced from the Panaversity Agent Factory textbook (Part 6, Chapters 61–77) and cover the Agentic AI development curriculum.
- **FR-005**: System MUST contain exactly 50 quiz questions — 5 per chapter.
- **FR-006**: Each quiz question MUST have: `question`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_answer` (A/B/C/D), `explanation`, and `order_num` (1–5).
- **FR-007**: Quiz questions MUST be factually accurate and directly testable from the chapter content.
- **FR-008**: The seeding operation MUST be idempotent — running it multiple times produces the same result without duplicates.
- **FR-009**: Chapter descriptions MUST be 1–2 sentences suitable for display on chapter cards in the web app.

### Key Entities

- **Chapter**: 10 records covering Agentic AI development topics, each with full textbook-sourced content and tier-gated access.
- **Quiz Question**: 50 records (5 per chapter), each a multiple-choice question with one correct answer and an educational explanation.

### Chapter Catalogue

| # | Title | Tier | Textbook Source |
|---|-------|------|----------------|
| 1 | Introduction to AI Agents | free | Ch 61 |
| 2 | OpenAI Agents SDK | free | Ch 62 |
| 3 | Anthropic Claude Agent SDK | free | Ch 65 |
| 4 | MCP Fundamentals | premium | Ch 66 |
| 5 | Advanced MCP Server Development | premium | Ch 67 |
| 6 | Agent Skills & MCP Code Execution | premium | Ch 68 |
| 7 | FastAPI for Agents | premium | Ch 70 |
| 8 | Vector Databases & RAG | pro | Ch 73 |
| 9 | Multi-Agent Reliability | pro | Ch 69 |
| 10 | Evals — Measuring Agent Performance | pro | Ch 77 |

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 10 chapters exist in the database with correct IDs, titles, tiers, and order numbers.
- **SC-002**: All 10 chapters have content of at least 500 words each (5,000+ words total across all chapters).
- **SC-003**: All 50 quiz questions exist — exactly 5 per chapter — verified by querying `GET /quizzes/{chapter_id}` for each chapter.
- **SC-004**: The seeding script runs to completion without errors and is safe to re-run.
- **SC-005**: A ChatGPT tutor simulation (calling search + chapter endpoints) can teach any of the 10 topics using only the seeded content.
- **SC-006**: Tier enforcement works correctly with real content — free users can access chapters 1–3, premium users 1–7, pro users all 10.
