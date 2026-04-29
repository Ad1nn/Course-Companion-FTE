# Feature Specification: ChatGPT App — AI Tutor Integration

**Feature Branch**: `003-chatgpt-app`  
**Created**: 2026-04-28  
**Status**: Draft  
**Input**: User description: "let go for phase 3"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Student Learns a Topic Through ChatGPT (Priority: P1)

A student opens ChatGPT, finds the Course Companion app, and asks about an Agentic AI topic. The tutor searches the course, fetches the relevant chapter, and teaches using only that content — never improvising from general knowledge. The student feels they have a knowledgeable, focused tutor.

**Why this priority**: This is the core value proposition. Without working teaching flow, nothing else matters. It is also the primary evaluation criterion for the ChatGPT App platform judges.

**Independent Test**: Open the ChatGPT App and ask "What is MCP?" — the tutor should fetch chapter 4 and explain. Ask about a topic not in the course — the tutor should decline gracefully. Both flows testable without quizzes or progress.

**Acceptance Scenarios**:

1. **Given** a student asks "Explain the agent loop", **When** the tutor searches the course and finds chapter 1, **Then** the tutor fetches chapter 1 and explains using only its content — no external knowledge added.
2. **Given** a student asks about "blockchain", **When** the tutor searches and finds no relevant chapter, **Then** the tutor responds "That topic isn't covered in this course."
3. **Given** a student asks a vague question like "tell me about agents", **When** the tutor searches, **Then** it identifies the most relevant chapter and proceeds to teach from it.
4. **Given** a free-tier student asks about chapter 4 (MCP — premium tier), **When** the tutor checks access, **Then** it warmly informs the student that chapter 4 requires a Premium plan without revealing any content.

---

### User Story 2 — Student Takes a Quiz Through ChatGPT (Priority: P1)

A student says "quiz me on chapter 2" and the tutor administers the 5 questions one at a time, accepts the student's answers, scores each one, shows the educational explanation, and at the end reports the final score and saves progress.

**Why this priority**: Quizzes are the primary learning reinforcement mechanism and a key product differentiator. Judges will test this flow explicitly.

**Independent Test**: Say "quiz me on chapter 1" in the ChatGPT App — the tutor should present question 1 of 5, wait for an answer, score it, show the explanation, then proceed through all 5. Final score must be displayed and saved.

**Acceptance Scenarios**:

1. **Given** a student says "quiz me on chapter 1", **When** the tutor fetches the questions, **Then** it presents only question 1 (never all 5 at once) and waits for the student's answer.
2. **Given** a student answers correctly, **When** the tutor submits the answer, **Then** it celebrates and shows the educational explanation.
3. **Given** a student answers incorrectly, **When** the tutor submits the answer, **Then** it responds encouragingly, reveals the correct answer, and shows the explanation.
4. **Given** a student answers the 5th question, **When** the tutor submits it, **Then** it calculates and displays the final score (e.g., "4 out of 5 — 80%") and confirms progress has been saved.

---

### User Story 3 — Student Checks Their Progress (Priority: P2)

A student asks "how am I doing?" and the tutor fetches their live progress record and presents it encouragingly — showing which chapters are complete, scores, streak, and a suggested next chapter.

**Why this priority**: Progress feedback sustains engagement and demonstrates the full learning loop. Depends on quiz flow having saved at least one result first.

**Independent Test**: Complete at least one quiz, then ask "how am I doing?" — the tutor should report progress accurately and suggest a next chapter.

**Acceptance Scenarios**:

1. **Given** a student asks "how am I doing?", **When** the tutor fetches progress, **Then** it presents: chapters completed, scores, streak, and average score.
2. **Given** a student has completed some chapters, **When** progress is shown, **Then** the tutor proactively suggests the next uncompleted accessible chapter.
3. **Given** a student has no progress yet, **When** they ask "how am I doing?", **Then** the tutor encourages them warmly and directs them to start with chapter 1.

---

### Edge Cases

