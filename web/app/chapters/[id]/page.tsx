'use client'
import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import ReactMarkdown from 'react-markdown'
import Navbar from '@/components/Navbar'
import Sidebar from '@/components/Sidebar'
import LockedOverlay from '@/components/LockedOverlay'
import { useAuth } from '@/lib/useAuth'
import {
  getChapters,
  checkAccess,
  getChapter,
  getProgress,
  type ChapterSummary,
  type ChapterDetail,
  type Tier,
} from '@/lib/api'

const TIER_ORDER: Record<Tier, number> = { free: 0, premium: 1, pro: 2 }

export default function ChapterPage() {
  const { session, loading } = useAuth()
  const params = useParams()
  const router = useRouter()
  const chapterId = Number(params.id)

  const [allChapters, setAllChapters] = useState<ChapterSummary[]>([])
  const [completedIds, setCompletedIds] = useState<number[]>([])
  const [chapter, setChapter] = useState<ChapterDetail | null>(null)
  const [lockedTier, setLockedTier] = useState<string | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!session || !chapterId) return

    async function load() {
      try {
        const [allChs, access] = await Promise.all([
          getChapters(session!.access_token),
          checkAccess(session!.access_token, chapterId),
        ])
        setAllChapters(allChs)

        if (!access.allowed) {
          setLockedTier(access.required_tier || 'premium')
          return
        }
        const ch = await getChapter(session!.access_token, chapterId)
        setChapter(ch)
      } catch {
        setError('Failed to load chapter. Please try again.')
      }

      // Progress is optional — load separately so it never blocks content
      getProgress(session!.access_token, session!.user_id)
        .then((p) => setCompletedIds(p.chapters.filter((c) => c.completed).map((c) => c.chapter_id)))
        .catch(() => {/* sidebar checkmarks unavailable — not critical */})
    }

    load()
  }, [session, chapterId])

  if (loading || !session) return null

  const currentChapter = allChapters.find((c) => c.id === chapterId)
  const prevChapter = allChapters.find((c) => c.order_num === (currentChapter?.order_num ?? 0) - 1)
  const nextChapter = allChapters.find((c) => c.order_num === (currentChapter?.order_num ?? 0) + 1)

  return (
    <>
      <Navbar />
      <div className="mx-auto flex max-w-6xl gap-8 px-6 py-10">
        {/* Sidebar */}
        {allChapters.length > 0 && (
          <Sidebar
            chapters={allChapters}
            currentId={chapterId}
            completedIds={completedIds}
            userTier={session.tier}
          />
        )}

        {/* Main content */}
        <main className="flex-1">
          {error && (
            <p className="mb-6 rounded-lg bg-red-50 px-4 py-2 text-sm text-red-600">{error}</p>
          )}

          {lockedTier ? (
            <LockedOverlay requiredTier={lockedTier} />
          ) : chapter ? (
            <>
              <div className="mb-6">
                <h1 className="text-3xl font-bold text-gray-900">{chapter.title}</h1>
                <p className="mt-2 text-gray-500">{chapter.description}</p>
              </div>

              <article className="prose prose-violet max-w-none rounded-xl border border-gray-200 bg-white p-8">
                <ReactMarkdown>{chapter.content}</ReactMarkdown>
              </article>

              {/* Navigation */}
              <div className="mt-8 flex items-center justify-between">
                <div>
                  {prevChapter && (
                    <Link
                      href={`/chapters/${prevChapter.id}`}
                      className="rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                    >
                      ← {prevChapter.title}
                    </Link>
                  )}
                </div>
                <div className="flex gap-3">
                  <Link
                    href={`/quiz/${chapterId}`}
                    className="rounded-lg bg-violet-600 px-5 py-2 text-sm font-semibold text-white hover:bg-violet-700"
                  >
                    Start Quiz →
                  </Link>
                  {nextChapter && TIER_ORDER[session.tier] >= TIER_ORDER[nextChapter.tier] && (
                    <Link
                      href={`/chapters/${nextChapter.id}`}
                      className="rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                    >
                      Next Chapter →
                    </Link>
                  )}
                </div>
              </div>
            </>
          ) : (
            !error && (
              <div className="flex items-center justify-center py-24">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-violet-200 border-t-violet-600" />
              </div>
            )
          )}
        </main>
      </div>
    </>
  )
}
