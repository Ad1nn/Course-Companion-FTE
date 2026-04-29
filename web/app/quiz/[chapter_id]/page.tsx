'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import Navbar from '@/components/Navbar'
import QuizQuestionCard from '@/components/QuizQuestion'
import { useAuth } from '@/lib/useAuth'
import { getQuizQuestions, submitAnswer, type QuizQuestion, type SubmitResult } from '@/lib/api'

interface QuizState {
  questions: QuizQuestion[]
  currentIndex: number
  selectedAnswer: 'A' | 'B' | 'C' | 'D' | null
  submitted: boolean
  result: SubmitResult | null
  finalScore: number | null
  isComplete: boolean
}

export default function QuizPage() {
  const { session, loading } = useAuth()
  const params = useParams()
  const chapterId = Number(params.chapter_id)

  const [state, setState] = useState<QuizState>({
    questions: [],
    currentIndex: 0,
    selectedAnswer: null,
    submitted: false,
    result: null,
    finalScore: null,
    isComplete: false,
  })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (!session || !chapterId) return
    getQuizQuestions(session.access_token, chapterId)
      .then((qs) => setState((s) => ({ ...s, questions: qs })))
      .catch(() => setError('Failed to load quiz questions. Please try again.'))
  }, [session, chapterId])

  async function handleSubmit() {
    if (!session || !state.selectedAnswer || submitting) return
    const q = state.questions[state.currentIndex]
    setSubmitting(true)
    try {
      const result = await submitAnswer(session.access_token, q.id, session.user_id, state.selectedAnswer)
      const isLast = state.currentIndex === state.questions.length - 1
      setState((s) => ({
        ...s,
        submitted: true,
        result,
        finalScore: result.score ?? s.finalScore,
        isComplete: isLast,
      }))
    } catch {
      setError('Failed to submit answer. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  function handleNext() {
    setState((s) => ({
      ...s,
      currentIndex: s.currentIndex + 1,
      selectedAnswer: null,
      submitted: false,
      result: null,
    }))
  }

  function handleRetake() {
    setState({
      questions: state.questions,
      currentIndex: 0,
      selectedAnswer: null,
      submitted: false,
      result: null,
      finalScore: null,
      isComplete: false,
    })
  }

  if (loading || !session) return null

  const { questions, currentIndex, selectedAnswer, submitted, result, finalScore, isComplete } = state
  const currentQuestion = questions[currentIndex]

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-2xl px-6 py-12">
        {error && (
          <p className="mb-6 rounded-lg bg-red-50 px-4 py-2 text-sm text-red-600">{error}</p>
        )}

        {questions.length === 0 && !error && (
          <div className="flex items-center justify-center py-24">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-violet-200 border-t-violet-600" />
          </div>
        )}

        {isComplete && finalScore !== null ? (
          /* Score screen */
          <div className="rounded-2xl border border-gray-200 bg-white p-10 text-center shadow-lg">
            <div className="mb-4 text-5xl">🎓</div>
            <h1 className="mb-2 text-3xl font-extrabold text-gray-900">
              {Math.round((finalScore / 100) * questions.length)} / {questions.length} Correct
            </h1>
            <p className="mb-6 text-5xl font-bold text-violet-600">{finalScore}%</p>
            <p className="mb-8 text-gray-500">
              {finalScore >= 80 ? 'Excellent work! Ready for the next chapter.' : 'Keep practising — you can retake the quiz anytime.'}
            </p>
            <div className="flex flex-col gap-3 sm:flex-row sm:justify-center">
              <Link
                href={`/chapters/${chapterId}`}
                className="rounded-lg border border-gray-300 px-6 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-50"
              >
                ← Back to Chapter
              </Link>
              <button
                onClick={handleRetake}
                className="rounded-lg bg-violet-600 px-6 py-3 text-sm font-semibold text-white hover:bg-violet-700"
              >
                Retake Quiz
              </button>
            </div>
          </div>
        ) : currentQuestion ? (
          /* Question view */
          <div className="flex flex-col items-center">
            <QuizQuestionCard
              question={currentQuestion}
              questionNumber={currentIndex + 1}
              totalQuestions={questions.length}
              selectedAnswer={selectedAnswer}
              submitted={submitted}
              result={result}
              onSelect={(key) => !submitted && setState((s) => ({ ...s, selectedAnswer: key }))}
              onSubmit={handleSubmit}
            />

            {submitted && !isComplete && (
              <button
                onClick={handleNext}
                className="mt-6 rounded-xl bg-violet-600 px-8 py-3 font-semibold text-white hover:bg-violet-700"
              >
                Next Question →
              </button>
            )}
          </div>
        ) : null}
      </main>
    </>
  )
}
