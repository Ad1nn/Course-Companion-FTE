import Link from 'next/link'
import type { ChapterSummary } from '@/lib/api'
import TierBadge from './TierBadge'

interface ChapterCardProps {
  chapter: ChapterSummary
  completed: boolean
  locked: boolean
}

export default function ChapterCard({ chapter, completed, locked }: ChapterCardProps) {
  const inner = (
    <div
      className={`rounded-xl border bg-white p-6 shadow-sm transition-shadow ${
        locked ? 'opacity-60' : 'hover:shadow-md cursor-pointer'
      }`}
    >
      <div className="mb-2 flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wide text-gray-400">
          Chapter {chapter.order_num}
        </span>
        <div className="flex items-center gap-2">
          <TierBadge tier={chapter.tier} />
          {completed && <span title="Completed">✅</span>}
          {locked && !completed && <span title="Locked">🔒</span>}
        </div>
      </div>
      <h3 className="mb-1 text-lg font-semibold text-gray-900">{chapter.title}</h3>
      <p className="text-sm text-gray-500 line-clamp-2">{chapter.description}</p>
    </div>
  )

  if (locked) return <div>{inner}</div>
  return <Link href={`/chapters/${chapter.id}`}>{inner}</Link>
}
