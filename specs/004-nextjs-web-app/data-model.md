# Data Model: Next.js Web App — LMS Dashboard

**Date**: 2026-04-28 | **Branch**: `004-nextjs-web-app`

> The web app has no local database. All persistent data lives in Supabase and is accessed exclusively through the FastAPI backend. This document describes the **TypeScript types** used to represent backend responses in the frontend, and the **client-side state** models for quiz flow.

---

## Backend Response Types (read-only, from FastAPI)

These types mirror the schemas in `chatgpt-app/openapi.yaml`. They are defined in `src/lib/api.ts`.

### ChapterSummary
```typescript
interface ChapterSummary {
  id: number;           // Chapter ID (1–10)
  title: string;        // Chapter title
  excerpt?: string;     // Short snippet from search (may be absent from list endpoint)
  tier: 'free' | 'premium' | 'pro';  // Minimum tier required
}
```

### ChapterFull
```typescript
interface ChapterFull {
  id: number;
  title: string;
  description: string;  // 2-sentence summary
  content: string;      // Full Markdown text — NEVER rendered for locked chapters
  order_num: number;    // 1–10
  tier: 'free' | 'premium' | 'pro';
}
```

### AccessResult
```typescript
interface AccessResult {
  allowed: boolean;
  required_tier?: 'free' | 'premium' | 'pro';
  user_tier?: 'free' | 'premium' | 'pro';
}
```

### QuizQuestion
```typescript
interface QuizQuestion {
  id: number;           // Use this as quiz_id when submitting
  chapter_id: number;
  question: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  order_num: number;    // 1–5
  // Note: correct_answer is NEVER returned by GET /quizzes/{chapter_id}
}
```

### SubmitResult
```typescript
interface SubmitResult {
  correct: boolean;
  correct_answer: 'A' | 'B' | 'C' | 'D';
  explanation: string;
  score?: number;       // 0–100, only present after question 5
}
```

### ProgressRecord
```typescript
interface ProgressRecord {
  tier: 'free' | 'premium' | 'pro';
  streak_days: number;
  avg_score: number;        // 0–100
  chapters_completed: number;
  chapters: ChapterProgress[];
}

interface ChapterProgress {
  chapter_id: number;
  title: string;
  completed: boolean;
  score: number | null;     // null if not attempted
  attempts: number;
}
```

---

## Client-Side State Models

### AuthSession (managed by Supabase, read by app)

```typescript
// Accessed via supabase.auth.getSession() or onAuthStateChange
interface AuthSession {
  user: {
    id: string;           // UUID — passed to /progress/{user_id} and quiz submit
    email: string;
    user_metadata: {
      tier?: 'free' | 'premium' | 'pro';  // Set by admin endpoint; default 'free'
    };
  };
  access_token: string;   // JWT — sent as Bearer token to FastAPI
}
```

### QuizState (useState in quiz/[id]/page.tsx)

```typescript
interface QuizState {
  questions: QuizQuestion[];      // All 5 questions, fetched on page load
  currentIndex: number;           // 0-based, current question shown
  selectedAnswer: 'A' | 'B' | 'C' | 'D' | null;
  submitted: boolean;             // True after "Submit Answer" clicked
  result: SubmitResult | null;    // Backend response for submitted answer
  finalScore: number | null;      // Populated after question 5 (from result.score)
  isComplete: boolean;            // True when all 5 questions answered
}
```

**State transitions:**
```
LOADING (fetch questions)
  → QUESTION (show currentIndex question, selectedAnswer=null, submitted=false)
  → SUBMITTED (show result, explanation, colour feedback)
    → if currentIndex < 4: back to QUESTION (increment currentIndex)
    → if currentIndex === 4: COMPLETE (show score screen)
```

---

## Relationships (Frontend View)

```
AuthSession.user.id
  ├── used in: POST /quizzes/{id}/submit (body.user_id)
  └── used in: GET /progress/{user_id}

ChapterSummary[]
  └── displayed on: /chapters (chapter list page)

ChapterFull
  ├── content rendered on: /chapters/[id] (if allowed)
  └── blocked by: AccessResult.allowed === false → LockedOverlay shown

QuizQuestion[] (5 per chapter)
  └── answered via: SubmitResult (one per question)
      └── score (on 5th): written to progress via backend

ProgressRecord
  └── displayed on: /progress and /dashboard
```

---

## Tier Access Rules (Frontend Display Logic)

| Chapter Range | Required Tier | Badge Colour |
|---------------|---------------|--------------|
| 1–3           | free          | green        |
| 4–7           | premium       | violet       |
| 8–10          | pro           | gold/amber   |

> **Note**: These are display hints only. The backend is the authoritative access enforcer. Frontend never makes access decisions — it shows the LockedOverlay based on the `/access/check` response or a 403 from `/chapters/{id}`.
