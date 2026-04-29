'use client'
import { useEffect, useState } from 'react'
import Navbar from '@/components/Navbar'
import ChapterCard from '@/components/ChapterCard'
import { useAuth } from '@/lib/useAuth'
import { getChapters, getProgress, type ChapterSummary, type Tier } from '@/lib/api'

const TIER_ORDER: Record<Tier, number> = { free: 0, premium: 1, pro: 2 }

export default function ChaptersPage() {
  const { session, loading } = useAuth()
  const [chapters, setChapters] = useState<ChapterSummary[]>([])
  const [completedIds, setCompletedIds] = useState<number[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    if (!session) return
    Promise.all([
      getChapters(session.access_token),
      getProgress(session.access_token, session.user_id),
    ])
      .then(([chs, progress]) => {
        setChapters(chs)
        setCompletedIds(progress.chapters.filter((c) => c.completed).map((c) => c.chapter_id))
      })
      .catch(() => setError('Failed to load chapters. Please refresh.'))
  }, [session])

  if (loading || !session) return null

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-5xl px-6 py-10">
        <h1 className="mb-2 text-3xl font-bold text-gray-900">Course Chapters</h1>
        <p className="mb-8 text-gray-500">
          {completedIds.length} of {chapters.length} completed
        </p>

        {error && (
          <p className="mb-6 rounded-lg bg-red-50 px-4 py-2 text-sm text-red-600">{error}</p>
        )}

        <div className="grid gap-4 md:grid-cols-2">
          {chapters.map((ch) => {
            const locked = TIER_ORDER[session.tier] < TIER_ORDER[ch.tier]
            return (
              <ChapterCard
                key={ch.id}
                chapter={ch}
                completed={completedIds.includes(ch.id)}
                locked={locked}
              />
            )
          })}
        </div>
      </main>
    </>
  )
}
