-- Course Companion FTE — Database Schema
-- Run this in Supabase Dashboard → SQL Editor

-- 1. chapters
CREATE TABLE IF NOT EXISTS public.chapters (
    id          integer PRIMARY KEY,
    title       text    NOT NULL,
    description text,
    content     text    NOT NULL,
    order_num   integer NOT NULL UNIQUE,
    tier        text    NOT NULL DEFAULT 'free'
);

-- 2. quizzes
CREATE TABLE IF NOT EXISTS public.quizzes (
    id             integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    chapter_id     integer NOT NULL REFERENCES public.chapters(id) ON DELETE CASCADE,
    question       text    NOT NULL,
    option_a       text    NOT NULL,
    option_b       text    NOT NULL,
    option_c       text    NOT NULL,
    option_d       text    NOT NULL,
    correct_answer text    NOT NULL,
    explanation    text    NOT NULL,
    order_num      integer
);

-- 3. users  (links to Supabase Auth)
CREATE TABLE IF NOT EXISTS public.users (
    id         uuid        PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email      text        NOT NULL,
    tier       text        NOT NULL DEFAULT 'free',
    created_at timestamptz NOT NULL DEFAULT now()
);

-- 4. progress
CREATE TABLE IF NOT EXISTS public.progress (
    id            integer     PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id       uuid        NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    chapter_id    integer     NOT NULL REFERENCES public.chapters(id) ON DELETE CASCADE,
    completed     boolean     NOT NULL DEFAULT false,
    score         integer,
    attempts      integer     NOT NULL DEFAULT 0,
    last_accessed timestamptz NOT NULL DEFAULT now(),
    completed_at  timestamptz,
    UNIQUE (user_id, chapter_id)
);

-- 5. llm_costs  (Phase 5 placeholder)
CREATE TABLE IF NOT EXISTS public.llm_costs (
    id         integer        PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id    uuid           NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    feature    text,
    tokens_in  integer,
    tokens_out integer,
    cost_usd   numeric(10,6),
    created_at timestamptz    NOT NULL DEFAULT now()
);

-- Enable RLS on all tables (service role bypasses automatically)
ALTER TABLE public.chapters  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quizzes   ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.users     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.progress  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.llm_costs ENABLE ROW LEVEL SECURITY;
