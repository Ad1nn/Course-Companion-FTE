'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import Navbar from '@/components/Navbar'
import { useAuth } from '@/lib/useAuth'
import { getProgress, type ProgressRecord } from '@/lib/api'

const TIER_LABELS: Record<string, string> = { free: 'Free', premium: 'Premium', pro: 'Pro' }
const TIER_COLORS: Record<string, string> = {
  free: 'bg-gray-100 text-gray-600',
  premium: 'bg-violet-100 text-violet-700',
  pro: 'bg-amber-100 text-amber-700',
}

export default function ProfilePage() {
  const { session, loading } = useAuth()
  const [progress, setProgress] = useState<ProgressRecord | null>(null)

  useEffect(() => {
    if (!session) return
    getProgress(session.access_token, session.user_id)
      .then(setProgress)
      .catch(() => {})
  }, [session])

  if (loading || !session) return null

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-2xl px-6 py-12">
        <h1 className="mb-8 text-3xl font-bold text-gray-900">Profile</h1>

        {/* Account details */}
        <div className="mb-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-gray-400">Account</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">Email</span>
              <span className="text-sm font-medium text-gray-900">{session.email}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">Plan</span>
              <span className={`rounded-full px-3 py-0.5 text-xs font-semibold ${TIER_COLORS[session.tier]}`}>
                {TIER_LABELS[session.tier]}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">User ID</span>
              <span className="font-mono text-xs text-gray-400">{session.user_id.slice(0, 16)}…</span>
            </div>
          </div>
        </div>

        {/* Stats */}
        {progress && (
          <div className="mb-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-gray-400">Learning Stats</h2>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold text-violet-600">{progress.chapters_completed}</p>
                <p className="text-xs text-gray-500">Chapters Done</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-violet-600">{progress.streak_days}</p>
                <p className="text-xs text-gray-500">Day Streak</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-violet-600">{progress.avg_score}%</p>
                <p className="text-xs text-gray-500">Avg Score</p>
              </div>
            </div>
          </div>
        )}

        {/* Upgrade CTA */}
        {session.tier !== 'pro' && (
          <div className="mb-4 rounded-2xl border border-amber-200 bg-amber-50 p-6">
            <h2 className="mb-1 font-semibold text-amber-900">
              {session.tier === 'free' ? 'Unlock all 10 chapters + AI features' : 'Unlock AI features'}
            </h2>
            <p className="mb-4 text-sm text-amber-700">
              {session.tier === 'free'
                ? 'Upgrade to Pro for all chapters, adaptive learning path, and AI-graded assessments.'
                : 'Upgrade to Pro for adaptive learning path and AI-graded assessments.'}
            </p>
            <Link
              href={`/upgrade?tier=${session.tier === 'free' ? 'premium' : 'pro'}`}
              className="inline-block rounded-lg bg-amber-500 px-5 py-2 text-sm font-semibold text-white hover:bg-amber-600"
            >
              Upgrade Now →
            </Link>
          </div>
        )}

        {/* Quick links */}
        <div className="flex gap-3">
          <Link href="/dashboard" className="rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
            Dashboard
          </Link>
          <Link href="/progress" className="rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
            View Progress
          </Link>
        </div>
      </main>
    </>
  )
}
