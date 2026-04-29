# Quickstart: Phase 2 — Course Content Seeding

## Prerequisites

- Phase 1 backend complete (Supabase tables exist)
- `.env` at project root with `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`
- Python venv active: `source backend/.venv/bin/activate`

---

## Run the Seeding Script

```bash
cd backend
python3 seed.py
```

Expected output:
```
Seeding chapters...
✓ Upserted 10 chapters
Seeding quizzes...
✓ Upserted 50 quiz questions
Seeding complete.
```

---

## Verify via API

With the backend running (`uvicorn main:app --reload`):

### Check all 10 chapters exist
```bash
curl -s http://localhost:8000/chapters -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'Total chapters: {len(d)}')
for c in d:
    print(f'  [{c[\"tier\"]:8}] Ch{c[\"order_num\"]}: {c[\"title\"]}')
"
```
Expected: 10 chapters, tiers match (free/premium/pro).

### Check all 10 chapters have content
```bash
for i in $(seq 1 10); do
  CONTENT=$(curl -s http://localhost:8000/chapters/$i \
    -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json; d=json.load(sys.stdin)
words = len(d.get('content','').split())
print(f'Ch{d[\"order_num\"]}: {words} words')
")
  echo $CONTENT
done
```
Expected: Each chapter has 500+ words.

### Check all 50 quiz questions
```bash
total=0
for i in $(seq 1 10); do
  count=$(curl -s "http://localhost:8000/quizzes/$i" \
    -H "Authorization: Bearer $TOKEN" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")
  echo "Chapter $i: $count questions"
  total=$((total + count))
done
echo "Total: $total questions (expected 50)"
```
Expected: 5 per chapter, 50 total.

### Verify idempotency (safe to re-run)
```bash
python3 seed.py   # run again
# Then re-check counts — should still be exactly 10 chapters, 50 questions
```
