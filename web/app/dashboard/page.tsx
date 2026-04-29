'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import Navbar from '@/components/Navbar'
import StatCard from '@/components/StatCard'
import { useAuth } from '@/lib/useAuth'
import { getProgress, type ProgressRecord, type Tier } from '@/lib/api'

const TIER_ORDER: Record<Tier, number> = { free: 0, premium: 1, pro: 2 }

const CHAPTER_TIERS: Record<number, Tier> = {
  1: 'free', 2: 'free', 3: 'free',
  4: 'premium', 5: 'premium', 6: 'premium', 7: 'premium',
  8: 'pro', 9: 'pro', 10: 'pro',
}

const CHAPTER_TITLES: Record<number, string> = {
  1: 'Introduction to AI Agents',
  2: 'OpenAI Agents SDK',
  3: 'Anthropic Claude Agent SDK',
  4: 'MCP Fundamentals',
  5: 'Advanced MCP Server Development',
  6: 'Agent Skills & MCP Code Execution',
  7: 'FastAPI for Agents',
  8: 'Vector Databases & RAG',
  9: 'Multi-Agent Reliability',
  10: 'Evals — Measuring Agent Performance',
}

export default function DashboardPage() {
  const { session, loading } = useAuth()
  const [progress, setProgress] = useState<ProgressRecord | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!session) return
    getProgress(session.access_token, session.user_id)
      .then(setProgress)
      .catch(() => setError('Failed to load progress.'))
  }, [session])

  if (loading || !session) return null

  // Find the next chapter to continue: first incomplete accessible chapter
  const continueChapterId = progress
    ? (() => {
        const completedIds = new Set(progress.chapters.filter((c) => c.completed).map((c) => c.chapter_id))
        for (let i = 1; i <= 10; i++) {
          const chTier = CHAPTER_TIERS[i] ?? 'free'
          if (TIER_ORDER[progress.tier] >= TIER_ORDER[chTier] && !completedIds.has(i)) {
            return i
          }
        }
        return null
      })()
    : null

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-4xl px-6 py-10">
        {/* Welcome */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back{session.email ? `, ${session.email.split('@')[0]}` : ''}! 👋
          </h1>
          <p className="mt-1 text-gray-500">Here&apos;s where you stand today.</p>
        </div>

        {error && (
          <p className="mb-6 rounded-lg bg-red-50 px-4 py-2 text-sm text-red-600">{error}</p>
        )}

        {/* Stat cards */}
        <div className="mb-8 grid gap-4 md:grid-cols-3">
          <StatCard
            label="Chapters Completed"
            value={`${progress?.chapters_completed ?? 0} / 10`}
            icon="📚"
          />
          <StatCard
            label="Day Streak"
            value={`${progress?.streak_days ?? 0} days`}
            icon="🔥"
          />
          <StatCard
            label="Average Score"
            value={`${progress?.avg_score ?? 0}%`}
            icon="📊"
          />
        </div>

        {/* Continue / Start card */}
        <div className="rounded-2xl border border-violet-200 bg-violet-50 p-8">
          {continueChapterId ? (
            <>
              <p className="mb-1 text-sm font-semibold uppercase tracking-wide text-violet-500">Continue Learning</p>
              <h2 className="mb-4 text-2xl font-bold text-gray-900">
                {CHAPTER_TITLES[continueChapterId] ?? `Chapter ${continueChapterId}`}
              </h2>
              <Link
                href={`/chapters/${continueChapterId}`}
                className="inline-block rounded-xl bg-violet-600 px-6 py-3 font-semibold text-white hover:bg-violet-700"
              >
                Continue →
              </Link>
            </>
          ) : (
            <>
              <p className="mb-1 text-sm font-semibold uppercase tracking-wide text-violet-500">Get Started</p>
              <h2 className="mb-4 text-2xl font-bold text-gray-900">Introduction to AI Agents</h2>
              <Link
                href="/chapters/1"
                className="inline-block rounded-xl bg-violet-600 px-6 py-3 font-semibold text-white hover:bg-violet-700"
              >
                Start with Chapter 1 →
              </Link>
            </>
          )}
        </div>

        {/* Quick links */}
        <div className="mt-8 flex gap-4">
          <Link
            href="/chapters"
            className="rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            All Chapters →
          </Link>
          <Link
            href="/progress"
            className="rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            View Progress →
          </Link>
        </div>
      </main>
    </>
  )
}
