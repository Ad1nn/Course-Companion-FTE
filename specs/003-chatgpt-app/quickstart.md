# Quickstart: Phase 3 — ChatGPT App Registration & Testing

## Prerequisites

- Phase 1 backend deployed and running on Railway (`https://course-companion.railway.app`)
- Phase 2 content seeded (10 chapters, 50 questions in Supabase)
- OpenAI account with access to GPT Builder (ChatGPT Plus or Team)
- Demo user account created via `POST /auth/login`

---

## Step 1: Get Demo JWT

```bash
curl -s -X POST https://course-companion.railway.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@coursecompanion.ai", "password": "<demo-password>"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('user_id:', d['user_id']); print('token:', d['access_token'])"
```

Save the `access_token` and `user_id` — you will need both during GPT registration.

---

## Step 2: Validate the OpenAPI Schema

Before uploading, verify the schema is valid:

```bash
# Install npx if needed, then:
npx @redocly/cli lint chatgpt-app/openapi.yaml
```

Expected: 0 errors, 0 warnings.

Also smoke-test a key endpoint with the demo JWT:

```bash
TOKEN="<your-access-token>"

# Test search
curl -s "https://course-companion.railway.app/search?q=MCP" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Test access check
curl -s "https://course-companion.railway.app/access/check?chapter_id=1" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Test chapter fetch
curl -s "https://course-companion.railway.app/chapters/1" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(f'Chapter: {d[\"title\"]}')
print(f'Words: {len(d[\"content\"].split())}')
"
```

---

## Step 3: Register the GPT

1. Go to **chatgpt.com** → click your profile → **My GPTs** → **Create a GPT**
2. Click **Configure** tab (not the chat builder)
3. Fill in:
   - **Name**: `Course Companion — Agentic AI Tutor`
   - **Description**: `Your 24/7 AI tutor for Agentic AI development. Teaches 10 chapters, runs quizzes, and tracks your progress.`
   - **Instructions**: Paste full contents of `chatgpt-app/system-prompt.md`
4. Scroll to **Actions** → click **Add Action** → **Import from URL** or paste the contents of `chatgpt-app/openapi.yaml`
5. Under **Authentication**:
   - Type: **API Key**
   - Auth Type: **Bearer**
   - API Key: paste your demo `access_token`
6. Click **Save** → set visibility to **Anyone with the link** (for demo sharing)

---

## Step 4: Test All Three User Story Flows

Open a fresh chat with your registered GPT.

### US1 — Teaching Flow

```
You: What is the agent loop?
Expected: Tutor searches, finds Chapter 1, explains the Perceive→Reason→Act loop using chapter content.

You: Tell me about blockchain
Expected: "That topic isn't covered in this course."

You: Explain RAG
Expected: Tutor finds Chapter 8, explains Retrieval-Augmented Generation from chapter content.
```

### US1 — Access Control (requires free-tier demo account)

```
You: Tell me about MCP
Expected: "Chapter 4 (MCP Fundamentals) requires a Premium plan. You can upgrade at [url]."
         Tutor does NOT reveal any chapter 4 content.
```

### US2 — Quiz Flow

```
You: Quiz me on chapter 1
Expected: Question 1 of 5 appears. Tutor waits.

You: B
Expected: Correct/incorrect feedback + explanation. Question 2 appears.

[Continue through all 5 questions]
Expected: Final score shown (e.g., "4 out of 5 — 80%"). Progress saved confirmed.
```

### US3 — Progress Flow

```
You: How am I doing?
Expected: Chapters completed, scores, streak, avg score. Suggestion for next chapter.

You: [If no quiz done yet] How am I doing?
Expected: Warm encouragement to start Chapter 1.
```

---

## Step 5: Verify Progress Was Saved

```bash
USER_ID="<your-demo-user-id>"
TOKEN="<your-access-token>"

curl -s "https://course-companion.railway.app/progress/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Expected: Chapter 1 shows `"completed": true` and the score from the quiz.

---

## Verification Checklist

- [ ] GPT registered and accessible via share link
- [ ] Teaching flow: chapter 1 explained using fetched content
- [ ] Teaching flow: off-topic question gracefully declined
- [ ] Access control: premium chapter blocked for free-tier user
- [ ] Quiz flow: all 5 questions answered one at a time, score displayed
- [ ] Progress flow: accurate stats returned and next chapter suggested
- [ ] Progress saved: `GET /progress` confirms quiz score persisted
