'use client'
import { useEffect, useState } from 'react'
import Navbar from '@/components/Navbar'
import ProgressBar from '@/components/ProgressBar'
import TierBadge from '@/components/TierBadge'
import StatCard from '@/components/StatCard'
import { useAuth } from '@/lib/useAuth'
import { getProgress, type ProgressRecord, type Tier } from '@/lib/api'

const TIER_ORDER: Record<Tier, number> = { free: 0, premium: 1, pro: 2 }

// All 10 chapters with their required tier
const CHAPTER_TIERS: Record<number, Tier> = {
  1: 'free', 2: 'free', 3: 'free',
  4: 'premium', 5: 'premium', 6: 'premium', 7: 'premium',
  8: 'pro', 9: 'pro', 10: 'pro',
}

export default function ProgressPage() {
  const { session, loading } = useAuth()
  const [progress, setProgress] = useState<ProgressRecord | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!session) return
    getProgress(session.access_token, session.user_id)
      .then(setProgress)
      .catch(() => setError('Failed to load progress. Please refresh.'))
  }, [session])

  if (loading || !session) return null

  const completionPct = progress ? Math.round((progress.chapters_completed / 10) * 100) : 0

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-4xl px-6 py-10">
        <h1 className="mb-2 text-3xl font-bold text-gray-900">Your Progress</h1>
        <p className="mb-8 text-gray-500">Track your learning journey across all 10 chapters.</p>

        {error && (
          <p className="mb-6 rounded-lg bg-red-50 px-4 py-2 text-sm text-red-600">{error}</p>
        )}

        {progress && (
          <>
            {/* Overall stats */}
            <div className="mb-8 grid gap-4 md:grid-cols-3">
              <StatCard
                label="Chapters Completed"
                value={`${progress.chapters_completed} / 10`}
                icon="📚"
              />
              <StatCard
                label="Day Streak"
                value={`${progress.streak_days} days`}
                icon="🔥"
              />
              <StatCard
                label="Average Score"
                value={`${progress.avg_score}%`}
                icon="📊"
              />
            </div>

            <div className="mb-8">
              <ProgressBar value={completionPct} label="Overall Completion" />
            </div>

            {/* Per-chapter table */}
            <div className="rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden">
              <table className="w-full text-sm">
                <thead className="border-b border-gray-200 bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left font-semibold text-gray-600">Chapter</th>
                    <th className="px-4 py-3 text-left font-semibold text-gray-600">Tier</th>
                    <th className="px-4 py-3 text-left font-semibold text-gray-600">Status</th>
                    <th className="px-4 py-3 text-left font-semibold text-gray-600">Score</th>
                    <th className="px-4 py-3 text-left font-semibold text-gray-600">Attempts</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {Array.from({ length: 10 }, (_, i) => i + 1).map((chId) => {
                    const chProgress = progress.chapters.find((c) => c.chapter_id === chId)
                    const chTier = CHAPTER_TIERS[chId] ?? 'free'
                    const isLocked = TIER_ORDER[progress.tier] < TIER_ORDER[chTier]
                    const isCompleted = chProgress?.completed ?? false
                    const score = chProgress?.score ?? null
                    const attempts = chProgress?.attempts ?? 0

                    return (
                      <tr key={chId} className="hover:bg-gray-50">
                        <td className="px-4 py-3 font-medium text-gray-900">
                          {chProgress?.title || `Chapter ${chId}`}
                        </td>
                        <td className="px-4 py-3">
                          <TierBadge tier={chTier} />
                        </td>
                        <td className="px-4 py-3">
                          {isLocked ? (
                            <span className="text-gray-400">🔒 Locked</span>
                          ) : isCompleted ? (
                            <span className="font-medium text-green-600">✅ Completed</span>
                          ) : (
                            <span className="text-gray-400">— Not started</span>
                          )}
                        </td>
                        <td className="px-4 py-3 text-gray-700">
                          {score !== null ? `${score}%` : '—'}
                        </td>
                        <td className="px-4 py-3 text-gray-500">{attempts || '—'}</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </>
        )}

        {!progress && !error && (
          <div className="flex items-center justify-center py-24">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-violet-200 border-t-violet-600" />
          </div>
        )}
      </main>
    </>
  )
}
