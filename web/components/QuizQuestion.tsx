import type { QuizQuestion as QuizQuestionType, SubmitResult } from '@/lib/api'
import ProgressBar from './ProgressBar'

type AnswerState = 'default' | 'selected' | 'correct' | 'wrong'

const optionKeys = ['A', 'B', 'C', 'D'] as const
type OptionKey = (typeof optionKeys)[number]

function getOptionText(q: QuizQuestionType, key: OptionKey): string {
  return q[`option_${key.toLowerCase()}` as 'option_a' | 'option_b' | 'option_c' | 'option_d']
}

function optionStyle(state: AnswerState): string {
  switch (state) {
    case 'correct': return 'border-green-500 bg-green-50 text-green-800'
    case 'wrong': return 'border-red-500 bg-red-50 text-red-800'
    case 'selected': return 'border-violet-500 bg-violet-50 text-violet-800'
    default: return 'border-gray-200 bg-white text-gray-800 hover:border-violet-400 hover:bg-violet-50'
  }
}

interface Props {
  question: QuizQuestionType
  questionNumber: number
  totalQuestions: number
  selectedAnswer: OptionKey | null
  submitted: boolean
  result: SubmitResult | null
  onSelect: (key: OptionKey) => void
  onSubmit: () => void
}

export default function QuizQuestionCard({
  question,
  questionNumber,
  totalQuestions,
  selectedAnswer,
  submitted,
  result,
  onSelect,
  onSubmit,
}: Props) {
  function getState(key: OptionKey): AnswerState {
    if (!submitted) return key === selectedAnswer ? 'selected' : 'default'
    if (result?.correct_answer === key) return 'correct'
    if (selectedAnswer === key && !result?.correct) return 'wrong'
    return 'default'
  }

  const progress = Math.round(((questionNumber - 1) / totalQuestions) * 100)

  return (
    <div className="w-full max-w-2xl">
      <div className="mb-6">
        <div className="mb-2 flex items-center justify-between text-sm text-gray-500">
          <span>Question {questionNumber} of {totalQuestions}</span>
          <span>{questionNumber - 1}/{totalQuestions} answered</span>
        </div>
        <ProgressBar value={progress} />
      </div>

      <h2 className="mb-6 text-xl font-semibold text-gray-900">{question.question}</h2>

      <div className="mb-6 space-y-3">
        {optionKeys.map((key) => (
          <button
            key={key}
            disabled={submitted}
            onClick={() => onSelect(key)}
            className={`w-full rounded-xl border-2 px-4 py-3 text-left text-sm font-medium transition-all ${optionStyle(getState(key))}`}
          >
            <span className="mr-3 font-bold">{key}.</span>
            {getOptionText(question, key)}
          </button>
        ))}
      </div>

      {result && (
        <div className={`mb-6 rounded-xl p-4 ${result.correct ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
          <p className="font-semibold mb-1">{result.correct ? '✅ Correct!' : `❌ The correct answer is ${result.correct_answer}`}</p>
          <p className="text-sm">{result.explanation}</p>
        </div>
      )}

      {!submitted && (
        <button
          onClick={onSubmit}
          disabled={!selectedAnswer}
          className="w-full rounded-xl bg-violet-600 px-6 py-3 font-semibold text-white transition-colors hover:bg-violet-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Submit Answer
        </button>
      )}
    </div>
  )
}
