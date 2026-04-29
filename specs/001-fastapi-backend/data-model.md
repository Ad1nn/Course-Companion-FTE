# Data Model: Phase 1 — FastAPI Backend

**Branch**: `001-fastapi-backend` | **Date**: 2026-04-28

---

## Entities

### Chapter

Represents a single course unit. Content is the full concatenated text from 3 textbook
sub-pages. Content is intentionally NOT returned in list endpoints.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | integer | PK, auto-increment | |
| title | text | NOT NULL | Displayed in chapter list and sidebar |
| description | text | nullable | 2-sentence summary for chapter cards |
| content | text | NOT NULL | Full text; only returned in `/chapters/{id}` |
| order_num | integer | NOT NULL, UNIQUE | 1–10; determines prev/next navigation |
| tier | text | DEFAULT 'free' | One of: `free` \| `premium` \| `pro` |

**Tier access rules:**
- `free` → accessible to all tiers
- `premium` → requires `premium` or `pro`
- `pro` → requires `pro` only

**Tier hierarchy:** `free < premium < pro`

---

### Quiz

Represents one multiple-choice question within a chapter's quiz. Each chapter has
exactly 5 quiz questions.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | integer | PK, auto-increment | |
| chapter_id | integer | FK → chapters.id | |
| question | text | NOT NULL | The question text |
| option_a | text | NOT NULL | |
| option_b | text | NOT NULL | |
| option_c | text | NOT NULL | |
| option_d | text | NOT NULL | |
| correct_answer | text | NOT NULL | One of: `A` \| `B` \| `C` \| `D` |
| explanation | text | NOT NULL | Shown after answer submitted |
| order_num | integer | nullable | 1–5; question ordering within chapter |

**Critical rule:** `correct_answer` is NEVER returned by `GET /quizzes/{chapter_id}`.
It is only used server-side during `POST /quizzes/{quiz_id}/submit`.

---

### User

Application-level user record linked to the Supabase Auth `auth.users` table.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid | PK, FK → auth.users | Set by Supabase Auth on registration |
| email | text | NOT NULL | Copied from auth.users at register time |
| tier | text | DEFAULT 'free' | One of: `free` \| `premium` \| `pro` |
| created_at | timestamp | DEFAULT now() | |

---

### Progress

Tracks a student's progress on a per-chapter basis. One row per (user, chapter) pair.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | integer | PK, auto-increment | |
| user_id | uuid | FK → users.id | |
| chapter_id | integer | FK → chapters.id | |
| completed | boolean | DEFAULT false | True when all 5 quiz questions answered |
| score | integer | nullable | Percentage 0–100; set on final quiz submission |
| attempts | integer | DEFAULT 0 | Incremented each time quiz is fully submitted |
| last_accessed | timestamp | DEFAULT now() | Updated on each chapter access |
| completed_at | timestamp | nullable | Set when `completed` transitions to true |
| — | — | UNIQUE(user_id, chapter_id) | One row per student per chapter |

**Streak calculation**: Query all `progress` rows for a user where `completed = true`,
extract `completed_at` dates, sort descending, count consecutive calendar days.

---

### LLM Cost

Audit log for Phase 5 AI feature usage. Created now; unused in Phase 1.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | integer | PK, auto-increment | |
| user_id | uuid | FK → users.id | |
| feature | text | nullable | `adaptive_path` \| `assessment` |
| tokens_in | integer | nullable | |
| tokens_out | integer | nullable | |
| cost_usd | numeric(10,6) | nullable | |
| created_at | timestamp | DEFAULT now() | |

---

## Pydantic Response Models (Phase 1)

### ChapterSummary (used in GET /chapters)
```python
id, title, description, order_num, tier
# content is excluded
```

### ChapterDetail (used in GET /chapters/{id})
```python
id, title, description, content, order_num, tier
```

### QuizQuestion (used in GET /quizzes/{chapter_id})
```python
id, chapter_id, question, option_a, option_b, option_c, option_d, order_num
# correct_answer is excluded
```

### SubmitResponse (used in POST /quizzes/{id}/submit)
```python
correct: bool
correct_answer: str       # A | B | C | D
explanation: str
score: int | None         # Only present on final (5th) question
```

### ProgressResponse (used in GET /progress/{user_id})
```python
tier: str
streak_days: int
avg_score: float
chapters_completed: int
chapters: list[ChapterProgress]

# ChapterProgress:
chapter_id: int
title: str
completed: bool
score: int | None
attempts: int
```

### AuthRegisterResponse
```python
user_id: str
email: str
tier: str
```

### AuthLoginResponse
```python
access_token: str
user_id: str
tier: str
```

### AccessCheckResponse
```python
allowed: bool
required_tier: str | None   # Only when allowed=False
user_tier: str | None       # Only when allowed=False
```

### SearchResult (used in GET /search)
```python
id: int
title: str
excerpt: str    # ~150 chars around keyword match
tier: str
```
