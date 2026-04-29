# API Contracts: Phase 1 — FastAPI Backend

**Base URL (local)**: `http://localhost:8000`
**Base URL (production)**: `https://course-companion.railway.app`
**Auth**: All protected routes require `Authorization: Bearer <JWT>` header.

---

## Auth Endpoints

### POST /auth/register

Creates a new student account.

**Auth**: None required

**Request body:**
```json
{
  "email": "student@example.com",
  "password": "securepassword123"
}
```

**Response 200:**
```json
{
  "user_id": "uuid",
  "email": "student@example.com",
  "tier": "free"
}
```

**Response 400:** Duplicate email or invalid input
```json
{ "detail": "Email already registered" }
```

---

### POST /auth/login

Authenticates an existing student.

**Auth**: None required

**Request body:**
```json
{
  "email": "student@example.com",
  "password": "securepassword123"
}
```

**Response 200:**
```json
{
  "access_token": "<jwt>",
  "user_id": "uuid",
  "tier": "free"
}
```

**Response 401:**
```json
{ "detail": "Invalid credentials" }
```

---

## Chapter Endpoints

### GET /chapters

Returns all 10 chapters (summary only — no content field).

**Auth**: Required

**Response 200:**
```json
[
  {
    "id": 1,
    "title": "Introduction to AI Agents",
    "description": "Learn what AI agents are and how they work.",
    "order_num": 1,
    "tier": "free"
  }
]
```

**Response 401:** Missing or invalid token

---

### GET /chapters/{id}

Returns a single chapter with full content. Enforces tier access.

**Auth**: Required

**Response 200:**
```json
{
  "id": 4,
  "title": "MCP Fundamentals",
  "description": "...",
  "content": "Full chapter text...",
  "order_num": 4,
  "tier": "premium"
}
```

**Response 403:** User tier insufficient
```json
{
  "detail": "Access denied",
  "required_tier": "premium",
  "user_tier": "free",
  "message": "Chapter 4 requires a Premium subscription."
}
```

**Response 404:** Chapter not found

---

### GET /chapters/{id}/next

Returns the next chapter object (summary). Skips inaccessible chapters.

**Auth**: Required

**Response 200:** Same shape as ChapterSummary
**Response 404:** No next chapter exists

---

### GET /chapters/{id}/prev

Returns the previous chapter object (summary).

**Auth**: Required

**Response 200:** Same shape as ChapterSummary
**Response 404:** No previous chapter exists

---

## Search Endpoint

### GET /search?q={keyword}

Full-text search across chapter titles and content.

**Auth**: Required

**Query params:**
- `q` (required): search keyword, 1–100 chars

**Response 200:**
```json
[
  {
    "id": 4,
    "title": "MCP Fundamentals",
    "excerpt": "...MCP (Model Context Protocol) defines how agents communicate with tools...",
    "tier": "premium"
  }
]
```

Max 5 results. Empty array if no matches.

**Response 400:** Missing or empty `q` parameter

---

## Quiz Endpoints

### GET /quizzes/{chapter_id}

Returns all 5 questions for a chapter. `correct_answer` is NEVER included.

**Auth**: Required

**Response 200:**
```json
[
  {
    "id": 1,
    "chapter_id": 1,
    "question": "What is an AI agent?",
    "option_a": "A chatbot",
    "option_b": "A system that perceives and acts autonomously",
    "option_c": "A search engine",
    "option_d": "A database",
    "order_num": 1
  }
]
```

**Response 404:** Chapter not found

---

### POST /quizzes/{quiz_id}/submit

Submits a student's answer to a single quiz question.

**Auth**: Required

**Request body:**
```json
{
  "user_id": "uuid",
  "answer": "B"
}
```

**Response 200 (non-final question):**
```json
{
  "correct": true,
  "correct_answer": "B",
  "explanation": "An AI agent perceives its environment and takes autonomous actions."
}
```

**Response 200 (final / 5th question):**
```json
{
  "correct": false,
  "correct_answer": "A",
  "explanation": "...",
  "score": 80
}
```

**Response 400:** Answer not one of A/B/C/D
**Response 404:** Quiz question not found

---

## Progress Endpoints

### GET /progress/{user_id}

Returns complete progress for a student.

**Auth**: Required (must match user_id or be admin)

**Response 200:**
```json
{
  "tier": "free",
  "streak_days": 3,
  "avg_score": 80.0,
  "chapters_completed": 1,
  "chapters": [
    {
      "chapter_id": 1,
      "title": "Introduction to AI Agents",
      "completed": true,
      "score": 80,
      "attempts": 1
    }
  ]
}
```

**Response 404:** User not found

---

### PUT /progress/{user_id}

Upserts a chapter progress record.

**Auth**: Required

**Request body:**
```json
{
  "chapter_id": 1,
  "completed": true,
  "score": 80
}
```

**Response 200:**
```json
{ "message": "Progress updated" }
```

---

## Access Endpoint

### GET /access/check?chapter_id={id}

Checks if the authenticated student can access a chapter.

**Auth**: Required

**Response 200 (allowed):**
```json
{ "allowed": true }
```

**Response 200 (denied):**
```json
{
  "allowed": false,
  "required_tier": "premium",
  "user_tier": "free"
}
```

---

## Admin Endpoint

### POST /admin/upgrade

Upgrades a student's subscription tier. Requires `ADMIN_SECRET` header.

**Auth**: `ADMIN_SECRET` header (not JWT)

**Headers:**
```
ADMIN_SECRET: <secret>
```

**Request body:**
```json
{
  "user_id": "uuid",
  "tier": "premium"
}
```

**Response 200:**
```json
{ "message": "User upgraded to premium" }
```

**Response 403:** Missing or wrong ADMIN_SECRET

---

## Hybrid Endpoints (Phase 5 Stubs)

### POST /hybrid/adaptive-path
### POST /hybrid/assess

Both return:

**Response 501:**
```json
{ "detail": "Not implemented — available in Phase 5" }
```

---

## Error Response Format

All errors follow FastAPI default:
```json
{ "detail": "<human-readable message>" }
```

For tier errors on `/chapters/{id}`, the response includes extra fields:
```json
{
  "detail": "Access denied",
  "required_tier": "premium",
  "user_tier": "free",
  "message": "Chapter 4 requires a Premium subscription."
}
```
