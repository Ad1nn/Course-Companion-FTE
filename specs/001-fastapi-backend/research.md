# Research: Phase 1 — FastAPI Backend

**Branch**: `001-fastapi-backend` | **Date**: 2026-04-28

No NEEDS CLARIFICATION items were identified — the project plan provides complete
endpoint contracts, database schema, and tech stack decisions. This document records
the key decisions and rationale for reference.

---

## Decision 1: Supabase Python Client for All DB Access

**Decision**: Use `supabase-py` (official Supabase Python SDK) for all database reads
and writes, with the `service_role` key on the server side.

**Rationale**: The service role key bypasses Row Level Security, eliminating the need
to write and maintain RLS policies for the hackathon scope. All access control is
enforced in application code (route handlers), not at the database level.

**Alternatives considered**:
- `asyncpg` direct PostgreSQL — more performant but requires managing connection pools
  and writing raw SQL. Not worth the complexity for hackathon scale.
- `SQLAlchemy` ORM — adds migration tooling and type safety but significant setup
  overhead for 5 simple tables.

---

## Decision 2: JWT Validation via Supabase Auth

**Decision**: Validate every protected request by calling `supabase.auth.get_user(token)`
with the bearer token extracted from the `Authorization` header.

**Rationale**: Supabase Auth issues and validates JWTs. Using their SDK to verify tokens
means we don't need to manage JWT secrets, public keys, or expiry logic ourselves.

**Alternatives considered**:
- `python-jose` / `PyJWT` manual validation — requires sharing the JWT secret and
  handling algorithm selection. Adds risk; Supabase SDK is safer.

---

## Decision 3: No Caching Layer

**Decision**: No Redis or in-memory cache. Every request hits Supabase directly.

**Rationale**: Hackathon demo with single-digit concurrent users. Chapter content is
static after seeding. Adding a cache layer adds operational complexity with no
measurable benefit at this scale.

**Alternatives considered**:
- In-process dict cache for chapters — rejected; premature optimization. Can be added
  in Phase 5 if needed.

---

## Decision 4: No Service Layer — Routes Call Supabase Directly

**Decision**: Route handlers call the Supabase client directly. No intermediate service
or repository classes.

**Rationale**: Five endpoint groups, each with 1–3 operations. Abstracting into service
classes would add 5 extra files with no reuse benefit. Constitution Principle V
(Smallest Viable Diff) explicitly prohibits this for one-time operations.

---

## Decision 5: Streak Calculation in Application Code

**Decision**: Calculate `streak_days` in the `GET /progress/{user_id}` route handler
by querying `completed_at` timestamps from the `progress` table and counting consecutive
calendar days.

**Rationale**: The `progress` table already stores `completed_at` timestamps. A simple
Python sort-and-diff algorithm on the returned rows avoids a complex SQL window function.
Acceptable for ≤10 chapters per user.

---

## Decision 6: Search via Supabase `ilike` (not PostgreSQL FTS)

**Decision**: Implement `GET /search` using Supabase `.ilike()` filter on `title` and
`content` columns, returning up to 5 results with a Python-generated excerpt.

**Rationale**: PostgreSQL full-text search requires adding a `tsvector` column and
GIN index — setup overhead not worth it for 10 chapters. `ilike` on 10 rows is
instantaneous. The excerpt is a 150-char substring around the first keyword match.

**Alternatives considered**:
- PostgreSQL `to_tsvector` FTS — better ranking for large corpora; overkill for 10 chapters.
- Supabase text search extension — same overhead concern.
