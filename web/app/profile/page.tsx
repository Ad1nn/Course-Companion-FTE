'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import Navbar from '@/components/Navbar'
import { useAuth } from '@/lib/useAuth'
import { clearSession } from '@/lib/auth'
import { getProgress, type ProgressRecord } from '@/lib/api'

const TIER_LABELS: Record<string, string> = { free: 'Free', premium: 'Premium', pro: 'Pro' }
const TIER_COLORS: Record<string, string> = {
  free: 'bg-gray-100 text-gray-600 dark:bg-slate-700 dark:text-slate-300',
  premium: 'bg-violet-100 text-violet-700 dark:bg-violet-900 dark:text-violet-300',
  pro: 'bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-300',
}

export default function ProfilePage() {
  const { session, loading } = useAuth()
  const [progress, setProgress] = useState<ProgressRecord | null>(null)
  const router = useRouter()

  useEffect(() => {
    if (!session) return
    getProgress(session.access_token, session.user_id)
      .then(setProgress)
      .catch(() => {})
  }, [session])

  if (loading || !session) return null

  function handleLogout() {
    clearSession()
    router.push('/')
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-2xl px-6 py-12">
        <h1 className="mb-8 text-3xl font-bold text-gray-900 dark:text-slate-100">Profile</h1>

        {/* Account details */}
        <div className="mb-4 rounded-2xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm">
          <h2 className="mb-4 text-xs font-semibold uppercase tracking-wide text-gray-400 dark:text-slate-500">Account</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500 dark:text-slate-400">Email</span>
              <span className="text-sm font-medium text-gray-900 dark:text-slate-200">{session.email}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500 dark:text-slate-400">Plan</span>
              <span className={`rounded-full px-3 py-0.5 text-xs font-semibold ${TIER_COLORS[session.tier]}`}>
                {TIER_LABELS[session.tier]}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500 dark:text-slate-400">User ID</span>
              <span className="font-mono text-xs text-gray-400 dark:text-slate-500">{session.user_id.slice(0, 16)}…</span>
            </div>
          </div>
        </div>

        {/* Stats */}
        {progress && (
          <div className="mb-4 rounded-2xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm">
            <h2 className="mb-4 text-xs font-semibold uppercase tracking-wide text-gray-400 dark:text-slate-500">Learning Stats</h2>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold text-violet-600 dark:text-violet-400">{progress.chapters_completed}</p>
                <p className="text-xs text-gray-500 dark:text-slate-400">Chapters Done</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-violet-600 dark:text-violet-400">{progress.streak_days}</p>
                <p className="text-xs text-gray-500 dark:text-slate-400">Day Streak</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-violet-600 dark:text-violet-400">{progress.avg_score}%</p>
                <p className="text-xs text-gray-500 dark:text-slate-400">Avg Score</p>
              </div>
            </div>
          </div>
        )}

        {/* Upgrade CTA */}
        {session.tier !== 'pro' && (
          <div className="mb-4 rounded-2xl border border-amber-200 dark:border-amber-900 bg-amber-50 dark:bg-amber-950/40 p-6">
            <h2 className="mb-1 font-semibold text-amber-900 dark:text-amber-300">
              {session.tier === 'free' ? 'Unlock all 10 chapters + AI features' : 'Unlock AI features'}
            </h2>
            <p className="mb-4 text-sm text-amber-700 dark:text-amber-400">
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

        {/* Actions */}
        <div className="flex gap-3">
          <Link href="/dashboard" className="rounded-lg border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-4 py-2 text-sm font-medium text-gray-700 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-slate-800 transition-colors">
            Dashboard
          </Link>
          <Link href="/progress" className="rounded-lg border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-4 py-2 text-sm font-medium text-gray-700 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-slate-800 transition-colors">
            View Progress
          </Link>
          <button
            onClick={handleLogout}
            className="ml-auto rounded-lg border border-red-200 dark:border-red-900 bg-white dark:bg-slate-900 px-4 py-2 text-sm font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/40 transition-colors"
          >
            Log out
          </button>
        </div>
      </main>
    </>
  )
}
