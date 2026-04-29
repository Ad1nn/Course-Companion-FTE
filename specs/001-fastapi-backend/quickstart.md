# Quickstart: Phase 1 — FastAPI Backend

## Prerequisites

- Python 3.11+
- `.env` at project root with `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`, `ADMIN_SECRET`
- Supabase project with 5 tables created (chapters, quizzes, users, progress, llm_costs)

---

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Run Locally

```bash
cd backend
uvicorn main:app --reload --port 8000
```

API available at: `http://localhost:8000`
Swagger docs at: `http://localhost:8000/docs`

---

## Smoke Test — Full Student Journey

Run these in order to verify all endpoints work end-to-end.

### 1. Register a student
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```
Expected: `{"user_id": "...", "email": "test@example.com", "tier": "free"}`

### 2. Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```
Expected: `{"access_token": "...", "user_id": "...", "tier": "free"}`

Save the token: `TOKEN=<access_token from above>`

### 3. List chapters
```bash
curl http://localhost:8000/chapters \
  -H "Authorization: Bearer $TOKEN"
```
Expected: Array of 10 chapters (no `content` field)

### 4. Read a free chapter
```bash
curl http://localhost:8000/chapters/1 \
  -H "Authorization: Bearer $TOKEN"
```
Expected: Chapter with `content` field populated

### 5. Try a locked chapter (free user)
```bash
curl http://localhost:8000/chapters/4 \
  -H "Authorization: Bearer $TOKEN"
```
Expected: `403` with `required_tier: "premium"`

### 6. Get quiz questions
```bash
curl http://localhost:8000/quizzes/1 \
  -H "Authorization: Bearer $TOKEN"
```
Expected: 5 questions — verify `correct_answer` is NOT in any question object

### 7. Submit a quiz answer
```bash
curl -X POST http://localhost:8000/quizzes/1/submit \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "<your_user_id>", "answer": "B"}'
```
Expected: `{"correct": true/false, "correct_answer": "...", "explanation": "..."}`

### 8. Check progress
```bash
curl http://localhost:8000/progress/<your_user_id> \
  -H "Authorization: Bearer $TOKEN"
```
Expected: Progress object with chapters array

### 9. Search content
```bash
curl "http://localhost:8000/search?q=agent" \
  -H "Authorization: Bearer $TOKEN"
```
Expected: Up to 5 results with `excerpt` field

### 10. Admin tier upgrade
```bash
curl -X POST http://localhost:8000/admin/upgrade \
  -H "ADMIN_SECRET: hackathon-admin-2026" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "<your_user_id>", "tier": "premium"}'
```
Expected: `{"message": "User upgraded to premium"}`

### 11. Re-test locked chapter (now premium)
```bash
# Login again to get fresh token with updated tier
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Then access premium chapter
curl http://localhost:8000/chapters/4 \
  -H "Authorization: Bearer $NEW_TOKEN"
```
Expected: Full chapter content returned

---

## Verify Zero LLM Calls

```bash
curl -X POST http://localhost:8000/hybrid/adaptive-path \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "<your_user_id>"}'
```
Expected: `501 Not Implemented`

---

## Deploy to Railway

1. Push repo to GitHub
2. Create new Railway project → connect GitHub repo
3. Set root directory to `backend`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`, `ADMIN_SECRET`
6. Deploy and test with the Railway URL
