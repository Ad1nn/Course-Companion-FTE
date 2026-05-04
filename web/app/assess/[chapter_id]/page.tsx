'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import Navbar from '@/components/Navbar'
import { useAuth } from '@/lib/useAuth'
import { getChapter, generateQuestion, assessAnswer, type ChapterDetail, type AssessResult } from '@/lib/api'

type Mode = 'pick' | 'ai-question' | 'free-explain'

export default function AssessPage() {
  const { session, loading } = useAuth()
  const params = useParams()
  const chapterId = Number(params.chapter_id)

  const [chapter, setChapter] = useState<ChapterDetail | null>(null)
  const [mode, setMode] = useState<Mode>('pick')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [generatingQ, setGeneratingQ] = useState(false)
  const [result, setResult] = useState<AssessResult | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!session || !chapterId) return
    getChapter(session.access_token, chapterId)
      .then(setChapter)
      .catch(() => {})
  }, [session, chapterId])

  if (loading || !session) return null

  if (session.tier !== 'pro') {
    return (
      <>
        <Navbar />
        <main className="mx-auto max-w-2xl px-6 py-20 text-center">
          <div className="rounded-2xl border border-amber-200 bg-amber-50 p-10">
            <div className="mb-4 text-5xl">🔒</div>
            <h1 className="mb-2 text-2xl font-bold text-gray-900">Pro Feature</h1>
            <p className="mb-6 text-gray-500">AI-graded assessments are available on the Pro plan.</p>
            <Link href="/upgrade?tier=pro" className="inline-block rounded-lg bg-amber-500 px-6 py-2.5 font-semibold text-white hover:bg-amber-600">
              Upgrade to Pro →
            </Link>
          </div>
        </main>
      </>
    )
  }

  async function handleGenerateQuestion() {
    if (!session) return
    setError('')
    setGeneratingQ(true)
    setQuestion('')
    try {
      const data = await generateQuestion(session.access_token, session.user_id, chapterId)
      setQuestion(data.question)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to generate question.')
    } finally {
      setGeneratingQ(false)
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!session || !answer.trim()) return
    const finalQuestion = mode === 'ai-question' ? question : `Explain the following about ${chapter?.title ?? `Chapter ${chapterId}`}: ${question || 'the key concepts'}`
    setError('')
    setSubmitting(true)
    setResult(null)
    try {
      const data = await assessAnswer(session.access_token, session.user_id, chapterId, finalQuestion, answer)
      setResult(data)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to assess answer. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  function handleRetry() {
    setResult(null)
    setAnswer('')
    if (mode === 'ai-question') setQuestion('')
  }

  const scoreColor = result
    ? result.score >= 80 ? 'text-emerald-600' : result.score >= 50 ? 'text-amber-500' : 'text-red-600'
    : ''

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-2xl px-6 py-12">
        <div className="mb-2">
          <Link href={`/chapters/${chapterId}`} className="text-sm text-violet-600 hover:text-violet-700">
            ← Back to Chapter
          </Link>
        </div>
        <h1 className="mb-1 text-3xl font-bold text-gray-900">AI Assessment</h1>
        {chapter && <p className="mb-8 text-gray-500">{chapter.title}</p>}

        {error && <p className="mb-4 rounded-lg bg-red-50 px-4 py-2 text-sm text-red-600">{error}</p>}

        {/* Result view */}
        {result ? (
          <div className="space-y-4">
            <div className="rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
              <p className="mb-1 text-sm font-semibold uppercase tracking-wide text-gray-400">Your Score</p>
              <p className={`text-6xl font-extrabold ${scoreColor}`}>{result.score}%</p>
              <p className="mt-4 text-gray-600">{result.feedback}</p>
            </div>

            {result.strengths.length > 0 && (
              <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-6">
                <h3 className="mb-3 font-semibold text-emerald-800">What you got right</h3>
                <ul className="space-y-2">
                  {result.strengths.map((s) => (
                    <li key={s} className="flex items-start gap-2 text-sm text-emerald-700">
                      <span className="mt-0.5 font-bold">✓</span> {s}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {result.areas_to_improve.length > 0 && (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
                <h3 className="mb-3 font-semibold text-amber-800">Areas to improve</h3>
                <ul className="space-y-2">
                  {result.areas_to_improve.map((a) => (
                    <li key={a} className="flex items-start gap-2 text-sm text-amber-700">
                      <span className="mt-0.5">→</span> {a}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="flex gap-3">
              <button onClick={handleRetry} className="flex-1 rounded-lg border border-gray-200 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50">
                Try Again
              </button>
              <Link href={`/chapters/${chapterId}`} className="flex-1 rounded-lg bg-violet-600 py-2.5 text-center text-sm font-semibold text-white hover:bg-violet-700">
                Back to Chapter
              </Link>
            </div>
          </div>

        /* Mode picker */
        ) : mode === 'pick' ? (
          <div className="grid gap-4 sm:grid-cols-2">
            <button
              onClick={() => { setMode('ai-question'); handleGenerateQuestion() }}
              className="rounded-2xl border-2 border-violet-200 bg-white p-6 text-left hover:border-violet-400 hover:shadow-md transition-all"
            >
              <div className="mb-3 text-3xl">🤖</div>
              <h2 className="mb-1 font-semibold text-gray-900">AI generates a question</h2>
              <p className="text-sm text-gray-500">Get a thought-provoking question about this chapter, then write your answer for AI grading.</p>
            </button>

            <button
              onClick={() => setMode('free-explain')}
              className="rounded-2xl border-2 border-gray-200 bg-white p-6 text-left hover:border-violet-400 hover:shadow-md transition-all"
            >
              <div className="mb-3 text-3xl">✍️</div>
              <h2 className="mb-1 font-semibold text-gray-900">Explain a concept</h2>
              <p className="text-sm text-gray-500">Write your own question or topic, explain it in your own words, and get AI feedback on your understanding.</p>
            </button>
          </div>

        /* AI question mode */
        ) : mode === 'ai-question' ? (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="rounded-xl border border-violet-200 bg-violet-50 p-4">
              {generatingQ ? (
                <div className="flex items-center gap-3 text-sm text-violet-600">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-violet-300 border-t-violet-600" />
                  Generating question…
                </div>
              ) : question ? (
                <div>
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-violet-500">Your question</p>
                  <p className="text-gray-800">{question}</p>
                  <button type="button" onClick={handleGenerateQuestion} className="mt-3 text-xs text-violet-600 hover:underline">
                    Generate a different question
                  </button>
                </div>
              ) : null}
            </div>

            {question && !generatingQ && (
              <>
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-700">Your answer</label>
                  <textarea
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    placeholder="Write your answer here…"
                    required
                    rows={7}
                    className="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-violet-500 focus:outline-none focus:ring-1 focus:ring-violet-500"
                  />
                </div>
                <button
                  type="submit"
                  disabled={submitting || !answer.trim()}
                  className="w-full rounded-lg bg-violet-600 py-3 font-semibold text-white hover:bg-violet-700 disabled:opacity-60"
                >
                  {submitting ? 'AI is grading…' : 'Submit for AI Grading →'}
                </button>
              </>
            )}

            <button type="button" onClick={() => { setMode('pick'); setQuestion(''); setAnswer('') }} className="w-full text-sm text-gray-400 hover:text-gray-600">
              ← Back
            </button>
          </form>

        /* Free explain mode */
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                What concept do you want to explain? <span className="text-gray-400">(optional)</span>
              </label>
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="e.g. How does tool use work in Claude agents?"
                className="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-violet-500 focus:outline-none focus:ring-1 focus:ring-violet-500"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">Your explanation</label>
              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Explain the concept in your own words…"
                required
                rows={8}
                className="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-violet-500 focus:outline-none focus:ring-1 focus:ring-violet-500"
              />
            </div>

            <button
              type="submit"
              disabled={submitting || !answer.trim()}
              className="w-full rounded-lg bg-violet-600 py-3 font-semibold text-white hover:bg-violet-700 disabled:opacity-60"
            >
              {submitting ? 'AI is assessing…' : 'Get AI Feedback →'}
            </button>

            <button type="button" onClick={() => { setMode('pick'); setAnswer('') }} className="w-full text-sm text-gray-400 hover:text-gray-600">
              ← Back
            </button>
          </form>
        )}
      </main>
    </>
  )
}