- What happens when a student asks a quiz question mid-lesson rather than via "quiz me"? The tutor should redirect to the structured quiz flow.
- What if the student answers a quiz question in freeform text (e.g., "I think it's B")? The tutor should parse their intent correctly before submitting.
- What if the backend is unreachable? The tutor should apologise and ask the student to try again — it must never fabricate an answer.
- What if a student's tier is upgraded mid-session? Access must be checked fresh on each chapter request, not cached from earlier in the conversation.
- What if a student asks to skip a quiz question? The tutor should decline gently and ask them to attempt an answer.

---

## Requirements *(mandatory)*

### Functional Requirements

**Teaching flow:**
- **FR-001**: The tutor MUST search course content before answering any topic question — it must never teach from general knowledge without first fetching chapter content.
- **FR-002**: The tutor MUST check the student's access tier before fetching any chapter — if the chapter is locked it must not reveal content and must explain the upgrade path warmly.
- **FR-003**: When a topic is not found in the course, the tutor MUST decline to teach it and inform the student clearly.

**Quiz flow:**
- **FR-004**: The tutor MUST present quiz questions one at a time — never all 5 at once.
- **FR-005**: The tutor MUST wait for the student's answer before advancing to the next question.
- **FR-006**: The tutor MUST submit each answer to the backend and use the backend's result — it must not score locally.
- **FR-007**: After the final question, the tutor MUST display the total score and confirm that progress has been saved.

**Progress flow:**
- **FR-008**: The tutor MUST fetch live progress data when asked about performance — it must not estimate or recall from earlier in the conversation.
- **FR-009**: The tutor MUST suggest the next chapter to study based on the student's fetched progress data.

**Personality and safety:**
- **FR-010**: The tutor MUST maintain a warm, patient, and encouraging tone at all times.
- **FR-011**: The tutor MUST frame wrong answers as learning opportunities — it must never be condescending.
- **FR-012**: The tutor MUST adjust explanation depth to match the apparent level of the student's questions.

**Access control:**
- **FR-013**: When a locked chapter is requested, the tutor MUST name the required tier and direct the student to upgrade without partially revealing the content.

### Key Entities

- **Chapter**: A course unit with a title, tier, and full text content — fetched by the tutor to teach.
- **Quiz Question**: A multiple-choice question with four options — fetched per chapter, scored by the backend.
- **Progress Record**: A student's completion status, score, and streak — fetched and displayed on demand.
- **Student Tier**: The access level of the authenticated student (free / premium / pro) — checked before every chapter access.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A student can discover the app, ask a question, and receive a full explanation in under 3 conversational turns.
- **SC-002**: The tutor correctly refuses to reveal locked content 100% of the time across all tier scenarios tested.
- **SC-003**: A complete 5-question quiz can be administered end-to-end without errors or incorrect scoring in every test run.
- **SC-004**: The tutor never fabricates course content — 100% of teaching responses reference fetched chapter data, verifiable by disabling the backend and confirming the tutor does not improvise.
- **SC-005**: Students receive accurate progress data and a next-chapter recommendation within a single "how am I doing?" interaction.

## Assumptions

- The FastAPI backend (Phase 1) is deployed and reachable at a public URL on Railway.
- All 10 chapters and 50 quiz questions are seeded in Supabase (Phase 2 complete).
- The ChatGPT App platform supports custom OpenAPI actions — the three config files (system prompt, OpenAPI spec, manifest) are the only deliverables for this phase; no new backend code is written.
- For the hackathon demo, a single test user account with a pre-configured identity is used to demonstrate all flows — full production OAuth wiring is out of scope.
- The OpenAPI spec must exactly match the deployed backend's endpoint signatures — any mismatch will cause action calls to fail silently.

## Out of Scope

- Building any new backend endpoints — Phase 1 endpoints are used as-is.
- A web-based UI — the ChatGPT App lives entirely inside the ChatGPT platform.
- Payment or subscription management — tier upgrades are done via the admin endpoint for demo purposes.
- Phase 5 hybrid features (adaptive learning path, LLM-graded assessments) — separate routes not exposed through this app.
