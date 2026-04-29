import Link from 'next/link'
import type { ChapterSummary, Tier } from '@/lib/api'
import TierBadge from './TierBadge'

const TIER_ORDER: Record<Tier, number> = { free: 0, premium: 1, pro: 2 }

interface SidebarProps {
  chapters: ChapterSummary[]
  currentId: number
  completedIds: number[]
  userTier: Tier
}

export default function Sidebar({ chapters, currentId, completedIds, userTier }: SidebarProps) {
  return (
    <aside className="w-72 flex-shrink-0 rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
      <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-gray-400">Chapters</h2>
      <ul className="space-y-1">
        {chapters.map((ch) => {
          const isLocked = TIER_ORDER[userTier] < TIER_ORDER[ch.tier]
          const isCurrent = ch.id === currentId
          const isDone = completedIds.includes(ch.id)

          const base = 'flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors'
          const active = isCurrent ? 'bg-violet-100 font-semibold text-violet-800' : ''
          const locked = isLocked ? 'cursor-not-allowed text-gray-400' : 'text-gray-700 hover:bg-gray-100'

          const content = (
            <>
              <span className="w-5 text-center text-xs font-medium text-gray-400">{ch.order_num}</span>
              <span className="flex-1 truncate">{ch.title}</span>
              {isDone && <span>✅</span>}
              {isLocked && !isDone && <span>🔒</span>}
              {!isDone && !isLocked && isCurrent && (
                <TierBadge tier={ch.tier} />
              )}
            </>
          )

          if (isLocked) {
            return (
              <li key={ch.id}>
                <div className={`${base} ${locked}`}>{content}</div>
              </li>
            )
          }

          return (
            <li key={ch.id}>
              <Link href={`/chapters/${ch.id}`} className={`${base} ${active || locked}`}>
                {content}
              </Link>
            </li>
          )
        })}
      </ul>
    </aside>
  )
}
