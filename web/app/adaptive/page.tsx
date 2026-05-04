'use client'
import { useState } from 'react'
import Link from 'next/link'
import Navbar from '@/components/Navbar'
import { useAuth } from '@/lib/useAuth'
import { getAdaptivePath, type AdaptivePathResult } from '@/lib/api'

export default function AdaptivePage() {
  const { session, loading } = useAuth()
  const [result, setResult] = useState<AdaptivePathResult | null>(null)
  const [thinking, setThinking] = useState(false)
  const [error, setError] = useState('')

  if (loading || !session) return null

  if (session.tier !== 'pro') {
    return (
      <>
        <Navbar />
        <main className="mx-auto max-w-2xl px-6 py-20 text-center">
          <div className="rounded-2xl border border-amber-200 bg-amber-50 p-10">
            <div className="mb-4 text-5xl">🔒</div>
            <h1 className="mb-2 text-2xl font-bold text-gray-900">Pro Feature</h1>
            <p className="mb-6 text-gray-500">Adaptive learning path is available on the Pro plan.</p>
            <Link
              href="/upgrade?tier=pro"
              className="inline-block rounded-lg bg-amber-500 px-6 py-2.5 font-semibold text-white hover:bg-amber-600"
            >
              Upgrade to Pro →
            </Link>
          </div>
        </main>
      </>
    )
  }

  async function handleAnalyse() {
    if (!session) return
    setError('')
    setThinking(true)
    setResult(null)
    try {
      const data = await getAdaptivePath(session.access_token, session.user_id)
      setResult(data)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to get recommendation. Please try again.')
    } finally {
      setThinking(false)
    }
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-2xl px-6 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Adaptive Learning Path</h1>
          <p className="mt-2 text-gray-500">
            AI analyses your progress and tells you exactly what to study next.
          </p>
        </div>

        {!result && !thinking && (
          <div className="rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
            <div className="mb-4 text-5xl">🤖</div>
            <h2 className="mb-2 text-xl font-semibold text-gray-900">Ready to analyse your progress</h2>
            <p className="mb-6 text-gray-500 text-sm">
              GPT-4o will review your completed chapters, quiz scores, and weak areas to recommend your next step.
            </p>
            <button
              onClick={handleAnalyse}
              className="rounded-lg bg-violet-600 px-8 py-3 font-semibold text-white hover:bg-violet-700"
            >
              Analyse My Progress →
            </button>
          </div>
        )}

        {thinking && (
          <div className="flex flex-col items-center justify-center py-24 gap-4">
            <div className="h-10 w-10 animate-spin rounded-full border-4 border-violet-200 border-t-violet-600" />
            <p className="text-sm text-gray-500">AI is analysing your progress…</p>
          </div>
        )}

        {error && (
          <p className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600">{error}</p>
        )}

        {result && (
          <div className="space-y-4">
            {/* Main recommendation */}
            <div className="rounded-2xl border-2 border-violet-200 bg-violet-50 p-8">
              <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-violet-500">Recommended Next</p>
              <h2 className="mb-3 text-2xl font-bold text-gray-900">Chapter {result.recommended_next_chapter_id}</h2>
              <p className="mb-6 text-gray-600">{result.reasoning}</p>
              <div className="flex items-center gap-4">
                <Link
                  href={`/chapters/${result.recommended_next_chapter_id}`}
                  className="rounded-lg bg-violet-600 px-6 py-2.5 font-semibold text-white hover:bg-violet-700"
                >
                  Go to Chapter →
                </Link>
                <span className="text-sm text-gray-500">
                  ⏱ ~{result.estimated_study_time_minutes} min
                </span>
              </div>
            </div>

            {/* Weak areas */}
            {result.weak_areas.length > 0 && (
              <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                <h3 className="mb-3 font-semibold text-gray-900">Areas to Strengthen</h3>
                <ul className="space-y-2">
                  {result.weak_areas.map((area) => (
                    <li key={area} className="flex items-start gap-2 text-sm text-gray-600">
                      <span className="mt-0.5 text-amber-500">⚠</span> {area}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Re-analyse */}
            <button
              onClick={handleAnalyse}
              className="w-full rounded-lg border border-gray-200 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50"
            >
              Re-analyse
            </button>
          </div>
        )}
      </main>
    </>
  )
}
