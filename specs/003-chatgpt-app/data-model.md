# Data Model: Phase 3 — ChatGPT App

**Note**: Phase 3 creates no new database tables or entities. It consumes the existing Phase 1 backend. This document maps the entities the tutor interacts with to the Actions it calls.

---

## Entities the Tutor Consumes

### Chapter (read-only)

The tutor fetches chapter content via `GET /chapters/{id}` and search results via `GET /search`.

| Field | Type | Used by tutor |
|-------|------|---------------|
| id | integer | Used as path param for fetch and access check |
| title | string | Displayed to student when discussing the chapter |
| description | string | Shown in search results to identify relevance |
| content | string | Full text used to teach — never truncated |
| tier | string (free/premium/pro) | Shown when explaining access requirements |
| order_num | integer | Used to describe chapter sequence |

### Quiz Question (read-only fetch, write via submit)

The tutor fetches questions via `GET /quizzes/{chapter_id}` and submits answers via `POST /quizzes/{quiz_id}/submit`.

| Field | Type | Used by tutor |
|-------|------|---------------|
| id | integer | Used as path param in submit call |
| chapter_id | integer | Links question to chapter |
| question | string | Presented to student verbatim |
| option_a/b/c/d | string | Presented as answer choices |
| order_num | integer | Used to track progress through 5 questions |
| correct_answer | string | NEVER returned by GET — only revealed by submit response |
| explanation | string | Shown after answer submitted (from submit response) |

### Progress Record (read-only fetch, written by backend on final quiz submit)

The tutor fetches progress via `GET /progress/{user_id}`.

| Field | Type | Used by tutor |
|-------|------|---------------|
| tier | string | Confirms current access level |
| streak_days | integer | Highlighted as encouragement |
| avg_score | float | Summarised as overall performance |
| chapters_completed | integer | Used in "X of 10 chapters done" summary |
| chapters[] | array | Per-chapter status, score, attempts |

### Access Result (read-only check)

The tutor calls `GET /access/check?chapter_id={id}` before every chapter fetch.

| Field | Type | Used by tutor |
|-------|------|---------------|
| allowed | boolean | Gate: if false, tutor explains upgrade instead of fetching |
| required_tier | string | Told to student when denied |
| user_tier | string | Confirmed in explanation |

---

## Tutor Action → Backend Endpoint Map

| Tutor Action | HTTP Call | When |
|--------------|-----------|------|
| Find relevant chapter | `GET /search?q={keyword}` | Student asks topic question |
| Check access | `GET /access/check?chapter_id={id}` | Before every chapter fetch |
| Fetch chapter | `GET /chapters/{id}` | After access confirmed |
| Start quiz | `GET /quizzes/{chapter_id}` | Student says "quiz me" |
| Submit answer | `POST /quizzes/{quiz_id}/submit` | After each student answer |
| Show progress | `GET /progress/{user_id}` | Student asks "how am I doing?" |
