# Research: Phase 2 — Course Content Seeding

**Branch**: `002-content-seeding` | **Date**: 2026-04-28

No unknowns. All decisions are straightforward given the constraints.

---

## Decision 1: Content Authored Inline (not fetched from textbook API)

**Decision**: Chapter content written as Python strings directly in `seed.py`.

**Rationale**: The Panaversity textbook is not available via a public API. Content must
be authored manually as educational summaries of each chapter topic. This is faster
than scraping and produces content optimised for the ChatGPT tutor use case.
Each chapter targets 600–1000 words — enough for ChatGPT to teach from, not so much
that it overwhelms context windows.

**Alternatives considered**:
- Scraping the textbook website — requires auth, fragile, risk of ToS violation.
- External LLM to generate content — violates Constitution Principle I (no LLM calls)
  and produces unverified content.

---

## Decision 2: Upsert via chapter `id` for idempotency

**Decision**: Use `supabase.table("chapters").upsert(data)` with explicit `id` fields
(1–10). For quizzes, upsert on `(chapter_id, order_num)` composite.

**Rationale**: Allows the script to be re-run safely without duplicating rows. If content
is improved, re-running the script updates the existing rows in place.

**Alternatives considered**:
- Delete-then-insert — loses any manually-added rows; destructive.
- Insert with conflict ignore — doesn't update existing rows if content changes.

---

## Decision 3: Single `backend/seed.py` script, no CLI args

**Decision**: `python3 seed.py` seeds everything. No flags, no partial seeding.

**Rationale**: 10 chapters and 50 questions is small enough that always seeding
everything is simpler than partial seeding. Constitution Principle V: smallest viable
solution.
