# API Contracts: Next.js Web App → FastAPI Backend

**Date**: 2026-04-28 | **Branch**: `004-nextjs-web-app`

> The web app is a consumer of the existing FastAPI backend. All calls are defined in `src/lib/api.ts`. No new backend endpoints are introduced by this phase.
>
> Full backend schema: `chatgpt-app/openapi.yaml`  
> Base URL env var: `NEXT_PUBLIC_API_BASE_URL` (e.g. `https://course-companion.railway.app`)

---

## Auth Header (all protected calls)

```
Authorization: Bearer <session.access_token>
```

Obtained from `supabase.auth.getSession()` → `session.access_token`.

---

## Endpoint 1 — Chapter List

> Used by: `/chapters` page (chapter list)

```
GET /chapters
```

**Note**: The existing backend has a `/search?q=` endpoint and a `/chapters/{id}` endpoint. The chapter list page needs all 10 chapters. If no `GET /chapters` list endpoint exists, the frontend calls `/search?q=` with a broad term or fetches chapters 1–10 individually.

**Preferred resolution**: Implement `GET /chapters` in the backend (returns all 10 `ChapterSummary` objects) — OR — the frontend fetches chapters by calling `/chapters/1` through `/chapters/10` on the list page. The latter adds 10 sequential requests; the former is cleaner.

**Decision for implementation**: Call `GET /chapters` — add this endpoint to backend if not present, or substitute with individual fetches if time-constrained.

**Response** (array of ChapterSummary):
```json
[
  {
    "id": 1,
    "title": "Introduction to AI Agents",
    "description": "Overview of AI agents and agentic frameworks.",
    "tier": "free",
    "order_num": 1
  }
]
```

---

## Endpoint 2 — Access Check

> Used by: `/chapters/[id]` page (before rendering content)

```
GET /access/check?chapter_id={id}
Authorization: Bearer <token>
```

**Response**:
```json
{ "allowed": true }
// or
{ "allowed": false, "required_tier": "premium", "user_tier": "free" }
```

**Frontend action**:
- `allowed: true` → render `<ChapterContent content={...} />`
- `allowed: false` → render `<LockedOverlay requiredTier={...} />`

---

## Endpoint 3 — Chapter Full Content

> Used by: `/chapters/[id]` page (only when `allowed: true`)

```
GET /chapters/{id}
Authorization: Bearer <token>
```

**Response** (ChapterFull):
```json
{
  "id": 1,
  "title": "Introduction to AI Agents",
  "description": "...",
  "content": "# Introduction\n\nAI agents are...",
  "order_num": 1,
  "tier": "free"
}
```

**Error responses**:
- `403` → locked (should not happen if `/access/check` was called first; handle defensively)
- `404` → chapter not found → show error message

---

## Endpoint 4 — Quiz Questions

> Used by: `/quiz/[id]` page on load

```
GET /quizzes/{chapter_id}
Authorization: Bearer <token>
```

**Response** (array of 5 QuizQuestion — `correct_answer` NEVER present):
```json
[
  {
    "id": 1,
    "chapter_id": 1,
    "question": "What is an AI agent?",
    "option_a": "A static script",
    "option_b": "A system that perceives and acts",
    "option_c": "A trained model only",
    "option_d": "A database query",
    "order_num": 1
  }
]
```

---

## Endpoint 5 — Submit Quiz Answer

> Used by: `/quiz/[id]` page on each answer submission

```
POST /quizzes/{quiz_id}/submit
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": "<uuid>",
  "answer": "B"
}
```

**Response** (SubmitResult):
```json
{
  "correct": true,
  "correct_answer": "B",
  "explanation": "An AI agent perceives its environment and takes actions...",
  "score": null
}
// After 5th question:
{
  "correct": false,
  "correct_answer": "C",
  "explanation": "...",
  "score": 80
}
```

**Frontend action**:
- `correct: true` → colour selected option green
- `correct: false` → colour selected option red, highlight `correct_answer` green
- Always show `explanation`
- If `score` present → transition to `<ScoreScreen score={score} />`

---

## Endpoint 6 — Progress

> Used by: `/progress` page and `/dashboard` page

```
GET /progress/{user_id}
Authorization: Bearer <token>
```

**Response** (ProgressRecord):
```json
{
  "tier": "free",
  "streak_days": 3,
  "avg_score": 80.0,
  "chapters_completed": 2,
  "chapters": [
    { "chapter_id": 1, "title": "Introduction to AI Agents", "completed": true, "score": 80, "attempts": 1 },
    { "chapter_id": 2, "title": "OpenAI Agents SDK", "completed": true, "score": 100, "attempts": 2 },
    { "chapter_id": 3, "title": "Anthropic Claude Agent SDK", "completed": false, "score": null, "attempts": 0 }
  ]
}
```

---

## Error Handling Contract (all endpoints)

| HTTP Status | Frontend Behaviour |
|-------------|-------------------|
| `200` | Render data |
| `403` | Show locked overlay (chapters) or upgrade prompt (quiz) |
| `404` | Show "not found" inline error message |
| `401` | Clear session, redirect to `/login` |
| `5xx` / Network error | Show "Something went wrong — please try again" toast |

---

## `src/lib/api.ts` — Function Signatures

```typescript
const BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

async function getChapters(token: string): Promise<ChapterSummary[]>
async function checkAccess(token: string, chapterId: number): Promise<AccessResult>
async function getChapter(token: string, id: number): Promise<ChapterFull>
async function getQuizQuestions(token: string, chapterId: number): Promise<QuizQuestion[]>
async function submitAnswer(token: string, quizId: number, userId: string, answer: string): Promise<SubmitResult>
async function getProgress(token: string, userId: string): Promise<ProgressRecord>
```

All functions throw `ApiError` on non-2xx responses, with `.status` and `.message` fields.
