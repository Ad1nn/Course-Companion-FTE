# Research: Next.js Web App — LMS Dashboard

**Date**: 2026-04-28 | **Branch**: `004-nextjs-web-app`

---

## Decision 1: Next.js App Router vs Pages Router

**Decision**: Next.js 14 App Router  
**Rationale**: App Router is the current Next.js default and supports route groups `(public)` / `(protected)` for clean auth boundary separation. Nested layouts allow the chapter sidebar to be mounted once and shared across chapter reader routes. Server Components reduce bundle size for data-heavy pages.  
**Alternatives considered**:
- Pages Router: Stable, well-documented, but no native route groups — auth protection requires per-page HOC pattern, more boilerplate. Deprecated direction.
- Remix: Excellent data loading model but not in the constitution's tech stack.

---

## Decision 2: Supabase Auth Integration Pattern — `@supabase/ssr`

**Decision**: `@supabase/ssr` for middleware + server components; `@supabase/supabase-js` browser client for client components  
**Rationale**: `@supabase/ssr` is the official Supabase package for Next.js App Router. It handles cookie-based session persistence correctly in the App Router's server/client component split. Without SSR, Supabase sessions can be lost on server renders. The browser client is used only in client components that need auth state reactively (e.g., login/signup forms).  
**Alternatives considered**:
- `@supabase/supabase-js` only: Works in client components but causes hydration mismatches and no server-side session validation.
- NextAuth.js: Overkill; we're using Supabase Auth specifically to share the same session mechanism as the FastAPI backend (which validates the same JWTs).

---

## Decision 3: Route Protection — Middleware vs Per-Page Check

**Decision**: Next.js Middleware (`src/middleware.ts`) for route protection  
**Rationale**: Middleware runs at the edge before any page renders — no flash of protected content. A single matcher pattern `/(dashboard|chapters|quiz|progress)/:path*` covers all protected routes. The middleware reads the Supabase session from cookies and redirects to `/login` if absent. This is the pattern recommended in the official Supabase + Next.js documentation.  
**Alternatives considered**:
- Per-page `useEffect` redirect: Client-side, causes flash of protected content before redirect.
- Per-page Server Component session check: Works but duplicates logic across every protected page.

---

## Decision 4: API Call Layer — `src/lib/api.ts`

**Decision**: Centralized typed API client module (`src/lib/api.ts`)  
**Rationale**: All 6 FastAPI endpoints are called from multiple pages. A single module with typed return values (matching the OpenAPI schemas in `chatgpt-app/openapi.yaml`) eliminates duplicated fetch boilerplate, centralizes the base URL and token injection, and makes mock-swapping trivial for demos. Functions are async and throw on non-2xx responses.  
**Alternatives considered**:
- React Query / SWR: Adds caching, deduplication, and loading states — useful for production but adds a dependency. Not needed for hackathon where pages are short-lived and data staleness is acceptable.
- Direct fetch in each page: Works but duplicates the Authorization header injection and error handling on every call.

---

## Decision 5: Quiz State — `useState` Only

**Decision**: React `useState` within the quiz page component for all quiz state  
**Rationale**: Quiz state (questions list, current index, selected answer, submitted flag, results, final score) lives for the duration of a single quiz session. It resets on page navigation, which is acceptable per the spec's edge case: "partial answers are lost on session expiry — acceptable for hackathon scope." Using Zustand or Context would add a dependency and coupling with no benefit.  
**Alternatives considered**:
- Zustand: Better for cross-page state sharing; unnecessary here since quiz state is page-local.
- URL params for question index: Makes browser back/forward work for quiz navigation; adds complexity without spec requirement.

---

## Decision 6: Content Rendering — `react-markdown`

**Decision**: `react-markdown` for chapter content  
**Rationale**: Chapter `content` field is Markdown text (per ChapterFull schema). `react-markdown` is a lightweight, well-maintained renderer with plugin support for syntax highlighting (via `rehype-highlight` if needed). Tailwind's `@tailwindcss/typography` (`prose` class) provides good default styling for rendered Markdown.  
**Alternatives considered**:
- `dangerouslySetInnerHTML` with a Markdown-to-HTML converter: Works but introduces XSS risk if content field is ever user-controlled.
- MDX: For authored static content only; chapter content is fetched dynamically from the backend.

---

## Decision 7: Locked Content — Component Not Mounted vs CSS Hidden

**Decision**: Do NOT mount `ChapterContent` component for locked chapters — render `LockedOverlay` in its place  
**Rationale**: Constitution Principle IV (Content Isolation) + FR-005 ("content MUST NOT be visible") + SC-003 ("verified by inspecting the page DOM and confirming the content field is absent"). Hiding with CSS (`opacity-0`, `blur`) still puts content in the DOM — a failing DOM inspection. The content must not reach the component tree.  
**Implementation**: After `checkAccess` returns `allowed: false`, the page renders `<LockedOverlay />` instead of `<ChapterContent content={...} />`. The raw content string is never passed to any component prop.  
**Alternatives considered**:
- CSS blur only: Fails SC-003 DOM inspection requirement.
- Fetch content but don't render it: Still leaks data to the browser; backend will 403 anyway.

---

## Decision 8: Styling — Tailwind CSS + Violet Primary

**Decision**: Tailwind CSS 3 with custom violet primary colour; `@tailwindcss/typography` for prose  
**Rationale**: Constitution mandates Tailwind CSS and no CSS-in-JS. Violet is the project's primary brand colour per the project plan. `tailwind.config.ts` extends the colour palette with `primary` → violet shades for consistent button/badge colouring.  
**Alternatives considered**:
- shadcn/ui: Pre-built components on top of Tailwind + Radix UI — accelerates development. Decision: include for Button, Card, Badge primitives to save implementation time (it uses Tailwind, not CSS-in-JS — constitution compliant).
- Mantine / Chakra UI: CSS-in-JS internally — violates constitution.

---

## Decision 9: Deployment — Vercel

**Decision**: Vercel for Next.js hosting  
**Rationale**: Constitution specifies Vercel. Zero-config Next.js deployment. Environment variables (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_API_BASE_URL`) set in Vercel dashboard.  
**Environment variables required**:
- `NEXT_PUBLIC_SUPABASE_URL` — Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` — Supabase anon/public key (safe to expose)
- `NEXT_PUBLIC_API_BASE_URL` — `https://course-companion.railway.app`

---

## Resolved: All NEEDS CLARIFICATION items

All technical unknowns resolved. No open questions remain before Phase 1 design.
