const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://course-companion.railway.app'

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

async function request<T>(path: string, token: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
      ...(options?.headers || {}),
    },
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new ApiError(res.status, typeof err.detail === 'string' ? err.detail : 'Request failed')
  }
  return res.json()
}

// ── Types ──────────────────────────────────────────────────────────────────────

export type Tier = 'free' | 'premium' | 'pro'

export interface ChapterSummary {
  id: number
  title: string
  description: string
  order_num: number
  tier: Tier
}

export interface ChapterDetail extends ChapterSummary {
  content: string
}

export interface AccessResult {
  allowed: boolean
  required_tier?: Tier
  user_tier?: Tier
}

export interface QuizQuestion {
  id: number
  chapter_id: number
  question: string
  option_a: string
  option_b: string
  option_c: string
  option_d: string
  order_num: number
}

export interface SubmitResult {
  correct: boolean
  correct_answer: 'A' | 'B' | 'C' | 'D'
  explanation: string
  score?: number
}

export interface ChapterProgress {
  chapter_id: number
  title: string
  completed: boolean
  score: number | null
  attempts: number
}

export interface ProgressRecord {
  tier: Tier
  streak_days: number
  avg_score: number
  chapters_completed: number
  chapters: ChapterProgress[]
}

// ── API functions ──────────────────────────────────────────────────────────────

export async function getChapters(token: string): Promise<ChapterSummary[]> {
  return request('/chapters', token)
}

export async function checkAccess(token: string, chapterId: number): Promise<AccessResult> {
  return request(`/access/check?chapter_id=${chapterId}`, token)
}

export async function getChapter(token: string, id: number): Promise<ChapterDetail> {
  return request(`/chapters/${id}`, token)
}

export async function getQuizQuestions(token: string, chapterId: number): Promise<QuizQuestion[]> {
  return request(`/quizzes/${chapterId}`, token)
}

export async function submitAnswer(
  token: string,
  quizId: number,
  userId: string,
  answer: string,
): Promise<SubmitResult> {
  return request(`/quizzes/${quizId}/submit`, token, {
    method: 'POST',
    body: JSON.stringify({ user_id: userId, answer }),
  })
}

export async function getProgress(token: string, userId: string): Promise<ProgressRecord> {
  return request(`/progress/${userId}`, token)
}

// ── Auth endpoints (no Bearer token needed) ────────────────────────────────────

export async function apiRegister(email: string, password: string): Promise<{ user_id: string; email: string; tier: Tier }> {
  const res = await fetch(`${BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Registration failed' }))
    throw new ApiError(res.status, typeof err.detail === 'string' ? err.detail : 'Registration failed')
  }
  return res.json()
}

export async function apiLogin(email: string, password: string): Promise<{ access_token: string; user_id: string; tier: Tier }> {
  const res = await fetch(`${BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Invalid credentials' }))
    throw new ApiError(res.status, typeof err.detail === 'string' ? err.detail : 'Invalid credentials')
  }
  return res.json()
}
